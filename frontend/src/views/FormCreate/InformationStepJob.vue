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
          <h2 class="step-title">Información del Trabajo</h2>
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
              <label class="form-label">Título *</label>
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
                <!-- ANÓNIMO (INLINE) -->
                <va-switch
                  v-model="localFormData.companyAnonymous"
                  label="Anónimo"
                  color="warning"
                  size="small"
                  style="margin-top: 0.35rem;"
                />
              </div>
            </div>
          </div>

          <!-- CATEGORÍA Y TIPO (GRID 2 COL) -->
          <div class="form-grid">
            <div class="form-row compact">
              <label class="form-label">Categoría *</label>
              <va-select
                v-model="localFormData.jobCategory"
                :options="categoryOptions"
                placeholder="Selecciona"
                :rules="[(v) => !!v || 'La categoría es requerida']"
                size="small"
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
          </div>

          <!-- CIUDAD, FECHA, PROVINCIA (GRID 3 COL) -->
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
              <label class="form-label">Fecha Vencimiento *</label>
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
          </div>
        </div>

        <!-- SEPARADOR VISUAL -->
        <div class="field-separator"></div>

        <!-- GRUPO 2: CKEDITOR WYSIWYG -->
        <div class="field-group">
          <div class="form-row">
            <label class="form-label">Detalles del Empleo *</label>
            <div class="editor-wrapper-ckeditor">
              <div ref="editorContainer" class="ckeditor-container"></div>
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
            Compensación y Vacantes
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

          <!-- BENEFICIOS (COMPACTO) -->
          <div class="form-row compact">
            <label class="form-label">Beneficios (Opcional)</label>
            <va-textarea
              v-model="localFormData.benefits"
              placeholder="Ej: Seguro de salud, bonos, capacitación..."
              :min-rows="2"
              counter
              maxlength="300"
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
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

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

const loadingCategories = ref(true)
const loadingContractTypes = ref(true)
const loadingCities = ref(true)

// ========== MODAL DE ERRORES ==========
const showErrorModal = ref(false)
const validationErrors = ref([])

// ========== INICIALIZAR CKEDITOR 5 ==========
const initCKEditor = () => {
  // Cargar CKEditor desde CDN - VERSIÓN SUPERBUILD con todos los plugins
  if (!window.ClassicEditor) {
    // Cargar CSS de CKEditor
    const link = document.createElement('link')
    link.href = 'https://cdn.ckeditor.com/ckeditor5/43.3.1/ckeditor5.css'
    link.rel = 'stylesheet'
    document.head.appendChild(link)
    
    // Cargar JS de CKEditor
    const script = document.createElement('script')
    script.src = 'https://cdn.ckeditor.com/ckeditor5/43.3.1/ckeditor5.umd.js'
    script.type = 'module'
    script.onload = () => {
      // Esperar a que se cargue completamente
      setTimeout(createEditor, 100)
    }
    document.head.appendChild(script)
  } else {
    createEditor()
  }
}

const createEditor = async () => {
  if (!editorContainer.value || editorInstance) return

  try {
    const {
      ClassicEditor,
      Essentials,
      Bold,
      Italic,
      Underline,
      Strikethrough,
      Paragraph,
      Heading,
      List,
      Link,
      BlockQuote,
      Indent,
      IndentBlock,
      Alignment,
      Font,
      Undo
    } = window.CKEDITOR

    const editor = await ClassicEditor.create(editorContainer.value, {
      plugins: [
        Essentials,
        Bold,
        Italic,
        Underline,
        Strikethrough,
        Paragraph,
        Heading,
        List,
        Link,
        BlockQuote,
        Indent,
        IndentBlock,
        Alignment,
        Font,
        Undo
      ],
      toolbar: {
        items: [
          'heading',
          '|',
          'fontSize',
          'fontFamily',
          'fontColor',
          'fontBackgroundColor',
          '|',
          'bold',
          'italic',
          'underline',
          'strikethrough',
          '|',
          'alignment',
          '|',
          'bulletedList',
          'numberedList',
          '|',
          'outdent',
          'indent',
          '|',
          'link',
          'blockQuote',
          '|',
          'undo',
          'redo'
        ],
        shouldNotGroupWhenFull: true
      },
      heading: {
        options: [
          { model: 'paragraph', title: 'Párrafo', class: 'ck-heading_paragraph' },
          { model: 'heading1', view: 'h1', title: 'Título 1', class: 'ck-heading_heading1' },
          { model: 'heading2', view: 'h2', title: 'Título 2', class: 'ck-heading_heading2' },
          { model: 'heading3', view: 'h3', title: 'Título 3', class: 'ck-heading_heading3' }
        ]
      },
      fontSize: {
        options: [
          'tiny',
          'small',
          'default',
          'big',
          'huge'
        ]
      },
      fontFamily: {
        options: [
          'default',
          'Arial, Helvetica, sans-serif',
          'Georgia, serif',
          'Courier New, Courier, monospace',
          'Times New Roman, Times, serif'
        ]
      },
      link: {
        defaultProtocol: 'https://',
        decorators: {
          openInNewTab: {
            mode: 'manual',
            label: 'Abrir en nueva pestaña',
            attributes: {
              target: '_blank',
              rel: 'noopener noreferrer'
            }
          }
        }
      },
      placeholder: 'Cuéntale al candidato sobre el puesto: Descripción del trabajo, Responsabilidades principales, Requisitos y habilidades necesarias, Experiencia requerida, Beneficios y oportunidades'
    })

    editorInstance = editor

    // Establecer contenido inicial
    if (localFormData.value.jobDetailsHtml) {
      editor.setData(localFormData.value.jobDetailsHtml)
    }

    // Actualizar contador y sincronizar cambios
    editor.model.document.on('change:data', () => {
      const data = editor.getData()
      const textContent = getTextFromHtml(data)
      charCount.value = textContent.length
      localFormData.value.jobDetailsHtml = data
    })

    // Calcular contador inicial
    const initialText = getTextFromHtml(editor.getData())
    charCount.value = initialText.length

    console.log('✅ CKEditor 5 Superbuild inicializado correctamente')
  } catch (error) {
    console.error('Error al inicializar CKEditor:', error)
    // Fallback al método anterior si falla
    initCKEditorClassic()
  }
}

// Fallback al método clásico
const initCKEditorClassic = () => {
  if (!editorContainer.value || editorInstance) return

  window.ClassicEditor
    .create(editorContainer.value, {
      placeholder: 'Cuéntale al candidato sobre el puesto: Descripción del trabajo, Responsabilidades principales, Requisitos y habilidades necesarias, Experiencia requerida, Beneficios y oportunidades',
      toolbar: [
        'heading', '|',
        'bold', 'italic', 'underline', '|',
        'bulletedList', 'numberedList', '|',
        'outdent', 'indent', '|',
        'link', 'blockQuote', '|',
        'undo', 'redo'
      ],
      heading: {
        options: [
          { model: 'paragraph', title: 'Párrafo', class: 'ck-heading_paragraph' },
          { model: 'heading2', view: 'h2', title: 'Título 2', class: 'ck-heading_heading2' },
          { model: 'heading3', view: 'h3', title: 'Título 3', class: 'ck-heading_heading3' }
        ]
      }
    })
    .then(editor => {
      editorInstance = editor

      if (localFormData.value.jobDetailsHtml) {
        editor.setData(localFormData.value.jobDetailsHtml)
      }

      editor.model.document.on('change:data', () => {
        const data = editor.getData()
        const textContent = getTextFromHtml(data)
        charCount.value = textContent.length
        localFormData.value.jobDetailsHtml = data
      })

      const initialText = getTextFromHtml(editor.getData())
      charCount.value = initialText.length

      console.log('✅ CKEditor 5 Classic (fallback) inicializado')
    })
    .catch(error => {
      console.error('Error al inicializar CKEditor Classic:', error)
    })
}

// Función para extraer texto plano del HTML
const getTextFromHtml = (html) => {
  const tmp = document.createElement('DIV')
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ''
}

// ========== WATCH PARA SINCRONIZACIÓN ==========
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
      if (editorInstance) {
        editorInstance.setData(description)
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
    const response = await fetch('http://localhost:8000/api/jobs/categories-dynamic')
    const data = await response.json()

    if (data.success && data.categories) {
      categoryOptions.value = data.categories
      console.log(`✅ ${data.count} categorías cargadas dinámicamente`)
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
      console.log(`✅ ${data.count} tipos de contrato cargados dinámicamente`)
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
      console.log(`✅ ${data.count} ciudades cargadas dinámicamente`)
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
  
  // Inicializar CKEditor
  initCKEditor()
})

onBeforeUnmount(() => {
  // Destruir instancia de CKEditor
  if (editorInstance) {
    editorInstance.destroy()
      .then(() => {
        console.log('✅ CKEditor destruido correctamente')
      })
      .catch(error => {
        console.error('Error al destruir CKEditor:', error)
      })
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

  console.log('✅ Validación exitosa - todos los campos obligatorios completos')
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
  position: relative;
}

.form-section::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #7C3AED 0%, #A855F7 100%);
  border-radius: 12px 0 0 12px;
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
  font-size: 0.9rem;
}

/* ========== CKEDITOR STYLES ========== */
.editor-wrapper-ckeditor {
  border: 2px solid #E2E8F0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
  background: white;
  position: relative;
  z-index: 1; /* Mantener bajo para no superponer navbar */
}

.editor-wrapper-ckeditor:focus-within {
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.ckeditor-container {
  min-height: 300px;
  position: relative;
  z-index: 1;
}

/* CKEditor 5 Toolbar Customization */
:deep(.ck-toolbar) {
  background: linear-gradient(135deg, #F9F5FF 0%, #F5EFFF 100%) !important;
  border-bottom: 2px solid #E9D5FF !important;
  padding: 0.75rem !important;
  border-top-left-radius: 6px !important;
  border-top-right-radius: 6px !important;
}

:deep(.ck-button) {
  border-radius: 6px !important;
  transition: all 0.2s !important;
}

:deep(.ck-button:hover) {
  background: #EDE9FE !important;
}

:deep(.ck-button.ck-on) {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%) !important;
  color: white !important;
}

:deep(.ck-toolbar__separator) {
  background: #E9D5FF !important;
}

/* CKEditor Content Area */
:deep(.ck-editor__editable) {
  min-height: 300px !important;
  max-height: 500px !important;
  padding: 1.5rem !important;
  font-size: 15px !important;
  line-height: 1.6 !important;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
  color: #334155 !important;
  border: none !important;
}

/* Placeholder visible y grande */
:deep(.ck-placeholder)::before {
  color: #9CA3AF !important;
  opacity: 0.8 !important;
  font-size: 15px !important;
}

:deep(.ck-editor__editable:focus) {
  box-shadow: none !important;
  border: none !important;
}

:deep(.ck-editor__editable p) {
  margin-bottom: 0.75rem;
}

:deep(.ck-editor__editable strong) {
  font-weight: 700;
  color: #1E293B;
}

:deep(.ck-editor__editable em) {
  font-style: italic;
}

:deep(.ck-editor__editable ul),
:deep(.ck-editor__editable ol) {
  margin-left: 1.5rem;
  margin-bottom: 0.75rem;
}

:deep(.ck-editor__editable li) {
  margin-bottom: 0.5rem;
}

:deep(.ck-editor__editable blockquote) {
  border-left: 4px solid #7C3AED;
  padding-left: 1rem;
  margin: 1rem 0;
  font-style: italic;
  color: #64748B;
}

:deep(.ck-editor__editable h1) {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #1E293B;
}

:deep(.ck-editor__editable h2) {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #1E293B;
}

:deep(.ck-editor__editable h3) {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #334155;
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
</style>