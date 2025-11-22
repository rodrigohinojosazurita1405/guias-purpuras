<!-- frontend/src/components/Dashboard/CandidatesView.vue -->
<template>
  <div class="candidates-view">
    <!-- Header -->
    <div class="section-header">
      <h2>Base de Talento</h2>
      <p class="section-subtitle">Gestiona todos los candidatos de tus publicaciones</p>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid" v-if="!applicationMgr.isLoading">
      <div class="stat-card">
        <div class="stat-icon total">
          <va-icon name="people" />
        </div>
        <div class="stat-content">
          <h3>Total de Candidatos</h3>
          <div class="stat-number">{{ applicationMgr.totalApplications }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon received">
          <va-icon name="mail" />
        </div>
        <div class="stat-content">
          <h3>Recibidas</h3>
          <div class="stat-number">{{ applicationMgr.receivedCount }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon reviewing">
          <va-icon name="visibility" />
        </div>
        <div class="stat-content">
          <h3>En Revisión</h3>
          <div class="stat-number">{{ applicationMgr.reviewingCount }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon shortlisted">
          <va-icon name="check_circle" />
        </div>
        <div class="stat-content">
          <h3>Preseleccionados</h3>
          <div class="stat-number">{{ applicationMgr.shortlistedCount }}</div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <div class="search-box">
        <va-icon name="search" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar candidato o trabajo..."
          class="search-input"
        />
      </div>

      <select v-model="filterStatus" class="filter-select">
        <option value="">Todos los estados</option>
        <option value="received">Recibida</option>
        <option value="reviewing">En revisión</option>
        <option value="shortlisted">Preseleccionado</option>
        <option value="accepted">Aceptado</option>
        <option value="rejected">Rechazado</option>
      </select>
    </div>

    <!-- Loading State -->
    <div v-if="applicationMgr.isLoading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
      <p>Cargando candidatos...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="applicationMgr.error" class="error-state">
      <va-icon name="error" size="3rem" color="danger" />
      <p>{{ applicationMgr.error }}</p>
      <button @click="applicationMgr.loadApplications()" class="retry-btn">
        <va-icon name="refresh" />
        Reintentar
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredApplications.length === 0" class="empty-state">
      <va-icon name="person_add" size="3rem" />
      <h3>No hay candidatos</h3>
      <p>Los candidatos aparecerán aquí cuando postulen a tus publicaciones</p>
    </div>

    <!-- Applications List -->
    <div v-else class="applications-list">
      <div
        v-for="application in filteredApplications"
        :key="application.id"
        class="application-card"
        :class="`status-${application.status}`"
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
              <p class="job-title">Puesto: {{ application.jobTitle }}</p>
              <span class="application-date">
                Aplicó {{ formatRelativeDate(application.createdAt) }}
              </span>
            </div>
          </div>

          <div class="card-actions">
            <div class="status-badge" :class="`status-${application.status}`">
              {{ getStatusLabel(application.status) }}
            </div>
            <button
              @click="toggleExpanded(application.id)"
              class="expand-btn"
            >
              <va-icon :name="expandedId === application.id ? 'expand_less' : 'expand_more'" />
            </button>
          </div>
        </div>

        <!-- Card Body (Expandable) -->
        <div v-if="expandedId === application.id" class="card-body">
          <!-- Contact Information -->
          <div class="section">
            <h4 class="section-title">Información de Contacto</h4>
            <div class="contact-grid">
              <div v-if="application.applicantPhone" class="contact-item">
                <span class="contact-label">Teléfono:</span>
                <span class="contact-value">{{ application.applicantPhone }}</span>
              </div>
              <div v-if="application.applicantWhatsapp" class="contact-item">
                <span class="contact-label">WhatsApp:</span>
                <a
                  :href="`https://wa.me/${application.applicantWhatsapp}`"
                  target="_blank"
                  class="contact-link"
                >
                  {{ application.applicantWhatsapp }}
                </a>
              </div>
            </div>
          </div>

          <!-- Change Status -->
          <div class="section">
            <h4 class="section-title">Cambiar Estado</h4>
            <div class="status-buttons">
              <button
                v-for="status in statusOptions"
                :key="status"
                @click="changeStatus(application, status)"
                class="status-btn"
                :class="{ active: application.status === status }"
                :disabled="updating"
              >
                {{ getStatusLabel(status) }}
              </button>
            </div>
          </div>

          <!-- Notes -->
          <div class="section">
            <h4 class="section-title">Notas del Reclutador</h4>
            <textarea
              v-model="application.recruiterNotes"
              @blur="saveNotes(application)"
              placeholder="Añade tus notas sobre este candidato..."
              class="notes-textarea"
              :disabled="updating"
            ></textarea>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vuestic-ui'
import { useApplications } from '@/composables/useApplications'

// ========== COMPOSABLES ==========
const { init: notify } = useToast()
const applicationMgr = useApplications()

// ========== DATA ==========
const searchQuery = ref('')
const filterStatus = ref('')
const expandedId = ref(null)
const updating = ref(false)

const statusOptions = ['received', 'reviewing', 'shortlisted', 'accepted', 'rejected']

// ========== COMPUTED ==========
const filteredApplications = computed(() => {
  let filtered = applicationMgr.applications.value

  // Filter by status
  if (filterStatus.value) {
    filtered = filtered.filter(app => app.status === filterStatus.value)
  }

  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(app =>
      app.applicantName.toLowerCase().includes(query) ||
      app.applicantEmail.toLowerCase().includes(query) ||
      app.jobTitle.toLowerCase().includes(query)
    )
  }

  return filtered
})

// ========== LIFECYCLE ==========
onMounted(() => {
  // Solo cargar si aún no se han cargado (evitar bucle infinito)
  if (!applicationMgr.isLoaded.value) {
    applicationMgr.loadApplications()
  }
})

// ========== METHODS ==========
const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const formatRelativeDate = (dateString) => {
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

  return date.toLocaleDateString('es-ES')
}

const getStatusLabel = (status) => {
  const labels = {
    received: 'Recibida',
    reviewing: 'En revisión',
    shortlisted: 'Preseleccionado',
    accepted: 'Aceptado',
    rejected: 'Rechazado',
    withdrawn: 'Retirada'
  }
  return labels[status] || status
}

const toggleExpanded = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

const changeStatus = async (application, newStatus) => {
  try {
    updating.value = true
    await applicationMgr.updateApplicationStatus(
      application.jobId,
      application.id,
      newStatus
    )

    notify({
      message: `✅ Estado actualizado a ${getStatusLabel(newStatus)}`,
      color: 'success',
      duration: 3000
    })
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

const saveNotes = async (application) => {
  try {
    updating.value = true
    await applicationMgr.saveRecruiterNotes(
      application.jobId,
      application.id,
      application.recruiterNotes || ''
    )

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
  } finally {
    updating.value = false
  }
}
</script>

<style scoped>
.candidates-view {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* ========== HEADER ========== */
.section-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #E4E7EC;
}

.section-header h2 {
  margin: 0 0 0.5rem;
  font-size: 2rem;
  font-weight: 700;
  color: #1F2937;
}

.section-subtitle {
  margin: 0;
  font-size: 0.95rem;
  color: #6B7280;
  font-weight: 500;
}

/* ========== STATS GRID ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #E4E7EC;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 8px;
  color: white;
  font-size: 1.5rem;
}

.stat-icon.total {
  background: var(--color-purple);
}

.stat-icon.received {
  background: #3B82F6;
}

.stat-icon.reviewing {
  background: #F59E0B;
}

.stat-icon.shortlisted {
  background: #10B981;
}

.stat-content h3 {
  margin: 0;
  font-size: 0.8rem;
  color: #6B7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-number {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0.5rem 0 0;
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
  border: 1px solid #E4E7EC;
  border-radius: 8px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 0.95rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #E4E7EC;
  border-radius: 8px;
  background: white;
  font-size: 0.95rem;
  cursor: pointer;
}

/* ========== STATES ========== */
.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #E4E7EC;
}

.empty-state h3 {
  margin: 1rem 0 0.5rem;
  font-size: 1.25rem;
  color: #1F2937;
}

.empty-state p {
  margin: 0 0 1.5rem;
  color: #6B7280;
}

.retry-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-purple);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.retry-btn:hover {
  background: #5b21b6;
  transform: translateY(-2px);
}

/* ========== APPLICATIONS LIST ========== */
.applications-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.application-card {
  background: white;
  border-radius: 8px;
  border: 1px solid #E4E7EC;
  overflow: hidden;
  transition: all 0.2s;
}

.application-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #F9FAFB;
  border-bottom: 1px solid #E4E7EC;
}

.applicant-info {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.applicant-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
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
  color: #1F2937;
}

.applicant-email {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  color: #6B7280;
}

.job-title {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: #9CA3AF;
  font-weight: 500;
}

.application-date {
  font-size: 0.8rem;
  color: #9CA3AF;
  margin-top: 0.25rem;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge.status-received {
  background: #DBEAFE;
  color: #1E40AF;
}

.status-badge.status-reviewing {
  background: #FEF3C7;
  color: #92400E;
}

.status-badge.status-shortlisted {
  background: #DCFCE7;
  color: #15803D;
}

.status-badge.status-accepted {
  background: #D1FAE5;
  color: #065F46;
}

.status-badge.status-rejected {
  background: #FEE2E2;
  color: #991B1B;
}

.expand-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6B7280;
  transition: color 0.2s;
}

.expand-btn:hover {
  color: var(--color-purple);
}

.card-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: #FAFAFA;
}

.section {
  padding: 1rem;
  background: white;
  border-radius: 6px;
  border: 1px solid #E4E7EC;
}

.section-title {
  margin: 0 0 1rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1F2937;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
}

.contact-item {
  padding: 0.75rem;
  background: #F3F4F6;
  border-radius: 4px;
}

.contact-label {
  display: block;
  font-size: 0.8rem;
  color: #6B7280;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.contact-value,
.contact-link {
  display: block;
  font-size: 0.9rem;
  color: #1F2937;
}

.contact-link {
  color: var(--color-purple);
  text-decoration: none;
  transition: color 0.2s;
}

.contact-link:hover {
  color: #5b21b6;
  text-decoration: underline;
}

.status-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.status-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #E4E7EC;
  border-radius: 6px;
  background: white;
  color: #6B7280;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
}

.status-btn:hover:not(:disabled) {
  border-color: var(--color-purple);
  color: var(--color-purple);
}

.status-btn.active {
  background: var(--color-purple);
  border-color: var(--color-purple);
  color: white;
}

.status-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.notes-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #E4E7EC;
  border-radius: 6px;
  font-size: 0.9rem;
  font-family: inherit;
  resize: vertical;
  min-height: 100px;
}

.notes-textarea:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .candidates-view {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }

  .filter-bar {
    flex-direction: column;
  }

  .search-box {
    min-width: 100%;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .card-actions {
    width: 100%;
    justify-content: space-between;
  }

  .contact-grid {
    grid-template-columns: 1fr;
  }

  .status-buttons {
    justify-content: flex-start;
  }
}
</style>
