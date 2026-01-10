<template>
  <div class="shortlisted-view">
    <div class="section-header">
      <h1>Trabajos Guardados</h1>
      <p class="subtitle">Administra los trabajos que has guardado como favoritos</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <va-progress-circle indeterminate color="purple" />
      <p>Cargando trabajos guardados...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!isLoading && savedJobs.length === 0" class="empty-state">
      <div class="empty-icon">
        <va-icon name="bookmark_border" size="4rem" />
      </div>
      <h3>No tienes trabajos guardados</h3>
      <p>Guarda trabajos que te interesen para revisarlos más tarde</p>
      <va-button color="purple" @click="goToJobs">
        <va-icon name="search" size="small" />
        Buscar Trabajos
      </va-button>
    </div>

    <!-- Saved Jobs List -->
    <div v-else class="saved-jobs-list">
      <!-- Stats Row -->
      <div class="stats-row">
        <div class="stat-card stat-card-purple">
          <div class="stat-icon stat-icon-purple">
            <va-icon name="bookmark" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ savedJobs.length }}</span>
            <span class="stat-label">Total Guardados</span>
          </div>
        </div>
        <div class="stat-card stat-card-blue">
          <div class="stat-icon stat-icon-blue">
            <va-icon name="work" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ activeJobsCount }}</span>
            <span class="stat-label">Activos</span>
          </div>
        </div>
        <div class="stat-card stat-card-orange">
          <div class="stat-icon stat-icon-orange">
            <va-icon name="schedule" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ expiringJobsCount }}</span>
            <span class="stat-label">Por Expirar</span>
          </div>
        </div>
        <div class="stat-card stat-card-red">
          <div class="stat-icon stat-icon-red">
            <va-icon name="event_busy" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ expiredJobsCount }}</span>
            <span class="stat-label">Expirados</span>
          </div>
        </div>
        <div class="stat-card stat-card-green">
          <div class="stat-icon stat-icon-green">
            <va-icon name="check_circle" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ alreadyAppliedCount }}</span>
            <span class="stat-label">Ya Postulados</span>
          </div>
        </div>
      </div>

      <!-- Filters Section -->
      <div class="filters-section">
        <div class="filters-header">
          <div class="filters-title">
            <va-icon name="filter_list" size="1.25rem" />
            <h3>Filtros</h3>
          </div>
          <button
            v-if="searchQuery || filterModality || filterStatus || filterNotApplied"
            class="btn-clear-filters"
            @click="clearFilters"
          >
            <va-icon name="clear" size="small" />
            Limpiar
          </button>
        </div>
        <div class="filters-content">
          <div class="filter-group search-group">
            <label class="filter-label">
              <va-icon name="search" size="small" />
              Búsqueda
            </label>
            <va-input
              v-model="searchQuery"
              placeholder="Buscar por título o empresa..."
              clearable
              class="filter-input"
            >
              <template #prepend>
                <va-icon name="search" />
              </template>
            </va-input>
          </div>
          <div class="filter-group">
            <label class="filter-label">
              <va-icon name="work" size="small" />
              Modalidad
            </label>
            <va-select
              v-model="filterModality"
              :options="modalityOptions"
              text-by="text"
              value-by="value"
              placeholder="Todas las modalidades"
              clearable
              class="filter-select"
            />
          </div>
          <div class="filter-group">
            <label class="filter-label">
              <va-icon name="label" size="small" />
              Estado
            </label>
            <va-select
              v-model="filterStatus"
              :options="statusFilterOptions"
              text-by="text"
              value-by="value"
              placeholder="Todos los estados"
              clearable
              class="filter-select"
            />
          </div>
          <div class="filter-group">
            <label class="filter-label">
              <va-icon name="sort" size="small" />
              Ordenar por
            </label>
            <va-select
              v-model="sortBy"
              :options="sortOptions"
              text-by="text"
              value-by="value"
              placeholder="Más reciente"
              class="filter-select"
            />
          </div>
        </div>
      </div>

      <!-- Quick Actions Section -->
      <div class="quick-actions-section">
        <div class="quick-actions-header">
          <div class="quick-actions-title">
            <va-icon name="bolt" size="1.25rem" />
            <h3>Acciones Rápidas</h3>
          </div>
        </div>
        <div class="quick-actions-buttons">
          <button
            class="btn-quick-action btn-remove-unavailable"
            @click="removeAllUnavailable"
            :disabled="unavailableJobsCount === 0"
          >
            <va-icon name="delete_sweep" size="small" />
            <span>Quitar No Disponibles ({{ unavailableJobsCount }})</span>
          </button>
          <button
            class="btn-quick-action btn-filter-not-applied"
            :class="{ active: filterNotApplied }"
            @click="toggleNotAppliedFilter"
          >
            <va-icon :name="filterNotApplied ? 'visibility_off' : 'send'" size="small" />
            <span>{{ filterNotApplied ? 'Mostrar Todos' : `Mostrar Pendientes de Postular (${notAppliedCount})` }}</span>
          </button>
        </div>
      </div>

      <!-- Results Count -->
      <div class="results-count">
        <va-icon name="work" size="small" />
        <span>{{ filteredJobs.length }} trabajo{{ filteredJobs.length !== 1 ? 's' : '' }} guardado{{ filteredJobs.length !== 1 ? 's' : '' }}</span>
      </div>

      <!-- Jobs Grid (2 columnas) usando JobListCompact -->
      <div class="jobs-grid">
        <transition-group name="job-list" tag="div" class="jobs-grid-inner">
          <div
            v-for="savedJob in sortedJobs"
            :key="savedJob.saved_id"
            class="job-wrapper"
          >
            <!-- Saved Badge -->
            <div class="saved-badge">
              <span class="badge badge-saved">
                <va-icon name="bookmark" size="12px" />
                Guardado
              </span>
              <span v-if="hasApplied(savedJob.job.id)" class="badge badge-applied">
                <va-icon name="check_circle" size="12px" />
                Ya Postulaste
              </span>
              <span v-if="getActualJobStatus(savedJob.job) !== 'active'" class="badge badge-inactive">
                {{ getJobStatusLabel(getActualJobStatus(savedJob.job)) }}
              </span>
            </div>

            <!-- JobListCompact Component -->
            <JobListCompact
              :listing="savedJob.job"
              @select="viewJob(savedJob.job.id)"
            />

            <!-- Footer con info adicional -->
            <div class="saved-footer">
              <div class="saved-info">
                <span class="saved-date">
                  <va-icon name="schedule" size="14px" />
                  {{ formatSavedDate(savedJob.saved_at) }}
                </span>
                <span v-if="savedJob.job.expiry_date" class="expiry-warning" :class="getExpiryClass(savedJob.job.expiry_date)">
                  <va-icon name="event" size="14px" />
                  {{ getExpiryText(savedJob.job.expiry_date) }}
                </span>
              </div>
              <div class="saved-actions">
                <button
                  class="btn-share"
                  @click.stop="shareJob(savedJob.job)"
                  title="Compartir trabajo"
                >
                  <va-icon name="share" size="14px" />
                </button>
                <button
                  class="btn-unsave"
                  @click.stop="unsaveJob(savedJob)"
                  title="Quitar de guardados"
                >
                  <va-icon name="bookmark_remove" size="14px" />
                  Quitar
                </button>
                <button
                  v-if="getActualJobStatus(savedJob.job) === 'active' && !hasApplied(savedJob.job.id)"
                  class="btn-apply"
                  @click.stop="applyToJob(savedJob.job.id)"
                >
                  <va-icon name="send" size="14px" />
                  Postular
                </button>
                <button
                  v-else-if="hasApplied(savedJob.job.id)"
                  class="btn-already-applied"
                  disabled
                >
                  <va-icon name="check_circle" size="14px" />
                  Postulado
                </button>
                <button
                  v-else
                  class="btn-disabled"
                  disabled
                >
                  <va-icon name="block" size="14px" />
                  No Disponible
                </button>
              </div>
            </div>
          </div>
        </transition-group>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'
import JobListCompact from '@/views/Detail/JobListCompact.vue'

const router = useRouter()
const authStore = useAuthStore()
const { init: notify } = useToast()

// State
const savedJobs = ref([])
const userApplications = ref([]) // Track user's applications
const isLoading = ref(false)
const searchQuery = ref('')
const filterModality = ref(null)
const filterStatus = ref(null)
const filterNotApplied = ref(false) // New filter for non-applied jobs
const sortBy = ref('expiring') // Changed default to expiring first

// Filter Options
const modalityOptions = [
  { text: 'Presencial', value: 'presencial' },
  { text: 'Remoto', value: 'remoto' },
  { text: 'Híbrido', value: 'hibrido' }
]

const statusFilterOptions = [
  { text: 'Activo', value: 'active' },
  { text: 'Pausado', value: 'paused' },
  { text: 'No Disponible', value: 'unavailable' }
]

const sortOptions = [
  { text: 'Por expirar primero', value: 'expiring' },
  { text: 'Más reciente', value: 'recent' },
  { text: 'Más antiguo', value: 'oldest' },
  { text: 'Título (A-Z)', value: 'title_asc' },
  { text: 'Título (Z-A)', value: 'title_desc' },
  { text: 'Empresa (A-Z)', value: 'company_asc' }
]

// Helper function to get actual job status (considering expiration)
const getActualJobStatus = (job) => {
  // If status is explicitly set to closed, paused, or rejected, return that
  if (job.status === 'closed' || job.status === 'paused' || job.status === 'rejected' || job.status === 'draft') {
    return job.status
  }

  // Check if job is expired by date (only for active/pending jobs)
  if (job.expiryDate) {
    const expiryDate = new Date(job.expiryDate)
    const now = new Date()
    if (expiryDate < now) {
      return 'expired'
    }
  }

  // Return the job's status field (active or pending)
  return job.status
}

// Computed Stats
const activeJobsCount = computed(() => {
  return savedJobs.value.filter(saved => {
    const actualStatus = getActualJobStatus(saved.job)
    return actualStatus === 'active'
  }).length
})

const expiringJobsCount = computed(() => {
  const now = new Date()
  const sevenDaysFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)
  return savedJobs.value.filter(saved => {
    if (!saved.job.expiryDate) return false
    const expiryDate = new Date(saved.job.expiryDate)
    return expiryDate <= sevenDaysFromNow && expiryDate >= now && getActualJobStatus(saved.job) === 'active'
  }).length
})

const expiredJobsCount = computed(() => {
  return savedJobs.value.filter(saved => {
    const status = getActualJobStatus(saved.job)
    return status === 'expired' || status === 'closed' || status === 'rejected' || status === 'draft'
  }).length
})

const alreadyAppliedCount = computed(() => {
  return savedJobs.value.filter(saved => hasApplied(saved.job.id)).length
})

const uniqueCities = computed(() => {
  const cities = new Set(savedJobs.value.map(saved => saved.job.city))
  return cities.size
})

// Check if user already applied to a job
const hasApplied = (jobId) => {
  // El endpoint devuelve 'job_id', no 'job'
  return userApplications.value.some(app => app.job_id === jobId)
}

// Count of jobs not yet applied to
const notAppliedCount = computed(() => {
  return savedJobs.value.filter(saved => !hasApplied(saved.job.id)).length
})

// Count of unavailable jobs (expired, closed, etc.)
const unavailableJobsCount = computed(() => {
  return savedJobs.value.filter(saved => {
    const status = getActualJobStatus(saved.job)
    return status === 'closed' || status === 'expired' || status === 'rejected' || status === 'draft'
  }).length
})

// Filtered and Sorted Jobs
const filteredJobs = computed(() => {
  let jobs = savedJobs.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    jobs = jobs.filter(saved =>
      saved.job.title.toLowerCase().includes(query) ||
      saved.job.companyName?.toLowerCase().includes(query)
    )
  }

  // Modality filter
  if (filterModality.value) {
    jobs = jobs.filter(saved => {
      const jobModality = saved.job.modality?.toLowerCase()
      return jobModality === filterModality.value
    })
  }

  // Status filter
  if (filterStatus.value) {
    jobs = jobs.filter(saved => {
      const actualStatus = getActualJobStatus(saved.job)

      // "No Disponible" includes closed, expired, rejected, and draft
      if (filterStatus.value === 'unavailable') {
        return actualStatus === 'closed' || actualStatus === 'expired' || actualStatus === 'rejected' || actualStatus === 'draft'
      }

      return actualStatus === filterStatus.value
    })
  }

  // Filter by not applied
  if (filterNotApplied.value) {
    jobs = jobs.filter(saved => !hasApplied(saved.job.id))
  }

  return jobs
})

const sortedJobs = computed(() => {
  const jobs = [...filteredJobs.value]

  switch (sortBy.value) {
    case 'expiring':
      // Sort by expiration date - active jobs with nearest expiry first
      return jobs.sort((a, b) => {
        const statusA = getActualJobStatus(a.job)
        const statusB = getActualJobStatus(b.job)

        // Active jobs first
        if (statusA === 'active' && statusB !== 'active') return -1
        if (statusA !== 'active' && statusB === 'active') return 1

        // For active jobs, sort by expiry date
        if (statusA === 'active' && statusB === 'active') {
          const dateA = a.job.expiryDate ? new Date(a.job.expiryDate) : new Date('9999-12-31')
          const dateB = b.job.expiryDate ? new Date(b.job.expiryDate) : new Date('9999-12-31')
          return dateA - dateB
        }

        // For non-active, most recent first
        return new Date(b.saved_at) - new Date(a.saved_at)
      })
    case 'recent':
      return jobs.sort((a, b) => new Date(b.saved_at) - new Date(a.saved_at))
    case 'oldest':
      return jobs.sort((a, b) => new Date(a.saved_at) - new Date(b.saved_at))
    case 'title_asc':
      return jobs.sort((a, b) => a.job.title.localeCompare(b.job.title))
    case 'title_desc':
      return jobs.sort((a, b) => b.job.title.localeCompare(a.job.title))
    case 'company_asc':
      return jobs.sort((a, b) => (a.job.companyName || '').localeCompare(b.job.companyName || ''))
    default:
      return jobs
  }
})

// Methods
const loadSavedJobs = async () => {
  isLoading.value = true

  try {
    const response = await fetch('/api/saved-jobs/', {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (!response.ok) {
      throw new Error('Error al cargar trabajos guardados')
    }

    const data = await response.json()
    savedJobs.value = data.saved_jobs || []
  } catch (error) {
    console.error('Error loading saved jobs:', error)
    notify({
      message: 'Error al cargar trabajos guardados',
      color: 'danger',
      duration: 3000
    })
  } finally {
    isLoading.value = false
  }
}

const loadUserApplications = async () => {
  try {
    // Cargar TODAS las postulaciones sin límite
    const response = await fetch('/api/applications/?limit=1000', {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (!response.ok) {
      throw new Error('Error al cargar postulaciones')
    }

    const data = await response.json()
    userApplications.value = data.applications || []

    console.log('Postulaciones cargadas:', userApplications.value.length)
  } catch (error) {
    console.error('Error loading applications:', error)
  }
}

const removeAllUnavailable = async () => {
  const unavailableJobs = savedJobs.value.filter(saved => {
    const status = getActualJobStatus(saved.job)
    return status === 'closed' || status === 'expired' || status === 'rejected' || status === 'draft'
  })

  if (unavailableJobs.length === 0) {
    notify({
      message: 'No hay trabajos no disponibles para quitar',
      color: 'info',
      duration: 2500
    })
    return
  }

  try {
    // Remove each unavailable job
    for (const savedJob of unavailableJobs) {
      await fetch('/api/saved-jobs/unsave/', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          job_id: savedJob.job.id
        })
      })
    }

    // Remove from local array
    savedJobs.value = savedJobs.value.filter(saved => {
      const status = getActualJobStatus(saved.job)
      return !(status === 'closed' || status === 'expired' || status === 'rejected' || status === 'draft')
    })

    notify({
      message: `✓ ${unavailableJobs.length} trabajo${unavailableJobs.length !== 1 ? 's' : ''} no disponible${unavailableJobs.length !== 1 ? 's' : ''} eliminado${unavailableJobs.length !== 1 ? 's' : ''}`,
      color: 'success',
      duration: 3000
    })
  } catch (error) {
    console.error('Error removing unavailable jobs:', error)
    notify({
      message: 'Error al quitar trabajos no disponibles',
      color: 'danger',
      duration: 3000
    })
  }
}

const toggleNotAppliedFilter = () => {
  filterNotApplied.value = !filterNotApplied.value
}

const shareJob = async (job) => {
  const jobUrl = `${window.location.origin}/guias/trabajos?selected=${job.id}`

  try {
    if (navigator.share) {
      await navigator.share({
        title: job.title,
        text: `Mira esta oferta de trabajo: ${job.title} en ${job.companyName}`,
        url: jobUrl
      })
    } else {
      // Fallback: copy to clipboard
      await navigator.clipboard.writeText(jobUrl)
      notify({
        message: '✓ Enlace copiado al portapapeles',
        color: 'success',
        duration: 2500
      })
    }
  } catch (error) {
    console.error('Error sharing:', error)
  }
}

const unsaveJob = async (savedJob) => {
  try {
    const response = await fetch('/api/saved-jobs/unsave/', {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        job_id: savedJob.job.id
      })
    })

    if (!response.ok) {
      throw new Error('Error al quitar de guardados')
    }

    // Remove from local array
    savedJobs.value = savedJobs.value.filter(j => j.saved_id !== savedJob.saved_id)

    notify({
      message: '✓ Trabajo quitado de guardados',
      color: 'success',
      duration: 2500
    })
  } catch (error) {
    console.error('Error unsaving job:', error)
    notify({
      message: 'Error al quitar trabajo de guardados',
      color: 'danger',
      duration: 3000
    })
  }
}

const viewJob = (jobId) => {
  router.push(`/guias/trabajos?selected=${jobId}`)
}

const applyToJob = (jobId) => {
  router.push(`/guias/trabajos?selected=${jobId}&apply=true`)
}

const goToJobs = () => {
  router.push('/guias/trabajos')
}

const clearFilters = () => {
  searchQuery.value = ''
  filterModality.value = null
  filterStatus.value = null
  filterNotApplied.value = false
  sortBy.value = 'expiring'
}

const getJobStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    paused: 'Pausado',
    expired: 'Expirado',
    closed: 'Cerrado'
  }
  return labels[status] || status
}

const formatSavedDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Guardado hoy'
  if (diffDays === 1) return 'Guardado ayer'
  if (diffDays < 7) return `Guardado hace ${diffDays} días`
  if (diffDays < 30) return `Guardado hace ${Math.floor(diffDays / 7)} semanas`

  return `Guardado: ${date.toLocaleDateString('es-BO', { month: 'short', day: 'numeric' })}`
}

const getExpiryText = (expiryDate) => {
  const date = new Date(expiryDate)
  const now = new Date()
  const diffTime = date - now
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) return 'Expirado'
  if (diffDays === 0) return 'Expira hoy'
  if (diffDays === 1) return 'Expira mañana'
  if (diffDays < 7) return `Expira en ${diffDays} días`

  return `Expira: ${date.toLocaleDateString('es-BO', { month: 'short', day: 'numeric' })}`
}

const getExpiryClass = (expiryDate) => {
  const date = new Date(expiryDate)
  const now = new Date()
  const diffTime = date - now
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) return 'expired'
  if (diffDays <= 3) return 'expiring-soon'
  if (diffDays <= 7) return 'expiring-warning'
  return ''
}

// Lifecycle
onMounted(() => {
  loadSavedJobs()
  loadUserApplications()
})
</script>

<style scoped>
/* ========== LAYOUT ========== */
.shortlisted-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* ========== HEADER ========== */
.section-header {
  margin-bottom: 2rem;
}

.section-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #6B7280;
  font-size: 1rem;
  margin: 0;
}

/* ========== LOADING & EMPTY STATES ========== */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1.25rem;
  gap: 1.25rem;
}

.loading-container p {
  color: #6B7280;
  font-size: 1rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1.25rem;
  text-align: center;
  gap: 1rem;
}

.empty-icon {
  width: 6rem;
  height: 6rem;
  background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9333EA;
  margin-bottom: 0.5rem;
}

.empty-state h3 {
  color: #374151;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.empty-state p {
  color: #9CA3AF;
  margin: 0;
  font-size: 1rem;
}

/* ========== STATS ROW ========== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon-purple {
  background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%);
}

.stat-icon-blue {
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
}

.stat-icon-orange {
  background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
}

.stat-icon-red {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
}

.stat-icon-green {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1F2937;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
  margin-top: 0.25rem;
}

/* ========== QUICK ACTIONS SECTION ========== */
.quick-actions-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  background-image: linear-gradient(white, white), linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

.quick-actions-header {
  margin-bottom: 1rem;
}

.quick-actions-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #7C3AED;
}

.quick-actions-title h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.quick-actions-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-quick-action {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid;
  flex: 1;
  min-width: 200px;
}

.btn-remove-unavailable {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.btn-remove-unavailable:hover:not(:disabled) {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.btn-remove-unavailable:disabled {
  background: #E5E7EB;
  color: #9CA3AF;
  cursor: not-allowed;
  box-shadow: none;
  border-color: #E5E7EB;
}

.btn-filter-not-applied {
  background: white;
  color: #7C3AED;
  border-color: #7C3AED;
}

.btn-filter-not-applied:hover {
  background: #F5F3FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}

.btn-filter-not-applied.active {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.btn-filter-not-applied.active:hover {
  background: linear-gradient(135deg, #6D28D9 0%, #5B21B6 100%);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
}

/* ========== FILTERS SECTION ========== */
.filters-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filters-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #7C3AED;
}

.filters-title h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.btn-clear-filters {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  color: #6B7280;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-clear-filters:hover {
  background: #F9FAFB;
  border-color: #D1D5DB;
  color: #374151;
}

.filters-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.search-group {
  grid-column: span 2;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

/* ========== RESULTS COUNT ========== */
.results-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
  border-radius: 8px;
  color: #7C3AED;
  font-weight: 500;
  margin-bottom: 1.5rem;
}

/* ========== JOBS GRID (2 COLUMNAS) ========== */
.jobs-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.jobs-grid-inner {
  display: contents;
}

.job-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
}

/* ========== SAVED BADGE ========== */
.saved-badge {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.badge-saved {
  background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(147, 51, 234, 0.3);
}

.badge-applied {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.badge-inactive {
  background: #FEF3C7;
  color: #92400E;
}

/* ========== SAVED FOOTER ========== */
.saved-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-top: none;
  border-radius: 0 0 8px 8px;
  gap: 1rem;
  flex-wrap: wrap;
}

.saved-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.saved-date {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 500;
}

.expiry-warning {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  width: fit-content;
}

.expiry-warning.expiring-soon {
  background: #FEE2E2;
  color: #DC2626;
}

.expiry-warning.expiring-warning {
  background: #FEF3C7;
  color: #D97706;
}

.expiry-warning.expired {
  background: #F3F4F6;
  color: #6B7280;
}

.saved-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-share,
.btn-unsave,
.btn-apply,
.btn-already-applied,
.btn-disabled {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-share {
  background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
  color: white;
  box-shadow: 0 2px 6px rgba(139, 92, 246, 0.3);
  padding: 0.5rem;
}

.btn-share:hover {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.btn-unsave {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: white;
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.3);
  border: none;
}

.btn-unsave:hover {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.btn-apply {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.25);
}

.btn-apply:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
}

.btn-already-applied {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
  cursor: not-allowed;
  opacity: 0.7;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.2);
}

.btn-already-applied:hover {
  transform: none;
  opacity: 0.7;
}

.btn-disabled {
  background: #E5E7EB;
  color: #9CA3AF;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-disabled:hover {
  background: #E5E7EB;
  transform: none;
}

/* ========== ANIMATIONS ========== */
.job-list-enter-active,
.job-list-leave-active {
  transition: all 0.3s ease;
}

.job-list-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.job-list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1200px) {
  .jobs-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 1024px) {
  .filters-content {
    grid-template-columns: 1fr;
  }

  .search-group {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .shortlisted-view {
    padding: 1rem;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .section-header h1 {
    font-size: 1.5rem;
  }

  .quick-actions-buttons {
    flex-direction: column;
  }

  .btn-quick-action {
    min-width: 100%;
  }

  .saved-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .saved-actions {
    width: 100%;
  }

  .btn-share {
    padding: 0.5rem 0.875rem;
  }

  .btn-unsave,
  .btn-apply,
  .btn-already-applied {
    flex: 1;
  }
}
</style>
