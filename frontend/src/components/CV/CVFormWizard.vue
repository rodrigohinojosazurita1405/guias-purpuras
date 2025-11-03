<!-- frontend/src/components/CV/CVFormWizard.vue -->
<template>
  <div class="cv-form-wizard">
    
    <!-- Header con Progress -->
    <div class="wizard-header">
      <h2 class="wizard-title">
        <va-icon :name="isEditing ? 'edit' : 'description'" size="1.5rem" />
        {{ isEditing ? 'Editar mi Currículum' : 'Crear mi Currículum' }}
      </h2>
      <p class="wizard-subtitle">
        {{ isEditing ? 'Actualiza tu CV profesional' : 'Completa tu CV profesional paso a paso' }}
      </p>

      <!-- Progress Bar -->
      <div class="progress-container">
        <VaProgressBar 
          :model-value="progressPercentage" 
          color="purple"
          size="large"
        />
        <span class="progress-text">{{ currentStepIndex + 1 }} de {{ steps.length }} pasos</span>
      </div>

      <!-- Steps Indicator -->
      <div class="steps-indicator">
        <div 
          v-for="(step, index) in steps" 
          :key="index"
          class="step-indicator"
          :class="{
            active: currentStepIndex === index,
            completed: currentStepIndex > index
          }"
        >
          <div class="step-circle">
            <va-icon 
              v-if="currentStepIndex > index" 
              name="check" 
              size="small"
            />
            <span v-else>{{ index + 1 }}</span>
          </div>
          <span class="step-label">{{ step.label }}</span>
        </div>
      </div>
    </div>

    <!-- Contenido del Wizard -->
    <div class="wizard-content">
      
      <!-- PASO 1: Datos Personales -->
      <div v-if="currentStepIndex === 0" class="wizard-step">
        <h3 class="step-title">
          <va-icon name="person" color="purple" />
          Datos Personales
        </h3>
        
        <div class="form-grid">
          <VaInput
            v-model="cvData.personalInfo.firstName"
            label="Nombres *"
            placeholder="Juan Carlos"
            :rules="[v => !!v || 'Campo requerido']"
          />
          
          <VaInput
            v-model="cvData.personalInfo.lastName"
            label="Apellidos *"
            placeholder="Pérez Gómez"
            :rules="[v => !!v || 'Campo requerido']"
          />

          <VaInput
            v-model="cvData.personalInfo.email"
            type="email"
            label="Email *"
            placeholder="juan@email.com"
            :rules="[
              v => !!v || 'Campo requerido',
              v => /.+@.+\..+/.test(v) || 'Email inválido'
            ]"
          />

          <VaInput
            v-model="cvData.personalInfo.phone"
            label="Teléfono *"
            placeholder="70123456"
            :rules="[v => !!v || 'Campo requerido']"
          />

          <VaInput
            v-model="cvData.personalInfo.city"
            label="Ciudad *"
            placeholder="Cochabamba"
            :rules="[v => !!v || 'Campo requerido']"
          />

          <VaInput
            v-model="cvData.personalInfo.address"
            label="Dirección"
            placeholder="Av. América #123"
          />

          <VaDateInput
            v-model="cvData.personalInfo.birthDate"
            label="Fecha de Nacimiento"
            placeholder="Selecciona una fecha"
          />

          <VaSelect
            v-model="cvData.personalInfo.gender"
            label="Género"
            :options="['Masculino', 'Femenino', 'Otro', 'Prefiero no decir']"
            placeholder="Selecciona"
          />

          <VaInput
            v-model="cvData.personalInfo.nationalId"
            label="CI / Documento"
            placeholder="12345678"
          />

          <VaInput
            v-model="cvData.personalInfo.linkedin"
            label="LinkedIn (Opcional)"
            placeholder="linkedin.com/in/usuario"
          />
        </div>

        <div class="form-full-width">
          <VaTextarea
            v-model="cvData.personalInfo.summary"
            label="Resumen Profesional *"
            placeholder="Describe brevemente tu perfil profesional, experiencia y objetivos..."
            :min-rows="4"
            :max-rows="8"
            counter
            :max-length="500"
            :rules="[v => !!v || 'Campo requerido']"
          />
        </div>
      </div>

      <!-- PASO 2: Formación Académica -->
      <div v-if="currentStepIndex === 1" class="wizard-step">
        <h3 class="step-title">
          <va-icon name="school" color="purple" />
          Formación Académica
        </h3>

        <VaButton
          @click="addEducation"
          color="purple"
          preset="secondary"
          icon="add"
          class="add-btn"
        >
          Agregar Formación
        </VaButton>

        <div 
          v-for="(edu, index) in cvData.education" 
          :key="index"
          class="repeatable-item"
        >
          <div class="item-header">
            <h4>Formación {{ index + 1 }}</h4>
            <VaButton
              v-if="cvData.education.length > 1"
              preset="plain"
              icon="delete"
              color="danger"
              @click="removeEducation(index)"
            />
          </div>

          <div class="form-grid">
            <VaSelect
              v-model="edu.level"
              label="Nivel *"
              :options="educationLevels"
              placeholder="Selecciona"
              :rules="[v => !!v || 'Campo requerido']"
            />

            <VaInput
              v-model="edu.institution"
              label="Institución *"
              placeholder="Universidad / Instituto"
              :rules="[v => !!v || 'Campo requerido']"
            />

            <VaInput
              v-model="edu.degree"
              label="Título / Carrera *"
              placeholder="Ej: Ingeniería de Sistemas"
              :rules="[v => !!v || 'Campo requerido']"
            />

            <VaInput
              v-model="edu.field"
              label="Área de Estudio"
              placeholder="Ej: Informática"
            />

            <VaDateInput
              v-model="edu.startDate"
              label="Fecha de Inicio *"
              placeholder="MM/AAAA"
            />

            <VaDateInput
              v-model="edu.endDate"
              label="Fecha de Fin"
              placeholder="MM/AAAA"
              :disabled="edu.current"
            />
          </div>

          <VaCheckbox
            v-model="edu.current"
            label="Actualmente cursando"
          />

          <VaTextarea
            v-model="edu.description"
            label="Descripción (Opcional)"
            placeholder="Menciones honoríficas, logros, proyectos destacados..."
            :min-rows="2"
            :max-rows="4"
            class="full-width-textarea"
          />
        </div>

        <div v-if="cvData.education.length === 0" class="empty-state">
          <va-icon name="school" size="3rem" color="#CCC" />
          <p>No has agregado ninguna formación académica</p>
          <VaButton @click="addEducation" color="purple">
            Agregar la primera
          </VaButton>
        </div>
      </div>

      <!-- PASO 3: Experiencia Laboral -->
      <div v-if="currentStepIndex === 2" class="wizard-step">
        <h3 class="step-title">
          <va-icon name="work" color="purple" />
          Experiencia Laboral
        </h3>

        <VaButton
          @click="addExperience"
          color="purple"
          preset="secondary"
          icon="add"
          class="add-btn"
        >
          Agregar Experiencia
        </VaButton>

        <div 
          v-for="(exp, index) in cvData.experience" 
          :key="index"
          class="repeatable-item"
        >
          <div class="item-header">
            <h4>Experiencia {{ index + 1 }}</h4>
            <VaButton
              v-if="cvData.experience.length > 1"
              preset="plain"
              icon="delete"
              color="danger"
              @click="removeExperience(index)"
            />
          </div>

          <div class="form-grid">
            <VaInput
              v-model="exp.position"
              label="Cargo / Puesto *"
              placeholder="Ej: Desarrollador Full Stack"
              :rules="[v => !!v || 'Campo requerido']"
            />

            <VaInput
              v-model="exp.company"
              label="Empresa *"
              placeholder="Nombre de la empresa"
              :rules="[v => !!v || 'Campo requerido']"
            />

            <VaInput
              v-model="exp.location"
              label="Ubicación"
              placeholder="Ciudad, País"
            />

            <VaSelect
              v-model="exp.employmentType"
              label="Tipo de Empleo"
              :options="employmentTypes"
              placeholder="Selecciona"
            />

            <VaDateInput
              v-model="exp.startDate"
              label="Fecha de Inicio *"
              placeholder="MM/AAAA"
            />

            <VaDateInput
              v-model="exp.endDate"
              label="Fecha de Fin"
              placeholder="MM/AAAA"
              :disabled="exp.current"
            />
          </div>

          <VaCheckbox
            v-model="exp.current"
            label="Actualmente trabajo aquí"
          />

          <VaTextarea
            v-model="exp.description"
            label="Descripción de Responsabilidades *"
            placeholder="Describe tus funciones, logros y responsabilidades principales..."
            :min-rows="4"
            :max-rows="8"
            counter
            :max-length="1000"
            :rules="[v => !!v || 'Campo requerido']"
            class="full-width-textarea"
          />
        </div>

        <div v-if="cvData.experience.length === 0" class="empty-state">
          <va-icon name="work" size="3rem" color="#CCC" />
          <p>No has agregado ninguna experiencia laboral</p>
          <VaButton @click="addExperience" color="purple">
            Agregar la primera
          </VaButton>
        </div>
      </div>

      <!-- PASO 4: Habilidades -->
      <div v-if="currentStepIndex === 3" class="wizard-step">
        <h3 class="step-title">
          <va-icon name="psychology" color="purple" />
          Habilidades y Competencias
        </h3>

        <div class="skills-section">
          <VaInput
            v-model="newSkill"
            label="Agregar Habilidad"
            placeholder="Ej: JavaScript, Liderazgo, Excel..."
            @keyup.enter="addSkill"
          >
            <template #appendInner>
              <VaButton
                preset="plain"
                icon="add"
                @click="addSkill"
              />
            </template>
          </VaInput>

          <div class="skills-chips">
            <VaChip
              v-for="(skill, index) in cvData.skills"
              :key="index"
              closeable
              color="purple"
              @update:model-value="removeSkill(index)"
            >
              {{ skill }}
            </VaChip>
          </div>

          <div v-if="cvData.skills.length === 0" class="empty-state-small">
            <p>No has agregado habilidades. Presiona Enter o el botón + para agregar.</p>
          </div>
        </div>
      </div>

      <!-- PASO 5: Idiomas -->
      <div v-if="currentStepIndex === 4" class="wizard-step">
        <h3 class="step-title">
          <va-icon name="translate" color="purple" />
          Idiomas
        </h3>

        <VaButton
          @click="addLanguage"
          color="purple"
          preset="secondary"
          icon="add"
          class="add-btn"
        >
          Agregar Idioma
        </VaButton>

        <div 
          v-for="(lang, index) in cvData.languages" 
          :key="index"
          class="repeatable-item-small"
        >
          <div class="item-header">
            <h4>Idioma {{ index + 1 }}</h4>
            <VaButton
              v-if="cvData.languages.length > 1"
              preset="plain"
              icon="delete"
              color="danger"
              size="small"
              @click="removeLanguage(index)"
            />
          </div>

          <div class="form-grid-small">
            <VaInput
              v-model="lang.name"
              label="Idioma *"
              placeholder="Ej: Inglés"
              :rules="[v => !!v || 'Campo requerido']"
            />

            <VaSelect
              v-model="lang.level"
              label="Nivel *"
              :options="languageLevels"
              placeholder="Selecciona"
              :rules="[v => !!v || 'Campo requerido']"
            />
          </div>
        </div>

        <div v-if="cvData.languages.length === 0" class="empty-state">
          <va-icon name="translate" size="3rem" color="#CCC" />
          <p>No has agregado idiomas</p>
          <VaButton @click="addLanguage" color="purple">
            Agregar el primero
          </VaButton>
        </div>
      </div>

      <!-- PASO 6: Preview -->
      <div v-if="currentStepIndex === 5" class="wizard-step">
        <h3 class="step-title">
          <va-icon name="preview" color="purple" />
          Vista Previa de tu CV
        </h3>

        <div class="cv-preview-container">
          <!-- Datos Personales -->
          <div class="preview-section">
            <h4 class="preview-section-title">
              <va-icon name="person" size="small" />
              Datos Personales
            </h4>
            <div class="preview-content">
              <p><strong>Nombre:</strong> {{ cvData.personalInfo.firstName }} {{ cvData.personalInfo.lastName }}</p>
              <p><strong>Email:</strong> {{ cvData.personalInfo.email }}</p>
              <p><strong>Teléfono:</strong> {{ cvData.personalInfo.phone }}</p>
              <p><strong>Ciudad:</strong> {{ cvData.personalInfo.city }}</p>
              <p v-if="cvData.personalInfo.linkedin"><strong>LinkedIn:</strong> {{ cvData.personalInfo.linkedin }}</p>
              <p class="preview-summary">{{ cvData.personalInfo.summary }}</p>
            </div>
          </div>

          <!-- Formación -->
          <div v-if="cvData.education.length > 0" class="preview-section">
            <h4 class="preview-section-title">
              <va-icon name="school" size="small" />
              Formación Académica
            </h4>
            <div 
              v-for="(edu, index) in cvData.education"
              :key="index"
              class="preview-item"
            >
              <h5>{{ edu.degree }}</h5>
              <p>{{ edu.institution }} - {{ edu.level }}</p>
              <p class="preview-date">{{ formatDate(edu.startDate) }} - {{ edu.current ? 'Presente' : formatDate(edu.endDate) }}</p>
              <p v-if="edu.description">{{ edu.description }}</p>
            </div>
          </div>

          <!-- Experiencia -->
          <div v-if="cvData.experience.length > 0" class="preview-section">
            <h4 class="preview-section-title">
              <va-icon name="work" size="small" />
              Experiencia Laboral
            </h4>
            <div 
              v-for="(exp, index) in cvData.experience"
              :key="index"
              class="preview-item"
            >
              <h5>{{ exp.position }}</h5>
              <p>{{ exp.company }} - {{ exp.employmentType }}</p>
              <p class="preview-date">{{ formatDate(exp.startDate) }} - {{ exp.current ? 'Presente' : formatDate(exp.endDate) }}</p>
              <p>{{ exp.description }}</p>
            </div>
          </div>

          <!-- Habilidades -->
          <div v-if="cvData.skills.length > 0" class="preview-section">
            <h4 class="preview-section-title">
              <va-icon name="psychology" size="small" />
              Habilidades
            </h4>
            <div class="preview-skills">
              <span 
                v-for="(skill, index) in cvData.skills"
                :key="index"
                class="preview-skill"
              >
                {{ skill }}
              </span>
            </div>
          </div>

          <!-- Idiomas -->
          <div v-if="cvData.languages.length > 0" class="preview-section">
            <h4 class="preview-section-title">
              <va-icon name="translate" size="small" />
              Idiomas
            </h4>
            <div class="preview-content">
              <p 
                v-for="(lang, index) in cvData.languages"
                :key="index"
              >
                <strong>{{ lang.name }}:</strong> {{ lang.level }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Botones de Navegación -->
    <div class="wizard-footer">
      <VaButton
        v-if="currentStepIndex > 0"
        preset="secondary"
        @click="previousStep"
      >
        <va-icon name="arrow_back" />
        Anterior
      </VaButton>

      <VaButton
        @click="cancelWizard"
        preset="secondary"
        color="danger"
      >
        Cancelar
      </VaButton>

      <div style="flex: 1;"></div>

      <VaButton
        v-if="currentStepIndex < steps.length - 1"
        color="purple"
        @click="nextStep"
      >
        Siguiente
        <va-icon name="arrow_forward" />
      </VaButton>

      <VaButton
        v-if="currentStepIndex === steps.length - 1"
        color="success"
        @click="saveCV"
        :loading="isSaving"
      >
        <va-icon name="save" />
        {{ saveButtonText }}
      </VaButton>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useToast } from 'vuestic-ui'

// ========== PROPS & EMITS ==========
const props = defineProps({
  existingCV: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['save', 'update', 'cancel'])

// ========== COMPOSABLES ==========
const { init: notify } = useToast()

// ========== STATE ==========
const currentStepIndex = ref(0)
const isSaving = ref(false)
const newSkill = ref('')

const steps = ref([
  { label: 'Datos Personales' },
  { label: 'Formación' },
  { label: 'Experiencia' },
  { label: 'Habilidades' },
  { label: 'Idiomas' },
  { label: 'Revisión' }
])

const cvData = ref({
  personalInfo: {
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    city: '',
    address: '',
    birthDate: null,
    gender: '',
    nationalId: '',
    linkedin: '',
    summary: ''
  },
  education: [],
  experience: [],
  skills: [],
  languages: []
})

// ========== OPTIONS ==========
const educationLevels = [
  'Bachiller',
  'Técnico Superior',
  'Licenciatura',
  'Ingeniería',
  'Maestría',
  'Doctorado',
  'Diplomado',
  'Otro'
]

const employmentTypes = [
  'Tiempo Completo',
  'Medio Tiempo',
  'Contrato',
  'Freelance',
  'Pasantía',
  'Voluntariado'
]

const languageLevels = [
  'Nativo',
  'Fluido / Avanzado',
  'Intermedio Alto',
  'Intermedio',
  'Básico'
]

// ========== COMPUTED ==========
const progressPercentage = computed(() => {
  return ((currentStepIndex.value + 1) / steps.value.length) * 100
})

const isEditing = computed(() => {
  return props.existingCV !== null
})

const saveButtonText = computed(() => {
  return isEditing.value ? 'Actualizar CV' : 'Guardar CV'
})

// ========== WATCH FOR EXISTING CV ==========
watch(() => props.existingCV, (newCV) => {
  if (newCV && newCV.data) {
    // Cargar datos del CV existente
    cvData.value = JSON.parse(JSON.stringify(newCV.data))
  }
}, { immediate: true })

// ========== METHODS - NAVIGATION ==========
const nextStep = () => {
  // Validar paso actual antes de avanzar
  if (!validateCurrentStep()) {
    return
  }

  if (currentStepIndex.value < steps.value.length - 1) {
    currentStepIndex.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const previousStep = () => {
  if (currentStepIndex.value > 0) {
    currentStepIndex.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const validateCurrentStep = () => {
  if (currentStepIndex.value === 0) {
    // Validar datos personales
    const pi = cvData.value.personalInfo
    if (!pi.firstName || !pi.lastName || !pi.email || !pi.phone || !pi.city || !pi.summary) {
      notify({
        message: '⚠️ Por favor completa todos los campos requeridos',
        color: 'warning'
      })
      return false
    }
  }
  return true
}

const cancelWizard = () => {
  if (confirm('¿Estás seguro de cancelar? Se perderán todos los cambios.')) {
    emit('cancel')
  }
}

// ========== METHODS - EDUCATION ==========
const addEducation = () => {
  cvData.value.education.push({
    level: '',
    institution: '',
    degree: '',
    field: '',
    startDate: null,
    endDate: null,
    current: false,
    description: ''
  })
}

const removeEducation = (index) => {
  cvData.value.education.splice(index, 1)
}

// ========== METHODS - EXPERIENCE ==========
const addExperience = () => {
  cvData.value.experience.push({
    position: '',
    company: '',
    location: '',
    employmentType: '',
    startDate: null,
    endDate: null,
    current: false,
    description: ''
  })
}

const removeExperience = (index) => {
  cvData.value.experience.splice(index, 1)
}

// ========== METHODS - SKILLS ==========
const addSkill = () => {
  if (newSkill.value.trim()) {
    cvData.value.skills.push(newSkill.value.trim())
    newSkill.value = ''
  }
}

const removeSkill = (index) => {
  cvData.value.skills.splice(index, 1)
}

// ========== METHODS - LANGUAGES ==========
const addLanguage = () => {
  cvData.value.languages.push({
    name: '',
    level: ''
  })
}

const removeLanguage = (index) => {
  cvData.value.languages.splice(index, 1)
}

// ========== METHODS - SAVE ==========
const saveCV = async () => {
  isSaving.value = true

  // Simular guardado
  await new Promise(resolve => setTimeout(resolve, 1500))

  if (isEditing.value) {
    notify({
      message: '✅ CV actualizado exitosamente',
      color: 'success',
      duration: 3000
    })
    emit('update', { id: props.existingCV.id, data: cvData.value })
  } else {
    notify({
      message: '✅ CV guardado exitosamente',
      color: 'success',
      duration: 3000
    })
    emit('save', cvData.value)
  }

  isSaving.value = false
}

// ========== HELPERS ==========
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('es-ES', {
    month: 'short',
    year: 'numeric'
  })
}
</script>

<style scoped>
/* ========== Container ========== */
.cv-form-wizard {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 10000;
}

/* ========== Header ========== */
.wizard-header {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.wizard-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.wizard-subtitle {
  color: #666;
  margin: 0 0 2rem 0;
  font-size: 1rem;
}

.progress-container {
  margin-bottom: 2rem;
}

.progress-text {
  display: block;
  text-align: center;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
}

/* ========== Steps Indicator ========== */
.steps-indicator {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  overflow-x: auto;
  padding: 1rem 0;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  min-width: 80px;
}

.step-circle {
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

.step-indicator.active .step-circle {
  background: var(--color-purple);
  color: white;
  transform: scale(1.1);
}

.step-indicator.completed .step-circle {
  background: #4CAF50;
  color: white;
}

.step-label {
  font-size: 0.75rem;
  color: #666;
  text-align: center;
  font-weight: 500;
}

.step-indicator.active .step-label {
  color: var(--color-purple);
  font-weight: 600;
}

/* ========== Content ========== */
.wizard-content {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  min-height: 500px;
}

.wizard-step {
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

.step-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 2rem 0;
  padding-bottom: 1rem;
  border-bottom: 2px solid #E0E0E0;
}

/* ========== Forms ========== */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-full-width {
  width: 100%;
  margin-bottom: 1.5rem;
}

.form-full-width .va-input-wrapper,
.form-full-width .va-textarea {
  width: 100% !important;
}

.full-width-textarea {
  width: 100% !important;
  margin-top: 1rem;
}

.full-width-textarea .va-input-wrapper,
.full-width-textarea .va-textarea {
  width: 100% !important;
}

.form-grid-small {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
}

/* ========== Repeatable Items ========== */
.add-btn {
  margin-bottom: 1.5rem;
}

.repeatable-item {
  padding: 2rem;
  background: #F8F8F8;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.repeatable-item-small {
  padding: 1.5rem;
  background: #F8F8F8;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.item-header h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin: 0;
}

/* ========== Empty States ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.empty-state p {
  color: #999;
  margin: 1rem 0;
  font-size: 1rem;
}

.empty-state-small {
  text-align: center;
  padding: 2rem;
}

.empty-state-small p {
  color: #999;
  margin: 0;
}

/* ========== Skills ========== */
.skills-section {
  margin-bottom: 1.5rem;
}

.skills-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

/* ========== Preview ========== */
.cv-preview-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.preview-section {
  padding: 1.5rem;
  background: #F8F8F8;
  border-radius: 12px;
}

.preview-section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #E0E0E0;
}

.preview-content p {
  margin: 0 0 0.5rem 0;
  color: #333;
  line-height: 1.6;
}

.preview-summary {
  margin-top: 1rem !important;
  font-style: italic;
  background: white;
  padding: 1rem;
  border-radius: 8px;
}

.preview-item {
  padding: 1rem;
  background: white;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.preview-item:last-child {
  margin-bottom: 0;
}

.preview-item h5 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.preview-item p {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.preview-date {
  color: #666 !important;
  font-size: 0.9rem;
  font-style: italic;
}

.preview-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preview-skill {
  padding: 0.5rem 1rem;
  background: var(--color-purple);
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

/* ========== Footer ========== */
.wizard-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .wizard-header,
  .wizard-content,
  .wizard-footer {
    padding: 1.5rem;
  }

  .wizard-title {
    font-size: 1.5rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-grid-small {
    grid-template-columns: 1fr;
  }

  .steps-indicator {
    gap: 0.25rem;
  }

  .step-indicator {
    min-width: 60px;
  }

  .step-circle {
    width: 32px;
    height: 32px;
  }

  .step-label {
    font-size: 0.65rem;
  }

  .wizard-footer {
    flex-wrap: wrap;
  }
}
</style>