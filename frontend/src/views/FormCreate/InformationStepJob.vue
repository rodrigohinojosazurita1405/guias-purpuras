<!--
  ==========================================
  INFORMATIONSTEPJOB.VUE - CON CKEDITOR 5 WYSIWYG
  ==========================================
-->
<template>
  <div class="information-step-job">

    <!-- FORMULARIO SIMPLE Y LIMPIO CON HEADER INTEGRADO -->
    <div class="form-content">

      <!-- HEADER INTEGRADO -->
      <div class="integrated-header">
        <div class="header-icon">
          <va-icon name="work" size="2rem" style="color: white;" />
        </div>
        <div>
          <h2 class="step-title">Información detallada del Trabajo</h2>
          <p class="step-subtitle">
            Completa los detalles principales de la oferta laboral de forma simple y directa
          </p>
        </div>
      </div>

      <!-- SECCIÓN UNIFICADA -->
      <div class="form-section unified-job-section">
        <!-- GRUPO 1: DATOS BÁSICOS -->
        <div class="field-group">
          <!-- TÍTULO Y EMPRESA (GRID 2 COL) -->
          <div class="form-grid">
            <div class="form-row compact">
              <label class="form-label">Título del puesto laboral *</label>
              <va-input
                v-model="localFormData.title"
                placeholder="Ej: Administrador de empresas"
                counter
                maxlength="100"
                :rules="[
                  (v) => !!v || 'El título es requerido',
                  (v) => (v && v.length >= 5) || 'Mínimo 5 caracteres'
                ]"
                size="small"
              >
                <template #prepend>
                  <va-icon name="title" color="purple" />
                </template>
              </va-input>
            </div>

            <div class="form-row compact">
              <label class="form-label" :class="{ 'opacity-50': localFormData.companyAnonymous }">
                Empresa <span v-if="!localFormData.companyAnonymous">*</span>
              </label>
              <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
                <va-input
                  v-model="localFormData.companyName"
                  placeholder="TechCorp Bolivia"
                  :disabled="localFormData.companyAnonymous"
                  :rules="[
                    (v) => localFormData.companyAnonymous || !!v || 'El nombre de la empresa es requerido'
                  ]"
                  size="small"
                  style="flex: 1;"
                >
                  <template #prepend>
                    <va-icon name="business" color="purple" />
                  </template>
                </va-input>
                <!-- ANÓNIMO (INLINE) - Mini Switch Custom -->
                <div class="anonymous-switch-wrapper">
                  <label class="custom-switch">
                    <input
                      type="checkbox"
                      v-model="localFormData.companyAnonymous"
                      class="switch-checkbox"
                    />
                    <span class="switch-slider"></span>
                  </label>
                  <span class="switch-label">Anónimo</span>
                </div>
              </div>
            </div>
          </div>

          <!-- CATEGORÍA, TIPO Y MODALIDAD (GRID 3 COL) -->
          <div class="form-grid grid-3col">
            <div class="form-row compact">
              <label class="form-label">Categoría del anuncio *</label>
              <va-select
                v-model="localFormData.jobCategory"
                :options="categoryOptions"
                placeholder="Selecciona"
                :rules="[(v) => !!v || 'La categoría es requerida']"
                size="small"
                searchable
                highlight-matched-text
                :max-visible-options="6"
              >
                <template #prepend>
                  <va-icon name="category" color="purple" />
                </template>
              </va-select>
            </div>

            <div class="form-row compact">
              <label class="form-label">Tipo Contrato *</label>
              <va-select
                v-model="localFormData.contractType"
                :options="contractTypeOptions"
                placeholder="Selecciona"
                :rules="[(v) => !!v || 'El tipo de contrato es requerido']"
                size="small"
              >
                <template #prepend>
                  <va-icon name="schedule" color="purple" />
                </template>
              </va-select>
            </div>

            <div class="form-row compact">
              <label class="form-label">Modalidad *</label>
              <va-select
                v-model="localFormData.modality"
                :options="modalityOptions"
                placeholder="Selecciona"
                :rules="[(v) => !!v || 'La modalidad es requerida']"
                size="small"
              >
                <template #prepend>
                  <va-icon name="laptop" color="purple" />
                </template>
              </va-select>
            </div>
          </div>

          <!-- CIUDAD, PROVINCIA, FECHA (GRID 3 COL) -->
          <div class="form-grid grid-3col">
            <div class="form-row compact">
              <label class="form-label">Ciudad *</label>
              <va-select
                v-model="localFormData.city"
                :options="cityOptions"
                placeholder="Selecciona"
                :rules="[(v) => !!v || 'La ciudad es requerida']"
                size="small"
              >
                <template #prepend>
                  <va-icon name="location_city" color="purple" />
                </template>
              </va-select>
            </div>

            <div class="form-row compact">
              <label class="form-label">Provincia / Municipio</label>
              <va-input
                v-model="localFormData.municipality"
                placeholder="Opcional"
                size="small"
              >
                <template #prepend>
                  <va-icon name="place" color="purple" />
                </template>
              </va-input>
            </div>

            <div class="form-row compact">
              <label class="form-label">Fecha límite postulación *</label>
              <va-date-input
                v-model="localFormData.expiryDate"
                placeholder="Selecciona"
                :rules="[(v) => !!v || 'La fecha de vencimiento es requerida']"
                size="small"
              >
                <template #prepend>
                  <va-icon name="event" color="purple" />
                </template>
              </va-date-input>
            </div>
          </div>
        </div>

        <!-- SEPARADOR VISUAL -->
        <div class="field-separator"></div>

        <!-- GRUPO 2: TINYMCE WYSIWYG -->
        <div class="field-group">
          <div class="form-row">
            <label class="form-label">Detalles de la oferta Laboral *</label>
            <div class="editor-wrapper">
              <div ref="editorContainer" class="tinymce-container"></div>
              <div class="editor-char-count">
                {{ charCount }} / 2000 caracteres
                <span v-if="charCount < 50" class="char-warning"> - Mínimo 50 caracteres</span>
                <span v-else-if="charCount > 2000" class="char-error"> - Máximo excedido</span>
                <span v-else class="char-success"> ✓</span>
              </div>
            </div>
          </div>
        </div>

        <!-- SEPARADOR VISUAL -->
        <div class="field-separator"></div>

        <!-- GRUPO 3: COMPENSACIÓN Y VACANTES (COMPACTO) -->
        <div class="field-group">
          <h4 class="group-subtitle">
            <va-icon name="attach_money" size="1rem" />
            Compensación Económica y Vacantes Disponibles
          </h4>

          <!-- GRID COMPACTO: VACANTES + TIPO SALARIO -->
          <div class="form-grid compact-compensation-grid">
            <!-- VACANTES -->
            <div class="form-row compact">
              <label class="form-label">Vacantes *</label>
              <div class="vacancy-input-group compact">
                <button
                  type="button"
                  class="vacancy-btn-sm"
                  @click="decrementVacancies"
                  :disabled="localFormData.vacancies <= 1"
                >
                  −
                </button>
                <input
                  v-model.number="localFormData.vacancies"
                  type="number"
                  min="1"
                  max="100"
                  class="vacancy-input-sm"
                  @input="(e) => updateVacancies(parseInt(e.target.value) || 1)"
                />
                <button
                  type="button"
                  class="vacancy-btn-sm"
                  @click="incrementVacancies"
                  :disabled="localFormData.vacancies >= 100"
                >
                  +
                </button>
              </div>
            </div>

            <!-- TIPO SALARIO -->
            <div class="form-row compact">
              <label class="form-label">Salario *</label>
              <div class="salary-type-compact">
                <label class="radio-label-compact">
                  <va-radio
                    v-model="localFormData.salaryType"
                    option="range"
                    label=""
                  />
                  <span>Rango</span>
                </label>
                <label class="radio-label-compact">
                  <va-radio
                    v-model="localFormData.salaryType"
                    option="fixed"
                    label=""
                  />
                  <span>Fijo</span>
                </label>
                <label class="radio-label-compact">
                  <va-radio
                    v-model="localFormData.salaryType"
                    option="negotiable"
                    label=""
                  />
                  <span>A convenir</span>
                </label>
              </div>
            </div>
          </div>

          <!-- SALARIO - RANGO (INLINE) -->
          <div v-if="localFormData.salaryType === 'range'" class="salary-inputs-inline">
            <div class="form-field-inline">
              <label class="form-label-sm">Mín (Bs.) *</label>
              <va-input
                v-model.number="localFormData.salaryMin"
                type="number"
                placeholder="Min"
                :rules="[(v) => !!v || 'Requerido']"
                size="small"
              />
            </div>
            <span class="separator">−</span>
            <div class="form-field-inline">
              <label class="form-label-sm">Máx (Bs.) *</label>
              <va-input
                v-model.number="localFormData.salaryMax"
                type="number"
                placeholder="Max"
                :rules="[
                  (v) => !!v || 'Requerido',
                  (v) => !localFormData.salaryMin || v > localFormData.salaryMin || 'Debe ser mayor'
                ]"
                size="small"
              />
            </div>
          </div>

          <!-- SALARIO - FIJO (INLINE) -->
          <div v-if="localFormData.salaryType === 'fixed'" class="form-row compact">
            <label class="form-label-sm">Salario (Bs.) *</label>
            <va-input
              v-model.number="localFormData.salaryFixed"
              type="number"
              placeholder="Salario fijo"
              :rules="[(v) => !!v || 'Requerido']"
              size="small"
            />
          </div>
        </div>

      </div>

      <!-- BOTONES DE NAVEGACIÓN -->
      <div class="navigation-buttons">
        <button class="btn btn-secondary" @click="handleBack">
          <va-icon name="arrow_back" size="small" />
          Atrás
        </button>

        <button class="btn btn-primary" @click="handleNext">
          Siguiente
          <va-icon name="arrow_forward" size="small" />
        </button>
      </div>

    </div>

    <!-- MODAL DE ERRORES DE VALIDACIÓN -->
    <va-modal
      v-model="showErrorModal"
      title="Campos Incompletos"
      size="medium"
      ok-text="Entendido"
      hide-default-actions
    >
      <div class="error-modal-content">
        <div class="error-icon">
          <va-icon name="error" size="4rem" color="danger" />
        </div>
        <h3 class="error-title">Por favor completa los siguientes campos:</h3>
        <ul class="error-list">
          <li v-for="(error, index) in validationErrors" :key="index" class="error-item">
            <va-icon name="arrow_right" size="small" color="danger" />
            {{ error }}
          </li>
        </ul>
      </div>
      <template #footer>
        <va-button @click="showErrorModal = false" color="primary">
          Entendido
        </va-button>
      </template>
    </va-modal>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'

// ========== PROPS Y EMITS ==========
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])

// ========== CKEDITOR VARIABLES ==========
const editorContainer = ref(null)
let editorInstance = null
const charCount = ref(0)

// ========== FUNCIÓN HELPER PARA INICIALIZAR DATOS ==========
const initializeFormData = (modelValue) => ({
  title: modelValue.title || '',
  companyName: modelValue.companyName || '',
  companyAnonymous: modelValue.companyAnonymous || false,
  jobDetailsHtml: modelValue.jobDetailsHtml || modelValue.description || '',
  jobCategory: modelValue.jobCategory || '',
  city: modelValue.city || '',
  municipality: modelValue.municipality || '',
  contractType: modelValue.contractType || '',
  modality: modelValue.modality || 'presencial',
  expiryDate: modelValue.expiryDate || null,
  salaryType: modelValue.salaryType || 'range',
  salaryMin: modelValue.salaryMin || null,
  salaryMax: modelValue.salaryMax || null,
  salaryFixed: modelValue.salaryFixed || null,
  benefits: modelValue.benefits || '',
  vacancies: modelValue.vacancies || 1
})

// ========== DATA LOCAL ==========
const localFormData = ref(initializeFormData(props.modelValue))

// ========== OPCIONES DE FORMULARIO (DINÁMICAS) ==========
const categoryOptions = ref([])
const contractTypeOptions = ref([])
const cityOptions = ref([])

// Opciones de modalidad (estáticas)
const modalityOptions = [
  { text: 'Presencial', value: 'presencial' },
  { text: 'Remoto', value: 'remoto' },
  { text: 'Híbrido', value: 'hibrido' }
]

const loadingCategories = ref(true)
const loadingContractTypes = ref(true)
const loadingCities = ref(true)

// ========== MODAL DE ERRORES ==========
const showErrorModal = ref(false)
const validationErrors = ref([])

// ========== INICIALIZAR QUILL EDITOR ==========
const initQuill = () => {
  // Cargar Quill desde CDN - 100% GRATUITO
  if (!window.Quill) {
    // Cargar CSS
    const link = document.createElement('link')
    link.href = 'https://cdn.quilljs.com/1.3.7/quill.snow.css'
    link.rel = 'stylesheet'
    document.head.appendChild(link)

    // Cargar JS
    const script = document.createElement('script')
    script.src = 'https://cdn.quilljs.com/1.3.7/quill.min.js'
    script.onload = () => {
      setTimeout(createQuill, 100)
    }
    document.head.appendChild(script)
  } else {
    createQuill()
  }
}

const createQuill = () => {
  if (!editorContainer.value || editorInstance) return

  const toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'indent': '-1'}, { 'indent': '+1' }],
    ['blockquote', 'link'],
    ['clean']
  ]

  editorInstance = new window.Quill(editorContainer.value, {
    theme: 'snow',
    placeholder: 'Cuéntale al candidato sobre el puesto: Descripción del trabajo, Responsabilidades principales, Requisitos y habilidades necesarias, Experiencia requerida, Beneficios y oportunidades',
    modules: {
      toolbar: toolbarOptions
    },
    formats: ['bold', 'italic', 'underline', 'strike', 'list', 'indent', 'blockquote', 'link']
  })

  // Establecer contenido inicial
  if (localFormData.value.jobDetailsHtml) {
    editorInstance.root.innerHTML = localFormData.value.jobDetailsHtml
  }

  // Sincronizar cambios y limpiar headers H1-H6
  editorInstance.on('text-change', () => {
    let html = editorInstance.root.innerHTML

    // Convertir todas las etiquetas H1-H6 a párrafos <p>
    html = html.replace(/<h[1-6]([^>]*)>/gi, '<p$1>')
    html = html.replace(/<\/h[1-6]>/gi, '</p>')

    const textContent = getTextFromHtml(html)
    charCount.value = textContent.length
    localFormData.value.jobDetailsHtml = html
  })

  // Calcular contador inicial
  setTimeout(() => {
    const initialText = getTextFromHtml(editorInstance.root.innerHTML)
    charCount.value = initialText.length
  }, 100)
}

// Función para extraer texto plano del HTML
const getTextFromHtml = (html) => {
  const tmp = document.createElement('DIV')
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ''
}

// Función para convertir texto a Title Case
const toTitleCase = (str) => {
  if (!str) return ''

  // Palabras que deben permanecer en minúsculas (excepto al inicio)
  const smallWords = ['de', 'del', 'la', 'el', 'los', 'las', 'y', 'e', 'o', 'u', 'en', 'a', 'al', 'con', 'por', 'para']

  return str
    .toLowerCase()
    .split(' ')
    .map((word, index) => {
      // Primera palabra siempre con mayúscula
      if (index === 0) {
        return word.charAt(0).toUpperCase() + word.slice(1)
      }
      // Palabras pequeñas en minúsculas (excepto la primera)
      if (smallWords.includes(word)) {
        return word
      }
      // Resto con mayúscula inicial
      return word.charAt(0).toUpperCase() + word.slice(1)
    })
    .join(' ')
}

// ========== WATCH PARA SINCRONIZACIÓN ==========
// Convertir título a Title Case automáticamente
watch(() => localFormData.value.title, (newTitle) => {
  if (newTitle && newTitle !== toTitleCase(newTitle)) {
    // Usar nextTick para evitar loops infinitos
    nextTick(() => {
      localFormData.value.title = toTitleCase(newTitle)
    })
  }
})

watch(localFormData, (newValue) => {
  const cleanedValue = {
    ...props.modelValue,
    ...newValue,
    description: newValue.jobDetailsHtml,
    jobCategory: typeof newValue.jobCategory === 'object' ? newValue.jobCategory?.value : newValue.jobCategory,
    city: typeof newValue.city === 'object' ? newValue.city?.value : newValue.city,
    contractType: typeof newValue.contractType === 'object' ? newValue.contractType?.value : newValue.contractType
  }
  emit('update:modelValue', cleanedValue)
}, { deep: true })

watch(() => [props.modelValue.description, props.modelValue.title, props.modelValue.jobDetailsHtml],
  (newVals) => {
    const [description] = newVals
    if (description && description !== localFormData.value.jobDetailsHtml) {
      localFormData.value = initializeFormData(props.modelValue)
      if (editorInstance && editorInstance.root) {
        editorInstance.root.innerHTML = description
      }
    }
  },
  { deep: true }
)

// ========== MÉTODOS DE VACANTES ==========
const incrementVacancies = () => {
  if (localFormData.value.vacancies < 100) {
    localFormData.value.vacancies++
  }
}

const decrementVacancies = () => {
  if (localFormData.value.vacancies > 1) {
    localFormData.value.vacancies--
  }
}

const updateVacancies = (value) => {
  if (value >= 1 && value <= 100) {
    localFormData.value.vacancies = value
  }
}

// ========== CARGAR DATOS DINÁMICOS DEL API ==========
const loadJobCategories = async () => {
  try {
    loadingCategories.value = true
    // Agregar timestamp para evitar caché del navegador
    const timestamp = new Date().getTime()
    const response = await fetch(`http://localhost:8000/api/jobs/categories-dynamic?_t=${timestamp}`, {
      cache: 'no-store'
    })
    const data = await response.json()

    if (data.success && data.categories) {
      categoryOptions.value = data.categories
    } else {
      console.error('Error loading categories:', data.message)
    }
  } catch (error) {
    console.error('Error fetching categories:', error)
  } finally {
    loadingCategories.value = false
  }
}

const loadContractTypes = async () => {
  try {
    loadingContractTypes.value = true
    const response = await fetch('http://localhost:8000/api/jobs/contract-types')
    const data = await response.json()

    if (data.success && data.contractTypes) {
      contractTypeOptions.value = data.contractTypes
    } else {
      console.error('Error loading contract types:', data.message)
    }
  } catch (error) {
    console.error('Error fetching contract types:', error)
  } finally {
    loadingContractTypes.value = false
  }
}

const loadCities = async () => {
  try {
    loadingCities.value = true
    const response = await fetch('http://localhost:8000/api/jobs/cities')
    const data = await response.json()

    if (data.success && data.cities) {
      cityOptions.value = data.cities
    } else {
      console.error('Error loading cities:', data.message)
    }
  } catch (error) {
    console.error('Error fetching cities:', error)
  } finally {
    loadingCities.value = false
  }
}

onMounted(() => {
  // Cargar todos los datos dinámicos en paralelo
  Promise.all([
    loadJobCategories(),
    loadContractTypes(),
    loadCities()
  ])
  
  // Inicializar Quill
  initQuill()
})

onBeforeUnmount(() => {
  // Destruir instancia de Quill
  if (editorInstance) {
    editorInstance = null
  }
})

// ========== NAVEGACIÓN ==========
const handleNext = () => {
  if (validate()) {
    emit('next')
  }
}

const handleBack = () => {
  emit('back')
}

// ========== VALIDACIÓN ==========
const validate = () => {
  const errors = []

  if (!localFormData.value.title) {
    errors.push('El título del puesto es requerido')
  }

  if (!localFormData.value.companyAnonymous && !localFormData.value.companyName) {
    errors.push('El nombre de la empresa es requerido (o marca como anónima)')
  }

  // Validar contenido de detalles del empleo
  const jobDetailsLength = charCount.value
  if (!localFormData.value.jobDetailsHtml || jobDetailsLength < 50) {
    errors.push(`La información del empleo debe tener al menos 50 caracteres (actualmente: ${jobDetailsLength})`)
  }

  if (jobDetailsLength > 2000) {
    errors.push(`La información del empleo no puede exceder 2000 caracteres (actualmente: ${jobDetailsLength})`)
  }

  if (!localFormData.value.jobCategory) {
    errors.push('La categoría es requerida')
  }

  if (!localFormData.value.city) {
    errors.push('La ciudad es requerida')
  }

  if (!localFormData.value.contractType) {
    errors.push('El tipo de contrato es requerido')
  }

  if (!localFormData.value.expiryDate) {
    errors.push('La fecha de vencimiento es requerida')
  }

  // Validación de salario
  if (localFormData.value.salaryType === 'range') {
    if (!localFormData.value.salaryMin) {
      errors.push('El salario mínimo es requerido')
    }
    if (!localFormData.value.salaryMax) {
      errors.push('El salario máximo es requerido')
    }
    if (localFormData.value.salaryMin && localFormData.value.salaryMax &&
        localFormData.value.salaryMin >= localFormData.value.salaryMax) {
      errors.push('El salario máximo debe ser mayor al mínimo')
    }
  }

  if (localFormData.value.salaryType === 'fixed' && !localFormData.value.salaryFixed) {
    errors.push('El salario es requerido')
  }

  if (errors.length > 0) {
    console.error('❌ ERRORES DE VALIDACIÓN:', errors)
    validationErrors.value = errors
    showErrorModal.value = true
    return false
  }

  return true
}

// ========== EXPONER MÉTODOS AL PADRE ==========
defineExpose({
  validate
})
</script>

<style scoped>
.information-step-job {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  background: linear-gradient(135deg, #FAFBFF 0%, #F5F3FF 100%);
  min-height: 100vh;
  padding: 1.5rem;
  position: relative;
  overflow-x: hidden; /* Evitar que CKEditor se salga horizontalmente */
}

.integrated-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #E9D5FF;
  margin-bottom: 1rem;
}

.header-icon {
  width: 72px;
  height: 72px;
  border-radius: 12px;
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.step-title {
  font-size: 2rem;
  font-weight: 800;
  color: #0F172A;
  margin: 0;
  letter-spacing: -0.4px;
  line-height: 1.2;
}

.step-subtitle {
  font-size: 1rem;
  color: #475569;
  margin: 0.75rem 0 0 0;
  line-height: 1.6;
  font-weight: 500;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: white;
  padding: 2rem;
  border-radius: 16px;
  max-width: 1160px;
  margin: 0 auto;
  box-shadow: 0 2px 12px rgba(124, 58, 237, 0.08);
  border: 1px solid rgba(124, 58, 237, 0.1);
  width: 100%;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
  background: linear-gradient(135deg, #FAFBFF 0%, #F7F6FF 100%);
  border-radius: 12px;
  border: 1px solid #E9D5FF;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1.25rem;
}

.form-row.compact {
  margin-bottom: 1.25rem;
  gap: 0.35rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.form-grid.grid-3col {
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.unified-job-section {
  gap: 1.25rem;
  padding: 1.75rem;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.field-separator {
  height: 1px;
  background: linear-gradient(90deg, transparent, #E9D5FF, transparent);
  margin: 0.75rem 0;
}

.group-subtitle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1E293B;
  margin: 0.25rem 0 0.5rem 0;
  padding: 0;
}

.form-label {
  font-weight: 600;
  color: #1E293B;
  font-size: 0.95rem;;
}

/* ========== TINYMCE STYLES ========== */
.editor-wrapper {
  width: 100%;
  position: relative;
  z-index: 1;
}

.tinymce-container {
  width: 100%;
  min-height: 300px;
}

/* Quill Editor - Fondo blanco */
:deep(.ql-container) {
  background: white !important;
}

:deep(.ql-editor) {
  background: white !important;
  min-height: 300px;
}

/* Neutralizar headers en Quill - forzar estilo de párrafo normal */
:deep(.ql-editor h1),
:deep(.ql-editor h2),
:deep(.ql-editor h3),
:deep(.ql-editor h4),
:deep(.ql-editor h5),
:deep(.ql-editor h6) {
  font-size: 1rem !important;
  font-weight: normal !important;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.5 !important;
}

/* TinyMCE Toolbar - Personalización */
:deep(.tox .tox-toolbar) {
  background: linear-gradient(135deg, #F9F5FF 0%, #F5EFFF 100%) !important;
  border-bottom: 2px solid #E9D5FF !important;
}

:deep(.tox .tox-tbtn) {
  border-radius: 6px !important;
}

:deep(.tox .tox-tbtn:hover) {
  background: #EDE9FE !important;
}

:deep(.tox .tox-tbtn--enabled) {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%) !important;
}

:deep(.tox .tox-tbtn--enabled svg) {
  fill: white !important;
}

:deep(.tox-tinymce) {
  border: 2px solid #E2E8F0 !important;
  border-radius: 8px !important;
}

:deep(.tox-tinymce:focus-within) {
  border-color: #7C3AED !important;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
}

:deep(.tox .tox-statusbar) {
  display: none !important;
}

.editor-char-count {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: #F8FAFC;
  border-top: 1px solid #E2E8F0;
  font-size: 0.85rem;
  color: #64748B;
}

.char-warning {
  color: #F59E0B;
  font-weight: 600;
}

.char-error {
  color: #DC2626;
  font-weight: 600;
}

.char-success {
  color: #10B981;
  font-weight: 600;
}

/* ========== INPUT STYLES ========== */
:deep(.va-input),
:deep(.va-input__field),
:deep(.va-textarea),
:deep(.va-textarea__textarea),
:deep(.va-select),
:deep(.va-date-input) {
  height: 32px !important;
  font-size: 0.85rem !important;
}

:deep(.va-input) {
  background: white !important;
  color: #1E293B !important;
}

:deep(.va-input__field) {
  height: 32px !important;
  padding: 0.4rem 0.7rem !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 5px !important;
  font-size: 0.85rem !important;
  background: white !important;
  color: #1E293B !important;
}

:deep(.va-input__field::placeholder) {
  font-size: 1rem !important;
  opacity: 1 !important;
}

:deep(.va-input__field:focus) {
  border-color: #7C3AED !important;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.1) !important;
}

:deep(.va-textarea) {
  height: auto !important;
  background: white !important;
  color: #1E293B !important;
}

:deep(.va-textarea__textarea) {
  height: 32px !important;
  padding: 0.4rem 0.7rem !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 5px !important;
  font-size: 0.85rem !important;
  background: white !important;
  color: #1E293B !important;
}

:deep(.va-select) {
  height: 32px !important;
  background: white !important;
  color: #1E293B !important;
}

:deep(.va-select__field) {
  height: 32px !important;
  padding: 0.4rem 0.7rem !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 5px !important;
  font-size: 0.85rem !important;
  display: flex !important;
  align-items: center !important;
  background: white !important;
  color: #1E293B !important;
}

:deep(.va-select__field:focus) {
  border-color: #7C3AED !important;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.1) !important;
}

/* Fix: Dropdown del select debe mostrar desde el inicio, no desde el final */
:deep(.va-select-dropdown) {
  scroll-behavior: auto !important;
}

:deep(.va-select-dropdown__content) {
  scroll-behavior: auto !important;
}

:deep(.va-dropdown__content) {
  max-height: 300px !important;
  overflow-y: auto !important;
}

/* Asegurar que cuando se abra el dropdown, inicie en la posición top */
:deep(.va-select-option-list) {
  scroll-behavior: auto !important;
}

:deep(.va-date-input) {
  height: 32px !important;
  background: white !important;
  color: #1E293B !important;
}

:deep(.va-date-input__field) {
  height: 32px !important;
  padding: 0.4rem 0.7rem !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 5px !important;
  font-size: 0.85rem !important;
  display: flex !important;
  align-items: center !important;
  background: white !important;
  color: #1E293B !important;
}

:deep(.va-date-input__field:focus) {
  border-color: #7C3AED !important;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.1) !important;
}

input[type="text"],
input[type="number"],
input[type="email"],
input[type="date"],
textarea {
  height: 32px !important;
  padding: 0.4rem 0.7rem !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 5px !important;
  font-size: 0.85rem !important;
  background: white !important;
  color: #1E293B !important;
}

/* ========== COMPENSATION & VACANCIES ========== */
.form-grid.compact-compensation-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.vacancy-input-group.compact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.vacancy-btn-sm {
  width: 36px;
  height: 36px;
  border: 1px solid #E2E8F0;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: #7C3AED;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.vacancy-btn-sm:hover:not(:disabled) {
  background: #F8FAFC;
  border-color: #7C3AED;
  box-shadow: 0 2px 4px rgba(124, 58, 237, 0.2);
}

.vacancy-btn-sm:disabled {
  color: #CBD5E1;
  cursor: not-allowed;
  border-color: #E2E8F0;
}

.vacancy-input-sm {
  width: 60px;
  padding: 0.5rem;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  text-align: center;
  font-weight: 600;
  color: #7C3AED;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.vacancy-input-sm:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.salary-type-compact {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: center;
}

.radio-label-compact {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9rem;
  cursor: pointer;
  font-weight: 500;
  color: #1E293B;
}

.radio-label-compact:hover {
  color: #7C3AED;
}

.salary-inputs-inline {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.form-field-inline {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.form-label-sm {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1E293B;
}

.separator {
  color: #7C3AED;
  font-weight: 600;
  padding-bottom: 0.5rem;
  line-height: 1;
}

/* ========== NAVIGATION BUTTONS ========== */
.navigation-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  margin-top: 2rem;
  border-top: 1px solid #E5E7EB;
}

.btn {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.3);
}

.btn-secondary {
  background: #F3F4F6;
  color: #1F2937;
  border: 2px solid #E5E7EB;
  font-weight: 600;
}

.btn-secondary:hover {
  background: #E5E7EB;
  border-color: #D1D5DB;
}

.opacity-50 {
  opacity: 0.5;
}

/* ========== ERROR MODAL ========== */
/* Asegurar que el modal de errores esté por encima de CKEditor */
:deep(.va-modal__overlay) {
  z-index: 10500 !important;
  background-color: rgba(0, 0, 0, 0.5) !important;
}

:deep(.va-modal__container) {
  z-index: 10500 !important;
}

:deep(.va-modal__dialog) {
  z-index: 10600 !important;
}

:deep(.va-modal__inner) {
  z-index: 10700 !important;
}

.error-modal-content {
  text-align: center;
  padding: 1.5rem 1rem;
}

.error-icon {
  margin-bottom: 1.5rem;
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

.error-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #DC2626;
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.error-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
  max-width: 500px;
  margin: 0 auto;
}

.error-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: rgba(220, 38, 38, 0.05);
  border-left: 3px solid #DC2626;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
  color: #1F2937;
  line-height: 1.5;
  animation: slideInLeft 0.3s ease backwards;
}

.error-item:nth-child(1) { animation-delay: 0.1s; }
.error-item:nth-child(2) { animation-delay: 0.2s; }
.error-item:nth-child(3) { animation-delay: 0.3s; }
.error-item:nth-child(4) { animation-delay: 0.4s; }
.error-item:nth-child(5) { animation-delay: 0.5s; }

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .information-step-job {
    padding: 1rem;
  }

  .integrated-header {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
    padding-bottom: 1rem;
  }

  .header-icon {
    width: 56px;
    height: 56px;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .step-subtitle {
    font-size: 0.95rem;
  }

  .form-content {
    padding: 1.5rem;
    gap: 1.25rem;
  }

  .form-section {
    padding: 1rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .form-grid.grid-3col {
    grid-template-columns: 1fr;
  }

  .navigation-buttons {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .information-step-job {
    padding: 0.75rem;
  }

  .header-icon {
    width: 48px;
    height: 48px;
  }

  .step-title {
    font-size: 1.25rem;
  }

  .form-content {
    padding: 1rem;
    gap: 1rem;
  }

  .form-label {
    font-size: 0.9rem;
  }

}

/* ========== MINI SWITCH CUSTOM (ESTILO TOPSEARCHBAR) ========== */
.anonymous-switch-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.35rem;
}

.custom-switch {
  position: relative;
  display: inline-block;
  width: 32px;
  height: 18px;
  cursor: pointer;
  flex-shrink: 0;
}

.switch-checkbox {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #CBD5E1;
  border-radius: 18px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.switch-slider::before {
  content: '';
  position: absolute;
  height: 14px;
  width: 14px;
  left: 2px;
  bottom: 2px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Estado ACTIVADO - Púrpura hermoso */
.switch-checkbox:checked + .switch-slider {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.4);
}

.switch-checkbox:checked + .switch-slider::before {
  transform: translateX(14px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
}

/* Hover */
.custom-switch:hover .switch-slider {
  background: #94A3B8;
}

.custom-switch:hover .switch-checkbox:checked + .switch-slider {
  background: linear-gradient(135deg, #6D28D9 0%, #9333EA 100%);
  box-shadow: 0 2px 10px rgba(124, 58, 237, 0.5);
}

/* Animación de pulso cuando se activa */
.switch-checkbox:checked + .switch-slider::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 18px;
  background: rgba(124, 58, 237, 0.3);
  animation: pulse-purple 0.6s ease-out;
}

@keyframes pulse-purple {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.4);
    opacity: 0;
  }
}

.switch-label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #64748B;
  user-select: none;
}

.switch-checkbox:checked ~ .switch-label {
  color: #7C3AED;
  font-weight: 600;
}
</style>