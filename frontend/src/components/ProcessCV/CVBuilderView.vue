<!-- frontend/src/views/Dashboard/CVBuilderView.vue -->
<template>
  <div class="cv-builder-view">
    <div class="cv-builder-container">
      <!-- Header -->
      <div class="cv-builder-header">
        <button class="back-button" @click="handleBack">
          <va-icon name="arrow_back" size="20px" />
          Volver a Mis CVs
        </button>
        <h1 class="cv-builder-title">{{ isEditing ? 'Editar CV' : 'Crear CV Profesional Formato Harvard' }}</h1>
        <p class="cv-builder-subtitle">Completa la información para crear tu currículum profesional</p>
      </div>

      <!-- Steps Indicator -->
      <CVStepsIndicator :currentStep="currentStep" :steps="cvSteps" />

      <!-- Form Content -->
      <div class="cv-builder-content">
        <!-- Step 0: Información Personal -->
        <div v-if="currentStep === 0" class="step-content">
          <h2 class="step-heading">Información Personal</h2>
          <p class="step-description">Proporciona tus datos de contacto principales</p>

          <div class="form-grid">
            <va-input
              v-model="cvFormData.personalInfo.fullName"
              label="Nombre Completo"
              placeholder="Ej: Juan Carlos Pérez López"
              required-mark
              class="full-width"
            />
            <va-input
              v-model="cvFormData.personalInfo.phone"
              label="Teléfono"
              placeholder="+591 XXXXXXXX"
              required-mark
            />
            <va-input
              v-model="cvFormData.personalInfo.email"
              label="Correo Profesional"
              placeholder="correo.profesional@ejemplo.com"
              type="email"
              required-mark
            />
            <va-input
              v-model="cvFormData.personalInfo.location"
              label="Ciudad y País"
              placeholder="La Paz, Bolivia"
            />
            <va-input
              v-model="cvFormData.personalInfo.linkedin"
              label="LinkedIn"
              placeholder="linkedin.com/in/usuario"
            />
            <va-input
              v-model="cvFormData.personalInfo.portfolio"
              label="Portafolio / Sitio Web"
              placeholder="www.misitioweb.com"
            />
          </div>
        </div>

        <!-- Step 1: Perfil Profesional -->
        <div v-if="currentStep === 1" class="step-content">
          <h2 class="step-heading">Perfil Profesional</h2>
          <p class="step-description">Resume tu experiencia y valor profesional en 3-4 líneas</p>

          <va-textarea
            v-model="cvFormData.professionalProfile"
            placeholder="Resuma su experiencia, fortalezas clave y el valor que aporta. Ej: 'Profesional con 5+ años de experiencia en gestión comercial, especializado en desarrollo de estrategias y liderazgo de equipos. Comprobada capacidad para superar objetivos y aumentar la rentabilidad en un 30%.'"
            :min-rows="6"
            :max-rows="10"
            counter
            :max-length="500"
          />
          <p class="field-hint">Enfóquese en logros cuantificables y el impacto de su trabajo.</p>
        </div>

        <!-- Step 2: Experiencia Profesional -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="step-header-section">
            <div>
              <h2 class="step-heading">Experiencia Profesional</h2>
              <p class="step-description">Orden cronológico inverso. Enfatice logros medibles e impacto.</p>
            </div>
            <button class="add-btn" @click="addExperience">
              <va-icon name="add" size="small" />
              Agregar Experiencia
            </button>
          </div>

          <div v-if="cvFormData.experience.length === 0" class="empty-state">
            <va-icon name="work_outline" size="3rem" color="#D1D5DB" />
            <p>No ha agregado experiencia profesional</p>
          </div>

          <div v-for="(exp, index) in cvFormData.experience" :key="index" class="item-card">
            <div class="item-header">
              <span class="item-number">{{ index + 1 }}</span>
              <button class="remove-btn" @click="removeExperience(index)">
                <va-icon name="close" size="small" />
              </button>
            </div>

            <div class="form-grid">
              <va-input v-model="exp.startYear" label="Año Inicio" placeholder="YYYY" />
              <va-input v-model="exp.endYear" label="Año Fin" placeholder="YYYY o 'Actual'" :disabled="exp.current" />

              <div class="switch-wrapper">
                <label class="custom-switch">
                  <input type="checkbox" v-model="exp.current" />
                  <span class="custom-switch-slider"></span>
                </label>
                <span class="switch-text">Estado:</span>
                <span class="divider">|</span>
                <span class="switch-status" :class="{ active: exp.current }">
                  {{ exp.current ? 'Trabajo Actual' : 'Finalizado' }}
                </span>
              </div>

              <va-input v-model="exp.position" label="Cargo" placeholder="Ej: Gerente de Ventas Regional" class="full-width" />
              <va-input v-model="exp.company" label="Empresa" placeholder="Nombre de la empresa" class="full-width" />

              <div class="achievements-section full-width">
                <label class="achievements-label">Logros y Resultados (3-4 puntos clave)</label>
                <div v-for="(achievement, achIndex) in exp.achievements" :key="achIndex" class="achievement-input-wrapper">
                  <va-input
                    v-model="exp.achievements[achIndex]"
                    :placeholder="`Logro ${achIndex + 1}: Ej: 'Lideré equipo de 8 personas que superó las metas trimestrales en un 40%'`"
                  >
                    <template #append>
                      <button v-if="exp.achievements.length > 1" class="remove-achievement-btn" @click="removeAchievement(index, achIndex)">
                        <va-icon name="close" size="small" />
                      </button>
                    </template>
                  </va-input>
                </div>
                <button v-if="exp.achievements.length < 4" class="add-achievement-btn" @click="addAchievement(index)">
                  <va-icon name="add" size="small" />
                  Agregar logro
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3: Educación -->
        <div v-if="currentStep === 3" class="step-content">
          <div class="step-header-section">
            <div>
              <h2 class="step-heading">Educación</h2>
              <p class="step-description">Orden cronológico inverso (más reciente primero)</p>
            </div>
            <button class="add-btn" @click="addEducation">
              <va-icon name="add" size="small" />
              Agregar Educación
            </button>
          </div>

          <div v-if="cvFormData.education.length === 0" class="empty-state">
            <va-icon name="school" size="3rem" color="#D1D5DB" />
            <p>No ha agregado formación académica</p>
          </div>

          <div v-for="(edu, index) in cvFormData.education" :key="index" class="item-card">
            <div class="item-header">
              <span class="item-number">{{ index + 1 }}</span>
              <button class="remove-btn" @click="removeEducation(index)">
                <va-icon name="close" size="small" />
              </button>
            </div>

            <div class="form-grid">
              <va-input v-model="edu.startYear" label="Año Inicio" placeholder="YYYY" />
              <va-input v-model="edu.endYear" label="Año Fin" placeholder="YYYY o 'Actual'" />
              <va-input v-model="edu.degree" label="Título Obtenido" placeholder="Ej: Licenciatura en Administración de Empresas" class="full-width" />
              <va-input v-model="edu.institution" label="Institución" placeholder="Nombre de la universidad/instituto" class="full-width" />
              <va-textarea v-model="edu.achievements" label="Logros o Detalles Relevantes" placeholder="Ej: Graduado con mención honorífica" :min-rows="2" class="full-width" />
            </div>
          </div>
        </div>

        <!-- Step 4: Habilidades -->
        <div v-if="currentStep === 4" class="step-content">
          <h2 class="step-heading">Habilidades</h2>
          <p class="step-description">Agrega tus habilidades técnicas y blandas más relevantes</p>

          <!-- Habilidades Técnicas -->
          <div class="skills-subsection">
            <label class="subsection-label">Habilidades Técnicas</label>
            <div class="skills-input-wrapper">
              <va-input
                v-model="newTechnicalSkill"
                placeholder="Ej: Excel Avanzado, SAP, CRM Salesforce"
                @keyup.enter="addTechnicalSkill"
              >
                <template #append>
                  <button class="add-skill-btn" @click="addTechnicalSkill" :disabled="!newTechnicalSkill.trim()">
                    <va-icon name="add" size="small" />
                  </button>
                </template>
              </va-input>
            </div>
            <div v-if="cvFormData.technicalSkills.length > 0" class="skills-list">
              <div v-for="(skill, index) in cvFormData.technicalSkills" :key="index" class="skill-tag">
                <span>{{ skill }}</span>
                <button @click="removeTechnicalSkill(index)" class="remove-skill-btn">
                  <va-icon name="close" size="small" />
                </button>
              </div>
            </div>
          </div>

          <!-- Habilidades Blandas -->
          <div class="skills-subsection">
            <label class="subsection-label">Habilidades Blandas</label>
            <div class="skills-input-wrapper">
              <va-input
                v-model="newSoftSkill"
                placeholder="Ej: Liderazgo, Comunicación efectiva"
                @keyup.enter="addSoftSkill"
              >
                <template #append>
                  <button class="add-skill-btn" @click="addSoftSkill" :disabled="!newSoftSkill.trim()">
                    <va-icon name="add" size="small" />
                  </button>
                </template>
              </va-input>
            </div>
            <div v-if="cvFormData.softSkills.length > 0" class="skills-list">
              <div v-for="(skill, index) in cvFormData.softSkills" :key="index" class="skill-tag soft">
                <span>{{ skill }}</span>
                <button @click="removeSoftSkill(index)" class="remove-skill-btn">
                  <va-icon name="close" size="small" />
                </button>
              </div>
            </div>
          </div>

          <!-- Certificaciones, Idiomas, Proyectos -->
          <div class="additional-sections">
            <!-- Certificaciones -->
            <div class="subsection-card">
              <div class="subsection-header">
                <h3><va-icon name="verified" size="small" /> Certificaciones</h3>
                <button class="add-btn-small" @click="addCertification">
                  <va-icon name="add" size="small" />
                </button>
              </div>
              <div v-if="cvFormData.certifications.length === 0" class="mini-empty-state">
                <p>Sin certificaciones</p>
              </div>
              <div v-for="(cert, index) in cvFormData.certifications" :key="index" class="mini-item">
                <div class="mini-item-header">
                  <span class="mini-number">{{ index + 1 }}</span>
                  <button class="remove-btn-mini" @click="removeCertification(index)">
                    <va-icon name="close" size="12px" />
                  </button>
                </div>
                <div class="form-grid-mini">
                  <va-input v-model="cert.year" label="Año" placeholder="YYYY" />
                  <va-input v-model="cert.name" label="Certificación" placeholder="Nombre" class="full-width" />
                  <va-input v-model="cert.institution" label="Institución" placeholder="Institución" class="full-width" />
                </div>
              </div>
            </div>

            <!-- Idiomas -->
            <div class="subsection-card">
              <div class="subsection-header">
                <h3><va-icon name="language" size="small" /> Idiomas</h3>
                <button class="add-btn-small" @click="addLanguage">
                  <va-icon name="add" size="small" />
                </button>
              </div>
              <div v-if="cvFormData.languages.length === 0" class="mini-empty-state">
                <p>Sin idiomas</p>
              </div>
              <div v-for="(lang, index) in cvFormData.languages" :key="index" class="mini-item">
                <div class="mini-item-header">
                  <span class="mini-number">{{ index + 1 }}</span>
                  <button class="remove-btn-mini" @click="removeLanguage(index)">
                    <va-icon name="close" size="12px" />
                  </button>
                </div>
                <div class="form-grid-mini">
                  <va-input v-model="lang.name" label="Idioma" placeholder="Ej: Español" />
                  <div class="select-wrapper">
                    <label class="select-label">Nivel</label>
                    <select v-model="lang.level" class="custom-select">
                      <option value="" disabled>Selecciona</option>
                      <option value="Básico">Básico</option>
                      <option value="Intermedio">Intermedio</option>
                      <option value="Avanzado">Avanzado</option>
                      <option value="Nativo / Bilingüe">Nativo / Bilingüe</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <!-- Proyectos -->
            <div class="subsection-card">
              <div class="subsection-header">
                <h3><va-icon name="article" size="small" /> Proyectos (Opcional)</h3>
                <button class="add-btn-small" @click="addProject">
                  <va-icon name="add" size="small" />
                </button>
              </div>
              <div v-if="cvFormData.projects.length === 0" class="mini-empty-state">
                <p>Sin proyectos</p>
              </div>
              <div v-for="(project, index) in cvFormData.projects" :key="index" class="mini-item">
                <div class="mini-item-header">
                  <span class="mini-number">{{ index + 1 }}</span>
                  <button class="remove-btn-mini" @click="removeProject(index)">
                    <va-icon name="close" size="12px" />
                  </button>
                </div>
                <div class="form-grid-mini">
                  <va-input v-model="project.year" label="Año" placeholder="YYYY" />
                  <va-input v-model="project.name" label="Proyecto" placeholder="Nombre" class="full-width" />
                  <va-textarea v-model="project.description" label="Descripción" placeholder="Impacto y resultados" :min-rows="2" class="full-width" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 5: Vista Previa -->
        <div v-if="currentStep === 5" class="step-content">
          <h2 class="step-heading">Vista Previa</h2>
          <p class="step-description">Revisa tu información antes de guardar</p>

          <div class="preview-container">
            <div class="preview-section">
              <h3>📋 Información Personal</h3>
              <p><strong>Nombre:</strong> {{ cvFormData.personalInfo.fullName || 'Sin especificar' }}</p>
              <p><strong>Email:</strong> {{ cvFormData.personalInfo.email || 'Sin especificar' }}</p>
              <p><strong>Teléfono:</strong> {{ cvFormData.personalInfo.phone || 'Sin especificar' }}</p>
              <p v-if="cvFormData.personalInfo.location"><strong>Ubicación:</strong> {{ cvFormData.personalInfo.location }}</p>
            </div>

            <div class="preview-section" v-if="cvFormData.professionalProfile">
              <h3>💼 Perfil Profesional</h3>
              <p>{{ cvFormData.professionalProfile }}</p>
            </div>

            <div class="preview-section" v-if="cvFormData.experience.length > 0">
              <h3>🏢 Experiencia ({{ cvFormData.experience.length }})</h3>
              <div v-for="(exp, i) in cvFormData.experience" :key="i" class="preview-item">
                <p><strong>{{ exp.position }}</strong> en {{ exp.company }}</p>
                <p class="text-muted">{{ exp.startYear }} - {{ exp.current ? 'Actual' : exp.endYear }}</p>
              </div>
            </div>

            <div class="preview-section" v-if="cvFormData.education.length > 0">
              <h3>🎓 Educación ({{ cvFormData.education.length }})</h3>
              <div v-for="(edu, i) in cvFormData.education" :key="i" class="preview-item">
                <p><strong>{{ edu.degree }}</strong></p>
                <p class="text-muted">{{ edu.institution }} ({{ edu.startYear }} - {{ edu.endYear }})</p>
              </div>
            </div>

            <div class="preview-section" v-if="cvFormData.technicalSkills.length > 0 || cvFormData.softSkills.length > 0">
              <h3>💡 Habilidades</h3>
              <p v-if="cvFormData.technicalSkills.length > 0"><strong>Técnicas:</strong> {{ cvFormData.technicalSkills.join(', ') }}</p>
              <p v-if="cvFormData.softSkills.length > 0"><strong>Blandas:</strong> {{ cvFormData.softSkills.join(', ') }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="cv-builder-actions">
        <button
          v-if="currentStep > 0"
          class="action-btn secondary-btn"
          @click="previousStep"
        >
          <va-icon name="arrow_back" size="18px" />
          Anterior
        </button>

        <button
          v-if="currentStep < cvSteps.length - 1"
          class="action-btn primary-btn"
          @click="nextStep"
        >
          Siguiente
          <va-icon name="arrow_forward" size="18px" />
        </button>

        <button
          v-else
          class="action-btn save-btn"
          @click="saveCV"
          :disabled="!isValidCV"
        >
          <va-icon name="save" size="18px" />
          {{ isEditing ? 'Actualizar CV' : 'Guardar CV' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'
import CVStepsIndicator from './CVStepsIndicator.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { init: initToast } = useToast()

// State
const currentStep = ref(0)
const cvFormData = ref({
  personalInfo: {
    fullName: '',
    phone: '',
    email: '',
    location: '',
    linkedin: '',
    portfolio: ''
  },
  professionalProfile: '',
  education: [],
  experience: [],
  technicalSkills: [],
  softSkills: [],
  certifications: [],
  languages: [],
  projects: []
})

const isEditing = ref(false)
const editingCVId = ref(null)

// Skills state
const newTechnicalSkill = ref('')
const newSoftSkill = ref('')

// Steps configuration
const cvSteps = [
  { name: 'Información Personal', description: 'Datos básicos' },
  { name: 'Perfil Profesional', description: 'Sobre ti' },
  { name: 'Experiencia', description: 'Historial laboral' },
  { name: 'Educación', description: 'Formación académica' },
  { name: 'Habilidades', description: 'Competencias' },
  { name: 'Vista Previa', description: 'Revisión final' }
]

// Computed
const isValidCV = computed(() => {
  const info = cvFormData.value?.personalInfo
  if (!info) return false

  return (
    info.fullName?.trim().length > 0 &&
    info.email?.trim().length > 0 &&
    info.phone?.trim().length > 0
  )
})

// Methods
const nextStep = () => {
  if (currentStep.value < cvSteps.length - 1) {
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

const handleBack = () => {
  if (confirm('¿Estás seguro? Se perderán todos los cambios no guardados.')) {
    router.push('/dashboard/cv')
  }
}

// Education functions
const addEducation = () => {
  cvFormData.value.education.push({
    startYear: '',
    endYear: '',
    degree: '',
    institution: '',
    achievements: ''
  })
}

const removeEducation = (index) => {
  cvFormData.value.education.splice(index, 1)
}

// Experience functions
const addExperience = () => {
  cvFormData.value.experience.push({
    startYear: '',
    endYear: '',
    current: false,
    position: '',
    company: '',
    achievements: ['', '', '']
  })
}

const removeExperience = (index) => {
  cvFormData.value.experience.splice(index, 1)
}

const addAchievement = (expIndex) => {
  if (cvFormData.value.experience[expIndex].achievements.length < 4) {
    cvFormData.value.experience[expIndex].achievements.push('')
  }
}

const removeAchievement = (expIndex, achIndex) => {
  cvFormData.value.experience[expIndex].achievements.splice(achIndex, 1)
}

// Technical Skills functions
const addTechnicalSkill = () => {
  const skill = newTechnicalSkill.value.trim()
  if (skill && !cvFormData.value.technicalSkills.includes(skill)) {
    cvFormData.value.technicalSkills.push(skill)
    newTechnicalSkill.value = ''
  }
}

const removeTechnicalSkill = (index) => {
  cvFormData.value.technicalSkills.splice(index, 1)
}

// Soft Skills functions
const addSoftSkill = () => {
  const skill = newSoftSkill.value.trim()
  if (skill && !cvFormData.value.softSkills.includes(skill)) {
    cvFormData.value.softSkills.push(skill)
    newSoftSkill.value = ''
  }
}

const removeSoftSkill = (index) => {
  cvFormData.value.softSkills.splice(index, 1)
}

// Certifications functions
const addCertification = () => {
  cvFormData.value.certifications.push({
    year: '',
    name: '',
    institution: ''
  })
}

const removeCertification = (index) => {
  cvFormData.value.certifications.splice(index, 1)
}

// Languages functions
const addLanguage = () => {
  cvFormData.value.languages.push({
    name: '',
    level: 'Básico'
  })
}

const removeLanguage = (index) => {
  cvFormData.value.languages.splice(index, 1)
}

// Projects functions
const addProject = () => {
  cvFormData.value.projects.push({
    year: '',
    name: '',
    description: ''
  })
}

const removeProject = (index) => {
  cvFormData.value.projects.splice(index, 1)
}

const saveCV = async () => {
  if (!isValidCV.value) {
    initToast({
      message: 'Por favor completa los campos obligatorios (Nombre, Email, Teléfono)',
      color: 'warning',
      duration: 3000
    })
    return
  }

  try {
    const cvName = `CV - ${cvFormData.value.personalInfo.fullName}`

    if (isEditing.value && editingCVId.value) {
      // Update existing CV
      const response = await fetch(`http://localhost:8000/api/cvs/${editingCVId.value}/update/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: cvName,
          cv_data: cvFormData.value
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Error al actualizar CV')
      }

      initToast({
        message: 'CV actualizado exitosamente',
        color: 'success',
        duration: 3000
      })
    } else {
      // Create new CV
      const response = await fetch('http://localhost:8000/api/cvs/save/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          cv_type: 'created',
          name: cvName,
          cv_data: cvFormData.value
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Error al guardar CV')
      }

      initToast({
        message: 'CV creado exitosamente',
        color: 'success',
        duration: 3000
      })
    }

    // Redirect back to CVs list
    router.push('/dashboard')
  } catch (error) {
    console.error('Error saving CV:', error)
    initToast({
      message: error.message,
      color: 'danger',
      duration: 3000
    })
  }
}

// Load CV if editing
onMounted(async () => {
  const cvId = route.query.edit
  if (cvId) {
    isEditing.value = true
    editingCVId.value = cvId

    try {
      const response = await fetch(`http://localhost:8000/api/cvs/${cvId}/`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })

      if (!response.ok) {
        throw new Error('Error al cargar CV')
      }

      const data = await response.json()
      cvFormData.value = data.cv.cv_data || cvFormData.value
    } catch (error) {
      console.error('Error loading CV:', error)
      initToast({
        message: 'Error al cargar CV para edición',
        color: 'danger',
        duration: 3000
      })
    }
  }
})
</script>

<style scoped>
.cv-builder-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
  padding: 2rem 1rem;
}

.cv-builder-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.cv-builder-header {
  text-align: center;
  margin-bottom: 2rem;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  color: #6b7280;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 1.5rem;
}

.back-button:hover {
  border-color: #7c3aed;
  color: #7c3aed;
  transform: translateX(-4px);
}

.cv-builder-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cv-builder-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin: 0;
}

/* Content */
.cv-builder-content {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  margin-bottom: 2rem;
}

/* Actions */
.cv-builder-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.action-btn {
  flex: 1;
  max-width: 250px;
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 15px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.primary-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
  margin-left: auto;
}

.primary-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
}

.secondary-btn {
  background: white;
  color: #6b7280;
  border: 2px solid #e5e7eb;
}

.secondary-btn:hover {
  border-color: #7c3aed;
  color: #7c3aed;
}

.save-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
  margin-left: auto;
}

.save-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35);
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Step Content */
.step-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.step-heading {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.step-description {
  font-size: 1rem;
  color: #6b7280;
  margin: -0.5rem 0 0;
}

.step-header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.field-hint {
  font-size: 0.875rem;
  color: #6b7280;
  margin: -0.5rem 0 0;
  font-style: italic;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.full-width {
  grid-column: 1 / -1;
}

/* Buttons */
.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: white;
  border: 2px solid #7c3aed;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #7c3aed;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-btn:hover {
  background: #7c3aed;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.2);
}

.add-btn-small {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  background: white;
  border: 1.5px solid #7c3aed;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #7c3aed;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-btn-small:hover {
  background: #7c3aed;
  color: white;
}

/* Item Cards */
.item-card {
  background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.item-card:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.item-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 28px;
  padding: 0 0.5rem;
  background: #7c3aed;
  color: white;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 700;
}

.remove-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-btn:hover {
  background: #fef2f2;
  border-color: #fca5a5;
  color: #dc2626;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
  background: #f9fafb;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
}

.empty-state p {
  margin: 0.75rem 0 0;
  font-size: 0.9375rem;
  color: #9ca3af;
  font-weight: 500;
}

/* Switch */
.switch-wrapper {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1.125rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.switch-text {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #6b7280;
  margin-left: 0.5rem;
}

.divider {
  color: #d1d5db;
  margin: 0 0.375rem;
}

.switch-status {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #6b7280;
  transition: color 0.2s ease;
}

.switch-status.active {
  color: #10b981;
}

.custom-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 22px;
  cursor: pointer;
}

.custom-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.custom-switch-slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #d1d5db;
  border-radius: 22px;
  transition: all 0.3s ease;
}

.custom-switch-slider::before {
  content: "";
  position: absolute;
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.custom-switch input:checked + .custom-switch-slider {
  background-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.custom-switch input:checked + .custom-switch-slider::before {
  transform: translateX(22px);
}

/* Achievements */
.achievements-section {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
  padding: 1.125rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.achievements-label {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #374151;
}

.achievement-input-wrapper {
  display: flex;
  gap: 0.5rem;
}

.remove-achievement-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-achievement-btn:hover {
  color: #dc2626;
}

.add-achievement-btn {
  align-self: flex-start;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-achievement-btn:hover {
  background: #f9fafb;
  border-color: #7c3aed;
  color: #7c3aed;
}

/* Skills */
.skills-subsection {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
  padding: 1.125rem;
  background: #f9fafb;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
}

.subsection-label {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.skills-input-wrapper {
  margin-bottom: 0.5rem;
}

.add-skill-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: #7c3aed;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-skill-btn:hover:not(:disabled) {
  background: #6d28d9;
  transform: scale(1.05);
}

.add-skill-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
}

.skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.875rem;
  background: white;
  border: 2px solid #7c3aed;
  border-radius: 20px;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #7c3aed;
  transition: all 0.2s ease;
}

.skill-tag:hover {
  background: #f3f4f6;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(124, 58, 237, 0.1);
}

.skill-tag.soft {
  border-color: #10b981;
  color: #10b981;
}

.remove-skill-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: transparent;
  border: none;
  border-radius: 50%;
  color: currentColor;
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0.7;
}

.remove-skill-btn:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.08);
}

/* Additional Sections */
.additional-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.subsection-card {
  background: #fafafa;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1rem;
}

.subsection-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.875rem;
}

.subsection-header h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.mini-empty-state {
  padding: 1.5rem;
  text-align: center;
  background: white;
  border: 1px dashed #d1d5db;
  border-radius: 8px;
}

.mini-empty-state p {
  margin: 0;
  font-size: 0.875rem;
  color: #9ca3af;
}

.mini-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.875rem;
  margin-bottom: 0.75rem;
}

.mini-item:last-child {
  margin-bottom: 0;
}

.mini-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.mini-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 0.375rem;
  background: #7c3aed;
  color: white;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
}

.remove-btn-mini {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  color: #9ca3af;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-btn-mini:hover {
  background: #fef2f2;
  border-color: #fca5a5;
  color: #dc2626;
}

.form-grid-mini {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

/* Select */
.select-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.select-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.custom-select {
  width: 100%;
  padding: 0.625rem 0.875rem;
  font-size: 1rem;
  color: #1f2937;
  background-color: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.custom-select:hover {
  border-color: #9ca3af;
}

.custom-select:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

/* Preview */
.preview-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.preview-section {
  padding: 1.5rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.preview-section h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 1rem 0;
}

.preview-section p {
  font-size: 0.9375rem;
  color: #374151;
  margin: 0.5rem 0;
  line-height: 1.6;
}

.preview-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.preview-item:last-child {
  border-bottom: none;
}

.text-muted {
  color: #6b7280 !important;
  font-size: 0.875rem !important;
}

/* Responsive */
@media (max-width: 768px) {
  .cv-builder-view {
    padding: 1rem 0.5rem;
  }

  .cv-builder-title {
    font-size: 1.75rem;
  }

  .cv-builder-subtitle {
    font-size: 1rem;
  }

  .cv-builder-content {
    padding: 1.5rem;
  }

  .cv-builder-actions {
    flex-direction: column;
    padding: 1rem;
  }

  .action-btn {
    max-width: 100%;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: 1;
  }

  .step-header-section {
    flex-direction: column;
    align-items: stretch;
  }

  .add-btn {
    width: 100%;
    justify-content: center;
  }

  .additional-sections {
    grid-template-columns: 1fr;
  }

  .step-heading {
    font-size: 1.5rem;
  }
}
</style>
