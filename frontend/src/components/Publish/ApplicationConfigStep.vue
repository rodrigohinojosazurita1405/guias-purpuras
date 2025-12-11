<!-- frontend/src/components/Publish/ApplicationConfigStep.vue -->
<!-- PASO 4: CONFIGURACIÓN DE APLICACIÓN (Interna/Externa) -->

<template>
  <div class="application-config-step">
    <!-- MODAL DE ERRORES DE VALIDACIÓN -->
    <va-modal
      v-model="showErrorModal"
      title="Campos Incompletos"
      size="medium"
      hide-default-actions
    >
      <div class="error-modal-content">
        <div class="error-icon">
          <va-icon name="error" size="4rem" color="danger" />
        </div>
        <h3 class="error-title">Por favor completa lo siguiente:</h3>
        <ul class="error-list">
          <li v-for="(error, index) in validationErrors" :key="index" class="error-item">
            <va-icon name="arrow_right" size="small" color="danger" />
            {{ error }}
          </li>
        </ul>
      </div>
      <template #footer>
        <va-button @click="showErrorModal = false" color="primary">
          Entendido
        </va-button>
      </template>
    </va-modal>

    <!-- Header -->
    <div class="step-header">
      <div class="header-content">
        <va-icon name="assignment" size="3rem" color="#7C3AED" />
        <div class="header-text">
          <h2 class="step-title">Configuración de Aplicación Laboral</h2>
          <p class="step-description">
            Elige cómo los candidatos aplicarán a esta oferta
          </p>
        </div>
      </div>
    </div>

    <!-- Form Container -->
    <div class="form-container">
      <!-- Tipo de Aplicación -->
      <div class="form-section">
        <h3 class="section-title">
          <va-icon name="how_to_reg" size="1.25rem" />
          Tipo de Aplicación
        </h3>

        <div class="application-type-options">
          <!-- Opción Interna -->
          <div
            class="option-card"
            :class="{ selected: modelValue.applicationType === 'internal' }"
            @click="updateData('applicationType', 'internal')"
          >
            <div class="option-header">
              <va-radio
                v-model="modelValue.applicationType"
                option="internal"
                label=""
                @update:model-value="updateData('applicationType', 'internal')"
              />
              <h4>Interna</h4>
            </div>
            <p class="option-description">
              Los candidatos aplican directamente en Guías Púrpuras
            </p>
            <div class="option-benefits">
              <div class="benefit">
                <va-icon name="check_circle" size="small" color="success" />
                <span>Gestión centralizada</span>
              </div>
              <div class="benefit">
                <va-icon name="check_circle" size="small" color="success" />
                <span>Filtrado automático</span>
              </div>
              <div class="benefit">
                <va-icon name="check_circle" size="small" color="success" />
                <span>Datos validados</span>
              </div>
            </div>
          </div>

          <!-- Opción Externa -->
          <div
            class="option-card"
            :class="{ selected: modelValue.applicationType === 'external' }"
            @click="updateData('applicationType', 'external')"
          >
            <div class="option-header">
              <va-radio
                v-model="modelValue.applicationType"
                option="external"
                label=""
                @update:model-value="updateData('applicationType', 'external')"
              />
              <h4>Externa</h4>
            </div>
            <p class="option-description">
              Los candidatos aplican en tu sitio o plataforma externa
            </p>
            <div class="option-benefits">
              <div class="benefit">
                <va-icon name="check_circle" size="small" color="success" />
                <span>Tu propio sistema</span>
              </div>
              <div class="benefit">
                <va-icon name="check_circle" size="small" color="success" />
                <span>Máxima flexibilidad</span>
              </div>
              <div class="benefit">
                <va-icon name="check_circle" size="small" color="success" />
                <span>URL personalizada</span>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Instrucciones para el Candidato (si es externa) -->
      <div v-if="modelValue.applicationType === 'external'" class="form-section">
        <h3 class="section-title">
          <va-icon name="description" size="1.25rem" />
          Instrucciones para el Candidato
        </h3>
        <p class="section-description">
          Proporciona instrucciones claras sobre cómo deben aplicar los candidatos
        </p>
<br>
        <!-- Instrucciones de Aplicación -->
        <div class="form-row">
          <label for="application-instructions">Instrucciones de Aplicación (Opcional)</label>
          <textarea
            id="application-instructions"
            :value="modelValue.applicationInstructions || ''"
            placeholder="Ej: Por favor envía tu CV en formato PDF, incluye referencias, carta de presentación..."
            class="form-textarea"
            rows="4"
            maxlength="500"
            @input="updateData('applicationInstructions', $event.target.value)"
          />
          <small class="form-hint">
            Máximo 500 caracteres. Instrucciones especiales que deben conocer los candidatos al aplicar.
          </small>
        </div>
      </div>

      <!-- Preguntas de Filtrado (solo para aplicación interna) -->
      <div v-if="modelValue.applicationType === 'internal'" class="form-section">
        <div class="screening-header">
          <div>
            <h3 class="section-title">
              <va-icon name="quiz" size="1.25rem" />
              Preguntas de Filtrado (Opcional)
            </h3>
            <p class="section-description">
              Agrega preguntas para filtrar candidatos automáticamente
            </p>
          </div>
          <va-badge
            :text="`${modelValue.screeningQuestions?.length || 0}/5`"
            color="primary"
            size="large"
          />
        </div>

        <div class="screening-tip-box">
          <va-icon name="lightbulb" color="#7C3AED" size="1.5rem" />
          <div class="tip-content">
            <strong>Consejo:</strong>
            <p>Las preguntas te ayudan a recibir solo candidatos calificados y ahorran tiempo en selección.</p>
          </div>
        </div>

        <!-- Lista de preguntas -->
        <div v-if="modelValue.screeningQuestions && modelValue.screeningQuestions.length > 0" class="questions-list">
          <div
            v-for="(question, index) in modelValue.screeningQuestions"
            :key="index"
            class="screening-question"
          >
            <div class="question-header">
              <div class="question-number-badge">
                <va-icon name="help_outline" size="small" />
                Pregunta {{ index + 1 }}
              </div>
              <button class="btn-delete" @click="removeQuestion(index)">
                <va-icon name="delete" size="small" />
              </button>
            </div>

            <!-- Campos de edición de pregunta -->
            <div class="question-form">
              <div class="form-row">
                <label>Texto de la pregunta *</label>
                <input
                  :value="question.text"
                  type="text"
                  placeholder="Ej: ¿Cuáles son tus idiomas?"
                  class="form-input"
                  @input="updateQuestion(index, 'text', $event.target.value)"
                />
              </div>

              <div class="form-row">
                <label>Tipo de pregunta *</label>
                <select
                  :value="question.type"
                  class="form-input"
                  @change="updateQuestion(index, 'type', $event.target.value)"
                >
                  <option value="text">Texto corto</option>
                  <option value="yesno">Sí / No</option>
                  <option value="multiple">Opción múltiple</option>
                </select>
              </div>

              <div class="form-row checkbox">
                <label>
                  <input
                    :checked="question.required"
                    type="checkbox"
                    @change="updateQuestion(index, 'required', $event.target.checked)"
                  />
                  <span>Hacer obligatoria</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Botón agregar pregunta -->
        <button
          v-if="!modelValue.screeningQuestions || modelValue.screeningQuestions.length < 5"
          class="btn btn-add-question"
          @click="addQuestion"
        >
          <va-icon name="add_circle" size="small" />
          Agregar Pregunta ({{ modelValue.screeningQuestions?.length || 0 }}/5)
        </button>

        <div v-else class="max-questions-message">
          <va-icon name="info" color="warning" />
          <span>Has alcanzado el máximo de 5 preguntas</span>
        </div>
      </div>

      <!-- INFORMACIÓN DE CONTACTO (si es externa) -->
      <div v-if="modelValue.applicationType === 'external'" class="form-section">
        <h3 class="section-title">
          <va-icon name="phone" size="1.25rem" />
          Información de Contacto
        </h3>
        <p class="section-description">
          Usted puede elegir el medio externo por donde los candidatos podrán postular a su vacante laboral, selecione al menos una opción.
        </p>
<br>
        <!-- URL del Formulario Externo -->
        <div class="form-row">
          <label for="external-url">URL del Formulario Externo (Opcional)</label>
          <input
            id="external-url"
            :value="modelValue.externalApplicationUrl"
            type="url"
            placeholder="https://forms.google.com/... o https://ejemplo.com/aplicar"
            class="form-input"
            @input="updateData('externalApplicationUrl', $event.target.value)"
          />
          <small class="form-hint">
            Enlace a Google Forms, Typeform, LinkedIn, o tu propio formulario
          </small>
        </div>

        <!-- Email de Contacto -->
        <div class="form-row">
          <label for="contact-email">Email de Contacto (Opcional)</label>
          <input
            id="contact-email"
            :value="modelValue.email || ''"
            type="email"
            placeholder="correo@empresa.com"
            class="form-input"
            @input="updateData('email', $event.target.value)"
          />
          <small class="form-hint">Los candidatos podrán enviar su CV a este email</small>
        </div>

        <!-- WhatsApp/Teléfono -->
        <div class="form-row">
          <label for="contact-whatsapp">WhatsApp/Teléfono (Opcional)</label>
          <input
            id="contact-whatsapp"
            :value="modelValue.whatsapp || ''"
            type="text"
            placeholder="Ej: +591 XXXXXXXXX o 6532-4767"
            class="form-input"
            @input="updateData('whatsapp', $event.target.value)"
          />
          <small class="form-hint">Los candidatos podrán contactarte por WhatsApp o llamada</small>
        </div>

        <!-- Sitio Web (Opcional) -->
        <div class="form-row">
          <label for="contact-website">Sitio Web (Opcional)</label>
          <input
            id="contact-website"
            :value="modelValue.website || ''"
            type="url"
            placeholder="https://www.ejemplo.com"
            class="form-input"
            @input="updateData('website', $event.target.value)"
          />
          <small class="form-hint">Enlace a tu sitio web o portafolio</small>
        </div>

        <div class="info-box">
          <va-icon name="info" color="#7C3AED" size="1.5rem" />
          <div class="info-content">
            <p><strong>Proporciona al menos un método de contacto</strong> (URL del formulario externo, Email o WhatsApp) para que los candidatos puedan aplicar exitosamente.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Buttons -->
    <div class="navigation-buttons">
      <button class="btn btn-secondary" @click="$emit('back')">
        <va-icon name="arrow_back" size="small" />
        Atrás
      </button>
      <button class="btn btn-primary" @click="handleNext">
        Siguiente
        <va-icon name="arrow_forward" size="small" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])

// Estados para el modal de validación
const showErrorModal = ref(false)
const validationErrors = ref([])

const updateData = (key, value) => {
  emit('update:modelValue', {
    ...props.modelValue,
    [key]: value
  })
}

const addQuestion = () => {
  const questions = props.modelValue.screeningQuestions || []
  if (questions.length < 5) {
    emit('update:modelValue', {
      ...props.modelValue,
      screeningQuestions: [
        ...questions,
        {
          text: '',
          type: 'text',
          required: true,
          optionsList: []
        }
      ]
    })
  }
}

const removeQuestion = (index) => {
  const questions = [...props.modelValue.screeningQuestions]
  questions.splice(index, 1)
  emit('update:modelValue', {
    ...props.modelValue,
    screeningQuestions: questions
  })
}

const updateQuestion = (index, field, value) => {
  const questions = [...props.modelValue.screeningQuestions]
  questions[index] = {
    ...questions[index],
    [field]: value
  }
  emit('update:modelValue', {
    ...props.modelValue,
    screeningQuestions: questions
  })
}

const getQuestionTypeLabel = (type) => {
  const labels = {
    text: 'Texto corto',
    yesno: 'Sí / No',
    multiple: 'Opción múltiple'
  }
  return labels[type] || type
}

const handleNext = () => {
  if (validate()) {
    emit('next')
  }
}

const validate = () => {
  const errors = []

  // Validar que se haya seleccionado un tipo de aplicación
  if (!props.modelValue.applicationType) {
    errors.push('Debes seleccionar un tipo de aplicación (Interna o Externa)')
  }

  // Validar aplicación externa
  if (props.modelValue.applicationType === 'external') {
    const hasUrl = props.modelValue.externalApplicationUrl && props.modelValue.externalApplicationUrl.trim()
    const hasEmail = props.modelValue.email && props.modelValue.email.trim()
    const hasWhatsapp = props.modelValue.whatsapp && props.modelValue.whatsapp.trim()

    // Debe tener al menos uno de los tres métodos de contacto
    if (!hasUrl && !hasEmail && !hasWhatsapp) {
      errors.push('Debes proporcionar al menos un método de contacto: URL del formulario externo, Email o WhatsApp')
    }

    // Si hay URL, validar que sea válida
    if (hasUrl) {
      try {
        new URL(props.modelValue.externalApplicationUrl)
      } catch {
        errors.push('La URL del formulario externo no es válida. Debe comenzar con http:// o https://')
      }
    }

    // Si hay email, validar formato básico
    if (hasEmail && !props.modelValue.email.includes('@')) {
      errors.push('El email de contacto no es válido')
    }
  }

  // Si hay errores, mostrar modal
  if (errors.length > 0) {
    validationErrors.value = errors
    showErrorModal.value = true
    return false
  }

  return true
}
</script>

<style scoped>
.application-config-step {
  padding: 2rem;
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  min-height: 100vh;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding: 2.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border-top: 3px solid #7C3AED;
}

.header-content {
  display: flex;
  gap: 1.5rem;
}

.header-text {
  flex: 1;
}

.step-title {
  font-size: 2rem;
  font-weight: 800;
  color: #0F172A;
  margin: 0;
}

.step-description {
  font-size: 0.95rem;
  color: #64748B;
  margin: 0.5rem 0 0 0;
}

.form-container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.form-section {
  margin-bottom: 2.5rem;
  padding: 2rem;
  background: linear-gradient(135deg, #F8FAFC 0%, #FFFBFE 100%);
  border-radius: 12px;
  border: 2px solid #E9D5FF;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: #7C3AED;
  margin: 0 0 1rem 0;
}

.section-description {
  font-size: 0.95rem;
  color: #64748B;
  margin: 0;
}

/* Opciones de Aplicación */
.application-type-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  max-width: 900px;
  margin: 0 auto;
}

.option-card {
  padding: 1.75rem;
  background: white;
  border: 2px solid #E2E8F0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-card:hover {
  border-color: #7C3AED;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.1);
  transform: translateY(-2px);
}

.option-card.selected {
  border-color: #7C3AED;
  background: #F9F5FF;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
}

.option-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.option-header h4 {
  margin: 0;
  font-size: 1.1rem;
  color: #1E293B;
}

.option-description {
  font-size: 0.95rem;
  color: #64748B;
  margin: 0 0 1.25rem 0;
  line-height: 1.5;
}

.option-benefits {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.benefit {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  color: #1E293B;
}

/* Formulario */
.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.75rem;
}

.form-row label {
  font-weight: 600;
  color: #1E293B;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
}

.form-input {
  padding: 0.9rem 1.1rem;
  border: 2px solid #E2E8F0;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s;
  line-height: 1.6;
  letter-spacing: 0.2px;
}

.form-input:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.form-hint {
  display: block;
  font-size: 0.85rem;
  color: #64748B;
  margin-top: 0.5rem;
}

/* Textarea */
.form-textarea {
  padding: 0.9rem 1.1rem;
  border: 2px solid #E2E8F0;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s;
  resize: vertical;
  min-height: 100px;
  line-height: 1.6;
  letter-spacing: 0.2px;
}

.form-textarea:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

/* Preguntas de Filtrado */
.screening-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.screening-tip-box {
  display: flex;
  gap: 1.25rem;
  padding: 1.75rem;
  background: linear-gradient(135deg, #F3E8FF 0%, #FAF5FF 100%);
  border-left: 4px solid #7C3AED;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.tip-content {
  flex: 1;
}

.tip-content strong {
  display: block;
  color: #6D28D9;
  margin-bottom: 0.5rem;
}

.tip-content p {
  margin: 0;
  color: #5B21B6;
  font-size: 0.95rem;
  line-height: 1.5;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.screening-question {
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  transition: all 0.3s ease;
}

.question-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid #E2E8F0;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-row label {
  font-weight: 600;
  color: #1E293B;
  font-size: 0.95rem;
}

.form-input {
  padding: 0.9rem 1.1rem;
  border: 2px solid #E2E8F0;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s;
  line-height: 1.6;
  letter-spacing: 0.2px;
}

.form-input:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.form-row.checkbox {
  flex-direction: row;
  gap: 0.75rem;
  align-items: center;
}

.form-row.checkbox label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0;
  cursor: pointer;
  font-weight: 500;
}

.form-row.checkbox input {
  cursor: pointer;
  width: 20px;
  height: 20px;
}

.screening-question:hover {
  border-color: #7C3AED;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}

.question-number-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  white-space: nowrap;
}

.btn-delete {
  background: none;
  border: none;
  color: #EF4444;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-delete:hover {
  background: #FEE2E2;
  border-radius: 6px;
}

.question-text {
  font-weight: 600;
  color: #1E293B;
  margin: 0 0 0.75rem 0;
}

.question-meta {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.meta-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  background: #E0E7FF;
  color: #7C3AED;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
}

.meta-badge.required {
  background: #FEE2E2;
  color: #DC2626;
}

.btn-add-question {
  width: 100%;
  padding: 1rem;
  background: white;
  border: 2px dashed #7C3AED;
  border-radius: 8px;
  color: #7C3AED;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s;
  margin-top: 1rem;
}

.btn-add-question:hover {
  background: #F9F5FF;
  border-color: #6D28D9;
}

.max-questions-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1.25rem;
  background: #FFF3E0;
  border-radius: 12px;
  border: 2px solid #FFB74D;
  color: #F57C00;
  font-weight: 600;
  margin-top: 1rem;
}

/* Info Box */
.info-box {
  display: flex;
  gap: 1.25rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #F3E8FF 0%, #FFFBFE 100%);
  border-left: 4px solid #7C3AED;
  border-radius: 12px;
  margin-top: 1.5rem;
}

.info-content {
  flex: 1;
}

.info-content strong {
  color: #6D28D9;
  font-weight: 600;
}

.info-content p {
  margin: 0;
  color: #6D28D9;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Botones */
.navigation-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  margin-top: 2rem;
  border-top: 2px solid #E2E8F0;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-secondary {
  background: #F3F4F6;
  color: #1F2937;
  border: 2px solid #E5E7EB;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

/* Responsive */
@media (max-width: 768px) {
  .application-config-step {
    padding: 1rem;
  }

  .step-header {
    flex-direction: column;
    gap: 1rem;
  }

  .header-content {
    flex-direction: column;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .form-container {
    padding: 1.5rem;
  }

  .application-type-options {
    grid-template-columns: 1fr;
  }

  .navigation-buttons {
    flex-direction: column;
  }

  .btn {
    justify-content: center;
  }
}

/* Modal de Errores de Validación */
.error-modal-content {
  text-align: center;
  padding: 1.5rem;
}

.error-icon {
  margin-bottom: 1.5rem;
  animation: shake 0.5s ease-in-out;
}

.error-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 1.5rem;
}

.error-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
  max-width: 500px;
  margin: 0 auto;
}

.error-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #FEF2F2 0%, #FFFFFF 100%);
  border-left: 3px solid #EF4444;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #1F2937;
  animation: slideIn 0.3s ease-out forwards;
  opacity: 0;
}

.error-item:nth-child(1) { animation-delay: 0.1s; }
.error-item:nth-child(2) { animation-delay: 0.2s; }
.error-item:nth-child(3) { animation-delay: 0.3s; }
.error-item:nth-child(4) { animation-delay: 0.4s; }
.error-item:nth-child(5) { animation-delay: 0.5s; }

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
