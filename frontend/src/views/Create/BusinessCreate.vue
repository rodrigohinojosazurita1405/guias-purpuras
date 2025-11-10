<!-- frontend/src/views/BusinessCreate.vue -->
<!-- ✨ INTEGRADO CON BRANCHMANAGER + ANCHO CORRECTO -->
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
                file-types="image/*"
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
                file-types="image/*"
              />
              <span class="field-hint">
                Tamaño recomendado: 200x200px
              </span>
            </div>
          </div>
        </div>

        <!-- ✨ Step 4: Ubicación GPS + SUCURSALES (MODIFICADO) -->
        <div v-show="currentStep === 4" class="form-step">
          <div class="step-header">
            <va-icon name="location_on" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Ubicación Principal</h2>
              <p class="step-description">Define la ubicación GPS de tu negocio</p>
            </div>
          </div>

          <!-- Ubicación GPS Principal -->
          <GPSLocation
            v-model:coordinates="formData.coordinates"
            v-model:address="formData.gpsAddress"
            :error="errors.coordinates"
          />

          <!-- ✨ SUCURSALES ADICIONALES (NUEVO) -->
          <div style="margin-top: 3rem;">
            <BranchManager
              ref="branchManagerRef"
              v-model="formData.branches"
              :user-plan="userPlan"
              :cities="cities"
              @upgrade-plan="handleUpgradePlan"
            />
          </div>
        </div>

        <!-- Step 5: SEO -->
        <div v-show="currentStep === 5" class="form-step">
          <div class="step-header">
            <va-icon name="search" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">SEO y Optimización</h2>
              <p class="step-description">Mejora la visibilidad de tu negocio</p>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="link" size="small" />
                URL personalizada
              </label>
              <VaInput
                v-model="formData.slug"
                placeholder="mi-negocio-la-paz"
              />
              <span class="field-hint">
                Tu negocio aparecerá en: guiaspurpuras.com/negocios/{{ formData.slug || 'tu-url' }}
              </span>
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="key" size="small" />
                Palabra clave principal
              </label>
              <VaInput
                v-model="formData.mainKeyword"
                placeholder="Ej: fábrica plásticos La Paz"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="tag" size="small" />
                Etiquetas adicionales
              </label>
              <VaInput
                v-model="formData.tagsInput"
                placeholder="manufactura, plásticos, Bolivia"
                @input="updateTags"
              />
              <span class="field-hint">
                Separa las etiquetas con comas
              </span>
            </div>

            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="description" size="small" />
                Descripción para buscadores
              </label>
              <VaTextarea
                v-model="formData.metaDescription"
                placeholder="Descripción breve que aparecerá en Google..."
                :max-length="160"
                :min-rows="3"
                counter
              />
            </div>
          </div>
        </div>

        <!-- Step 6: Plan -->
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

        <!-- Step 7: Confirmar -->
        <div v-show="currentStep === 7" class="form-step">
          <div class="step-header">
            <va-icon name="check_circle" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Confirmar Publicación</h2>
              <p class="step-description">Revisa todos los datos antes de publicar</p>
            </div>
          </div>

          <div class="summary-card">
            <h3 style="margin-bottom: 1.5rem;">Resumen de tu anuncio:</h3>
            
            <div class="summary-item">
              <span class="summary-label">Nombre:</span>
              <span class="summary-value">{{ formData.name || 'Sin especificar' }}</span>
            </div>
            
            <div class="summary-item">
              <span class="summary-label">Categoría:</span>
              <span class="summary-value">{{ formData.category || 'Sin especificar' }}</span>
            </div>
            
            <div class="summary-item">
              <span class="summary-label">Ciudad:</span>
              <span class="summary-value">{{ formData.city || 'Sin especificar' }}</span>
            </div>
            
            <div class="summary-item">
              <span class="summary-label">Teléfono:</span>
              <span class="summary-value">{{ formData.phone || 'Sin especificar' }}</span>
            </div>

            <div class="summary-item">
              <span class="summary-label">Email:</span>
              <span class="summary-value">{{ formData.email || 'Sin especificar' }}</span>
            </div>

            <!-- ✨ SUCURSALES EN RESUMEN (NUEVO) -->
            <div v-if="formData.branches && formData.branches.length > 0" class="summary-item">
              <span class="summary-label">Sucursales adicionales:</span>
              <span class="summary-value">{{ formData.branches.length }}</span>
            </div>

            <div class="summary-item">
              <span class="summary-label">Plan seleccionado:</span>
              <span class="summary-value">{{ formData.plan || 'Sin especificar' }}</span>
            </div>
          </div>

          <div style="padding: 1.5rem; background: #E8F5E8; border-radius: 12px; margin-top: 2rem;">
            <h4 style="color: #2E7D2E; margin-bottom: 1rem;">
              <va-icon name="info" color="#2E7D2E" />
              ¿Qué sucede después?
            </h4>
            <ul style="margin: 0; color: #2E7D2E;">
              <li>Tu anuncio será publicado inmediatamente</li>
              <li>Aparecerá en los resultados de búsqueda</li>
              <li>Los usuarios podrán contactarte directamente</li>
              <li>Puedes editarlo en cualquier momento</li>
            </ul>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="form-actions">
          <VaButton
            v-if="currentStep > 1"
            preset="secondary"
            @click="previousStep"
            size="large"
          >
            <va-icon name="arrow_back" />
            Anterior
          </VaButton>

          <div style="flex: 1;"></div>

          <VaButton
            v-if="currentStep < 7"
            color="success"
            @click="nextStep"
            size="large"
            :disabled="!isStepValid"
          >
            Continuar
            <va-icon name="arrow_forward" />
          </VaButton>

          <VaButton
            v-if="currentStep === 7"
            color="success"
            @click="submitForm"
            size="large"
            :loading="isSubmitting"
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'

// ✅ IMPORTS CORREGIDOS
import MainLayout from '@/components/Layout/MainLayout.vue'
import GPSLocation from '@/components/Location/GPSLocation.vue'
import BranchManager from '@/components/Common/BranchManager.vue'

// ========== COMPOSABLES ==========
const router = useRouter()
const { init: notify } = useToast()

// ========== REACTIVE STATE ==========
const currentStep = ref(1)
const isSubmitting = ref(false)
const branchManagerRef = ref(null)

// ✨ PLAN DEL USUARIO (TEMPORAL)
const userPlan = computed(() => 'plata')

// ========== FORM DATA ==========
const formData = ref({
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
  coordinates: '',
  gpsAddress: '',
  branches: [], // ✨ NUEVO
  slug: '',
  mainKeyword: '',
  tags: [],
  tagsInput: '',
  metaDescription: '',
  locationKeywords: '',
  seoCategories: [],
  plan: 'basico'
})

const errors = ref({})

// ========== CONFIGURATION DATA ==========
const steps = [
  { number: 1, label: 'Información' },
  { number: 2, label: 'Contacto' },
  { number: 3, label: 'Imágenes' },
  { number: 4, label: 'Ubicación' },
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
  'Automotriz',
  'Otro'
]

const cities = [
  'La Paz',
  'Santa Cruz',
  'Cochabamba',
  'Sucre',
  'Oruro',
  'Potosí',
  'Tarija',
  'Beni',
  'Pando'
]

const plans = [
  {
    id: 'basico',
    name: 'Plan Básico',
    price: 'GRATIS',
    badge: 'Básico',
    features: [
      'Publicación básica',
      '1 imagen',
      'Información de contacto',
      'Ubicación en mapa'
    ]
  },
  {
    id: 'destacado',
    name: 'Plan Destacado',
    price: '50 Bs/mes',
    badge: 'Popular',
    features: [
      'Publicación destacada',
      '5 imágenes',
      'Logo y banner',
      'Posición preferencial',
      'Estadísticas básicas'
    ]
  },
  {
    id: 'top',
    name: 'Plan Top',
    price: '100 Bs/mes',
    badge: 'Premium',
    features: [
      'Máxima visibilidad',
      '10 imágenes',
      'Video promocional',
      'SEO optimizado',
      'Estadísticas avanzadas',
      'Soporte prioritario'
    ]
  }
]

// ========== COMPUTED ==========
const isStepValid = computed(() => {
  switch (currentStep.value) {
    case 1: // Información
      return formData.value.name && 
             formData.value.category && 
             formData.value.description &&
             formData.value.city &&
             formData.value.address
    case 2: // Contacto
      return formData.value.phone && 
             formData.value.email && 
             formData.value.nit
    case 3: // Imágenes
      return true // Opcional
    case 4: // Ubicación + Sucursales
      if (!formData.value.coordinates) return false
      if (branchManagerRef.value && !branchManagerRef.value.validate()) return false
      return true
    case 5: // SEO
      return true // Opcional
    case 6: // Plan
      return formData.value.plan
    default:
      return true
  }
})

// ========== METHODS ==========
const nextStep = () => {
  if (!isStepValid.value) {
    notify({
      message: 'Por favor completa todos los campos requeridos',
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

const updateTags = () => {
  formData.value.tags = formData.value.tagsInput
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag.length > 0)
}

const submitForm = async () => {
  if (!isStepValid.value) {
    notify({
      message: 'Por favor completa todos los campos',
      color: 'danger'
    })
    return
  }

  isSubmitting.value = true

  try {
    // Simular envío
    await new Promise(resolve => setTimeout(resolve, 2000))

    notify({
      message: '¡Negocio publicado exitosamente!',
      color: 'success'
    })

    // Redireccionar
    router.push('/negocios')
  } catch (error) {
    notify({
      message: 'Error al publicar el negocio',
      color: 'danger'
    })
  } finally {
    isSubmitting.value = false
  }
}

const handleUpgradePlan = () => {
  router.push('/planes')
}
</script>

<style scoped>
/* ========== Container - COPIADO DE JOBCREATE ========== */
.business-create {
  max-width: 1200px; /* ✅ ANCHO LIMITADO */
  margin: 0 auto;    /* ✅ CENTRADO */
  padding: 2rem;
  min-height: 100vh;
}

/* ========== Header ========== */
.create-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 3px solid #5C0099;
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

/* ========== Stepper ========== */
.stepper-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
  padding: 0 1rem;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
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
  font-size: 1.2rem;
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
  background: #4CAF50;
  color: white;
}

.step-line {
  position: absolute;
  top: 25px;
  left: 50%;
  width: 100%;
  height: 3px;
  background: #E0E0E0;
  z-index: 1;
}

.step-item.completed .step-line {
  background: #4CAF50;
}

.step-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #999;
  text-align: center;
}

.step-item.active .step-label {
  color: #5C0099;
}

.step-item.completed .step-label {
  color: #4CAF50;
}

/* ========== Form Container - COPIADO DE JOBCREATE ========== */
.form-container {
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

/* ========== Step Header ========== */
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

/* ========== Form Grid ========== */
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

/* ========== Plans Grid ========== */
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

/* ========== Summary ========== */
.summary-card {
  background: #F8F4FF;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(92, 0, 153, 0.1);
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

/* ========== Actions ========== */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #E0E0E0;
}

/* ========== Responsive ========== */
@media (max-width: 968px) {
  .business-create {
    padding: 1rem;
  }

  .form-container {
    padding: 2rem 1.5rem;
  }

  .stepper-container {
    overflow-x: auto;
    padding-bottom: 1rem;
  }

  .step-label {
    font-size: 0.75rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .plans-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column-reverse;
  }
}
</style>