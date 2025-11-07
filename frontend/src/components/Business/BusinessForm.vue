<!-- frontend/src/components/Business/BusinessForm.vue -->
<!-- ✨ INTEGRADO CON BRANCHMANAGER -->
<template>
  <div class="business-form">
    
    <div class="form-header">
      <h2 class="form-title">
        <va-icon :name="isEditing ? 'edit' : 'add_business'" size="2rem" />
        {{ isEditing ? 'Editar Negocio' : 'Crear Nuevo Negocio' }}
      </h2>
      <p class="form-subtitle">
        Completa la información de tu empresa para aparecer en Guías Púrpuras
      </p>
    </div>

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
              label="Categoría *"
              placeholder="Selecciona una categoría"
              :options="categories"
              :rules="[v => !!v || 'Campo requerido']"
            />
          </div>

          <VaTextarea
            v-model="businessData.description"
            label="Descripción de la Empresa *"
            placeholder="Describe tu empresa, productos o servicios..."
            :min-rows="5"
            :rules="[
              v => !!v || 'Campo requerido',
              v => v.length >= 100 || 'Mínimo 100 caracteres'
            ]"
            counter
          />
        </div>
      </div>

      <!-- Step 3: Ubicación GPS + ✨ SUCURSALES -->
      <div v-show="currentStep === 2" class="form-step">
        
        <!-- GPS Location Principal -->
        <div class="step-section">
          <h3 class="section-title">
            <va-icon name="place" />
            Ubicación Principal
          </h3>
          <GPSLocation
            v-model:coordinates="businessData.coordinates"
            v-model:address="businessData.address"
          />
        </div>

        <!-- ✨ SUCURSALES ADICIONALES (NUEVO) -->
        <div class="step-section">
          <BranchManager
            ref="branchManagerRef"
            v-model="businessData.branches"
            :user-plan="userPlan"
            :cities="cities"
            @upgrade-plan="handleUpgradePlan"
          />
        </div>

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
            <div v-if="businessData.banner" class="review-banner">
              <img :src="bannerPreview" alt="Banner" />
            </div>

            <div class="review-header">
              <div v-if="businessData.logo" class="review-logo">
                <img :src="logoPreview" alt="Logo" />
              </div>
              <div class="review-info">
                <h2>{{ businessData.name || 'Nombre de la empresa' }}</h2>
                <p class="review-category">{{ businessData.category || 'Categoría' }}</p>
              </div>
            </div>

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
                <!-- ✨ SUCURSALES (NUEVO) -->
                <p v-if="businessData.branches && businessData.branches.length > 0">
                  <strong>Sucursales adicionales:</strong> {{ businessData.branches.length }}
                </p>
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

// ⭐ IMPORTS CON ALIAS @
import ImageUploadBusiness from '@/components/Upload/ImageUploadBusiness.vue'
import GPSLocation from '@/components/Location/GPSLocation.vue'
import SEOFields from '@/components/SEO/SEOFields.vue'
import BranchManager from '@/components/Common/BranchManager.vue' // ✨ NUEVO

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
const branchManagerRef = ref(null) // ✨ NUEVO

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
  branches: [], // ✨ NUEVO
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

// ✨ CIUDADES (NUEVO)
const cities = ref([
  { id: 'cochabamba', name: 'Cochabamba' },
  { id: 'la-paz', name: 'La Paz' },
  { id: 'santa-cruz', name: 'Santa Cruz' },
  { id: 'sucre', name: 'Sucre' },
  { id: 'tarija', name: 'Tarija' },
  { id: 'potosi', name: 'Potosí' },
  { id: 'oruro', name: 'Oruro' },
  { id: 'beni', name: 'Beni' },
  { id: 'pando', name: 'Pando' }
])

// ✨ USER PLAN (NUEVO)
const userPlan = computed(() => {
  // TODO: return useUserStore().plan || 'free'
  return 'oro' // Cambiar cuando store esté listo
})

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
    case 2: // Ubicación + Sucursales ✨ MODIFICADO
      // Validar ubicación principal
      if (!businessData.value.coordinates) return false
      // Validar sucursales si existen
      if (branchManagerRef.value && !branchManagerRef.value.validate()) return false
      return true
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

// ✨ HANDLER UPGRADE PLAN (NUEVO)
const handleUpgradePlan = () => {
  router.push('/planes')
}

// Cargar datos si está editando
if (props.existingBusiness) {
  Object.assign(businessData.value, props.existingBusiness)
}
</script>

<style scoped>
/* Estilos originales mantenidos */
.business-form {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

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
  color: var(--color-purple);
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 1.125rem;
  color: #666;
}

.form-steps {
  display: flex;
  justify-content: space-between;
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

.step-item:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 20px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: #E0E0E0;
  z-index: -1;
}

.step-item.completed:not(:last-child)::after {
  background: var(--color-purple);
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #E0E0E0;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  transition: all 0.3s ease;
}

.step-item.active .step-number {
  background: var(--color-purple);
  color: white;
  transform: scale(1.1);
}

.step-item.completed .step-number {
  background: var(--color-purple);
  color: white;
}

.step-label {
  font-size: 0.875rem;
  color: #666;
  text-align: center;
}

.step-item.active .step-label {
  color: var(--color-purple);
  font-weight: 600;
}

.form-content {
  min-height: 500px;
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
  margin-bottom: 3rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple);
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #E0E0E0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.review-section {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.review-banner {
  height: 200px;
  overflow: hidden;
}

.review-banner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
  background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
}

.review-logo {
  width: 100px;
  height: 100px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.review-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.review-info h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple);
  margin-bottom: 0.5rem;
}

.review-category {
  font-size: 1.125rem;
  color: #666;
}

.review-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 2rem;
}

.review-card {
  background: #F9FAFB;
  border-radius: 12px;
  padding: 1.5rem;
}

.review-card h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-purple);
  margin-bottom: 1rem;
}

.review-card p {
  margin-bottom: 0.5rem;
  color: #374151;
  line-height: 1.6;
}

.form-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding-top: 2rem;
  border-top: 2px solid #E0E0E0;
}

.nav-spacer {
  flex: 1;
}

@media (max-width: 768px) {
  .business-form {
    padding: 1rem;
  }

  .form-steps {
    flex-direction: column;
    gap: 1rem;
  }

  .step-item:not(:last-child)::after {
    display: none;
  }

  .form-grid {
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