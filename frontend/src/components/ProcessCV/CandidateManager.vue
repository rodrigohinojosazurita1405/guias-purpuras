<!-- frontend/src/components/Process/CandidateManager.vue -->
<template>
  <div class="candidate-manager">
    <!-- Header -->
    <div class="manager-header">
      <div class="header-info">
        <h2>Gestor de Candidatos</h2>
        <p class="job-title" v-if="jobTitle">{{ jobTitle }}</p>
      </div>
      <div class="header-stats">
        <div class="stat">
          <span class="stat-value">{{ totalApplications }}</span>
          <span class="stat-label">Aplicaciones</span>
        </div>
        <div class="stat">
          <span class="stat-value">{{ reviewingCount }}</span>
          <span class="stat-label">En revisión</span>
        </div>
        <div class="stat">
          <span class="stat-value">{{ shortlistedCount }}</span>
          <span class="stat-label">Preseleccionados</span>
        </div>
      </div>
    </div>

    <!-- Controls -->
    <div class="manager-controls">
      <div class="search-box">
        <va-icon name="search" size="small" />
        <va-input
          v-model="searchQuery"
          placeholder="Buscar por nombre o email..."
          class="search-input"
        />
      </div>

      <div class="filter-group">
        <label class="filter-label">Filtrar por estado:</label>
        <va-select
          v-model="selectedStatus"
          :options="statusOptions"
          value-by="value"
          text-by="label"
          class="status-filter"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <va-progress-bar indeterminate color="purple" />
      <p>Cargando candidatos...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <va-icon name="error" size="3rem" color="danger" />
      <p>{{ error }}</p>
      <va-button @click="loadApplications" color="purple">
        Reintentar
      </va-button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredApplications.length === 0" class="empty-state">
      <va-icon name="person_add" size="3rem" color="textSecondary" />
      <p>No hay candidatos</p>
      <small>Los candidatos aparecerán aquí cuando postulen a este empleo</small>
    </div>

    <!-- Applications List -->
    <div v-else class="applications-list">
      <div
        v-for="application in filteredApplications"
        :key="application.id"
        class="application-card"
      >
        <!-- Card Header -->
        <div class="card-header">
          <div class="applicant-info">
            <div class="applicant-avatar">
              {{ getInitials(application.applicantName) }}
            </div>
            <div class="applicant-details">
              <h3 class="applicant-name">{{ application.applicantName }}</h3>
              <p class="applicant-email">{{ application.applicantEmail }}</p>
              <span class="application-date">
                Aplicó hace {{ getRelativeDate(application.createdAt) }}
              </span>
            </div>
          </div>

          <div class="card-actions">
            <va-chip
              :color="getStatusColor(application.status)"
              :text-color="getStatusTextColor(application.status)"
              size="small"
              class="status-chip"
            >
              {{ getStatusLabel(application.status) }}
            </va-chip>
            <va-button
              preset="plain"
              color="purple"
              @click="toggleExpanded(application.id)"
              size="small"
            >
              <va-icon :name="expandedId === application.id ? 'expand_less' : 'expand_more'" />
            </va-button>
          </div>
        </div>

        <!-- Card Body (Expandable) -->
        <div v-if="expandedId === application.id" class="card-body">
          <!-- Contact Information -->
          <div class="section">
            <h4 class="section-title">Información de Contacto</h4>
            <div class="contact-grid">
              <div class="contact-item" v-if="application.applicantPhone">
                <span class="contact-label">Teléfono:</span>
                <span class="contact-value">{{ application.applicantPhone }}</span>
              </div>
              <div class="contact-item" v-if="application.applicantWhatsapp">
                <span class="contact-label">WhatsApp:</span>
                <a :href="`https://wa.me/${application.applicantWhatsapp}`" target="_blank" class="contact-link">
                  {{ application.applicantWhatsapp }}
                </a>
              </div>
            </div>
          </div>

          <!-- Screening Answers -->
          <div v-if="Object.keys(application.screeningAnswers).length > 0" class="section">
            <h4 class="section-title">Respuestas a Preguntas</h4>
            <div class="answers-list">
              <div
                v-for="(answer, questionIdx) in application.screeningAnswers"
                :key="questionIdx"
                class="answer-item"
              >
                <p class="answer-question">Pregunta {{ parseInt(questionIdx) + 1 }}</p>
                <p class="answer-text">{{ answer }}</p>
              </div>
            </div>
          </div>

          <!-- Status and Notes -->
          <div class="section">
            <h4 class="section-title">Seguimiento</h4>

            <div class="status-selector">
              <label class="selector-label">Cambiar estado:</label>
              <div class="status-buttons">
                <va-button
                  v-for="status in statusOptions"
                  :key="status.value"
                  :preset="application.status === status.value ? 'solid' : 'plain'"
                  :color="application.status === status.value ? 'purple' : 'textSecondary'"
                  size="small"
                  @click="updateApplicationStatus(application.id, status.value)"
                  :disabled="updating"
                >
                  {{ status.label }}
                </va-button>
              </div>
            </div>

            <div class="notes-section">
              <label class="notes-label">Notas del Reclutador:</label>
              <va-textarea
                v-model="application.recruiterNotes"
                placeholder="Añade tus notas sobre este candidato..."
                rows="3"
                class="notes-textarea"
                @blur="saveRecruiterNotes(application.id)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vuestic-ui'

// ========== PROPS ==========
const props = defineProps({
  jobId: {
    type: String,
    required: true
  }
})

// ========== COMPOSABLES ==========
const { init: notify } = useToast()

// ========== DATA ==========
const loading = ref(true)
const error = ref(null)
const updating = ref(false)
const applications = ref([])
const jobTitle = ref('')
const searchQuery = ref('')
const selectedStatus = ref('all')
const expandedId = ref(null)

const statusOptions = [
  { label: 'Todas', value: 'all' },
  { label: 'Recibida', value: 'received' },
  { label: 'En revisión', value: 'reviewing' },
  { label: 'Preseleccionada', value: 'shortlisted' },
  { label: 'Aceptada', value: 'accepted' },
  { label: 'Rechazada', value: 'rejected' }
]

// ========== COMPUTED ==========
const filteredApplications = computed(() => {
  let filtered = applications.value

  // Filter by status
  if (selectedStatus.value !== 'all') {
    filtered = filtered.filter(app => app.status === selectedStatus.value)
  }

  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(app =>
      app.applicantName.toLowerCase().includes(query) ||
      app.applicantEmail.toLowerCase().includes(query)
    )
  }

  return filtered
})

const totalApplications = computed(() => applications.value.length)

const reviewingCount = computed(
  () => applications.value.filter(app => app.status === 'reviewing').length
)

const shortlistedCount = computed(
  () => applications.value.filter(app => app.status === 'shortlisted').length
)

// ========== LIFECYCLE ==========
onMounted(() => {
  loadApplications()
})

// ========== METHODS ==========
const loadApplications = async () => {
  try {
    loading.value = true
    error.value = null

    const response = await fetch(`/api/jobs/${props.jobId}/applications`)

    if (!response.ok) {
      throw new Error('Error al cargar candidatos')
    }

    const data = await response.json()
    if (data.success) {
      applications.value = data.applications
      jobTitle.value = data.jobTitle
    }
  } catch (err) {
    error.value = err.message
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    loading.value = false
  }
}

const updateApplicationStatus = async (applicationId, newStatus) => {
  try {
    updating.value = true
    const response = await fetch(
      `/api/jobs/${props.jobId}/applications/${applicationId}`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          status: newStatus
        })
      }
    )

    if (!response.ok) {
      throw new Error('Error al actualizar estado')
    }

    const data = await response.json()
    if (data.success) {
      // Update local state
      const app = applications.value.find(a => a.id === applicationId)
      if (app) {
        app.status = newStatus
      }

      notify({
        message: 'Estado actualizado',
        color: 'success',
        duration: 3000
      })
    }
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    updating.value = false
  }
}

const saveRecruiterNotes = async (applicationId) => {
  try {
    const app = applications.value.find(a => a.id === applicationId)
    if (!app) return

    const response = await fetch(
      `/api/jobs/${props.jobId}/applications/${applicationId}`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          recruiterNotes: app.recruiterNotes
        })
      }
    )

    if (!response.ok) {
      throw new Error('Error al guardar notas')
    }

    notify({
      message: '✅ Notas guardadas',
      color: 'success',
      duration: 2000
    })
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  }
}

const toggleExpanded = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getRelativeDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffMinutes = Math.floor(diffMs / (1000 * 60))

  if (diffMinutes < 1) return 'hace unos segundos'
  if (diffMinutes < 60) return `hace ${diffMinutes} minutos`
  if (diffHours < 24) return `hace ${diffHours} horas`
  if (diffDays < 30) return `hace ${diffDays} días`

  return date.toLocaleDateString()
}

const getStatusLabel = (status) => {
  const labels = {
    received: 'Recibida',
    reviewing: 'En revisión',
    shortlisted: 'Preseleccionada',
    accepted: 'Aceptada',
    rejected: 'Rechazada',
    withdrawn: 'Retirada'
  }
  return labels[status] || status
}

const getStatusColor = (status) => {
  const colors = {
    received: '#e8e8e8',
    reviewing: '#fff3cd',
    shortlisted: '#d4edda',
    accepted: '#90ee90',
    rejected: '#ffcccc',
    withdrawn: '#e2e3e5'
  }
  return colors[status] || '#e8e8e8'
}

const getStatusTextColor = (status) => {
  const colors = {
    received: '#666',
    reviewing: '#856404',
    shortlisted: '#155724',
    accepted: '#006400',
    rejected: '#721c24',
    withdrawn: '#383d41'
  }
  return colors[status] || '#666'
}
</script>

<style scoped>
/* ========== CONTAINER ========== */
.candidate-manager {
  padding: 2rem;
  background: #f5f5f5;
  min-height: 100vh;
}

/* ========== HEADER ========== */
.manager-header {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.header-info h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.75rem;
  color: #333;
}

.job-title {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

.header-stats {
  display: flex;
  gap: 2rem;
}

.stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #5C0099;
  margin-bottom: 0.25rem;
}

.stat-label {
  display: block;
  font-size: 0.85rem;
  color: #666;
}

/* ========== CONTROLS ========== */
.manager-controls {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  display: flex;
  gap: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #f8f8f8;
  border-radius: 8px;
}

.search-input {
  flex: 1;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.filter-label {
  font-weight: 600;
  color: #333;
  white-space: nowrap;
}

.status-filter {
  min-width: 150px;
}

/* ========== STATES ========== */
.loading-state,
.error-state,
.empty-state {
  background: white;
  padding: 4rem 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.error-state p,
.empty-state p {
  margin: 1rem 0;
  font-size: 1.1rem;
  color: #666;
}

.empty-state small {
  display: block;
  color: #999;
  margin-bottom: 1.5rem;
}

/* ========== APPLICATIONS LIST ========== */
.applications-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.application-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.application-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.card-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fafafa;
  border-bottom: 1px solid #eee;
}

.applicant-info {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.applicant-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #5C0099 0%, #3D0066 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}

.applicant-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.applicant-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
}

.applicant-email {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  color: #666;
}

.application-date {
  font-size: 0.8rem;
  color: #999;
  margin-top: 0.25rem;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-chip {
  font-weight: 600;
  padding: 0.5rem 0.75rem;
}

.card-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ========== SECTIONS ========== */
.section {
  border: 1px solid #eee;
  padding: 1.5rem;
  border-radius: 8px;
  background: #fafafa;
}

.section-title {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* ========== CONTACT INFORMATION ========== */
.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.contact-item {
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  border: 1px solid #eee;
}

.contact-label {
  display: block;
  font-weight: 600;
  color: #666;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.contact-value,
.contact-link {
  display: block;
  color: #333;
  font-size: 0.95rem;
}

.contact-link {
  color: #5C0099;
  text-decoration: none;
  transition: color 0.2s;
}

.contact-link:hover {
  color: #3D0066;
  text-decoration: underline;
}

/* ========== SCREENING ANSWERS ========== */
.answers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.answer-item {
  padding: 1rem;
  background: white;
  border-radius: 6px;
  border-left: 4px solid #5C0099;
}

.answer-question {
  margin: 0 0 0.5rem 0;
  font-weight: 600;
  color: #5C0099;
  font-size: 0.9rem;
}

.answer-text {
  margin: 0;
  color: #333;
  line-height: 1.5;
}

/* ========== STATUS AND NOTES ========== */
.status-selector {
  margin-bottom: 1.5rem;
}

.selector-label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.75rem;
}

.status-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.notes-section {
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.notes-label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.75rem;
}

.notes-textarea {
  width: 100%;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .candidate-manager {
    padding: 1rem;
  }

  .manager-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .header-stats {
    width: 100%;
    justify-content: space-around;
  }

  .manager-controls {
    flex-direction: column;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .card-actions {
    align-self: flex-start;
  }

  .contact-grid {
    grid-template-columns: 1fr;
  }

  .status-buttons {
    justify-content: center;
  }
}
</style>
