<template>
  <div class="shortlisted-view">
    <div class="section-header">
      <h1>Trabajos Guardados (Favoritos)</h1>
      <p class="subtitle">Trabajos que has guardado para revisar más tarde</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <va-progress-circle indeterminate color="purple" />
      <p>Cargando trabajos guardados...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!isLoading && savedJobs.length === 0" class="empty-state">
      <va-icon name="bookmark_border" size="4rem" color="#ccc" />
      <h3>No tienes trabajos guardados</h3>
      <p>Guarda trabajos que te interesen para revisarlos más tarde</p>
      <va-button color="purple" @click="goToJobs">Buscar Trabajos</va-button>
    </div>

    <!-- Saved Jobs List -->
    <div v-else class="saved-jobs-list">
      <!-- Search Bar -->
      <div class="search-bar">
        <va-input
          v-model="searchQuery"
          placeholder="Buscar por título o empresa..."
          clearable
        >
          <template #prepend>
            <va-icon name="search" />
          </template>
        </va-input>
      </div>

      <!-- Jobs Grid -->
      <div class="jobs-grid">
        <div
          v-for="savedJob in filteredJobs"
          :key="savedJob.saved_id"
          class="job-card"
        >
          <div class="card-header">
            <div class="job-title-section">
              <h3>{{ savedJob.job.title }}</h3>
              <p class="company">{{ savedJob.job.company }}</p>
            </div>
            <va-button
              icon="bookmark"
              color="purple"
              preset="plain"
              @click="unsaveJob(savedJob)"
              title="Quitar de guardados"
            />
          </div>

          <div class="card-body">
            <div class="info-row">
              <va-icon name="location_on" size="small" color="#666" />
              <span>{{ savedJob.job.city }}</span>
            </div>
            <div class="info-row">
              <va-icon name="work" size="small" color="#666" />
              <span>{{ getModalityLabel(savedJob.job.modality) }}</span>
            </div>
            <div class="info-row">
              <va-icon name="payments" size="small" color="#666" />
              <span>{{ getSalaryLabel(savedJob.job.salary_type) }}</span>
            </div>
            <div class="info-row">
              <va-icon name="schedule" size="small" color="#666" />
              <span>Guardado: {{ formatDate(savedJob.saved_at) }}</span>
            </div>
            <div v-if="savedJob.job.expiry_date" class="info-row">
              <va-icon name="event" size="small" color="#666" />
              <span>Expira: {{ formatDate(savedJob.job.expiry_date) }}</span>
            </div>
          </div>

          <div class="card-footer">
            <va-button
              size="small"
              color="purple"
              @click="viewJob(savedJob.job.id)"
            >
              Ver Detalles
            </va-button>
            <va-button
              size="small"
              color="success"
              @click="applyToJob(savedJob.job.id)"
            >
              Postular Ahora
            </va-button>
          </div>

          <!-- Status Badge -->
          <div v-if="savedJob.job.status !== 'active'" class="status-badge">
            <va-badge :text="getJobStatusLabel(savedJob.job.status)" color="warning" />
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <va-pagination
          v-model="currentPage"
          :pages="totalPages"
          :visible-pages="5"
          @update:model-value="loadSavedJobs"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'

const router = useRouter()
const authStore = useAuthStore()
const { init: initToast } = useToast()

// State
const savedJobs = ref([])
const isLoading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const limit = ref(12)
const searchQuery = ref('')

// Computed
const filteredJobs = computed(() => {
  if (!searchQuery.value) {
    return savedJobs.value
  }

  const query = searchQuery.value.toLowerCase()
  return savedJobs.value.filter(saved =>
    saved.job.title.toLowerCase().includes(query) ||
    saved.job.company.toLowerCase().includes(query)
  )
})

// Methods
const loadSavedJobs = async () => {
  isLoading.value = true

  try {
    const offset = (currentPage.value - 1) * limit.value
    const response = await fetch(`/api/saved-jobs/?limit=${limit.value}&offset=${offset}`, {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (!response.ok) {
      throw new Error('Error al cargar trabajos guardados')
    }

    const data = await response.json()
    savedJobs.value = data.saved_jobs || []
    totalPages.value = Math.ceil((data.total || 0) / limit.value)
  } catch (error) {
    console.error('Error loading saved jobs:', error)
    initToast({
      message: 'Error al cargar trabajos guardados',
      color: 'danger',
      duration: 3000
    })
  } finally {
    isLoading.value = false
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

    initToast({
      message: 'Trabajo quitado de guardados',
      color: 'success',
      duration: 2500
    })
  } catch (error) {
    console.error('Error unsaving job:', error)
    initToast({
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

const getModalityLabel = (modality) => {
  const labels = {
    presencial: 'Presencial',
    remoto: 'Remoto',
    hibrido: 'Híbrido'
  }
  return labels[modality] || modality
}

const getSalaryLabel = (salaryType) => {
  const labels = {
    monthly: 'Mensual',
    hourly: 'Por hora',
    negotiable: 'A convenir',
    fixed: 'Fijo',
    pretension_salarial: 'Pretensión Salarial'
  }
  return labels[salaryType] || salaryType
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

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-BO', { year: 'numeric', month: 'short', day: 'numeric' })
}

// Lifecycle
onMounted(() => {
  loadSavedJobs()
})
</script>

<style scoped>
.shortlisted-view {
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

.search-bar {
  margin-bottom: 25px;
  max-width: 500px;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.job-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  transition: all 0.3s ease;
  position: relative;
}

.job-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 15px;
}

.job-title-section h3 {
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

.status-badge {
  position: absolute;
  top: 15px;
  right: 15px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

@media (max-width: 768px) {
  .jobs-grid {
    grid-template-columns: 1fr;
  }
}
</style>
