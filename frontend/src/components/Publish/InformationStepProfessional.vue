<!-- frontend/src/components/Publish/InformationStepProfessional.vue -->
<template>
  <div class="information-step-professional">
    <h2 class="step-title">
      <va-icon name="work" color="purple" size="large" />
      Información Profesional
    </h2>

    <p class="step-description">
      Completa tu perfil profesional para generar confianza
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
          placeholder="Ej: Abogado especializado en derecho civil y familiar"
          maxlength="100"
          required
        />
        <span v-if="errors.title" class="error-message">{{ errors.title }}</span>
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
          placeholder="Ej: Licenciado en Derecho"
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
          v-model="localData.yearsExperience"
          type="number"
          class="form-input"
          placeholder="Ej: 5"
          min="0"
          max="50"
          required
        />
        <span v-if="errors.yearsExperience" class="error-message">{{ errors.yearsExperience }}</span>
      </div>

      <!-- UNIVERSIDAD -->
      <div class="form-group">
        <label class="form-label">
          <va-icon name="school" size="small" />
          Universidad
        </label>
        <input
          v-model="localData.university"
          type="text"
          class="form-input"
          placeholder="Ej: Universidad Mayor de San Simón"
        />
      </div>

      <!-- AÑO DE GRADUACIÓN -->
      <div class="form-group">
        <label class="form-label">
          <va-icon name="event" size="small" />
          Año de graduación
        </label>
        <input
          v-model.number="localData.graduationYear"
          type="number"
          class="form-input"
          placeholder="Ej: 2015"
          :min="1950"
          :max="new Date().getFullYear()"
        />
      </div>

      <!-- SERVICIOS -->
      <div class="form-group full-width">
        <label class="form-label required">
          <va-icon name="description" size="small" />
          Descripción de servicios
        </label>
        <textarea
          v-model="localData.services"
          class="form-textarea"
          placeholder="Describe los servicios que ofreces, tu especialidad, metodología de trabajo..."
          rows="5"
          maxlength="500"
          required
        ></textarea>
        <span v-if="errors.services" class="error-message">{{ errors.services }}</span>
      </div>

      <!-- HORARIO -->
      <div class="form-group">
        <label class="form-label">
          <va-icon name="schedule" size="small" />
          Horario de atención
        </label>
        <input
          v-model="localData.schedule"
          type="text"
          class="form-input"
          placeholder="Ej: Lun-Vie 9:00-18:00"
        />
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
            placeholder="71234567"
            maxlength="8"
            required
          />
        </div>
        <span v-if="errors.whatsapp" class="error-message">{{ errors.whatsapp }}</span>
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
          placeholder="tu@email.com"
        />
      </div>

      <!-- WEBSITE (OPCIONAL) -->
      <div class="form-group full-width">
        <label class="form-label">
          <va-icon name="language" size="small" />
          Sitio web (Opcional)
        </label>
        <input
          v-model="localData.website"
          type="url"
          class="form-input"
          placeholder="https://tusitioweb.com"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

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

  if (!localData.value.services || localData.value.services.length < 50) {
    errors.value.services = 'Describe tus servicios (mínimo 50 caracteres)'
    isValid = false
  }

  if (!localData.value.whatsapp || localData.value.whatsapp.length !== 8) {
    errors.value.whatsapp = 'Ingresa un número de WhatsApp válido (8 dígitos)'
    isValid = false
  }

  return isValid
}

watch(localData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

watch(() => props.modelValue, (newValue) => {
  localData.value = { ...newValue }
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

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

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

.error-message {
  color: #E34B4A;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
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
}
</style>