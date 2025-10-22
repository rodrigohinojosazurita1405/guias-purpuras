<!-- frontend/src/components/Publish/InformationStep.vue -->
<template>
  <div class="information-step">
    <!-- 
      ==========================================
      PASO 2: INFORMACIÓN DEL ANUNCIO
      ==========================================
      CAMBIOS APLICADOS:
        - "Teléfono/WhatsApp" → "WhatsApp"
        - Pre-llenado con +591
        - Validación específica para WhatsApp boliviano
        - Link automático a WhatsApp (wa.me)
      
      TODO Django:
        - Guardar número con formato internacional (+591XXXXXXXX)
        - Generar link de WhatsApp automáticamente
        - Validar palabras prohibidas en título/descripción
        - Sanitizar HTML para evitar XSS
    -->

    <h2 class="step-title">
      <va-icon name="description" color="purple" size="large" />
      Información del Anuncio
    </h2>

    <p class="step-description">
      Describe tu servicio/producto de forma clara y atractiva
    </p>

    <div class="form-grid">
      <!-- ==========================================
           TÍTULO DEL ANUNCIO
           ========================================== -->
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
          placeholder="Ej: Abogado especializado en derecho civil y familiar"
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

      <!-- ==========================================
           DESCRIPCIÓN
           ========================================== -->
      <div class="form-group full-width">
        <label class="form-label required">
          <va-icon name="notes" size="small" />
          Descripción detallada
        </label>
        <textarea
          v-model="localData.description"
          class="form-textarea"
          :class="{ 'has-error': errors.description }"
          placeholder="Describe tu servicio, experiencia, horarios de atención, zona de cobertura, etc."
          rows="6"
          maxlength="500"
          @input="validateDescription"
          required
        ></textarea>
        <div class="input-footer">
          <span v-if="errors.description" class="error-message">{{ errors.description }}</span>
          <span class="char-count" :class="{ warning: localData.description.length > 450 }">
            {{ localData.description.length }}/500
          </span>
        </div>
      </div>

      <!-- ==========================================
           PRECIO (OPCIONAL)
           ========================================== -->
      <div class="form-group">
        <label class="form-label">
          <va-icon name="payments" size="small" />
          Precio (Opcional)
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
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Deja en blanco si el precio varía o es "A consultar"
        </span>
      </div>

      <!-- ==========================================
           WHATSAPP (CAMBIO: Antes era "Teléfono/WhatsApp")
           ========================================== -->
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
        <span class="form-hint success">
          <va-icon name="check_circle" size="small" />
          Los clientes podrán contactarte directamente por WhatsApp
        </span>
      </div>

      <!-- ==========================================
           EMAIL (OPCIONAL)
           ========================================== -->
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

      <!-- ==========================================
           SITIO WEB / REDES SOCIALES (OPCIONAL)
           ========================================== -->
      <div class="form-group">
        <label class="form-label">
          <va-icon name="link" size="small" />
          Sitio web o redes sociales
        </label>
        <input
          v-model="localData.website"
          type="url"
          class="form-input"
          :class="{ 'has-error': errors.website }"
          placeholder="https://tu-sitio.com o https://facebook.com/tupagina"
          @input="validateWebsite"
        />
        <span v-if="errors.website" class="error-message">{{ errors.website }}</span>
      </div>
    </div>

    <!-- ==========================================
         GUARDADO AUTOMÁTICO (BORRADOR)
         ========================================== -->
    <div v-if="autoSaveStatus" class="auto-save-indicator">
      <va-icon :name="autoSaveIcon" size="small" :color="autoSaveColor" />
      <span>{{ autoSaveStatus }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// ==========================================
// PROPS
// ==========================================
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

// ==========================================
// EMITS
// ==========================================
const emit = defineEmits(['update:modelValue'])

// ==========================================
// STATE LOCAL
// ==========================================
const localData = ref({ ...props.modelValue })
const errors = ref({})
const autoSaveStatus = ref('')
const autoSaveTimer = ref(null)

// Estado específico para WhatsApp (solo los 8 dígitos)
const whatsappNumber = ref('')

// ==========================================
// COMPUTED
// ==========================================
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

// ==========================================
// VALIDACIONES
// ==========================================
const validateTitle = () => {
  errors.value.title = ''
  
  if (!localData.value.title) {
    errors.value.title = 'El título es obligatorio'
    return false
  }
  
  if (localData.value.title.length < 10) {
    errors.value.title = 'El título debe tener al menos 10 caracteres'
    return false
  }
  
  if (localData.value.title.length > 100) {
    errors.value.title = 'El título no puede exceder 100 caracteres'
    return false
  }

  // TODO Django: Validar palabras prohibidas
  
  return true
}

const validateDescription = () => {
  errors.value.description = ''
  
  if (!localData.value.description) {
    errors.value.description = 'La descripción es obligatoria'
    return false
  }
  
  if (localData.value.description.length < 50) {
    errors.value.description = 'La descripción debe tener al menos 50 caracteres'
    return false
  }
  
  if (localData.value.description.length > 500) {
    errors.value.description = 'La descripción no puede exceder 500 caracteres'
    return false
  }
  
  return true
}

// CAMBIO: Validación específica para WhatsApp boliviano
const validateWhatsApp = () => {
  errors.value.whatsapp = ''
  
  if (!whatsappNumber.value) {
    errors.value.whatsapp = 'El WhatsApp es obligatorio'
    return false
  }
  
  // Remover espacios y caracteres no numéricos
  const cleanNumber = whatsappNumber.value.replace(/\D/g, '')
  
  // Validar que tenga exactamente 8 dígitos
  if (cleanNumber.length !== 8) {
    errors.value.whatsapp = 'Debe tener 8 dígitos (Ej: 70123456)'
    return false
  }
  
  // Validar que empiece con 6 o 7 (números de celular en Bolivia)
  if (!cleanNumber.startsWith('6') && !cleanNumber.startsWith('7')) {
    errors.value.whatsapp = 'Número inválido. Debe empezar con 6 o 7'
    return false
  }
  
  // Guardar el número completo con código de país
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
        errors.value.website = 'La URL debe comenzar con http:// o https://'
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
  const descValid = validateDescription()
  const whatsappValid = validateWhatsApp()
  const emailValid = validateEmail()
  const websiteValid = validateWebsite()
  
  return titleValid && descValid && whatsappValid && emailValid && websiteValid
}

// ==========================================
// AUTO-GUARDADO (BORRADOR)
// ==========================================
const saveAsDraft = () => {
  autoSaveStatus.value = 'Guardando borrador...'
  
  // TODO Django: POST /api/listings/draft/
  localStorage.setItem('listing_draft', JSON.stringify(localData.value))
  
  setTimeout(() => {
    autoSaveStatus.value = 'Borrador guardado ✓'
    setTimeout(() => {
      autoSaveStatus.value = ''
    }, 3000)
  }, 500)
}

// ==========================================
// WATCHERS
// ==========================================
watch(localData, (newValue) => {
  emit('update:modelValue', newValue)
  
  clearTimeout(autoSaveTimer.value)
  autoSaveTimer.value = setTimeout(() => {
    if (newValue.title || newValue.description) {
      saveAsDraft()
    }
  }, 2000)
}, { deep: true })

watch(() => props.modelValue, (newValue) => {
  localData.value = { ...newValue }
  // Extraer solo los 8 dígitos si ya hay un número guardado
  if (newValue.whatsapp) {
    whatsappNumber.value = newValue.whatsapp.replace('+591', '').replace(/\D/g, '')
  }
}, { deep: true })

// ==========================================
// EXPOSE
// ==========================================
defineExpose({
  validate
})
</script>

<style scoped>
/* Estilos base (reutilizados del archivo anterior) */
.information-step {
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
  background-color: white;
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
  min-height: 120px;
  line-height: 1.6;
}

/* ==========================================
   CAMPO DE PRECIO
   ========================================== */
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

/* ==========================================
   CAMPO DE WHATSAPP (NUEVO)
   ========================================== */
.whatsapp-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.country-code {
  position: absolute;
  left: 1rem;
  font-weight: 600;
  color: #25D366; /* Color verde de WhatsApp */
  pointer-events: none;
  font-size: 1rem;
}

.whatsapp-input {
  padding-left: 4rem;
}

/* ==========================================
   FOOTER DE INPUT
   ========================================== */
.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

/* ==========================================
   MENSAJES
   ========================================== */
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

.form-hint.success {
  color: #25D366;
  font-style: normal;
  font-weight: 500;
}

/* ==========================================
   INDICADOR DE AUTO-GUARDADO
   ========================================== */
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

/* ==========================================
   RESPONSIVE
   ========================================== */
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

  .input-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .char-count {
    align-self: flex-end;
  }
}
</style>