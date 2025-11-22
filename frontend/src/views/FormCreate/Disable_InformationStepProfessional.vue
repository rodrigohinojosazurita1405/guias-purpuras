<!-- frontend/src/components/Publish/InformationStepProfessional.vue -->
<template>
  <div class="information-step-professional">
    <h2 class="step-title">
      <va-icon name="work" color="purple" size="large" />
      Información Profesional
    </h2>

    <p class="step-description">
      Completa tu perfil profesional para destacar y generar confianza
    </p>

    <div class="form-grid">
      <!-- TÍTULO DEL ANUNCIO -->
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
          placeholder="Ej: Profesional con amplia experiencia en mi área"
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
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Un buen título es claro, específico y atractivo
        </span>
      </div>

      <!-- TÍTULO PROFESIONAL -->
      <div class="form-group">
        <label class="form-label required">
          <va-icon name="badge" size="small" />
          Título Profesional
        </label>
        <input
          v-model="localData.professionalTitle"
          type="text"
          class="form-input"
          :class="{ 'has-error': errors.professionalTitle }"
          placeholder="Ej: Licenciado en..."
          required
        />
        <span v-if="errors.professionalTitle" class="error-message">{{ errors.professionalTitle }}</span>
      </div>

      <!-- AÑOS DE EXPERIENCIA -->
      <div class="form-group">
        <label class="form-label required">
          <va-icon name="trending_up" size="small" />
          Años de experiencia
        </label>
        <input
          v-model.number="localData.yearsExperience"
          type="number"
          class="form-input"
          :class="{ 'has-error': errors.yearsExperience }"
          placeholder="Ej: 5"
          min="0"
          max="50"
          required
        />
        <span v-if="errors.yearsExperience" class="error-message">{{ errors.yearsExperience }}</span>
      </div>

      <!-- ESPECIALIDADES -->
      <div class="form-group full-width">
        <label class="form-label required">
          <va-icon name="category" size="small" />
          Especialidades / Áreas de expertise
        </label>
        <div class="specialties-container">
          <div
            v-for="specialty in availableSpecialties"
            :key="specialty"
            class="specialty-chip"
            :class="{ selected: localData.specialties.includes(specialty) }"
            @click="toggleSpecialty(specialty)"
          >
            <va-icon 
              :name="localData.specialties.includes(specialty) ? 'check_circle' : 'radio_button_unchecked'" 
              size="small" 
            />
            {{ specialty }}
          </div>
        </div>
        <span v-if="errors.specialties" class="error-message">{{ errors.specialties }}</span>
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Selecciona al menos 2 especialidades
        </span>
      </div>

      <!-- DESCRIPCIÓN DE SERVICIOS -->
      <div class="form-group full-width">
        <label class="form-label required">
          <va-icon name="description" size="small" />
          Descripción de servicios
        </label>
        <textarea
          v-model="localData.services"
          class="form-textarea large"
          :class="{ 'has-error': errors.services }"
          placeholder="Describe los servicios que ofreces, tu especialidad, metodología de trabajo, qué te hace diferente de otros profesionales..."
          rows="8"
          maxlength="1000"
          @input="validateServices"
          required
        ></textarea>
        <div class="input-footer">
          <span v-if="errors.services" class="error-message">{{ errors.services }}</span>
          <span class="char-count" :class="{ warning: localData.services.length > 900 }">
            {{ localData.services.length }}/1000
          </span>
        </div>
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Describe qué ofreces, cómo trabajas y que te hace único (mínimo 50 caracteres)
        </span>
      </div>

      <!-- CASOS DE ÉXITO / LOGROS -->
      <div class="form-group full-width">
        <label class="form-label">
          <va-icon name="emoji_events" size="small" />
          Casos de éxito / Logros destacados
        </label>
        <textarea
          v-model="localData.successCases"
          class="form-textarea"
          placeholder="Ej: +200 casos exitosos, Reconocimientos profesionales, 98% de clientes satisfechos..."
          rows="4"
          maxlength="500"
        ></textarea>
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Menciona logros concretos que generen confianza
        </span>
      </div>

      <!-- ¿POR QUÉ ELEGIRME? -->
      <div class="form-group full-width">
        <label class="form-label">
          <va-icon name="thumb_up" size="small" />
          ¿Por qué elegirme?
        </label>
        <textarea
          v-model="localData.whyChooseMe"
          class="form-textarea"
          placeholder="Ej: Atención personalizada 24/7, Primera consulta gratis, Pago flexible, Experiencia comprobada..."
          rows="4"
          maxlength="500"
        ></textarea>
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Tu propuesta de valor única
        </span>
      </div>

      <!-- IDIOMAS -->
      <div class="form-group full-width">
        <label class="form-label">
          <va-icon name="language" size="small" />
          Idiomas que manejo
        </label>
        <div class="languages-container">
          <div
            v-for="language in availableLanguages"
            :key="language"
            class="language-chip"
            :class="{ selected: localData.languages.includes(language) }"
            @click="toggleLanguage(language)"
          >
            <va-icon 
              :name="localData.languages.includes(language) ? 'check_circle' : 'radio_button_unchecked'" 
              size="small" 
            />
            {{ language }}
          </div>
        </div>
      </div>

      <!-- PRECIO/TARIFA -->
      <div class="form-group">
        <label class="form-label">
          <va-icon name="payments" size="small" />
          Tarifa / Precio
        </label>
        <div class="price-options">
          <label class="radio-option">
            <input 
              type="radio" 
              v-model="localData.priceType" 
              value="consultar"
            />
            <span>A consultar</span>
          </label>
          <label class="radio-option">
            <input 
              type="radio" 
              v-model="localData.priceType" 
              value="desde"
            />
            <span>Desde</span>
          </label>
        </div>
        <div v-if="localData.priceType === 'desde'" class="price-input-wrapper">
          <span class="currency-prefix">Bs.</span>
          <input
            v-model.number="localData.price"
            type="number"
            class="form-input price-input"
            placeholder="500"
            min="0"
          />
        </div>
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Opcional - puedes dejarlo como "A consultar"
        </span>
      </div>

      <!-- HORARIO DE ATENCIÓN -->
      <div class="form-group">
        <label class="form-label">
          <va-icon name="schedule" size="small" />
          Horario de atención
        </label>
        <input
          v-model="localData.schedule"
          type="text"
          class="form-input"
          placeholder="Ej: Lun-Vie 9:00-18:00, Sáb 9:00-13:00"
        />
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Indica tu disponibilidad para atender clientes
        </span>
      </div>

      <!-- WHATSAPP -->
      <div class="form-group">
        <label class="form-label required">
          <va-icon name="phone" size="small" />
          WhatsApp
        </label>
        <div class="phone-input-wrapper">
          <span class="phone-prefix">+591</span>
          <input
            v-model="localData.whatsapp"
            type="tel"
            class="form-input phone-input"
            :class="{ 'has-error': errors.whatsapp }"
            placeholder="71234567"
            maxlength="8"
            @input="validateWhatsapp"
            required
          />
        </div>
        <span v-if="errors.whatsapp" class="error-message">{{ errors.whatsapp }}</span>
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Número de WhatsApp donde los clientes pueden contactarte
        </span>
      </div>

      <!-- EMAIL (OPCIONAL) -->
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

      <!-- SITIO WEB (OPCIONAL) -->
      <div class="form-group full-width">
        <label class="form-label">
          <va-icon name="public" size="small" />
          Sitio web (Opcional)
        </label>
        <input
          v-model="localData.website"
          type="url"
          class="form-input"
          :class="{ 'has-error': errors.website }"
          placeholder="https://tusitioweb.com"
          @input="validateWebsite"
        />
        <span v-if="errors.website" class="error-message">{{ errors.website }}</span>
      </div>

      <!-- 🆕 REDES SOCIALES - COMPONENTE REUTILIZABLE -->
      <div class="form-group full-width">
        <SocialMediaFields v-model="localData.socialMedia" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import SocialMediaFields from '@/components/Common/SocialMediaFields.vue'

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

// Especialidades disponibles según subcategoría
const availableSpecialties = ref([
  'Derecho Civil',
  'Derecho Familiar',
  'Derecho Penal',
  'Derecho Laboral',
  'Derecho Comercial',
  'Derecho Tributario',
])

const availableLanguages = ref([
  'Español',
  'Inglés',
  'Quechua',
  'Aymara',
  'Guaraní',
  'Portugués'
])

const localData = ref({
  title: '',
  professionalTitle: '',
  yearsExperience: null,
  specialties: [],
  services: '',
  successCases: '',
  whyChooseMe: '',
  languages: ['Español'],
  priceType: 'consultar',
  price: null,
  schedule: '',
  whatsapp: '',
  email: '',
  website: '',
  socialMedia: {
    facebook: '',
    instagram: '',
    tiktok: '',
    linkedin: '',
    twitter: '',
    youtube: ''
  },
  ...props.modelValue
})

const errors = ref({})

// Toggle specialty
const toggleSpecialty = (specialty) => {
  const index = localData.value.specialties.indexOf(specialty)
  if (index > -1) {
    localData.value.specialties = localData.value.specialties.filter(s => s !== specialty)
  } else {
    localData.value.specialties = [...localData.value.specialties, specialty]
  }
}

// Toggle language
const toggleLanguage = (language) => {
  const index = localData.value.languages.indexOf(language)
  if (index > -1) {
    localData.value.languages = localData.value.languages.filter(l => l !== language)
  } else {
    localData.value.languages = [...localData.value.languages, language]
  }
}

// Validaciones
const validateTitle = () => {
  if (localData.value.title.length < 10) {
    errors.value.title = 'El título debe tener al menos 10 caracteres'
  } else {
    delete errors.value.title
  }
}

const validateServices = () => {
  if (localData.value.services.length < 50) {
    errors.value.services = 'Describe tus servicios con al menos 50 caracteres'
  } else {
    delete errors.value.services
  }
}

const validateWhatsapp = () => {
  const whatsapp = localData.value.whatsapp.replace(/\D/g, '')
  if (whatsapp.length !== 8 || !whatsapp.startsWith('6') && !whatsapp.startsWith('7')) {
    errors.value.whatsapp = 'Ingresa un número válido de 8 dígitos (debe comenzar con 6 o 7)'
  } else {
    delete errors.value.whatsapp
  }
}

const validateEmail = () => {
  if (localData.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(localData.value.email)) {
    errors.value.email = 'Ingresa un email válido'
  } else {
    delete errors.value.email
  }
}

const validateWebsite = () => {
  if (localData.value.website && !localData.value.website.startsWith('http')) {
    errors.value.website = 'La URL debe comenzar con http:// o https://'
  } else {
    delete errors.value.website
  }
}

const validate = () => {
  errors.value = {}
  let isValid = true

  if (!localData.value.title || localData.value.title.length < 10) {
    errors.value.title = 'El título debe tener al menos 10 caracteres'
    isValid = false
  }

  if (!localData.value.professionalTitle) {
    errors.value.professionalTitle = 'El título profesional es obligatorio'
    isValid = false
  }

  if (!localData.value.yearsExperience || localData.value.yearsExperience < 0) {
    errors.value.yearsExperience = 'Ingresa los años de experiencia'
    isValid = false
  }

  if (localData.value.specialties.length < 2) {
    errors.value.specialties = 'Selecciona al menos 2 especialidades'
    isValid = false
  }

  if (!localData.value.services || localData.value.services.length < 50) {
    errors.value.services = 'Describe tus servicios con al menos 50 caracteres'
    isValid = false
  }

  if (!localData.value.whatsapp || localData.value.whatsapp.length !== 8) {
    errors.value.whatsapp = 'Ingresa un número de WhatsApp válido (8 dígitos)'
    isValid = false
  }

  if (localData.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(localData.value.email)) {
    errors.value.email = 'Ingresa un email válido'
    isValid = false
  }

  if (localData.value.website && !localData.value.website.startsWith('http')) {
    errors.value.website = 'La URL debe comenzar con http:// o https://'
    isValid = false
  }

  return isValid
}

watch(localData, (newValue) => {
  // Emitir todos los campos incluyendo socialMedia
  emit('update:modelValue', {
    ...props.modelValue,
    title: newValue.title,
    professionalTitle: newValue.professionalTitle,
    yearsExperience: newValue.yearsExperience,
    specialties: newValue.specialties,
    services: newValue.services,
    successCases: newValue.successCases,
    whyChooseMe: newValue.whyChooseMe,
    languages: newValue.languages,
    priceType: newValue.priceType,
    price: newValue.price,
    schedule: newValue.schedule,
    whatsapp: newValue.whatsapp,
    email: newValue.email,
    website: newValue.website,
    socialMedia: newValue.socialMedia
  })
}, { deep: true })

watch(() => props.modelValue, (newValue) => {
  localData.value = { ...localData.value, ...newValue }
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
.form-textarea {
  padding: 0.875rem 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-input:focus,
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
}

.form-textarea.large {
  min-height: 180px;
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
}

.char-count.warning {
  color: #FF9800;
  font-weight: 600;
}

.form-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #666;
}

/* Especialidades */
.specialties-container,
.languages-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.specialty-chip,
.language-chip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.specialty-chip:hover,
.language-chip:hover {
  border-color: var(--color-purple);
  background: rgba(92, 0, 153, 0.05);
}

.specialty-chip.selected,
.language-chip.selected {
  border-color: var(--color-purple);
  background: var(--color-purple);
  color: white;
}

/* Precio */
.price-options {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 0.75rem;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.radio-option input[type="radio"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.price-input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.currency-prefix {
  padding: 0.875rem 1rem;
  background: #F5F5F5;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  font-weight: 600;
  color: #666;
}

.price-input {
  flex: 1;
}

/* WhatsApp */
.phone-input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.phone-prefix {
  padding: 0.875rem 1rem;
  background: #F5F5F5;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  font-weight: 600;
  color: #666;
}

.phone-input {
  flex: 1;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .step-description {
    font-size: 0.95rem;
  }

  .price-options {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>