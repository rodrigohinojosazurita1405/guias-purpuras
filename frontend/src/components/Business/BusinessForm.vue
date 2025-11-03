<!-- frontend/src/components/Business/BusinessForm.vue -->
<template>
  <div class="business-form">
    
    <!-- Header -->
    <div class="form-header">
      <h2 class="form-title">
        <va-icon :name="isEditing ? 'edit' : 'add_business'" size="2rem" />
        {{ isEditing ? 'Editar Negocio' : 'Crear Nuevo Negocio' }}
      </h2>
      <p class="form-subtitle">
        Completa la información de tu empresa para aparecer en Guías Púrpuras
      </p>
    </div>

    <!-- Progress Steps -->
    <div class="form-steps">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="step-item"
        :class="{
          active: currentStep === index,
          completed: currentStep > index
        }"
      >
        <div class="step-number">
          <va-icon v-if="currentStep > index" name="check" size="small" />
          <span v-else>{{ index + 1 }}</span>
        </div>
        <span class="step-label">{{ step }}</span>
      </div>
    </div>

    <!-- Form Content -->
    <div class="form-content">
      
      <!-- Step 1: Imágenes -->
      <div v-show="currentStep === 0" class="form-step">
        <ImageUploadBusiness
          v-model:logo="businessData.logo"
          v-model:banner="businessData.banner"
        />
      </div>

      <!-- Step 2: Datos Básicos -->
      <div v-show="currentStep === 1" class="form-step">
        <div class="step-section">
          <h3 class="section-title">
            <va-icon name="business" />
            Datos de la Empresa
          </h3>

          <div class="form-grid">
            <VaInput
              v-model="businessData.name"
              label="Nombre de la Empresa *"
              placeholder="Ej: Fábrica de Plásticos Belén"
              :rules="[v => !!v || 'Campo requerido']"
            />

            <VaInput
              v-model="businessData.nit"
              label="NIT / RUC *"
              placeholder="123456789"
              :rules="[v => !!v || 'Campo requerido']"
            />

            <VaInput
              v-model="businessData.phone"
              label="Teléfono *"
              placeholder="4-4567890"
              :rules="[v => !!v || 'Campo requerido']"
              type="tel"
            >
              <template #appendInner>
                <VaIcon name="phone" />
              </template>
            </VaInput>

            <VaInput
              v-model="businessData.email"
              label="Email *"
              placeholder="info@empresa.com"
              :rules="[
                v => !!v || 'Campo requerido',
                v => /.+@.+\..+/.test(v) || 'Email inválido'
              ]"
              type="email"
            >
              <template #appendInner>
                <VaIcon name="email" />
              </template>
            </VaInput>

            <VaInput
              v-model="businessData.website"
              label="Sitio Web"
              placeholder="www.empresa.com"
              type="url"
            >
              <template #appendInner>
                <VaIcon name="language" />
              </template>
            </VaInput>

            <VaSelect
              v-model="businessData.category"
              label="Categoría Principal *"
              :options="categories"
              placeholder="Selecciona una categoría"
              :rules="[v => !!v || 'Campo requerido']"
            />
          </div>

          <VaTextarea
            v-model="businessData.description"
            label="Descripción de la Empresa *"
            placeholder="Describe tu empresa, productos y servicios..."
            :min-rows="4"
            :max-rows="8"
            counter
            :max-length="1000"
            :rules="[
              v => !!v || 'Campo requerido',
              v => v.length >= 100 || 'Mínimo 100 caracteres'
            ]"
          />
        </div>
      </div>

      <!-- Step 3: Ubicación GPS -->
      <div v-show="currentStep === 2" class="form-step">
        <GPSLocation
          v-model:coordinates="businessData.coordinates"
          v-model:address="businessData.address"
        />
      </div>

      <!-- Step 4: SEO -->
      <div v-show="currentStep === 3" class="form-step">
        <SEOFields
          v-model="businessData.seo"
          entity-type="negocio"
          base-url="guiaspurpuras.com/negocios"
          :available-categories="seoCategories"
        />
      </div>

      <!-- Step 5: Revisión -->
      <div v-show="currentStep === 4" class="form-step">
        <div class="review-section">
          <h3 class="section-title">
            <va-icon name="preview" />
            Vista Previa
          </h3>

          <div class="review-content">
            <!-- Banner Preview -->
            <div v-if="businessData.banner" class="review-banner">
              <img :src="bannerPreview" alt="Banner" />
            </div>

            <!-- Logo + Info -->
            <div class="review-header">
              <div v-if="businessData.logo" class="review-logo">
                <img :src="logoPreview" alt="Logo" />
              </div>
              <div class="review-info">
                <h2>{{ businessData.name || 'Nombre de la empresa' }}</h2>
                <p class="review-category">{{ businessData.category || 'Categoría' }}</p>
              </div>
            </div>

            <!-- Details -->
            <div class="review-details">
              <div class="review-card">
                <h4><va-icon name="info" /> Información</h4>
                <p><strong>NIT:</strong> {{ businessData.nit || 'N/A' }}</p>
                <p><strong>Teléfono:</strong> {{ businessData.phone || 'N/A' }}</p>
                <p><strong>Email:</strong> {{ businessData.email || 'N/A' }}</p>
                <p v-if="businessData.website"><strong>Web:</strong> {{ businessData.website }}</p>
              </div>

              <div class="review-card">
                <h4><va-icon name="description" /> Descripción</h4>
                <p>{{ businessData.description || 'Sin descripción' }}</p>
              </div>

              <div class="review-card">
                <h4><va-icon name="place" /> Ubicación</h4>
                <p v-if="businessData.coordinates">{{ businessData.coordinates }}</p>
                <p v-if="businessData.address">{{ businessData.address }}</p>
                <p v-if="!businessData.coordinates && !businessData.address">Sin ubicación</p>
              </div>

              <div class="review-card">
                <h4><va-icon name="search" /> SEO</h4>
                <p><strong>Slug:</strong> {{ businessData.seo.slug || 'N/A' }}</p>
                <p><strong>Palabra clave:</strong> {{ businessData.seo.mainKeyword || 'N/A' }}</p>
                <p><strong>Tags:</strong> {{ businessData.seo.tags.length }} agregados</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Buttons -->
    <div class="form-navigation">
      <VaButton
        v-if="currentStep > 0"
        preset="secondary"
        @click="previousStep"
      >
        <va-icon name="arrow_back" />
        Anterior
      </VaButton>

      <div class="nav-spacer"></div>

      <VaButton
        v-if="currentStep < steps.length - 1"
        color="purple"
        @click="nextStep"
        :disabled="!canProceed"
      >
        Siguiente
        <va-icon name="arrow_forward" />
      </VaButton>

      <VaButton
        v-else
        color="success"
        @click="submitForm"
        :loading="saving"
      >
        <va-icon name="check" />
        {{ isEditing ? 'Actualizar' : 'Publicar' }}
      </VaButton>

      <VaButton
        preset="plain"
        @click="cancelForm"
      >
        Cancelar
      </VaButton>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'

// ⭐ IMPORTS CORREGIDOS CON ALIAS @
import ImageUploadBusiness from '@/components/Upload/ImageUploadBusiness.vue'
import GPSLocation from '@/components/Location/GPSLocation.vue'
import SEOFields from '@/components/SEO/SEOFields.vue'

// ========== PROPS ==========
const props = defineProps({
  existingBusiness: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['save', 'update', 'cancel'])

// ========== COMPOSABLES ==========
const router = useRouter()
const { init: notify } = useToast()

// ========== STATE ==========
const currentStep = ref(0)
const saving = ref(false)

const steps = [
  'Imágenes',
  'Datos',
  'Ubicación',
  'SEO',
  'Revisión'
]

const businessData = ref({
  logo: null,
  banner: null,
  name: '',
  nit: '',
  phone: '',
  email: '',
  website: '',
  category: '',
  description: '',
  coordinates: '',
  address: '',
  seo: {
    slug: '',
    mainKeyword: '',
    tags: [],
    metaDescription: '',
    locationKeywords: '',
    categories: []
  }
})

const categories = [
  'Manufactura',
  'Servicios',
  'Comercio',
  'Tecnología',
  'Alimentación',
  'Construcción',
  'Textil',
  'Automotriz',
  'Salud',
  'Educación',
  'Turismo',
  'Logística'
]

const seoCategories = [
  { id: 1, name: 'Manufactura', selected: false },
  { id: 2, name: 'Servicios', selected: false },
  { id: 3, name: 'Comercio', selected: false },
  { id: 4, name: 'Tecnología', selected: false },
  { id: 5, name: 'Alimentación', selected: false },
  { id: 6, name: 'Construcción', selected: false },
  { id: 7, name: 'Textil', selected: false },
  { id: 8, name: 'Automotriz', selected: false }
]

// ========== COMPUTED ==========
const isEditing = computed(() => {
  return props.existingBusiness !== null
})

const logoPreview = computed(() => {
  if (!businessData.value.logo) return null
  if (typeof businessData.value.logo === 'string') return businessData.value.logo
  return URL.createObjectURL(businessData.value.logo)
})

const bannerPreview = computed(() => {
  if (!businessData.value.banner) return null
  if (typeof businessData.value.banner === 'string') return businessData.value.banner
  return URL.createObjectURL(businessData.value.banner)
})

const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0: // Imágenes
      return businessData.value.logo && businessData.value.banner
    case 1: // Datos
      return businessData.value.name && 
             businessData.value.nit && 
             businessData.value.phone && 
             businessData.value.email && 
             businessData.value.category &&
             businessData.value.description.length >= 100
    case 2: // Ubicación
      return businessData.value.coordinates
    case 3: // SEO
      return businessData.value.seo.slug && 
             businessData.value.seo.mainKeyword && 
             businessData.value.seo.metaDescription
    default:
      return true
  }
})

// ========== METHODS ==========
const nextStep = () => {
  if (!canProceed.value) {
    notify({
      message: '⚠️ Por favor completa todos los campos requeridos',
      color: 'warning'
    })
    return
  }

  if (currentStep.value < steps.length - 1) {
    currentStep.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const submitForm = async () => {
  saving.value = true

  // Simular guardado
  await new Promise(resolve => setTimeout(resolve, 2000))

  if (isEditing.value) {
    emit('update', businessData.value)
  } else {
    emit('save', businessData.value)
  }

  saving.value = false
}

const cancelForm = () => {
  if (confirm('¿Estás seguro de cancelar? Los cambios no guardados se perderán.')) {
    emit('cancel')
  }
}

// Cargar datos si está editando
if (props.existingBusiness) {
  businessData.value = { ...props.existingBusiness }
}
</script>

<style scoped>
/* ========== Container ========== */
.business-form {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

/* ========== Header ========== */
.form-header {
  text-align: center;
  margin-bottom: 3rem;
}

.form-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 2rem;
  font-weight: 700;
  color: #5C0099;
  margin: 0 0 1rem 0;
}

.form-subtitle {
  margin: 0;
  color: #666;
  font-size: 1.1rem;
}

/* ========== Steps ========== */
.form-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 3rem;
  position: relative;
}

.form-steps::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 40px;
  right: 40px;
  height: 2px;
  background: #E0E0E0;
  z-index: 0;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  z-index: 1;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  border: 2px solid #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #999;
  transition: all 0.3s ease;
}

.step-item.active .step-number {
  border-color: #5C0099;
  background: #5C0099;
  color: white;
}

.step-item.completed .step-number {
  border-color: #4CAF50;
  background: #4CAF50;
  color: white;
}

.step-label {
  font-size: 0.85rem;
  color: #666;
  font-weight: 500;
}

.step-item.active .step-label {
  color: #5C0099;
  font-weight: 600;
}

/* ========== Form Content ========== */
.form-content {
  margin-bottom: 2rem;
}

.form-step {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.step-section {
  padding: 2rem;
  background: white;
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #5C0099;
  margin: 0 0 2rem 0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

/* ========== Review ========== */
.review-section {
  padding: 2rem;
  background: white;
  border-radius: 16px;
}

.review-content {
  margin-top: 2rem;
}

.review-banner {
  width: 100%;
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.review-banner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.review-header {
  display: flex;
  gap: 2rem;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid #F0F0F0;
}

.review-logo {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  border: 2px solid #E0E0E0;
}

.review-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 0.5rem;
}

.review-info h2 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.5rem;
}

.review-category {
  margin: 0;
  color: #5C0099;
  font-weight: 600;
}

.review-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.review-card {
  padding: 1.5rem;
  background: #F8F8F8;
  border-radius: 12px;
}

.review-card h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 1rem 0;
  color: #5C0099;
  font-size: 1.1rem;
}

.review-card p {
  margin: 0 0 0.5rem 0;
  color: #666;
  line-height: 1.6;
}

.review-card p:last-child {
  margin-bottom: 0;
}

/* ========== Navigation ========== */
.form-navigation {
  display: flex;
  gap: 1rem;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.nav-spacer {
  flex: 1;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .business-form {
    padding: 1rem;
  }

  .form-title {
    font-size: 1.5rem;
    flex-direction: column;
  }

  .form-steps {
    overflow-x: auto;
    padding-bottom: 1rem;
  }

  .step-label {
    font-size: 0.75rem;
    white-space: nowrap;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .review-header {
    flex-direction: column;
    text-align: center;
  }

  .review-details {
    grid-template-columns: 1fr;
  }

  .form-navigation {
    flex-wrap: wrap;
  }

  .nav-spacer {
    display: none;
  }
}
</style>