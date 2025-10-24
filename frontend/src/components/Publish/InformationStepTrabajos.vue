<!-- frontend/src/components/Publish/InformationStepTrabajos.vue -->
<template>
  <div class="information-step-trabajos">
    <h2 class="step-title">
      <va-icon name="work" size="2rem" color="purple" />
      Información de la Oferta de Trabajo
    </h2>
    <p class="step-description">
      Completa los datos de tu oferta laboral. Mientras más detallada sea la información, mejores candidatos atraerás.
    </p>

    <!-- ========== SECCIÓN 1: INFORMACIÓN DEL PUESTO ========== -->
    <div class="form-section">
      <h3 class="section-title">
        <va-icon name="badge" color="purple" />
        1. Información del Puesto
      </h3>

      <div class="form-row">
        <VaInput
          v-model="formData.jobTitle"
          label="Título del Puesto *"
          placeholder="Ej: Desarrollador Full Stack Senior"
          :rules="[(v) => !!v || 'El título es obligatorio']"
          class="full-width"
        >
          <template #prepend>
            <va-icon name="work" />
          </template>
        </VaInput>
      </div>

      <div class="form-row two-columns">
        <VaSelect
          v-model="formData.area"
          label="Área / Departamento *"
          placeholder="Selecciona el área"
          :options="areaOptions"
          :rules="[(v) => !!v || 'El área es obligatoria']"
        />

        <VaSelect
          v-model="formData.experienceLevel"
          label="Nivel de Experiencia *"
          placeholder="Selecciona el nivel"
          :options="experienceLevelOptions"
          :rules="[(v) => !!v || 'El nivel es obligatorio']"
        />
      </div>

      <div class="form-row">
        <VaInput
          v-model.number="formData.vacancies"
          type="number"
          label="Cantidad de Vacantes *"
          placeholder="Número de posiciones disponibles"
          :min="1"
          :rules="[(v) => v > 0 || 'Debe haber al menos 1 vacante']"
        >
          <template #prepend>
            <va-icon name="groups" />
          </template>
        </VaInput>
      </div>

      <div class="form-row">
        <VaTextarea
          v-model="formData.description"
          label="Descripción del Puesto *"
          placeholder="Describe el puesto, la misión principal y el contexto del equipo..."
          :min-rows="5"
          :max-rows="10"
          counter
          :max-length="3000"
          class="full-width"
          :rules="[
            (v) => !!v || 'La descripción es obligatoria',
            (v) => v?.length >= 100 || 'Mínimo 100 caracteres'
          ]"
        />
        <div class="field-hint">
          💡 Incluye información sobre el rol, el equipo y la misión del puesto
        </div>
      </div>
    </div>

    <!-- ========== SECCIÓN 2: REQUISITOS ========== -->
    <div class="form-section">
      <h3 class="section-title">
        <va-icon name="checklist" color="purple" />
        2. Requisitos del Candidato
      </h3>

      <div class="form-row">
        <label class="va-input-label">Educación Requerida *</label>
        <div class="education-checkboxes">
          <VaCheckbox
            v-for="option in educationOptions"
            :key="option"
            v-model="formData.education"
            :array-value="option"
            :label="option"
          />
        </div>
        <div class="field-hint">
          💡 Selecciona todos los niveles educativos aceptables para el puesto
        </div>
      </div>

      <div class="form-row">

        <VaInput
          v-model.number="formData.yearsExperience"
          type="number"
          label="Años de Experiencia *"
          placeholder="Años mínimos requeridos"
          :min="0"
          :rules="[(v) => v >= 0 || 'Debe ser mayor o igual a 0']"
        >
          <template #append>
            <span class="input-suffix">años</span>
          </template>
        </VaInput>
      </div>

      <div class="form-row">
        <VaSelect
          v-model="formData.languages"
          label="Idiomas Requeridos"
          placeholder="Selecciona idiomas"
          :options="languageOptions"
          multiple
          searchable
        />
        <div class="field-hint">
          💡 Selecciona todos los idiomas necesarios para el puesto
        </div>
      </div>

      <div class="form-row">
        <label class="va-input-label">Competencias Técnicas *</label>
        <div class="tags-input-wrapper">
          <VaInput
            v-model="technicalSkillInput"
            placeholder="Escribe una competencia y presiona Enter"
            @keyup.enter="addTechnicalSkill"
          >
            <template #prepend>
              <va-icon name="code" />
            </template>
          </VaInput>
          <div class="tags-display">
            <div
              v-for="(skill, index) in formData.technicalSkills"
              :key="index"
              class="skill-tag"
            >
              {{ skill }}
              <button 
                type="button"
                class="remove-tag-btn" 
                @click="removeTechnicalSkill(index)"
                title="Eliminar"
              >
                ×
              </button>
            </div>
          </div>
        </div>
        <div class="field-hint">
          💡 Ej: Python, JavaScript, React, SQL, Git, etc.
        </div>
      </div>

      <div class="form-row">
        <label class="va-input-label">Competencias Blandas</label>
        <div class="tags-input-wrapper">
          <VaInput
            v-model="softSkillInput"
            placeholder="Escribe una competencia y presiona Enter"
            @keyup.enter="addSoftSkill"
          >
            <template #prepend>
              <va-icon name="psychology" />
            </template>
          </VaInput>
          <div class="tags-display">
            <div
              v-for="(skill, index) in formData.softSkills"
              :key="index"
              class="skill-tag skill-tag-soft"
            >
              {{ skill }}
              <button 
                type="button"
                class="remove-tag-btn" 
                @click="removeSoftSkill(index)"
                title="Eliminar"
              >
                ×
              </button>
            </div>
          </div>
        </div>
        <div class="field-hint">
          💡 Ej: Trabajo en equipo, Liderazgo, Comunicación, etc.
        </div>
      </div>

      <div class="form-row">
        <VaTextarea
          v-model="formData.additionalRequirements"
          label="Requisitos Adicionales"
          placeholder="Otros requisitos importantes para el puesto..."
          :min-rows="3"
          :max-rows="5"
          class="full-width"
        />
      </div>
    </div>

    <!-- ========== SECCIÓN 3: CONDICIONES LABORALES ========== -->
    <div class="form-section">
      <h3 class="section-title">
        <va-icon name="event_note" color="purple" />
        3. Condiciones Laborales
      </h3>

      <div class="form-row three-columns">
        <VaSelect
          v-model="formData.contractType"
          label="Tipo de Contrato *"
          placeholder="Selecciona el tipo"
          :options="contractTypeOptions"
          :rules="[(v) => !!v || 'El tipo de contrato es obligatorio']"
        />

        <VaSelect
          v-model="formData.workday"
          label="Jornada Laboral *"
          placeholder="Selecciona la jornada"
          :options="workdayOptions"
          :rules="[(v) => !!v || 'La jornada es obligatoria']"
        />

        <VaSelect
          v-model="formData.modality"
          label="Modalidad *"
          placeholder="Selecciona modalidad"
          :options="modalityOptions"
          :rules="[(v) => !!v || 'La modalidad es obligatoria']"
        />
      </div>

      <div class="form-row">
        <VaInput
          v-model="formData.schedule"
          label="Horario de Trabajo"
          placeholder="Ej: Lunes a Viernes de 9:00 a 18:00"
        >
          <template #prepend>
            <va-icon name="schedule" />
          </template>
        </VaInput>
      </div>

      <div class="form-row">
        <label class="va-input-label">Salario *</label>
        <div class="salary-inputs">
          <VaRadio
            v-model="formData.salaryType"
            option="range"
            label="Rango Salarial"
          />
          <VaRadio
            v-model="formData.salaryType"
            option="undisclosed"
            label="A convenir / No declarado"
          />
        </div>

        <div v-if="formData.salaryType === 'range'" class="salary-range">
          <VaSelect
            v-model="formData.currency"
            label="Moneda"
            :options="['Bs.', 'USD', '$us']"
            style="max-width: 120px;"
          />
          <VaInput
            v-model.number="formData.salaryMin"
            type="number"
            label="Desde"
            placeholder="Salario mínimo"
            :min="0"
          />
          <VaInput
            v-model.number="formData.salaryMax"
            type="number"
            label="Hasta"
            placeholder="Salario máximo"
            :min="formData.salaryMin || 0"
          />
        </div>
      </div>
    </div>

    <!-- ========== SECCIÓN 4: BENEFICIOS ========== -->
    <div class="form-section">
      <h3 class="section-title">
        <va-icon name="card_giftcard" color="purple" />
        4. Beneficios y Ventajas
      </h3>

      <div class="form-row">
        <label class="va-input-label">Beneficios Incluidos</label>
        <div class="benefits-grid">
          <VaCheckbox
            v-for="benefit in benefitOptions"
            :key="benefit"
            v-model="formData.benefits"
            :array-value="benefit"
            :label="benefit"
          />
        </div>
      </div>

      <div class="form-row">
        <VaTextarea
          v-model="formData.otherBenefits"
          label="Otros Beneficios"
          placeholder="Describe otros beneficios o ventajas que ofreces..."
          :min-rows="3"
          class="full-width"
        />
      </div>
    </div>

    <!-- ========== SECCIÓN 5: INFORMACIÓN DE LA EMPRESA ========== -->
    <div class="form-section">
      <h3 class="section-title">
        <va-icon name="business" color="purple" />
        5. Información de la Empresa
      </h3>

      <div class="form-row">
        <VaCheckbox
          v-model="formData.confidential"
          label="Publicación Confidencial"
        />
        <div class="field-hint">
          🔒 Si marcas esta opción, el nombre de tu empresa no se mostrará públicamente
        </div>
      </div>

      <div v-if="!formData.confidential">
        <div class="form-row">
          <VaInput
            v-model="formData.companyName"
            label="Nombre de la Empresa *"
            placeholder="Nombre oficial de la empresa"
            :rules="[(v) => !!v || 'El nombre de la empresa es obligatorio']"
          >
            <template #prepend>
              <va-icon name="business" />
            </template>
          </VaInput>
        </div>

        <div class="form-row two-columns">
          <VaSelect
            v-model="formData.companySector"
            label="Sector / Industria *"
            placeholder="Sector de la empresa"
            :options="sectorOptions"
            searchable
            :rules="[(v) => !!v || 'El sector es obligatorio']"
          />

          <VaSelect
            v-model="formData.companySize"
            label="Tamaño de la Empresa"
            placeholder="Número de empleados"
            :options="companySizeOptions"
          />
        </div>

        <div class="form-row">
          <VaTextarea
            v-model="formData.companyDescription"
            label="Descripción de la Empresa"
            placeholder="Describe brevemente tu empresa, su misión y cultura..."
            :min-rows="3"
            :max-rows="5"
            counter
            :max-length="500"
          class="full-width"
          />
        </div>

        <div class="form-row">
          <VaInput
            v-model="formData.companyWebsite"
            label="Sitio Web"
            placeholder="https://www.tuempresa.com"
            type="url"
          >
            <template #prepend>
              <va-icon name="language" />
            </template>
          </VaInput>
        </div>
      </div>

      <div v-else class="confidential-notice">
        <va-icon name="visibility_off" size="2rem" color="#999" />
        <p>Esta oferta se publicará como "Publicación Confidencial" o "Importante Empresa"</p>
      </div>
    </div>

    <!-- ========== SECCIÓN 6: PROCESO DE POSTULACIÓN ========== -->
    <div class="form-section">
      <h3 class="section-title">
        <va-icon name="send" color="purple" />
        6. Proceso de Postulación
      </h3>

      <div class="form-row">
        <label class="va-input-label">¿Cómo pueden postular los candidatos? *</label>
        <div class="application-methods">
          <VaCheckbox
            v-model="formData.applicationMethods"
            array-value="email"
            label="Por Email"
          />
          <VaCheckbox
            v-model="formData.applicationMethods"
            array-value="whatsapp"
            label="Por WhatsApp"
          />
          <VaCheckbox
            v-model="formData.applicationMethods"
            array-value="external"
            label="Link Externo"
          />
          <VaCheckbox
            v-model="formData.applicationMethods"
            array-value="internal"
            label="Sistema Interno (formulario)"
          />
        </div>
      </div>

      <div v-if="formData.applicationMethods.includes('email')" class="form-row">
        <VaInput
          v-model="formData.applicationEmail"
          label="Email para Postulaciones *"
          placeholder="rrhh@empresa.com"
          type="email"
          :rules="[
            (v) => !!v || 'El email es obligatorio',
            (v) => /.+@.+\..+/.test(v) || 'Email inválido'
          ]"
        >
          <template #prepend>
            <va-icon name="email" />
          </template>
        </VaInput>
      </div>

      <div v-if="formData.applicationMethods.includes('whatsapp')" class="form-row">
        <VaInput
          v-model="formData.applicationWhatsapp"
          label="WhatsApp para Postulaciones *"
          placeholder="+591 XXXXXXXX"
          :rules="[(v) => !!v || 'El WhatsApp es obligatorio']"
        >
          <template #prepend>
            <va-icon name="phone" />
          </template>
        </VaInput>
      </div>

      <div v-if="formData.applicationMethods.includes('external')" class="form-row">
        <VaInput
          v-model="formData.applicationLink"
          label="Link de Postulación *"
          placeholder="https://..."
          type="url"
          :rules="[(v) => !!v || 'El link es obligatorio']"
        >
          <template #prepend>
            <va-icon name="link" />
          </template>
        </VaInput>
      </div>

      <div class="form-row two-columns">
        <VaDateInput
          v-model="formData.closingDate"
          label="Fecha de Cierre de Convocatoria"
          placeholder="Selecciona una fecha"
          :min-date="new Date()"
        />

        <VaCheckbox
          v-model="formData.urgentHiring"
          label="Contratación Urgente"
          class="urgent-checkbox"
        />
      </div>

      <div class="form-row">
        <VaTextarea
          v-model="formData.applicationNotes"
          label="Información Adicional para Postulantes"
          placeholder="Instrucciones especiales, documentos requeridos, etc..."
          :min-rows="3"
          class="full-width"
        />
      </div>
    </div>

    <!-- Validación Summary (solo cuando hay errores) -->
    <div v-if="showValidationErrors" class="validation-summary">
      <va-icon name="error" color="danger" />
      <div>
        <h4>Por favor completa los siguientes campos obligatorios:</h4>
        <ul>
          <li v-for="error in validationErrors" :key="error">{{ error }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

// ========== DATOS DEL FORMULARIO ==========
const formData = ref({
  // Sección 1: Información del Puesto
  jobTitle: '',
  area: '',
  experienceLevel: '',
  vacancies: 1,
  description: '',

  // Sección 2: Requisitos
  education: [],
  yearsExperience: 0,
  languages: [],
  technicalSkills: [],
  softSkills: [],
  additionalRequirements: '',

  // Sección 3: Condiciones Laborales
  contractType: '',
  workday: '',
  modality: '',
  schedule: '',
  salaryType: 'range',
  currency: 'Bs.',
  salaryMin: null,
  salaryMax: null,

  // Sección 4: Beneficios
  benefits: [],
  otherBenefits: '',

  // Sección 5: Información de la Empresa
  confidential: false,
  companyName: '',
  companySector: '',
  companySize: '',
  companyDescription: '',
  companyWebsite: '',

  // Sección 6: Proceso de Postulación
  applicationMethods: ['internal'],
  applicationEmail: '',
  applicationWhatsapp: '',
  applicationLink: '',
  closingDate: null,
  urgentHiring: false,
  applicationNotes: ''
})

// ========== INPUTS TEMPORALES PARA TAGS ==========
const technicalSkillInput = ref('')
const softSkillInput = ref('')

// ========== OPCIONES DE SELECTS ==========
const areaOptions = [
  'Tecnología e IT',
  'Administración y Finanzas',
  'Ventas y Marketing',
  'Recursos Humanos',
  'Producción y Operaciones',
  'Logística y Distribución',
  'Atención al Cliente',
  'Legal',
  'Salud',
  'Educación',
  'Ingeniería',
  'Diseño y Creatividad',
  'Otros'
]

const experienceLevelOptions = [
  'Sin experiencia / Pasante',
  'Junior (0-2 años)',
  'Semi-Senior (2-5 años)',
  'Senior (5+ años)',
  'Líder / Gerente',
  'Director / Executive'
]

const educationOptions = [
  'Bachiller',
  'Técnico Medio',
  'Técnico Superior',
  'Universitario en curso',
  'Licenciatura / Título Profesional',
  'Especialización',
  'Maestría',
  'Doctorado',
  'No requerido'
]

const languageOptions = [
  'Español',
  'Inglés',
  'Portugués',
  'Francés',
  'Alemán',
  'Italiano',
  'Chino',
  'Japonés',
  'Quechua',
  'Aymara',
  'Guaraní'
]

const contractTypeOptions = [
  'Tiempo Indefinido',
  'Plazo Fijo',
  'Por Proyecto',
  'Temporal / Reemplazo',
  'Freelance',
  'Consultoría',
  'Pasantía / Práctica'
]

const workdayOptions = [
  'Tiempo Completo',
  'Medio Tiempo',
  'Por Horas',
  'Fines de Semana',
  'Nocturno',
  'Turnos Rotativos'
]

const modalityOptions = [
  'Presencial',
  'Remoto',
  'Híbrido'
]

const benefitOptions = [
  'Seguro Médico',
  'Seguro de Vida',
  'Aguinaldo',
  'Bono de Desempeño',
  'Capacitación Pagada',
  'Días de Vacación Adicionales',
  'Home Office',
  'Horario Flexible',
  'Comedor',
  'Transporte',
  'Bono de Transporte',
  'Equipos de Trabajo',
  'Laptop',
  'Celular Corporativo',
  'Descuentos en Productos/Servicios'
]

const sectorOptions = [
  'Tecnología e IT',
  'Agricultura y Campo',
  'Comercio y Retail',
  'Construcción',
  'Educación',
  'Salud',
  'Finanzas y Seguros',
  'Manufactura',
  'Minería',
  'Turismo y Hotelería',
  'Transporte y Logística',
  'Telecomunicaciones',
  'Energía',
  'Alimentos y Bebidas',
  'Servicios Profesionales',
  'Marketing y Publicidad',
  'Medios y Comunicación',
  'ONGs',
  'Gobierno',
  'Otros'
]

const companySizeOptions = [
  '1-10 empleados',
  '11-50 empleados',
  '51-200 empleados',
  '201-500 empleados',
  '501-1000 empleados',
  'Más de 1000 empleados'
]

// ========== MÉTODOS PARA TAGS ==========
const addTechnicalSkill = () => {
  if (technicalSkillInput.value.trim()) {
    formData.value.technicalSkills.push(technicalSkillInput.value.trim())
    technicalSkillInput.value = ''
  }
}

const removeTechnicalSkill = (index) => {
  formData.value.technicalSkills.splice(index, 1)
}

const addSoftSkill = () => {
  if (softSkillInput.value.trim()) {
    formData.value.softSkills.push(softSkillInput.value.trim())
    softSkillInput.value = ''
  }
}

const removeSoftSkill = (index) => {
  formData.value.softSkills.splice(index, 1)
}

// ========== VALIDACIÓN ==========
const showValidationErrors = ref(false)

const validationErrors = computed(() => {
  const errors = []
  
  if (!formData.value.jobTitle) errors.push('Título del puesto')
  if (!formData.value.area) errors.push('Área / Departamento')
  if (!formData.value.experienceLevel) errors.push('Nivel de experiencia')
  if (!formData.value.description || formData.value.description.length < 100) {
    errors.push('Descripción del puesto (mínimo 100 caracteres)')
  }
  if (formData.value.education.length === 0) errors.push('Al menos un nivel de educación')
  if (formData.value.technicalSkills.length === 0) errors.push('Al menos una competencia técnica')
  if (!formData.value.contractType) errors.push('Tipo de contrato')
  if (!formData.value.workday) errors.push('Jornada laboral')
  if (!formData.value.modality) errors.push('Modalidad de trabajo')
  
  if (!formData.value.confidential) {
    if (!formData.value.companyName) errors.push('Nombre de la empresa')
    if (!formData.value.companySector) errors.push('Sector de la empresa')
  }
  
  if (formData.value.applicationMethods.length === 0) {
    errors.push('Al menos un método de postulación')
  }
  
  if (formData.value.applicationMethods.includes('email') && !formData.value.applicationEmail) {
    errors.push('Email para postulaciones')
  }
  
  if (formData.value.applicationMethods.includes('whatsapp') && !formData.value.applicationWhatsapp) {
    errors.push('WhatsApp para postulaciones')
  }
  
  if (formData.value.applicationMethods.includes('external') && !formData.value.applicationLink) {
    errors.push('Link de postulación')
  }
  
  return errors
})

const isValid = computed(() => validationErrors.value.length === 0)

// ========== WATCH PARA EMITIR CAMBIOS ==========
watch(formData, (newValue) => {
  emit('update:modelValue', {
    ...newValue,
    isValid: isValid.value
  })
}, { deep: true })

// ========== INICIALIZAR CON DATOS EXISTENTES ==========
if (props.modelValue && Object.keys(props.modelValue).length > 0) {
  Object.assign(formData.value, props.modelValue)
}

// Emitir validación inicial
emit('update:modelValue', {
  ...formData.value,
  isValid: isValid.value
})

// Exponer método para validar desde el padre
defineExpose({
  validate: () => {
    showValidationErrors.value = !isValid.value
    return isValid.value
  }
})
</script>

<style scoped>
.information-step-trabajos {
  max-width: 900px;
  margin: 0 auto;
}

.step-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0 0 1rem 0;
}

.step-description {
  font-size: 1.05rem;
  color: #666;
  margin: 0 0 3rem 0;
  line-height: 1.6;
}

/* ========== Secciones ========== */
.form-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1.5rem 0;
  padding-bottom: 1rem;
  border-bottom: 2px solid #F0F0F0;
}

/* ========== Filas de Formulario ========== */
.form-row {
  margin-bottom: 1.5rem;
}

.form-row.two-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-row.three-columns {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

/* ========== Education Checkboxes ========== */
.education-checkboxes {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  padding: 1rem;
  background: #F8F8F8;
  border-radius: 8px;
}

.full-width {
  width: 100%;
}

.field-hint {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

.input-suffix {
  color: #666;
  font-size: 0.9rem;
}

/* ========== Tags Input ========== */
.tags-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tags-display {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  min-height: 40px;
  padding: 0.75rem;
  background: #F8F8F8;
  border-radius: 8px;
  border: 2px dashed #E0E0E0;
}

/* ========== Salary Inputs ========== */
.salary-inputs {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
}

.salary-range {
  display: grid;
  grid-template-columns: 120px 1fr 1fr;
  gap: 1rem;
  margin-top: 1rem;
}

/* ========== Benefits Grid ========== */
.benefits-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  padding: 1rem;
  background: #F8F8F8;
  border-radius: 8px;
}

/* ========== Application Methods ========== */
.application-methods {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background: #F8F8F8;
  border-radius: 8px;
}

.urgent-checkbox {
  display: flex;
  align-items: center;
  margin-top: 1.5rem;
}

/* ========== Confidential Notice ========== */
.confidential-notice {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  background: #F8F8F8;
  border-radius: 8px;
  text-align: center;
  color: #666;
}

/* ========== Validation Summary ========== */
.validation-summary {
  background: rgba(244, 67, 54, 0.1);
  border-left: 4px solid #F44336;
  padding: 1.5rem;
  border-radius: 8px;
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.validation-summary h4 {
  color: #D32F2F;
  margin: 0 0 0.75rem 0;
  font-size: 1.1rem;
}

.validation-summary ul {
  margin: 0;
  padding-left: 1.5rem;
  color: #D32F2F;
}

.validation-summary li {
  margin-bottom: 0.35rem;
}

/* ========== Responsive ========== */
/* Tablets */
@media (max-width: 992px) {
  .form-row.three-columns {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .form-section {
    padding: 1.5rem;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .section-title {
    font-size: 1.25rem;
  }

  .form-row.two-columns,
  .form-row.three-columns {
    grid-template-columns: 1fr;
  }
  
  .education-checkboxes {
    grid-template-columns: 1fr;
  }

  .salary-range {
    grid-template-columns: 1fr;
  }

  .benefits-grid {
    grid-template-columns: 1fr;
  }

  .salary-inputs {
    flex-direction: column;
    gap: 0.75rem;
  }
}

/* ========== Custom Skill Tags ========== */
.skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: var(--color-purple);
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.skill-tag-soft {
  background: #2E7D32;
}

.remove-tag-btn {
  background: rgba(255, 255, 255, 0.3);
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  line-height: 1;
  color: white;
  transition: all 0.2s ease;
  padding: 0;
  margin: 0;
}

.remove-tag-btn:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: scale(1.1);
}

</style>