<!-- frontend/src/components/Dashboard/JobsManager.vue -->
<template>
  <div class="jobs-manager-wrapper">
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
        Publicar Nuevo Anuncio
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
          <option value="pending">Pendientes</option>
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
            <va-icon name="visibility" color="#6366F1" />
            <span class="stat-text">{{ job.views }}</span>
          </div>
          <div class="stat-item">
            <va-icon name="people" color="#8B5CF6" />
            <span class="stat-text">{{ job.applications }}</span>
          </div>
          <div class="stat-item plan-stat">
            <va-icon name="card_giftcard" color="#7c3aed" />
            <span class="stat-text plan-badge" :class="getPlanCssClass(job.selectedPlan)">
              {{ formatPlanName(job.selectedPlan, job.planLabel, job.planPrice) }}
            </span>
          </div>

          <!-- Payment Verification Status -->
          <div class="stat-item">
            <va-icon
              :name="job.paymentVerified ? 'check_circle' : 'pending'"
              :color="job.paymentVerified ? '#10b981' : '#f59e0b'"
            />
            <span
              class="stat-text payment-status"
              :class="job.paymentVerified ? 'verified' : 'pending'"
            >
              {{ job.paymentVerified ? 'Anuncio Aprobado' : 'Pendiente verificación' }}
            </span>
          </div>

          <!-- Public Visibility Indicator -->
          <div class="stat-item" v-if="job.status !== 'active'">
            <va-icon name="visibility_off" color="#dc2626" />
            <span class="stat-text visibility-warning">No visible públicamente</span>
          </div>

          <div class="stat-divider">|</div>
          <div class="stat-item">
            <va-icon name="schedule" color="#64748B" />
            <span class="stat-label">Publicado:</span>
            <span class="stat-text stat-date">{{ formatExactDateTime(job.createdAt) }}</span>
          </div>
          <div class="stat-item">
            <va-icon name="event_note" color="#64748B" />
            <span class="stat-label">Vence:</span>
            <span class="stat-text stat-date">{{ formatExpiryDate(job.expiryDate) }}</span>
          </div>
          <div class="stat-item">
            <va-icon name="timer" color="#F59E0B" />
            <span class="stat-label">Restan:</span>
            <span class="stat-text">{{ calculateDaysRemaining(job.expiryDate) }} días</span>
          </div>
        </div>

        <!-- Card Actions -->
        <div class="job-actions">
          <!-- Toggle Switch Activar/Desactivar -->
          <div class="toggle-container">
            <label class="toggle-label" :class="{ 'disabled': !job.paymentVerified && job.status !== 'active' }">
              <input
                type="checkbox"
                :checked="job.status === 'active'"
                @change="toggleJobStatus(job)"
                :disabled="!job.paymentVerified && job.status !== 'active'"
                class="toggle-input"
              />
              <span class="toggle-slider"></span>
              <span class="toggle-text">
                {{ job.status === 'active' ? 'Activo' : 'Inactivo' }}
              </span>
            </label>
          </div>

          <!-- Botones de acción -->
          <div class="action-buttons">
            <button class="action-btn view" title="Ver detalles" @click="viewJob(job)">
              <va-icon name="visibility" size="small" />
              <span class="btn-text">Ver</span>
            </button>
            <button class="action-btn edit" title="Editar anuncio" @click="editJob(job)">
              <va-icon name="edit" size="small" />
              <span class="btn-text">Editar</span>
            </button>
            <button class="action-btn delete" title="Eliminar anuncio" @click="deleteJob(job)">
              <va-icon name="delete" size="small" />
              <span class="btn-text">Eliminar</span>
            </button>
          </div>
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

    <!-- Modal de Edición -->
    <va-modal
      v-model="showEditModal"
      size="large"
      :close-button="false"
      hide-default-actions
    >
      <template #header>
        <div class="modal-header-content">
          <h2 class="modal-title">Editar Anuncio</h2>
          <p class="modal-subtitle">Actualiza los detalles de tu oferta de trabajo</p>
        </div>
      </template>

      <div class="edit-form">
        <div class="form-group">
          <label class="form-label">Título del Puesto *</label>
          <va-input
            v-model="editFormData.title"
            placeholder="Ej: Desarrollador Full Stack"
          />
          <span class="field-hint">Nombre del cargo que estás ofreciendo</span>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Ciudad *</label>
            <va-input
              v-model="editFormData.city"
              placeholder="Ej: Santa Cruz"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Número de Vacantes</label>
            <va-input
              v-model.number="editFormData.vacancies"
              type="number"
              :min="1"
              placeholder="1"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Tipo de Contrato *</label>
          <va-select
            v-model="editFormData.contractType"
            :options="['Tiempo Completo', 'Medio Tiempo', 'Por Proyecto', 'Freelance', 'Temporal', 'Indefinido']"
            placeholder="Selecciona el tipo de contrato"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Descripción del Trabajo *</label>
          <va-textarea
            v-model="editFormData.description"
            placeholder="Describe las responsabilidades, requisitos y detalles del puesto..."
            :min-rows="6"
            autosize
            class="description-field"
          />
          <span class="field-hint">Detalla las funciones del cargo y lo que buscas en un candidato</span>
        </div>

        <div class="form-group">
          <label class="form-label">Beneficios Adicionales</label>
          <va-textarea
            v-model="editFormData.benefits"
            placeholder="Aguinaldo, bono de producción, seguro médico, horario flexible, trabajo remoto..."
            :min-rows="3"
            autosize
            class="benefits-field"
          />
          <span class="field-hint">Beneficios que hagan más atractivo tu anuncio</span>
        </div>

        <div class="info-box">
          <va-icon name="info" size="small" color="#F59E0B" />
          <div class="info-text">
            <strong>Datos protegidos</strong>
            <p>El salario, plan contratado y método de pago no pueden editarse. Contacta a soporte si necesitas modificarlos.</p>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="modal-footer">
          <va-button color="secondary" @click="closeEditModal">
            Cancelar
          </va-button>
          <va-button @click="saveEditedJob" class="save-btn">
            <va-icon name="save" size="small" />
            Guardar Cambios
          </va-button>
        </div>
      </template>
    </va-modal>
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
const showEditModal = ref(false)
const selectedJob = ref(null)
const editFormData = ref({
  title: '',
  city: '',
  vacancies: 1,
  contractType: '',
  description: '',
  benefits: ''
})

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
        companyLogo: job.companyLogo || null,
        status: job.status,
        paymentVerified: job.paymentVerified || false,
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
    pending: '⏳ Pendiente',
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

const formatPlanName = (planKey, planLabel, planPrice) => {
  // Determinar el nombre del plan
  let name = planLabel

  if (!name) {
    if (!planKey) return 'Sin plan'
    const planNames = {
      'estandar': 'Estandar',
      'escencial': 'Estandar',  // Soporte para nombre antiguo
      'purpura': 'Púrpura',
      'impulso': 'Impulso Pro'
    }
    name = planNames[planKey.toLowerCase()] || planKey
  }

  // Si el planLabel ya incluye el precio (contiene paréntesis), no agregar
  if (name && name.includes('(') && name.includes(')')) {
    return name
  }

  // Agregar precio si está disponible y no está ya en el nombre
  if (planPrice) {
    return `${name} (${planPrice})`
  }

  return name
}

const getPlanCssClass = (planKey) => {
  // Normalizar plan key para aplicar la clase CSS correcta
  // Mapear 'escencial' a 'estandar' para compatibilidad
  const normalizedKey = planKey === 'escencial' ? 'estandar' : planKey
  return `plan-${normalizedKey}`
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
    console.log('✅ Detalles completos del trabajo cargados:', data.job)
    console.log('📷 Logo de empresa recibido:', data.job.companyLogo)
    console.log('🏢 Nombre de empresa:', data.job.companyName)
  } catch (err) {
    console.error('Error cargando detalles del trabajo:', err)
    notify({
      message: `Error al cargar detalles: ${err.message}`,
      color: 'danger'
    })
  }
}

const editJob = async (job) => {
  try {
    // Cargar datos completos del job
    const response = await fetch(`/api/jobs/${job.id}`, {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al cargar anuncio')
    }

    // Llenar formulario con campos editables
    selectedJob.value = job
    editFormData.value = {
      title: data.job.title || '',
      city: data.job.city || '',
      vacancies: data.job.vacancies || 1,
      contractType: data.job.contractType || '',
      description: data.job.description || '',
      benefits: data.job.benefits || ''
    }

    // Abrir modal
    showEditModal.value = true
  } catch (err) {
    console.error('Error loading job for edit:', err)
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 4000,
      position: 'top-right'
    })
  }
}

const toggleJobStatus = async (job) => {
  try {
    const newStatus = job.status === 'active' ? 'closed' : 'active'

    // VALIDACIÓN: No permitir activar si el pago no está verificado
    if (newStatus === 'active' && !job.paymentVerified) {
      notify({
        message: 'No puedes activar este anuncio. El pago aún no ha sido verificado por el administrador.',
        color: 'warning',
        duration: 4500,
        position: 'top-right',
        closeable: true
      })
      return
    }

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

    // Notificación sutil
    const message = newStatus === 'active' ? 'Anuncio activado' : 'Anuncio desactivado'

    notify({
      message: message,
      color: newStatus === 'active' ? 'success' : 'info',
      duration: 2000,
      position: 'top-right',
      closeable: true
    })
  } catch (err) {
    console.error('Error updating job status:', err)
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 4000,
      position: 'top-right',
      closeable: true
    })
  }
}

const deleteJob = async (job) => {
  if (!confirm(`¿Está seguro de que desea eliminar "${job.title}"?`)) return

  try {
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
      message: 'Anuncio eliminado',
      color: 'success',
      duration: 2000,
      position: 'top-right',
      closeable: true
    })
  } catch (err) {
    console.error('Error deleting job:', err)
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 4000,
      position: 'top-right',
      closeable: true
    })
  }
}

const saveEditedJob = async () => {
  if (!selectedJob.value) return

  try {
    const response = await fetch(`/api/jobs/${selectedJob.value.id}/update`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(editFormData.value)
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al actualizar anuncio')
    }

    // Actualizar campos editados en la lista
    const index = jobs.value.findIndex(j => j.id === selectedJob.value.id)
    if (index !== -1) {
      jobs.value[index].title = editFormData.value.title
      jobs.value[index].city = editFormData.value.city
      jobs.value[index].vacancies = editFormData.value.vacancies
      jobs.value[index].contractType = editFormData.value.contractType
      jobs.value[index].description = editFormData.value.description
      jobs.value[index].benefits = editFormData.value.benefits
    }

    // Cerrar modal
    showEditModal.value = false
    selectedJob.value = null

    notify({
      message: 'Anuncio actualizado',
      color: 'success',
      duration: 2000,
      position: 'top-right',
      closeable: true
    })
  } catch (err) {
    console.error('Error updating job:', err)
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 4000,
      position: 'top-right',
      closeable: true
    })
  }
}

const closeEditModal = () => {
  showEditModal.value = false
  selectedJob.value = null
  editFormData.value = {
    title: '',
    city: '',
    vacancies: 1,
    contractType: '',
    description: '',
    benefits: ''
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

  // VALIDACIÓN: No permitir activar si el pago no está verificado
  if (!selectedJob.value.paymentVerified) {
    notify({
      message: 'No puedes activar este anuncio. El pago aún no ha sido verificado por el administrador.',
      color: 'warning',
      duration: 4500,
      position: 'top-right',
      closeable: true
    })
    return
  }

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
  border-color: #7c3aed, #6d28d9;
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

.job-badge.pending {
  background: #fff3e0;
  color: #e65100;
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
  color: #9CA3AF;
}

/* Colorear íconos según contexto */
.stat-item:has(.payment-status.verified) svg {
  color: #10b981 !important;
}

.stat-item:has(.payment-status.pending) svg {
  color: #f59e0b !important;
}

.stat-item:has(.visibility-warning) svg {
  color: #dc2626 !important;
}

.stat-item:has(.plan-badge) svg {
  color: #7c3aed !important;
}

.stat-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6B7280;
  margin-right: 0.25rem;
}

.stat-text {
  font-weight: 500;
  color: #1a1a1a;
}

.stat-date {
  font-size: 0.8rem;
  color: #374151;
  font-weight: 500;
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

.plan-escencial {
  /* Alias para compatibilidad con jobs antiguos */
  background: linear-gradient(135deg, #F59E0B, #FBBF24);
}

.plan-purpura {
  background: linear-gradient(135deg,  #7c3aed, #6d28d9);
}

.plan-impulso {
  background: linear-gradient(135deg, #10B981, #34D399);
}

/* ========== JOB ACTIONS ========== */
.job-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #E5E7EB;
}

/* ========== TOGGLE SWITCH ========== */
.toggle-container {
  display: flex;
  align-items: center;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  user-select: none;
}

.toggle-label.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toggle-input {
  display: none;
}

.toggle-slider {
  position: relative;
  width: 40px;
  height: 20px;
  background-color: #D1D5DB;
  border-radius: 20px;
  transition: background-color 0.3s;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-input:checked + .toggle-slider {
  background-color: #10B981;
}

.toggle-input:checked + .toggle-slider::before {
  transform: translateX(20px);
}

.toggle-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
  min-width: 60px;
}

.toggle-input:checked ~ .toggle-text {
  color: #10B981;
}

/* ========== ACTION BUTTONS ========== */
.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-left: auto;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.action-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Botón Ver - Azul elegante */
.action-btn.view {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
}

.action-btn.view:hover {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
}

/* Botón Editar - Verde azulado */
.action-btn.edit {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
}

.action-btn.edit:hover {
  background: #059669;
}

/* Botón Eliminar - Rojo elegante */
.action-btn.delete {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  color: white;
}

.action-btn.delete:hover {
  background: #DC2626;
}

/* Estilos para botones antiguos (por si acaso) */
.action-btn.duplicate {
  background: #F59E0B;
  color: white;
}

.action-btn.duplicate:hover {
  background: #D97706;
}

.action-btn.close {
  background: #EF4444;
  color: white;
}

.action-btn.close:hover {
  background: #DC2626;
}

.action-btn.reopen {
  background: #10B981;
  color: white;
}

.action-btn.reopen:hover {
  background: #059669;
}

/* ========== PAYMENT STATUS ========== */
.payment-status {
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}

.payment-status.verified {
  color: #10b981;
}

.payment-status.pending {
  color: #f59e0b;
}

.visibility-warning {
  color: #dc2626 !important;
  font-weight: 600;
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

/* ========== EDIT MODAL ========== */
.modal-header-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.modal-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
}

.modal-subtitle {
  margin: 0;
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 400;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem 0;
  max-height: 60vh;
  overflow-y: auto;
}

.edit-form::-webkit-scrollbar {
  width: 8px;
}

.edit-form::-webkit-scrollbar-track {
  background: #F3F4F6;
  border-radius: 10px;
}

.edit-form::-webkit-scrollbar-thumb {
  background: #9f7aea;
  border-radius: 10px;
}

.edit-form::-webkit-scrollbar-thumb:hover {
  background: #7c3aed;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 0.25rem;
}

.field-hint {
  font-size: 0.8rem;
  color: #6B7280;
  font-style: italic;
  margin-top: 0.25rem;
}

.description-field,
.benefits-field {
  font-family: inherit;
  font-size: 0.95rem;
  line-height: 1.6;
}

.info-box {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  border-radius: 8px;
  margin-top: 0.5rem;
}

.info-text {
  flex: 1;
}

.info-text strong {
  display: block;
  color: #92400E;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.info-text p {
  margin: 0;
  font-size: 0.85rem;
  color: #B45309;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.875rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E5E7EB;
  margin-top: 0.5rem;
}

.modal-footer .va-button {
  padding: 0.625rem 1.25rem !important;
  border-radius: 10px !important;
  font-weight: 600;
  font-size: 0.75rem;
  transition: all 0.3s ease;
}

.save-btn {
  background: linear-gradient(135deg, #10B981, #059669) !important;
  color: white !important;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.25);
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
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

  .publish-btn-new {
    display: none; /* Ocultar en móvil para evitar duplicación con navbar */
  }

  .empty-action-btn {
    width: 100%;
    justify-content: center;
    padding: 0.875rem 1rem;
    font-size: 0.9rem;
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

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-title {
    font-size: 1.25rem;
  }

  .modal-subtitle {
    font-size: 0.8rem;
  }

  .edit-form {
    max-height: 50vh;
  }

  .info-box {
    flex-direction: column;
    gap: 0.5rem;
  }

  .modal-footer {
    flex-direction: column;
    gap: 0.5rem;
  }

  .modal-footer .va-button {
    width: 100%;
  }
}
</style>
