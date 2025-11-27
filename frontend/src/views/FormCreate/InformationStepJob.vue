<!--
  ==========================================
  INFORMATIONSTEPJOB.VUE - VERSIÓN SIMPLIFICADA
  ✨ Formulario limpio sin acordeones
  📝 Editor de texto rico para información del empleo
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

        <!-- GRUPO 2: EDITOR DE TEXTO RICO -->
        <div class="field-group">
          <div class="form-row">
            <label class="form-label">Detalles del Empleo *</label>
            <QuillEditor
              :key="quillKey"
              v-model="localFormData.jobDetailsHtml"
              content-type="html"
              theme="snow"
              :toolbar="quillToolbar"
              class="job-details-editor"
              placeholder="Describe el puesto, responsabilidades, requisitos, habilidades necesarias... ¡A tu gusto!"
            />
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
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

// ========== PROPS Y EMITS ==========
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])

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

// ========== QUILL KEY PARA REINICIALIZACIÓN ==========
const quillKey = ref(0)

// ========== QUILL EDITOR TOOLBAR ==========
const quillToolbar = [
  ['bold', 'italic', 'underline'],
  [{ 'header': [1, 2, 3, false] }],
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  ['blockquote'],
  ['clean']
]

// ========== OPCIONES DE FORMULARIO ==========
const categoryOptions = ref([])
const loadingCategories = ref(true)

const contractTypeOptions = [
  { text: 'Tiempo Completo', value: 'Tiempo Completo' },
  { text: 'Medio Tiempo', value: 'Medio Tiempo' },
  { text: 'Por Proyecto', value: 'Por Proyecto' },
  { text: 'Temporal', value: 'Temporal' },
  { text: 'Pasantía', value: 'Pasantía' },
  { text: 'Freelance', value: 'Freelance' }
]

const cityOptions = [
  { text: 'Cochabamba', value: 'Cochabamba' },
  { text: 'La Paz', value: 'La Paz' },
  { text: 'Santa Cruz', value: 'Santa Cruz' },
  { text: 'Sucre', value: 'Sucre' },
  { text: 'Tarija', value: 'Tarija' },
  { text: 'Potosí', value: 'Potosí' },
  { text: 'Oruro', value: 'Oruro' },
  { text: 'Beni', value: 'Beni' },
  { text: 'Pando', value: 'Pando' }
]

// ========== WATCH PARA SINCRONIZACIÓN ==========
// Watch para cambios internos del formulario - emite actualizaciones al parent
watch(localFormData, (newValue) => {
  const cleanedValue = {
    ...props.modelValue,
    ...newValue,
    description: newValue.jobDetailsHtml, // Mapear editor HTML a description
    jobCategory: typeof newValue.jobCategory === 'object' ? newValue.jobCategory?.value : newValue.jobCategory,
    city: typeof newValue.city === 'object' ? newValue.city?.value : newValue.city,
    contractType: typeof newValue.contractType === 'object' ? newValue.contractType?.value : newValue.contractType
  }
  emit('update:modelValue', cleanedValue)
}, { deep: true })

// Watch para sincronizar cuando vuelves atrás - carga datos guardados
watch(() => [props.modelValue.description, props.modelValue.title, props.modelValue.jobDetailsHtml],
  (newVals) => {
    const [description] = newVals
    // Si el description del store cambió pero jobDetailsHtml local no coincide, recargar
    if (description && description !== localFormData.value.jobDetailsHtml) {
      localFormData.value = initializeFormData(props.modelValue)
      quillKey.value++ // Forzar reinicialización del Quill
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

// ========== CARGAR CATEGORÍAS DEL API ==========
const loadJobCategories = async () => {
  try {
    loadingCategories.value = true
    const response = await fetch('http://localhost:8000/api/jobs/categories')
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

onMounted(() => {
  loadJobCategories()
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
// Función auxiliar para extraer texto sin HTML
const stripHtmlTags = (html) => {
  if (!html) return ''
  // Crear elemento temporal para extraer texto
  const temp = document.createElement('div')
  temp.innerHTML = html
  // Obtener solo el texto, eliminando tags pero respetando espacios
  return temp.textContent || temp.innerText || ''
}

// Función auxiliar para contar caracteres sin espacios excesivos
const cleanTextLength = (html) => {
  const text = stripHtmlTags(html)
  // Eliminar espacios en blanco al inicio/final y espacios múltiples
  return text.trim().replace(/\s+/g, ' ').length
}

const validate = () => {
  const errors = []

  if (!localFormData.value.title) {
    errors.push('El título del puesto es requerido')
  }

  if (!localFormData.value.companyAnonymous && !localFormData.value.companyName) {
    errors.push('El nombre de la empresa es requerido (o marca como anónima)')
  }

  // Validar contenido del Quill editor (contar solo texto real, sin HTML)
  const jobDetailsLength = cleanTextLength(localFormData.value.jobDetailsHtml)
  if (!localFormData.value.jobDetailsHtml || jobDetailsLength < 50) {
    errors.push(`La información del empleo debe tener al menos 50 caracteres (actualmente: ${jobDetailsLength})`)
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
    const errorMessage = errors.join('\n• ')
    alert(`⚠️ Por favor completa los siguientes campos:\n\n• ${errorMessage}`)
    return false
  }

  console.log('✅ Validación exitosa - todos los campos obligatorios completo')
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
}

.step-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2.5rem;
  max-width: 1160px;
  margin-left: auto;
  margin-right: auto;
  padding: 2.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(124, 58, 237, 0.15);
  border-top: 4px solid transparent;
  background-image:
    linear-gradient(white, white),
    linear-gradient(90deg, #7C3AED, #A855F7);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  width: 100%;
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

.integrated-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #E9D5FF;
  margin-bottom: 1rem;
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

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: #1E293B;
  margin: 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #E9D5FF;
}

.section-title va-icon {
  color: #7C3AED;
  font-size: 1.5rem;
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

.form-row-flex {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
  margin-bottom: 0.3rem;
}

.form-row-flex.compact {
  gap: 0.5rem;
}

.anonymous-inline-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 0.15rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.form-grid.compact-grid {
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.form-grid.grid-3col {
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

/* ========== UNIFIED JOB SECTION STYLES ========== */
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

.group-subtitle va-icon {
  color: #7C3AED;
}

.basic-info-section {
  gap: 0.75rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-label {
  font-weight: 600;
  color: #1E293B;
  font-size: 0.9rem;
}

/* ========== INPUT UNIFORMITY - ALL INPUTS IDENTICAL ========== */
/* Base sizing for all input elements */
:deep(.va-input),
:deep(.va-input__field),
:deep(.va-textarea),
:deep(.va-textarea__textarea),
:deep(.va-select),
:deep(.va-date-input) {
  height: 32px !important;
  font-size: 0.85rem !important;
}

/* VA-INPUT styling */
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

:deep(.va-input__field) {
  --va-font-size: 1rem !important;
}

:deep(.va-input__field:focus) {
  border-color: #7C3AED !important;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.1) !important;
}

/* VA-TEXTAREA styling */
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

:deep(.va-textarea__textarea::placeholder) {
  font-size: 1rem !important;
  opacity: 1 !important;
}

:deep(.va-textarea__textarea) {
  --va-font-size: 1rem !important;
}

/* VA-SELECT styling */
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

/* Select placeholder text - make it larger and visible */
:deep(.va-select__placeholder) {
  font-size: 1rem !important;
  opacity: 1 !important;
  --va-font-size: 1rem !important;
}

:deep(.va-select__field .va-select__placeholder) {
  font-size: 1rem !important;
  --va-font-size: 1rem !important;
}

/* Select option text */
:deep(.va-select__content) {
  font-size: 0.85rem !important;
}

:deep(.va-select__option) {
  font-size: 0.85rem !important;
}

/* VA-DATE-INPUT styling */
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

:deep(.va-date-input__field::placeholder) {
  font-size: 0.9rem !important;
  opacity: 1 !important;
}

/* Generic input and textarea fallback */
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

input::placeholder,
textarea::placeholder {
  font-size: 1rem !important;
  opacity: 1 !important;
}

/* Additional Vuestic input element targeting */
:deep(.va-input input),
:deep(.va-textarea textarea),
:deep(.va-select select),
:deep(.va-date-input input) {
  background: white !important;
  color: #1E293B !important;
}

/* Target all wrapper containers */
:deep(.va-input__container),
:deep(.va-textarea__container),
:deep(.va-select__container),
:deep(.va-date-input__container) {
  background: white !important;
  color: #1E293B !important;
}

/* ========== VALIDATION ERROR MESSAGES ========== */
:deep(.va-input__error-messages),
:deep(.va-select__error-messages),
:deep(.va-textarea__error-messages),
:deep(.va-date-input__error-messages) {
  font-size: 0.75rem !important;
  color: #DC2626 !important;
  margin-top: 0.35rem !important;
  margin-bottom: 0 !important;
  padding: 0 !important;
  line-height: 1.2 !important;
  display: block !important;
  word-wrap: break-word !important;
}

:deep(.va-input__error-message),
:deep(.va-select__error-message),
:deep(.va-textarea__error-message),
:deep(.va-date-input__error-message) {
  font-size: 0.75rem !important;
  color: #DC2626 !important;
}

.input-hint {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.9rem;
  color: #5B21B6;
  padding: 0.75rem 1rem;
  background: #F9F5FF;
  border-radius: 8px;
  border-left: 3px solid #7C3AED;
  line-height: 1.5;
  margin-top: 0.4rem;
}

.input-hint.compact-hint {
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
  margin-top: 0.2rem;
}

.success-hint {
  background: #F0FDF4;
  color: #166534;
  border-left-color: #16A34A;
}

.anonymous-switch-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: #F5F3FF;
  border-radius: 8px;
  border-left: 3px solid #DDD6FE;
}

.anonymous-switch-container.compact {
  padding: 0.5rem;
  gap: 0.25rem;
  background: transparent;
  border: none;
}

.anonymous-helper-text {
  font-size: 0.85rem;
  color: #5B21B6;
  font-weight: 500;
}

.currency-symbol {
  font-weight: 700;
  color: #7C3AED;
  padding: 0.5rem 0.75rem;
  background: #E0E7FF;
  border-radius: 6px;
  font-size: 0.9rem;
}

.salary-tip {
  display: flex;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: #FFFBEB;
  border-left: 3px solid #FBBF24;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #92400E;
  line-height: 1.5;
  align-items: flex-start;
}

.salary-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  margin-bottom: 1rem;
}

.salary-radio {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  font-weight: 500;
  color: #1E293B;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background 0.2s;
}

.salary-radio:hover {
  background: #F1F5F9;
}

.salary-inputs {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
}

.salary-separator {
  font-size: 1.5rem;
  font-weight: 700;
  color: #7C3AED;
  padding-bottom: 0.5rem;
}

.vacancy-input-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.vacancy-btn {
  width: 44px;
  height: 44px;
  border: 2px solid #E2E8F0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  color: #7C3AED;
  font-size: 1.25rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.vacancy-btn:hover:not(:disabled) {
  background: #F8FAFC;
  border-color: #7C3AED;
  box-shadow: 0 2px 4px rgba(124, 58, 237, 0.2);
}

.vacancy-btn:disabled {
  color: #CBD5E1;
  cursor: not-allowed;
  border-color: #E2E8F0;
}

.vacancy-input {
  width: 100px;
  padding: 0.75rem;
  border: 2px solid #E2E8F0;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 700;
  text-align: center;
  color: #7C3AED;
  transition: all 0.2s;
}

.vacancy-input:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

/* ========== QUILL EDITOR STYLES - DOCUMENT STYLE ========== */
.job-details-editor {
  background: white;
  border: none;
  border-radius: 12px;
  min-height: 280px;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.12);
  overflow: hidden;
}

:deep(.ql-toolbar) {
  background: linear-gradient(135deg, #F8FAFC 0%, #F5F3FF 100%);
  border: none;
  border-bottom: 1px solid #E9D5FF;
  border-radius: 12px 12px 0 0;
  padding: 0.75rem 1rem;
}

:deep(.ql-toolbar.ql-snow) {
  padding: 0.75rem 1rem;
}

:deep(.ql-toolbar button) {
  color: #7C3AED;
}

:deep(.ql-toolbar button:hover) {
  color: #A855F7;
}

:deep(.ql-container) {
  border: none;
  border-radius: 0 0 12px 12px;
  font-size: 0.95rem;
  background: white;
}

:deep(.ql-editor) {
  min-height: 240px;
  padding: 2rem 1.5rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #334155;
}

:deep(.ql-editor.ql-blank::before) {
  color: #CBD5E1;
  font-style: italic;
  font-size: 0.95rem;
}

:deep(.ql-editor h1) {
  font-size: 1.75rem;
  margin: 0.5rem 0;
}

:deep(.ql-editor h2) {
  font-size: 1.5rem;
  margin: 0.5rem 0;
}

:deep(.ql-editor h3) {
  font-size: 1.25rem;
  margin: 0.4rem 0;
}

:deep(.ql-editor p) {
  margin: 0.5rem 0;
}

:deep(.ql-editor ul, .ql-editor ol) {
  margin: 0.5rem 0 0.5rem 2rem;
}

:deep(.ql-editor li) {
  margin: 0.25rem 0;
}

/* ========== BOTONES DE NAVEGACIÓN ========== */
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

/* ========== COMPENSATION & VACANCIES COMPACT STYLES ========== */

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

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .information-step-job {
    padding: 1rem;
  }

  .step-header {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
    padding: 1.5rem;
    margin-bottom: 1rem;
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

  .section-title {
    font-size: 1rem;
  }

  .salary-inputs {
    flex-direction: column;
  }

  .salary-separator {
    display: none;
  }

  .navigation-buttons {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  :deep(.ql-editor) {
    min-height: 200px;
  }
}

@media (max-width: 480px) {
  .information-step-job {
    padding: 0.75rem;
  }

  .step-header {
    padding: 1rem;
    gap: 0.5rem;
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

  .section-title {
    font-size: 0.95rem;
  }

  .form-label {
    font-size: 0.9rem;
  }

  :deep(.ql-editor) {
    min-height: 150px;
    padding: 0.75rem;
  }
}
</style>
