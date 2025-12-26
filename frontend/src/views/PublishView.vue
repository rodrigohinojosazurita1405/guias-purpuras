<template>
  <MainLayout>
    <!-- BOTÓN LIMPIAR BORRADOR (flotante en la esquina) -->
    <div v-if="publishStore.currentStep > 0" class="clear-draft-btn">
      <va-button
        preset="plain"
        size="small"
        icon="refresh"
        @click="showClearConfirm = true"
        title="Limpiar borrador y empezar de nuevo"
        class="clear-btn"
      >
        Limpiar
      </va-button>
    </div>

    <!-- MODAL DE CONFIRMACIÓN PARA LIMPIAR BORRADOR -->
    <va-modal
      v-model="showClearConfirm"
      size="small"
      hide-default-actions
      :mobile-fullscreen="false"
    >
      <template #header>
        <div class="modal-title">
          <va-icon name="warning" color="warning" size="1.5rem" />
          <span>Confirmar acción</span>
        </div>
      </template>

      <div class="modal-content">
        <p class="modal-message">
          ¿Estás seguro de que deseas limpiar el borrador?
        </p>
        <p class="modal-warning">
          Todos los cambios no guardados se perderán y deberás comenzar desde el inicio.
        </p>
      </div>

      <template #footer>
        <div class="modal-actions">
          <va-button
            preset="secondary"
            @click="showClearConfirm = false"
            class="btn-cancel"
          >
            Cancelar
          </va-button>
          <va-button
            color="danger"
            @click="confirmClearDraft"
            class="btn-confirm"
          >
            Sí, limpiar
          </va-button>
        </div>
      </template>
    </va-modal>

    <!-- INDICADOR VISUAL DE PASOS -->
    <PublishStepsIndicator
      :current-step="publishStore.currentStep"
      :steps="wizardSteps"
    />

    <!-- PASO 0: Selección Inicial (Tipo de trabajo y Ciudad) -->
    <JobPublishStart
      v-if="publishStore.currentStep === 0"
      :model-value="{ contractType: publishStore.jobData.contractType, city: publishStore.jobData.city }"
      @update:formData="handleFormData"
      @proceed-to-wizard="proceedToWizard"
      @cancel="goHome"
    />

    <!-- PASO 1: Plan de Pago -->
    <PlanStep
      v-if="publishStore.currentStep === 1"
      ref="planStepRef"
      :model-value="publishStore.jobData.selectedPlan"
      @update:model-value="(plan) => publishStore.setJobData({ selectedPlan: plan })"
      @next="handlePlanStepNext"
      @back="previousStep"
    />

    <!-- PASO 2: Información del Trabajo -->
    <InformationStepJob
      v-if="publishStore.currentStep === 2"
      ref="informationStepRef"
      v-model="publishStore.jobData"
      @next="handleInformationStepNext"
      @back="previousStep"
    />

    <!-- PASO 3: Configuración de Aplicación -->
    <ApplicationConfigStep
      v-if="publishStore.currentStep === 3"
      v-model="publishStore.jobData"
      @next="nextStep"
      @back="previousStep"
    />

    <!-- PASO 4: Resumen y Confirmación -->
    <SummaryCard
      v-if="publishStore.currentStep === 4"
      type="job"
      :job-data="publishStore.jobData"
      :form-data="{}"
      :is-submitting="isSubmitting"
      @submit="handleSubmit"
      @back="previousStep"
    />

    <!-- MODAL DE ÉXITO DESPUÉS DE PUBLICACIÓN -->
    <PublishSuccessModal
      v-model="showSuccessModal"
      :job-data="publishedJob"
      @publish-another="() => {
        publishStore.setCurrentStep(0)
        showSuccessModal = false
      }"
    />
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import { useAuthStore } from '@/stores/useAuthStore'
import { usePublishStore } from '@/stores/usePublishStore'
import { useCompanyStore } from '@/stores/useCompanyStore'
import MainLayout from '@/components/Layout/MainLayout.vue'
import PublishStepsIndicator from '@/components/Publish/PublishStepsIndicator.vue'
import JobPublishStart from '@/components/Publish/JobPublishStart.vue'
import InformationStepJob from '@/views/FormCreate/InformationStepJob.vue'
import ApplicationConfigStep from '@/components/Publish/ApplicationConfigStep.vue'
import PlanStep from '@/components/Publish/PlanStep.vue'
import SummaryCard from '@/components/Cards/SummaryCard.vue'
import PublishSuccessModal from '@/components/Modals/PublishSuccessModal.vue'

const router = useRouter()
const { init: notify } = useToast()
const authStore = useAuthStore()
const publishStore = usePublishStore()
const companyStore = useCompanyStore()
const isSubmitting = ref(false)

// Refs para acceder a métodos validate() de los componentes
const planStepRef = ref(null)
const informationStepRef = ref(null)

// Estado del modal de éxito
const showSuccessModal = ref(false)
const publishedJob = ref(null)

// Estado del modal de confirmación para limpiar borrador
const showClearConfirm = ref(false)

// ========== CARGAR BORRADOR Y OBTENER EMPRESA ==========
onMounted(async () => {
  // Verificar si viene un jobId en query params (edición de anuncio existente)
  const jobId = router.currentRoute.value.query.jobId

  if (jobId) {
    // Modo edición: cargar datos del anuncio existente
    try {
      const response = await fetch(`/api/jobs/${jobId}/`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })

      const data = await response.json()

      if (data.success && data.job) {
        const job = data.job
        // Cargar todos los datos del trabajo en la store
        publishStore.setJobData({
          id: job.id,
          title: job.title,
          description: job.description,
          city: job.city,
          municipality: job.municipality,
          subcategory: job.subcategory,
          contractType: job.contractType,
          modality: job.modality,
          expiryDate: job.expiryDate,
          requirements: job.requirements,
          responsibilities: job.responsibilities,
          education: job.education,
          experience: job.experience,
          languages: job.languages,
          technicalSkills: job.technicalSkills,
          softSkills: job.softSkills,
          salaryType: job.salaryType,
          salaryMin: job.salaryMin,
          salaryMax: job.salaryMax,
          salaryFixed: job.salaryFixed,
          benefits: job.benefits,
          vacancies: job.vacancies,
          applicationInstructions: job.applicationInstructions,
          applicationType: job.applicationType,
          externalApplicationUrl: job.externalApplicationUrl,
          selectedPlan: job.selectedPlan,
          jobCategory: job.jobCategory,
          companyName: job.companyName,
          companyAnonymous: job.companyAnonymous,
          screeningQuestions: job.screeningQuestions || []
        })

        // Ir al paso 2 (Información) ya que el plan ya está seleccionado
        publishStore.setCurrentStep(2)
        notify({
          message: `✓ Anuncio cargado: ${job.title}`,
          color: 'success'
        })
      } else {
        throw new Error(data.message || 'Error al cargar anuncio')
      }
    } catch (error) {
      console.error('Error cargando anuncio:', error)
      notify({
        message: `Error al cargar anuncio: ${error.message}`,
        color: 'danger'
      })
      // Volver al paso 0 en caso de error
      publishStore.setCurrentStep(0)
    }
  } else {
    // Modo creación: cargar borrador guardado
    publishStore.loadDraftFromStorage()
  }

  try {
    // Obtener la empresa del usuario autenticado
    const result = await companyStore.getMyCompany()

    if (result.success && result.company) {
      // Asignar datos de empresa al jobData (solo si no vienen del borrador o del trabajo cargado)
      if (!jobId) {
        publishStore.setJobData({
          companyName: result.company.companyName,
          companyId: result.company.id,
          logo: result.company.logo || null, // URL completa desde el backend
          city: publishStore.jobData.city || result.company.city // Prioriza lo guardado
        })
      }
    }
  } catch (error) {
    console.error('Error al obtener empresa:', error)
  }
})

// Definición de pasos del wizard (5 pasos simplificado)
const wizardSteps = ref([
  { name: 'Selección', description: 'Tipo de trabajo y ciudad' },
  { name: 'Plan de Pago', description: 'Elegir plan y precio' },
  { name: 'Información', description: 'Detalles del empleo' },
  { name: 'Aplicación', description: 'Configurar postulaciones' },
  { name: 'Resumen', description: 'Confirmación final' }
])

// ========== MÉTODOS DE NAVEGACIÓN CON SCROLL ==========
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handlePlanStepNext = () => {
  // Validar que se ha seleccionado un plan
  if (planStepRef.value && !planStepRef.value.validate()) {
    notify({
      message: 'Por favor, selecciona un plan de pago para continuar',
      color: 'warning',
      duration: 3000
    })
    return
  }
  nextStep()
}

const handleInformationStepNext = () => {
  // Validar que se han completado los datos
  if (informationStepRef.value && !informationStepRef.value.validate()) {
    // El componente ya muestra un alert con los errores
    return
  }
  nextStep()
}

const nextStep = () => {
  publishStore.nextStep()

  // Cuando se llega al paso 4 (resumen), setear la fecha de publicación si no existe
  if (publishStore.currentStep === 4 && !publishStore.jobData.publishedDate) {
    publishStore.setJobData({
      publishedDate: new Date().toISOString()
    })
  }

  scrollToTop()
}

const previousStep = () => {
  publishStore.previousStep()
  scrollToTop()
}

// ========== HANDLERS ==========
const handleFormData = (data) => {
  publishStore.setJobData(data)
}

const proceedToWizard = () => {
  publishStore.setCurrentStep(1)
  scrollToTop()
}

const handleSubmit = async () => {
  // ========== VALIDACIÓN PREVIA ==========
  if (!authStore.isAuthenticated || !authStore.accessToken) {
    notify({
      message: 'Debes iniciar sesión para publicar un trabajo',
      color: 'warning',
      duration: 3000
    })
    router.push('/login')
    return
  }

  // ========== VALIDAR DATOS MÍNIMOS ==========
  const { title, description, city, contractType, expiryDate } = publishStore.jobData
  const email = authStore.user?.email // Email del usuario autenticado
  const fieldErrors = {}

  if (!title?.trim()) fieldErrors.title = 'Título es requerido'
  if (!description?.trim()) fieldErrors.description = 'Descripción es requerida'
  if (!email?.trim()) fieldErrors.email = 'Email es requerido'
  if (!city?.trim()) fieldErrors.city = 'Ciudad es requerida'
  if (!contractType?.trim()) fieldErrors.contractType = 'Tipo de contrato es requerido'
  if (!expiryDate) fieldErrors.expiryDate = 'Fecha de vencimiento es requerida'

  // FASE 7.1: Validación de comprobante de pago obligatorio (verificar el archivo real en la store)
  if (!publishStore.proofOfPaymentFile) fieldErrors.proofOfPayment = 'El comprobante de pago es requerido'

  if (Object.keys(fieldErrors).length > 0) {
    console.error('❌ Errores de validación frontend:', fieldErrors)
    notify({
      message: 'Por favor, completa todos los campos requeridos incluido el comprobante de pago',
      color: 'warning',
      duration: 4000
    })
    return
  }

  try {
    isSubmitting.value = true

    // Preparar datos como FormData para permitir envío de archivo (FASE 7.1)
    const formData = new FormData()

    // Agregar todos los campos del jobData
    Object.keys(publishStore.jobData).forEach(key => {
      const value = publishStore.jobData[key]

      // Saltar proofOfPaymentPreview (es solo para preview, no enviar al backend)
      if (key === 'proofOfPaymentPreview') return

      // Para expiryDate (Date object), convertir a ISO 8601 format (YYYY-MM-DD)
      if (key === 'expiryDate' && value instanceof Date) {
        formData.append(key, value.toISOString().split('T')[0])
      }
      // Para screeningQuestions (es array), convertir a JSON
      else if (key === 'screeningQuestions' && Array.isArray(value)) {
        formData.append(key, JSON.stringify(value))
      }
      // Para billingData (es objeto), convertir a JSON
      else if (key === 'billingData' && value && typeof value === 'object') {
        formData.append(key, JSON.stringify(value))
      }
      // Para modality, si es un objeto extraer solo el valor
      else if (key === 'modality' && value && typeof value === 'object' && value.value) {
        formData.append(key, value.value)
      }
      // Para booleanos, convertir explícitamente a string 'true' o 'false'
      else if (typeof value === 'boolean') {
        formData.append(key, value.toString())
      }
      else if (value != null && value !== '') {
        formData.append(key, value)
      }
    })

    // Agregar email del usuario autenticado
    formData.append('email', authStore.user?.email || publishStore.jobData.email)

    // FASE 7.1: Agregar archivo de comprobante de pago si existe
    if (publishStore.proofOfPaymentFile) {
      formData.append('proofOfPayment', publishStore.proofOfPaymentFile)
    }

    // Llamar al endpoint backend con autenticación
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 30000) // 30s timeout

    const response = await fetch('http://localhost:8000/api/jobs/publish', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
        // NO establecer Content-Type: multipart/form-data, el navegador lo hace automáticamente
      },
      body: formData,
      signal: controller.signal
    })

    clearTimeout(timeoutId)

    // Parsear respuesta
    let result
    try {
      result = await response.json()
    } catch (parseError) {
      console.error('❌ Error al parsear JSON:', parseError)
      notify({
        message: 'Error: Respuesta inválida del servidor',
        color: 'danger',
        duration: 4000
      })
      return
    }

    // ========== MANEJO DE ERRORES ==========
    if (!response.ok) {
      console.error('❌ Error del servidor (status:', response.status, '):', result)

      // Errores de validación (400)
      if (response.status === 400) {
        if (result.errors) {
          const errorMessages = Object.entries(result.errors)
            .map(([field, message]) => `• ${field}: ${message}`)
            .join('\n')
          console.error('Errores de campo:', errorMessages)
          notify({
            message: `Errores de validación:\n${errorMessages}`,
            color: 'warning',
            duration: 5000
          })
        } else {
          notify({
            message: result.message || 'Datos inválidos',
            color: 'warning',
            duration: 4000
          })
        }
        return
      }

      // Error de autenticación (401)
      if (response.status === 401) {
        console.error('Token inválido o expirado')
        notify({
          message: 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.',
          color: 'danger',
          duration: 4000
        })
        authStore.logout()
        router.push('/login')
        return
      }

      // Error del servidor (500)
      if (response.status === 500) {
        console.error('Error interno del servidor')
        notify({
          message: 'Error interno del servidor. Por favor, intenta más tarde.',
          color: 'danger',
          duration: 4000
        })
        return
      }

      // Error genérico
      notify({
        message: result.message || `Error (${response.status}): No se pudo publicar la oferta`,
        color: 'danger',
        duration: 4000
      })
      return
    }

    // ========== ÉXITO ==========
    // Validar respuesta exitosa
    if (!result.success || !result.id) {
      console.error('❌ Respuesta exitosa pero sin ID:', result)
      notify({
        message: 'Error: La oferta se publicó pero no se pudo obtener su ID',
        color: 'danger',
        duration: 4000
      })
      return
    }

    // Guardar datos del job publicado para mostrar en el modal
    publishedJob.value = {
      id: result.id,
      title: publishStore.jobData.title,
      createdAt: result.createdAt
    }

    // Mostrar modal de éxito
    showSuccessModal.value = true

    // Limpiar form
    publishStore.resetForm()

  } catch (error) {
    console.error('❌ Error de conexión:', error)

    // Diferenciar tipos de error
    if (error.name === 'AbortError') {
      notify({
        message: 'Timeout: El servidor tardó demasiado en responder (30s). Por favor, intenta nuevamente.',
        color: 'danger',
        duration: 5000
      })
    } else if (error instanceof TypeError && error.message.includes('fetch')) {
      notify({
        message: 'Error de conexión: No se pudo conectar al servidor. Verifica que esté disponible.',
        color: 'danger',
        duration: 5000
      })
    } else {
      notify({
        message: `Error de conexión: ${error.message}`,
        color: 'danger',
        duration: 4000
      })
    }
  } finally {
    isSubmitting.value = false
  }
}

const goHome = () => {
  publishStore.resetForm()
  router.push('/')
}

// Limpiar borrador manualmente (confirmación)
const confirmClearDraft = () => {
  publishStore.resetForm()
  showClearConfirm.value = false
  notify({
    message: 'Borrador limpiado exitosamente.',
    color: 'success',
    duration: 2000
  })
}
</script>

<style scoped>
/* BOTÓN LIMPIAR BORRADOR */
.clear-draft-btn {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 100;
}

.clear-btn {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%) !important;
  color: white !important;
  padding: 0.6rem 1.2rem !important;
  border-radius: 10px !important;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4) !important;
  backdrop-filter: blur(10px);
  text-transform: uppercase;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  transition: all 0.3s ease !important;
  border: none !important;
}

.clear-btn:hover {
  background: linear-gradient(135deg, #6D28D9 0%, #9333EA 100%) !important;
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.5) !important;
  transform: translateY(-2px);
}

.clear-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.4) !important;
}

.clear-draft-btn :deep(.va-button__content) {
  color: white !important;
}

.clear-draft-btn :deep(.va-icon) {
  color: white !important;
  margin-right: 0.35rem;
}

@media (max-width: 768px) {
  .clear-draft-btn {
    top: 70px;
    right: 10px;
    padding: 0.35rem;
  }
}

/* MODAL DE CONFIRMACIÓN */
:deep(.va-modal__container) {
  backdrop-filter: none !important;
  background: rgba(0, 0, 0, 0.5) !important;
}

:deep(.va-modal__dialog) {
  border-radius: 16px !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2) !important;
  max-width: 450px !important;
  width: 100% !important;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.modal-title span {
  flex: 1;
}

.modal-content {
  padding: 1rem 0;
}

.modal-message {
  font-size: 1rem;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.modal-warning {
  font-size: 0.9rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  width: 100%;
  flex-wrap: wrap;
}

.modal-actions .va-button {
  min-width: 100px;
  flex: 1;
  max-width: 150px;
}

/* RESPONSIVE MÓVIL */
@media (max-width: 640px) {
  :deep(.va-modal__dialog) {
    margin: 1rem !important;
    max-width: calc(100vw - 2rem) !important;
  }

  .modal-title {
    font-size: 1rem;
    gap: 0.5rem;
  }

  .modal-title .va-icon {
    font-size: 1.25rem !important;
  }

  .modal-content {
    padding: 0.75rem 0;
  }

  .modal-message {
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
  }

  .modal-warning {
    font-size: 0.85rem;
  }

  .modal-actions {
    gap: 0.5rem;
    flex-direction: column;
  }

  .modal-actions .va-button {
    width: 100%;
    max-width: 100%;
    min-width: 100%;
  }

  .btn-cancel {
    order: 2;
  }

  .btn-confirm {
    order: 1;
  }
}
</style>
