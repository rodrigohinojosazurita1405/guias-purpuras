<!-- frontend/src/views/ApplicationProcess.vue -->
<!-- ACTUALIZADO V2.0 - Compatible con JobCreate V2.0 -->
<template>
  <MainLayout>
    <section class="application-process-section">
      <div class="container">
        
        <!-- Breadcrumb -->
        <nav class="breadcrumb">
          <router-link to="/">Inicio</router-link>
          <span class="separator">/</span>
          <router-link to="/guias/trabajos">Trabajos</router-link>
          <span class="separator">/</span>
          <router-link :to="`/guias/trabajos/${jobId}`">{{ jobTitle }}</router-link>
          <span class="separator">/</span>
          <span class="current">Postulación</span>
        </nav>

        <!-- Header con Info del Trabajo -->
        <div class="job-header">
          <div class="job-logo">
            <img 
              v-if="jobData.companyLogo" 
              :src="jobData.companyLogo" 
              :alt="jobData.companyName"
            />
            <div v-else class="placeholder-logo">
              <va-icon name="business" size="3rem" color="#999" />
            </div>
          </div>
          <div class="job-info">
            <h1 class="job-title">{{ jobTitle }}</h1>
            <p class="company-name">{{ jobData.companyName }}</p>
            <p class="job-location">
              <va-icon name="place" size="small" />
              {{ jobData.city }}
            </p>
            <!-- Salary Info Badge (NUEVO) -->
            <div v-if="showSalaryInfo" class="salary-badge">
              <va-icon name="payments" size="small" />
              <span>{{ salaryDisplayText }}</span>
            </div>
          </div>
        </div>

        <!-- Stepper / Progress Bar - ACTUALIZADO: 4 pasos -->
        <div class="stepper">
          <div 
            v-for="(step, index) in steps" 
            :key="index"
            class="step"
            :class="{
              active: currentStep === index,
              completed: currentStep > index
            }"
          >
            <div class="step-indicator">
              <div class="step-circle">
                <va-icon 
                  v-if="currentStep > index" 
                  name="check" 
                  size="1.25rem" 
                  color="white"
                />
                <span v-else>{{ index + 1 }}</span>
              </div>
              <span class="step-label">{{ step.label }}</span>
            </div>
            <div v-if="index < steps.length - 1" class="step-line"></div>
          </div>
        </div>

        <!-- Contenido de los Pasos -->
        <div class="step-content">
          
          <!-- PASO 1: Pretensión y Carta (ACTUALIZADO - Condicional) -->
          <div v-if="currentStep === 0" class="step-panel">
            <h2 class="panel-title">
              {{ requiresSalaryExpectation ? 'Pretensión Salarial y Carta' : 'Carta de Presentación' }}
            </h2>
            <p class="panel-description">
              {{ requiresSalaryExpectation 
                ? 'Cuéntanos sobre tu pretensión salarial y escribe una carta de presentación para esta posición.'
                : 'Escribe una carta de presentación destacando por qué eres el candidato ideal para esta posición.'
              }}
            </p>

            <div class="form-section">
              
              <!-- Pretensión Salarial (CONDICIONAL - Solo si es "A convenir") -->
              <div v-if="requiresSalaryExpectation" class="salary-section">
                <h3 class="section-subtitle">
                  <va-icon name="payments" color="purple" />
                  Pretensión Salarial *
                </h3>

                <div class="salary-info-notice">
                  <va-icon name="info" size="small" color="#2196F3" />
                  <p>
                    La empresa ha indicado que el salario es <strong>"A convenir"</strong>. 
                    Por favor, indica tu pretensión salarial para esta posición.
                  </p>
                </div>

                <div class="salary-type-selector">
                  <VaRadio
                    v-model="applicationData.salaryType"
                    option="bruto"
                    label="Sueldo Bruto"
                  />
                  <VaRadio
                    v-model="applicationData.salaryType"
                    option="neto"
                    label="Sueldo Neto"
                  />
                </div>

                <div class="salary-input">
                  <VaSelect
                    v-model="applicationData.salaryCurrency"
                    :options="['Bs.', 'USD', '$us']"
                    style="max-width: 120px;"
                  />
                  <VaInput
                    v-model.number="applicationData.salaryAmount"
                    type="number"
                    placeholder="Monto"
                    :min="0"
                    style="flex: 1;"
                    :error="!!errors.salaryAmount"
                    :error-messages="errors.salaryAmount"
                  />
                </div>

                <div class="salary-info-box">
                  <va-icon name="info" size="small" color="#2196F3" />
                  <div>
                    <p><strong>Pretensión salarial mensual {{ applicationData.salaryType }}</strong></p>
                    <p v-if="applicationData.salaryType === 'bruto'" class="salary-note">
                      Recibirás líquido Bs. {{ calculatedNetSalary }} después del aporte obligatorio a la Gestora de Seguridad Social
                    </p>
                    <p class="salary-final">
                      La pretensión salarial que enviarás a la empresa es:
                      <strong>{{ applicationData.salaryCurrency }} {{ applicationData.salaryAmount || 0 }}</strong>
                    </p>
                  </div>
                </div>
              </div>

              <!-- Mensaje si el salario ya está definido (NUEVO) -->
              <div v-else class="salary-defined-message">
                <va-icon name="check_circle" color="success" size="large" />
                <div>
                  <h4>Salario Definido por la Empresa</h4>
                  <p>{{ salaryDisplayText }}</p>
                  <p class="hint">No necesitas indicar tu pretensión salarial.</p>
                </div>
              </div>

              <!-- Carta de Presentación -->
              <div class="cover-letter-section">
                <h3 class="section-subtitle">
                  <va-icon name="edit_note" color="purple" />
                  Carta de Presentación (Recomendado)
                </h3>

               <VaTextarea
                  v-model="applicationData.coverLetter"
                  placeholder="Escribe aquí tu carta de presentación..."
                  :min-rows="8"
                  :max-rows="15"
                  counter
                  :max-length="2000"
                  class="cover-letter-input"
                  style="width: 100% !important;"
                />

                <div class="field-hint">
                  💡 Una buena carta de presentación aumenta tus posibilidades. Menciona por qué te interesa la posición y qué puedes aportar.
                </div>
              </div>
            </div>
          </div>

          <!-- PASO 2: Preguntas de Screening (NUEVO - V2.0) -->
          <div v-if="currentStep === 1" class="step-panel">
            <h2 class="panel-title">Preguntas del Reclutador</h2>
            <p class="panel-description">
              Por favor, responde las siguientes preguntas para completar tu postulación.
            </p>

            <!-- Si no hay preguntas de screening -->
            <div v-if="!hasScreeningQuestions" class="no-screening-message">
              <va-icon name="info" size="large" color="#2196F3" />
              <div>
                <h4>No hay preguntas adicionales</h4>
                <p>El reclutador no ha configurado preguntas de screening para esta posición.</p>
                <p class="hint">Puedes continuar al siguiente paso.</p>
              </div>
            </div>

            <!-- Si hay preguntas de screening -->
            <div v-else class="screening-questions-section">
              <div class="screening-info-box">
                <va-icon name="quiz" color="purple" />
                <div>
                  <p>
                    El reclutador ha preparado <strong>{{ screeningQuestions.length }} pregunta(s)</strong> 
                    para conocerte mejor y filtrar candidatos.
                  </p>
                  <p class="hint">
                    Las preguntas marcadas con <span class="required-mark">*</span> son obligatorias.
                  </p>
                </div>
              </div>

              <!-- Lista de preguntas -->
              <div class="screening-questions-list">
                <div 
                  v-for="(question, index) in screeningQuestions"
                  :key="index"
                  class="screening-question-card"
                >
                  <div class="question-header">
                    <span class="question-number">{{ index + 1 }}</span>
                    <label class="question-text">
                      {{ question.text }}
                      <span v-if="question.required" class="required-mark">*</span>
                    </label>
                  </div>

                  <div class="question-answer">
                    <!-- Tipo: Texto corto -->
                    <VaInput
                      v-if="question.type === 'text'"
                      v-model="applicationData.screeningAnswers[index]"
                      placeholder="Tu respuesta..."
                      :error="!!errors[`screening_${index}`]"
                      :error-messages="errors[`screening_${index}`]"
                    />

                    <!-- Tipo: Sí/No -->
                    <VaRadioGroup
                      v-else-if="question.type === 'yesno'"
                      v-model="applicationData.screeningAnswers[index]"
                      :options="yesNoOptions"
                      :error="!!errors[`screening_${index}`]"
                      :error-messages="errors[`screening_${index}`]"
                      class="yesno-group"
                    />

                    <!-- Tipo: Opción múltiple -->
                    <VaSelect
                      v-else-if="question.type === 'multiple'"
                      v-model="applicationData.screeningAnswers[index]"
                      :options="question.options.split('\n').filter(opt => opt.trim())"
                      placeholder="Selecciona una opción..."
                      :error="!!errors[`screening_${index}`]"
                      :error-messages="errors[`screening_${index}`]"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- PASO 3: Currículum (antes paso 2) -->
          <div v-if="currentStep === 2" class="step-panel">
            <h2 class="panel-title">Currículum</h2>
            <p class="panel-description">
              Revisa que tu currículum esté actualizado y con datos de contacto correctos.
            </p>

            <div class="cv-review">
              <!-- Opción de usar CV guardado -->
              <div v-if="hasSavedCV" class="saved-cv-option">
                <VaCheckbox
                  v-model="applicationData.useSavedCV"
                  @update:model-value="handleCVCheckboxChange"
                >
                  Usar mi currículum guardado
                </VaCheckbox>

                <!-- Lista de CVs guardados (solo si está activado el checkbox) -->
                <transition name="fade">
                  <div v-if="applicationData.useSavedCV" class="saved-cv-list">
                    <CVList
                      v-model="selectedSavedCVId"
                      @create-new="handleCreateNewFromList"
                      @edit="handleEditFromList"
                    />
                  </div>
                </transition>
              </div>

              <!-- Mensaje si no hay CV guardado -->
              <VaAlert
                v-if="!hasSavedCV"
                color="warning"
                border="left"
              >
                <template #icon>
                  <va-icon name="info" />
                </template>
                No tienes un currículum guardado. Por favor, sube uno nuevo o crea tu CV.
              </VaAlert>

              <!-- Sección para subir nuevo CV o crear uno -->
              <transition name="fade">
                <div v-if="!applicationData.useSavedCV || !hasSavedCV" class="cv-sections">
                  
                  <!-- Notice informativo -->
                  <div class="cv-notice">
                    <va-icon name="info" color="#2196F3" />
                    <p>
                      Puedes subir tu CV en formato PDF, DOC o DOCX, o llenar tu información directamente en nuestra plataforma.
                    </p>
                  </div>

                  <!-- Opciones: Subir archivo o llenar formulario -->
                  <div class="cv-options">
                    <VaButton 
                      color="purple"
                      @click="showUploadCVModal = true"
                      size="large"
                      class="cv-option-btn"
                    >
                      <va-icon name="upload_file" size="large" />
                      <div class="btn-content">
                        <span class="btn-title">Subir mi CV</span>
                        <span class="btn-subtitle">PDF, DOC o DOCX</span>
                      </div>
                    </VaButton>

                    <div class="option-divider">
                      <span>o</span>
                    </div>

                    <VaButton 
                      preset="secondary"
                      @click="showCVFormWizard = true"
                      size="large"
                      class="cv-option-btn"
                    >
                      <va-icon name="edit" size="large" />
                      <div class="btn-content">
                        <span class="btn-title">Crear mi CV</span>
                        <span class="btn-subtitle">Llenar formulario</span>
                      </div>
                    </VaButton>
                  </div>

                  <!-- Mostrar CV subido (si existe) -->
                  <transition name="fade">
                    <div v-if="applicationData.uploadedCV" class="uploaded-cv-card">
                      <div class="cv-file-info">
                        <va-icon name="check_circle" color="success" size="2.5rem" />
                        <div class="file-details">
                          <h4>{{ applicationData.uploadedCV.name }}</h4>
                          <p>{{ formatFileSize(applicationData.uploadedCV.size) }} • {{ applicationData.uploadedCV.type }}</p>
                          <p class="upload-date">Subido {{ formatUploadDate(applicationData.uploadedCV.uploadedAt) }}</p>
                        </div>
                      </div>
                      <div class="cv-file-actions">
                        <VaButton
                          preset="plain"
                          icon="visibility"
                          @click="previewCV"
                          title="Ver CV"
                        />
                        <VaButton
                          preset="plain"
                          icon="delete"
                          color="danger"
                          @click="removeUploadedCV"
                          title="Eliminar"
                        />
                      </div>
                    </div>
                  </transition>

                  <!-- Mostrar CV creado con wizard (si existe) -->
                  <transition name="fade">
                    <div v-if="cvCreated" class="cv-created-preview">
                      <div class="cv-created-header">
                        <va-icon name="check_circle" color="success" size="2.5rem" />
                        <div class="cv-created-info">
                          <h4>CV Completo Creado</h4>
                          <p>Tu currículum está listo para ser enviado</p>
                        </div>
                        <div class="cv-created-actions">
                          <VaButton
                            preset="plain"
                            icon="visibility"
                            @click="showCVPreviewModal = true"
                            title="Ver CV completo"
                          >
                            Ver
                          </VaButton>
                          <VaButton
                            preset="plain"
                            icon="edit"
                            @click="showCVFormWizard = true"
                            title="Editar CV"
                          >
                            Editar
                          </VaButton>
                        </div>
                      </div>

                      <!-- Detalles del CV creado -->
                      <div class="cv-created-details">
                        <div class="cv-detail-row">
                          <va-icon name="person" size="small" />
                          <strong>{{ cvFormData.personalInfo.fullName }}</strong>
                        </div>
                        <div class="cv-detail-row">
                          <va-icon name="email" size="small" />
                          {{ cvFormData.personalInfo.email }}
                        </div>
                        <div class="cv-detail-row">
                          <va-icon name="phone" size="small" />
                          {{ cvFormData.personalInfo.phone }}
                        </div>
                        <div class="cv-detail-row">
                          <va-icon name="place" size="small" />
                          {{ cvFormData.personalInfo.city }}
                        </div>
                      </div>

                      <!-- Stats del CV -->
                      <div class="cv-created-stats">
                        <div class="stat-item">
                          <va-icon name="school" size="small" color="purple" />
                          {{ cvFormData.education.length }} Formación(es)
                        </div>
                        <div class="stat-item">
                          <va-icon name="work" size="small" color="purple" />
                          {{ cvFormData.experience.length }} Experiencia(s)
                        </div>
                        <div class="stat-item">
                          <va-icon name="lightbulb" size="small" color="purple" />
                          {{ cvFormData.skills.length }} Habilidad(es)
                        </div>
                        <div class="stat-item">
                          <va-icon name="language" size="small" color="purple" />
                          {{ cvFormData.languages.length }} Idioma(s)
                        </div>
                      </div>
                    </div>
                  </transition>

                </div>
              </transition>

            </div>
          </div>

          <!-- PASO 4: Confirmación (antes paso 3) -->
          <div v-if="currentStep === 3" class="step-panel">
            <h2 class="panel-title">Confirmar y Enviar</h2>
            <p class="panel-description">
              Revisa tu postulación antes de enviarla. Asegúrate de que toda la información sea correcta.
            </p>

            <div class="confirmation-section">
              
              <!-- Resumen del trabajo -->
              <div class="confirmation-card">
                <h3 class="confirmation-subtitle">
                  <va-icon name="work" color="purple" />
                  Postulación para
                </h3>
                <div class="job-summary">
                  <h4>{{ jobTitle }}</h4>
                  <p>{{ jobData.companyName }}</p>
                  <p>
                    <va-icon name="place" size="small" />
                    {{ jobData.city }}
                  </p>
                </div>
              </div>

              <!-- Resumen de pretensión salarial (si aplica) -->
              <div v-if="requiresSalaryExpectation && applicationData.salaryAmount" class="confirmation-card">
                <h3 class="confirmation-subtitle">
                  <va-icon name="payments" color="purple" />
                  Pretensión Salarial
                </h3>
                <div class="salary-summary">
                  <p class="salary-amount">
                    {{ applicationData.salaryCurrency }} {{ applicationData.salaryAmount.toLocaleString() }}
                  </p>
                  <p class="salary-type">{{ applicationData.salaryType === 'bruto' ? 'Bruto' : 'Neto' }}</p>
                </div>
                <VaButton
                  preset="plain"
                  size="small"
                  @click="currentStep = 0"
                >
                  Editar
                </VaButton>
              </div>

              <!-- Resumen de preguntas de screening (si hay) -->
              <div v-if="hasScreeningQuestions && hasAnsweredScreening" class="confirmation-card">
                <h3 class="confirmation-subtitle">
                  <va-icon name="quiz" color="purple" />
                  Respuestas a Preguntas
                </h3>
                <div class="screening-answers-summary">
                  <div 
                    v-for="(question, index) in screeningQuestions"
                    :key="index"
                    class="answer-item"
                  >
                    <p class="answer-question">{{ index + 1 }}. {{ question.text }}</p>
                    <p class="answer-response">
                      <va-icon name="check_circle" size="small" color="success" />
                      {{ applicationData.screeningAnswers[index] || 'Sin respuesta' }}
                    </p>
                  </div>
                </div>
                <VaButton
                  preset="plain"
                  size="small"
                  @click="currentStep = 1"
                >
                  Editar
                </VaButton>
              </div>

              <!-- Resumen de carta de presentación -->
              <div v-if="applicationData.coverLetter" class="confirmation-card">
                <h3 class="confirmation-subtitle">
                  <va-icon name="edit_note" color="purple" />
                  Carta de Presentación
                </h3>
                <div class="cover-letter-summary">
                  <p>{{ applicationData.coverLetter.substring(0, 200) }}{{ applicationData.coverLetter.length > 200 ? '...' : '' }}</p>
                </div>
                <VaButton
                  preset="plain"
                  size="small"
                  @click="currentStep = 0"
                >
                  Editar
                </VaButton>
              </div>

              <!-- Resumen del CV -->
              <div class="confirmation-card">
                <h3 class="confirmation-subtitle">
                  <va-icon name="description" color="purple" />
                  Currículum
                </h3>
                <div class="cv-summary">
                  <div v-if="applicationData.useSavedCV && selectedSavedCVId">
                    <va-icon name="check_circle" color="success" />
                    <p>CV guardado seleccionado</p>
                  </div>
                  <div v-else-if="applicationData.uploadedCV">
                    <va-icon name="check_circle" color="success" />
                    <p>{{ applicationData.uploadedCV.name }}</p>
                  </div>
                  <div v-else-if="cvCreated">
                    <va-icon name="check_circle" color="success" />
                    <p>CV creado - {{ cvFormData.personalInfo.fullName }}</p>
                  </div>
                </div>
                <VaButton
                  preset="plain"
                  size="small"
                  @click="currentStep = 2"
                >
                  Editar
                </VaButton>
              </div>

              <!-- Términos y condiciones -->
               <div class="terms-section">
                <div class="terms-checkbox-wrapper">
                  <VaCheckbox
                    v-model="applicationData.acceptedTerms"
                    :error="!!errors.acceptedTerms"
                    :error-messages="errors.acceptedTerms"
                  />
                  <div class="terms-text">
                    He leído y acepto los 
                    <a href="/terminos" target="_blank">términos y condiciones</a> 
                    y la 
                    <a href="/privacidad" target="_blank">política de privacidad</a>
                  </div>
                </div>
              </div>

              <!-- Botón de envío -->
              <div class="submit-section">
                <VaButton
                  color="success"
                  size="large"
                  :loading="submitting"
                  @click="submitApplication"
                  :disabled="!canSubmit"
                  class="submit-button"
                >
                  <va-icon name="send" />
                  Enviar Postulación
                </VaButton>
                <p class="submit-hint">
                  Al enviar tu postulación, la empresa recibirá tu información y se pondrá en contacto contigo.
                </p>
              </div>

            </div>
          </div>

        </div>

        <!-- Botones de navegación -->
        <div class="navigation-buttons">
          <VaButton
            v-if="currentStep > 0"
            preset="secondary"
            @click="previousStep"
            size="large"
          >
            <va-icon name="arrow_back" />
            Anterior
          </VaButton>
          
          <VaButton
            v-if="currentStep < 3"
            color="purple"
            @click="nextStep"
            size="large"
          >
            Siguiente
            <va-icon name="arrow_forward" />
          </VaButton>
        </div>

      </div>
    </section>

    <!-- Modal para subir CV -->
    <VaModal
      v-model="showUploadCVModal"
      title="Subir tu Currículum"
      size="medium"
      :close-button="true"
      hide-default-actions
    >
      <div class="upload-cv-modal-content">
        <p class="modal-description">
          Sube tu CV en formato PDF, DOC o DOCX. El archivo no debe superar los 5 MB.
        </p>

        <VaFileUpload
          v-model="uploadedFiles"
          type="single"
          file-types=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          dropzone
          @file-added="handleFileAdded"
          @file-removed="handleFileRemoved"
        >
          <template #content>
            <div class="upload-dropzone">
              <va-icon name="cloud_upload" size="4rem" color="#9155FD" />
              <p class="upload-text">Arrastra tu CV aquí o haz click para seleccionar</p>
              <p class="upload-hint">PDF, DOC o DOCX • Máximo 5 MB</p>
            </div>
          </template>
        </VaFileUpload>

        <div class="modal-actions">
          <VaButton
            preset="secondary"
            @click="showUploadCVModal = false"
          >
            Cancelar
          </VaButton>
          <VaButton
            color="purple"
            @click="confirmCVUpload"
            :disabled="uploadedFiles.length === 0"
          >
            Confirmar
          </VaButton>
        </div>
      </div>
    </VaModal>

    <!-- Modal de wizard para crear CV -->
    <VaModal
      v-model="showCVFormWizard"
      title="Crear mi Currículum"
      size="large"
      :close-button="true"
      hide-default-actions
    >
      <CVFormWizard
        v-if="showCVFormWizard"
        v-model="cvFormData"
        @save="handleCVFormSave"
        @cancel="showCVFormWizard = false"
      />
    </VaModal>

    <!-- Modal para vista previa del CV creado -->
    <VaModal
      v-model="showCVPreviewModal"
      title="Vista Previa de tu CV"
      size="large"
      :close-button="true"
      hide-default-actions
    >
      <div class="cv-full-preview">
        <!-- Información Personal -->
        <div class="preview-section">
          <h3 class="preview-section-title">
            <va-icon name="person" />
            Información Personal
          </h3>
          <div class="preview-content">
            <p><strong>Nombre:</strong> {{ cvFormData.personalInfo.fullName }}</p>
            <p><strong>Email:</strong> {{ cvFormData.personalInfo.email }}</p>
            <p><strong>Teléfono:</strong> {{ cvFormData.personalInfo.phone }}</p>
            <p><strong>Ciudad:</strong> {{ cvFormData.personalInfo.city }}</p>
            <p v-if="cvFormData.personalInfo.summary" class="preview-summary">
              {{ cvFormData.personalInfo.summary }}
            </p>
          </div>
        </div>

        <!-- Educación -->
        <div v-if="cvFormData.education.length" class="preview-section">
          <h3 class="preview-section-title">
            <va-icon name="school" />
            Formación Académica
          </h3>
          <div class="preview-content">
            <div 
              v-for="(edu, index) in cvFormData.education" 
              :key="index"
              class="preview-item"
            >
              <h5>{{ edu.degree }}</h5>
              <p>{{ edu.institution }}</p>
              <p>{{ edu.startDate }} - {{ edu.endDate || 'Presente' }}</p>
            </div>
          </div>
        </div>

        <!-- Experiencia -->
        <div v-if="cvFormData.experience.length" class="preview-section">
          <h3 class="preview-section-title">
            <va-icon name="work" />
            Experiencia Laboral
          </h3>
          <div class="preview-content">
            <div 
              v-for="(exp, index) in cvFormData.experience" 
              :key="index"
              class="preview-item"
            >
              <h5>{{ exp.position }}</h5>
              <p>{{ exp.company }}</p>
              <p>{{ exp.startDate }} - {{ exp.endDate || 'Presente' }}</p>
              <p v-if="exp.description">{{ exp.description }}</p>
            </div>
          </div>
        </div>

        <!-- Habilidades -->
        <div v-if="cvFormData.skills.length" class="preview-section">
          <h3 class="preview-section-title">
            <va-icon name="lightbulb" />
            Habilidades
          </h3>
          <div class="preview-content">
            <div class="preview-skills">
              <span 
                v-for="(skill, index) in cvFormData.skills" 
                :key="index"
                class="preview-skill"
              >
                {{ skill }}
              </span>
            </div>
          </div>
        </div>

        <!-- Idiomas -->
        <div v-if="cvFormData.languages.length" class="preview-section">
          <h3 class="preview-section-title">
            <va-icon name="language" />
            Idiomas
          </h3>
          <div class="preview-content">
            <div 
              v-for="(lang, index) in cvFormData.languages" 
              :key="index"
              class="preview-item"
            >
              <p><strong>{{ lang.language }}:</strong> {{ lang.level }}</p>
            </div>
          </div>
        </div>
      </div>
    </VaModal>

  </MainLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import MainLayout from '@/components/Layout/MainLayout.vue'
import CVFormWizard from '@/components/Forms/CVFormWizard.vue'
import CVList from '@/components/Lists/CVList.vue'

const route = useRoute()
const router = useRouter()
const { init: notify } = useToast()

// Props from route
const jobId = ref(route.params.id)

// Job Data (ACTUALIZADO - Necesita salaryType y screeningQuestions)
const jobData = ref({
  companyName: 'Empresa Demo',
  companyLogo: null,
  city: 'Santa Cruz',
  salaryType: 'negotiable', // TODO: Get from API - 'range', 'fixed', 'negotiable', 'hidden'
  salaryMin: null,
  salaryMax: null,
  salaryFixed: null,
  screeningQuestions: [
    // TODO: Get from API
    // Example:
    // {
    //   text: '¿Tienes licencia de conducir?',
    //   type: 'yesno',
    //   options: '',
    //   required: true
    // }
  ]
})

const jobTitle = ref('Técnico Comercial Agrónomo')

// Steps (ACTUALIZADO - 4 pasos)
const steps = ref([
  { label: 'Pretensión y Carta' },
  { label: 'Preguntas' }, // NUEVO
  { label: 'Currículum' },
  { label: 'Confirmar' }
])

const currentStep = ref(0)

// Application Data (ACTUALIZADO)
const applicationData = reactive({
  // Pretensión salarial (condicional)
  salaryType: 'bruto',
  salaryCurrency: 'Bs.',
  salaryAmount: null,
  
  // Carta de presentación
  coverLetter: '',
  
  // Screening answers (NUEVO V2.0)
  screeningAnswers: [],
  
  // CV
  useSavedCV: false,
  uploadedCV: null,
  
  // Terms
  acceptedTerms: false
})

// CV Form Data (para wizard)
const cvFormData = reactive({
  personalInfo: {
    fullName: '',
    email: '',
    phone: '',
    city: '',
    summary: ''
  },
  education: [],
  experience: [],
  skills: [],
  languages: []
})

// States
const submitting = ref(false)
const hasSavedCV = ref(false)
const selectedSavedCVId = ref(null)
const cvCreated = ref(false)
const showUploadCVModal = ref(false)
const showCVFormWizard = ref(false)
const showCVPreviewModal = ref(false)
const uploadedFiles = ref([])

// Errors
const errors = reactive({})

// Options for Yes/No questions
const yesNoOptions = [
  { text: 'Sí', value: 'Sí' },
  { text: 'No', value: 'No' }
]

// Computed Properties (NUEVOS para V2.0)
const requiresSalaryExpectation = computed(() => {
  return jobData.value.salaryType === 'negotiable'
})

const hasScreeningQuestions = computed(() => {
  return jobData.value.screeningQuestions && jobData.value.screeningQuestions.length > 0
})

const screeningQuestions = computed(() => {
  return jobData.value.screeningQuestions || []
})

const hasAnsweredScreening = computed(() => {
  if (!hasScreeningQuestions.value) return false
  return applicationData.screeningAnswers.some(answer => answer && answer.trim())
})

const showSalaryInfo = computed(() => {
  const type = jobData.value.salaryType
  return type && type !== 'hidden'
})

const salaryDisplayText = computed(() => {
  const type = jobData.value.salaryType
  if (type === 'range' && jobData.value.salaryMin && jobData.value.salaryMax) {
    return `Bs. ${jobData.value.salaryMin.toLocaleString()} - ${jobData.value.salaryMax.toLocaleString()}`
  }
  if (type === 'fixed' && jobData.value.salaryFixed) {
    return `Bs. ${jobData.value.salaryFixed.toLocaleString()}`
  }
  if (type === 'negotiable') {
    return 'A convenir'
  }
  return null
})

const calculatedNetSalary = computed(() => {
  if (!applicationData.salaryAmount || applicationData.salaryType !== 'bruto') {
    return 0
  }
  // Cálculo aproximado (12.71% de aporte laboral)
  const netSalary = applicationData.salaryAmount * 0.8729
  return Math.round(netSalary)
})

const canSubmit = computed(() => {
  // Must accept terms
  if (!applicationData.acceptedTerms) return false
  
  // Must have CV (saved, uploaded, or created)
  const hasCV = applicationData.useSavedCV || applicationData.uploadedCV || cvCreated.value
  if (!hasCV) return false
  
  // If salary expectation is required, must have amount
  if (requiresSalaryExpectation.value && !applicationData.salaryAmount) return false
  
  // Must answer required screening questions
  if (hasScreeningQuestions.value) {
    for (let i = 0; i < screeningQuestions.value.length; i++) {
      const question = screeningQuestions.value[i]
      if (question.required) {
        const answer = applicationData.screeningAnswers[i]
        if (!answer || !answer.toString().trim()) {
          return false
        }
      }
    }
  }
  
  return true
})

// Validation
const validateStep = () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  if (currentStep.value === 0) {
    // Validate salary expectation if required
    if (requiresSalaryExpectation.value && !applicationData.salaryAmount) {
      errors.salaryAmount = 'La pretensión salarial es requerida'
      return false
    }
  }
  
  if (currentStep.value === 1) {
    // Validate screening questions
    if (hasScreeningQuestions.value) {
      let hasError = false
      screeningQuestions.value.forEach((question, index) => {
        if (question.required) {
          const answer = applicationData.screeningAnswers[index]
          if (!answer || !answer.toString().trim()) {
            errors[`screening_${index}`] = 'Esta pregunta es obligatoria'
            hasError = true
          }
        }
      })
      if (hasError) return false
    }
  }
  
  if (currentStep.value === 2) {
    // Validate CV
    const hasCV = applicationData.useSavedCV || applicationData.uploadedCV || cvCreated.value
    if (!hasCV) {
      notify({
        message: '⚠️ Debes subir o crear tu currículum',
        color: 'warning'
      })
      return false
    }
  }
  
  if (currentStep.value === 3) {
    // Validate terms
    if (!applicationData.acceptedTerms) {
      errors.acceptedTerms = 'Debes aceptar los términos y condiciones'
      return false
    }
  }
  
  return true
}

// Navigation
const nextStep = () => {
  if (validateStep()) {
    // Skip screening step if no questions
    if (currentStep.value === 0 && !hasScreeningQuestions.value) {
      currentStep.value = 2 // Skip to CV
    } else {
      currentStep.value++
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } else {
    notify({
      message: '⚠️ Por favor completa todos los campos requeridos',
      color: 'warning'
    })
  }
}

const previousStep = () => {
  // Skip screening step if no questions (going back)
  if (currentStep.value === 2 && !hasScreeningQuestions.value) {
    currentStep.value = 0 // Go back to first step
  } else {
    currentStep.value--
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// CV Handlers
const handleCVCheckboxChange = (value) => {
  if (!value) {
    selectedSavedCVId.value = null
  }
}

const handleCreateNewFromList = () => {
  applicationData.useSavedCV = false
  showCVFormWizard.value = true
}

const handleEditFromList = (cvId) => {
  // TODO: Load CV data for editing
  showCVFormWizard.value = true
}

const handleFileAdded = (files) => {
  console.log('Files received:', files)
  
  // Verificar que sea array y tenga archivos
  if (!Array.isArray(files) || files.length === 0) {
    console.error('No files received or invalid format')
    return
  }
  
  const file = files[0] // Tomar el primer archivo
  
  // Validar tipo de archivo
  const validTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ]
  
  if (!validTypes.includes(file.type)) {
    notify({
      message: '⚠️ Solo se permiten archivos PDF, DOC o DOCX',
      color: 'warning'
    })
    return
  }
  
  // Validar tamaño (máximo 10MB)
  const maxSize = 10 * 1024 * 1024 // 10MB
  if (file.size > maxSize) {
    notify({
      message: '⚠️ El archivo es demasiado grande. Máximo 10MB',
      color: 'warning'
    })
    return
  }
  
  // Almacenar en uploadedFiles
  uploadedFiles.value = [file]
  
  // Auto-confirmar upload inmediatamente
  confirmCVUpload()
}

const handleFileRemoved = (file) => {
  console.log('File removed:', file)
}

const confirmCVUpload = () => {
  if (uploadedFiles.value.length > 0) {
    const file = uploadedFiles.value[0]
    applicationData.uploadedCV = {
      name: file.name,
      size: file.size,
      type: file.type,
      uploadedAt: new Date(),
      file: file
    }
    
    // Cerrar modal si estaba abierto
    showUploadCVModal.value = false
    
    // Mostrar confirmación exitosa
    notify({
      message: `✅ CV "${file.name}" subido correctamente`,
      color: 'success',
      duration: 4000
    })
    
    console.log('CV uploaded successfully:', applicationData.uploadedCV)
  } else {
    notify({
      message: '⚠️ No se encontró ningún archivo para subir',
      color: 'warning'
    })
  }
}
const removeUploadedCV = () => {
  applicationData.uploadedCV = null
  notify({
    message: 'CV eliminado',
    color: 'info'
  })
}

const previewCV = () => {
  // TODO: Implement CV preview
  notify({
    message: 'Vista previa del CV',
    color: 'info'
  })
}

const handleCVFormSave = (data) => {
  Object.assign(cvFormData, data)
  cvCreated.value = true
  showCVFormWizard.value = false
  
  notify({
    message: '✅ CV creado exitosamente',
    color: 'success'
  })
}

// Submit
const submitApplication = async () => {
  if (!canSubmit.value) {
    notify({
      message: '⚠️ Por favor completa todos los campos requeridos',
      color: 'warning'
    })
    return
  }

  submitting.value = true

  try {
    // TODO: Implement API call
    const applicationPayload = {
      jobId: jobId.value,
      salaryExpectation: requiresSalaryExpectation.value ? {
        type: applicationData.salaryType,
        currency: applicationData.salaryCurrency,
        amount: applicationData.salaryAmount
      } : null,
      coverLetter: applicationData.coverLetter,
      screeningAnswers: hasScreeningQuestions.value ? applicationData.screeningAnswers : null,
      cv: applicationData.useSavedCV ? { savedCVId: selectedSavedCVId.value } : 
          applicationData.uploadedCV ? { file: applicationData.uploadedCV.file } :
          cvCreated.value ? { formData: cvFormData } : null
    }

    console.log('Submitting application:', applicationPayload)

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))

    notify({
      message: '🎉 ¡Postulación enviada exitosamente!',
      color: 'success',
      duration: 5000
    })

    // Redirect to job detail or success page
    setTimeout(() => {
      router.push(`/guias/trabajos/${jobId.value}`)
    }, 1500)

  } catch (error) {
    notify({
      message: '❌ Error al enviar la postulación. Intenta nuevamente.',
      color: 'danger'
    })
  } finally {
    submitting.value = false
  }
}

// Helpers
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatUploadDate = (date) => {
  const now = new Date()
  const diff = Math.floor((now - date) / 1000 / 60)
  if (diff < 1) return 'Hace unos segundos'
  if (diff < 60) return `Hace ${diff} minuto${diff > 1 ? 's' : ''}`
  const hours = Math.floor(diff / 60)
  if (hours < 24) return `Hace ${hours} hora${hours > 1 ? 's' : ''}`
  return date.toLocaleDateString()
}

// Lifecycle
onMounted(async () => {
  // TODO: Fetch job data from API
  // const job = await fetchJobData(jobId.value)
  // Object.assign(jobData.value, job)
  
  // TODO: Check if user has saved CVs
  // hasSavedCV.value = await checkSavedCVs()
  
  // Initialize screening answers array
  if (hasScreeningQuestions.value) {
    applicationData.screeningAnswers = new Array(screeningQuestions.value.length).fill('')
  }
})
</script>

<style scoped>
/* ========== Container ========== */
.application-process-section {
  padding: 4rem 0;
  min-height: calc(100vh - 80px);
  background: linear-gradient(135deg, #F8F4FF 0%, #FFFFFF 100%);
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* ========== Breadcrumb ========== */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  color: #666;
}

.breadcrumb a {
  color: var(--color-purple);
  text-decoration: none;
  transition: color 0.2s;
}

.breadcrumb a:hover {
  color: var(--color-purple-dark);
}

.breadcrumb .separator {
  color: #999;
}

.breadcrumb .current {
  color: #333;
  font-weight: 600;
}

/* ========== Job Header ========== */
.job-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.job-logo {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.job-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 12px;
}

.placeholder-logo {
  width: 100%;
  height: 100%;
  background: #F5F5F5;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.job-info {
  flex: 1;
}

.job-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.company-name {
  font-size: 1.1rem;
  color: #666;
  margin: 0 0 0.25rem 0;
}

.job-location {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #999;
  font-size: 0.95rem;
  margin: 0;
}

/* Salary Badge (NUEVO) */
.salary-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #E8F5E9;
  color: #2E7D32;
  border-radius: 20px;
  font-size: 0.95rem;
  font-weight: 600;
  margin-top: 0.75rem;
}

/* ========== Stepper ========== */
.stepper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.step {
  display: flex;
  align-items: center;
  flex: 1;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
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
  font-size: 1.25rem;
  transition: all 0.3s ease;
}

.step.active .step-circle {
  background: var(--color-purple);
  color: white;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

.step.completed .step-circle {
  background: #4CAF50;
  color: white;
}

.step-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #999;
  text-align: center;
}

.step.active .step-label {
  color: var(--color-purple);
}

.step.completed .step-label {
  color: #4CAF50;
}

.step-line {
  flex: 1;
  height: 3px;
  background: #E0E0E0;
  margin: 0 1rem;
  position: relative;
  top: -1.5rem;
}

.step.completed .step-line {
  background: #4CAF50;
}

/* ========== Step Content ========== */
.step-content {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  min-height: 400px;
}

.step-panel {
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

.panel-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.panel-description {
  font-size: 1.05rem;
  color: #666;
  margin: 0 0 2rem 0;
}

/* ========== Form Section ========== */
.form-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section-subtitle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1rem 0;
}

/* ========== Salary Section (ACTUALIZADO) ========== */
.salary-section {
  padding: 2rem;
  background: #F8F4FF;
  border-radius: 12px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.salary-info-notice {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #E3F2FD;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.salary-info-notice p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.salary-type-selector {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.salary-input {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.salary-info-box {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
}

.salary-info-box p {
  margin: 0 0 0.5rem 0;
  color: #666;
}

.salary-note {
  font-size: 0.9rem;
  font-style: italic;
}

.salary-final {
  margin-top: 0.5rem;
  font-weight: 600;
  color: #333;
}

/* Salary Defined Message (NUEVO) */
.salary-defined-message {
  display: flex;
  gap: 1.5rem;
  padding: 2rem;
  background: #E8F5E9;
  border-radius: 12px;
  border: 2px solid #4CAF50;
}

.salary-defined-message h4 {
  margin: 0 0 0.5rem 0;
  color: #2E7D32;
  font-size: 1.25rem;
  font-weight: 700;
}

.salary-defined-message p {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 1rem;
}

.salary-defined-message .hint {
  font-size: 0.9rem;
  font-style: italic;
  color: #999;
}

/* ========== Cover Letter Section ========== */
.cover-letter-section {
  padding: 2rem;
  background: #F5F5F5;
  border-radius: 12px;
}

.cover-letter-input {
  margin-bottom: 1rem;
}

.field-hint {
  font-size: 0.9rem;
  color: #999;
  font-style: italic;
}

/* ========== Screening Questions Section (NUEVO V2.0) ========== */
.no-screening-message {
  display: flex;
  gap: 1.5rem;
  padding: 2rem;
  background: #E3F2FD;
  border-radius: 12px;
  text-align: left;
}

.no-screening-message h4 {
  margin: 0 0 0.5rem 0;
  color: #1976D2;
  font-size: 1.25rem;
  font-weight: 700;
}

.no-screening-message p {
  margin: 0 0 0.5rem 0;
  color: #666;
}

.no-screening-message .hint {
  font-size: 0.9rem;
  font-style: italic;
  color: #999;
}

.screening-questions-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.screening-info-box {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: #F8F4FF;
  border-radius: 12px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.screening-info-box p {
  margin: 0 0 0.5rem 0;
  color: #666;
  line-height: 1.6;
}

.screening-info-box .hint {
  font-size: 0.9rem;
  font-style: italic;
  color: #999;
  margin-top: 0.5rem;
}

.required-mark {
  color: #F44336;
  font-weight: 700;
  margin-left: 0.25rem;
}

.screening-questions-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.screening-question-card {
  padding: 1.5rem;
  background: white;
  border: 2px solid #E0E0E0;
  border-radius: 12px;
  transition: border-color 0.3s;
}

.screening-question-card:hover {
  border-color: var(--color-purple);
}

.question-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.question-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--color-purple);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.question-text {
  flex: 1;
  font-size: 1.05rem;
  font-weight: 600;
  color: #333;
  line-height: 1.5;
}

.question-answer {
  padding-left: 3rem;
}

.yesno-group {
  display: flex;
  gap: 2rem;
}

/* ========== CV Review ========== */
.cv-review {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.saved-cv-option {
  padding: 1.5rem;
  background: #F8F4FF;
  border-radius: 12px;
}

.saved-cv-list {
  margin-top: 1rem;
}

.cv-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.cv-notice {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #E3F2FD;
  border-radius: 8px;
}

.cv-notice p {
  margin: 0;
  color: #666;
}

.cv-options {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.cv-option-btn {
  flex: 1;
  max-width: 400px;
  height: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.btn-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.btn-title {
  font-size: 1.1rem;
  font-weight: 700;
}

.btn-subtitle {
  font-size: 0.9rem;
  opacity: 0.8;
}

.option-divider {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #F5F5F5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #999;
  flex-shrink: 0;
}

.uploaded-cv-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  background: #E8F5E9;
  border: 2px solid #4CAF50;
  border-radius: 12px;
}

.cv-file-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.file-details h4 {
  margin: 0 0 0.25rem 0;
  color: #2E7D32;
  font-size: 1.1rem;
  font-weight: 700;
}

.file-details p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.upload-date {
  font-size: 0.85rem !important;
  color: #999 !important;
}

.cv-file-actions {
  display: flex;
  gap: 0.5rem;
}

/* ========== Confirmation Section ========== */
.confirmation-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.confirmation-card {
  padding: 2rem;
  background: #F8F4FF;
  border-radius: 12px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.confirmation-subtitle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-purple);
  margin: 0 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(92, 0, 153, 0.1);
}

.job-summary h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  color: var(--color-purple-darkest);
}

.job-summary p {
  margin: 0 0 0.25rem 0;
  color: #666;
}

.salary-summary {
  display: flex;
  align-items: baseline;
  gap: 1rem;
}

.salary-amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2E7D32;
  margin: 0;
}

.salary-type {
  font-size: 1rem;
  color: #666;
  margin: 0;
}

/* Screening Answers Summary (NUEVO) */
.screening-answers-summary {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.answer-item {
  padding: 1rem;
  background: white;
  border-radius: 8px;
}

.answer-question {
  font-weight: 600;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.answer-response {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  margin: 0;
}

.cover-letter-summary p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.cv-summary {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.cv-summary p {
  margin: 0;
  color: #666;
}

.terms-section {
  padding: 1.5rem;
  background: #FFF3E0;
  border-radius: 12px;
}

.terms-section a {
  color: var(--color-purple);
  text-decoration: none;
  font-weight: 600;
}

.terms-section a:hover {
  text-decoration: underline;
}

.submit-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  background: linear-gradient(135deg, #F0FFF0 0%, #FFFFFF 100%);
  border-radius: 12px;
  border: 2px solid #4CAF50;
}

.submit-button {
  min-width: 300px;
}

.submit-hint {
  margin: 0;
  text-align: center;
  color: #666;
  font-size: 0.9rem;
}

/* ========== Navigation Buttons ========== */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0 2rem;
}

/* ========== Modal Styles ========== */
.upload-cv-modal-content {
  padding: 2rem;
}

.modal-description {
  margin: 0 0 2rem 0;
  color: #666;
  line-height: 1.6;
}

.upload-dropzone {
  padding: 3rem;
  text-align: center;
}

.upload-text {
  margin: 1rem 0 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.upload-hint {
  margin: 0;
  color: #999;
  font-size: 0.9rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

/* ========== Transitions ========== */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* ========== Responsive ========== */
@media (max-width: 968px) {
  .container {
    padding: 0 1rem;
  }

  .job-header {
    flex-direction: column;
    text-align: center;
  }

  .stepper {
    overflow-x: auto;
    padding: 1.5rem;
  }

  .step-circle {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }

  .step-label {
    font-size: 0.8rem;
  }

  .step-line {
    margin: 0 0.5rem;
  }

  .step-content {
    padding: 1.5rem;
  }

  .panel-title {
    font-size: 1.5rem;
  }

  .job-title {
    font-size: 1.25rem;
  }

  .salary-input {
    flex-direction: column;
  }

  .cv-options {
    flex-direction: column;
  }

  .cv-option-btn {
    max-width: 100%;
    width: 100%;
  }

  .option-divider {
    transform: rotate(90deg);
  }

  .uploaded-cv-card {
    flex-direction: column;
    gap: 1rem;
  }

  .cv-file-actions {
    width: 100%;
    justify-content: center;
  }

  .navigation-buttons {
    flex-wrap: wrap;
  }

  .navigation-buttons .va-button {
    flex: 1;
    min-width: 120px;
  }

  .upload-cv-modal-content {
    padding: 1.5rem;
  }

  .modal-actions {
    flex-direction: column-reverse;
  }

  .modal-actions .va-button {
    width: 100%;
  }

  .cv-created-header {
    flex-direction: column;
    text-align: center;
  }

  .cv-created-actions {
    width: 100%;
    justify-content: center;
  }

  .cv-created-stats {
    grid-template-columns: 1fr;
  }
}

/* ========== Z-INDEX FIX ========== */
:deep(.va-modal__container) {
  z-index: 9999 !important;
}

:deep(.va-modal__overlay) {
  z-index: 9998 !important;
}

:deep(.va-modal__dialog) {
  z-index: 10000 !important;
}

/* Asegurar que el contenido del modal sea interactivo */
:deep(.va-modal__inner) {
  position: relative;
  z-index: 10001 !important;
  pointer-events: auto !important;
}

/* ========== CV Created Preview ========== */
.cv-created-preview {
  padding: 2rem;
  background: linear-gradient(135deg, #F0FFF0 0%, #FFFFFF 100%);
  border: 2px solid #4CAF50;
  border-radius: 16px;
  margin-top: 1.5rem;
}

.cv-created-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid rgba(76, 175, 80, 0.2);
}

.cv-created-info {
  flex: 1;
}

.cv-created-info h4 {
  margin: 0 0 0.25rem;
  color: #2E7D32;
  font-size: 1.25rem;
  font-weight: 700;
}

.cv-created-info p {
  margin: 0;
  color: #666;
  font-size: 1rem;
}

.cv-created-actions {
  display: flex;
  gap: 0.5rem;
}

.cv-created-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
}

.cv-detail-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #333;
  font-size: 0.95rem;
}

.cv-created-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #333;
}

/* ========== CV Full Preview (Modal) ========== */
.cv-full-preview {
  max-height: 70vh;
  overflow-y: auto;
  padding: 1rem;
}

.cv-full-preview .preview-section {
  padding: 1.5rem;
  background: #F8F8F8;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.cv-full-preview .preview-section:last-child {
  margin-bottom: 0;
}

.cv-full-preview .preview-section-title {
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

.cv-full-preview .preview-content p {
  margin: 0 0 0.5rem 0;
  color: #333;
  line-height: 1.6;
}

.cv-full-preview .preview-summary {
  margin-top: 1rem !important;
  font-style: italic;
  background: white;
  padding: 1rem;
  border-radius: 8px;
}

.cv-full-preview .preview-item {
  padding: 1rem;
  background: white;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.cv-full-preview .preview-item:last-child {
  margin-bottom: 0;
}

.cv-full-preview .preview-item h5 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.cv-full-preview .preview-item p {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.cv-full-preview .preview-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.cv-full-preview .preview-skill {
  padding: 0.5rem 1rem;
  background: var(--color-purple);
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Fix para términos y condiciones */
.terms-checkbox-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.terms-text {
  color: #333;
  font-size: 0.95rem;
  line-height: 1.5;
  margin-top: 2px; /* Alinear con checkbox */
}

.terms-text a {
  color: var(--color-purple);
  text-decoration: none;
  font-weight: 600;
}

.terms-text a:hover {
  text-decoration: underline;
}


</style>