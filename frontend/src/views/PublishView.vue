<template>
  <MainLayout>
    <section class="publish-section">
      <div class="container">
        <div class="publish-header">
          <div class="header-icon">
            <va-icon name="add_circle" size="3rem" color="purple" />
          </div>
          <h1 class="publish-title">Publica tu Anuncio</h1>
          <p class="publish-subtitle">
            Completa el formulario y llega a miles de personas en Bolivia
          </p>
        </div>

        <!-- Progress Bar Moderno -->
        <div class="progress-container">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: ((currentStep / getTotalSteps()) * 100) + '%' }"
            ></div>
          </div>
          <div class="progress-steps">
            <div 
              v-for="(step, index) in stepsList" 
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

        <div class="form-card" :key="currentStep">
          
          <!-- Paso 1: Categoría -->
          <CategoryStep
            v-if="currentStep === 1"
            ref="categoryStepRef"
            v-model="formData"
          />

          <!-- Paso 2: Información -->
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
          
          <InformationStepTrabajos
            v-if="currentStep === 2 && formData.category === 'trabajos'"
            ref="informationStepRef"
            v-model="formData"
          />
          
          <InformationStep
            v-if="currentStep === 2 && formData.category !== 'profesionales' && formData.category !== 'gastronomia' && formData.category !== 'trabajos'"
            ref="informationStepRef"
            v-model="formData"
          />

          <!-- Paso 3: GPS (profesionales y gastronomía) -->
          <GPSStep
            v-if="currentStep === 3 && (formData.category === 'profesionales' || formData.category === 'gastronomia')"
            ref="gpsStepRef"
            v-model:coordinates="formData.coordinates"
            v-model:address="formData.gpsAddress"
          />

          <!-- Paso 4: SEO (profesionales y gastronomía) -->
          <SEOStep
            v-if="currentStep === 4 && formData.category === 'profesionales'"
            ref="seoStepRef"
            v-model="formData.seoData"
            entity-type="profesional"
            base-url="guiaspurpuras.com/profesionales"
          />

          <SEOStep
            v-if="currentStep === 4 && formData.category === 'gastronomia'"
            ref="seoStepRef"
            v-model="formData.seoData"
            entity-type="restaurante"
            base-url="guiaspurpuras.com/gastronomia"
          />

          <!-- Imágenes -->
          <ImagesStep
            v-if="(currentStep === 3 && formData.category !== 'profesionales' && formData.category !== 'gastronomia') || 
                  (currentStep === 5 && (formData.category === 'profesionales' || formData.category === 'gastronomia'))"
            ref="imagesStepRef"
            v-model="formData.images"
            :plan="formData.plan"
          />

          <!-- Menú (solo gastronomía) -->
          <MenuStep
            v-if="currentStep === 6 && formData.category === 'gastronomia'"
            ref="menuStepRef"
            v-model="formData.menuItems"
          />

          <!-- Plan -->
          <PlanStep
            v-if="(currentStep === 4 && formData.category !== 'gastronomia' && formData.category !== 'profesionales') || 
                  (currentStep === 7 && formData.category === 'gastronomia') ||
                  (currentStep === 6 && formData.category === 'profesionales')"
            ref="planStepRef"
            v-model="formData.plan"
          />

          <!-- Confirmar -->
          <div 
            v-if="(currentStep === 5 && formData.category !== 'gastronomia' && formData.category !== 'profesionales') || 
                  (currentStep === 8 && formData.category === 'gastronomia') ||
                  (currentStep === 7 && formData.category === 'profesionales')"
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
import CategoryStep from '@/components/Publish/CategoryStep.vue'
import InformationStep from '@/components/Publish/InformationStep.vue'
import InformationStepProfessional from '@/components/Publish/InformationStepProfessional.vue'
import InformationStepGastronomia from '@/components/Publish/InformationStepGastronomia.vue'
import InformationStepTrabajos from '@/components/Publish/InformationStepTrabajos.vue'
import ImagesStep from '@/components/Publish/ImagesStep.vue'
import MenuStep from '@/components/Publish/MenuStep.vue'
import PlanStep from '@/components/Publish/PlanStep.vue'
import SummaryCard from '@/components/Publish/SummaryCard.vue'
import GPSStep from '@/components/Publish/GPSStep.vue'
import SEOStep from '@/components/Publish/SEOStep.vue'

const router = useRouter()

const currentStep = ref(1)
const isSubmitting = ref(false)

const categoryStepRef = ref(null)
const informationStepRef = ref(null)
const imagesStepRef = ref(null)
const menuStepRef = ref(null)
const planStepRef = ref(null)
const gpsStepRef = ref(null)
const seoStepRef = ref(null)

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

const stepsList = ref(['Categoría', 'Información', 'Imágenes', 'Plan', 'Confirmar'])

const getTotalSteps = () => {
  // Profesionales: 7 pasos
  if (formData.value.category === 'profesionales') {
    return 7
  }
  // ✨ GASTRONOMÍA: 8 PASOS (Info, GPS, SEO, Imágenes, Menú, Plan, Confirmar)
  if (formData.value.category === 'gastronomia') {
    return 8
  }
  // Otros: 5 pasos
  return 5
}

const updateStepsList = () => {
  if (formData.value.category === 'profesionales') {
    stepsList.value = ['Categoría', 'Información', 'GPS', 'SEO', 'Imágenes', 'Plan', 'Confirmar']
  } else if (formData.value.category === 'gastronomia') {
    // ✨ GASTRONOMÍA CON GPS Y SEO
    stepsList.value = ['Categoría', 'Información', 'GPS', 'SEO', 'Imágenes', 'Menú', 'Plan', 'Confirmar']
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
  
  // 🎯 REDIRIGIR A FORMULARIOS ESPECÍFICOS DESPUÉS DEL PASO 1
  if (currentStep.value === 1) {
    updateStepsList()
    
    // Si selecciona "Negocios", redirigir al formulario específico
    if (formData.value.category === 'negocios') {
      router.push('/guias/negocios/crear')
      return
    }
    
    // Si selecciona "Trabajos", redirigir al formulario específico
    if (formData.value.category === 'trabajos') {
      router.push('/guias/trabajos/crear')
      return
    }
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
      // Paso 3: GPS (profesionales y gastronomía) o Imágenes (otros)
      if (formData.value.category === 'profesionales' || formData.value.category === 'gastronomia') {
        stepRef = gpsStepRef.value // GPS es opcional, siempre válido
      } else {
        stepRef = imagesStepRef.value
      }
      break
    
    case 4:
      // Paso 4: SEO (profesionales y gastronomía) o Plan (otros)
      if (formData.value.category === 'profesionales' || formData.value.category === 'gastronomia') {
        stepRef = seoStepRef.value // SEO es opcional, siempre válido
      } else {
        stepRef = planStepRef.value
      }
      break
    
    case 5:
      // Paso 5: Imágenes (profesionales y gastronomía) o Confirmar (otros)
      if (formData.value.category === 'profesionales' || formData.value.category === 'gastronomia') {
        stepRef = imagesStepRef.value
      } else {
        return true // Confirmar, no valida
      }
      break
    
    case 6:
      // Paso 6: Menú (gastronomía) o Plan (profesionales)
      if (formData.value.category === 'gastronomia') {
        stepRef = menuStepRef.value
      } else if (formData.value.category === 'profesionales') {
        stepRef = planStepRef.value
      }
      break
    
    case 7:
      // Paso 7: Plan (gastronomía) o Confirmar (profesionales)
      if (formData.value.category === 'gastronomia') {
        stepRef = planStepRef.value
      } else {
        return true // Confirmar, no valida
      }
      break
    
    case 8:
      // Paso 8: Confirmar (gastronomía)
      return true // No valida
    
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

.header-icon {
  margin-bottom: 1rem;
  animation: fadeInDown 0.6s ease;
}

.publish-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #5C0099, #9333EA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  animation: fadeInDown 0.6s ease 0.1s backwards;
}

.publish-subtitle {
  font-size: 1.125rem;
  color: #6B7280;
  line-height: 1.5;
  animation: fadeInDown 0.6s ease 0.2s backwards;
}

/* ===================================
   PROGRESS BAR MODERNO
   =================================== */
.progress-container {
  margin-bottom: 3rem;
  animation: fadeIn 0.6s ease 0.3s backwards;
}

.progress-bar {
  height: 8px;
  background: #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 2rem;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #5C0099, #9333EA, #DB2777);
  border-radius: 10px;
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  position: relative;
}

.step-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: white;
  border: 3px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.125rem;
  color: #9CA3AF;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  z-index: 2;
}

.progress-step.active .step-circle {
  background: linear-gradient(135deg, #5C0099, #9333EA);
  border-color: #5C0099;
  color: white;
  transform: scale(1.15);
  box-shadow: 0 4px 16px rgba(92, 0, 153, 0.4);
}

.progress-step.completed .step-circle {
  background: linear-gradient(135deg, #FDC500, #FFA500);
  border-color: #FDC500;
  color: #5C0099;
  box-shadow: 0 4px 16px rgba(253, 197, 0, 0.4);
}

.step-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #9CA3AF;
  transition: color 0.3s ease;
  text-align: center;
}

.progress-step.active .step-name {
  color: #5C0099;
  font-weight: 700;
}

.progress-step.completed .step-name {
  color: #6B7280;
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

  .step-name {
    display: none;
  }

  .progress-steps {
    padding: 0 1rem;
  }

  .step-circle {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}

/* ===================================
   ANIMACIONES
   =================================== */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>