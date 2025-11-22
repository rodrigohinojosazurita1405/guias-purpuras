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
  // Validar autenticación
  if (!authStore.isAuthenticated || !authStore.accessToken) {
    notify({
      message: 'Debes iniciar sesión para publicar un trabajo',
      color: 'warning'
    })
    router.push('/login')
    return
  }

  try {
    isSubmitting.value = true
    console.log('📝 Enviando publicación al backend...')
    console.log('Datos:', publishStore.jobData)

    // Preparar datos - asegurarse que email esté incluido
    const jobData = {
      ...publishStore.jobData,
      email: authStore.user?.email || publishStore.jobData.email
    }

    // Llamar al endpoint backend con autenticación
    const response = await fetch('http://localhost:8000/api/jobs/publish', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.accessToken}`
      },
      body: JSON.stringify(jobData)
    })

    const result = await response.json()

    if (!response.ok) {
      console.error('❌ Error del servidor:', result)
      notify({
        message: result.message || 'Error al publicar la oferta',
        color: 'danger',
        duration: 4000
      })
      return
    }

    console.log('✅ Publicación exitosa:', result)

    // Mostrar éxito
    notify({
      message: '¡Oferta publicada exitosamente! 🎉',
      color: 'success',
      duration: 3000
    })

    // Limpiar form y redirigir
    publishStore.resetForm()
    setTimeout(() => {
      router.push(`/guias/trabajos/${result.id}`)
    }, 500)
  } catch (error) {
    console.error('❌ Error de conexión:', error)
    notify({
      message: `Error de conexión: ${error.message}`,
      color: 'danger',
      duration: 4000
    })
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
