<!-- frontend/src/views/JobCreate.vue -->
<!-- FORMULARIO PROFESIONAL PARA PUBLICAR TRABAJOS - VERSIÓN 2.1 CON SEO -->
<template>
  <MainLayout>
    <div class="job-create">
      
      <!-- Header -->
      <div class="create-header">
        <h1 class="header-title">Publica tu Oferta de Trabajo</h1>
        <p class="header-subtitle">
          Encuentra al candidato ideal para tu empresa - Completa el formulario en 8 pasos
        </p>
      </div>

      <!-- Stepper -->
      <div class="stepper-container">
        <div 
          v-for="step in steps" 
          :key="step.number"
          class="step-item"
          :class="{ 
            active: currentStep === step.number,
            completed: currentStep > step.number 
          }"
        >
          <div class="step-circle">
            <va-icon v-if="currentStep > step.number" name="check" size="small" />
            <span v-else>{{ step.number }}</span>
          </div>
          <div class="step-line" v-if="step.number < steps.length"></div>
          <span class="step-label">{{ step.label }}</span>
        </div>
      </div>

      <!-- Auto-save indicator -->
      <transition name="fade">
        <div v-if="autoSaving" class="autosave-indicator">
          <va-icon name="cloud_upload" size="small" />
          Guardando borrador...
        </div>
        <div v-else-if="lastSaved" class="autosave-indicator saved">
          <va-icon name="cloud_done" size="small" />
          Guardado {{ lastSaved }}
        </div>
      </transition>

      <!-- Form Container -->
      <div class="form-container">
        
        <!-- Step 1: Información del Trabajo -->
        <div v-show="currentStep === 1" class="form-step">
          <div class="step-header">
            <va-icon name="work" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Información del Trabajo</h2>
              <p class="step-description">Datos principales del puesto disponible</p>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="title" size="small" />
                Título del Puesto *
              </label>
              <VaInput
                v-model="formData.title"
                placeholder="Ej: Técnico(a) Comercial Agrónomo(a)"
                :error="!!errors.title"
                :error-messages="errors.title"
                counter
                :max-length="100"
              />
              <span class="field-hint">
                💡 Títulos claros reciben 2x más postulaciones
              </span>
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="business" size="small" />
                Nombre de la Empresa *
              </label>
              <VaInput
                v-model="formData.companyName"
                placeholder="Ej: Agropartners S.R.L."
                :error="!!errors.companyName"
                :error-messages="errors.companyName"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="image" size="small" />
                Logo de la Empresa (Opcional)
              </label>
              <VaFileUpload
                v-model="formData.companyLogo"
                type="single"
                file-types="image/*"
                dropzone
              />
              <!-- Preview del logo -->
              <div v-if="companyLogoPreview" class="logo-preview-container">
                <p class="logo-preview-label">Vista previa:</p>
                <img 
                  :src="companyLogoPreview" 
                  alt="Preview logo"
                  class="logo-preview-image"
                />
              </div>
            </div>

            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="description" size="small" />
                Descripción del Trabajo *
              </label>
              <VaTextarea
                v-model="formData.description"
                placeholder="Describe el puesto, responsabilidades, y qué hace especial trabajar en tu empresa..."
                :min-rows="6"
                :max-length="1000"
                counter
                :error="!!errors.description"
                :error-messages="errors.description"
              />
              <span class="field-hint">
                💡 Descripciones detalladas atraen candidatos de mejor calidad
              </span>
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="category" size="small" />
                Categoría/Área *
              </label>
              <VaSelect
                v-model="formData.category"
                :options="categories"
                placeholder="Selecciona una categoría"
                :error="!!errors.category"
                :error-messages="errors.category"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="place" size="small" />
                Ciudad *
              </label>
              <VaSelect
                v-model="formData.city"
                :options="cities"
                placeholder="Selecciona una ciudad"
                :error="!!errors.city"
                :error-messages="errors.city"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="schedule" size="small" />
                Tipo de Contrato *
              </label>
              <VaSelect
                v-model="formData.contractType"
                :options="contractTypes"
                placeholder="Selecciona el tipo"
                :error="!!errors.contractType"
                :error-messages="errors.contractType"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="event" size="small" />
                Fecha de Vencimiento *
              </label>
              <VaDateInput
                v-model="formData.expiryDate"
                placeholder="Selecciona fecha"
                :error="!!errors.expiryDate"
                :error-messages="errors.expiryDate"
              />
              <span class="field-hint">
                Fecha límite para recibir postulaciones
              </span>
            </div>
          </div>
        </div>

        <!-- Step 2: Requisitos y Detalles -->
        <div v-show="currentStep === 2" class="form-step">
          <div class="step-header">
            <va-icon name="checklist" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Requisitos y Detalles</h2>
              <p class="step-description">Especifica qué buscas en el candidato ideal</p>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="assignment" size="small" />
                Requisitos del Puesto *
              </label>
              <VaTextarea
                v-model="formData.requirements"
                placeholder="Ej: - Título universitario en Agronomía&#10;- 2+ años de experiencia en ventas&#10;- Licencia de conducir&#10;- Disponibilidad para viajar"
                :min-rows="6"
                :max-length="1000"
                counter
                :error="!!errors.requirements"
                :error-messages="errors.requirements"
              />
            </div>

            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="work_outline" size="small" />
                Funciones Principales (Opcional)
              </label>
              <VaTextarea
                v-model="formData.responsibilities"
                placeholder="Describe las responsabilidades diarias del puesto..."
                :min-rows="4"
                :max-length="800"
                counter
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="school" size="small" />
                Formación Requerida
              </label>
              <VaInput
                v-model="formData.education"
                placeholder="Ej: Título en Agronomía"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="badge" size="small" />
                Experiencia Necesaria
              </label>
              <VaInput
                v-model="formData.experience"
                placeholder="Ej: 2-3 años en ventas"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="language" size="small" />
                Idiomas Requeridos
              </label>
              <VaInput
                v-model="formData.languages"
                placeholder="Ej: Español (nativo), Inglés (intermedio)"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="build" size="small" />
                Habilidades Técnicas
              </label>
              <VaInput
                v-model="formData.technicalSkills"
                placeholder="Ej: Excel avanzado, CRM"
              />
            </div>
          </div>
        </div>

        <!-- Step 3: Salario y Beneficios -->
        <div v-show="currentStep === 3" class="form-step">
          <div class="step-header">
            <va-icon name="payments" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Salario y Beneficios</h2>
              <p class="step-description">Información sobre compensación</p>
            </div>
          </div>

          <!-- Salary Tip -->
          <div class="salary-tip">
            <va-icon name="lightbulb" color="warning" />
            <div>
              <strong>💡 Tip Pro:</strong> Publicaciones con salario visible reciben 
              <strong>3x más postulaciones</strong> y candidatos de mejor calidad.
            </div>
          </div>

          <div class="form-grid">
            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="attach_money" size="small" />
                Información Salarial *
              </label>
              
              <div class="salary-options">
                <VaRadio
                  v-model="formData.salaryType"
                  option="range"
                  label="Rango salarial específico"
                />
                <div v-if="formData.salaryType === 'range'" class="salary-inputs">
                  <VaInput
                    v-model.number="formData.salaryMin"
                    type="number"
                    placeholder="5000"
                    label="Desde (Bs.)"
                  />
                  <span class="salary-separator">-</span>
                  <VaInput
                    v-model.number="formData.salaryMax"
                    type="number"
                    placeholder="7000"
                    label="Hasta (Bs.)"
                  />
                </div>

                <VaRadio
                  v-model="formData.salaryType"
                  option="fixed"
                  label="Monto fijo"
                />
                <div v-if="formData.salaryType === 'fixed'" class="salary-inputs">
                  <VaInput
                    v-model.number="formData.salaryFixed"
                    type="number"
                    placeholder="6000"
                    label="Salario mensual (Bs.)"
                  />
                </div>

                <VaRadio
                  v-model="formData.salaryType"
                  option="negotiable"
                  label="A convenir"
                />
                <div v-if="formData.salaryType === 'negotiable'" class="salary-note">
                  <va-icon name="info" size="small" />
                  Los candidatos indicarán su pretensión salarial al postular
                </div>

                <VaRadio
                  v-model="formData.salaryType"
                  option="hidden"
                  label="No mostrar información salarial"
                />
              </div>

              <!-- Salary Preview -->
              <div v-if="salaryPreview" class="salary-preview">
                <va-icon name="visibility" size="small" />
                <span>Vista previa: <strong>{{ salaryPreview }}</strong></span>
                <VaChip :color="salaryBadgeColor" size="small">
                  {{ salaryBadgeText }}
                </VaChip>
              </div>
            </div>

            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="star" size="small" />
                Beneficios Adicionales (Opcional)
              </label>
              <VaTextarea
                v-model="formData.benefits"
                placeholder="Ej: Seguro médico, bono de productividad, capacitaciones, horario flexible..."
                :min-rows="4"
                :max-length="500"
                counter
              />
            </div>
          </div>
        </div>

        <!-- Step 4: Contacto -->
        <div v-show="currentStep === 4" class="form-step">
          <div class="step-header">
            <va-icon name="contact_mail" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Información de Contacto</h2>
              <p class="step-description">¿Cómo deben postular los candidatos?</p>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-field">
              <label class="field-label">
                <va-icon name="email" size="small" />
                Email de Contacto *
              </label>
              <VaInput
                v-model="formData.email"
                type="email"
                placeholder="rrhh@empresa.com"
                :error="!!errors.email"
                :error-messages="errors.email"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="phone" size="small" />
                WhatsApp *
              </label>
              <VaInput
                v-model="formData.whatsapp"
                placeholder="+591 70123456"
                :error="!!errors.whatsapp"
                :error-messages="errors.whatsapp"
              >
                <template #prepend>
                  <span class="whatsapp-icon">📱</span>
                </template>
              </VaInput>
            </div>

            <div class="form-field">
              <label class="field-label">
                <va-icon name="public" size="small" />
                Sitio Web (Opcional)
              </label>
              <VaInput
                v-model="formData.website"
                placeholder="https://www.empresa.com"
              />
            </div>

            <div class="form-field full-width">
              <label class="field-label">
                <va-icon name="info" size="small" />
                Instrucciones de Postulación (Opcional)
              </label>
              <VaTextarea
                v-model="formData.applicationInstructions"
                placeholder="Ej: Enviar CV actualizado con asunto 'Postulación - Técnico Comercial'"
                :min-rows="3"
                :max-length="300"
                counter
              />
            </div>
          </div>
        </div>

        <!-- Step 5: Preguntas de Screening (NUEVO - V2.0) -->
        <div v-show="currentStep === 5" class="form-step">
          <div class="step-header">
            <va-icon name="quiz" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Preguntas de Screening</h2>
              <p class="step-description">Filtra candidatos automáticamente (máximo 5 preguntas)</p>
            </div>
          </div>

          <div class="screening-info">
            <va-icon name="info" color="info" />
            <p>
              Las preguntas de screening te ayudan a filtrar candidatos antes de revisar sus CVs.
              Los candidatos responderán estas preguntas al postular.
            </p>
          </div>

          <!-- Screening Questions List -->
          <div class="screening-questions">
            <div 
              v-for="(question, index) in formData.screeningQuestions" 
              :key="index"
              class="screening-question-item"
            >
              <div class="question-header">
                <span class="question-number">Pregunta {{ index + 1 }}</span>
                <VaButton
                  preset="plain"
                  icon="delete"
                  color="danger"
                  size="small"
                  @click="removeScreeningQuestion(index)"
                />
              </div>

              <div class="question-fields">
                <VaInput
                  v-model="question.text"
                  label="Texto de la pregunta *"
                  placeholder="Ej: ¿Tienes licencia de conducir?"
                  class="question-input"
                />

                <VaSelect
                  v-model="question.type"
                  label="Tipo de respuesta"
                  :options="questionTypes"
                  class="question-type"
                />

                <div v-if="question.type === 'multiple'" class="multiple-options">
                  <label>Opciones (una por línea):</label>
                  <VaTextarea
                    v-model="question.options"
                    placeholder="Opción 1&#10;Opción 2&#10;Opción 3"
                    :min-rows="3"
                  />
                </div>

                <VaCheckbox
                  v-model="question.required"
                  label="Pregunta obligatoria"
                />
              </div>
            </div>

            <!-- Add Question Button -->
            <VaButton
              v-if="formData.screeningQuestions.length < 5"
              preset="secondary"
              icon="add"
              @click="addScreeningQuestion"
              class="add-question-btn"
            >
              Agregar Pregunta ({{ formData.screeningQuestions.length }}/5)
            </VaButton>

            <div v-else class="max-questions-message">
              <va-icon name="info" size="small" />
              Has alcanzado el máximo de 5 preguntas
            </div>
          </div>

          <!-- Preview -->
          <div v-if="formData.screeningQuestions.length > 0" class="screening-preview">
            <h3>
              <va-icon name="visibility" size="small" />
              Vista previa para candidatos
            </h3>
            <div class="preview-questions">
              <div 
                v-for="(q, i) in formData.screeningQuestions" 
                :key="i"
                class="preview-question"
              >
                <label>
                  {{ i + 1 }}. {{ q.text }}
                  <span v-if="q.required" class="required-mark">*</span>
                </label>
                <div v-if="q.type === 'text'" class="preview-input">
                  <input type="text" placeholder="Respuesta del candidato..." disabled />
                </div>
                <div v-else-if="q.type === 'yesno'" class="preview-radio">
                  <label><input type="radio" disabled /> Sí</label>
                  <label><input type="radio" disabled /> No</label>
                </div>
                <div v-else-if="q.type === 'multiple'" class="preview-select">
                  <select disabled>
                    <option>Seleccionar...</option>
                    <option v-for="(opt, j) in q.options.split('\n')" :key="j">
                      {{ opt }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 6: SEO -->
        <div v-show="currentStep === 6" class="form-step">
          <SEOStep
            v-model="formData.seoData"
            entity-type="trabajo"
            base-url="guiaspurpuras.com/trabajos"
          />
        </div>


        <!-- Step 7: Plan -->
        <div v-show="currentStep === 7" class="form-step">
          <div class="step-header">
            <va-icon name="verified" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Selecciona tu Plan</h2>
              <p class="step-description">Elige el plan que mejor se adapte a tus necesidades</p>
            </div>
          </div>

          <div class="plans-grid">
            <div 
              v-for="plan in plans" 
              :key="plan.id"
              class="plan-card"
              :class="{ selected: formData.plan === plan.id }"
              @click="formData.plan = plan.id"
            >
              <div class="plan-badge" :class="`badge-${plan.id}`">
                {{ plan.badge }}
              </div>
              <h3 class="plan-name">{{ plan.name }}</h3>
              <div class="plan-price">{{ plan.price }}</div>
              <ul class="plan-features">
                <li v-for="(feature, index) in plan.features" :key="index">
                  <va-icon name="check_circle" size="small" />
                  {{ feature }}
                </li>
              </ul>
              <VaButton
                :color="formData.plan === plan.id ? 'success' : 'primary'"
                :preset="formData.plan === plan.id ? undefined : 'secondary'"
                block
              >
                {{ formData.plan === plan.id ? 'Seleccionado' : 'Seleccionar' }}
              </VaButton>
            </div>
          </div>
        </div>

        <!-- Step 8: Vista Previa y Confirmar (NUEVO - V2.0) -->
        <div v-show="currentStep === 8" class="form-step">
          <div class="step-header">
            <va-icon name="visibility" size="large" color="#5C0099" />
            <div>
              <h2 class="step-title">Vista Previa y Confirmar</h2>
              <p class="step-description">Revisa cómo se verá tu publicación</p>
            </div>
          </div>

          <!-- Preview Toggle -->
          <div class="preview-toggle">
            <VaButton
              :color="showPreview ? 'primary' : 'secondary'"
              @click="showPreview = !showPreview"
              icon="visibility"
            >
              {{ showPreview ? 'Ocultar' : 'Ver' }} Vista Previa
            </VaButton>
          </div>

          <!-- Live Preview -->
          <transition name="slide">
            <div v-if="showPreview" class="job-preview">
              <div class="preview-header">
                <va-icon name="preview" />
                <span>Así verán los candidatos tu oferta:</span>
              </div>

              <div class="preview-content">
                <!-- Badges -->
                <div class="preview-badges">
                  <VaChip 
                    v-if="formData.plan === 'destacado'" 
                    color="warning"
                    icon="star"
                  >
                    Oferta Destacada
                  </VaChip>
                  <VaChip 
                    v-if="formData.plan === 'urgente'" 
                    color="danger"
                    icon="priority_high"
                  >
                    Urgente
                  </VaChip>
                  <VaChip 
                    v-if="formData.salaryType !== 'hidden'" 
                    color="success"
                  >
                    {{ salaryBadgeText }}
                  </VaChip>
                </div>

                <!-- Title -->
                <h1 class="preview-title">{{ formData.title || 'Título del puesto' }}</h1>
                <div class="preview-company">
                  <img 
                    v-if="companyLogoPreview" 
                    :src="companyLogoPreview" 
                    alt="Logo empresa"
                    class="company-logo-preview"
                  />
                  <va-icon v-else name="business" size="small" />
                  <span>{{ formData.companyName || 'Nombre de la empresa' }}</span>
                </div>

                <!-- Info Grid -->
                <div class="preview-info-grid">
                  <div class="info-item">
                    <va-icon name="place" />
                    <span>{{ formData.city || 'Ciudad' }}</span>
                  </div>
                  <div class="info-item">
                    <va-icon name="schedule" />
                    <span>{{ formData.contractType || 'Tipo de contrato' }}</span>
                  </div>
                  <div class="info-item">
                    <va-icon name="event" />
                    <span>Vence: {{ formData.expiryDate || 'Fecha' }}</span>
                  </div>
                  <div class="info-item">
                    <va-icon name="category" />
                    <span>{{ formData.category || 'Categoría' }}</span>
                  </div>
                </div>

                <!-- Salary -->
                <div v-if="salaryPreview" class="preview-salary">
                  <va-icon name="payments" />
                  <strong>{{ salaryPreview }}</strong>
                </div>

                <!-- Description -->
                <div class="preview-section">
                  <h3>Descripción del Puesto</h3>
                  <p>{{ formData.description || 'Descripción...' }}</p>
                </div>

                <!-- Requirements -->
                <div class="preview-section">
                  <h3>Requisitos</h3>
                  <p class="preserve-breaks">{{ formData.requirements || 'Requisitos...' }}</p>
                </div>
              </div>
            </div>
          </transition>

          <!-- Summary (Editable) -->
          <div class="summary-card">
            <h3>Resumen de tu Publicación</h3>
            
            <div class="summary-item">
              <span class="summary-label">Título:</span>
              <span class="summary-value">{{ formData.title }}</span>
              <VaButton preset="plain" size="small" @click="goToStep(1)">
                Editar
              </VaButton>
            </div>

            <div class="summary-item">
              <span class="summary-label">Empresa:</span>
              <span class="summary-value">{{ formData.companyName }}</span>
              <VaButton preset="plain" size="small" @click="goToStep(1)">
                Editar
              </VaButton>
            </div>

            <div class="summary-item">
              <span class="summary-label">Ciudad:</span>
              <span class="summary-value">{{ formData.city }}</span>
              <VaButton preset="plain" size="small" @click="goToStep(1)">
                Editar
              </VaButton>
            </div>

            <div class="summary-item">
              <span class="summary-label">Salario:</span>
              <span class="summary-value">{{ salaryPreview || 'No especificado' }}</span>
              <VaButton preset="plain" size="small" @click="goToStep(3)">
                Editar
              </VaButton>
            </div>

            <div class="summary-item">
              <span class="summary-label">Contacto:</span>
              <span class="summary-value">{{ formData.email }}</span>
              <VaButton preset="plain" size="small" @click="goToStep(4)">
                Editar
              </VaButton>
            </div>

            <div class="summary-item">
              <span class="summary-label">Preguntas de screening:</span>
              <span class="summary-value">{{ formData.screeningQuestions.length }} preguntas</span>
              <VaButton preset="plain" size="small" @click="goToStep(5)">
                Editar
              </VaButton>
            </div>

            <div class="summary-item">
              <span class="summary-label">Plan:</span>
              <span class="summary-value">{{ getPlanName(formData.plan) }}</span>
              <VaButton preset="plain" size="small" @click="goToStep(7)">
                Editar
              </VaButton>
            </div>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="form-actions">
          <VaButton
            v-if="currentStep > 1"
            preset="secondary"
            @click="previousStep"
          >
            <va-icon name="arrow_back" />
            Anterior
          </VaButton>
          
          <VaButton
            v-if="currentStep < 8"
            color="purple"
            @click="nextStep"
          >
            Siguiente
            <va-icon name="arrow_forward" />
          </VaButton>

          <!-- Save Draft Button -->
          <VaButton
            v-if="currentStep < 8"
            preset="plain"
            icon="save"
            @click="saveDraft"
            :loading="savingDraft"
          >
            Guardar Borrador
          </VaButton>

          <!-- Publish Button -->
          <VaButton
            v-if="currentStep === 8"
            color="success"
            :loading="submitting"
            @click="submitForm"
            size="large"
          >
            <va-icon name="check_circle" />
            Publicar Oferta de Trabajo
          </VaButton>
        </div>

      </div>

    </div>
  </MainLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import MainLayout from '@/components/Layout/MainLayout.vue'
import SEOStep from '@/components/Publish/SEOStep.vue'

const router = useRouter()
const { init: notify } = useToast()

const currentStep = ref(1)
const submitting = ref(false)
const savingDraft = ref(false)
const autoSaving = ref(false)
const lastSaved = ref('')
const showPreview = ref(false)
const companyLogoPreview = ref(null)

const steps = [
  { number: 1, label: 'Información' },
  { number: 2, label: 'Requisitos' },
  { number: 3, label: 'Salario' },
  { number: 4, label: 'Contacto' },
  { number: 5, label: 'Screening' },
  { number: 6, label: 'SEO' },
  { number: 7, label: 'Plan' },
  { number: 8, label: 'Confirmar' }
]

const categories = [
  'Administración y Finanzas',
  'Agronomía y Veterinaria',
  'Comercial y Ventas',
  'Construcción',
  'Educación',
  'Ingeniería',
  'Legal',
  'Marketing y Publicidad',
  'Salud',
  'Tecnología e Informática',
  'Turismo y Hostelería',
  'Otro'
]

const cities = [
  'La Paz',
  'Santa Cruz',
  'Cochabamba',
  'Oruro',
  'Potosí',
  'Tarija',
  'Sucre',
  'Beni',
  'Pando'
]

const contractTypes = [
  'Tiempo Completo',
  'Medio Tiempo',
  'Por Proyecto',
  'Temporal',
  'Pasantía',
  'Freelance'
]

const questionTypes = [
  { text: 'Texto corto', value: 'text' },
  { text: 'Sí / No', value: 'yesno' },
  { text: 'Opción múltiple', value: 'multiple' }
]

const plans = [
  {
    id: 'basico',
    name: 'Básico',
    badge: 'GRATIS',
    price: 'Bs. 0',
    features: [
      'Publicación básica',
      'Visible 30 días',
      'Información de contacto',
      'Sin badge especial'
    ]
  },
  {
    id: 'destacado',
    name: 'Destacado',
    badge: 'POPULAR',
    price: 'Bs. 100',
    features: [
      'Badge "Oferta Destacada"',
      'Visible 60 días',
      'Aparece en búsquedas destacadas',
      'Prioridad en listados'
    ]
  },
  {
    id: 'urgente',
    name: 'Urgente',
    badge: 'PREMIUM',
    price: 'Bs. 150',
    features: [
      'Badge "Urgente"',
      'Visible 60 días',
      'Posición superior',
      'Máxima visibilidad'
    ]
  }
]

const formData = reactive({
  // Step 1
  title: '',
  companyName: '',
  companyLogo: [],
  description: '',
  category: '',
  city: '',
  contractType: '',
  expiryDate: null,
  
  // Step 2
  requirements: '',
  responsibilities: '',
  education: '',
  experience: '',
  languages: '',
  technicalSkills: '',
  
  // Step 3
  salaryType: 'range', // range, fixed, negotiable, hidden
  salaryMin: null,
  salaryMax: null,
  salaryFixed: null,
  benefits: '',
  
  // Step 4
  email: '',
  whatsapp: '',
  website: '',
  applicationInstructions: '',
  
  // Step 5 - Screening Questions (NEW V2.0)
  screeningQuestions: [],
  
  // Step 6
  plan: 'basico',
  
  // Analytics (prepared for future)
  analytics: {
    views: 0,
    saves: 0,
    applications: 0,
    conversionRate: 0
  }
,
  
  // SEO Fields (Step 6)
  seoData: {
    slug: '',
    mainKeyword: '',
    tags: [],
    metaDescription: '',
    locationKeywords: '',
    categories: []
  }
})

const errors = reactive({})

// Watch para actualizar preview del logo
watch(() => formData.companyLogo, (newValue) => {
  console.log('🔍 Logo changed:', newValue)
  console.log('🔍 Type:', typeof newValue)
  console.log('🔍 Is Array?:', Array.isArray(newValue))
  
  // VaFileUpload con type="single" devuelve el File directamente, NO un array
  if (newValue) {
    const file = Array.isArray(newValue) ? newValue[0] : newValue
    console.log('📁 File object:', file)
    console.log('📁 File type:', typeof file)
    console.log('📁 Is File?:', file instanceof File)
    console.log('📁 Has url?:', file?.url)
    
    // VaFileUpload puede devolver un objeto con diferentes estructuras
    if (file instanceof File) {
      companyLogoPreview.value = URL.createObjectURL(file)
      console.log('✅ Preview URL (File):', companyLogoPreview.value)
    } else if (file?.url) {
      // Vuestic VaFile object
      companyLogoPreview.value = file.url
      console.log('✅ Preview URL (VaFile):', companyLogoPreview.value)
    } else if (typeof file === 'string') {
      companyLogoPreview.value = file
      console.log('✅ Preview URL (String):', companyLogoPreview.value)
    } else {
      console.log('❌ Unknown file structure')
      companyLogoPreview.value = null
    }
  } else {
    companyLogoPreview.value = null
    console.log('❌ No logo')
  }
}, { deep: true })

// Computed Properties
const salaryPreview = computed(() => {
  if (formData.salaryType === 'range' && formData.salaryMin && formData.salaryMax) {
    return `Bs. ${formData.salaryMin.toLocaleString()} - ${formData.salaryMax.toLocaleString()}`
  }
  if (formData.salaryType === 'fixed' && formData.salaryFixed) {
    return `Bs. ${formData.salaryFixed.toLocaleString()}`
  }
  if (formData.salaryType === 'negotiable') {
    return 'A convenir'
  }
  if (formData.salaryType === 'hidden') {
    return null
  }
  return null
})

const salaryBadgeColor = computed(() => {
  if (formData.salaryType === 'range' || formData.salaryType === 'fixed') {
    return 'success'
  }
  if (formData.salaryType === 'negotiable') {
    return 'warning'
  }
  return 'secondary'
})

const salaryBadgeText = computed(() => {
  if (formData.salaryType === 'range' || formData.salaryType === 'fixed') {
    return 'Salario visible'
  }
  if (formData.salaryType === 'negotiable') {
    return 'Negociable'
  }
  return 'Sin información'
})

// Validation
const validateStep = () => {
  Object.keys(errors).forEach(key => delete errors[key])
  
  if (currentStep.value === 1) {
    if (!formData.title) errors.title = 'El título es requerido'
    if (!formData.companyName) errors.companyName = 'El nombre de la empresa es requerido'
    if (!formData.description) errors.description = 'La descripción es requerida'
    if (!formData.category) errors.category = 'La categoría es requerida'
    if (!formData.city) errors.city = 'La ciudad es requerida'
    if (!formData.contractType) errors.contractType = 'El tipo de contrato es requerido'
    if (!formData.expiryDate) errors.expiryDate = 'La fecha de vencimiento es requerida'
  }
  
  if (currentStep.value === 2) {
    if (!formData.requirements) errors.requirements = 'Los requisitos son requeridos'
  }
  
  if (currentStep.value === 3) {
    if (formData.salaryType === 'range') {
      if (!formData.salaryMin) errors.salaryMin = 'El salario mínimo es requerido'
      if (!formData.salaryMax) errors.salaryMax = 'El salario máximo es requerido'
      if (formData.salaryMin && formData.salaryMax && formData.salaryMin >= formData.salaryMax) {
        errors.salaryMax = 'El máximo debe ser mayor al mínimo'
      }
    }
    if (formData.salaryType === 'fixed' && !formData.salaryFixed) {
      errors.salaryFixed = 'El salario es requerido'
    }
  }
  
  if (currentStep.value === 4) {
    if (!formData.email) errors.email = 'El email es requerido'
    if (!formData.whatsapp) errors.whatsapp = 'El WhatsApp es requerido'
  }
  
  // Step 5 (Screening) - Optional, no required validation
  // Step 6 (SEO) - Optional, no required validation
  // Step 7 (Plan) - Always has default
  
  return Object.keys(errors).length === 0
}

// Navigation
const nextStep = () => {
  if (validateStep()) {
    if (currentStep.value < 8) {
      currentStep.value++
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  } else {
    notify({
      message: '⚠️ Por favor completa todos los campos requeridos',
      color: 'warning'
    })
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const goToStep = (step) => {
  currentStep.value = step
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Screening Questions
const addScreeningQuestion = () => {
  if (formData.screeningQuestions.length < 5) {
    formData.screeningQuestions.push({
      text: '',
      type: 'text',
      options: '',
      required: true
    })
  }
}

const removeScreeningQuestion = (index) => {
  formData.screeningQuestions.splice(index, 1)
}

// Draft Management (NEW V2.0)
const DRAFT_KEY = 'job_create_draft'

const saveDraft = async () => {
  savingDraft.value = true
  try {
    localStorage.setItem(DRAFT_KEY, JSON.stringify(formData))
    const now = new Date()
    lastSaved.value = now.toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' })
    
    notify({
      message: '💾 Borrador guardado exitosamente',
      color: 'success'
    })
  } catch (error) {
    notify({
      message: '❌ Error al guardar borrador',
      color: 'danger'
    })
  } finally {
    savingDraft.value = false
  }
}

const loadDraft = () => {
  try {
    const draft = localStorage.getItem(DRAFT_KEY)
    if (draft) {
      const parsed = JSON.parse(draft)
      Object.assign(formData, parsed)
      
      notify({
        message: '📄 Borrador cargado',
        color: 'info',
        duration: 3000
      })
    }
  } catch (error) {
    console.error('Error loading draft:', error)
  }
}

const clearDraft = () => {
  localStorage.removeItem(DRAFT_KEY)
}

// Auto-save every 30 seconds (NEW V2.0)
let autoSaveInterval = null

const startAutoSave = () => {
  autoSaveInterval = setInterval(() => {
    if (Object.keys(formData).some(key => formData[key])) {
      autoSaving.value = true
      setTimeout(() => {
        saveDraft()
        autoSaving.value = false
      }, 500)
    }
  }, 30000) // 30 seconds
}

const stopAutoSave = () => {
  if (autoSaveInterval) {
    clearInterval(autoSaveInterval)
  }
}

// Submit
const getPlanName = (planId) => {
  const plan = plans.find(p => p.id === planId)
  return plan ? plan.name : planId
}

const submitForm = async () => {
  if (!validateStep()) {
    notify({
      message: '⚠️ Por favor revisa todos los campos',
      color: 'warning'
    })
    return
  }

  submitting.value = true

  try {
    // TODO: Implement API call
    console.log('Submitting job:', formData)

    await new Promise(resolve => setTimeout(resolve, 2000))

    notify({
      message: '🎉 ¡Trabajo publicado exitosamente!',
      color: 'success',
      duration: 5000
    })

    // Clear draft after successful submission
    clearDraft()
    stopAutoSave()

    // Redirect to jobs list
    setTimeout(() => {
      router.push('/guias/trabajos')
    }, 1500)

  } catch (error) {
    notify({
      message: '❌ Error al publicar. Intenta nuevamente.',
      color: 'danger'
    })
  } finally {
    submitting.value = false
  }
}

// Lifecycle
onMounted(() => {
  // Check for draft
  const hasDraft = localStorage.getItem(DRAFT_KEY)
  if (hasDraft) {
    // Ask user if they want to load draft
    if (confirm('¿Deseas continuar con tu borrador guardado?')) {
      loadDraft()
    }
  }
  
  // Start auto-save
  startAutoSave()
})

// Cleanup
import { onBeforeUnmount } from 'vue'
onBeforeUnmount(() => {
  stopAutoSave()
})
</script>

<style scoped>
/* ========== Container ========== */
.job-create {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}

/* ========== Header ========== */
.create-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 3px solid var(--color-purple);
}

.header-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0 0 1rem 0;
}

.header-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

/* ========== Stepper ========== */
.stepper-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
  padding: 0 1rem;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  position: relative;
}

.step-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #E0E0E0;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  z-index: 2;
}

.step-item.active .step-circle {
  background: var(--color-purple);
  color: white;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

.step-item.completed .step-circle {
  background: #4CAF50;
  color: white;
}

.step-line {
  position: absolute;
  top: 25px;
  left: 50%;
  width: 100%;
  height: 3px;
  background: #E0E0E0;
  z-index: 1;
}

.step-item.completed .step-line {
  background: #4CAF50;
}

.step-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #999;
  text-align: center;
}

.step-item.active .step-label {
  color: var(--color-purple);
}

.step-item.completed .step-label {
  color: #4CAF50;
}

/* ========== Auto-save Indicator ========== */
.autosave-indicator {
  position: fixed;
  top: 100px;
  right: 20px;
  background: white;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #666;
  z-index: 100;
}

.autosave-indicator.saved {
  color: #4CAF50;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* ========== Form Container ========== */
.form-container {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.form-step {
  min-height: 400px;
}

.step-header {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid rgba(92, 0, 153, 0.1);
}

.step-title {
  margin: 0 0 0.25rem 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #5C0099;
}

.step-description {
  margin: 0;
  color: #666;
  font-size: 1rem;
}

/* ========== Form Grid ========== */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-field.full-width {
  grid-column: 1 / -1;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.field-hint {
  font-size: 0.85rem;
  color: #999;
  font-style: italic;
}

.whatsapp-icon {
  font-size: 1.2rem;
}

/* ========== Salary Section ========== */
.salary-tip {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #FFF3E0;
  border-left: 4px solid #FF9800;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.salary-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: #F8F4FF;
  border-radius: 12px;
}

.salary-inputs {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-left: 2rem;
  margin-top: 0.5rem;
}

.salary-separator {
  font-weight: 700;
  color: #666;
}

.salary-note {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: 2rem;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #666;
}

.salary-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  margin-top: 1rem;
}

/* ========== Screening Questions ========== */
.screening-info {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #E3F2FD;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.screening-questions {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.screening-question-item {
  padding: 1.5rem;
  background: #F8F4FF;
  border-radius: 12px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-number {
  font-weight: 700;
  color: var(--color-purple);
}

.question-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.question-input {
  width: 100%;
}

.question-type {
  width: 100%;
}

.multiple-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.add-question-btn {
  align-self: flex-start;
}

.max-questions-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #FFF3E0;
  border-radius: 8px;
  color: #F57C00;
}

/* ========== Screening Preview ========== */
.screening-preview {
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px solid #E0E0E0;
}

.screening-preview h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 1rem 0;
  color: #666;
  font-size: 0.95rem;
}

.preview-questions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.preview-question {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.preview-question label {
  font-weight: 600;
  color: #333;
}

.required-mark {
  color: #F44336;
}

.preview-input input,
.preview-select select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #DDD;
  border-radius: 4px;
  background: #F5F5F5;
}

.preview-radio {
  display: flex;
  gap: 1rem;
}

.preview-radio label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
}

/* ========== Plans Grid ========== */
.plans-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.plan-card {
  padding: 2rem;
  border: 2px solid #E0E0E0;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.plan-card:hover {
  border-color: var(--color-purple);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.15);
}

.plan-card.selected {
  border-color: var(--color-purple);
  background: #F8F4FF;
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.2);
}

.plan-badge {
  position: absolute;
  top: -12px;
  right: 20px;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
}

.badge-basico {
  background: #607D8B;
}

.badge-destacado {
  background: #FF9800;
}

.badge-urgente {
  background: #F44336;
}

.plan-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 1rem 0 0.5rem 0;
}

.plan-price {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-purple);
  margin-bottom: 1.5rem;
}

.plan-features {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem 0;
}

.plan-features li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  color: #666;
}

/* ========== Preview ========== */
.preview-toggle {
  margin-bottom: 2rem;
}

.job-preview {
  margin-bottom: 2rem;
  border: 2px solid var(--color-purple);
  border-radius: 12px;
  overflow: hidden;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: var(--color-purple);
  color: white;
  font-weight: 600;
}

.preview-content {
  padding: 2rem;
  background: white;
}

.preview-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.preview-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 1rem 0 0.5rem 0;
}

.preview-company {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.company-logo-preview {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
  border: 2px solid #E0E0E0;
}

.logo-preview-container {
  margin-top: 1rem;
  padding: 1rem;
  background: #F8F4FF;
  border-radius: 8px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.logo-preview-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #5C0099;
  margin: 0 0 0.5rem 0;
}

.logo-preview-image {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  object-fit: cover;
  border: 3px solid #5C0099;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.2);
}

.preview-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #F5F5F5;
  border-radius: 8px;
}

.preview-salary {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #E8F5E9;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.preview-salary strong {
  font-size: 1.3rem;
  color: #2E7D32;
}

.preview-section {
  margin-bottom: 2rem;
}

.preview-section h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-purple);
  margin: 0 0 0.75rem 0;
}

.preserve-breaks {
  white-space: pre-wrap;
}

.slide-enter-active, .slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* ========== Summary ========== */
.summary-card {
  background: #F8F4FF;
  padding: 2rem;
  border-radius: 12px;
  margin-top: 2rem;
}

.summary-card h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-purple);
}

.summary-item {
  display: grid;
  grid-template-columns: 150px 1fr auto;
  gap: 1rem;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(92, 0, 153, 0.1);
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-label {
  font-weight: 600;
  color: #666;
}

.summary-value {
  color: #333;
}

/* ========== Actions ========== */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #E0E0E0;
}

/* ========== Responsive ========== */
@media (max-width: 968px) {
  .job-create {
    padding: 1rem;
  }

  .form-container {
    padding: 2rem 1.5rem;
  }

  .stepper-container {
    overflow-x: auto;
    padding-bottom: 1rem;
  }

  .step-label {
    font-size: 0.75rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .plans-grid {
    grid-template-columns: 1fr;
  }

  .preview-info-grid {
    grid-template-columns: 1fr;
  }

  .salary-inputs {
    flex-direction: column;
    align-items: stretch;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .summary-item {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}
</style>