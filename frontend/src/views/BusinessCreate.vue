<!-- frontend/src/views/BusinessCreate.vue -->
<!-- FORMULARIO ESPECÍFICO PARA NEGOCIOS - ESTILO CONSISTENTE -->
<template>
  <MainLayout>
    <div class="business-create">
      
      <!-- Header -->
      <div class="create-header">
        <h1 class="header-title">Publica tu Negocio</h1>
        <p class="header-subtitle">
          Completa el formulario y llega a miles de personas en Bolivia
        </p>
      </div>

      <!-- Stepper -->
      <div class="stepper-container">
        <div 
          v-for="step in steps" 
          :key="step.number"
          class="step-item"
          :class="{ 
            active: currentStep === step.number,
            completed: currentStep > step.number 
          }"
        >
          <div class="step-circle">
            <va-icon v-if="currentStep > step.number" name="check" size="small" />
            <span v-else>{{ step.number }}</span>
          </div>
          <div class="step-line" v-if="step.number < steps.length"></div>
          <span class="step-label">{{ step.label }}</span>
        </div>
      </div>

      <!-- Form Container -->
      <div class="form-container">
        
        <!-- Step 1: Información Básica -->
        <div v-show="currentStep === 1" class="form-step">
          <div class="step-header">
            <va-icon name="business" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Información del Negocio</h2>
              <p class="step-description">Datos principales de tu empresa</p>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-field">
              <label class="field-label">
                <va-icon name="business" size="small" />
                Nombre del Negocio *
              </label>
              <VaInput
                v-model="formData.name"
                placeholder="Ej: Fábrica de Plásticos Belén"
                :error="!!errors.name"
                :error-messages="errors.name"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="category" size="small" />
                Categoría *
              </label>
              <VaSelect
                v-model="formData.category"
                :options="categories"
                placeholder="Selecciona una categoría"
                :error="!!errors.category"
                :error-messages="errors.category"
              />
            </div>

            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="description" size="small" />
                Descripción *
              </label>
              <VaTextarea
                v-model="formData.description"
                placeholder="Describe tu negocio, productos y servicios..."
                :min-rows="4"
                :max-length="500"
                counter
                :error="!!errors.description"
                :error-messages="errors.description"
              />
              <span class="field-hint">
                Una buena descripción ayuda a atraer más clientes
              </span>
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="place" size="small" />
                Ciudad *
              </label>
              <VaSelect
                v-model="formData.city"
                :options="cities"
                placeholder="Selecciona una ciudad"
                :error="!!errors.city"
                :error-messages="errors.city"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="home" size="small" />
                Dirección *
              </label>
              <VaInput
                v-model="formData.address"
                placeholder="Ej: Av. América #123, Zona Sur"
                :error="!!errors.address"
                :error-messages="errors.address"
              />
            </div>
          </div>
        </div>

        <!-- Step 2: Contacto -->
        <div v-show="currentStep === 2" class="form-step">
          <div class="step-header">
            <va-icon name="contact_phone" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Información de Contacto</h2>
              <p class="step-description">¿Cómo pueden contactarte?</p>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-field">
              <label class="field-label">
                <va-icon name="phone" size="small" />
                Teléfono *
              </label>
              <VaInput
                v-model="formData.phone"
                placeholder="Ej: 4-4567890"
                :error="!!errors.phone"
                :error-messages="errors.phone"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="email" size="small" />
                Email *
              </label>
              <VaInput
                v-model="formData.email"
                type="email"
                placeholder="Ej: contacto@negocio.com"
                :error="!!errors.email"
                :error-messages="errors.error"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="language" size="small" />
                Sitio Web (Opcional)
              </label>
              <VaInput
                v-model="formData.website"
                placeholder="Ej: www.minegocio.com"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="badge" size="small" />
                NIT / RUC *
              </label>
              <VaInput
                v-model="formData.nit"
                placeholder="Ej: 123456789"
                :error="!!errors.nit"
                :error-messages="errors.nit"
              />
            </div>
          </div>
        </div>

        <!-- Step 3: Imágenes -->
        <div v-show="currentStep === 3" class="form-step">
          <div class="step-header">
            <va-icon name="image" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Imágenes</h2>
              <p class="step-description">Agrega fotos de tu negocio</p>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="panorama" size="small" />
                Banner Principal (Opcional)
              </label>
              <VaFileUpload
                v-model="formData.bannerFile"
                type="single"
                file-types=".jpg,.jpeg,.png"
              />
              <span class="field-hint">
                Tamaño recomendado: 1200x400px
              </span>
            </div>

            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="image" size="small" />
                Logo (Opcional)
              </label>
              <VaFileUpload
                v-model="formData.logoFile"
                type="single"
                file-types=".jpg,.jpeg,.png"
              />
              <span class="field-hint">
                Tamaño recomendado: 200x200px
              </span>
            </div>
          </div>
        </div>

        <!-- Step 4: Plan -->
        <!-- Step 4: Ubicación GPS -->
        <div v-show="currentStep === 4" class="form-step">
          <GPSLocation
            v-model:coordinates="formData.coordinates"
            v-model:address="formData.gpsAddress"
            :error="errors.coordinates"
          />
        </div>

        <!-- Step 5: SEO -->
        <div v-show="currentStep === 5" class="form-step">
          <SEOFields
            :model-value="{
              slug: formData.slug,
              mainKeyword: formData.mainKeyword,
              tags: formData.tags,
              metaDescription: formData.metaDescription,
              locationKeywords: formData.locationKeywords,
              categories: formData.seoCategories
            }"
            @update:model-value="(val) => {
              formData.slug = val.slug
              formData.mainKeyword = val.mainKeyword
              formData.tags = val.tags
              formData.metaDescription = val.metaDescription
              formData.locationKeywords = val.locationKeywords
              formData.seoCategories = val.categories
            }"
            entity-type="negocio"
            base-url="guiaspurpuras.com/negocios"
            :available-categories="seoCategories"
          />
        </div>
        <div v-show="currentStep === 6" class="form-step">
          <div class="step-header">
            <va-icon name="verified" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Selecciona tu Plan</h2>
              <p class="step-description">Elige el plan que mejor se adapte a tu negocio</p>
            </div>
          </div>

          <div class="plans-grid">
            <div 
              v-for="plan in plans" 
              :key="plan.id"
              class="plan-card"
              :class="{ selected: formData.plan === plan.id }"
              @click="formData.plan = plan.id"
            >
              <div class="plan-badge" :class="`badge-${plan.id}`">
                {{ plan.badge }}
              </div>
              <h3 class="plan-name">{{ plan.name }}</h3>
              <div class="plan-price">{{ plan.price }}</div>
              <ul class="plan-features">
                <li v-for="(feature, index) in plan.features" :key="index">
                  <va-icon name="check_circle" size="small" />
                  {{ feature }}
                </li>
              </ul>
              <VaButton
                :color="formData.plan === plan.id ? 'success' : 'primary'"
                :preset="formData.plan === plan.id ? undefined : 'secondary'"
                block
              >
                {{ formData.plan === plan.id ? 'Seleccionado' : 'Seleccionar' }}
              </VaButton>
            </div>
          </div>
        </div>

        <!-- Step 5: Confirmar -->
        <div v-show="currentStep === 7" class="form-step">
          <div class="step-header">
            <va-icon name="check_circle" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Confirmar Publicación</h2>
              <p class="step-description">Revisa la información antes de publicar</p>
            </div>
          </div>

          <div class="summary-card">
            <div class="summary-item">
              <span class="summary-label">Nombre:</span>
              <span class="summary-value">{{ formData.name || '-' }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Categoría:</span>
              <span class="summary-value">{{ formData.category || '-' }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Ciudad:</span>
              <span class="summary-value">{{ formData.city || '-' }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Plan:</span>
              <span class="summary-value">{{ getPlanName(formData.plan) }}</span>
            </div>
          </div>

          <VaAlert color="info" border="left">
            <template #title>Importante</template>
            Tu anuncio será revisado por nuestro equipo antes de ser publicado. 
            Recibirás una notificación cuando esté activo.
          </VaAlert>
        </div>

        <!-- Navigation Buttons -->
        <div class="form-actions">
          <VaButton
            v-if="currentStep > 1"
            preset="secondary"
            @click="previousStep"
          >
            <va-icon name="arrow_back" />
            Anterior
          </VaButton>
          
          <VaButton
            v-if="currentStep < 7"
            color="purple"
            @click="nextStep"
          >
            Siguiente
            <va-icon name="arrow_forward" />
          </VaButton>

          <VaButton
            v-if="currentStep === 7"
            color="success"
            :loading="submitting"
            @click="submitForm"
          >
            <va-icon name="check" />
            Publicar Negocio
          </VaButton>
        </div>

      </div>

    </div>
  </MainLayout>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import MainLayout from '@/components/Layout/MainLayout.vue'
import SEOFields from '@/components/SEO/SEOFields.vue'
import GPSLocation from '@/components/Location/GPSLocation.vue'

const router = useRouter()
const { init: notify } = useToast()

const currentStep = ref(1)
const submitting = ref(false)

const steps = [
  { number: 1, label: 'Información' },
  { number: 2, label: 'Contacto' },
  { number: 3, label: 'Imágenes' },
  { number: 4, label: 'Ubicación GPS' },
  { number: 5, label: 'SEO' },
  { number: 6, label: 'Plan' },
  { number: 7, label: 'Confirmar' }
]

const categories = [
  'Manufactura',
  'Servicios',
  'Comercio',
  'Tecnología',
  'Alimentación',
  'Construcción',
  'Textil',
  'Automotriz'
]

const cities = [
  'La Paz',
  'Santa Cruz',
  'Cochabamba',
  'Oruro',
  'Potosí',
  'Tarija',
  'Sucre',
  'Beni',
  'Pando'
]

const plans = [
  {
    id: 'basico',
    name: 'Básico',
    badge: 'GRATIS',
    price: 'Bs. 0',
    features: [
      'Publicación básica',
      'Visible 30 días',
      'Información de contacto'
    ]
  },
  {
    id: 'destacado',
    name: 'Destacado',
    badge: 'POPULAR',
    price: 'Bs. 150',
    features: [
      'Badge "Destacado"',
      'Visible 60 días',
      'Aparece en búsquedas destacadas',
      'Soporte prioritario'
    ]
  },
  {
    id: 'top',
    name: 'TOP',
    badge: 'PREMIUM',
    price: 'Bs. 300',
    features: [
      'Badge "TOP"',
      'Visible 90 días',
      'Posición privilegiada',
      'Verificación incluida',
      'Estadísticas detalladas'
    ]
  }
]

const formData = reactive({
  name: '',
  category: '',
  description: '',
  city: '',
  address: '',
  phone: '',
  email: '',
  website: '',
  nit: '',
  bannerFile: [],
  logoFile: [],
  plan: 'basico',
  // GPS Location
  coordinates: '',
  gpsAddress: '',
  // SEO Fields
  slug: '',
  mainKeyword: '',
  tags: [],
  metaDescription: '',
  locationKeywords: '',
  seoCategories: []
})

const errors = reactive({})

const validateStep = () => {
  Object.keys(errors).forEach(key => delete errors[key])
  
  if (currentStep.value === 1) {
    if (!formData.name) errors.name = 'El nombre es requerido'
    if (!formData.category) errors.category = 'La categoría es requerida'
    if (!formData.description) errors.description = 'La descripción es requerida'
    if (!formData.city) errors.city = 'La ciudad es requerida'
    if (!formData.address) errors.address = 'La dirección es requerida'
  }
  
  if (currentStep.value === 2) {
    if (!formData.phone) errors.phone = 'El teléfono es requerido'
    if (!formData.email) errors.email = 'El email es requerido'
    if (!formData.nit) errors.nit = 'El NIT es requerido'
  }
  
  // Step 3: Imágenes - opcional
  
  // Step 4: GPS Location
  if (currentStep.value === 4) {
    if (!formData.coordinates) errors.coordinates = 'Las coordenadas GPS son requeridas'
  }
  
  // Step 5: SEO
  if (currentStep.value === 5) {
    if (!formData.slug) errors.slug = 'El slug es requerido'
    if (!formData.mainKeyword) errors.mainKeyword = 'La palabra clave principal es requerida'
    if (!formData.metaDescription) errors.metaDescription = 'La meta descripción es requerida'
  }
  
  return Object.keys(errors).length === 0
}

const nextStep = () => {
  if (validateStep()) {
    if (currentStep.value < 7) {
      currentStep.value++
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// Computed property para categorías SEO
const seoCategories = ref(categories.map((cat, idx) => ({
  id: idx + 1,
  name: cat,
  selected: false
})))

const getPlanName = (planId) => {
  const plan = plans.find(p => p.id === planId)
  return plan ? plan.name : '-'
}

const submitForm = async () => {
  submitting.value = true
  
  // Simular envío
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  notify({
    message: '🎉 ¡Negocio publicado exitosamente!',
    color: 'success',
    duration: 3000
  })
  
  submitting.value = false
  router.push('/guias/negocios')
}
</script>

<style scoped>
/* Container */
.business-create {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}

/* Header */
.create-header {
  text-align: center;
  margin-bottom: 3rem;
}

.header-title {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
  font-weight: 700;
  color: #5C0099;
}

.header-subtitle {
  margin: 0;
  font-size: 1.1rem;
  color: #666;
}

/* Stepper */
.stepper-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
  position: relative;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  position: relative;
}

.step-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #E0E0E0;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  transition: all 0.3s ease;
  z-index: 2;
}

.step-item.active .step-circle {
  background: #5C0099;
  color: white;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

.step-item.completed .step-circle {
  background: #FFD700;
  color: #000;
}

.step-line {
  position: absolute;
  top: 25px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: #E0E0E0;
  z-index: 1;
}

.step-item.completed .step-line {
  background: #FFD700;
}

.step-label {
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
  text-align: center;
}

.step-item.active .step-label {
  color: #5C0099;
  font-weight: 700;
}

/* Form Container */
.form-container {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.form-step {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Step Header */
.step-header {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid rgba(92, 0, 153, 0.1);
}

.step-title {
  margin: 0 0 0.25rem 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #5C0099;
}

.step-description {
  margin: 0;
  color: #666;
  font-size: 1rem;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-field.full-width {
  grid-column: 1 / -1;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.field-hint {
  font-size: 0.85rem;
  color: #999;
  font-style: italic;
}

/* Plans Grid */
.plans-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.plan-card {
  padding: 2rem;
  border: 2px solid #E0E0E0;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.plan-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.plan-card.selected {
  border-color: #5C0099;
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.2);
}

.plan-badge {
  position: absolute;
  top: -12px;
  right: 1rem;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.75rem;
}

.badge-basico {
  background: #4CAF50;
  color: white;
}

.badge-destacado {
  background: #5C0099;
  color: white;
}

.badge-top {
  background: #FFD700;
  color: #000;
}

.plan-name {
  margin: 1rem 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
}

.plan-price {
  margin: 0 0 1.5rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #5C0099;
}

.plan-features {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem 0;
}

.plan-features li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  color: #666;
}

/* Summary */
.summary-card {
  background: #F8F8F8;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #E0E0E0;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-label {
  font-weight: 600;
  color: #666;
}

.summary-value {
  color: #333;
  font-weight: 600;
}

/* Actions */
.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid rgba(0, 0, 0, 0.05);
}

/* Responsive */
@media (max-width: 1024px) {
  .plans-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .business-create {
    padding: 1rem;
  }

  .header-title {
    font-size: 2rem;
  }

  .form-container {
    padding: 1.5rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .stepper-container {
    overflow-x: auto;
  }

  .step-line {
    display: none;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>