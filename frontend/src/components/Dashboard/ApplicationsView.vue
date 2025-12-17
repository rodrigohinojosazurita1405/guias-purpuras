<template>
  <div class="applications-view">
    <div class="section-header">
      <h1>Mis Postulaciones</h1>
      <p class="subtitle">Aquí puedes ver todas tus postulaciones y su estado actual</p>
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
        <div class="stat-card">
          <va-icon name="send" color="purple" />
          <div class="stat-info">
            <span class="stat-value">{{ stats.total }}</span>
            <span class="stat-label">Total</span>
          </div>
        </div>
        <div class="stat-card">
          <va-icon name="schedule" color="orange" />
          <div class="stat-info">
            <span class="stat-value">{{ stats.reviewing }}</span>
            <span class="stat-label">En Revisión</span>
          </div>
        </div>
        <div class="stat-card">
          <va-icon name="star" color="green" />
          <div class="stat-info">
            <span class="stat-value">{{ stats.shortlisted }}</span>
            <span class="stat-label">Pre-seleccionado</span>
          </div>
        </div>
        <div class="stat-card">
          <va-icon name="check_circle" color="blue" />
          <div class="stat-info">
            <span class="stat-value">{{ stats.interviewed }}</span>
            <span class="stat-label">Entrevistado</span>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters-row">
        <va-select
          v-model="filterStatus"
          label="Filtrar por estado"
          :options="statusOptions"
          placeholder="Todos"
          clearable
        />
        <va-input
          v-model="searchQuery"
          placeholder="Buscar por trabajo o empresa..."
          clearable
        >
          <template #prepend>
            <va-icon name="search" />
          </template>
        </va-input>
      </div>

      <!-- Applications Cards -->
      <div class="applications-grid">
        <div
          v-for="application in filteredApplications"
          :key="application.id"
          class="application-card"
        >
          <div class="card-header">
            <div class="job-info">
              <h3>{{ application.job_title }}</h3>
              <p class="company">{{ application.company_name }}</p>
            </div>
            <va-badge :text="getStatusLabel(application.status)" :color="getStatusColor(application.status)" />
          </div>

          <div class="card-body">
            <div class="info-row">
              <va-icon name="location_on" size="small" color="#666" />
              <span>{{ application.job_city || 'No especificado' }}</span>
            </div>
            <div class="info-row">
              <va-icon name="schedule" size="small" color="#666" />
              <span>Postulado: {{ formatDate(application.applied_at) }}</span>
            </div>
            <div v-if="application.updated_at !== application.applied_at" class="info-row">
              <va-icon name="update" size="small" color="#666" />
              <span>Actualizado: {{ formatDate(application.updated_at) }}</span>
            </div>
            <div class="info-row">
              <va-icon name="description" size="small" color="#666" />
              <span>CV: {{ application.cv_name || 'Sin CV' }}</span>
            </div>
          </div>

          <div class="card-footer">
            <va-button size="small" @click="viewDetails(application)">
              Ver Detalles
            </va-button>
            <va-button
              v-if="application.status === 'submitted'"
              size="small"
              color="danger"
              preset="plain"
              @click="withdrawApplication(application)"
            >
              Retirar
            </va-button>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <va-pagination
          v-model="currentPage"
          :pages="totalPages"
          :visible-pages="5"
          @update:model-value="loadApplications"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

const router = useRouter()
const authStore = useAuthStore()

// State
const applications = ref([])
const isLoading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const limit = ref(12)
const filterStatus = ref(null)
const searchQuery = ref('')

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
  let filtered = applications.value

  // Filter by status
  if (filterStatus.value) {
    filtered = filtered.filter(a => a.status === filterStatus.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(a =>
      a.job_title.toLowerCase().includes(query) ||
      a.company_name.toLowerCase().includes(query)
    )
  }

  return filtered
})

// Methods
const loadApplications = async () => {
  isLoading.value = true

  try {
    const offset = (currentPage.value - 1) * limit.value
    const response = await fetch(`/api/applications/?limit=${limit.value}&offset=${offset}`, {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (!response.ok) {
      throw new Error('Error al cargar postulaciones')
    }

    const data = await response.json()
    applications.value = data.applications || []
    totalPages.value = Math.ceil((data.total || 0) / limit.value)
  } catch (error) {
    console.error('Error loading applications:', error)
  } finally {
    isLoading.value = false
  }
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
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return 'Hoy'
  if (days === 1) return 'Ayer'
  if (days < 7) return `Hace ${days} días`
  if (days < 30) return `Hace ${Math.floor(days / 7)} semanas`

  return date.toLocaleDateString('es-BO', { year: 'numeric', month: 'short', day: 'numeric' })
}

const viewDetails = (application) => {
  // Navigate to job details with application info
  router.push(`/guias/trabajos?selected=${application.job_id}`)
}

const withdrawApplication = async (application) => {
  if (!confirm('¿Estás seguro de que deseas retirar esta postulación?')) {
    return
  }

  try {
    const response = await fetch(`/api/applications/${application.id}/withdraw/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Error al retirar postulación')
    }

    // Reload applications
    await loadApplications()
  } catch (error) {
    console.error('Error withdrawing application:', error)
    alert('Error al retirar la postulación')
  }
}

const goToJobs = () => {
  router.push('/guias/trabajos')
}

// Lifecycle
onMounted(() => {
  loadApplications()
})
</script>

<style scoped>
.applications-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.section-header {
  margin-bottom: 30px;
}

.section-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
}

.subtitle {
  color: #666;
  margin: 0;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  gap: 15px;
}

.empty-state h3 {
  color: #666;
  margin: 0;
}

.empty-state p {
  color: #999;
  margin: 0;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #333;
}

.stat-label {
  font-size: 13px;
  color: #666;
}

.filters-row {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 15px;
  margin-bottom: 25px;
}

.applications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.application-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  transition: all 0.3s ease;
}

.application-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 15px;
}

.job-info h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 5px 0;
}

.company {
  color: #7c3aed;
  font-weight: 500;
  margin: 0;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.card-footer {
  display: flex;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

@media (max-width: 768px) {
  .filters-row {
    grid-template-columns: 1fr;
  }

  .applications-grid {
    grid-template-columns: 1fr;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
