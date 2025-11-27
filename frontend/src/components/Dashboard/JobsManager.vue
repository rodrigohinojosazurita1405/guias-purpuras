<!-- frontend/src/components/Dashboard/JobsManager.vue -->
<template>
  <div class="jobs-manager">
    <!-- Job Detail Modal -->
    <JobDetailModal
      :visible="showDetailModal"
      :job="selectedJob || {}"
      @close="showDetailModal = false"
      @deactivate-job="deactivateJob"
      @activate-job="activateJob"
    />
    <!-- Header -->
    <div class="manager-header">
      <h1>Administrador Anuncios</h1>
      <router-link to="/publicar" class="publish-btn-new">
        <va-icon name="add_circle" />
        Publicar Nuevo
      </router-link>
    </div>

    <!-- Filters & Search -->
    <div class="filter-bar">
      <div class="search-box">
        <va-icon name="search" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar trabajos..."
          class="search-input"
        />
      </div>

      <div class="filter-controls">
        <select v-model="filterStatus" class="filter-select">
          <option value="">Todos los estados</option>
          <option value="active">Activos</option>
          <option value="closed">Cerrados</option>
          <option value="draft">Borradores</option>
        </select>

        <select v-model="sortBy" class="filter-select">
          <option value="recent">Más recientes</option>
          <option value="views">Más vistas</option>
          <option value="applications">Más aplicaciones</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
      <p>Cargando trabajos...</p>
    </div>

    <!-- Jobs List -->
    <div v-else-if="filteredJobs.length > 0" class="jobs-list">
      <div v-for="job in filteredJobs" :key="job.id" class="job-card">
        <!-- Card Header -->
        <div class="job-card-header">
          <div class="job-info">
            <h3 class="job-title">{{ job.title }}</h3>
            <p class="job-company">{{ job.companyName }}</p>
          </div>
          <div class="job-badge" :class="job.status">
            {{ statusLabel(job.status) }}
          </div>
        </div>

        <!-- Card Stats -->
        <div class="job-stats">
          <div class="stat-item">
            <va-icon name="visibility" />
            <span class="stat-text">{{ job.views }}</span>
          </div>
          <div class="stat-item">
            <va-icon name="people" />
            <span class="stat-text">{{ job.applications }}</span>
          </div>
          <div class="stat-item plan-stat">
            <va-icon name="card_giftcard" />
            <span class="stat-text plan-badge" :class="`plan-${job.selectedPlan}`">
              {{ formatPlanName(job.selectedPlan, job.planLabel) }}
            </span>
          </div>
          <div class="stat-divider">|</div>
          <div class="stat-item">
            <va-icon name="schedule" />
            <span class="stat-text stat-date">{{ formatExactDateTime(job.createdAt) }}</span>
          </div>
          <div class="stat-item">
            <va-icon name="event_note" />
            <span class="stat-text stat-date">{{ formatExpiryDate(job.expiryDate) }}</span>
          </div>
          <div class="stat-item">
            <va-icon name="timer" />
            <span class="stat-text">{{ calculateDaysRemaining(job.expiryDate) }}d</span>
          </div>
        </div>

        <!-- Card Actions -->
        <div class="job-actions">
          <button class="action-btn view" title="Ver detalles" @click="viewJob(job)">
            <va-icon name="visibility" />
            Ver
          </button>
          <button class="action-btn edit" title="Editar" @click="editJob(job)">
            <va-icon name="edit" />
            Editar
          </button>
          <button
            class="action-btn"
            :class="job.status === 'active' ? 'close' : 'reopen'"
            @click="toggleJobStatus(job)"
          >
            <va-icon :name="job.status === 'active' ? 'visibility_off' : 'visibility' " />
            {{ job.status === 'active' ? 'Desactivar' : 'Activar' }}
          </button>
          <button class="action-btn delete" title="Eliminar" @click="deleteJob(job)">
            <va-icon name="delete" />
            Eliminar
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <va-icon name="work" size="3rem" />
      <h3>No hay trabajos publicados</h3>
      <p>¡Comienza publicando tu primer empleo!</p>
      <router-link to="/publicar" class="empty-action-btn">
        <va-icon name="add_circle" />
        Publicar Trabajo
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import { useAuthStore } from '@/stores/useAuthStore'
import JobDetailModal from '@/components/Modals/JobDetailModal.vue'

// ========== COMPOSABLES ==========
const router = useRouter()
const { init: notify } = useToast()
const authStore = useAuthStore()

// ========== PROPS ==========
const props = defineProps({
  userProfileId: {
    type: String,
    required: true
  }
})

// ========== DATA ==========
const loading = ref(false)
const jobs = ref([])
const searchQuery = ref('')
const filterStatus = ref('')
const sortBy = ref('recent')
const showDetailModal = ref(false)
const selectedJob = ref(null)

// ========== COMPUTED ==========
const filteredJobs = computed(() => {
  let filtered = jobs.value

  // Filtrar por estado
  if (filterStatus.value) {
    filtered = filtered.filter(job => job.status === filterStatus.value)
  }

  // Filtrar por búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(job =>
      job.title.toLowerCase().includes(query) ||
      job.companyName.toLowerCase().includes(query)
    )
  }

  // Ordenar
  if (sortBy.value === 'views') {
    filtered.sort((a, b) => b.views - a.views)
  } else if (sortBy.value === 'applications') {
    filtered.sort((a, b) => b.applications - a.applications)
  } else {
    filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
  }

  return filtered
})

// ========== LIFECYCLE ==========
onMounted(() => {
  loadJobs()
})

// ========== METHODS ==========
const loadJobs = async () => {
  try {
    loading.value = true

    // Usar auth store en lugar de localStorage
    if (!authStore.user) {
      console.warn('No hay usuario autenticado en authStore')
      loading.value = false
      return
    }

    if (!authStore.accessToken) {
      console.warn('No hay token de autenticación en authStore')
      loading.value = false
      return
    }

    const email = authStore.user.email || ''

    console.log('JobsManager - Email buscando:', email)
    console.log('JobsManager - Token presente:', !!authStore.accessToken)
    console.log('JobsManager - isAuthenticated:', authStore.isAuthenticated)

    const url = `/api/user/published?email=${encodeURIComponent(email)}`
    console.log('JobsManager - URL construida:', url)
    console.log('JobsManager - Authorization header:', `Bearer ${authStore.accessToken?.substring(0, 30)}...`)

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      }
    })

    console.log('JobsManager - Response received, status:', response.status)
    console.log('JobsManager - Response content-type:', response.headers.get('content-type'))

    const data = await response.json()
    console.log('JobsManager - Data recibida:', data)

    if (!response.ok) {
      console.error('JobsManager - Error response:', data)
      const errorMsg = data.message || 'Error al cargar trabajos publicados'
      throw new Error(errorMsg)
    }

    if (data.success && data.jobs) {
      console.log(`JobsManager - ${data.jobs.length} trabajos encontrados`)
      // Mapear datos de la API al formato esperado
      jobs.value = data.jobs.map(job => ({
        id: job.id,
        title: job.title,
        companyName: job.companyName,
        status: job.status,
        views: job.views || 0,
        applications: job.applications || 0,
        createdAt: new Date(job.createdAt).toISOString(),
        expiryDate: job.expiryDate,
        selectedPlan: job.selectedPlan,
        // Datos del plan capturados en el momento de publicación
        planLabel: job.planLabel,
        planPrice: job.planPrice,
        planDuration: job.planDuration
      }))
    } else {
      console.warn('JobsManager - Respuesta sin éxito:', data)
      throw new Error(data.message || 'Respuesta del servidor inválida')
    }
  } catch (err) {
    console.error('Error en loadJobs:', err)
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
    // Mantener datos mock como fallback
  } finally {
    loading.value = false
  }
}

const statusLabel = (status) => {
  const labels = {
    active: '✓ Activo',
    closed: '✕ Cerrado',
    draft: '✎ Borrador'
  }
  return labels[status] || status
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const today = new Date()
  const diff = today - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return 'Hoy'
  if (days === 1) return 'Ayer'
  if (days < 7) return `Hace ${days} días`
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
}

const formatExactDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }) + ' ' + date.toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const formatExpiryDate = (dateString) => {
  if (!dateString) return 'Sin fecha'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const calculateDaysRemaining = (expiryDateString) => {
  if (!expiryDateString) return -1
  const expiryDate = new Date(expiryDateString)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  expiryDate.setHours(0, 0, 0, 0)
  const diff = expiryDate - today
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))
  return days
}

const formatPlanName = (planKey, planLabel) => {
  // Usar el planLabel capturado en el momento de publicación si está disponible
  if (planLabel) return planLabel

  if (!planKey) return 'Sin plan'
  const planNames = {
    'estandar': 'Estándar',
    'purpura': 'Púrpura',
    'impulso': 'Impulso Pro'
  }
  return planNames[planKey.toLowerCase()] || planKey
}

const viewJob = async (job) => {
  try {
    // Llamar a get_job para traer datos completos
    const response = await fetch(`/api/jobs/${job.id}/`, {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al cargar detalles del trabajo')
    }

    // Usar los datos completos del endpoint get_job
    selectedJob.value = data.job
    showDetailModal.value = true
    console.log('Detalles completos del trabajo cargados:', job.id)
  } catch (err) {
    console.error('Error cargando detalles del trabajo:', err)
    notify({
      message: `Error al cargar detalles: ${err.message}`,
      color: 'danger'
    })
  }
}

const editJob = (job) => {
  notify({
    message: `Abriendo editor para "${job.title}"...`,
    color: 'info'
  })
  // Navegar a vista de edición con ID del trabajo
  router.push({
    name: 'PublishJob',
    query: { jobId: job.id }
  })
}

const toggleJobStatus = async (job) => {
  try {
    const newStatus = job.status === 'active' ? 'closed' : 'active'
    const action = newStatus === 'active' ? 'Activando' : 'Desactivando'
    notify({
      message: `${action} anuncio...`,
      color: 'info'
    })

    const response = await fetch(`/api/jobs/${job.id}/update`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: newStatus })
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al actualizar anuncio')
    }

    job.status = newStatus
    const result = newStatus === 'active' ? 'Anuncio activado' : 'Anuncio desactivado'
    notify({
      message: `✓ ${result} exitosamente`,
      color: 'success'
    })
  } catch (err) {
    console.error('Error updating job status:', err)
    notify({
      message: `Error: ${err.message}`,
      color: 'danger'
    })
  }
}

const deleteJob = async (job) => {
  if (!confirm(`¿Está seguro de que desea eliminar "${job.title}"?`)) return

  try {
    notify({
      message: 'Eliminando trabajo...',
      color: 'info'
    })

    const response = await fetch(`/api/jobs/${job.id}/delete`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al eliminar trabajo')
    }

    jobs.value = jobs.value.filter(j => j.id !== job.id)
    notify({
      message: '✓ Trabajo eliminado exitosamente',
      color: 'success'
    })
  } catch (err) {
    console.error('Error deleting job:', err)
    notify({
      message: `Error: ${err.message}`,
      color: 'danger'
    })
  }
}

const deactivateJob = async () => {
  if (!selectedJob.value) return

  try {
    notify({
      message: 'Desactivando anuncio...',
      color: 'info'
    })

    const response = await fetch(`/api/jobs/${selectedJob.value.id}/update`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: 'closed' })
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al desactivar anuncio')
    }

    // Actualizar en lista
    const jobIndex = jobs.value.findIndex(j => j.id === selectedJob.value.id)
    if (jobIndex !== -1) {
      jobs.value[jobIndex].status = 'closed'
    }

    selectedJob.value.status = 'closed'

    notify({
      message: '✓ Anuncio desactivado exitosamente',
      color: 'success'
    })

    showDetailModal.value = false
  } catch (err) {
    console.error('Error deactivating job:', err)
    notify({
      message: `Error: ${err.message}`,
      color: 'danger'
    })
  }
}

const activateJob = async () => {
  if (!selectedJob.value) return

  try {
    notify({
      message: 'Activando anuncio...',
      color: 'info'
    })

    const response = await fetch(`/api/jobs/${selectedJob.value.id}/update`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: 'active' })
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al activar anuncio')
    }

    // Actualizar en lista
    const jobIndex = jobs.value.findIndex(j => j.id === selectedJob.value.id)
    if (jobIndex !== -1) {
      jobs.value[jobIndex].status = 'active'
    }

    selectedJob.value.status = 'active'

    notify({
      message: '✓ Anuncio activado exitosamente',
      color: 'success'
    })

    showDetailModal.value = false
  } catch (err) {
    console.error('Error activating job:', err)
    notify({
      message: `Error: ${err.message}`,
      color: 'danger'
    })
  }
}
</script>

<style scoped>
.jobs-manager {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* ========== HEADER ========== */
.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.manager-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
}

.publish-btn-new {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #9f7aea, #8b5cf6);
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.publish-btn-new:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

/* ========== FILTER BAR ========== */
.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 250px;
  padding: 0.75rem 1rem;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.2s;
}

.search-box:focus-within {
  border-color: #9f7aea;
  box-shadow: 0 0 0 3px rgba(159, 122, 234, 0.1);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 0.95rem;
  background: transparent;
}

.filter-controls {
  display: flex;
  gap: 0.75rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-select:hover {
  border-color: #9f7aea;
}

.filter-select:focus {
  outline: none;
  border-color: #9f7aea;
  box-shadow: 0 0 0 3px rgba(159, 122, 234, 0.1);
}

/* ========== LOADING STATE ========== */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-state p {
  margin-top: 1rem;
  color: #666;
}

/* ========== JOBS LIST ========== */
.jobs-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.job-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.job-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.job-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.job-info {
  flex: 1;
}

.job-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
}

.job-company {
  margin: 0.25rem 0 0;
  color: #666;
  font-size: 0.95rem;
}

.job-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
}

.job-badge.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.job-badge.closed {
  background: #ffebee;
  color: #c62828;
}

.job-badge.draft {
  background: #f3e5f5;
  color: #6a1b9a;
}

/* ========== JOB STATS ========== */
.job-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #666;
  font-size: 0.85rem;
  white-space: nowrap;
}

.stat-item svg {
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  color: #9f7aea;
}

.stat-text {
  font-weight: 500;
  color: #1a1a1a;
}

.stat-date {
  font-size: 0.75rem;
  color: #999;
}

.plan-stat {
  margin: 0 0.5rem;
}

.stat-divider {
  color: #ddd;
  font-size: 1.2rem;
  font-weight: 300;
  margin: 0 0.2rem;
  line-height: 1;
}

.plan-badge {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  white-space: nowrap;
}

.plan-estandar {
  background: linear-gradient(135deg, #F59E0B, #FBBF24);
}

.plan-purpura {
  background: linear-gradient(135deg, #9F7AEA, #A78BFA);
}

.plan-impulso {
  background: linear-gradient(135deg, #10B981, #34D399);
}

/* ========== JOB ACTIONS ========== */
.job-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.85rem;
  border: 1px solid #9f7aea;
  border-radius: 6px;
  background: white;
  color: #8b5cf6;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn:hover {
  border-color: #9f7aea;
  background: #faf5ff;
  color: #7c3aed;
}

.action-btn.edit {
  color: #1976d2;
  border-color: #bbdefb;
}

.action-btn.edit:hover {
  background: #e3f2fd;
}

.action-btn.duplicate {
  color: #f57c00;
  border-color: #ffe0b2;
}

.action-btn.duplicate:hover {
  background: #fff3e0;
}

.action-btn.close {
  color: #d32f2f;
  border-color: #ffcdd2;
}

.action-btn.close:hover {
  background: #ffebee;
}

.action-btn.reopen {
  color: #388e3c;
  border-color: #c8e6c9;
}

.action-btn.reopen:hover {
  background: #e8f5e9;
}

.action-btn.delete {
  color: #d32f2f;
  border-color: #ffcdd2;
}

.action-btn.delete:hover {
  background: #ffebee;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.empty-state h3 {
  margin: 1rem 0 0.5rem;
  font-size: 1.25rem;
  color: #1a1a1a;
}

.empty-state p {
  color: #666;
  margin-bottom: 1.5rem;
}

.empty-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.empty-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .jobs-manager {
    padding: 1rem;
  }

  .manager-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .manager-header h1 {
    font-size: 1.5rem;
  }

  .filter-bar {
    flex-direction: column;
  }

  .search-box {
    min-width: 100%;
  }

  .filter-controls {
    width: 100%;
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
  }

  .job-stats {
    gap: 0.75rem;
  }

  .stat-item {
    font-size: 0.75rem;
  }

  .stat-date {
    font-size: 0.65rem;
  }

  .job-actions {
    gap: 0.3rem;
  }

  .action-btn {
    padding: 0.4rem 0.7rem;
    font-size: 0.8rem;
  }
}
</style>
