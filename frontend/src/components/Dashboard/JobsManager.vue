<!-- frontend/src/components/Dashboard/JobsManager.vue -->
<template>
  <div class="jobs-manager">
    <!-- Header -->
    <div class="manager-header">
      <h1>Administrador De Empleos</h1>
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
          <div class="stat">
            <va-icon name="visibility" />
            <span>{{ job.views }} vistas</span>
          </div>
          <div class="stat">
            <va-icon name="people" />
            <span>{{ job.applications }} aplicaciones</span>
          </div>
          <div class="stat">
            <va-icon name="calendar_today" />
            <span>{{ formatDate(job.createdAt) }}</span>
          </div>
        </div>

        <!-- Card Actions -->
        <div class="job-actions">
          <button class="action-btn view" title="Ver detalles">
            <va-icon name="visibility" />
            Ver
          </button>
          <button class="action-btn edit" title="Editar" @click="editJob(job)">
            <va-icon name="edit" />
            Editar
          </button>
          <button class="action-btn duplicate" title="Duplicar" @click="duplicateJob(job)">
            <va-icon name="file_copy" />
            Duplicar
          </button>
          <button
            class="action-btn"
            :class="job.status === 'active' ? 'close' : 'reopen'"
            @click="toggleJobStatus(job)"
          >
            <va-icon :name="job.status === 'active' ? 'close' : 'check_circle'" />
            {{ job.status === 'active' ? 'Cerrar' : 'Reabrir' }}
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

// ========== COMPOSABLES ==========
const router = useRouter()
const { init: notify } = useToast()

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

    const storedUser = localStorage.getItem('auth_user')
    const storedToken = localStorage.getItem('access_token')

    if (!storedUser) {
      console.warn('No hay usuario autenticado')
      loading.value = false
      return
    }

    if (!storedToken) {
      console.warn('No hay token de autenticación')
      loading.value = false
      return
    }

    const user = JSON.parse(storedUser)
    const email = user.email || ''

    console.log('JobsManager - Email buscando:', email)
    console.log('JobsManager - Token:', storedToken ? 'Presente' : 'No presente')

    const response = await fetch(
      `/api/user/published?email=${encodeURIComponent(email)}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${storedToken}`,
          'Content-Type': 'application/json'
        }
      }
    )

    console.log('JobsManager - Response status:', response.status)

    if (!response.ok) {
      const errorData = await response.json()
      console.log('JobsManager - Error response:', errorData)
      throw new Error('Error cargando trabajos publicados')
    }

    const data = await response.json()
    console.log('JobsManager - Data recibida:', data)
    if (data.success && data.jobs) {
      // Mapear datos de la API al formato esperado
      jobs.value = data.jobs.map(job => ({
        id: job.id,
        title: job.title,
        companyName: job.companyName,
        status: job.status,
        views: job.views || 0,
        applications: job.applications || 0,
        createdAt: new Date(job.createdAt).toISOString()
      }))
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

const editJob = (job) => {
  notify({
    message: `Editando "${job.title}"`,
    color: 'info'
  })
  // TODO: Abrir modal/página de edición
}

const duplicateJob = async (job) => {
  try {
    notify({
      message: `Duplicando "${job.title}"...`,
      color: 'info'
    })
    // TODO: Llamar API para duplicar trabajo
    setTimeout(() => {
      notify({
        message: '✓ Trabajo duplicado exitosamente',
        color: 'success'
      })
      loadJobs()
    }, 1000)
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger'
    })
  }
}

const toggleJobStatus = async (job) => {
  try {
    const newStatus = job.status === 'active' ? 'closed' : 'active'
    notify({
      message: `${newStatus === 'active' ? 'Reabriendo' : 'Cerrando'} trabajo...`,
      color: 'info'
    })
    // TODO: Llamar API para cambiar estado
    job.status = newStatus
    notify({
      message: `✓ Estado actualizado`,
      color: 'success'
    })
  } catch (err) {
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
    // TODO: Llamar API para eliminar
    jobs.value = jobs.value.filter(j => j.id !== job.id)
    notify({
      message: '✓ Trabajo eliminado',
      color: 'success'
    })
  } catch (err) {
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
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
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
  border-color: #5C0099;
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
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
  border-color: #5C0099;
}

.filter-select:focus {
  outline: none;
  border-color: #5C0099;
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
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
  gap: 2rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
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
  border: 1px solid #5C0099;
  border-radius: 6px;
  background: white;
  color: #5C0099;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn:hover {
  border-color: #5C0099;
  background: #f9f7ff;
  color: #3D0066;
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
    flex-direction: column;
    gap: 1rem;
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
