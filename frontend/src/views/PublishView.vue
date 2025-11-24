<template>
  <MainLayout>
    <!-- INDICADOR VISUAL DE PASOS -->
    <PublishStepsIndicator
      :current-step="publishStore.currentStep"
      :steps="wizardSteps"
    />

    <!-- PASO 0: Selección Inicial (Tipo de trabajo y Ciudad) -->
    <JobPublishStart
      v-if="publishStore.currentStep === 0"
      :model-value="{ subcategory: publishStore.jobData.subcategory, city: publishStore.jobData.city }"
      @update:formData="handleFormData"
      @proceed-to-wizard="proceedToWizard"
      @cancel="goHome"
    />

    <!-- PASO 1: Información del Trabajo -->
    <InformationStepJob
      v-if="publishStore.currentStep === 1"
      v-model="publishStore.jobData"
      @next="nextStep"
      @back="previousStep"
    />

    <!-- PASO 2: Plan de Pago -->
    <PlanStep
      v-if="publishStore.currentStep === 2"
      :model-value="publishStore.jobData.selectedPlan"
      @update:model-value="(plan) => publishStore.setJobData({ selectedPlan: plan })"
      @next="nextStep"
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
      @submit="handleSubmit"
      @back="previousStep"
    />
  </MainLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import { useAuthStore } from '@/stores/useAuthStore'
import { usePublishStore } from '@/stores/usePublishStore'
import MainLayout from '@/components/Layout/MainLayout.vue'
import PublishStepsIndicator from '@/components/Publish/PublishStepsIndicator.vue'
import JobPublishStart from '@/components/Publish/JobPublishStart.vue'
import InformationStepJob from '@/views/FormCreate/InformationStepJob.vue'
import ApplicationConfigStep from '@/components/Publish/ApplicationConfigStep.vue'
import PlanStep from '@/components/Publish/PlanStep.vue'
import SummaryCard from '@/components/Cards/SummaryCard.vue'

const router = useRouter()
const { init: notify } = useToast()
const authStore = useAuthStore()
const publishStore = usePublishStore()
const isSubmitting = ref(false)

// Definición de pasos del wizard (5 pasos simplificado)
const wizardSteps = ref([
  { name: 'Selección', description: 'Tipo de trabajo y ciudad' },
  { name: 'Información', description: 'Detalles del empleo' },
  { name: 'Plan de Pago', description: 'Elegir plan y precio' },
  { name: 'Aplicación', description: 'Configurar postulaciones' },
  { name: 'Resumen', description: 'Confirmación final' }
])

// ========== MÉTODOS DE NAVEGACIÓN CON SCROLL ==========
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const nextStep = () => {
  publishStore.nextStep()
  scrollToTop()
}

const previousStep = () => {
  publishStore.previousStep()
  scrollToTop()
}

// ========== HANDLERS ==========
const handleFormData = (data) => {
  console.log('Datos del formulario inicial:', data)
  publishStore.setJobData(data)
}

const proceedToWizard = () => {
  console.log('Procediendo al wizard...')
  console.log('Datos guardados:', {
    subcategory: publishStore.jobData.subcategory,
    city: publishStore.jobData.city
  })
  publishStore.setCurrentStep(1)
  scrollToTop()
}

const handleSubmit = async () => {
  // ========== VALIDACIÓN PREVIA ==========
  if (!authStore.isAuthenticated || !authStore.accessToken) {
    console.warn('⚠️ Usuario no autenticado')
    notify({
      message: 'Debes iniciar sesión para publicar un trabajo',
      color: 'warning',
      duration: 3000
    })
    router.push('/login')
    return
  }

  // ========== VALIDAR DATOS MÍNIMOS ==========
  const { title, description, email, city, contractType, expiryDate, requirements } = publishStore.jobData
  const fieldErrors = {}

  if (!title?.trim()) fieldErrors.title = 'Título es requerido'
  if (!description?.trim()) fieldErrors.description = 'Descripción es requerida'
  if (!email?.trim()) fieldErrors.email = 'Email es requerido'
  if (!city?.trim()) fieldErrors.city = 'Ciudad es requerida'
  if (!contractType?.trim()) fieldErrors.contractType = 'Tipo de contrato es requerido'
  if (!expiryDate) fieldErrors.expiryDate = 'Fecha de vencimiento es requerida'
  if (!requirements?.trim()) fieldErrors.requirements = 'Requisitos son requeridos'

  if (Object.keys(fieldErrors).length > 0) {
    console.error('❌ Errores de validación frontend:', fieldErrors)
    notify({
      message: 'Por favor, completa todos los campos requeridos',
      color: 'warning',
      duration: 4000
    })
    return
  }

  try {
    isSubmitting.value = true
    console.log('📝 Iniciando publicación...')
    console.log('Usuario:', authStore.user?.email)
    console.log('Datos:', {
      title,
      city,
      company: publishStore.jobData.companyName,
      plan: publishStore.jobData.selectedPlan
    })

    // Preparar datos - asegurarse que email esté incluido
    const jobData = {
      ...publishStore.jobData,
      email: authStore.user?.email || publishStore.jobData.email
    }

    console.log('📤 Enviando a http://localhost:8000/api/jobs/publish...')

    // Llamar al endpoint backend con autenticación
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 30000) // 30s timeout

    const response = await fetch('http://localhost:8000/api/jobs/publish', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.accessToken}`
      },
      body: JSON.stringify(jobData),
      signal: controller.signal
    })

    clearTimeout(timeoutId)
    console.log(`📥 Response status: ${response.status}`)

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

    console.log('✅ Publicación exitosa:')
    console.log('   ID:', result.id)
    console.log('   Creado en:', result.createdAt)
    console.log('   Mensaje:', result.message)

    // Mostrar éxito
    notify({
      message: '¡Oferta publicada exitosamente! 🎉',
      color: 'success',
      duration: 3000
    })

    // Limpiar form
    publishStore.resetForm()

    // Redirigir a detalle del trabajo
    console.log(`🔗 Redirigiendo a /guias/trabajos/${result.id}...`)
    setTimeout(() => {
      router.push(`/guias/trabajos/${result.id}`)
    }, 500)

  } catch (error) {
    console.error('❌ Error de conexión:', error)
    console.error('Tipo de error:', error.name)
    console.error('Mensaje:', error.message)

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
</script>

<style scoped>
/* No se necesitan estilos adicionales, cada paso tiene los suyos */
</style>
