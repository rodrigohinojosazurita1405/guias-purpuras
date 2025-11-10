<!-- frontend/src/views/Create/RestaurantCreate.vue -->
<!-- EXTRAÍDO DE PUBLISHVIEW - GASTRONOMÍA DEDICADO -->
<template>
  <MainLayout>
    <div class="restaurant-create">
      
      <!-- Header -->
      <div class="create-header">
        <div class="header-icon">
          <va-icon name="restaurant" size="3rem" color="#5C0099" />
        </div>
        <h1 class="header-title">Publica tu Restaurante</h1>
        <p class="header-subtitle">
          Llega a miles de comensales y haz crecer tu negocio gastronómico
        </p>
      </div>

      <!-- Progress Bar -->
      <div class="progress-container">
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :style="{ width: ((currentStep / 7) * 100) + '%' }"
          ></div>
        </div>
        <div class="progress-steps">
          <div 
            v-for="(step, index) in steps" 
            :key="index"
            class="progress-step"
            :class="{ 
              active: currentStep === index + 1,
              completed: currentStep > index + 1
            }"
          >
            <div class="step-circle">
              <va-icon 
                v-if="currentStep > index + 1" 
                name="check" 
                size="1.2rem" 
              />
              <span v-else>{{ index + 1 }}</span>
            </div>
            <span class="step-name">{{ step }}</span>
          </div>
        </div>
      </div>

      <!-- Form Container -->
      <div class="form-card">
        
        <!-- Step 1: Información del Restaurante -->
        <div v-if="currentStep === 1" class="form-step">
          <InformationStepGastronomia
            ref="informationStepRef"
            v-model="formData"
            :subcategory="formData.subcategory"
          />
        </div>

        <!-- Step 2: GPS -->
        <div v-if="currentStep === 2" class="form-step">
          <GPSStep
            ref="gpsStepRef"
            v-model:coordinates="formData.coordinates"
            v-model:address="formData.gpsAddress"
          />
        </div>

        <!-- Step 3: SEO -->
        <div v-if="currentStep === 3" class="form-step">
          <SEOStep
            ref="seoStepRef"
            v-model="formData.seoData"
            entity-type="restaurante"
            base-url="guiaspurpuras.com/gastronomia"
          />
        </div>

        <!-- Step 4: Imágenes -->
        <div v-if="currentStep === 4" class="form-step">
          <ImagesStep
            ref="imagesStepRef"
            v-model="formData.images"
            :plan="formData.plan"
          />
        </div>

        <!-- Step 5: Menú -->
        <div v-if="currentStep === 5" class="form-step">
          <MenuStep
            ref="menuStepRef"
            v-model="formData.menuItems"
          />
        </div>

        <!-- Step 6: Plan -->
        <div v-if="currentStep === 6" class="form-step">
          <PlanStep
            ref="planStepRef"
            v-model="formData.plan"
          />
        </div>

        <!-- Step 7: Confirmar -->
        <div v-if="currentStep === 7" class="form-step">
          <div class="summary-step">
            <SummaryCard 
              :form-data="formData"
              :editable="true"
              @edit-step="goToStep"
            />
          </div>
        </div>

        <!-- Navigation -->
        <div class="form-navigation">
          <va-button
            v-if="currentStep > 1"
            @click="previousStep"
            color="secondary"
            size="large"
          >
            <va-icon name="arrow_back" />
            Anterior
          </va-button>

          <div style="flex: 1;"></div>

          <va-button
            v-if="currentStep < 7"
            @click="nextStep"
            color="success"
            size="large"
            :disabled="!isCurrentStepValid"
          >
            Continuar
            <va-icon name="arrow_forward" />
          </va-button>

          <va-button
            v-if="currentStep === 7"
            @click="submitForm"
            color="success"
            size="large"
            :loading="isSubmitting"
          >
            <va-icon name="check" />
            Publicar Restaurante
          </va-button>
        </div>

      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'

// Imports
import MainLayout from '@/components/Layout/MainLayout.vue'
import InformationStepGastronomia from '@/components/Publish/InformationStepGastronomia.vue'
import GPSStep from '@/components/Publish/GPSStep.vue'
import SEOStep from '@/components/Publish/SEOStep.vue'
import ImagesStep from '@/components/Publish/ImagesStep.vue'
import MenuStep from '@/components/Publish/MenuStep.vue'
import PlanStep from '@/components/Publish/PlanStep.vue'
import SummaryCard from '@/components/Publish/SummaryCard.vue'

// Composables
const router = useRouter()
const { init: notify } = useToast()

// State
const currentStep = ref(1)
const isSubmitting = ref(false)

// Refs
const informationStepRef = ref(null)
const gpsStepRef = ref(null)
const seoStepRef = ref(null)
const imagesStepRef = ref(null)
const menuStepRef = ref(null)
const planStepRef = ref(null)

// Steps
const steps = ['Información', 'GPS', 'SEO', 'Imágenes', 'Menú', 'Plan', 'Confirmar']

// Form Data (extraído de PublishView para gastronomía)
const formData = ref({
  category: 'gastronomia',
  subcategory: '',
  city: '',
  address: '',
  title: '',
  description: '',
  price: null,
  priceRange: '',
  deliveryAvailable: false,
  capacity: null,
  parking: false,
  features: [],
  menuItems: [],
  schedule: '',
  whatsapp: '',
  email: '',
  website: '',
  images: [],
  plan: 'free',
  // GPS Fields
  coordinates: '',
  gpsAddress: '',
  // SEO Fields
  seoData: {
    slug: '',
    mainKeyword: '',
    tags: [],
    metaDescription: '',
    locationKeywords: '',
    categories: []
  }
})

// Computed
const isCurrentStepValid = computed(() => {
  // Implementar validaciones según step actual
  switch (currentStep.value) {
    case 1:
      return informationStepRef.value?.isValid() || false
    case 2:
      return true // GPS es opcional
    case 3:
      return seoStepRef.value?.isValid() || false
    case 4:
      return imagesStepRef.value?.isValid() || false
    case 5:
      return menuStepRef.value?.isValid() || false
    case 6:
      return planStepRef.value?.isValid() || false
    case 7:
      return true
    default:
      return false
  }
})

// Methods
const nextStep = async () => {
  const isValid = await validateCurrentStep()
  
  if (!isValid) {
    notify({
      message: 'Por favor completa los campos requeridos',
      color: 'warning'
    })
    return
  }
  
  if (currentStep.value < 7) {
    currentStep.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const goToStep = (step) => {
  currentStep.value = step
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const validateCurrentStep = async () => {
  let stepRef = null
  
  switch (currentStep.value) {
    case 1:
      stepRef = informationStepRef.value
      break
    case 2:
      return true // GPS es opcional
    case 3:
      stepRef = seoStepRef.value
      break
    case 4:
      stepRef = imagesStepRef.value
      break
    case 5:
      stepRef = menuStepRef.value
      break
    case 6:
      stepRef = planStepRef.value
      break
    default:
      return true
  }
  
  if (stepRef && typeof stepRef.validate === 'function') {
    return await stepRef.validate()
  }
  
  return true
}

const submitForm = async () => {
  isSubmitting.value = true
  
  try {
    // Simular envío
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    notify({
      message: '¡Restaurante publicado exitosamente!',
      color: 'success'
    })
    
    // Redirigir
    router.push('/guias/gastronomia')
  } catch (error) {
    notify({
      message: 'Error al publicar el restaurante',
      color: 'danger'
    })
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
/* Container */
.restaurant-create {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}

/* Header */
.create-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 3px solid #5C0099;
}

.header-icon {
  margin-bottom: 1rem;
}

.header-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #5C0099;
  margin: 0 0 1rem 0;
}

.header-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

/* Progress */
.progress-container {
  margin-bottom: 3rem;
}

.progress-bar {
  height: 4px;
  background: #E0E0E0;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #5C0099 0%, #8B5CF6 100%);
  transition: width 0.3s ease;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #E0E0E0;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  transition: all 0.3s ease;
}

.progress-step.active .step-circle {
  background: #5C0099;
  color: white;
  transform: scale(1.1);
}

.progress-step.completed .step-circle {
  background: #4CAF50;
  color: white;
}

.step-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #666;
  text-align: center;
}

.progress-step.active .step-name {
  color: #5C0099;
}

.progress-step.completed .step-name {
  color: #4CAF50;
}

/* Form */
.form-card {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.form-step {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Navigation */
.form-navigation {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
  align-items: center;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 2px solid #E0E0E0;
}

/* Summary */
.summary-step {
  background: #F8F4FF;
  border-radius: 12px;
  padding: 2rem;
}

/* Responsive */
@media (max-width: 968px) {
  .restaurant-create {
    padding: 1rem;
  }

  .form-card {
    padding: 2rem 1.5rem;
  }

  .progress-steps {
    overflow-x: auto;
    padding-bottom: 1rem;
  }

  .step-name {
    font-size: 0.75rem;
  }

  .form-navigation {
    flex-direction: column-reverse;
    gap: 1rem;
  }
}
</style>