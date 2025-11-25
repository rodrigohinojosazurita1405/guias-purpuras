<!-- 
  ==========================================
  INFORMATIONSTEPJOB.VUE
  ✅ VERSIÓN CORREGIDA - PATRÓN CONSISTENTE
  ==========================================
-->
<template>
  <div class="information-step-job">

    <!-- HEADER -->
    <div class="step-header">
      <div class="header-icon">
        <va-icon name="work" size="2rem" color="#FFFFFF" />
      </div>
      <div>
        <h2 class="step-title">Información del Trabajo</h2>
        <p class="step-subtitle">
          Completa los datos de la oferta laboral - Expande las secciones según sea necesario
        </p>
      </div>
    </div>

    <!-- FORMULARIO CON ACORDEONES -->
    <div class="form-content">

      <!-- ACORDEÓN 1: INFORMACIÓN BÁSICA -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.basicInfo }">
        <div class="accordion-header" @click="toggleSection('basicInfo')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="info" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Información Básica del Puesto</h3>
              <p v-if="!expandedSections.basicInfo" class="accordion-summary">
                {{ getSummary('basicInfo') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.basicInfo ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.basicInfo" class="accordion-content">

          <!-- TÍTULO DEL PUESTO -->
        <div class="form-row">
          <va-input
            v-model="localFormData.title"
            label="Título del Puesto"
            placeholder="Ej: Técnico(a) Comercial Agrónomo(a)"
            required-mark
            counter
            maxlength="100"
            :rules="[
              (v) => !!v || 'El título es requerido',
              (v) => (v && v.length >= 5) || 'Mínimo 5 caracteres'
            ]"
          >
            <template #prepend>
              <va-icon name="title" color="purple" />
            </template>
          </va-input>
          
          <div class="input-hint success-hint" style="margin-top: 0.75rem;">
            <va-icon name="info" size="small" />
            <span>Títulos claros reciben más postulaciones</span>
          </div>
        </div>

        <div class="form-grid">
          <!-- NOMBRE DE LA EMPRESA -->
          <div class="form-row">
            <va-input
              v-model="localFormData.companyName"
              label="Nombre de la Empresa"
              placeholder="Ej: Agropartners S.R.L."
              :required-mark="!localFormData.companyAnonymous"
              :disabled="localFormData.companyAnonymous"
              :rules="[
                (v) => localFormData.companyAnonymous || !!v || 'El nombre de la empresa es requerido'
              ]"
            >
              <template #prepend>
                <va-icon name="business" color="purple" />
              </template>
            </va-input>
            
            <!-- CHECKBOX ANÓNIMO -->
            <div class="anonymous-checkbox">
              <va-switch
                v-model="localFormData.companyAnonymous"
                label="Publicar de forma anónima"
                color="warning"
                size="small"
              />
              <div class="input-hint" style="margin-top: 0.75rem;">
                <va-icon name="privacy_tip" size="small" />
                <span>Se mostrará como empresa confidencial sin logo ni nombre</span>
              </div>
            </div>
          </div>

        </div>

        <!-- DESCRIPCIÓN DEL TRABAJO -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.description"
            label="Descripción del Trabajo"
            placeholder="Describe el puesto, responsabilidades, y qué hace especial trabajar en tu empresa..."
            :min-rows="6"
            counter
            maxlength="1000"
            required-mark
            :rules="[
              (v) => !!v || 'La descripción es requerida',
              (v) => (v && v.length >= 50) || 'Mínimo 50 caracteres para una buena descripción'
            ]"
          >
            <template #prepend>
              <va-icon name="description" color="purple" />
            </template>
          </va-textarea>
          
          <div class="input-hint" style="margin-top: 0.75rem;">
            <va-icon name="info" size="small" />
            <span>Descripciones detalladas atraen candidatos de mejor calidad</span>
          </div>
        </div>

        <div class="form-grid">
          <!-- CATEGORÍA -->
          <div class="form-row">
            <va-select
              v-model="localFormData.jobCategory"
              label="Categoría/Área"
              :options="categoryOptions"
              placeholder="Selecciona una categoría"
              required-mark
              :rules="[(v) => !!v || 'La categoría es requerida']"
            >
              <template #prepend>
                <va-icon name="category" color="purple" />
              </template>
            </va-select>
          </div>

          <!-- CIUDAD -->
          <div class="form-row">
            <va-select
              v-model="localFormData.city"
              label="Ciudad"
              :options="cityOptions"
              placeholder="Selecciona la ciudad"
              required-mark
              :rules="[(v) => !!v || 'La ciudad es requerida']"
            >
              <template #prepend>
                <va-icon name="location_city" color="purple" />
              </template>
            </va-select>
          </div>
        </div>

        <div class="form-grid">
          <!-- TIPO DE CONTRATO -->
          <div class="form-row">
            <va-select
              v-model="localFormData.contractType"
              label="Tipo de Contrato"
              :options="contractTypeOptions"
              placeholder="Selecciona el tipo"
              required-mark
              :rules="[(v) => !!v || 'El tipo de contrato es requerido']"
            >
              <template #prepend>
                <va-icon name="schedule" color="purple" />
              </template>
            </va-select>
          </div>
        </div>

        <!-- FECHA DE VENCIMIENTO -->
        <div class="form-row">
          <va-date-input
            v-model="localFormData.expiryDate"
            label="Fecha de Vencimiento"
            placeholder="Selecciona fecha"
            required-mark
            :rules="[(v) => !!v || 'La fecha de vencimiento es requerida']"
          >
            <template #prepend>
              <va-icon name="event" color="purple" />
            </template>
          </va-date-input>
          
          <div class="input-hint">
            <va-icon name="calendar_today" size="small" />
            <span>Fecha límite para recibir postulaciones</span>
          </div>
        </div>
        </div>
      </div>

      <!-- ACORDEÓN 2: REQUISITOS Y RESPONSABILIDADES -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.requisites }">
        <div class="accordion-header" @click="toggleSection('requisites')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="assignment" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Requisitos y Responsabilidades</h3>
              <p v-if="!expandedSections.requisites" class="accordion-summary">
                {{ getSummary('requisites') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.requisites ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.requisites" class="accordion-content">

          <!-- REQUISITOS DEL PUESTO -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.requirements"
            label="Requisitos del Puesto"
            placeholder="Ej: - Título universitario en Agronomía&#10;- 2+ años de experiencia en ventas&#10;- Licencia de conducir&#10;- Disponibilidad para viajar"
            :min-rows="6"
            counter
            maxlength="1000"
            required-mark
            :rules="[(v) => !!v || 'Los requisitos son requeridos']"
          >
            <template #prepend>
              <va-icon name="checklist" color="purple" />
            </template>
          </va-textarea>
        </div>

        <!-- FUNCIONES PRINCIPALES -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.responsibilities"
            label="Funciones Principales (Opcional)"
            placeholder="Describe las responsabilidades diarias del puesto..."
            :min-rows="4"
            counter
            maxlength="800"
          >
            <template #prepend>
              <va-icon name="work_outline" color="purple" />
            </template>
          </va-textarea>
        </div>

        <div class="form-grid">
          <!-- FORMACIÓN REQUERIDA -->
          <div class="form-row">
            <va-input
              v-model="localFormData.education"
              label="Formación Requerida"
              placeholder="Ej: Título en Agronomía"
            >
              <template #prepend>
                <va-icon name="school" color="purple" />
              </template>
            </va-input>
          </div>

          <!-- EXPERIENCIA NECESARIA -->
          <div class="form-row">
            <va-input
              v-model="localFormData.experience"
              label="Experiencia Necesaria"
              placeholder="Ej: 2-3 años en ventas"
            >
              <template #prepend>
                <va-icon name="badge" color="purple" />
              </template>
            </va-input>
          </div>
        </div>

        <div class="form-grid">
          <!-- IDIOMAS -->
          <div class="form-row">
            <va-input
              v-model="localFormData.languages"
              label="Idiomas Requeridos"
              placeholder="Ej: Español (nativo), Inglés (intermedio)"
            >
              <template #prepend>
                <va-icon name="language" color="purple" />
              </template>
            </va-input>
          </div>

          <!-- HABILIDADES TÉCNICAS -->
          <div class="form-row">
            <va-input
              v-model="localFormData.technicalSkills"
              label="Habilidades Técnicas"
              placeholder="Ej: Excel avanzado, CRM"
            >
              <template #prepend>
                <va-icon name="build" color="purple" />
              </template>
            </va-input>
          </div>
        </div>
        </div>
      </div>

      <!-- ACORDEÓN 3: INFORMACIÓN SALARIAL -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.salary }">
        <div class="accordion-header" @click="toggleSection('salary')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="attach_money" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Compensación y Beneficios</h3>
              <p v-if="!expandedSections.salary" class="accordion-summary">
                {{ getSummary('salary') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.salary ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.salary" class="accordion-content">

          <div class="salary-tip">
          <va-icon name="lightbulb" color="warning" />
          <div>
            <strong>Consejo:</strong> Publicaciones con salario visible reciben más postulaciones y candidatos de mejor calidad
          </div>
        </div>

        <div class="salary-options">
          <va-radio
            v-model="localFormData.salaryType"
            option="range"
            label="Rango salarial específico"
          />
          <va-radio
            v-model="localFormData.salaryType"
            option="fixed"
            label="Salario fijo"
          />
          <va-radio
            v-model="localFormData.salaryType"
            option="negotiable"
            label="A convenir"
          />
          <va-radio
            v-model="localFormData.salaryType"
            option="hidden"
            label="No mostrar salario"
          />
        </div>

        <!-- SALARIO - RANGO -->
        <div v-if="localFormData.salaryType === 'range'" class="form-row">
          <div class="salary-inputs">
            <div class="form-field">
              <va-input
                v-model.number="localFormData.salaryMin"
                label="Salario Mínimo (Bs.)"
                type="number"
                placeholder="Ej: 3000"
                required-mark
                :rules="[(v) => !!v || 'El salario mínimo es requerido']"
              >
                <template #prepend>
                  <span class="currency-symbol">Bs.</span>
                </template>
              </va-input>
            </div>
            <span class="salary-separator">-</span>
            <div class="form-field">
              <va-input
                v-model.number="localFormData.salaryMax"
                label="Salario Máximo (Bs.)"
                type="number"
                placeholder="Ej: 5000"
                required-mark
                :rules="[
                  (v) => !!v || 'El salario máximo es requerido',
                  (v) => !localFormData.salaryMin || v > localFormData.salaryMin || 'El máximo debe ser mayor al mínimo'
                ]"
              >
                <template #prepend>
                  <span class="currency-symbol">Bs.</span>
                </template>
              </va-input>
            </div>
          </div>
        </div>

        <!-- SALARIO - FIJO -->
        <div v-if="localFormData.salaryType === 'fixed'" class="form-row">
          <va-input
            v-model.number="localFormData.salaryFixed"
            label="Salario (Bs.)"
            type="number"
            placeholder="Ej: 4000"
            required-mark
            :rules="[(v) => !!v || 'El salario es requerido']"
          >
            <template #prepend>
              <span class="currency-symbol">Bs.</span>
            </template>
          </va-input>
        </div>

        <!-- BENEFICIOS ADICIONALES -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.benefits"
            label="Beneficios Adicionales (Opcional)"
            placeholder="Ej: Seguro de salud, bonos trimestrales, capacitación pagada, descuentos en productos..."
            :min-rows="3"
            counter
            maxlength="500"
          >
            <template #prepend>
              <va-icon name="card_giftcard" color="purple" />
            </template>
          </va-textarea>
          
          <div class="input-hint success-hint">
            <va-icon name="trending_up" size="small" />
            <span>Incrementa el atractivo de tu oferta mencionando beneficios extra</span>
          </div>
        </div>
        </div>
      </div>

      <!-- ACORDEÓN 4: NÚMERO DE VACANTES -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.vacancies }">
        <div class="accordion-header" @click="toggleSection('vacancies')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="people" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Número de Vacantes</h3>
              <p v-if="!expandedSections.vacancies" class="accordion-summary">
                {{ getSummary('vacancies') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.vacancies ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.vacancies" class="accordion-content">

          <div class="form-row">
          <label class="form-label">¿Cuántos puestos disponibles? *</label>
          <div class="vacancy-input-group">
            <button
              type="button"
              class="vacancy-btn"
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
              class="vacancy-input"
              @input="(e) => updateVacancies(parseInt(e.target.value) || 1)"
            />
            <button
              type="button"
              class="vacancy-btn"
              @click="incrementVacancies"
              :disabled="localFormData.vacancies >= 100"
            >
              +
            </button>
          </div>
          <small class="form-hint">
            Puedes publicar{{ localFormData.vacancies > 1 ? ` ${localFormData.vacancies} puestos iguales` : ' 1 puesto' }}
          </small>
        </div>

        <!-- Visualización de vacantes -->
        <div class="vacancy-tracker">
          <div
            v-for="n in Math.min(localFormData.vacancies, 10)"
            :key="n"
            class="vacancy-icon"
            :title="`Vacante ${n}`"
          >
            <va-icon name="person" />
          </div>
          <div v-if="localFormData.vacancies > 10" class="vacancy-more">
            +{{ localFormData.vacancies - 10 }} más
          </div>
        </div>
        </div>
      </div>

      <!-- ACORDEÓN 5: INFORMACIÓN DE CONTACTO -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.contact }">
        <div class="accordion-header" @click="toggleSection('contact')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="contact_phone" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Información de Contacto</h3>
              <p v-if="!expandedSections.contact" class="accordion-summary">
                {{ getSummary('contact') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.contact ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.contact" class="accordion-content">

          <div class="form-grid">
          <!-- EMAIL -->
          <div class="form-row">
            <va-input
              v-model="localFormData.email"
              label="Email de Contacto"
              placeholder="rrhh@empresa.com"
              type="email"
              required-mark
              :rules="[
                (v) => !!v || 'El email es requerido',
                (v) => /.+@.+\..+/.test(v) || 'El email no es válido'
              ]"
            >
              <template #prepend>
                <va-icon name="email" color="purple" />
              </template>
            </va-input>
            
            <div class="input-hint">
              <va-icon name="mail" size="small" />
              <span>Los postulantes enviarán sus CVs a este correo</span>
            </div>
          </div>

          <!-- WHATSAPP -->
          <div class="form-row">
            <va-input
              v-model="localFormData.whatsapp"
              label="WhatsApp"
              placeholder="70123456"
              required-mark
              :rules="[
                (v) => !!v || 'WhatsApp es obligatorio',
                (v) => /^[67]\d{7}$/.test(v) || 'Número inválido (debe empezar con 6 o 7 y tener 8 dígitos)'
              ]"
            >
              <template #prepend>
                <span class="whatsapp-prefix">+591</span>
              </template>
              <template #append>
                <va-icon name="whatsapp" color="success" />
              </template>
            </va-input>
          </div>

          <!-- SITIO WEB -->
          <div class="form-row">
            <va-input
              v-model="localFormData.website"
              label="Sitio Web (Opcional)"
              placeholder="https://www.empresa.com"
              type="url"
              :rules="[
                (v) => !v || v.startsWith('http://') || v.startsWith('https://') || 'Debe empezar con http:// o https://'
              ]"
            >
              <template #prepend>
                <va-icon name="language" color="purple" />
              </template>
            </va-input>
          </div>
        </div>

        <!-- INSTRUCCIONES DE APLICACIÓN -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.applicationInstructions"
            label="Instrucciones Especiales para Postular (Opcional)"
            placeholder="Ej: Enviar CV y carta de presentación. Incluir pretensión salarial. Indicar disponibilidad de inicio..."
            :min-rows="3"
            counter
            maxlength="300"
          >
            <template #prepend>
              <va-icon name="description" color="purple" />
            </template>
          </va-textarea>
          
          <div class="input-hint">
            <va-icon name="assignment" size="small" />
            <span>Agrega requisitos específicos para el proceso de aplicación</span>
          </div>
        </div>
        </div>
      </div>

      <!-- BOTONES DE NAVEGACIÓN -->
      <div class="navigation-buttons">
        <va-button
          preset="secondary"
          icon="arrow_back"
          @click="handleBack"
        >
          Atrás
        </va-button>

        <va-button
          preset="primary"
          icon="arrow_forward"
          @click="handleNext"
          class="next-button"
        >
          Siguiente
        </va-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// ========== PROPS Y EMITS ==========
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])

// ========== ACCORDION STATE ==========
const expandedSections = ref({
  basicInfo: true,
  requisites: false,
  salary: false,
  vacancies: false,
  contact: false
})

// ========== DATA LOCAL (REF + WATCH) ==========
const localFormData = ref({
  title: props.modelValue.title || '',
  companyName: props.modelValue.companyName || '',
  companyAnonymous: props.modelValue.companyAnonymous || false,
  description: props.modelValue.description || '',
  jobCategory: props.modelValue.jobCategory || '',
  city: props.modelValue.city || '',
  contractType: props.modelValue.contractType || '',
  expiryDate: props.modelValue.expiryDate || null,
  requirements: props.modelValue.requirements || '',
  responsibilities: props.modelValue.responsibilities || '',
  education: props.modelValue.education || '',
  experience: props.modelValue.experience || '',
  languages: props.modelValue.languages || '',
  technicalSkills: props.modelValue.technicalSkills || '',
  salaryType: props.modelValue.salaryType || 'range',
  salaryMin: props.modelValue.salaryMin || null,
  salaryMax: props.modelValue.salaryMax || null,
  salaryFixed: props.modelValue.salaryFixed || null,
  benefits: props.modelValue.benefits || '',
  vacancies: props.modelValue.vacancies || 1,
  email: props.modelValue.email || '',
  whatsapp: props.modelValue.whatsapp || '',
  website: props.modelValue.website || '',
  applicationInstructions: props.modelValue.applicationInstructions || ''
})

// ========== OPCIONES DE FORMULARIO ==========
const categoryOptions = [
  { text: 'Administración', value: 'Administración' },
  { text: 'Agronomía y Veterinaria', value: 'Agronomía y Veterinaria' },
  { text: 'Comercial y Ventas', value: 'Comercial y Ventas' },
  { text: 'Construcción', value: 'Construcción' },
  { text: 'Educación', value: 'Educación' },
  { text: 'Ingeniería', value: 'Ingeniería' },
  { text: 'Legal', value: 'Legal' },
  { text: 'Marketing y Publicidad', value: 'Marketing y Publicidad' },
  { text: 'Salud', value: 'Salud' },
  { text: 'Tecnología e Informática', value: 'Tecnología e Informática' },
  { text: 'Turismo y Hostelería', value: 'Turismo y Hostelería' },
  { text: 'Otro', value: 'Otro' }
]

const contractTypeOptions = [
  { text: 'Tiempo Completo', value: 'Tiempo Completo' },
  { text: 'Medio Tiempo', value: 'Medio Tiempo' },
  { text: 'Por Proyecto', value: 'Por Proyecto' },
  { text: 'Temporal', value: 'Temporal' },
  { text: 'Pasantía', value: 'Pasantía' },
  { text: 'Freelance', value: 'Freelance' }
]

const questionTypeOptions = [
  { text: 'Texto corto', value: 'text' },
  { text: 'Sí / No', value: 'yesno' },
  { text: 'Opción múltiple', value: 'multiple' }
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
watch(localFormData, (newValue) => {
  // Extraer solo los valores de los selects (en caso de que sean objetos)
  const cleanedValue = {
    ...props.modelValue,
    ...newValue,
    jobCategory: typeof newValue.jobCategory === 'object' ? newValue.jobCategory?.value : newValue.jobCategory,
    city: typeof newValue.city === 'object' ? newValue.city?.value : newValue.city,
    contractType: typeof newValue.contractType === 'object' ? newValue.contractType?.value : newValue.contractType
  }
  emit('update:modelValue', cleanedValue)
}, { deep: true })

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

// ========== ACCORDION METHODS ==========
const toggleSection = (sectionName) => {
  expandedSections.value[sectionName] = !expandedSections.value[sectionName]
}

const getSummary = (sectionName) => {
  switch (sectionName) {
    case 'basicInfo':
      if (localFormData.value.title && localFormData.value.city) {
        return `${localFormData.value.title} - ${localFormData.value.city}`
      }
      return 'Completa los datos básicos del puesto'

    case 'requisites':
      if (localFormData.value.requirements) {
        return 'Requisitos definidos'
      }
      return 'Define los requisitos y responsabilidades'

    case 'salary':
      if (localFormData.value.salaryType === 'range' && localFormData.value.salaryMin) {
        return `Bs. ${localFormData.value.salaryMin} - ${localFormData.value.salaryMax || '...'}`
      } else if (localFormData.value.salaryType === 'fixed' && localFormData.value.salaryFixed) {
        return `Bs. ${localFormData.value.salaryFixed}`
      } else if (localFormData.value.salaryType === 'negotiable') {
        return 'Salario a convenir'
      } else if (localFormData.value.salaryType === 'hidden') {
        return 'Salario no visible'
      }
      return 'Configura la compensación'

    case 'vacancies':
      return `${localFormData.value.vacancies || 1} ${localFormData.value.vacancies === 1 ? 'vacante' : 'vacantes'} disponible${localFormData.value.vacancies === 1 ? '' : 's'}`

    case 'contact':
      if (localFormData.value.email && localFormData.value.whatsapp) {
        return `${localFormData.value.email} - +591 ${localFormData.value.whatsapp}`
      }
      return 'Agrega información de contacto'

    default:
      return ''
  }
}

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
  
  // Validar empresa solo si NO es anónima
  if (!localFormData.value.companyAnonymous && !localFormData.value.companyName) {
    errors.push('El nombre de la empresa es requerido (o marca como anónima)')
  }
  
  if (!localFormData.value.description || localFormData.value.description.length < 50) {
    errors.push('La descripción debe tener al menos 50 caracteres')
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
  
  if (!localFormData.value.requirements) {
    errors.push('Los requisitos son requeridos')
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
  
  if (!localFormData.value.email) {
    errors.push('El email de contacto es requerido')
  } else if (!/.+@.+\..+/.test(localFormData.value.email)) {
    errors.push('El email no es válido')
  }
  
  if (!localFormData.value.whatsapp) {
    errors.push('El WhatsApp es requerido')
  } else if (!/^[67]\d{7}$/.test(localFormData.value.whatsapp)) {
    errors.push('El número de WhatsApp debe ser válido (8 dígitos, empezar con 6 o 7)')
  }
  
  // Validación de website (opcional pero si lo llena debe ser válido)
  if (localFormData.value.website && 
      !localFormData.value.website.startsWith('http://') && 
      !localFormData.value.website.startsWith('https://')) {
    errors.push('La URL del sitio web debe empezar con http:// o https://')
  }
  
  if (errors.length > 0) {
    console.error('❌ ERRORES DE VALIDACIÓN:', errors)
    console.log('📋 Datos actuales:', localFormData.value)
    
    // Mostrar alert con los errores
    const errorMessage = errors.join('\n• ')
    alert(`⚠️ Por favor completa los siguientes campos:\n\n• ${errorMessage}`)
    
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
/* ========== GLOBAL VUESTIC LABEL STYLES ========== */
:deep(.va-input__label),
:deep(.va-textarea__label),
:deep(.va-select__label),
:deep(.va-date-input__label) {
  font-size: 0.95rem !important;
  font-weight: 600 !important;
  color: #1E293B !important;
  letter-spacing: 0.2px !important;
}

.information-step-job {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  background: linear-gradient(135deg, #F9F5FF 0%, #F3E8FF 100%);
  min-height: 100vh;
  padding: 1.5rem;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
  padding: 2rem;
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
  font-size: 1.75rem;
  font-weight: 700;
  color: #1E293B;
  margin: 0;
  letter-spacing: -0.3px;
  line-height: 1.3;
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
  gap: 1.25rem;
  background: white;
  padding: 2rem;
  border-radius: 16px;
  max-width: 1000px;
  margin: 0 auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
  background: #F8FAFC;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
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
}

.section-description {
  color: #666;
  font-size: 0.95rem;
  margin: -0.5rem 0 0.5rem 0;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.field-label,
.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #1E293B;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}

.input-hint {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.9rem;
  color: #5B21B6;
  padding: 0.875rem 1rem;
  background: #F9F5FF;
  border-radius: 8px;
  border-left: 3px solid #7C3AED;
  line-height: 1.5;
  margin-top: 0.75rem;
}

.success-hint {
  background: #F0FDF4;
  color: #166534;
  border-left-color: #16A34A;
}

.whatsapp-prefix {
  font-weight: 700;
  color: #7C3AED;
  padding: 0.5rem 0.75rem;
  background: #E0E7FF;
  border-radius: 6px;
  font-size: 0.9rem;
}

.currency-symbol {
  font-weight: 700;
  color: #7C3AED;
  padding: 0.5rem 0.75rem;
  background: #E0E7FF;
  border-radius: 6px;
  font-size: 0.9rem;
}

/* ========== Logo Preview ========== */
.logo-preview-container {
  margin-top: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px dashed #E2E8F0;
}

.logo-preview-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #7C3AED;
  margin: 0 0 1rem 0;
}

.logo-preview-image {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  object-fit: cover;
  border: 3px solid #7C3AED;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}

/* ========== Salary Section ========== */
.salary-tip {
  display: flex;
  gap: 0.875rem;
  padding: 1rem 1.25rem;
  background: #FFFBEB;
  border-left: 3px solid #FBBF24;
  border-radius: 8px;
  margin-bottom: 1.25rem;
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
  background: #F8FAFC;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
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


/* ========== Vacantes ========== */
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

.vacancy-tracker {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  margin-top: 1rem;
}

.vacancy-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  border-radius: 8px;
  color: white;
  font-size: 1.25rem;
  transition: all 0.2s;
}

.vacancy-icon:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.2);
}

.vacancy-more {
  padding: 0.5rem 1rem;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-weight: 700;
  color: #7C3AED;
  font-size: 0.9rem;
}

/* ========== Responsive ========== */
@media (max-width: 1024px) {
  .information-step-job {
    padding: 1.5rem;
  }

  .form-content {
    padding: 1.5rem;
  }

  .form-section {
    padding: 1rem;
  }
}

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
    margin: 0.5rem 0 0 0;
  }

  .form-content {
    padding: 1.5rem;
    gap: 1.25rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .form-section {
    padding: 1rem;
  }

  .section-title {
    font-size: 1rem;
  }

  .salary-inputs {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .salary-separator {
    display: none !important;
  }

  .accordion-header {
    padding: 1.25rem 1.5rem;
    gap: 1rem;
  }

  .accordion-icon {
    width: 48px;
    height: 48px;
  }

  .accordion-title {
    font-size: 1.1rem;
  }

  .accordion-summary {
    font-size: 0.85rem;
  }

  .accordion-content {
    padding: 1.25rem;
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

  .step-subtitle {
    font-size: 0.9rem;
    margin: 0.25rem 0 0 0;
  }

  .form-content {
    padding: 1rem;
    gap: 1rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .accordion-header {
    padding: 1rem;
    gap: 0.75rem;
  }

  .accordion-icon {
    width: 40px;
    height: 40px;
  }

  .accordion-title {
    font-size: 1rem;
  }

  .accordion-summary {
    font-size: 0.8rem;
  }

  .accordion-content {
    padding: 1rem;
  }
}

/* ========== Checkbox Anónimo ========== */
.anonymous-checkbox {
  margin-top: 1rem;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #FEF3C7 0%, #FEE2B8 100%);
  border-left: 4px solid #F59E0B;
  border-radius: 12px;
}


/* ========== Botones de Navegación ========== */
.navigation-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: space-between;
  align-items: center;
  margin-top: 2.5rem;
  padding-top: 2rem;
  border-top: 2px solid #E2E8F0;
}

.navigation-buttons .next-button {
  margin-left: auto;
}

@media (max-width: 768px) {
  .navigation-buttons {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .navigation-buttons button {
    width: 100%;
  }

  .navigation-buttons .next-button {
    margin-left: 0;
  }
}

/* ========== ACCORDION STYLES ========== */
.accordion-section {
  background: white;
  border-radius: 16px;
  border: 2px solid #E2E8F0;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin-bottom: 0;
}

.accordion-section:hover {
  border-color: #DDD6FE;
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.1);
}

.accordion-section.expanded {
  border-color: #7C3AED;
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.15);
}

.accordion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  cursor: pointer;
  background: white;
  transition: all 0.3s ease;
  user-select: none;
  gap: 1.5rem;
}

.accordion-header:hover {
  background: #F8FAFC;
}

.accordion-section.expanded .accordion-header {
  background: linear-gradient(135deg, #F9F5FF 0%, #F3E8FF 100%);
  border-bottom: 2px solid #E9D5FF;
}

.accordion-header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
  min-width: 0;
}

.accordion-header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.accordion-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6D28D9;
  flex-shrink: 0;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.accordion-section.expanded .accordion-icon {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
  transform: scale(1.12) translateY(-2px);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35);
}

.accordion-title-group {
  flex: 1;
  min-width: 0;
}

.accordion-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1E293B;
  margin: 0;
  line-height: 1.4;
  transition: color 0.3s ease;
}

.accordion-section.expanded .accordion-title {
  color: #7C3AED;
}

.accordion-summary {
  font-size: 0.95rem;
  color: #7C3AED;
  font-weight: 500;
  margin: 0.25rem 0 0 0;
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: all 0.3s ease;
}

.accordion-chevron {
  color: #94A3B8;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  flex-shrink: 0;
}

.accordion-section.expanded .accordion-chevron {
  color: #7C3AED;
  transform: rotate(180deg) scale(1.1);
}

.accordion-content {
  padding: 1.5rem;
  background: white;
  animation: accordionSlideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes accordionSlideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile accordion adjustments */
@media (max-width: 768px) {
  .accordion-header {
    padding: 1.25rem 1.5rem;
    gap: 1rem;
  }

  .accordion-header-left {
    gap: 1rem;
  }

  .accordion-icon {
    width: 48px;
    height: 48px;
  }

  .accordion-title {
    font-size: 1.1rem;
  }

  .accordion-summary {
    font-size: 0.85rem;
  }

  .accordion-content {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .accordion-header {
    padding: 1rem;
  }

  .accordion-header-left {
    gap: 0.75rem;
  }

  .accordion-icon {
    width: 40px;
    height: 40px;
  }

  .accordion-title {
    font-size: 1rem;
  }

  .accordion-summary {
    font-size: 0.8rem;
  }

  .accordion-content {
    padding: 1rem;
  }

  .accordion-header-right {
    gap: 0.5rem;
  }
}
</style>