<template>
  <div class="applications-view">
    <div class="section-header">
      <h1>Mis Postulaciones</h1>
      <p class="subtitle">Aquí puedes ver todas tus postulaciones y su estado actual</p>
      <div class="info-banner">
        <va-icon name="info" size="1.125rem" />
        <div class="info-content">
          <p class="info-text">
            Puedes retirar tus postulaciones en estados iniciales (Enviada, En Revisión).
            Una vez pre-seleccionado o entrevistado, no podrás retirarte para mantener el profesionalismo y evitar decisiones apresuradas en etapas avanzadas.
          </p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <va-progress-circle indeterminate color="purple" />
      <p>Cargando postulaciones...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!isLoading && applications.length === 0" class="empty-state">
      <va-icon name="assignment" size="4rem" color="#ccc" />
      <h3>No tienes postulaciones aún</h3>
      <p>Cuando te postules a trabajos, aparecerán aquí</p>
      <va-button color="purple" @click="goToJobs">Buscar Trabajos</va-button>
    </div>

    <!-- Applications List -->
    <div v-else class="applications-list">
      <!-- Stats Cards -->
      <div class="stats-row">
        <div
          class="stat-card stat-card-purple clickable"
          :class="{ 'active': filterStatus === null }"
          @click="filterByStatus(null)"
        >
          <div class="stat-icon stat-icon-purple">
            <va-icon name="send" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.total }}</span>
            <span class="stat-label">Total</span>
          </div>
        </div>
        <div
          class="stat-card stat-card-orange clickable"
          :class="{ 'active': filterStatus === 'reviewing' }"
          @click="filterByStatus('reviewing')"
        >
          <div class="stat-icon stat-icon-orange">
            <va-icon name="schedule" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.reviewing }}</span>
            <span class="stat-label">En Revisión</span>
          </div>
        </div>
        <div
          class="stat-card stat-card-green clickable"
          :class="{ 'active': filterStatus === 'shortlisted' }"
          @click="filterByStatus('shortlisted')"
        >
          <div class="stat-icon stat-icon-green">
            <va-icon name="star" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.shortlisted }}</span>
            <span class="stat-label">Pre-seleccionado</span>
          </div>
        </div>
        <div
          class="stat-card stat-card-blue clickable"
          :class="{ 'active': filterStatus === 'interviewed' }"
          @click="filterByStatus('interviewed')"
        >
          <div class="stat-icon stat-icon-blue">
            <va-icon name="check_circle" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.interviewed }}</span>
            <span class="stat-label">Entrevistado</span>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters-section">
        <div class="filters-header">
          <div class="filters-title">
            <va-icon name="filter_list" size="1.25rem" />
            <h3>Filtros</h3>
          </div>
          <button
            v-if="filterStatus || searchQuery"
            class="btn-clear-filters"
            @click="clearFilters"
          >
            <va-icon name="clear" size="small" />
            Limpiar
          </button>
        </div>
        <div class="filters-content">
          <div class="filter-group">
            <label class="filter-label">
              <va-icon name="label" size="small" />
              Estado
            </label>
            <va-select
              v-model="filterStatus"
              :options="statusOptions"
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
              placeholder="Más reciente"
              class="filter-select"
            />
          </div>
          <div class="filter-group search-group">
            <label class="filter-label">
              <va-icon name="search" size="small" />
              Búsqueda
            </label>
            <va-input
              v-model="searchQuery"
              placeholder="Buscar por trabajo o empresa..."
              clearable
              class="filter-input"
            >
              <template #prepend>
                <va-icon name="search" />
              </template>
            </va-input>
          </div>
        </div>
      </div>

      <!-- Applications Grid usando JobListCompact -->
      <div class="applications-grid">
        <transition-group name="application-list" tag="div" class="applications-grid-inner">
        <div
          v-for="application in filteredApplications"
          :key="application.id"
          class="application-wrapper"
        >
          <!-- Badges de estado sobre el card -->
          <div class="application-status-badges">
            <span class="badge" :class="`badge-${getStatusColor(application.status)}`">
              {{ getStatusLabel(application.status) }}
            </span>
            <span v-if="isRecent(application.applied_at)" class="badge badge-new">Reciente</span>
          </div>

          <!-- JobListCompact Component -->
          <JobListCompact
            :listing="mapApplicationToListing(application)"
            @select="viewDetails(application)"
          />

          <!-- Footer adicional con info de postulación -->
          <div class="application-footer">
            <div class="application-info">
              <span class="applied-date">
                <va-icon name="send" size="14px" />
                Postulado {{ formatDate(application.applied_at) }}
              </span>
              <span v-if="application.cv_name" class="cv-used">
                <va-icon name="description" size="14px" />
                CV: {{ application.cv_name }}
              </span>
              <span v-if="application.viewed_by_employer" class="viewed-indicator" title="La empresa vio tu postulación">
                <va-icon name="visibility" size="14px" />
                Visto por la empresa
              </span>
            </div>
            <button
              v-if="application.status === 'submitted' || application.status === 'reviewing'"
              class="btn-withdraw"
              @click.stop="withdrawApplication(application)"
            >
              <va-icon name="close" size="14px" />
              Retirar
            </button>
          </div>
        </div>
        </transition-group>
      </div>

      <!-- Scroll Infinito Loading -->
      <div v-if="hasMore && !isLoading" class="load-more-trigger" ref="loadMoreTrigger"></div>

      <!-- Loading más postulaciones -->
      <div v-if="isLoadingMore" class="loading-more">
        <va-progress-circle indeterminate color="purple" size="small" />
        <span>Cargando más postulaciones...</span>
      </div>

      <!-- Fin de resultados -->
      <div v-if="!hasMore && applications.length > 0" class="end-of-results">
        <va-icon name="check_circle" color="#10B981" />
        <span>Has visto todas tus postulaciones</span>
      </div>
    </div>

    <!-- Modal de Confirmación para Retirar -->
    <va-modal
      v-model="showWithdrawModal"
      title="Confirmar Retiro de Postulación"
      size="medium"
      :close-button="false"
      hide-default-actions
    >
      <div class="modal-content">
        <div class="modal-icon withdraw">
          <va-icon name="warning" size="3rem" />
        </div>
        <h3 class="modal-title">¿Estás seguro?</h3>
        <p class="modal-message">
          Estás a punto de retirar tu postulación a <strong>"{{ modalMessage }}"</strong>.
        </p>
        <p class="modal-warning">
          Esta acción no se puede deshacer y la empresa podrá ver que retiraste tu postulación.
        </p>
      </div>
      <template #footer>
        <div class="modal-actions">
          <va-button class="btn-modal-cancel" @click="cancelWithdraw">
            Cancelar
          </va-button>
          <va-button class="btn-modal-withdraw" @click="confirmWithdraw">
            Retirar Postulación
          </va-button>
        </div>
      </template>
    </va-modal>

    <!-- Modal de Éxito -->
    <va-modal
      v-model="showSuccessModal"
      title="Postulación Retirada"
      size="small"
      :close-button="false"
      hide-default-actions
    >
      <div class="modal-content">
        <div class="modal-icon success">
          <va-icon name="check_circle" size="3rem" />
        </div>
        <h3 class="modal-title">¡Listo!</h3>
        <p class="modal-message">
          Tu postulación ha sido retirada exitosamente.
        </p>
      </div>
      <template #footer>
        <div class="modal-actions">
          <va-button color="success" @click="showSuccessModal = false">
            Entendido
          </va-button>
        </div>
      </template>
    </va-modal>

    <!-- Modal de Error -->
    <va-modal
      v-model="showErrorModal"
      title="Error al Retirar"
      size="small"
      :close-button="false"
      hide-default-actions
    >
      <div class="modal-content">
        <div class="modal-icon error">
          <va-icon name="error" size="3rem" />
        </div>
        <h3 class="modal-title">Error</h3>
        <p class="modal-message">
          {{ modalMessage }}
        </p>
      </div>
      <template #footer>
        <div class="modal-actions">
          <va-button color="danger" @click="showErrorModal = false">
            Cerrar
          </va-button>
        </div>
      </template>
    </va-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import JobListCompact from '@/views/Detail/JobListCompact.vue'

const router = useRouter()
const authStore = useAuthStore()

// State
const applications = ref([])
const isLoading = ref(false)
const isLoadingMore = ref(false)
const currentPage = ref(1)
const hasMore = ref(true)
const limit = ref(12)
const filterStatus = ref(null)
const searchQuery = ref('')
const sortBy = ref('recent')
const loadMoreTrigger = ref(null)
const observer = ref(null)

// Modal state
const showWithdrawModal = ref(false)
const showSuccessModal = ref(false)
const showErrorModal = ref(false)
const modalMessage = ref('')
const applicationToWithdraw = ref(null)

// Status options
const statusOptions = [
  { value: 'submitted', text: 'Enviada' },
  { value: 'reviewing', text: 'En Revisión' },
  { value: 'shortlisted', text: 'Pre-seleccionado' },
  { value: 'interviewed', text: 'Entrevistado' },
  { value: 'rejected', text: 'Rechazado' },
  { value: 'accepted', text: 'Aceptado' },
  { value: 'withdrawn', text: 'Retirada' }
]

// Sort options
const sortOptions = [
  { value: 'recent', text: 'Más reciente' },
  { value: 'oldest', text: 'Más antigua' },
  { value: 'status', text: 'Por estado' }
]

// Computed
const stats = computed(() => {
  return {
    total: applications.value.length,
    reviewing: applications.value.filter(a => a.status === 'reviewing').length,
    shortlisted: applications.value.filter(a => a.status === 'shortlisted').length,
    interviewed: applications.value.filter(a => a.status === 'interviewed').length
  }
})

const filteredApplications = computed(() => {
  let filtered = [...applications.value]

  // Filter by status
  if (filterStatus.value) {
    filtered = filtered.filter(a => a.status === filterStatus.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(a => {
      const jobTitle = a.job?.title?.toLowerCase() || ''
      const companyName = a.job?.companyName?.toLowerCase() || ''
      return jobTitle.includes(query) || companyName.includes(query)
    })
  }

  // Sort
  if (sortBy.value === 'recent') {
    filtered.sort((a, b) => new Date(b.applied_at) - new Date(a.applied_at))
  } else if (sortBy.value === 'oldest') {
    filtered.sort((a, b) => new Date(a.applied_at) - new Date(b.applied_at))
  } else if (sortBy.value === 'status') {
    const statusOrder = ['shortlisted', 'interviewed', 'reviewing', 'submitted', 'accepted', 'rejected', 'withdrawn']
    filtered.sort((a, b) => statusOrder.indexOf(a.status) - statusOrder.indexOf(b.status))
  }

  return filtered
})

// Methods
const loadApplications = async (append = false) => {
  if (append) {
    isLoadingMore.value = true
  } else {
    isLoading.value = true
    currentPage.value = 1
    applications.value = []
  }

  try {
    const offset = (currentPage.value - 1) * limit.value

    // 1. Cargar aplicaciones (solo IDs y metadata)
    const appsResponse = await fetch(`/api/applications/?limit=${limit.value}&offset=${offset}`, {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (!appsResponse.ok) {
      throw new Error('Error al cargar postulaciones')
    }

    const appsData = await appsResponse.json()
    const applicationsBasic = appsData.applications || []

    // 2. Cargar datos completos de cada trabajo desde /api/jobs/
    const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
    const jobsResponse = await fetch(`${baseURL}/api/jobs/`)

    if (!jobsResponse.ok) {
      throw new Error('Error al cargar trabajos')
    }

    const jobsData = await jobsResponse.json()
    const jobsMap = new Map()

    // Crear un mapa de jobs por ID
    if (jobsData.success && jobsData.jobs) {
      jobsData.jobs.forEach(job => {
        jobsMap.set(job.id, job)
      })
    }

    // 3. Combinar applications con datos completos del job
    const newApplications = applicationsBasic.map(app => ({
      ...app,
      job: jobsMap.get(app.job_id) || {
        id: app.job_id,
        title: 'Trabajo no disponible',
        companyName: '-',
        city: '-'
      }
    }))

    // 4. Append o reemplazar
    if (append) {
      applications.value = [...applications.value, ...newApplications]
    } else {
      applications.value = newApplications
    }

    // 5. Verificar si hay más
    hasMore.value = applicationsBasic.length === limit.value
  } catch (error) {
    console.error('Error loading applications:', error)
  } finally {
    isLoading.value = false
    isLoadingMore.value = false
  }
}

const loadMore = () => {
  if (!hasMore.value || isLoadingMore.value) return
  currentPage.value++
  loadApplications(true)
}

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.text : status
}

const getStatusColor = (status) => {
  const colors = {
    submitted: 'info',
    reviewing: 'warning',
    shortlisted: 'success',
    interviewed: 'primary',
    rejected: 'danger',
    accepted: 'success',
    withdrawn: 'secondary'
  }
  return colors[status] || 'secondary'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()

  // Resetear horas
  now.setHours(0, 0, 0, 0)
  date.setHours(0, 0, 0, 0)

  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return 'hoy'
  if (days === 1) return 'ayer'
  if (days < 7) return `hace ${days} días`
  if (days < 30) {
    const weeks = Math.floor(days / 7)
    return `hace ${weeks} ${weeks === 1 ? 'semana' : 'semanas'}`
  }

  const months = Math.floor(days / 30)
  return `hace ${months} ${months === 1 ? 'mes' : 'meses'}`
}

const isRecent = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  return days <= 3
}

const mapApplicationToListing = (application) => {
  // El job ya viene con todos los datos desde /api/jobs/
  // Solo retornamos el objeto job directamente
  return application.job
}

const viewDetails = (application) => {
  // Navigate to job details with application info
  router.push(`/guias/trabajos?selected=${application.job.id}`)
}

const filterByStatus = (status) => {
  filterStatus.value = status
}

const withdrawApplication = (application) => {
  applicationToWithdraw.value = application
  const jobTitle = application.job?.title || 'este trabajo'
  modalMessage.value = jobTitle
  showWithdrawModal.value = true
}

const confirmWithdraw = async () => {
  showWithdrawModal.value = false

  if (!applicationToWithdraw.value) return

  try {
    const response = await fetch(`/api/applications/${applicationToWithdraw.value.id}/withdraw/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.error || 'Error al retirar postulación')
    }

    await response.json()

    // Mostrar mensaje de éxito
    showSuccessModal.value = true

    // Reload applications
    await loadApplications()
  } catch (error) {
    console.error('Error withdrawing application:', error)
    modalMessage.value = error.message
    showErrorModal.value = true
  } finally {
    applicationToWithdraw.value = null
  }
}

const cancelWithdraw = () => {
  showWithdrawModal.value = false
  applicationToWithdraw.value = null
}

const clearFilters = () => {
  filterStatus.value = null
  searchQuery.value = ''
}

const goToJobs = () => {
  router.push('/guias/trabajos')
}

// Lifecycle
onMounted(() => {
  loadApplications()

  // Configurar Intersection Observer para scroll infinito
  observer.value = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting && hasMore.value && !isLoadingMore.value) {
        loadMore()
      }
    },
    {
      rootMargin: '100px' // Cargar antes de llegar al final
    }
  )

  // Observar el elemento trigger cuando esté disponible
  if (loadMoreTrigger.value) {
    observer.value.observe(loadMoreTrigger.value)
  }
})

// Cleanup
onUnmounted(() => {
  if (observer.value) {
    observer.value.disconnect()
  }
})
</script>

<style scoped>
.applications-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  background: linear-gradient(to bottom, #f9fafb 0%, #ffffff 100%);
  min-height: 100vh;
}

/* Header mejorado */
.section-header {
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #E5E7EB;
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.section-header h1 {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.5px;
}

.subtitle {
  color: #6B7280;
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 500;
}

/* Info Banner */
.info-banner {
  display: flex;
  gap: 0.875rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  border: 1px solid #BFDBFE;
  border-left: 4px solid #3B82F6;
  border-radius: 10px;
  margin-top: 1rem;
}

.info-banner .va-icon {
  color: #3B82F6;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.info-content {
  flex: 1;
}

.info-text {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #1E40AF;
  font-weight: 500;
}

/* Loading mejorado */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  gap: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.loading-container p {
  color: #6B7280;
  font-size: 1rem;
  font-weight: 500;
}

/* Empty state mejorado */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  gap: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 2px dashed #E5E7EB;
}

.empty-state h3 {
  color: #374151;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.empty-state p {
  color: #9CA3AF;
  margin: 0;
  font-size: 1rem;
  max-width: 400px;
}

/* Stats cards mejorados */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.stat-card {
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 2px solid transparent;
}

.stat-card.clickable {
  cursor: pointer;
  user-select: none;
}

.stat-card.clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-card.clickable:active {
  transform: translateY(0);
}

.stat-card.active {
  border-width: 3px;
  transform: scale(1.02);
}

/* Card Púrpura */
.stat-card-purple {
  background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
  border-color: #ddd6fe;
}

.stat-card-purple:hover {
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.15);
  border-color: #c4b5fd;
}

/* Card Naranja */
.stat-card-orange {
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border-color: #fed7aa;
}

.stat-card-orange:hover {
  box-shadow: 0 6px 16px rgba(249, 115, 22, 0.15);
  border-color: #fdba74;
}

/* Card Verde */
.stat-card-green {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #bbf7d0;
}

.stat-card-green:hover {
  box-shadow: 0 6px 16px rgba(34, 197, 94, 0.15);
  border-color: #86efac;
}

/* Card Azul */
.stat-card-blue {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-color: #bfdbfe;
}

.stat-card-blue:hover {
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.15);
  border-color: #93c5fd;
}

/* Iconos de stats */
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon-purple {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  box-shadow: 0 4px 16px rgba(124, 58, 237, 0.3);
  color: white;
}

.stat-icon-orange {
  background: linear-gradient(135deg, #f97316, #ea580c);
  box-shadow: 0 4px 16px rgba(249, 115, 22, 0.3);
  color: white;
}

.stat-icon-green {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  box-shadow: 0 4px 16px rgba(34, 197, 94, 0.3);
  color: white;
}

.stat-icon-blue {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
  color: white;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #1F2937, #374151);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.stat-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

/* Filtros mejorados */
.filters-section {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #E5E7EB;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #F3F4F6;
}

.filters-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filters-title h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: #1F2937;
}

.btn-clear-filters {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
  color: #DC2626;
  border: 1px solid #FCA5A5;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-clear-filters:hover {
  background: linear-gradient(135deg, #FECACA 0%, #FCA5A5 100%);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.2);
}

.filters-content {
  display: grid;
  grid-template-columns: 200px 200px 1fr;
  gap: 1.5rem;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.search-group {
  flex: 1;
}

.applications-grid {
  margin-bottom: 30px;
}

.applications-grid-inner {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.application-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Animaciones de transición */
.application-list-enter-active {
  transition: all 0.4s ease;
}

.application-list-leave-active {
  transition: all 0.4s ease;
  position: absolute;
}

.application-list-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.application-list-leave-to {
  opacity: 0;
  transform: translateX(-100%) scale(0.8);
}

.application-list-move {
  transition: transform 0.4s ease;
}

/* Badges de estado */
.application-status-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  padding: 0 0.25rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-info {
  background: #DBEAFE;
  color: #1E40AF;
}

.badge-warning {
  background: #FEF3C7;
  color: #92400E;
}

.badge-success {
  background: #D1FAE5;
  color: #065F46;
}

.badge-primary {
  background: #E0E7FF;
  color: #3730A3;
}

.badge-danger {
  background: #FEE2E2;
  color: #991B1B;
}

.badge-secondary {
  background: #F3F4F6;
  color: #4B5563;
}

.badge-new {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
}

/* Footer de postulación */
.application-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  font-size: 0.8125rem;
  gap: 1rem;
}

.application-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.applied-date,
.cv-used,
.viewed-indicator {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: #6B7280;
  font-size: 0.8125rem;
}

.viewed-indicator {
  color: #7C3AED;
  background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  border: 1px solid #DDD6FE;
  font-weight: 600;
  animation: fadeIn 0.3s ease;
}

.viewed-indicator .va-icon {
  color: #7C3AED;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.btn-withdraw {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.25);
}

.btn-withdraw:hover {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35);
}

/* Scroll infinito */
.load-more-trigger {
  height: 20px;
  width: 100%;
}

.loading-more {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
  margin-top: 1rem;
}

.loading-more span {
  color: #6B7280;
  font-size: 0.9rem;
  font-weight: 500;
}

.end-of-results {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 2rem;
  margin-top: 1rem;
  background: white;
  border-radius: 12px;
  border: 2px dashed #D1FAE5;
}

.end-of-results span {
  color: #059669;
  font-size: 0.9rem;
  font-weight: 600;
}

@media (max-width: 768px) {
  .applications-view {
    padding: 1rem;
  }

  .section-header {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .section-header h1 {
    font-size: 1.5rem;
  }

  .filters-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .filters-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .btn-clear-filters {
    width: 100%;
    justify-content: center;
  }

  .applications-grid-inner {
    grid-template-columns: 1fr;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .stat-card {
    padding: 0.875rem 1rem;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
  }

  .stat-value {
    font-size: 1.25rem;
  }

  .stat-label {
    font-size: 0.7rem;
  }

  .application-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .btn-withdraw {
    width: 100%;
    justify-content: center;
  }
}

/* ========== Estilos de Modales ========== */
.modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.5rem 1rem;
  gap: 1rem;
}

.modal-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.modal-icon.warning {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  color: #D97706;
  box-shadow: 0 4px 16px rgba(217, 119, 6, 0.2);
}

.modal-icon.success {
  background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
  color: #059669;
  box-shadow: 0 4px 16px rgba(5, 150, 105, 0.2);
}

.modal-icon.error {
  background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
  color: #DC2626;
  box-shadow: 0 4px 16px rgba(220, 38, 38, 0.2);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
}

.modal-message {
  font-size: 1rem;
  color: #4B5563;
  margin: 0;
  line-height: 1.5;
}

.modal-message strong {
  color: #7C3AED;
  font-weight: 700;
}

.modal-warning {
  font-size: 0.875rem;
  color: #DC2626;
  background: #FEE2E2;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border-left: 4px solid #DC2626;
  margin: 0;
  line-height: 1.4;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  width: 100%;
}

.modal-actions .va-button {
  min-width: 140px;
}

/* ========== Tema Púrpura para Modal de Retirar ========== */
.modal-icon.withdraw {
  background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
  color: #9333EA;
  box-shadow: 0 4px 16px rgba(147, 51, 234, 0.2);
}

.modal-warning {
  font-size: 0.875rem;
  color: #7C3AED;
  background: linear-gradient(135deg, #FAF5FF 0%, #F3E8FF 100%);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border-left: 4px solid #9333EA;
  margin: 0;
  line-height: 1.4;
}

.btn-modal-cancel {
  background: linear-gradient(135deg, #FDE68A 0%, #FCD34D 100%);
  color: #92400E;
  border: 1px solid #FBBF24;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 140px;
  box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
}

.btn-modal-cancel:hover {
  background: linear-gradient(135deg, #FCD34D 0%, #FBBF24 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
}

.btn-modal-withdraw {
  background: linear-gradient(135deg, #A855F7 0%, #9333EA 100%);
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(168, 85, 247, 0.3);
  min-width: 140px;
}

.btn-modal-withdraw:hover {
  background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.4);
}
</style>
