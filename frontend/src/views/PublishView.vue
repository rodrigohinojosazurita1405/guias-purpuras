<!-- 
  ==========================================
  PUBLISHVIEW.VUE - BLOQUE 1: TEMPLATE
  ==========================================
  
  Este es el TEMPLATE (HTML) del PublishView.
  Copia este bloque en la sección <template> de tu archivo.
  
  Estructura:
    - MainLayout wrapper
    - Indicador de pasos (PublishSteps)
    - Contenedor de formulario
    - Paso activo actual
    - Botones de navegación
-->

<template>
  <MainLayout>
    <section class="publish-section">
      <div class="container">
        <!-- 
          ==========================================
          HEADER
          ==========================================
        -->
        <div class="publish-header">
          <h1 class="publish-title">Publica tu Anuncio</h1>
          <p class="publish-subtitle">
            Completa el formulario y llega a miles de personas en Bolivia
          </p>
        </div>

        <!-- 
          ==========================================
          INDICADOR DE PASOS
          ==========================================
        -->
        <PublishSteps 
          :current-step="currentStep" 
          :steps="steps" 
        />

        <!-- 
          ==========================================
          FORMULARIO PRINCIPAL
          ==========================================
        -->
        <div class="form-card">
          <!-- PASO 1: Categoría y Ubicación -->
          <CategoryStep
            v-if="currentStep === 1"
            ref="categoryStepRef"
            v-model="formData"
          />

          <!-- PASO 2: Información del Anuncio -->
          <!-- Usa formulario específico para profesionales -->
          <InformationStepProfessional
            v-if="currentStep === 2 && formData.category === 'profesionales'"
            ref="informationStepRef"
            v-model="formData"
            :subcategory="formData.subcategory"
          />
          
          <!-- Usa formulario genérico para otras categorías -->
          <InformationStep
            v-if="currentStep === 2 && formData.category !== 'profesionales'"
            ref="informationStepRef"
            v-model="formData"
          />

          <!-- PASO 3: Imágenes -->
          <ImagesStep
            v-if="currentStep === 3"
            ref="imagesStepRef"
            v-model="formData.images"
            :plan="formData.plan"
          />

          <!-- PASO 4: Selección de Plan -->
          <PlanStep
            v-if="currentStep === 4"
            ref="planStepRef"
            v-model="formData.plan"
          />

          <!-- PASO 5: Resumen y Confirmación -->
          <div v-if="currentStep === 5" class="summary-step">
            <SummaryCard 
              :form-data="formData"
              :editable="true"
              @edit-step="goToStep"
            />
          </div>

          <!-- 
            ==========================================
            NAVEGACIÓN ENTRE PASOS
            ==========================================
          -->
          <div class="form-navigation">
            <!-- Botón Anterior -->
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

            <!-- Espaciador -->
            <div class="spacer"></div>

            <!-- Botón Siguiente -->
            <va-button
              v-if="currentStep < 5"
              @click="nextStep"
              color="purple"
              size="large"
              class="nav-btn"
              :disabled="isSubmitting"
            >
              Siguiente
              <va-icon name="arrow_forward" />
            </va-button>

            <!-- Botón Publicar -->
            <va-button
              v-if="currentStep === 5"
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

        <!-- 
          ==========================================
          INDICADOR DE GUARDADO AUTOMÁTICO
          ==========================================
        -->
        <div v-if="showAutoSaveIndicator" class="auto-save-indicator">
          <va-icon name="cloud_done" color="success" />
          <span>Borrador guardado automáticamente</span>
        </div>
      </div>
    </section>
  </MainLayout>
</template>
<!-- BLOQUE 2: SCRIPT -->
<script setup>
// ==========================================
// PUBLISHVIEW.VUE - BLOQUE 2: SCRIPT SETUP
// ==========================================
// 
// Este es el SCRIPT (JavaScript) del PublishView.
// Copia este bloque en la sección <script setup> de tu archivo.
//
// Funcionalidades:
//   - Gestión del estado del formulario
//   - Navegación entre pasos con validación
//   - Auto-guardado de borrador
//   - Submit y envío al backend
// ==========================================

import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '@/components/Layout/MainLayout.vue'
import PublishSteps from '@/components/Publish/PublishSteps.vue'
import CategoryStep from '@/components/Publish/CategoryStep.vue'
import InformationStep from '@/components/Publish/InformationStep.vue'
import InformationStepProfessional from '@/components/Publish/InformationStepProfessional.vue'
import ImagesStep from '@/components/Publish/ImagesStep.vue'
import PlanStep from '@/components/Publish/PlanStep.vue'
import SummaryCard from '@/components/Publish/SummaryCard.vue'

// ==========================================
// COMPOSABLES
// ==========================================
const router = useRouter()

// ==========================================
// STATE
// ==========================================
const currentStep = ref(1)
const isSubmitting = ref(false)
const showAutoSaveIndicator = ref(false)

const steps = ['Categoría', 'Información', 'Imágenes', 'Plan', 'Confirmar']

// Referencias a los componentes de cada paso (para llamar validate())
const categoryStepRef = ref(null)
const informationStepRef = ref(null)
const imagesStepRef = ref(null)
const planStepRef = ref(null)

// Datos del formulario (modelo principal)
const formData = ref({
  // Paso 1: Categoría y Ubicación
  category: '',
  subcategory: '',
  city: '',
  address: '',
  
  // Paso 2: Información (Genérica O Profesional según categoría)
  title: '',
  
  // Campos genéricos (Gastronomía, Trabajos, Servicios)
  description: '',
  price: null,
  
  // Campos específicos para PROFESIONALES
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
  
  // Contacto (común para todos)
  whatsapp: '',
  email: '',
  website: '',
  
  // Paso 3: Imágenes
  images: [],
  
  // Paso 4: Plan
  plan: 'free'
})

// ==========================================
// MÉTODOS DE NAVEGACIÓN
// ==========================================

/**
 * Avanza al siguiente paso
 * Valida el paso actual antes de avanzar
 */
const nextStep = async () => {
  // Validar el paso actual
  const isValid = await validateCurrentStep()
  
  if (!isValid) {
    // Mostrar mensaje de error (TODO: implementar notificación)
    console.error('Validación fallida. Revisa los campos obligatorios.')
    return
  }
  
  // Avanzar al siguiente paso
  if (currentStep.value < 5) {
    currentStep.value++
    scrollToTop()
  }
}

/**
 * Retrocede al paso anterior
 */
const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    scrollToTop()
  }
}

/**
 * Ir a un paso específico (desde SummaryCard)
 */
const goToStep = (step) => {
  currentStep.value = step
  scrollToTop()
}

/**
 * Scroll suave al inicio del formulario
 */
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ==========================================
// VALIDACIONES
// ==========================================

/**
 * Valida el paso actual llamando al método validate() del componente
 */
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
      stepRef = planStepRef.value
      break
          case 5:
      return true // El paso 5 es solo resumen
  }
  
  if (stepRef && typeof stepRef.validate === 'function') {
    return stepRef.validate()
  }
  
  return true
}

// ==========================================
// AUTO-GUARDADO (BORRADOR)
// ==========================================

/**
 * Guarda el formulario en localStorage cada 3 segundos
 * TODO Django: Reemplazar con POST /api/listings/draft/
 */
const saveAsDraft = () => {
  try {
    localStorage.setItem('listing_draft', JSON.stringify(formData.value))
    showAutoSaveIndicator.value = true
    
    // Ocultar indicador después de 2 segundos
    setTimeout(() => {
      showAutoSaveIndicator.value = false
    }, 2000)
  } catch (error) {
    console.error('Error guardando borrador:', error)
  }
}

/**
 * Carga el borrador guardado al montar el componente
 */
const loadDraft = () => {
  try {
    const draft = localStorage.getItem('listing_draft')
    if (draft) {
      const parsed = JSON.parse(draft)
      
      // Preguntar al usuario si quiere continuar con el borrador
      if (confirm('¿Deseas continuar con tu borrador guardado?')) {
        formData.value = { ...formData.value, ...parsed }
      } else {
        // Limpiar borrador si el usuario no quiere usarlo
        localStorage.removeItem('listing_draft')
      }
    }
  } catch (error) {
    console.error('Error cargando borrador:', error)
  }
}

// ==========================================
// SUBMIT (PUBLICAR ANUNCIO)
// ==========================================

/**
 * Envía el formulario al backend
 * TODO Django: Implementar integración completa
 */
const submitForm = async () => {
  isSubmitting.value = true
  
  try {
    // Preparar FormData para envío (incluye imágenes)
    const payload = new FormData()
    
    // Datos básicos
    payload.append('category', formData.value.category)
    payload.append('subcategory', formData.value.subcategory)
    payload.append('city', formData.value.city) // CAMBIO: Ahora es ciudad en lugar de department
    payload.append('address', formData.value.address) // CAMBIO: Nueva dirección exacta
    payload.append('title', formData.value.title)
    payload.append('description', formData.value.description)
    payload.append('whatsapp', formData.value.whatsapp) // CAMBIO: WhatsApp con +591
    payload.append('plan', formData.value.plan)
    
    // Campos opcionales
    if (formData.value.price) {
      payload.append('price', formData.value.price)
    }
    if (formData.value.email) {
      payload.append('email', formData.value.email)
    }
    if (formData.value.website) {
      payload.append('website', formData.value.website)
    }
    
    // Imágenes
    formData.value.images.forEach((img, index) => {
      payload.append(`images`, img.file)
      if (index === 0) {
        payload.append('main_image_index', '0')
      }
    })
    
    // TODO Django: Descomentar cuando tengamos backend
    // const response = await axios.post('/api/listings/', payload, {
    //   headers: {
    //     'Content-Type': 'multipart/form-data'
    //   }
    // })
    
    // Simulación de respuesta del backend
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    console.log('Formulario enviado:', Object.fromEntries(payload))
    
    // Limpiar borrador
    localStorage.removeItem('listing_draft')
    
    // Verificar si requiere pago
    if (formData.value.plan !== 'free') {
      // TODO Django: Redirigir a pasarela de pago
      // window.location.href = response.data.payment_url
      alert(`Redirigiendo a pasarela de pago - Plan: ${formData.value.plan}`)
      // Por ahora, redirigir al home
      router.push('/')
    } else {
      // Plan gratis: Publicado inmediatamente
      alert('¡Anuncio publicado exitosamente! (Válido por 7 días)')
      router.push('/')
    }
    
  } catch (error) {
    console.error('Error al publicar anuncio:', error)
    alert('Error al publicar. Inténtalo de nuevo.')
  } finally {
    isSubmitting.value = false
  }
}

// ==========================================
// WATCHERS
// ==========================================

/**
 * Auto-guardar cada vez que cambia el formulario
 * Debounce de 3 segundos
 */
let autoSaveTimeout = null
watch(formData, () => {
  clearTimeout(autoSaveTimeout)
  autoSaveTimeout = setTimeout(() => {
    saveAsDraft()
  }, 3000)
}, { deep: true })

// ==========================================
// LIFECYCLE HOOKS
// ==========================================

/**
 * Al montar el componente:
 * - Cargar borrador si existe
 * - Scroll al inicio
 */
onMounted(() => {
  loadDraft()
  scrollToTop()
})
</script>



<!-- BLOQUE 3: STYLES -->
<style scoped>
/* ==========================================
   PUBLISHVIEW.VUE - BLOQUE 3: STYLES
   ==========================================
   
   Estos son los ESTILOS (CSS) del PublishView.
   Copia este bloque en la sección <style scoped> de tu archivo.
   
   Incluye:
     - Estilos del contenedor principal
     - Header
     - Formulario
     - Navegación
     - Indicadores
     - Responsive
   ========================================== */

/* ==========================================
   SECTION PRINCIPAL
   ========================================== */
.publish-section {
  min-height: calc(100vh - 200px);
  padding: 3rem 1rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

/* ==========================================
   HEADER
   ========================================== */
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

/* ==========================================
   FORMULARIO
   ========================================== */
.form-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  margin-bottom: 2rem;
}

/* Paso de Resumen */
.summary-step {
  padding: 0;
}

/* ==========================================
   NAVEGACIÓN
   ========================================== */
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

/* ==========================================
   INDICADOR DE AUTO-GUARDADO
   ========================================== */
.auto-save-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #E8F5E9;
  border-radius: 12px;
  color: #2E7D32;
  font-weight: 600;
  animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ==========================================
   RESPONSIVE - TABLET
   ========================================== */
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

/* ==========================================
   RESPONSIVE - MOBILE
   ========================================== */
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