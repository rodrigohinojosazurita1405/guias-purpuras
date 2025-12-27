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
          <option value="urgency">Por urgencia (próximos a expirar)</option>
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
      <div v-for="(job, index) in filteredJobs" :key="job.id">
        <!-- Separador: Anuncios Recientes (inicio) -->
        <div
          v-if="index === 0 && !isJobExpired(job) && job.paymentVerified"
          class="section-divider recent"
        >
          <div class="divider-line"></div>
          <div class="divider-label">
            <va-icon name="trending_up" size="small" color="#10b981" />
            <span>Anuncios Recientes</span>
          </div>
          <div class="divider-line"></div>
        </div>

        <!-- Separador: Pendientes de Aprobación -->
        <div
          v-if="index > 0 && filteredJobs[index - 1].paymentVerified && !job.paymentVerified && !isJobExpired(job) && job.status !== 'rejected'"
          class="section-divider pending"
        >
          <div class="divider-line"></div>
          <div class="divider-label">
            <va-icon name="pending" size="small" color="#f59e0b" />
            <span>Pendientes de Aprobación</span>
          </div>
          <div class="divider-line"></div>
        </div>

        <!-- Separador: Anuncios Rechazados -->
        <div
          v-if="index > 0 && filteredJobs[index - 1].status !== 'rejected' && job.status === 'rejected'"
          class="section-divider rejected"
        >
          <div class="divider-line"></div>
          <div class="divider-label">
            <va-icon name="block" size="small" color="#dc2626" />
            <span>Anuncios Rechazados</span>
          </div>
          <div class="divider-line"></div>
        </div>

        <!-- Separador: Anuncios Expirados -->
        <div
          v-if="index > 0 && !isJobExpired(filteredJobs[index - 1]) && isJobExpired(job) && job.status !== 'rejected'"
          class="section-divider expired"
        >
          <div class="divider-line"></div>
          <div class="divider-label">
            <va-icon name="archive" size="small" color="#f97316" />
            <span>Anuncios Expirados</span>
          </div>
          <div class="divider-line"></div>
        </div>

        <div class="job-card">
        <!-- Card Header -->
        <div class="job-card-header">
          <div class="job-info">
            <h3 class="job-title">{{ job.title }}</h3>
            <p class="job-company">{{ job.companyName }}</p>
          </div>
          <div class="job-badge" :class="isJobExpired(job) ? 'expired' : job.status">
            <va-icon v-if="isJobExpired(job)" name="event_busy" size="small" />
            <va-icon v-else-if="job.status === 'rejected'" name="block" size="small" />
            {{ isJobExpired(job) ? 'Expirado' : statusLabel(job.status) }}
          </div>
        </div>

        <!-- Rejection Warning Alert -->
        <div v-if="job.status === 'rejected'" class="rejection-alert">
          <div class="rejection-header">
            <va-icon name="block" size="24px" color="#dc2626" />
            <h4>Anuncio Rechazado por Incumplir Nuestras Normas</h4>
          </div>

          <div v-if="job.rejectionReason" class="rejection-main-reason">
            <p class="reason-text">{{ job.rejectionReason }}</p>
          </div>

          <p class="rejection-message">
            Su anuncio viola nuestros
            <router-link to="/terminos" class="terms-link" target="_blank">
              Términos y Condiciones
            </router-link>, específicamente la sección 3.4 sobre "Contenido Prohibido y Actividades Ilegales".
          </p>

          <p class="rejection-footer">
            Si considera que esto es un error, por favor contacte con
            <a href="mailto:contacto@guiaspurpuras.com.bo" class="support-link">Soporte Técnico</a>
            para solicitar una revisión.
          </p>
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
            <va-icon name="schedule" color="#7C3AED" />
            <span class="stat-label">Publicado:</span>
            <span class="stat-text stat-date">{{ formatExactDateTime(job.createdAt) }}</span>
          </div>
          <div class="stat-item deadline-item">
            <va-icon name="how_to_reg" color="#7C3AED" />
            <span class="stat-label">Cierra postulación:</span>
            <span class="stat-text stat-date" :class="{ 'deadline-closed': isDeadlinePassed(job) }">
              {{ formatExpiryDate(job.applicationDeadline || job.expiryDate) }}
            </span>
            <button
              v-show="canExtendDeadline(job)"
              class="edit-deadline-btn"
              @click.stop="openEditDeadlineModal(job)"
              title="Ampliar fecha límite de postulación"
            >
              <va-icon name="schedule" size="18px" color="white" />
            </button>
          </div>
          <div class="stat-item">
            <va-icon name="timer" color="#7C3AED" />
            <span class="stat-label">Faltan:</span>
            <span class="stat-text">{{ calculateDaysRemaining(job.applicationDeadline || job.expiryDate) }} días</span>
          </div>
          <div class="stat-item">
            <va-icon name="event_note" color="#7C3AED" />
            <span class="stat-label">Plan vence:</span>
            <span class="stat-text stat-date">{{ formatExpiryDate(job.expiryDate) }}</span>
          </div>
          <div class="stat-item" v-show="canExtendDeadline(job)">
            <va-icon name="info" color="#10B981" size="14px" />
            <span class="stat-text days-available">{{ calculateRemainingDays(job) }} días disponibles</span>
          </div>
        </div>

        <!-- Card Actions -->
        <div class="job-actions">
          <!-- Toggle Switch Activar/Desactivar -->
          <div class="toggle-container">
            <label class="toggle-label" :class="{ 'disabled': isJobExpired(job) || job.status === 'rejected' || (!job.paymentVerified && job.status !== 'active') }">
              <input
                type="checkbox"
                :checked="job.status === 'active'"
                @change="toggleJobStatus(job)"
                :disabled="isJobExpired(job) || job.status === 'rejected' || (!job.paymentVerified && job.status !== 'active')"
                class="toggle-input"
              />
              <span class="toggle-slider"></span>
              <span class="toggle-text">
                {{ job.status === 'rejected' ? 'Rechazado' : (isJobExpired(job) ? 'Expirado' : (job.status === 'active' ? 'Activo' : 'Inactivo')) }}
              </span>
            </label>
          </div>

          <!-- Botones de acción -->
          <div class="action-buttons">
            <button class="action-btn view" title="Ver detalles" @click="viewJob(job)">
              <va-icon name="visibility" size="small" />
              <span class="btn-text">Ver</span>
            </button>
            <button
              class="action-btn edit"
              :title="isJobExpired(job) ? 'No se puede editar un anuncio expirado' : 'Editar anuncio'"
              @click="editJob(job)"
              :disabled="isJobExpired(job)"
              :class="{ 'disabled': isJobExpired(job) }"
            >
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

    <!-- Modal de Confirmación de Eliminación -->
    <va-modal
      v-model="showDeleteModal"
      size="small"
      :close-button="false"
      hide-default-actions
    >
      <template #header>
        <div class="delete-header">
          <va-icon name="warning" size="2.5rem" color="#DC2626" />
          <h2 class="delete-title">¿Eliminar anuncio?</h2>
        </div>
      </template>

      <div class="delete-content">
        <!-- Job info -->
        <div class="job-info-box">
          <p class="job-name">{{ jobToDelete?.title }}</p>
          <p class="job-stats">{{ jobToDelete?.views || 0 }} vistas • {{ jobToDelete?.applications || 0 }} aplicaciones</p>
        </div>

        <!-- Warning -->
        <div class="warning-compact">
          <va-icon name="info" size="small" color="#DC2626" />
          <p>Esta acción es permanente. Se perderán todos los datos y no se puede deshacer.</p>
        </div>

        <!-- Checkbox -->
        <label class="confirm-label">
          <input type="checkbox" v-model="deleteConfirmed" class="confirm-check" />
          <span class="confirm-box"></span>
          <span class="confirm-text">Confirmo que deseo eliminar este anuncio</span>
        </label>
      </div>

      <template #footer>
        <div class="delete-actions">
          <va-button color="secondary" @click="closeDeleteModal">Cancelar</va-button>
          <va-button @click="confirmDelete" :disabled="!deleteConfirmed" class="btn-delete">
            <va-icon name="delete" size="small" />
            Eliminar
          </va-button>
        </div>
      </template>
    </va-modal>

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
            Guardar Cambios
          </va-button>
        </div>
      </template>
    </va-modal>

    <!-- Modal de Edición de Fecha Límite -->
    <va-modal
      v-model="showEditDeadlineModal"
      size="small"
      :close-button="false"
      hide-default-actions
      :mobile-fullscreen="true"
    >
      <template #header>
        <div class="deadline-modal-header">
          <va-icon name="edit_calendar" size="2rem" color="#7C3AED" class="header-icon" />
          <h2 class="deadline-modal-title">Editar Fecha Límite</h2>
          <button class="modal-close-btn" @click="closeEditDeadlineModal" aria-label="Cerrar">
            <va-icon name="close" size="1.5rem" />
          </button>
        </div>
      </template>

      <div class="deadline-modal-content">
        <!-- Job Info -->
        <div class="job-info-box">
          <p class="job-name">{{ jobToEditDeadline?.title }}</p>
          <p class="job-stats">{{ jobToEditDeadline?.views || 0 }} vistas • {{ jobToEditDeadline?.applications || 0 }} postulaciones</p>
        </div>

        <!-- Current Deadline Info -->
        <div class="current-deadline-info">
          <div class="info-row">
            <span class="info-label">Fecha límite actual:</span>
            <span class="info-value current">{{ formatExpiryDate(jobToEditDeadline?.applicationDeadline || jobToEditDeadline?.expiryDate) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Plan vence:</span>
            <span class="info-value">{{ formatExpiryDate(jobToEditDeadline?.expiryDate) }}</span>
          </div>
          <div class="info-row highlight">
            <va-icon name="info" size="14px" color="#10B981" />
            <span class="info-text">Tienes {{ calculateRemainingDays(jobToEditDeadline) }} días disponibles para extender</span>
          </div>
        </div>

        <!-- Date Picker (Native HTML5 para evitar problemas de z-index) -->
        <div class="form-group">
          <label class="form-label">Nueva fecha límite de postulación *</label>
          <div class="native-date-input-wrapper">
            <va-icon name="event" color="purple" class="date-icon" />
            <input
              type="date"
              v-model="newDeadlineDateString"
              class="native-date-input"
              :min="todayString"
              :max="jobToEditDeadline?.expiryDate"
              required
            />
          </div>
          <span class="field-hint">
            <va-icon name="info" size="12px" color="#6B7280" />
            La fecha debe estar entre hoy y {{ formatExpiryDate(jobToEditDeadline?.expiryDate) }}
          </span>
        </div>

        <!-- Warning -->
        <div class="warning-box">
          <va-icon name="warning" size="small" color="#F59E0B" />
          <p>Al extender la fecha límite, los candidatos podrán seguir postulando hasta la nueva fecha establecida.</p>
        </div>
      </div>

      <template #footer>
        <div class="deadline-modal-actions">
          <va-button color="secondary" @click="closeEditDeadlineModal">
            Cancelar
          </va-button>
          <va-button @click="saveNewDeadline" class="btn-save" :disabled="!newDeadlineDateString">
            <va-icon name="check_circle" size="small" />
            Guardar Nueva Fecha
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
import { apiCall } from '@/utils/api'
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
const showDeleteModal = ref(false)
const showEditDeadlineModal = ref(false)
const selectedJob = ref(null)
const jobToDelete = ref(null)
const jobToEditDeadline = ref(null)
const newDeadlineDate = ref(null)
const newDeadlineDateString = ref('')
const deleteConfirmed = ref(false)

// Calcular fecha de hoy en formato YYYY-MM-DD para el input date
const getTodayString = () => {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}
const todayString = ref(getTodayString())
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

  // Ordenar de forma inteligente con 3 grupos
  filtered.sort((a, b) => {
    const aExpired = isJobExpired(a)
    const bExpired = isJobExpired(b)
    const aVerified = a.paymentVerified
    const bVerified = b.paymentVerified
    const aDaysRemaining = calculateDaysRemaining(a.expiryDate)
    const bDaysRemaining = calculateDaysRemaining(b.expiryDate)

    // 1. PRIORIDAD MÁXIMA: Separar en 4 grupos
    // Grupo 1: Anuncios Recientes (verificados y no expirados)
    // Grupo 2: Pendientes de Aprobación (no verificados y no expirados)
    // Grupo 3: Anuncios Rechazados
    // Grupo 4: Anuncios Expirados

    const aRejected = a.status === 'rejected'
    const bRejected = b.status === 'rejected'

    let aGroup, bGroup
    if (aRejected) aGroup = 3
    else if (aExpired) aGroup = 4
    else aGroup = aVerified ? 1 : 2

    if (bRejected) bGroup = 3
    else if (bExpired) bGroup = 4
    else bGroup = bVerified ? 1 : 2

    if (aGroup !== bGroup) {
      return aGroup - bGroup // Ordenar por grupo
    }

    // 2. Dentro del mismo grupo, aplicar orden específico

    // Si AMBOS están expirados (Grupo 3)
    if (aExpired && bExpired) {
      return new Date(b.expiryDate) - new Date(a.expiryDate)
    }

    // Si AMBOS están en Grupo 1 o 2 (activos), aplicar el orden seleccionado
    if (sortBy.value === 'urgency') {
      // Ordenar por días restantes (menor a mayor = más urgente primero)
      return aDaysRemaining - bDaysRemaining
    } else if (sortBy.value === 'views') {
      // Ordenar por vistas (mayor a menor)
      return b.views - a.views
    } else if (sortBy.value === 'applications') {
      // Ordenar por aplicaciones (mayor a menor)
      return b.applications - a.applications
    } else if (sortBy.value === 'recent') {
      // Ordenar por fecha de creación (más recientes primero)
      return new Date(b.createdAt) - new Date(a.createdAt)
    } else {
      // Fallback: ordenar por fecha de creación
      return new Date(b.createdAt) - new Date(a.createdAt)
    }
  })

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

    // Verificar autenticación
    if (!authStore.isAuthenticated) {
      // Si no está autenticado, hacer logout y redirigir
      authStore.logout()
      notify({
        message: 'Por seguridad, su sesión ha sido cerrada. Por favor, inicie sesión nuevamente.',
        color: 'warning',
        duration: 5000
      })
      router.push('/login')
      return
    }

    const email = authStore.user.email || ''
    const url = `/user/published?email=${encodeURIComponent(email)}`

    // Usar apiCall que maneja automáticamente el refresh de tokens
    const response = await apiCall(url, {
      method: 'GET'
    })

    const data = await response.json()

    if (!response.ok) {
      const errorMsg = data.message || 'Error al cargar trabajos publicados'
      throw new Error(errorMsg)
    }

    if (data.success && data.jobs) {
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
        applicationDeadline: job.applicationDeadline,  // CRÍTICO: Fecha límite de postulación
        selectedPlan: job.selectedPlan,
        // Datos del plan capturados en el momento de publicación
        planLabel: job.planLabel,
        planPrice: job.planPrice,
        planDuration: job.planDuration
      }))
    } else {
      throw new Error(data.message || 'Respuesta del servidor inválida')
    }
  } catch (err) {
    // Si es error de sesión expirada, el interceptor ya hizo logout
    if (err.message.includes('sesión ha sido cerrada')) {
      router.push('/login')
      return
    }

    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    loading.value = false
  }
}

const statusLabel = (status) => {
  const labels = {
    pending: '⏳ Pendiente',
    active: '✓ Activo',
    closed: '✕ Cerrado',
    draft: '✎ Borrador',
    rejected: 'Rechazado'
  }
  return labels[status] || status
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
  // Parsear como fecha local para evitar problemas de zona horaria
  const [year, month, day] = dateString.split('-')
  const date = new Date(year, month - 1, day)
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const calculateDaysRemaining = (expiryDateString) => {
  if (!expiryDateString) return -1
  // Parsear como fecha local para evitar problemas de zona horaria
  const [year, month, day] = expiryDateString.split('-')
  const expiryDate = new Date(year, month - 1, day)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  expiryDate.setHours(0, 0, 0, 0)
  const diff = expiryDate - today
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))
  return days
}

const isJobExpired = (job) => {
  if (!job.expiryDate) return false
  const daysRemaining = calculateDaysRemaining(job.expiryDate)
  return daysRemaining < 0
}

// ========== DEADLINE MANAGEMENT FUNCTIONS ==========

const isDeadlinePassed = (job) => {
  const deadline = job.applicationDeadline || job.expiryDate
  if (!deadline) return false
  const daysRemaining = calculateDaysRemaining(deadline)
  return daysRemaining < 0
}

const canExtendDeadline = (job) => {
  if (!job || !job.applicationDeadline || !job.expiryDate) return false

  try {
    // Parsear fechas de manera consistente con otras funciones
    const [yearApp, monthApp, dayApp] = job.applicationDeadline.split('-')
    const [yearExp, monthExp, dayExp] = job.expiryDate.split('-')

    const deadline = new Date(yearApp, monthApp - 1, dayApp)
    const expiry = new Date(yearExp, monthExp - 1, dayExp)
    const today = new Date()

    today.setHours(0, 0, 0, 0)
    deadline.setHours(0, 0, 0, 0)
    expiry.setHours(0, 0, 0, 0)

    // Condiciones:
    // 1. El plan no debe estar expirado (expiryDate >= hoy)
    // 2. Debe haber días disponibles (applicationDeadline < expiryDate)
    // 3. El anuncio debe estar verificado
    return expiry >= today && deadline < expiry && job.paymentVerified
  } catch (error) {
    return false
  }
}

const calculateRemainingDays = (job) => {
  if (!job || !job.applicationDeadline || !job.expiryDate) return 0

  const [yearApp, monthApp, dayApp] = job.applicationDeadline.split('-')
  const [yearExp, monthExp, dayExp] = job.expiryDate.split('-')

  const deadline = new Date(yearApp, monthApp - 1, dayApp)
  const expiry = new Date(yearExp, monthExp - 1, dayExp)

  const diffTime = expiry - deadline
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  return diffDays > 0 ? diffDays : 0
}

const openEditDeadlineModal = (job) => {
  jobToEditDeadline.value = job

  // Pre-cargar la fecha actual en formato YYYY-MM-DD
  const currentDeadline = job.applicationDeadline || job.expiryDate
  if (currentDeadline) {
    newDeadlineDateString.value = currentDeadline // Ya viene en formato YYYY-MM-DD
  }

  showEditDeadlineModal.value = true
}

const closeEditDeadlineModal = () => {
  showEditDeadlineModal.value = false
  jobToEditDeadline.value = null
  newDeadlineDate.value = null
  newDeadlineDateString.value = ''
}

const saveNewDeadline = async () => {
  if (!newDeadlineDateString.value || !jobToEditDeadline.value) {
    notify({
      message: 'Por favor selecciona una fecha válida',
      color: 'danger'
    })
    return
  }

  // La fecha ya viene en formato YYYY-MM-DD del input nativo
  const formattedDate = newDeadlineDateString.value

  // Validaciones (las validaciones HTML5 ya cubren min/max, pero agregamos verificación adicional)
  const [yearSel, monthSel, daySel] = formattedDate.split('-')
  const selectedDate = new Date(yearSel, monthSel - 1, daySel)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  selectedDate.setHours(0, 0, 0, 0)

  // Validación 1: No puede ser anterior a hoy
  if (selectedDate < today) {
    notify({
      message: 'La fecha límite no puede ser anterior a hoy',
      color: 'danger'
    })
    return
  }

  // Validación 2: No puede exceder expiryDate
  const [yearExp, monthExp, dayExp] = jobToEditDeadline.value.expiryDate.split('-')
  const maxDate = new Date(yearExp, monthExp - 1, dayExp)
  maxDate.setHours(0, 0, 0, 0)

  if (selectedDate > maxDate) {
    notify({
      message: `La fecha límite no puede exceder la fecha de vencimiento del plan (${formatExpiryDate(jobToEditDeadline.value.expiryDate)})`,
      color: 'danger'
    })
    return
  }

  try {
    const response = await apiCall(`/jobs/${jobToEditDeadline.value.id}/update-deadline`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        applicationDeadline: formattedDate
      })
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al actualizar fecha límite')
    }

    if (data.success) {
      // Actualizar el job en el array local
      const jobIndex = jobs.value.findIndex(j => j.id === jobToEditDeadline.value.id)
      if (jobIndex !== -1) {
        jobs.value[jobIndex].applicationDeadline = formattedDate
      }

      notify({
        message: 'Fecha límite actualizada exitosamente',
        color: 'success'
      })

      closeEditDeadlineModal()
    } else {
      throw new Error(data.message || 'Error al actualizar fecha límite')
    }
  } catch (error) {
    notify({
      message: error.message || 'Error al actualizar la fecha límite',
      color: 'danger'
    })
  }
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
    // Llamar a get_job para traer datos completos usando apiCall
    const response = await apiCall(`/jobs/${job.id}/`, {
      method: 'GET'
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al cargar detalles del trabajo')
    }

    // Usar los datos completos del endpoint get_job
    selectedJob.value = data.job
    showDetailModal.value = true
  } catch (err) {
    if (err.message.includes('sesión ha sido cerrada')) {
      router.push('/login')
      return
    }
    notify({
      message: `Error al cargar detalles: ${err.message}`,
      color: 'danger'
    })
  }
}

const editJob = async (job) => {
  // Prevenir edición de anuncios expirados
  if (isJobExpired(job)) {
    notify({
      message: 'No puedes editar un anuncio expirado.',
      color: 'warning',
      duration: 3000,
      position: 'top-right'
    })
    return
  }

  try {
    // Cargar datos completos del job usando apiCall
    const response = await apiCall(`/jobs/${job.id}`, {
      method: 'GET'
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
    if (err.message.includes('sesión ha sido cerrada')) {
      router.push('/login')
      return
    }
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 4000,
      position: 'top-right'
    })
  }
}

const toggleJobStatus = async (job) => {
  // Prevenir cambios de estado en anuncios expirados
  if (isJobExpired(job)) {
    notify({
      message: 'No puedes cambiar el estado de un anuncio expirado.',
      color: 'warning',
      duration: 3000,
      position: 'top-right'
    })
    return
  }

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

    const response = await apiCall(`/jobs/${job.id}/update`, {
      method: 'PATCH',
      headers: {
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
    if (err.message.includes('sesión ha sido cerrada')) {
      router.push('/login')
      return
    }
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 4000,
      position: 'top-right',
      closeable: true
    })
  }
}

const deleteJob = (job) => {
  jobToDelete.value = job
  deleteConfirmed.value = false
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  jobToDelete.value = null
  deleteConfirmed.value = false
}

const confirmDelete = async () => {
  if (!deleteConfirmed.value || !jobToDelete.value) return

  try {
    const response = await apiCall(`/jobs/${jobToDelete.value.id}/delete`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Error al eliminar trabajo')
    }

    jobs.value = jobs.value.filter(j => j.id !== jobToDelete.value.id)

    closeDeleteModal()

    notify({
      message: 'Anuncio eliminado exitosamente',
      color: 'success',
      duration: 3000,
      position: 'top-right',
      closeable: true
    })
  } catch (err) {
    if (err.message.includes('sesión ha sido cerrada')) {
      router.push('/login')
      return
    }
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
    const response = await apiCall(`/jobs/${selectedJob.value.id}/update`, {
      method: 'PATCH',
      headers: {
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
    if (err.message.includes('sesión ha sido cerrada')) {
      router.push('/login')
      return
    }
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

    const response = await apiCall(`/jobs/${selectedJob.value.id}/update`, {
      method: 'PATCH',
      headers: {
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
    if (err.message.includes('sesión ha sido cerrada')) {
      router.push('/login')
      return
    }
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

    const response = await apiCall(`/jobs/${selectedJob.value.id}/update`, {
      method: 'PATCH',
      headers: {
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
    if (err.message.includes('sesión ha sido cerrada')) {
      router.push('/login')
      return
    }
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
  font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
  font-size: 1.35rem;
  font-weight: 600;
  color: #0F172A;
  letter-spacing: -0.01em;
  line-height: 1.3;
  font-family: 'Source Sans Pro', sans-serif;
}

.job-company {
  margin: 0.35rem 0 0;
  color: #64748B;
  font-size: 1rem;
  font-weight: 400;
  letter-spacing: 0.005em;
  font-family: 'Source Sans Pro', sans-serif;
}

.job-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-family: 'Source Sans Pro', sans-serif;
}

.job-badge.pending {
  background: #fff3e0;
  color: #e65100;
}

.job-badge.active {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.job-badge.closed {
  background: #ffebee;
  color: #c62828;
}

.job-badge.draft {
  background: #f3e5f5;
  color: #6a1b9a;
}

.job-badge.rejected {
  background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
  color: white;
  border: 1px solid #ef4444;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.4);
}

.job-badge.expired {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  border: 1px solid #fb923c;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.35);
}

/* ========== SEPARADORES DE SECCIONES ========== */
.section-divider {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
  padding: 0 1rem;
}

.divider-line {
  flex: 1;
  height: 2px;
  opacity: 0.3;
}

.divider-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.25rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.divider-label span {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.85rem;
}

/* Estilo para Anuncios Recientes (verde) */
.section-divider.recent .divider-line {
  background: linear-gradient(90deg, transparent 0%, #10b981 50%, transparent 100%);
}

.section-divider.recent .divider-label {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border: 1px solid #6ee7b7;
  color: #059669;
}

.section-divider.recent .divider-label span {
  color: #047857;
}

/* Estilo para Pendientes de Aprobación (amarillo/naranja) */
.section-divider.pending .divider-line {
  background: linear-gradient(90deg, transparent 0%, #f59e0b 50%, transparent 100%);
}

.section-divider.pending .divider-label {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 1px solid #fcd34d;
  color: #d97706;
}

.section-divider.pending .divider-label span {
  color: #b45309;
}

/* Estilo para Anuncios Expirados (rojo/naranja) */
.section-divider.expired .divider-line {
  background: linear-gradient(90deg, transparent 0%, #f97316 50%, transparent 100%);
}

.section-divider.expired .divider-label {
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border: 1px solid #fed7aa;
  color: #ea580c;
}

.section-divider.expired .divider-label span {
  color: #c2410c;
}

/* Estilo para Anuncios Rechazados (rojo intenso) */
.section-divider.rejected .divider-line {
  background: linear-gradient(90deg, transparent 0%, #dc2626 50%, transparent 100%);
}

.section-divider.rejected .divider-label {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 1px solid #fca5a5;
  color: #dc2626;
}

.section-divider.rejected .divider-label span {
  color: #991b1b;
}

/* ========== REJECTION ALERT ========== */
.rejection-alert {
  background: #fef2f2;
  padding: 1.25rem;
}

.rejection-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.rejection-header h4 {
  margin: 0;
  color: #dc2626;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.3px;
}

.rejection-message {
  color: #7f1d1d;
  margin: 0.5rem 0;
  font-size: 0.95rem;
  line-height: 1.5;
}

.rejection-message .terms-link {
  color: #dc2626;
  font-weight: 600;
  text-decoration: underline;
  transition: color 0.2s;
}

.rejection-message .terms-link:hover {
  color: #991b1b;
}

/* Motivo principal del rechazo - Prominente */
.rejection-main-reason {
  background: white;
  border: 2px solid #dc2626;
  border-radius: 6px;
  padding: 1rem;
  margin: 0.75rem 0;
}

.rejection-main-reason .reason-text {
  margin: 0;
  color: #991b1b;
  font-size: 1rem;
  font-weight: 600;
  white-space: pre-line;
  line-height: 1.6;
}

.rejection-footer {
  margin: 0.75rem 0 0 0;
  font-size: 0.85rem;
  color: #7f1d1d;
}

.rejection-footer .support-link {
  color: #dc2626;
  font-weight: 600;
  text-decoration: none;
  border-bottom: 1px solid #dc2626;
  transition: all 0.2s;
}

.rejection-footer .support-link:hover {
  color: #991b1b;
  border-bottom-color: #991b1b;
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
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748B;
  margin-right: 0.3rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-family: 'Source Sans Pro', sans-serif;
}

.stat-text {
  font-weight: 500;
  color: #0F172A;
  font-size: 0.95rem;
  letter-spacing: 0.005em;
  font-family: 'Source Sans Pro', sans-serif;
}

.stat-date {
  font-size: 0.9rem;
  color: #1E293B;
  font-weight: 500;
  letter-spacing: 0.003em;
  font-family: 'Source Sans Pro', sans-serif;
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
  padding: 0.3rem 0.7rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-family: 'Source Sans Pro', sans-serif;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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

.action-btn.edit.disabled,
.action-btn.edit:disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
  opacity: 0.6;
}

.action-btn.edit.disabled:hover,
.action-btn.edit:disabled:hover {
  transform: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  background: #e5e7eb;
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

/* ========== DELETE MODAL COMPACTO ========== */
.delete-header {
  text-align: center;
  padding: 1rem 0 0.5rem;
}

.delete-title {
  color: #DC2626;
  font-size: 1.4rem;
  font-weight: 700;
  margin: 0.75rem 0 0;
}

.delete-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem 0;
}

.job-info-box {
  background: #F9FAFB;
  border-left: 3px solid #7c3aed;
  padding: 0.75rem 1rem;
  border-radius: 6px;
}

.job-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1F2937;
}

.job-stats {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: #6B7280;
}

.warning-compact {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  padding: 0.75rem;
  background: #FEF2F2;
  border-radius: 6px;
  border: 1px solid #FECACA;
}

.warning-compact p {
  margin: 0;
  font-size: 0.85rem;
  color: #991B1B;
  line-height: 1.5;
}

.confirm-label {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  padding: 0.75rem;
  background: white;
  border: 1.5px solid #E5E7EB;
  border-radius: 6px;
  transition: all 0.2s;
}

.confirm-label:has(.confirm-check:checked) {
  border-color: #DC2626;
  background: #FEF2F2;
}

.confirm-check {
  display: none;
}

.confirm-box {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  border: 2px solid #D1D5DB;
  border-radius: 4px;
  background: white;
  position: relative;
  transition: all 0.2s;
}

.confirm-check:checked + .confirm-box {
  background: #DC2626;
  border-color: #DC2626;
}

.confirm-check:checked + .confirm-box::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 14px;
  font-weight: bold;
}

.confirm-text {
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

.confirm-check:checked ~ .confirm-text {
  color: #1F2937;
  font-weight: 600;
}

.delete-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.btn-delete {
  background: linear-gradient(135deg, #DC2626, #B91C1C) !important;
  color: white !important;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-delete:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

@media (max-width: 768px) {
  .delete-actions {
    flex-direction: column-reverse;
  }

  .delete-actions .va-button {
    width: 100%;
  }
}

/* ========== DEADLINE EDIT STYLES ========== */
.deadline-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.deadline-closed {
  color: #DC2626 !important;
  font-weight: 600;
}

.edit-deadline-btn {
  background: linear-gradient(135deg, #7C3AED, #6D28D9);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 0.35rem 0.6rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.5rem;
  box-shadow: 0 2px 4px rgba(124, 58, 237, 0.2);
  position: relative;
  overflow: hidden;
}

.edit-deadline-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.4s, height 0.4s;
}

.edit-deadline-btn:hover::before {
  width: 100px;
  height: 100px;
}

.edit-deadline-btn[style*="display: none"] {
  margin: 0;
  padding: 0;
  width: 0;
  height: 0;
  overflow: hidden;
}

.edit-deadline-btn:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 12px rgba(124, 58, 237, 0.4);
  border-color: rgba(255, 255, 255, 0.4);
}

.edit-deadline-btn:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 0 2px 4px rgba(124, 58, 237, 0.3);
}

.edit-deadline-btn .va-icon {
  color: white !important;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
  z-index: 1;
  position: relative;
}

.days-available {
  color: #10B981;
  font-weight: 500;
  font-size: 0.85rem;
  font-family: 'Source Sans Pro', sans-serif;
  letter-spacing: 0.005em;
}

/* Modal de Deadline */
.deadline-modal-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  text-align: center;
  margin-bottom: 1rem;
  position: relative;
}

.deadline-modal-header .header-icon {
  flex-shrink: 0;
}

.modal-close-btn {
  position: absolute;
  right: -0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: #F3F4F6;
  border: 2px solid #E5E7EB;
  cursor: pointer;
  padding: 0.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6B7280;
  transition: all 0.2s;
  border-radius: 50%;
  width: 2.25rem;
  height: 2.25rem;
}

.modal-close-btn:hover {
  background: #EF4444;
  color: white;
  border-color: #DC2626;
  transform: translateY(-50%) scale(1.05);
}

.modal-close-btn:active {
  transform: translateY(-50%) scale(0.95);
}

/* Native Date Input Styles */
.native-date-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #FFFFFF;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  transition: all 0.2s;
}

.native-date-input-wrapper:focus-within {
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.native-date-input-wrapper .date-icon {
  flex-shrink: 0;
}

.native-date-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1rem;
  font-family: inherit;
  color: #1F2937;
  background: transparent;
  cursor: pointer;
}

.native-date-input::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.native-date-input::-webkit-calendar-picker-indicator:hover {
  opacity: 1;
}

.deadline-modal-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
}

.deadline-modal-content {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 0.5rem;
}

.current-deadline-info {
  background: linear-gradient(135deg, #F9FAFB, #F3F4F6);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  border: 1px solid #E5E7EB;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.info-row.highlight {
  background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  gap: 0.5rem;
}

.info-label {
  font-weight: 600;
  color: #6B7280;
  font-size: 0.9rem;
}

.info-value {
  font-weight: 600;
  color: #1F2937;
}

.info-value.current {
  color: #7C3AED;
  font-size: 1.05rem;
}

.info-text {
  color: #059669;
  font-weight: 600;
  font-size: 0.9rem;
}

.warning-box {
  background: linear-gradient(135deg, #FEF3C7, #FDE68A);
  border: 1px solid #F59E0B;
  border-radius: 10px;
  padding: 0.85rem;
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
}

.warning-box p {
  margin: 0;
  color: #92400E;
  font-size: 0.9rem;
  line-height: 1.4;
}

.deadline-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 0.5rem;
}

.btn-save {
  background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
  color: white !important;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-save:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

/* ========== RESPONSIVE MODAL STYLES ========== */
@media (max-width: 768px) {
  .deadline-modal-header {
    gap: 0.5rem;
    margin-bottom: 0.75rem;
  }

  .deadline-modal-header .header-icon {
    width: 1.5rem;
    height: 1.5rem;
  }

  .deadline-modal-title {
    font-size: 1.1rem;
    line-height: 1.3;
  }

  .modal-close-btn {
    padding: 0.4rem;
    right: -0.5rem;
  }

  .deadline-modal-content {
    padding: 0.25rem;
    gap: 1rem;
  }

  .job-info-box {
    padding: 0.75rem;
  }

  .job-name {
    font-size: 0.95rem;
  }

  .job-stats {
    font-size: 0.8rem;
  }

  .current-deadline-info {
    padding: 0.75rem;
    gap: 0.6rem;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .info-row.highlight {
    flex-direction: row;
    align-items: center;
    padding: 0.5rem;
  }

  .info-label {
    font-size: 0.85rem;
  }

  .info-value {
    font-size: 0.9rem;
  }

  .info-value.current {
    font-size: 1rem;
  }

  .info-text {
    font-size: 0.85rem;
  }

  .native-date-input-wrapper {
    padding: 0.6rem 0.85rem;
  }

  .native-date-input {
    font-size: 0.95rem;
  }

  .field-hint {
    font-size: 0.8rem;
  }

  .warning-box {
    padding: 0.7rem;
    gap: 0.5rem;
  }

  .warning-box p {
    font-size: 0.85rem;
  }

  .deadline-modal-actions {
    flex-direction: column-reverse;
    gap: 0.5rem;
    padding-top: 0.25rem;
  }

  .deadline-modal-actions .va-button {
    width: 100%;
    font-size: 0.95rem;
  }

  .edit-deadline-btn {
    padding: 0.25rem 0.4rem;
  }
}

@media (max-width: 480px) {
  .deadline-modal-title {
    font-size: 1rem;
  }

  .job-name {
    font-size: 0.9rem;
  }

  .info-label,
  .info-value,
  .info-text {
    font-size: 0.8rem;
  }

  .native-date-input-wrapper {
    padding: 0.5rem 0.75rem;
  }

  .native-date-input {
    font-size: 0.9rem;
  }

  .warning-box p {
    font-size: 0.8rem;
    line-height: 1.3;
  }
}
</style>
