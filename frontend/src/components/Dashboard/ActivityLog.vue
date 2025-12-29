<!-- frontend/src/components/Dashboard/ActivityLog.vue -->
<template>
  <div class="activity-log-container">
    <!-- Header -->
    <div class="section-header">
      <div class="header-content">
        <h2>Registro de Actividad</h2>
        <p class="section-subtitle">Historial completo de tus acciones en el sistema</p>
      </div>

      <!-- Stats Summary -->
      <div v-if="summary" class="stats-summary">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #10b981, #059669)">
            <va-icon name="trending_up" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-label">Últimos 7 días</span>
            <span class="stat-value">{{ summary.recentActions }}</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6, #2563eb)">
            <va-icon name="check_circle" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-label">Total acciones</span>
            <span class="stat-value">{{ summary.totalActions }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="search-box">
        <va-icon name="search" />
        <va-input
          v-model="searchQuery"
          placeholder="Buscar en actividades..."
          type="text"
          clearable
          class="search-input"
        />
      </div>

      <div class="filter-controls">
        <va-select
          v-model="actionFilter"
          :options="actionOptions"
          text-by="text"
          value-by="value"
          placeholder="Filtrar por acción"
          clearable
          class="filter-select"
        />

        <va-select
          v-model="severityFilter"
          :options="severityOptions"
          text-by="text"
          value-by="value"
          placeholder="Filtrar por severidad"
          clearable
          class="filter-select"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
      <p>Cargando registro de actividad...</p>
    </div>

    <!-- Activity Timeline -->
    <div v-else-if="filteredLogs.length > 0" class="activity-timeline">
      <div
        v-for="log in filteredLogs"
        :key="log.id"
        class="timeline-item"
        :class="`severity-${log.severity}`"
      >
        <div class="timeline-marker" :class="`marker-${log.severity}`">
          <va-icon :name="getActionIcon(log.action)" size="small" />
        </div>

        <div class="timeline-content">
          <div class="content-header">
            <div class="header-left">
              <h3 class="action-title">
                {{ log.actionDisplay }}
                <span class="object-type">{{ log.objectTypeDisplay }}</span>
              </h3>
              <p class="object-name">{{ log.objectRepr }}</p>
            </div>

            <div class="header-right">
              <span class="timestamp">{{ formatTimestamp(log.timestamp) }}</span>
              <span class="severity-badge" :class="`badge-${log.severity}`">
                {{ log.severityDisplay }}
              </span>
            </div>
          </div>

          <p v-if="log.description" class="action-description">{{ log.description }}</p>

          <!-- Changes Details -->
          <div v-if="log.changes && Object.keys(log.changes).length > 0" class="changes-section">
            <button class="toggle-changes-btn" @click="toggleChanges(log.id)">
              <va-icon :name="expandedLogs.includes(log.id) ? 'expand_less' : 'expand_more'" size="small" />
              <span>{{ expandedLogs.includes(log.id) ? 'Ocultar' : 'Ver' }} cambios</span>
            </button>

            <div v-if="expandedLogs.includes(log.id)" class="changes-details">
              <div v-for="(change, field) in log.changes" :key="field" class="change-item">
                <span class="field-name">{{ field }}:</span>
                <div class="change-values">
                  <span class="old-value">"{{ change.old }}"</span>
                  <va-icon name="arrow_forward" size="small" class="arrow-icon" />
                  <span class="new-value">"{{ change.new }}"</span>
                </div>
              </div>
            </div>
          </div>

          <!-- IP Address (para admin/debugging) -->
          <div v-if="log.ipAddress" class="meta-info">
            <va-icon name="computer" size="small" />
            <span>IP: {{ log.ipAddress }}</span>
          </div>
        </div>
      </div>

      <!-- Load More Button -->
      <div v-if="hasMore" class="load-more-section">
        <button class="load-more-btn" @click="loadMore" :disabled="loading">
          <va-icon name="expand_more" />
          Cargar más actividades
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <va-icon name="history" size="4rem" color="#ccc" />
      <h3>No hay actividad registrada</h3>
      <p>Aún no has realizado ninguna acción en el sistema</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useToast } from 'vuestic-ui'
import { useAuthStore } from '@/stores/useAuthStore'

// ========== STORES ==========
const authStore = useAuthStore()
const { init: notify } = useToast()

// ========== DATA ==========
const loading = ref(false)
const logs = ref([])
const summary = ref(null)
const searchQuery = ref('')
const actionFilter = ref('')
const severityFilter = ref('')
const expandedLogs = ref([])
const offset = ref(0)
const limit = 50
const totalLogs = ref(0)

const actionOptions = [
  { text: 'Creado', value: 'create' },
  { text: 'Actualizado', value: 'update' },
  { text: 'Eliminado', value: 'delete' },
  { text: 'Pausado', value: 'pause' },
  { text: 'Activado', value: 'activate' },
  { text: 'Cerrado', value: 'close' },
  { text: 'Pago Verificado', value: 'verify_payment' },
  { text: 'Intento de Aplicación Bloqueado', value: 'block_attempt' },
  { text: 'Visualizado', value: 'view' },
  { text: 'Exportado', value: 'export' }
]

const severityOptions = [
  { text: 'Información', value: 'info' },
  { text: 'Advertencia', value: 'warning' },
  { text: 'Crítico', value: 'critical' }
]

// ========== LIFECYCLE ==========
onMounted(async () => {
  await loadSummary()
  await loadLogs()
})

// ========== COMPUTED PROPERTIES ==========
const hasMore = computed(() => logs.value.length < totalLogs.value)

const filteredLogs = computed(() => {
  if (!searchQuery.value) return logs.value

  const query = searchQuery.value.toLowerCase()
  return logs.value.filter(log =>
    log.objectRepr.toLowerCase().includes(query) ||
    log.actionDisplay.toLowerCase().includes(query) ||
    log.objectTypeDisplay.toLowerCase().includes(query) ||
    (log.description && log.description.toLowerCase().includes(query))
  )
})

// ========== METHODS ==========
const loadLogs = async (reset = true) => {
  try {
    if (reset) {
      offset.value = 0
      logs.value = []
    }

    loading.value = true

    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.value.toString()
    })

    if (actionFilter.value) {
      params.append('action', actionFilter.value)
    }

    if (severityFilter.value) {
      params.append('severity', severityFilter.value)
    }

    const response = await fetch(`http://localhost:8000/api/audit/my-activity?${params}`, {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        if (reset) {
          logs.value = data.logs
        } else {
          logs.value = [...logs.value, ...data.logs]
        }
        totalLogs.value = data.total
      } else {
        notify({
          message: `Error: ${data.message}`,
          color: 'danger'
        })
      }
    } else {
      notify({
        message: 'Error al cargar el registro de actividad',
        color: 'danger'
      })
    }
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger'
    })
  } finally {
    loading.value = false
  }
}

const loadSummary = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/audit/my-summary', {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        summary.value = data.summary
      }
    }
  } catch (err) {
    console.error('Error al cargar resumen:', err)
  }
}

const loadMore = async () => {
  offset.value += limit
  await loadLogs(false)
}

const toggleChanges = (logId) => {
  const index = expandedLogs.value.indexOf(logId)
  if (index > -1) {
    expandedLogs.value.splice(index, 1)
  } else {
    expandedLogs.value.push(logId)
  }
}

const getActionIcon = (action) => {
  const icons = {
    'create': 'add_circle',
    'update': 'edit',
    'delete': 'delete',
    'soft_delete': 'delete_outline',
    'pause': 'pause',
    'activate': 'play_arrow',
    'close': 'close',
    'verify_payment': 'check_circle',
    'reject_payment': 'cancel',
    'block_attempt': 'block',
    'view': 'visibility',
    'export': 'download'
  }
  return icons[action] || 'label'
}

const formatTimestamp = (isoString) => {
  const date = new Date(isoString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Hace un momento'
  if (diffMins < 60) return `Hace ${diffMins} min`
  if (diffHours < 24) return `Hace ${diffHours} h`
  if (diffDays < 7) return `Hace ${diffDays} días`

  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// ========== WATCHERS ==========
// Recargar logs cuando cambian los filtros
watch([actionFilter, severityFilter], () => {
  loadLogs(true)
})
</script>

<style scoped>
.activity-log-container {
  padding: 0;
}

/* ========== HEADER ========== */
.section-header {
  margin-bottom: 2rem;
}

.header-content h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.5rem;
}

.section-subtitle {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
}

/* ========== STATS SUMMARY ========== */
.stats-summary {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  flex: 1;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.85rem;
  color: #666;
  font-weight: 500;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a1a;
}

/* ========== FILTER BAR ========== */
.filter-bar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  transition: all 0.2s;
}

.search-box:focus-within {
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.search-box .va-icon {
  color: #999;
  flex-shrink: 0;
}

.search-input {
  width: 100%;
  border: none !important;
  padding: 0 !important;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select {
  flex: 1;
  min-width: 200px;
}

/* ========== LOADING STATE ========== */
.loading-state {
  text-align: center;
  padding: 3rem 2rem;
  background: white;
  border-radius: 12px;
}

.loading-state p {
  margin-top: 1rem;
  color: #666;
}

/* ========== ACTIVITY TIMELINE ========== */
.activity-timeline {
  position: relative;
}

.timeline-item {
  position: relative;
  display: flex;
  gap: 1.5rem;
  padding-bottom: 2rem;
}

.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 44px;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #e0e0e0 0%, transparent 100%);
}

.timeline-marker {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  z-index: 1;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.marker-info {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.marker-warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.marker-critical {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.timeline-content {
  flex: 1;
  background: white;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  padding: 1.5rem;
  transition: all 0.3s;
}

.timeline-content:hover {
  border-color: #e0e0e0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.header-left {
  flex: 1;
}

.action-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 0.25rem;
}

.object-type {
  font-weight: 400;
  color: #7c3aed;
  margin-left: 0.5rem;
}

.object-name {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.timestamp {
  font-size: 0.85rem;
  color: #999;
}

.severity-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-info {
  background: #dbeafe;
  color: #1e40af;
}

.badge-warning {
  background: #fef3c7;
  color: #92400e;
}

.badge-critical {
  background: #fee2e2;
  color: #991b1b;
}

.action-description {
  color: #666;
  font-size: 0.9rem;
  margin: 0.75rem 0;
  line-height: 1.5;
}

/* ========== CHANGES SECTION ========== */
.changes-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f5f5f5;
}

.toggle-changes-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  color: #666;
  transition: all 0.2s;
}

.toggle-changes-btn:hover {
  background: #f0f0f0;
  color: #1a1a1a;
}

.changes-details {
  margin-top: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
}

.change-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.change-item:last-child {
  border-bottom: none;
}

.field-name {
  font-weight: 600;
  color: #374151;
  font-size: 0.85rem;
  text-transform: capitalize;
}

.change-values {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
}

.old-value {
  color: #ef4444;
  text-decoration: line-through;
}

.arrow-icon {
  color: #9ca3af;
}

.new-value {
  color: #10b981;
  font-weight: 500;
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f5f5f5;
  font-size: 0.85rem;
  color: #999;
}

/* ========== LOAD MORE ========== */
.load-more-section {
  text-align: center;
  margin-top: 2rem;
}

.load-more-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  color: #666;
  transition: all 0.3s ease;
}

.load-more-btn:hover:not(:disabled) {
  border-color: #7c3aed;
  color: #7c3aed;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.2);
}

.load-more-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  border: 1px dashed #e0e0e0;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 1rem 0 0.5rem;
}

.empty-state p {
  color: #666;
  margin-bottom: 0;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .stats-summary {
    flex-direction: column;
  }

  .filter-controls {
    flex-direction: column;
  }

  .filter-select {
    min-width: auto;
  }

  .content-header {
    flex-direction: column;
  }

  .header-right {
    align-items: flex-start;
  }

  .timeline-item {
    gap: 1rem;
  }

  .timeline-marker {
    width: 36px;
    height: 36px;
  }

  .timeline-item:not(:last-child)::before {
    left: 18px;
  }
}
</style>
