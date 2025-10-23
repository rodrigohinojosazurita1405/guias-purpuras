<template>
  <MainLayout>
    <section class="publish-section">
      <div class="container">
        <div class="publish-header">
          <h1 class="publish-title">Publica tu Anuncio</h1>
          <p class="publish-subtitle">
            Completa el formulario y llega a miles de personas en Bolivia
          </p>
        </div>

        <PublishSteps 
          :current-step="currentStep" 
          :steps="stepsList" 
        />

        <div class="form-card" :key="currentStep">
          
          <CategoryStep
            v-if="currentStep === 1"
            ref="categoryStepRef"
            v-model="formData"
          />

          <InformationStepProfessional
            v-if="currentStep === 2 && formData.category === 'profesionales'"
            ref="informationStepRef"
            v-model="formData"
            :subcategory="formData.subcategory"
          />
          
          <InformationStepGastronomia
            v-if="currentStep === 2 && formData.category === 'gastronomia'"
            ref="informationStepRef"
            v-model="formData"
            :subcategory="formData.subcategory"
          />
          
          <InformationStep
            v-if="currentStep === 2 && formData.category !== 'profesionales' && formData.category !== 'gastronomia'"
            ref="informationStepRef"
            v-model="formData"
          />

          <ImagesStep
            v-if="currentStep === 3"
            ref="imagesStepRef"
            v-model="formData.images"
            :plan="formData.plan"
          />

          <MenuStep
            v-if="currentStep === 4 && formData.category === 'gastronomia'"
            ref="menuStepRef"
            v-model="formData.menuItems"
          />

          <PlanStep
            v-if="(currentStep === 4 && formData.category !== 'gastronomia') || (currentStep === 5 && formData.category === 'gastronomia')"
            ref="planStepRef"
            v-model="formData.plan"
          />

          <div 
            v-if="(currentStep === 5 && formData.category !== 'gastronomia') || (currentStep === 6 && formData.category === 'gastronomia')"
            class="summary-step"
          >
            <SummaryCard 
              :form-data="formData"
              :editable="true"
              @edit-step="goToStep"
            />
          </div>

          <div class="form-navigation">
            <va-button
              v-if="currentStep > 1"
              @click="previousStep"
              color="secondary"
              size="large"
              class="nav-btn"
            >
              <va-icon name="arrow_back" />
              Anterior
            </va-button>

            <div class="spacer"></div>

            <va-button
              v-if="currentStep < getTotalSteps()"
              @click="nextStep"
              color="purple"
              size="large"
              class="nav-btn"
              :disabled="isSubmitting"
            >
              Siguiente
              <va-icon name="arrow_forward" />
            </va-button>

            <va-button
              v-if="currentStep === getTotalSteps()"
              @click="submitForm"
              color="yellow-primary"
              size="large"
              class="nav-btn submit-btn"
              :loading="isSubmitting"
            >
              <va-icon name="check_circle" />
              {{ formData.plan === 'free' ? 'Publicar Gratis' : 'Ir al Pago' }}
            </va-button>
          </div>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '@/components/Layout/MainLayout.vue'
import PublishSteps from '@/components/Publish/PublishSteps.vue'
import CategoryStep from '@/components/Publish/CategoryStep.vue'
import InformationStep from '@/components/Publish/InformationStep.vue'
import InformationStepProfessional from '@/components/Publish/InformationStepProfessional.vue'
import InformationStepGastronomia from '@/components/Publish/InformationStepGastronomia.vue'
import ImagesStep from '@/components/Publish/ImagesStep.vue'
import MenuStep from '@/components/Publish/MenuStep.vue'
import PlanStep from '@/components/Publish/PlanStep.vue'
import SummaryCard from '@/components/Publish/SummaryCard.vue'

const router = useRouter()

const currentStep = ref(1)
const isSubmitting = ref(false)

const categoryStepRef = ref(null)
const informationStepRef = ref(null)
const imagesStepRef = ref(null)
const menuStepRef = ref(null)
const planStepRef = ref(null)

const formData = ref({
  category: '',
  subcategory: '',
  city: '',
  address: '',
  title: '',
  description: '',
  price: null,
  professionalTitle: '',
  yearsExperience: '',
  university: '',
  graduationYear: null,
  degree: '',
  certifications: '',
  specialties: [],
  services: '',
  successCases: '',
  schedule: '',
  languages: [],
  priceRange: '',
  deliveryAvailable: false,
  capacity: null,
  parking: false,
  features: [],
  menuItems: [],
  whatsapp: '',
  email: '',
  website: '',
  images: [],
  plan: 'free'
})

const stepsList = ref(['Categoría', 'Información', 'Imágenes', 'Plan', 'Confirmar'])

const getTotalSteps = () => {
  return formData.value.category === 'gastronomia' ? 6 : 5
}

const updateStepsList = () => {
  if (formData.value.category === 'gastronomia') {
    stepsList.value = ['Categoría', 'Información', 'Imágenes', 'Menú', 'Plan', 'Confirmar']
  } else {
    stepsList.value = ['Categoría', 'Información', 'Imágenes', 'Plan', 'Confirmar']
  }
}

const nextStep = async () => {
  const isValid = await validateCurrentStep()
  
  if (!isValid) {
    console.error('Validación fallida')
    return
  }
  
  if (currentStep.value === 1) {
    updateStepsList()
  }
  
  if (currentStep.value < getTotalSteps()) {
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
      stepRef = categoryStepRef.value
      break
    case 2:
      stepRef = informationStepRef.value
      break
    case 3:
      stepRef = imagesStepRef.value
      break
    case 4:
      if (formData.value.category === 'gastronomia') {
        stepRef = menuStepRef.value
      } else {
        stepRef = planStepRef.value
      }
      break
    case 5:
      if (formData.value.category === 'gastronomia') {
        stepRef = planStepRef.value
      } else {
        return true
      }
      break
    case 6:
      return true
    default:
      return true
  }
  
  if (stepRef && typeof stepRef.validate === 'function') {
    return stepRef.validate()
  }
  
  return true
}

const submitForm = async () => {
  isSubmitting.value = true
  
  try {
    await new Promise(resolve => setTimeout(resolve, 2000))
    console.log('Formulario enviado:', formData.value)
    
    if (formData.value.plan !== 'free') {
      alert(`Redirigiendo a pago - Plan: ${formData.value.plan}`)
    } else {
      alert('¡Anuncio publicado!')
    }
    router.push('/')
  } catch (error) {
    console.error('Error:', error)
    alert('Error al publicar')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  window.scrollTo({ top: 0 })
})
</script>

<style scoped>
.publish-section {
  min-height: calc(100vh - 200px);
  padding: 3rem 1rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.publish-header {
  text-align: center;
  margin-bottom: 3rem;
}

.publish-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin-bottom: 0.5rem;
}

.publish-subtitle {
  font-size: 1.125rem;
  color: #666;
  line-height: 1.5;
}

.form-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  margin-bottom: 2rem;
}

.summary-step {
  padding: 0;
}

.form-navigation {
  display: flex;
  gap: 1rem;
  padding-top: 2rem;
  margin-top: 2rem;
  border-top: 2px solid #E0E0E0;
}

.spacer {
  flex: 1;
}

.nav-btn {
  min-width: 140px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.nav-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.submit-btn {
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3);
}

.submit-btn:hover {
  box-shadow: 0 6px 20px rgba(253, 197, 0, 0.5);
}

@media (max-width: 768px) {
  .publish-section {
    padding: 2rem 1rem;
  }

  .publish-title {
    font-size: 2rem;
  }

  .publish-subtitle {
    font-size: 1rem;
  }

  .form-card {
    padding: 1.5rem;
  }

  .form-navigation {
    flex-direction: column;
  }

  .nav-btn {
    width: 100%;
    min-width: auto;
  }

  .spacer {
    display: none;
  }
}

@media (max-width: 480px) {
  .publish-section {
    padding: 1.5rem 0.75rem;
  }

  .publish-header {
    margin-bottom: 2rem;
  }

  .publish-title {
    font-size: 1.75rem;
  }

  .form-card {
    padding: 1rem;
    border-radius: 12px;
  }
}
</style>