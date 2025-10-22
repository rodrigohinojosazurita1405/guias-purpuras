<!-- frontend/src/components/Publish/InformationStepProfessional.vue -->
<template>
  <div class="information-step-professional">
    <h2 class="step-title">
      <va-icon name="school" color="purple" size="large" />
      Información Profesional
    </h2>

    <p class="step-description">
      Completa tu perfil profesional para generar más confianza
    </p>

    <!-- SECCIÓN 1: INFORMACIÓN BÁSICA -->
    <div class="section-card">
      <h3 class="section-title">
        <va-icon name="badge" size="small" />
        Información Básica
      </h3>

      <div class="form-grid">
        <div class="form-group full-width">
          <label class="form-label required">
            <va-icon name="title" size="small" />
            Título del anuncio
          </label>
          <input
            v-model="localData.title"
            type="text"
            class="form-input"
            :class="{ 'has-error': errors.title }"
            placeholder="Ej: Dr. Juan Pérez - Especialista en Cardiología"
            maxlength="100"
            @input="validateTitle"
            required
          />
          <div class="input-footer">
            <span v-if="errors.title" class="error-message">{{ errors.title }}</span>
            <span class="char-count" :class="{ warning: localData.title.length > 90 }">
              {{ localData.title.length }}/100
            </span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label required">
            <va-icon name="workspace_premium" size="small" />
            Título Profesional
          </label>
          <input
            v-model="localData.professionalTitle"
            type="text"
            class="form-input"
            :class="{ 'has-error': errors.professionalTitle }"
            placeholder="Ej: Abogado, Médico Cirujano"
            required
          />
          <span v-if="errors.professionalTitle" class="error-message">{{ errors.professionalTitle }}</span>
        </div>

        <div class="form-group">
          <label class="form-label required">
            <va-icon name="work_history" size="small" />
            Años de Experiencia
          </label>
          <select 
            v-model="localData.yearsExperience" 
            class="form-select"
            required
          >
            <option value="">Selecciona...</option>
            <option value="0-2">0-2 años</option>
            <option value="3-5">3-5 años</option>
            <option value="6-10">6-10 años</option>
            <option value="11-15">11-15 años</option>
            <option value="16-20">16-20 años</option>
            <option value="20+">Más de 20 años</option>
          </select>
          <span v-if="errors.yearsExperience" class="error-message">{{ errors.yearsExperience }}</span>
        </div>
      </div>
    </div>

    <!-- SECCIÓN 2: FORMACIÓN ACADÉMICA -->
    <div class="section-card">
      <h3 class="section-title">
        <va-icon name="school" size="small" />
        Formación Académica
      </h3>

      <div class="form-grid">
        <div class="form-group">
          <label class="form-label required">
            <va-icon name="account_balance" size="small" />
            Universidad/Institución
          </label>
          <input
            v-model="localData.university"
            type="text"
            class="form-input"
            placeholder="Ej: Universidad Mayor de San Simón"
            required
          />
          <span v-if="errors.university" class="error-message">{{ errors.university }}</span>
        </div>

        <div class="form-group">
          <label class="form-label required">
            <va-icon name="event" size="small" />
            Año de Graduación
          </label>
          <input
            v-model.number="localData.graduationYear"
            type="number"
            class="form-input"
            :min="1950"
            :max="currentYear"
            placeholder="Ej: 2015"
            required
          />
          <span v-if="errors.graduationYear" class="error-message">{{ errors.graduationYear }}</span>
        </div>

        <div class="form-group full-width">
          <label class="form-label required">
            <va-icon name="military_tech" size="small" />
            Título Obtenido
          </label>
          <input
            v-model="localData.degree"
            type="text"
            class="form-input"
            placeholder="Ej: Licenciatura en Derecho"
            required
          />
          <span v-if="errors.degree" class="error-message">{{ errors.degree }}</span>
        </div>

        <div class="form-group full-width">
          <label class="form-label">
            <va-icon name="verified" size="small" />
            Certificaciones Adicionales (Opcional)
          </label>
          <textarea
            v-model="localData.certifications"
            class="form-textarea"
            rows="3"
            placeholder="Ej: Maestría en Derecho Penal, Diplomado..."
          ></textarea>
        </div>
      </div>
    </div>

    <!-- SECCIÓN 3: ESPECIALIZACIÓN -->
    <div class="section-card">
      <h3 class="section-title">
        <va-icon name="star" size="small" />
        Especialización y Servicios
      </h3>

      <div class="form-grid">
        <div class="form-group full-width">
          <label class="form-label required">
            <va-icon name="label" size="small" />
            Especialidades / Áreas de Práctica
          </label>
          <div class="checkbox-grid">
            <label 
              v-for="specialty in availableSpecialties" 
              :key="specialty"
              class="checkbox-item"
            >
              <input
                type="checkbox"
                :value="specialty"
                v-model="localData.specialties"
              />
              <span>{{ specialty }}</span>
            </label>
          </div>
          <span v-if="errors.specialties" class="error-message">{{ errors.specialties }}</span>
        </div>

        <div class="form-group full-width">
          <label class="form-label required">
            <va-icon name="list_alt" size="small" />
            Servicios que Ofreces
          </label>
          <textarea
            v-model="localData.services"
            class="form-textarea"
            rows="4"
            placeholder="Lista los principales servicios que ofreces"
            maxlength="300"
            required
          ></textarea>
          <span class="char-count">{{ localData.services.length }}/300</span>
        </div>
      </div>
    </div>

    <!-- SECCIÓN 4: EXPERIENCIA -->
    <div class="section-card">
      <h3 class="section-title">
        <va-icon name="emoji_events" size="small" />
        Experiencia y Casos de Éxito
      </h3>

      <div class="form-grid">
        <div class="form-group full-width">
          <label class="form-label">
            <va-icon name="workspace_premium" size="small" />
            Casos de Éxito / Portfolio (Opcional)
          </label>
          <textarea
            v-model="localData.successCases"
            class="form-textarea"
            rows="5"
            placeholder="Describe brevemente casos relevantes o logros destacados"
            maxlength="500"
          ></textarea>
          <span class="char-count">{{ localData.successCases.length }}/500</span>
        </div>
      </div>
    </div>

    <!-- SECCIÓN 5: INFORMACIÓN PRÁCTICA -->
    <div class="section-card">
      <h3 class="section-title">
        <va-icon name="schedule" size="small" />
        Información Práctica
      </h3>

      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">
            <va-icon name="payments" size="small" />
            Precio de Consulta
          </label>
          <div class="price-input-wrapper">
            <span class="currency-prefix">Bs.</span>
            <input
              v-model.number="localData.price"
              type="number"
              class="form-input price-input"
              placeholder="0.00"
              min="0"
              step="0.01"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">
            <va-icon name="access_time" size="small" />
            Horarios de Atención
          </label>
          <input
            v-model="localData.schedule"
            type="text"
            class="form-input"
            placeholder="Ej: Lun-Vie 9:00-18:00"
          />
        </div>

        <div class="form-group full-width">
          <label class="form-label">
            <va-icon name="language" size="small" />
            Idiomas
          </label>
          <div class="checkbox-grid">
            <label 
              v-for="language in availableLanguages" 
              :key="language"
              class="checkbox-item"
            >
              <input
                type="checkbox"
                :value="language"
                v-model="localData.languages"
              />
              <span>{{ language }}</span>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- SECCIÓN 6: CONTACTO -->
    <div class="section-card">
      <h3 class="section-title">
        <va-icon name="contact_phone" size="small" />
        Información de Contacto
      </h3>

      <div class="form-grid">
        <div class="form-group">
          <label class="form-label required">
            <va-icon name="whatsapp" size="small" />
            WhatsApp
          </label>
          <div class="whatsapp-input-wrapper">
            <span class="country-code">+591</span>
            <input
              v-model="whatsappNumber"
              type="tel"
              class="form-input whatsapp-input"
              :class="{ 'has-error': errors.whatsapp }"
              placeholder="70123456"
              maxlength="8"
              @input="validateWhatsApp"
              required
            />
          </div>
          <span v-if="errors.whatsapp" class="error-message">{{ errors.whatsapp }}</span>
        </div>

        <div class="form-group">
          <label class="form-label">
            <va-icon name="email" size="small" />
            Email (Opcional)
          </label>
          <input
            v-model="localData.email"
            type="email"
            class="form-input"
            :class="{ 'has-error': errors.email }"
            placeholder="tu@email.com"
            @input="validateEmail"
          />
          <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label class="form-label">
            <va-icon name="link" size="small" />
            Sitio Web o Redes
          </label>
          <input
            v-model="localData.website"
            type="url"
            class="form-input"
            :class="{ 'has-error': errors.website }"
            placeholder="https://..."
            @input="validateWebsite"
          />
          <span v-if="errors.website" class="error-message">{{ errors.website }}</span>
        </div>
      </div>
    </div>

    <div v-if="autoSaveStatus" class="auto-save-indicator">
      <va-icon :name="autoSaveIcon" size="small" :color="autoSaveColor" />
      <span>{{ autoSaveStatus }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  subcategory: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const localData = ref({ ...props.modelValue })
const errors = ref({})
const autoSaveStatus = ref('')
const autoSaveTimer = ref(null)
const whatsappNumber = ref('')
const currentYear = new Date().getFullYear()

const availableSpecialties = computed(() => {
  const specialtiesBySubcategory = {
    'Abogados': ['Derecho Civil', 'Derecho Penal', 'Derecho Laboral', 'Derecho Familiar', 'Derecho Corporativo'],
    'Doctores': ['Medicina General', 'Pediatría', 'Ginecología', 'Cardiología', 'Traumatología'],
    'Contadores': ['Contabilidad General', 'Auditoría', 'Impuestos', 'Consultoría Financiera'],
    'Arquitectos': ['Diseño Arquitectónico', 'Remodelaciones', 'Diseño de Interiores', 'Construcción'],
    'Ingenieros': ['Civil', 'Sistemas', 'Industrial', 'Eléctrica', 'Mecánica'],
    'Psicólogos': ['Clínica', 'Organizacional', 'Educativa', 'Infantil', 'Pareja y Familia'],
    'Dentistas': ['Odontología General', 'Ortodoncia', 'Implantes', 'Estética Dental'],
    'Veterinarios': ['Pequeños Animales', 'Grandes Animales', 'Exóticos', 'Cirugía']
  }
  return specialtiesBySubcategory[props.subcategory] || ['Especialidad 1', 'Especialidad 2', 'Especialidad 3']
})

const availableLanguages = ['Español', 'Inglés', 'Quechua', 'Aymara', 'Guaraní', 'Portugués']

const autoSaveIcon = computed(() => {
  if (autoSaveStatus.value.includes('Guardado')) return 'check_circle'
  if (autoSaveStatus.value.includes('Guardando')) return 'sync'
  return 'info'
})

const autoSaveColor = computed(() => {
  if (autoSaveStatus.value.includes('Guardado')) return 'success'
  if (autoSaveStatus.value.includes('Guardando')) return 'info'
  return 'warning'
})

const validateTitle = () => {
  errors.value.title = ''
  if (!localData.value.title) {
    errors.value.title = 'El título es obligatorio'
    return false
  }
  if (localData.value.title.length < 10) {
    errors.value.title = 'Mínimo 10 caracteres'
    return false
  }
  return true
}

const validateWhatsApp = () => {
  errors.value.whatsapp = ''
  if (!whatsappNumber.value) {
    errors.value.whatsapp = 'El WhatsApp es obligatorio'
    return false
  }
  const cleanNumber = whatsappNumber.value.replace(/\D/g, '')
  if (cleanNumber.length !== 8) {
    errors.value.whatsapp = 'Debe tener 8 dígitos'
    return false
  }
  if (!cleanNumber.startsWith('6') && !cleanNumber.startsWith('7')) {
    errors.value.whatsapp = 'Número inválido. Debe empezar con 6 o 7'
    return false
  }
  localData.value.whatsapp = `+591${cleanNumber}`
  return true
}

const validateEmail = () => {
  errors.value.email = ''
  if (localData.value.email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(localData.value.email)) {
      errors.value.email = 'Email inválido'
      return false
    }
  }
  return true
}

const validateWebsite = () => {
  errors.value.website = ''
  if (localData.value.website) {
    try {
      new URL(localData.value.website)
      if (!localData.value.website.startsWith('http')) {
        errors.value.website = 'Debe comenzar con http:// o https://'
        return false
      }
    } catch {
      errors.value.website = 'URL inválida'
      return false
    }
  }
  return true
}

const validate = () => {
  const titleValid = validateTitle()
  const whatsappValid = validateWhatsApp()
  const emailValid = validateEmail()
  const websiteValid = validateWebsite()
  
  if (!localData.value.professionalTitle) {
    errors.value.professionalTitle = 'Campo obligatorio'
    return false
  }
  if (!localData.value.yearsExperience) {
    errors.value.yearsExperience = 'Selecciona años de experiencia'
    return false
  }
  if (!localData.value.university) {
    errors.value.university = 'Campo obligatorio'
    return false
  }
  if (!localData.value.degree) {
    errors.value.degree = 'Campo obligatorio'
    return false
  }
  if (!localData.value.specialties || localData.value.specialties.length === 0) {
    errors.value.specialties = 'Selecciona al menos una especialidad'
    return false
  }
  if (!localData.value.services || localData.value.services.length < 20) {
    errors.value.services = 'Describe tus servicios (mínimo 20 caracteres)'
    return false
  }
  
  return titleValid && whatsappValid && emailValid && websiteValid
}

const saveAsDraft = () => {
  autoSaveStatus.value = 'Guardando borrador...'
  localStorage.setItem('professional_draft', JSON.stringify(localData.value))
  setTimeout(() => {
    autoSaveStatus.value = 'Borrador guardado ✓'
    setTimeout(() => {
      autoSaveStatus.value = ''
    }, 3000)
  }, 500)
}

watch(localData, (newValue) => {
  emit('update:modelValue', newValue)
  clearTimeout(autoSaveTimer.value)
  autoSaveTimer.value = setTimeout(() => {
    if (newValue.title) {
      saveAsDraft()
    }
  }, 2000)
}, { deep: true })

watch(() => props.modelValue, (newValue) => {
  localData.value = { ...newValue }
  if (newValue.whatsapp) {
    whatsappNumber.value = newValue.whatsapp.replace('+591', '').replace(/\D/g, '')
  }
}, { deep: true })

defineExpose({
  validate
})
</script>

<style scoped>
.information-step-professional {
  padding: 1rem 0;
}

.step-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 0.5rem;
}

.step-description {
  color: #666;
  font-size: 1rem;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.section-card {
  background: white;
  border: 2px solid #E0E0E0;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple);
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #E0E0E0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  font-size: 0.95rem;
}

.form-label.required::after {
  content: '*';
  color: #E34B4A;
  margin-left: 0.25rem;
}

.form-input,
.form-select,
.form-textarea {
  padding: 0.875rem 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: inherit;
  background-color: white;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

.form-input.has-error,
.form-textarea.has-error {
  border-color: #E34B4A;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
  line-height: 1.6;
}

.form-select {
  cursor: pointer;
}

.price-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.currency-prefix {
  position: absolute;
  left: 1rem;
  font-weight: 600;
  color: var(--color-purple);
  pointer-events: none;
}

.price-input {
  padding-left: 3rem;
}

.whatsapp-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.country-code {
  position: absolute;
  left: 1rem;
  font-weight: 600;
  color: #25D366;
  pointer-events: none;
  font-size: 1rem;
}

.whatsapp-input {
  padding-left: 4rem;
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 0.75rem;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.checkbox-item:hover {
  border-color: var(--color-purple);
  background: rgba(92, 0, 153, 0.05);
}

.checkbox-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.error-message {
  color: #E34B4A;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.char-count {
  font-size: 0.85rem;
  color: #999;
  font-weight: 500;
  text-align: right;
}

.char-count.warning {
  color: #FF9800;
  font-weight: 600;
}

.form-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.85rem;
  font-style: italic;
}

.auto-save-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #E8F5E9;
  border-radius: 8px;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #2E7D32;
  font-weight: 500;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .section-card {
    padding: 1.5rem;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .checkbox-grid {
    grid-template-columns: 1fr;
  }
}
</style>