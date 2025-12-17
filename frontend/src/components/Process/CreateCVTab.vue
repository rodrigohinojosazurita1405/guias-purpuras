<template>
  <div class="create-cv-container">
    <div class="intro-banner">
      <va-icon name="workspace_premium" size="1.5rem" color="#7C3AED" />
      <div class="intro-content">
        <h2 class="intro-title">Crea tu CV Profesional</h2>
        <p class="intro-subtitle">Complete los campos siguiendo el formato Harvard para destacar ante los empleadores</p>
      </div>
    </div>

    <!-- 1. Datos Personales -->
    <section class="cv-section">
      <h3 class="section-title">
        <va-icon name="person" size="small" />
        Datos Personales
      </h3>
      <div class="form-grid">
        <va-input
          v-model="localData.personalInfo.fullName"
          label="Nombre Completo"
          placeholder="Ej: Juan Carlos Pérez López"
          required-mark
          class="full-width"
        />
        <va-input
          v-model="localData.personalInfo.phone"
          label="Teléfono"
          placeholder="+591 XXXXXXXX"
          required-mark
        />
        <va-input
          v-model="localData.personalInfo.email"
          label="Correo Profesional"
          placeholder="correo.profesional@ejemplo.com"
          type="email"
          required-mark
        />
        <va-input
          v-model="localData.personalInfo.location"
          label="Ciudad y País"
          placeholder="La Paz, Bolivia"
          required-mark
        />
        <va-input
          v-model="localData.personalInfo.linkedin"
          label="LinkedIn"
          placeholder="linkedin.com/in/usuario"
        />
        <va-input
          v-model="localData.personalInfo.portfolio"
          label="Portafolio / Sitio Web"
          placeholder="www.misitioweb.com"
        />
      </div>
    </section>

    <!-- 2. Perfil Profesional -->
    <section class="cv-section">
      <h3 class="section-title">
        <va-icon name="badge" size="small" />
        Perfil Profesional
      </h3>
      <va-textarea
        v-model="localData.professionalProfile"
        placeholder="Resuma su experiencia, fortalezas clave y el valor que aporta en 3-4 líneas. Ej: 'Profesional con 5+ años de experiencia en gestión comercial, especializado en desarrollo de estrategias y liderazgo de equipos. Comprobada capacidad para superar objetivos y aumentar la rentabilidad en un 30%.'"
        :min-rows="4"
        :max-rows="6"
        counter
        :max-length="500"
      />
      <p class="field-hint">Enfóquese en logros cuantificables y el impacto de su trabajo.</p>
    </section>

    <!-- 3. Educación -->
    <section class="cv-section">
      <div class="section-header">
        <h3 class="section-title">
          <va-icon name="school" size="small" />
          Educación
        </h3>
        <button class="add-btn" @click="addEducation">
          <va-icon name="add" size="small" />
          Agregar
        </button>
      </div>
      <p class="section-hint">Orden cronológico inverso (más reciente primero)</p>

      <div v-if="localData.education.length === 0" class="empty-state">
        <va-icon name="school" size="2rem" color="#D1D5DB" />
        <p>No ha agregado formación académica</p>
      </div>

      <div
        v-for="(edu, index) in localData.education"
        :key="index"
        class="item-card"
      >
        <div class="item-header">
          <span class="item-number">{{ index + 1 }}</span>
          <button class="remove-btn" @click="removeEducation(index)">
            <va-icon name="close" size="small" />
          </button>
        </div>

        <div class="form-grid">
          <va-input
            v-model="edu.startYear"
            label="Año Inicio"
            placeholder="YYYY"
          />
          <va-input
            v-model="edu.endYear"
            label="Año Fin"
            placeholder="YYYY o 'Actual'"
          />
          <va-input
            v-model="edu.degree"
            label="Título Obtenido"
            placeholder="Ej: Licenciatura en Administración de Empresas"
            class="full-width"
          />
          <va-input
            v-model="edu.institution"
            label="Institución"
            placeholder="Nombre de la universidad/instituto"
            class="full-width"
          />
          <va-textarea
            v-model="edu.achievements"
            label="Logros o Detalles Relevantes"
            placeholder="Ej: Graduado con mención honorífica, Primero de mi promoción, Beca otorgada por rendimiento académico"
            :min-rows="2"
            class="full-width"
          />
        </div>
      </div>
    </section>

    <!-- 4. Experiencia Profesional -->
    <section class="cv-section">
      <div class="section-header">
        <h3 class="section-title">
          <va-icon name="work" size="small" />
          Experiencia Profesional
        </h3>
        <button class="add-btn" @click="addExperience">
          <va-icon name="add" size="small" />
          Agregar
        </button>
      </div>
      <p class="section-hint">Orden cronológico inverso. Enfatice logros medibles e impacto.</p>

      <div v-if="localData.experience.length === 0" class="empty-state">
        <va-icon name="work_outline" size="2rem" color="#D1D5DB" />
        <p>No ha agregado experiencia profesional</p>
      </div>

      <div
        v-for="(exp, index) in localData.experience"
        :key="index"
        class="item-card"
      >
        <div class="item-header">
          <span class="item-number">{{ index + 1 }}</span>
          <button class="remove-btn" @click="removeExperience(index)">
            <va-icon name="close" size="small" />
          </button>
        </div>

        <div class="form-grid">
          <va-input
            v-model="exp.startYear"
            label="Año Inicio"
            placeholder="YYYY"
          />
          <va-input
            v-model="exp.endYear"
            label="Año Fin"
            placeholder="YYYY o 'Actual'"
            :disabled="exp.current"
          />
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
          <va-input
            v-model="exp.position"
            label="Cargo"
            placeholder="Ej: Gerente de Ventas Regional"
            class="full-width"
          />
          <va-input
            v-model="exp.company"
            label="Empresa"
            placeholder="Nombre de la empresa"
            class="full-width"
          />

          <!-- Logros (3-4 bullets) -->
          <div class="achievements-section full-width">
            <label class="achievements-label">Logros y Resultados (3-4 puntos clave)</label>
            <div
              v-for="(achievement, achIndex) in exp.achievements"
              :key="achIndex"
              class="achievement-input-wrapper"
            >
              <va-input
                v-model="exp.achievements[achIndex]"
                :placeholder="`Logro ${achIndex + 1}: Ej: 'Lideré equipo de 8 personas que superó las metas trimestrales en un 40%'`"
              >
                <template #append>
                  <button
                    v-if="exp.achievements.length > 1"
                    class="remove-achievement-btn"
                    @click="removeAchievement(index, achIndex)"
                  >
                    <va-icon name="close" size="small" />
                  </button>
                </template>
              </va-input>
            </div>
            <button
              v-if="exp.achievements.length < 4"
              class="add-achievement-btn"
              @click="addAchievement(index)"
            >
              <va-icon name="add" size="small" />
              Agregar logro
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. Habilidades -->
    <section class="cv-section">
      <h3 class="section-title">
        <va-icon name="lightbulb" size="small" />
        Habilidades
      </h3>

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
              <button
                class="add-skill-btn"
                @click="addTechnicalSkill"
                :disabled="!newTechnicalSkill.trim()"
              >
                <va-icon name="add" size="small" />
              </button>
            </template>
          </va-input>
        </div>
        <div v-if="localData.technicalSkills.length > 0" class="skills-list">
          <div
            v-for="(skill, index) in localData.technicalSkills"
            :key="index"
            class="skill-tag"
          >
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
              <button
                class="add-skill-btn"
                @click="addSoftSkill"
                :disabled="!newSoftSkill.trim()"
              >
                <va-icon name="add" size="small" />
              </button>
            </template>
          </va-input>
        </div>
        <div v-if="localData.softSkills.length > 0" class="skills-list">
          <div
            v-for="(skill, index) in localData.softSkills"
            :key="index"
            class="skill-tag soft"
          >
            <span>{{ skill }}</span>
            <button @click="removeSoftSkill(index)" class="remove-skill-btn">
              <va-icon name="close" size="small" />
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. Certificaciones -->
    <section class="cv-section">
      <div class="section-header">
        <h3 class="section-title">
          <va-icon name="verified" size="small" />
          Certificaciones
        </h3>
        <button class="add-btn" @click="addCertification">
          <va-icon name="add" size="small" />
          Agregar
        </button>
      </div>

      <div v-if="localData.certifications.length === 0" class="empty-state">
        <va-icon name="verified" size="2rem" color="#D1D5DB" />
        <p>No ha agregado certificaciones</p>
      </div>

      <div
        v-for="(cert, index) in localData.certifications"
        :key="index"
        class="item-card compact"
      >
        <div class="item-header">
          <span class="item-number">{{ index + 1 }}</span>
          <button class="remove-btn" @click="removeCertification(index)">
            <va-icon name="close" size="small" />
          </button>
        </div>

        <div class="form-grid">
          <va-input
            v-model="cert.year"
            label="Año"
            placeholder="YYYY"
          />
          <va-input
            v-model="cert.name"
            label="Nombre de la Certificación"
            placeholder="Ej: Certificación en Gestión de Proyectos PMP"
            class="full-width"
          />
          <va-input
            v-model="cert.institution"
            label="Institución Emisora"
            placeholder="Ej: Project Management Institute"
            class="full-width"
          />
        </div>
      </div>
    </section>

    <!-- 7. Idiomas -->
    <section class="cv-section">
      <div class="section-header">
        <h3 class="section-title">
          <va-icon name="language" size="small" />
          Idiomas
        </h3>
        <button class="add-btn" @click="addLanguage">
          <va-icon name="add" size="small" />
          Agregar
        </button>
      </div>

      <div v-if="localData.languages.length === 0" class="empty-state">
        <va-icon name="language" size="2rem" color="#D1D5DB" />
        <p>No ha agregado idiomas</p>
      </div>

      <div
        v-for="(lang, index) in localData.languages"
        :key="index"
        class="item-card compact"
      >
        <div class="item-header">
          <span class="item-number">{{ index + 1 }}</span>
          <button class="remove-btn" @click="removeLanguage(index)">
            <va-icon name="close" size="small" />
          </button>
        </div>

        <div class="form-grid">
          <va-input
            v-model="lang.name"
            label="Idioma"
            placeholder="Ej: Español"
          />
          <div class="select-wrapper">
            <label class="select-label">Nivel</label>
            <select v-model="lang.level" class="custom-select">
              <option value="" disabled>Selecciona el nivel</option>
              <option value="Básico">Básico</option>
              <option value="Intermedio">Intermedio</option>
              <option value="Avanzado">Avanzado</option>
              <option value="Nativo / Bilingüe">Nativo / Bilingüe</option>
            </select>
          </div>
        </div>
      </div>
    </section>

    <!-- 8. Proyectos o Publicaciones (Opcional) -->
    <section class="cv-section">
      <div class="section-header">
        <h3 class="section-title">
          <va-icon name="article" size="small" />
          Proyectos o Publicaciones (Opcional)
        </h3>
        <button class="add-btn" @click="addProject">
          <va-icon name="add" size="small" />
          Agregar
        </button>
      </div>

      <div v-if="localData.projects.length === 0" class="empty-state">
        <va-icon name="article" size="2rem" color="#D1D5DB" />
        <p>No ha agregado proyectos o publicaciones</p>
      </div>

      <div
        v-for="(project, index) in localData.projects"
        :key="index"
        class="item-card compact"
      >
        <div class="item-header">
          <span class="item-number">{{ index + 1 }}</span>
          <button class="remove-btn" @click="removeProject(index)">
            <va-icon name="close" size="small" />
          </button>
        </div>

        <div class="form-grid">
          <va-input
            v-model="project.year"
            label="Año"
            placeholder="YYYY"
          />
          <va-input
            v-model="project.name"
            label="Nombre del Proyecto"
            placeholder="Ej: Implementación de nuevo sistema de ventas"
            class="full-width"
          />
          <va-textarea
            v-model="project.description"
            label="Descripción del Aporte o Impacto"
            placeholder="Ej: 'Lideré implementación que aumentó las ventas en un 50%, generando $500K adicionales'"
            :min-rows="2"
            class="full-width"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const localData = ref({
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

const newTechnicalSkill = ref('')
const newSoftSkill = ref('')

const languageLevels = ['Básico', 'Intermedio', 'Avanzado', 'Nativo / Bilingüe']

watch(localData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

watch(() => props.modelValue, (newValue) => {
  if (newValue && Object.keys(newValue.personalInfo || {}).length > 0) {
    localData.value = JSON.parse(JSON.stringify(newValue))
  }
}, { deep: true, immediate: true })

// Education
const addEducation = () => {
  localData.value.education.push({
    startYear: '',
    endYear: '',
    degree: '',
    institution: '',
    achievements: ''
  })
}

const removeEducation = (index) => {
  localData.value.education.splice(index, 1)
}

// Experience
const addExperience = () => {
  localData.value.experience.push({
    startYear: '',
    endYear: '',
    current: false,
    position: '',
    company: '',
    achievements: ['', '', '']
  })
}

const removeExperience = (index) => {
  localData.value.experience.splice(index, 1)
}

const addAchievement = (expIndex) => {
  if (localData.value.experience[expIndex].achievements.length < 4) {
    localData.value.experience[expIndex].achievements.push('')
  }
}

const removeAchievement = (expIndex, achIndex) => {
  localData.value.experience[expIndex].achievements.splice(achIndex, 1)
}

// Technical Skills
const addTechnicalSkill = () => {
  const skill = newTechnicalSkill.value.trim()
  if (skill && !localData.value.technicalSkills.includes(skill)) {
    localData.value.technicalSkills.push(skill)
    newTechnicalSkill.value = ''
  }
}

const removeTechnicalSkill = (index) => {
  localData.value.technicalSkills.splice(index, 1)
}

// Soft Skills
const addSoftSkill = () => {
  const skill = newSoftSkill.value.trim()
  if (skill && !localData.value.softSkills.includes(skill)) {
    localData.value.softSkills.push(skill)
    newSoftSkill.value = ''
  }
}

const removeSoftSkill = (index) => {
  localData.value.softSkills.splice(index, 1)
}

// Certifications
const addCertification = () => {
  localData.value.certifications.push({
    year: '',
    name: '',
    institution: ''
  })
}

const removeCertification = (index) => {
  localData.value.certifications.splice(index, 1)
}

// Languages
const addLanguage = () => {
  localData.value.languages.push({
    name: '',
    level: 'Básico'
  })
}

const removeLanguage = (index) => {
  localData.value.languages.splice(index, 1)
}

// Projects
const addProject = () => {
  localData.value.projects.push({
    year: '',
    name: '',
    description: ''
  })
}

const removeProject = (index) => {
  localData.value.projects.splice(index, 1)
}
</script>

<style scoped>
.create-cv-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.intro-banner {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.08), rgba(109, 40, 217, 0.05));
  border: 1px solid rgba(124, 58, 237, 0.15);
  border-radius: 12px;
  margin-bottom: 0;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.08);
}

.intro-content {
  flex: 1;
}

.intro-title {
  margin: 0 0 0.25rem;
  font-size: 1.0625rem;
  font-weight: 700;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.01em;
}

.intro-subtitle {
  margin: 0;
  font-size: 0.8125rem;
  color: #6B7280;
  line-height: 1.4;
}

.cv-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
}

.section-hint {
  margin: -0.5rem 0 0;
  font-size: 0.8125rem;
  color: #9CA3AF;
  font-style: italic;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1.5px solid #7C3AED;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #7C3AED;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  background: #7C3AED;
  color: white;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.full-width {
  grid-column: 1 / -1;
}

.checkbox-wrapper {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
}

.switch-wrapper {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #F9FAFB;
  border-radius: 8px;
  border: 1px solid #E5E7EB;
}

.switch-text {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6B7280;
  margin-left: 0.5rem;
}

.switch-wrapper .divider {
  color: #D1D5DB;
  font-weight: 300;
  margin: 0 0.25rem;
}

.switch-status {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
  transition: color 0.2s;
}

.switch-status.active {
  color: #10B981;
}

.switch-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.switch-label-slot {
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Select personalizado para idiomas */
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
  font-family: inherit;
  color: #1F2937;
  background-color: white;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236B7280' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 12px;
  border: 1px solid #D1D5DB;
  border-radius: 8px;
  appearance: none;
  cursor: pointer;
  transition: all 0.2s;
}

.custom-select:hover {
  border-color: #9CA3AF;
}

.custom-select:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.custom-select:disabled {
  background-color: #F3F4F6;
  cursor: not-allowed;
  opacity: 0.6;
}

.item-card {
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item-card.compact {
  padding: 1rem;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.item-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: #7C3AED;
  color: white;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 700;
}

.remove-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 50%;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: #FEF2F2;
  border-color: #FCA5A5;
  color: #DC2626;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  background: #F9FAFB;
  border: 1px dashed #D1D5DB;
  border-radius: 8px;
}

.empty-state p {
  margin: 0.5rem 0 0;
  font-size: 0.875rem;
  color: #9CA3AF;
}

.field-hint {
  margin: -0.25rem 0 0;
  font-size: 0.8125rem;
  color: #6B7280;
  line-height: 1.4;
}

/* Achievements */
.achievements-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #E5E7EB;
}

.achievements-label {
  font-size: 0.875rem;
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
  width: 28px;
  height: 28px;
  background: transparent;
  border: none;
  color: #9CA3AF;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-achievement-btn:hover {
  color: #DC2626;
}

.add-achievement-btn {
  align-self: flex-start;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: white;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
}

.add-achievement-btn:hover {
  background: #F9FAFB;
  border-color: #7C3AED;
  color: #7C3AED;
}

/* Skills */
.skills-subsection {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 8px;
  border: 1px solid #E5E7EB;
}

.subsection-label {
  font-size: 0.9375rem;
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
  width: 32px;
  height: 32px;
  background: #7C3AED;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.add-skill-btn:hover:not(:disabled) {
  background: #6D28D9;
}

.add-skill-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: white;
  border: 1px solid #7C3AED;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #7C3AED;
}

.skill-tag.soft {
  border-color: #10B981;
  color: #10B981;
}

.remove-skill-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background: transparent;
  border: none;
  border-radius: 50%;
  color: currentColor;
  cursor: pointer;
  transition: all 0.2s;
  opacity: 0.6;
}

.remove-skill-btn:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.05);
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: 1;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .add-btn {
    width: 100%;
    justify-content: center;
  }
}

/* Sobrescribir estilos de Vuestic para mejorar la apariencia de los formularios */
:deep(.va-input-wrapper__label),
:deep(.va-textarea__label) {
  text-transform: none !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  color: #374151 !important;
  margin-bottom: 0.375rem !important;
}

:deep(.va-input-wrapper__field),
:deep(.va-textarea__wrapper) {
  border-radius: 8px !important;
}

:deep(.va-input-wrapper__field:focus-within),
:deep(.va-textarea__wrapper:focus-within) {
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
  border-color: #7C3AED !important;
}

/* Mejorar apariencia de las tarjetas de items */
.item-card {
  background: linear-gradient(135deg, #FAFAFA 0%, #F5F5F5 100%);
  border: 1px solid #E5E7EB;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.item-card:hover {
  border-color: #D1D5DB;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

/* Header minimalista de cada item */
.item-header {
  background: #F9FAFB;
  border-bottom: 1px solid #E5E7EB;
  margin: -1rem -1rem 1rem;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-number {
  background: #7C3AED;
  color: white;
  font-weight: 600;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.remove-btn {
  background: transparent;
  border: 1px solid #E5E7EB;
  color: #6B7280;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: #FEE2E2;
  color: #DC2626;
  border-color: #FCA5A5;
}

/* Switch personalizado - Más delgado */
.custom-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
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
  background-color: #D1D5DB;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.custom-switch-slider::before {
  content: "";
  position: absolute;
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.custom-switch input:checked + .custom-switch-slider {
  background-color: #10B981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.custom-switch input:checked + .custom-switch-slider::before {
  transform: translateX(20px);
}

.custom-switch input:focus + .custom-switch-slider {
  outline: 2px solid #10B981;
  outline-offset: 2px;
}
</style>
