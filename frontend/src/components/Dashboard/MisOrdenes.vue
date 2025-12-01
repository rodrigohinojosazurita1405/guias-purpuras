<!-- frontend/src/components/Dashboard/MisOrdenes.vue -->
<template>
  <div class="mis-ordenes-container">
    <!-- Header -->
    <div class="section-header">
      <h2>Mis Órdenes</h2>
      <p class="section-subtitle">Historial de compras de planes y facturas</p>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="search-box">
        <va-icon name="search" />
        <va-input
          v-model="searchQuery"
          placeholder="Buscar por título o empresa..."
          type="text"
          clearable
          class="search-input"
        />
      </div>

      <div class="filter-controls">
        <va-select
          v-model="filterStatus"
          :options="statusOptions"
          placeholder="Estado de aplicación"
          clearable
          class="filter-select"
        />

        <va-select
          v-model="sortBy"
          :options="sortOptions"
          placeholder="Ordenar por"
          class="filter-select"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
      <p>Cargando tus aplicaciones...</p>
    </div>

    <!-- Applications List -->
    <div v-else-if="filteredApplications.length > 0" class="applications-list">
      <div
        v-for="app in filteredApplications"
        :key="app.id"
        class="application-card"
        :class="[`status-${app.status}`]"
      >
        <!-- Header with Status -->
        <div class="card-header">
          <div class="job-info">
            <h3 class="job-title">{{ app.jobTitle }}</h3>
            <p class="company-name">{{ app.companyName }}</p>
          </div>
          <div class="status-badge" :class="'status-' + app.status">
            <va-icon :name="getStatusIcon(app.status)" size="small" />
            <span>{{ getStatusLabel(app.status) }}</span>
          </div>
        </div>

        <!-- Job Details -->
        <div class="job-details">
          <div class="detail-item">
            <va-icon name="location_on" size="small" />
            <span>{{ app.jobCity }}</span>
          </div>
          <div class="detail-item">
            <va-icon name="work" size="small" />
            <span>{{ app.jobModality }}</span>
          </div>
          <div class="detail-item">
            <va-icon name="calendar_month" size="small" />
            <span>{{ formatDate(app.appliedAt) }}</span>
          </div>
          <div v-if="app.salaryInfo" class="detail-item">
            <va-icon name="attach_money" size="small" />
            <span>{{ app.salaryInfo }}</span>
          </div>
        </div>

        <!-- Application Status Timeline -->
        <div class="status-timeline">
          <div class="timeline-item" :class="{ active: app.status !== 'received' }">
            <div class="timeline-dot"></div>
            <span>Recibida</span>
          </div>
          <div class="timeline-item" :class="{ active: ['reviewing', 'shortlisted', 'accepted'].includes(app.status) }">
            <div class="timeline-dot"></div>
            <span>En revisión</span>
          </div>
          <div class="timeline-item" :class="{ active: ['shortlisted', 'accepted'].includes(app.status) }">
            <div class="timeline-dot"></div>
            <span>Preseleccionado</span>
          </div>
          <div class="timeline-item" :class="{ active: app.status === 'accepted' }">
            <div class="timeline-dot"></div>
            <span>Aceptado</span>
          </div>
        </div>

        <!-- Card Actions -->
        <div class="card-actions">
          <button class="action-btn-gradient" @click="handleViewJob(app.jobId)">
            <va-icon name="visibility" size="small" />
            Ver Trabajo
          </button>

          <button class="action-btn-gradient" @click="handleViewApplication(app.id)">
            <va-icon name="description" size="small" />
            Ver Aplicación
          </button>

          <va-button
            v-if="app.status === 'received' || app.status === 'reviewing'"
            preset="plain"
            size="small"
            color="danger"
            @click="handleWithdrawApplication(app.id)"
          >
            <va-icon name="close" size="small" />
            Retirar
          </va-button>

          <va-button
            v-else-if="app.status === 'accepted'"
            preset="plain"
            size="small"
            color="success"
            disabled
          >
            <va-icon name="check_circle" size="small" />
            Aceptado
          </va-button>

          <va-button
            v-else-if="app.status === 'rejected'"
            preset="plain"
            size="small"
            color="textSecondary"
            disabled
          >
            <va-icon name="cancel" size="small" />
            Rechazado
          </va-button>
        </div>

        <!-- Recruiter Notes (if available) -->
        <div v-if="app.recruiterNotes" class="recruiter-notes">
          <va-icon name="message" size="small" />
          <div>
            <p class="notes-title">Notas del reclutador</p>
            <p class="notes-content">{{ app.recruiterNotes }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <va-icon name="assignment" size="4rem" color="purple" />
      <h3>No has aplicado a ningún trabajo</h3>
      <p>Explora las ofertas disponibles y comienza a aplicar</p>
      <button class="explore-btn" @click="$router.push('/guias/trabajos')">
        <va-icon name="search" />
        Explorar Trabajos
      </button>
    </div>

    <!-- Pagination (if needed in future) -->
    <div v-if="filteredApplications.length > 0 && totalApplications > itemsPerPage" class="pagination">
      <va-pagination
        v-model="currentPage"
        :pages="totalPages"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vuestic-ui'

// ========== COMPOSABLES ==========
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
const searchQuery = ref('')
const filterStatus = ref('')
const sortBy = ref('recent')
const currentPage = ref(1)
const itemsPerPage = 10

const applications = ref([
  {
    id: 'app001',
    jobId: 'job001',
    jobTitle: 'Desarrollador Senior React',
    companyName: 'Tech Solutions Bolivia',
    jobCity: 'La Paz',
    jobModality: 'Remoto',
    salaryInfo: '$1500 - $2500/mes',
    appliedAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
    status: 'shortlisted',
    recruiterNotes: 'Excelente perfil, próxima fase es entrevista técnica'
  },
  {
    id: 'app002',
    jobId: 'job002',
    jobTitle: 'Diseñador UX/UI Junior',
    companyName: 'Creative Digital Agency',
    jobCity: 'Cochabamba',
    jobModality: 'Presencial',
    salaryInfo: '$800 - $1200/mes',
    appliedAt: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
    status: 'received',
    recruiterNotes: null
  },
  {
    id: 'app003',
    jobId: 'job003',
    jobTitle: 'Gestor de Proyectos Senior',
    companyName: 'Consultoría Global',
    jobCity: 'Santa Cruz',
    jobModality: 'Híbrido',
    salaryInfo: 'A convenir',
    appliedAt: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000),
    status: 'accepted',
    recruiterNotes: 'Felicidades! Has sido seleccionado. Próximos pasos en email.'
  }
])

const statusOptions = [
  { text: 'Recibida', value: 'received' },
  { text: 'En revisión', value: 'reviewing' },
  { text: 'Preseleccionada', value: 'shortlisted' },
  { text: 'Aceptada', value: 'accepted' },
  { text: 'Rechazada', value: 'rejected' },
  { text: 'Retirada', value: 'withdrawn' }
]

const sortOptions = [
  { text: 'Más reciente', value: 'recent' },
  { text: 'Más antigua', value: 'oldest' },
  { text: 'Estado actualizado', value: 'updated' }
]

// ========== LIFECYCLE ==========
onMounted(() => {
  loadApplications()
})

// ========== COMPUTED PROPERTIES ==========
const filteredApplications = computed(() => {
  let filtered = applications.value

  // Filter by status
  if (filterStatus.value) {
    filtered = filtered.filter(app => app.status === filterStatus.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(app =>
      app.jobTitle.toLowerCase().includes(query) ||
      app.companyName.toLowerCase().includes(query)
    )
  }

  // Sort
  const sorted = [...filtered]
  if (sortBy.value === 'recent') {
    sorted.sort((a, b) => b.appliedAt - a.appliedAt)
  } else if (sortBy.value === 'oldest') {
    sorted.sort((a, b) => a.appliedAt - b.appliedAt)
  } else if (sortBy.value === 'updated') {
    sorted.sort((a, b) => {
      const statusOrder = {
        'received': 0,
        'reviewing': 1,
        'shortlisted': 2,
        'accepted': 3,
        'rejected': 4,
        'withdrawn': 5
      }
      return statusOrder[b.status] - statusOrder[a.status]
    })
  }

  return sorted.slice(
    (currentPage.value - 1) * itemsPerPage,
    currentPage.value * itemsPerPage
  )
})

const totalApplications = computed(() => applications.value.length)

const totalPages = computed(() =>
  Math.ceil(totalApplications.value / itemsPerPage)
)

// ========== METHODS ==========
const loadApplications = async () => {
  try {
    loading.value = true

    const storedUser = localStorage.getItem('authUser')
    if (!storedUser) {
      console.warn('No hay usuario autenticado')
      loading.value = false
      return
    }

    const user = JSON.parse(storedUser)
    const email = user.email || ''

    const response = await fetch(
      `/api/user/applied?email=${encodeURIComponent(email)}`
    )

    if (!response.ok) {
      throw new Error('Error cargando aplicaciones')
    }

    const data = await response.json()
    if (data.success && data.applications) {
      // Mapear datos de la API al formato esperado
      applications.value = data.applications.map(app => ({
        id: app.id,
        jobId: app.jobId,
        jobTitle: app.jobTitle,
        companyName: app.companyName,
        jobCity: app.jobCity,
        jobModality: app.jobModality,
        salaryInfo: null, // TODO: Agregar salaryInfo del job
        appliedAt: new Date(app.appliedAt),
        status: app.status,
        recruiterNotes: app.recruiterNotes
      }))
    }
  } catch (err) {
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

const getStatusLabel = (status) => {
  const labels = {
    'received': 'Recibida',
    'reviewing': 'En revisión',
    'shortlisted': 'Preseleccionada',
    'accepted': 'Aceptada',
    'rejected': 'Rechazada',
    'withdrawn': 'Retirada'
  }
  return labels[status] || status
}

const getStatusIcon = (status) => {
  const icons = {
    'received': 'mail',
    'reviewing': 'schedule',
    'shortlisted': 'bookmark',
    'accepted': 'check_circle',
    'rejected': 'cancel',
    'withdrawn': 'close'
  }
  return icons[status] || 'info'
}

const formatDate = (date) => {
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return 'Hoy'
  if (days === 1) return 'Ayer'
  if (days < 7) return `Hace ${days} días`
  if (days < 30) return `Hace ${Math.floor(days / 7)} semanas`
  if (days < 365) return `Hace ${Math.floor(days / 30)} meses`

  return date.toLocaleDateString('es-ES')
}

const handleViewJob = (jobId) => {
  // TODO: Navigate to job detail page
  notify({
    message: 'Redirigiendo a detalles del trabajo...',
    color: 'info'
  })
  // router.push(`/jobs/${jobId}`)
}

const handleViewApplication = (applicationId) => {
  // TODO: Open application detail modal or navigate to detail page
  notify({
    message: 'Abriendo detalles de la aplicación...',
    color: 'info'
  })
}

const handleWithdrawApplication = async (applicationId) => {
  try {
    // TODO: Replace with real API call
    // const response = await fetch(`/api/applications/${applicationId}/withdraw`, {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json'
    //   }
    // })

    const app = applications.value.find(a => a.id === applicationId)
    if (app) {
      app.status = 'withdrawn'
      notify({
        message: '✅ Aplicación retirada exitosamente',
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
  }
}
</script>

<style scoped>
.mis-ordenes-container {
  padding: 0;
}

/* ========== HEADER ========== */
.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.5rem;
}

.section-subtitle {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
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
  border-color: #5C0099;
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
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

/* ========== APPLICATIONS LIST ========== */
.applications-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.application-card {
  background: white;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.application-card:hover {
  border-color: #e0e0e0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.application-card.status-received {
  border-left: 4px solid #ffc107;
}

.application-card.status-reviewing {
  border-left: 4px solid #2196f3;
}

.application-card.status-shortlisted {
  border-left: 4px solid #9c27b0;
}

.application-card.status-accepted {
  border-left: 4px solid #4caf50;
}

.application-card.status-rejected {
  border-left: 4px solid #f44336;
}

.application-card.status-withdrawn {
  border-left: 4px solid #999;
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f5f5f5;
}

.job-info {
  flex: 1;
}

.job-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 0.25rem;
}

.company-name {
  color: #666;
  margin: 0;
  font-size: 0.9rem;
}

/* Status Badge */
.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge.status-received {
  background: #fff3cd;
  color: #856404;
}

.status-badge.status-reviewing {
  background: #cfe2ff;
  color: #084298;
}

.status-badge.status-shortlisted {
  background: #f3e5f5;
  color: #6a1b9a;
}

.status-badge.status-accepted {
  background: #d4edda;
  color: #155724;
}

.status-badge.status-rejected {
  background: #f8d7da;
  color: #721c24;
}

.status-badge.status-withdrawn {
  background: #e2e3e5;
  color: #383d41;
}

/* Job Details */
.job-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding: 1rem 0;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.detail-item .va-icon {
  color: #5C0099;
  flex-shrink: 0;
}

/* Status Timeline */
.status-timeline {
  display: flex;
  justify-content: space-around;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.timeline-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  flex: 1;
  font-size: 0.8rem;
  color: #ccc;
}

.timeline-item.active {
  color: #5C0099;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: currentColor;
  border: 2px solid white;
  box-shadow: 0 0 0 2px currentColor;
}

/* Card Actions */
.card-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  padding-top: 1rem;
  border-top: 1px solid #f5f5f5;
  margin-bottom: 1rem;
}

.card-actions .va-button {
  flex: 1;
  min-width: 120px;
}

/* Recruiter Notes */
.recruiter-notes {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #f5f5f5;
  border-left: 3px solid #5C0099;
  border-radius: 6px;
  margin-top: 1rem;
}

.recruiter-notes .va-icon {
  color: #5C0099;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.notes-title {
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 0.5rem;
  font-size: 0.9rem;
}

.notes-content {
  color: #666;
  margin: 0;
  font-size: 0.85rem;
  line-height: 1.5;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
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
  margin-bottom: 1.5rem;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f0f0f0;
}

/* Action Button Gradient */
.action-btn-gradient {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.85rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn-gradient:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
}

.explore-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.explore-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .mis-ordenes-container {
    padding: 0;
  }

  .filter-bar {
    flex-direction: column;
  }

  .filter-controls {
    flex-direction: column;
  }

  .filter-select {
    min-width: auto;
  }

  .card-header {
    flex-direction: column;
  }

  .status-badge {
    align-self: flex-start;
  }

  .job-details {
    gap: 1rem;
  }

  .status-timeline {
    gap: 0.25rem;
    padding: 0.75rem;
  }

  .timeline-item {
    gap: 0.25rem;
  }

  .timeline-item span {
    display: none;
  }

  .timeline-item.active span {
    display: block;
  }

  .card-actions {
    flex-direction: column;
  }

  .card-actions .va-button {
    min-width: auto;
  }

  .recruiter-notes {
    flex-direction: column;
    gap: 0.5rem;
  }

  .recruiter-notes .va-icon {
    margin-top: 0;
  }
}

@media (max-width: 480px) {
  .section-header h2 {
    font-size: 1.5rem;
  }

  .filter-bar {
    padding: 1rem;
  }

  .application-card {
    padding: 1rem;
  }

  .job-title {
    font-size: 1rem;
  }

  .job-details {
    flex-direction: column;
    gap: 0.75rem;
  }

  .status-timeline {
    justify-content: flex-start;
    overflow-x: auto;
  }
}
</style>
