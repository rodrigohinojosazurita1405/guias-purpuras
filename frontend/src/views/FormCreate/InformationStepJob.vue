<!-- 
  ==========================================
  INFORMATIONSTEPJOB.VUE
  ✅ VERSIÓN CORREGIDA - PATRÓN CONSISTENTE
  ==========================================
-->
<template>
  <div class="information-step-job">

    <!-- HEADER -->
    <div class="step-header">
      <div class="header-icon">
        <va-icon name="work" size="2rem" color="#FFFFFF" />
      </div>
      <div>
        <h2 class="step-title">Información del Trabajo</h2>
        <p class="step-subtitle">
          Completa los datos de la oferta laboral - Expande las secciones según sea necesario
        </p>
      </div>
    </div>

    <!-- FORMULARIO CON ACORDEONES -->
    <div class="form-content">

      <!-- ACORDEÓN 1: INFORMACIÓN BÁSICA -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.basicInfo }">
        <div class="accordion-header" @click="toggleSection('basicInfo')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="info" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Información Básica del Puesto</h3>
              <p v-if="!expandedSections.basicInfo" class="accordion-summary">
                {{ getSummary('basicInfo') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.basicInfo ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.basicInfo" class="accordion-content">

          <!-- TÍTULO DEL PUESTO -->
        <div class="form-row">
          <va-input
            v-model="localFormData.title"
            label="Título del Puesto"
            placeholder="Ej: Técnico(a) Comercial Agrónomo(a)"
            required-mark
            counter
            maxlength="100"
            :rules="[
              (v) => !!v || 'El título es requerido',
              (v) => (v && v.length >= 5) || 'Mínimo 5 caracteres'
            ]"
          >
            <template #prepend>
              <va-icon name="title" color="purple" />
            </template>
          </va-input>
          
          <div class="input-hint success-hint">
            <va-icon name="lightbulb" size="small" />
            <span>💡 Títulos claros reciben 2x más postulaciones</span>
          </div>
        </div>

        <div class="form-grid">
          <!-- NOMBRE DE LA EMPRESA -->
          <div class="form-row">
            <va-input
              v-model="localFormData.companyName"
              label="Nombre de la Empresa"
              placeholder="Ej: Agropartners S.R.L."
              :required-mark="!localFormData.companyAnonymous"
              :disabled="localFormData.companyAnonymous"
              :rules="[
                (v) => localFormData.companyAnonymous || !!v || 'El nombre de la empresa es requerido'
              ]"
            >
              <template #prepend>
                <va-icon name="business" color="purple" />
              </template>
            </va-input>
            
            <!-- CHECKBOX ANÓNIMO -->
            <div class="anonymous-checkbox">
              <va-switch
                v-model="localFormData.companyAnonymous"
                label="Publicar de forma anónima"
                color="warning"
                size="small"
              />
              <div class="input-hint" style="margin-top: 0.5rem;">
                <va-icon name="privacy_tip" size="small" />
                <span>Se mostrará como "Empresa Confidencial" sin logo ni nombre</span>
              </div>
            </div>
          </div>

        </div>

        <!-- DESCRIPCIÓN DEL TRABAJO -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.description"
            label="Descripción del Trabajo"
            placeholder="Describe el puesto, responsabilidades, y qué hace especial trabajar en tu empresa..."
            :min-rows="6"
            counter
            maxlength="1000"
            required-mark
            :rules="[
              (v) => !!v || 'La descripción es requerida',
              (v) => (v && v.length >= 50) || 'Mínimo 50 caracteres para una buena descripción'
            ]"
          >
            <template #prepend>
              <va-icon name="description" color="purple" />
            </template>
          </va-textarea>
          
          <div class="input-hint">
            <va-icon name="info" size="small" />
            <span>💡 Descripciones detalladas atraen candidatos de mejor calidad</span>
          </div>
        </div>

        <div class="form-grid">
          <!-- CATEGORÍA -->
          <div class="form-row">
            <va-select
              v-model="localFormData.jobCategory"
              label="Categoría/Área"
              :options="categoryOptions"
              placeholder="Selecciona una categoría"
              required-mark
              :rules="[(v) => !!v || 'La categoría es requerida']"
            >
              <template #prepend>
                <va-icon name="category" color="purple" />
              </template>
            </va-select>
          </div>

          <!-- CIUDAD -->
          <div class="form-row">
            <va-select
              v-model="localFormData.city"
              label="Ciudad"
              :options="cityOptions"
              placeholder="Selecciona la ciudad"
              required-mark
              :rules="[(v) => !!v || 'La ciudad es requerida']"
            >
              <template #prepend>
                <va-icon name="location_city" color="purple" />
              </template>
            </va-select>
          </div>
        </div>

        <div class="form-grid">
          <!-- TIPO DE CONTRATO -->
          <div class="form-row">
            <va-select
              v-model="localFormData.contractType"
              label="Tipo de Contrato"
              :options="contractTypeOptions"
              placeholder="Selecciona el tipo"
              required-mark
              :rules="[(v) => !!v || 'El tipo de contrato es requerido']"
            >
              <template #prepend>
                <va-icon name="schedule" color="purple" />
              </template>
            </va-select>
          </div>
        </div>

        <!-- FECHA DE VENCIMIENTO -->
        <div class="form-row">
          <va-date-input
            v-model="localFormData.expiryDate"
            label="Fecha de Vencimiento"
            placeholder="Selecciona fecha"
            required-mark
            :rules="[(v) => !!v || 'La fecha de vencimiento es requerida']"
          >
            <template #prepend>
              <va-icon name="event" color="purple" />
            </template>
          </va-date-input>
          
          <div class="input-hint">
            <va-icon name="info" size="small" />
            <span>Fecha límite para recibir postulaciones</span>
          </div>
        </div>
        </div>
      </div>

      <!-- ACORDEÓN 2: REQUISITOS Y RESPONSABILIDADES -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.requisites }">
        <div class="accordion-header" @click="toggleSection('requisites')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="assignment" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Requisitos y Responsabilidades</h3>
              <p v-if="!expandedSections.requisites" class="accordion-summary">
                {{ getSummary('requisites') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.requisites ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.requisites" class="accordion-content">

          <!-- REQUISITOS DEL PUESTO -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.requirements"
            label="Requisitos del Puesto"
            placeholder="Ej: - Título universitario en Agronomía&#10;- 2+ años de experiencia en ventas&#10;- Licencia de conducir&#10;- Disponibilidad para viajar"
            :min-rows="6"
            counter
            maxlength="1000"
            required-mark
            :rules="[(v) => !!v || 'Los requisitos son requeridos']"
          >
            <template #prepend>
              <va-icon name="checklist" color="purple" />
            </template>
          </va-textarea>
        </div>

        <!-- FUNCIONES PRINCIPALES -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.responsibilities"
            label="Funciones Principales (Opcional)"
            placeholder="Describe las responsabilidades diarias del puesto..."
            :min-rows="4"
            counter
            maxlength="800"
          >
            <template #prepend>
              <va-icon name="work_outline" color="purple" />
            </template>
          </va-textarea>
        </div>

        <div class="form-grid">
          <!-- FORMACIÓN REQUERIDA -->
          <div class="form-row">
            <va-input
              v-model="localFormData.education"
              label="Formación Requerida"
              placeholder="Ej: Título en Agronomía"
            >
              <template #prepend>
                <va-icon name="school" color="purple" />
              </template>
            </va-input>
          </div>

          <!-- EXPERIENCIA NECESARIA -->
          <div class="form-row">
            <va-input
              v-model="localFormData.experience"
              label="Experiencia Necesaria"
              placeholder="Ej: 2-3 años en ventas"
            >
              <template #prepend>
                <va-icon name="badge" color="purple" />
              </template>
            </va-input>
          </div>
        </div>

        <div class="form-grid">
          <!-- IDIOMAS -->
          <div class="form-row">
            <va-input
              v-model="localFormData.languages"
              label="Idiomas Requeridos"
              placeholder="Ej: Español (nativo), Inglés (intermedio)"
            >
              <template #prepend>
                <va-icon name="language" color="purple" />
              </template>
            </va-input>
          </div>

          <!-- HABILIDADES TÉCNICAS -->
          <div class="form-row">
            <va-input
              v-model="localFormData.technicalSkills"
              label="Habilidades Técnicas"
              placeholder="Ej: Excel avanzado, CRM"
            >
              <template #prepend>
                <va-icon name="build" color="purple" />
              </template>
            </va-input>
          </div>
        </div>
        </div>
      </div>

      <!-- ACORDEÓN 3: INFORMACIÓN SALARIAL -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.salary }">
        <div class="accordion-header" @click="toggleSection('salary')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="attach_money" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Compensación y Beneficios</h3>
              <p v-if="!expandedSections.salary" class="accordion-summary">
                {{ getSummary('salary') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.salary ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.salary" class="accordion-content">

          <div class="salary-tip">
          <va-icon name="lightbulb" color="warning" />
          <div>
            <strong>💡 Tip Pro:</strong> Publicaciones con salario visible reciben 
            <strong>3x más postulaciones</strong> y candidatos de mejor calidad.
          </div>
        </div>

        <div class="salary-options">
          <va-radio
            v-model="localFormData.salaryType"
            option="range"
            label="Rango salarial específico"
          />
          <va-radio
            v-model="localFormData.salaryType"
            option="fixed"
            label="Salario fijo"
          />
          <va-radio
            v-model="localFormData.salaryType"
            option="negotiable"
            label="A convenir"
          />
          <va-radio
            v-model="localFormData.salaryType"
            option="hidden"
            label="No mostrar salario"
          />
        </div>

        <!-- SALARIO - RANGO -->
        <div v-if="localFormData.salaryType === 'range'" class="form-row">
          <div class="salary-inputs">
            <div class="form-field">
              <va-input
                v-model.number="localFormData.salaryMin"
                label="Salario Mínimo (Bs.)"
                type="number"
                placeholder="Ej: 3000"
                required-mark
                :rules="[(v) => !!v || 'El salario mínimo es requerido']"
              >
                <template #prepend>
                  <span class="currency-symbol">Bs.</span>
                </template>
              </va-input>
            </div>
            <span class="salary-separator">-</span>
            <div class="form-field">
              <va-input
                v-model.number="localFormData.salaryMax"
                label="Salario Máximo (Bs.)"
                type="number"
                placeholder="Ej: 5000"
                required-mark
                :rules="[
                  (v) => !!v || 'El salario máximo es requerido',
                  (v) => !localFormData.salaryMin || v > localFormData.salaryMin || 'El máximo debe ser mayor al mínimo'
                ]"
              >
                <template #prepend>
                  <span class="currency-symbol">Bs.</span>
                </template>
              </va-input>
            </div>
          </div>
        </div>

        <!-- SALARIO - FIJO -->
        <div v-if="localFormData.salaryType === 'fixed'" class="form-row">
          <va-input
            v-model.number="localFormData.salaryFixed"
            label="Salario (Bs.)"
            type="number"
            placeholder="Ej: 4000"
            required-mark
            :rules="[(v) => !!v || 'El salario es requerido']"
          >
            <template #prepend>
              <span class="currency-symbol">Bs.</span>
            </template>
          </va-input>
        </div>

        <!-- BENEFICIOS ADICIONALES -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.benefits"
            label="Beneficios Adicionales (Opcional)"
            placeholder="Ej: Seguro de salud, bonos trimestrales, capacitación pagada, descuentos en productos..."
            :min-rows="3"
            counter
            maxlength="500"
          >
            <template #prepend>
              <va-icon name="card_giftcard" color="purple" />
            </template>
          </va-textarea>
          
          <div class="input-hint success-hint">
            <va-icon name="trending_up" size="small" />
            <span>💡 Incrementa el atractivo de tu oferta mencionando beneficios extra</span>
          </div>
        </div>
        </div>
      </div>

      <!-- ACORDEÓN 4: NÚMERO DE VACANTES -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.vacancies }">
        <div class="accordion-header" @click="toggleSection('vacancies')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="people" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Número de Vacantes</h3>
              <p v-if="!expandedSections.vacancies" class="accordion-summary">
                {{ getSummary('vacancies') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.vacancies ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.vacancies" class="accordion-content">

          <div class="form-row">
          <label>¿Cuántos puestos disponibles? *</label>
          <div class="vacancy-input-group">
            <button
              type="button"
              class="vacancy-btn"
              @click="decrementVacancies"
              :disabled="localFormData.vacancies <= 1"
            >
              −
            </button>
            <input
              v-model.number="localFormData.vacancies"
              type="number"
              min="1"
              max="100"
              class="vacancy-input"
              @input="(e) => updateVacancies(parseInt(e.target.value) || 1)"
            />
            <button
              type="button"
              class="vacancy-btn"
              @click="incrementVacancies"
              :disabled="localFormData.vacancies >= 100"
            >
              +
            </button>
          </div>
          <small class="form-hint">
            Puedes publicar{{ localFormData.vacancies > 1 ? ` ${localFormData.vacancies} puestos iguales` : ' 1 puesto' }}
          </small>
        </div>

        <!-- Visualización de vacantes -->
        <div class="vacancy-tracker">
          <div
            v-for="n in Math.min(localFormData.vacancies, 10)"
            :key="n"
            class="vacancy-icon"
            :title="`Vacante ${n}`"
          >
            <va-icon name="person" />
          </div>
          <div v-if="localFormData.vacancies > 10" class="vacancy-more">
            +{{ localFormData.vacancies - 10 }} más
          </div>
        </div>
        </div>
      </div>

      <!-- ACORDEÓN 5: INFORMACIÓN DE CONTACTO -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.contact }">
        <div class="accordion-header" @click="toggleSection('contact')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="contact_phone" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Información de Contacto</h3>
              <p v-if="!expandedSections.contact" class="accordion-summary">
                {{ getSummary('contact') }}
              </p>
            </div>
          </div>
          <va-icon
            :name="expandedSections.contact ? 'expand_less' : 'expand_more'"
            size="1.5rem"
            class="accordion-chevron"
          />
        </div>

        <div v-if="expandedSections.contact" class="accordion-content">

          <div class="form-grid">
          <!-- EMAIL -->
          <div class="form-row">
            <va-input
              v-model="localFormData.email"
              label="Email de Contacto"
              placeholder="rrhh@empresa.com"
              type="email"
              required-mark
              :rules="[
                (v) => !!v || 'El email es requerido',
                (v) => /.+@.+\..+/.test(v) || 'El email no es válido'
              ]"
            >
              <template #prepend>
                <va-icon name="email" color="purple" />
              </template>
            </va-input>
            
            <div class="input-hint">
              <va-icon name="info" size="small" />
              <span>Los postulantes enviarán sus CVs a este correo</span>
            </div>
          </div>

          <!-- WHATSAPP -->
          <div class="form-row">
            <va-input
              v-model="localFormData.whatsapp"
              label="WhatsApp"
              placeholder="70123456"
              required-mark
              :rules="[
                (v) => !!v || 'WhatsApp es obligatorio',
                (v) => /^[67]\d{7}$/.test(v) || 'Número inválido (debe empezar con 6 o 7 y tener 8 dígitos)'
              ]"
            >
              <template #prepend>
                <span class="whatsapp-prefix">+591</span>
              </template>
              <template #append>
                <va-icon name="whatsapp" color="success" />
              </template>
            </va-input>
          </div>

          <!-- SITIO WEB -->
          <div class="form-row">
            <va-input
              v-model="localFormData.website"
              label="Sitio Web (Opcional)"
              placeholder="https://www.empresa.com"
              type="url"
              :rules="[
                (v) => !v || v.startsWith('http://') || v.startsWith('https://') || 'Debe empezar con http:// o https://'
              ]"
            >
              <template #prepend>
                <va-icon name="language" color="purple" />
              </template>
            </va-input>
          </div>
        </div>

        <!-- INSTRUCCIONES DE APLICACIÓN -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.applicationInstructions"
            label="Instrucciones Especiales para Postular (Opcional)"
            placeholder="Ej: Enviar CV y carta de presentación. Incluir pretensión salarial. Indicar disponibilidad de inicio..."
            :min-rows="3"
            counter
            maxlength="300"
          >
            <template #prepend>
              <va-icon name="description" color="purple" />
            </template>
          </va-textarea>
          
          <div class="input-hint">
            <va-icon name="info" size="small" />
            <span>Agrega requisitos específicos para el proceso de aplicación</span>
          </div>
        </div>
        </div>
      </div>

      <!-- ACORDEÓN 6: PREGUNTAS DE FILTRADO -->
      <div class="accordion-section" :class="{ 'expanded': expandedSections.screening }">
        <div class="accordion-header" @click="toggleSection('screening')">
          <div class="accordion-header-left">
            <div class="accordion-icon">
              <va-icon name="quiz" size="1.5rem" />
            </div>
            <div class="accordion-title-group">
              <h3 class="accordion-title">Preguntas de Filtrado (Opcional)</h3>
              <p v-if="!expandedSections.screening" class="accordion-summary">
                {{ getSummary('screening') }}
              </p>
            </div>
          </div>
          <div class="accordion-header-right">
            <va-badge
              :text="`${localFormData.screeningQuestions?.length || 0}/5`"
              color="primary"
              size="large"
            />
            <va-icon
              :name="expandedSections.screening ? 'expand_less' : 'expand_more'"
              size="1.5rem"
              class="accordion-chevron"
            />
          </div>
        </div>

        <div v-if="expandedSections.screening" class="accordion-content">

          <!-- TIP BOX -->
        <div class="screening-tip-box">
          <va-icon name="lightbulb" color="#FFC107" size="1.5rem" />
          <div class="tip-content">
            <strong>💡 Tip Pro:</strong>
            <p>Las preguntas de filtrado te ayudan a recibir solo candidatos calificados y ahorran tiempo en el proceso de selección.</p>
          </div>
        </div>

        <!-- LISTA DE PREGUNTAS -->
        <div v-if="localFormData.screeningQuestions && localFormData.screeningQuestions.length > 0" class="questions-list">
          <div 
            v-for="(question, index) in localFormData.screeningQuestions" 
            :key="index" 
            class="screening-question"
          >
            <div class="question-header">
              <div class="question-number-badge">
                <va-icon name="help_outline" size="small" />
                Pregunta {{ index + 1 }}
              </div>
              <va-button
                preset="plain"
                icon="delete"
                color="danger"
                size="small"
                @click="removeScreeningQuestion(index)"
              >
                Eliminar
              </va-button>
            </div>

            <!-- TEXTO DE LA PREGUNTA -->
            <div class="question-field">
              <va-input
                v-model="question.text"
                label="Texto de la pregunta"
                placeholder="Ej: ¿Tienes licencia de conducir vigente?"
                required-mark
              >
                <template #prepend>
                  <va-icon name="text_fields" color="purple" />
                </template>
              </va-input>
            </div>

            <!-- TIPO Y OBLIGATORIEDAD -->
            <div class="question-settings">
              <va-select
                v-model="question.type"
                label="Tipo de respuesta"
                :options="questionTypeOptions"
                text-by="text"
                value-by="value"
                class="question-type-select"
                @update:model-value="(newType) => handleTypeChange(index, newType)"
              >
                <template #prepend>
                  <va-icon name="format_list_bulleted" color="purple" />
                </template>
              </va-select>

              <div class="required-switch">
                <va-switch
                  v-model="question.required"
                  label="Pregunta obligatoria"
                  color="success"
                />
              </div>
            </div>

            <!-- OPCIONES MÚLTIPLES (si el tipo es 'multiple') -->
            <div v-if="question.type === 'multiple'" class="multiple-options-section">
              <label class="options-label">
                <va-icon name="list" size="small" />
                Opciones de respuesta
              </label>

              <div class="options-manager">
                <!-- Lista de opciones -->
                <div v-if="question.optionsList && question.optionsList.length > 0" class="options-list">
                  <div 
                    v-for="(option, optIndex) in question.optionsList" 
                    :key="optIndex"
                    class="option-item"
                  >
                    <va-icon name="radio_button_unchecked" size="small" color="#999" />
                    <span class="option-text">{{ option }}</span>
                    <va-button
                      preset="plain"
                      icon="close"
                      size="small"
                      @click="removeOption(index, optIndex)"
                    />
                  </div>
                </div>

                <!-- Input para agregar nueva opción -->
                <div class="add-option-input">
                  <va-input
                    v-model="newOptions[index]"
                    placeholder="Escribe una opción y presiona Enter"
                    @keypress.enter="addOption(index)"
                  >
                    <template #prepend>
                      <va-icon name="add_circle_outline" color="purple" />
                    </template>
                    <template #append>
                      <va-button
                        preset="plain"
                        icon="add"
                        size="small"
                        @click="addOption(index)"
                        :disabled="!newOptions[index] || !newOptions[index].trim()"
                      >
                        Agregar
                      </va-button>
                    </template>
                  </va-input>
                </div>

                <div v-if="!question.optionsList || question.optionsList.length === 0" class="no-options-hint">
                  <va-icon name="info" size="small" />
                  <span>Agrega al menos 2 opciones para esta pregunta</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- BOTÓN AGREGAR PREGUNTA -->
        <va-button
          v-if="!localFormData.screeningQuestions || localFormData.screeningQuestions.length < 5"
          @click="addScreeningQuestion"
          color="primary"
          icon="add_circle"
          class="add-question-btn"
        >
          Agregar Pregunta de Filtrado ({{ localFormData.screeningQuestions?.length || 0 }}/5)
        </va-button>

        <!-- MENSAJE MÁXIMO ALCANZADO -->
        <div v-else class="max-questions-message">
          <va-icon name="info" color="warning" />
          <span>Has alcanzado el máximo de 5 preguntas de filtrado</span>
        </div>

        <!-- VISTA PREVIA DE PREGUNTAS -->
        <div v-if="localFormData.screeningQuestions && localFormData.screeningQuestions.length > 0" class="screening-preview">
          <div class="preview-header">
            <va-icon name="visibility" size="1.5rem" color="success" />
            <div>
              <h4 class="preview-title">Vista previa para candidatos</h4>
              <p class="preview-description">Así verán los candidatos las preguntas de filtrado:</p>
            </div>
          </div>
          
          <div class="preview-questions">
            <div 
              v-for="(q, i) in localFormData.screeningQuestions" 
              :key="i"
              class="preview-question"
            >
              <label class="preview-label">
                {{ i + 1 }}. {{ q.text || 'Sin texto aún...' }}
                <span v-if="q.required" class="required-mark">*</span>
              </label>
              
              <!-- Tipo: Texto -->
              <div v-if="q.type === 'text'" class="preview-input">
                <input type="text" placeholder="El candidato escribirá su respuesta aquí..." disabled />
              </div>
              
              <!-- Tipo: Sí/No -->
              <div v-else-if="q.type === 'yesno'" class="preview-radio">
                <label class="radio-option">
                  <div class="custom-radio">
                    <div class="radio-circle"></div>
                  </div>
                  <span>Sí</span>
                </label>
                <label class="radio-option">
                  <div class="custom-radio">
                    <div class="radio-circle"></div>
                  </div>
                  <span>No</span>
                </label>
              </div>
              
              <!-- Tipo: Opción Múltiple -->
              <div v-else-if="q.type === 'multiple'" class="preview-select">
                <select disabled>
                  <option value="">Seleccionar una opción...</option>
                  <template v-if="q.optionsList && q.optionsList.length > 0">
                    <option v-for="(opt, j) in q.optionsList" :key="j">
                      {{ opt }}
                    </option>
                  </template>
                  <template v-else>
                    <option disabled>(Agrega opciones arriba)</option>
                  </template>
                </select>
                
                <div v-if="!q.optionsList || q.optionsList.length === 0" class="preview-hint">
                  <va-icon name="arrow_upward" size="small" color="warning" />
                  <span>Agrega al menos 2 opciones de respuesta en la sección de arriba</span>
                </div>
              </div>

              <!-- Fallback: tipo desconocido o no definido -->
              <div v-else class="preview-warning">
                <va-icon name="error" size="small" color="warning" />
                <span>Por favor selecciona un tipo de pregunta válido (Texto corto, Sí / No, o Opción múltiple).</span>
              </div>
            </div>
          </div>
        </div>
        </div>
      </div>

      <!-- BOTONES DE NAVEGACIÓN -->
      <div class="navigation-buttons">
        <va-button
          preset="secondary"
          icon="arrow_back"
          @click="handleBack"
        >
          Atrás
        </va-button>

        <va-button
          preset="primary"
          icon="arrow_forward"
          @click="handleNext"
          class="next-button"
        >
          Siguiente
        </va-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// ========== PROPS Y EMITS ==========
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])

// ========== ACCORDION STATE ==========
const expandedSections = ref({
  basicInfo: true,
  requisites: false,
  salary: false,
  vacancies: false,
  contact: false,
  screening: false
})

// ========== DATA LOCAL (REF + WATCH) ==========
const localFormData = ref({
  title: props.modelValue.title || '',
  companyName: props.modelValue.companyName || '',
  companyAnonymous: props.modelValue.companyAnonymous || false,
  description: props.modelValue.description || '',
  jobCategory: props.modelValue.jobCategory || '',
  city: props.modelValue.city || '',
  contractType: props.modelValue.contractType || '',
  expiryDate: props.modelValue.expiryDate || null,
  requirements: props.modelValue.requirements || '',
  responsibilities: props.modelValue.responsibilities || '',
  education: props.modelValue.education || '',
  experience: props.modelValue.experience || '',
  languages: props.modelValue.languages || '',
  technicalSkills: props.modelValue.technicalSkills || '',
  salaryType: props.modelValue.salaryType || 'range',
  salaryMin: props.modelValue.salaryMin || null,
  salaryMax: props.modelValue.salaryMax || null,
  salaryFixed: props.modelValue.salaryFixed || null,
  benefits: props.modelValue.benefits || '',
  vacancies: props.modelValue.vacancies || 1,
  email: props.modelValue.email || '',
  whatsapp: props.modelValue.whatsapp || '',
  website: props.modelValue.website || '',
  applicationInstructions: props.modelValue.applicationInstructions || '',
  screeningQuestions: props.modelValue.screeningQuestions || []
})

// ========== OPCIONES DE FORMULARIO ==========
const categoryOptions = [
  { text: 'Administración', value: 'Administración' },
  { text: 'Agronomía y Veterinaria', value: 'Agronomía y Veterinaria' },
  { text: 'Comercial y Ventas', value: 'Comercial y Ventas' },
  { text: 'Construcción', value: 'Construcción' },
  { text: 'Educación', value: 'Educación' },
  { text: 'Ingeniería', value: 'Ingeniería' },
  { text: 'Legal', value: 'Legal' },
  { text: 'Marketing y Publicidad', value: 'Marketing y Publicidad' },
  { text: 'Salud', value: 'Salud' },
  { text: 'Tecnología e Informática', value: 'Tecnología e Informática' },
  { text: 'Turismo y Hostelería', value: 'Turismo y Hostelería' },
  { text: 'Otro', value: 'Otro' }
]

const contractTypeOptions = [
  { text: 'Tiempo Completo', value: 'Tiempo Completo' },
  { text: 'Medio Tiempo', value: 'Medio Tiempo' },
  { text: 'Por Proyecto', value: 'Por Proyecto' },
  { text: 'Temporal', value: 'Temporal' },
  { text: 'Pasantía', value: 'Pasantía' },
  { text: 'Freelance', value: 'Freelance' }
]

const questionTypeOptions = [
  { text: 'Texto corto', value: 'text' },
  { text: 'Sí / No', value: 'yesno' },
  { text: 'Opción múltiple', value: 'multiple' }
]

const cityOptions = [
  { text: 'Cochabamba', value: 'Cochabamba' },
  { text: 'La Paz', value: 'La Paz' },
  { text: 'Santa Cruz', value: 'Santa Cruz' },
  { text: 'Sucre', value: 'Sucre' },
  { text: 'Tarija', value: 'Tarija' },
  { text: 'Potosí', value: 'Potosí' },
  { text: 'Oruro', value: 'Oruro' },
  { text: 'Beni', value: 'Beni' },
  { text: 'Pando', value: 'Pando' }
]

// ========== WATCH PARA SINCRONIZACIÓN ==========
watch(localFormData, (newValue) => {
  emit('update:modelValue', { ...props.modelValue, ...newValue })
}, { deep: true })


// ========== REF PARA NUEVAS OPCIONES (TEMP) ==========
const newOptions = ref({})

// ========== MÉTODOS DE SCREENING QUESTIONS ==========
const addScreeningQuestion = () => {
  if (!localFormData.value.screeningQuestions) {
    localFormData.value.screeningQuestions = []
  }
  if (localFormData.value.screeningQuestions.length < 5) {
    localFormData.value.screeningQuestions.push({
      text: '',
      type: 'text',
      optionsList: [], // Array de opciones
      required: true
    })
  }
}

const removeScreeningQuestion = (index) => {
  localFormData.value.screeningQuestions.splice(index, 1)
  // Limpiar el input temporal de esa pregunta
  delete newOptions.value[index]
}

// Agregar opción a pregunta de tipo múltiple
const addOption = (questionIndex) => {
  const optionText = newOptions.value[questionIndex]
  
  if (!optionText || !optionText.trim()) {
    return
  }
  
  const question = localFormData.value.screeningQuestions[questionIndex]
  
  if (!question.optionsList) {
    question.optionsList = []
  }
  
  // Agregar opción si no está vacía y no está duplicada
  const trimmedOption = optionText.trim()
  if (!question.optionsList.includes(trimmedOption)) {
    question.optionsList.push(trimmedOption)
  }
  
  // Limpiar input
  newOptions.value[questionIndex] = ''
}

// Eliminar opción de pregunta de tipo múltiple
const removeOption = (questionIndex, optionIndex) => {
  const question = localFormData.value.screeningQuestions[questionIndex]
  if (question.optionsList) {
    question.optionsList.splice(optionIndex, 1)
  }
}
// Manejar cambio de tipo de pregunta

const handleTypeChange = (questionIndex, newType) => {
  const question = localFormData.value.screeningQuestions[questionIndex]
  question.type = newType
  
  // Inicializar optionsList si cambia a multiple
  if (newType === "multiple" && !question.optionsList) {
    question.optionsList = []
  }
  
  console.log(`Pregunta ${questionIndex} cambió a tipo: ${newType}`, question)
}

// ========== MÉTODOS DE VACANTES ==========
const incrementVacancies = () => {
  if (localFormData.value.vacancies < 100) {
    localFormData.value.vacancies++
  }
}

const decrementVacancies = () => {
  if (localFormData.value.vacancies > 1) {
    localFormData.value.vacancies--
  }
}

const updateVacancies = (value) => {
  if (value >= 1 && value <= 100) {
    localFormData.value.vacancies = value
  }
}

// ========== ACCORDION METHODS ==========
const toggleSection = (sectionName) => {
  expandedSections.value[sectionName] = !expandedSections.value[sectionName]
}

const getSummary = (sectionName) => {
  switch (sectionName) {
    case 'basicInfo':
      if (localFormData.value.title && localFormData.value.city) {
        return `${localFormData.value.title} - ${localFormData.value.city}`
      }
      return 'Completa los datos básicos del puesto'

    case 'requisites':
      if (localFormData.value.requirements) {
        return 'Requisitos definidos'
      }
      return 'Define los requisitos y responsabilidades'

    case 'salary':
      if (localFormData.value.salaryType === 'range' && localFormData.value.salaryMin) {
        return `Bs. ${localFormData.value.salaryMin} - ${localFormData.value.salaryMax || '...'}`
      } else if (localFormData.value.salaryType === 'fixed' && localFormData.value.salaryFixed) {
        return `Bs. ${localFormData.value.salaryFixed}`
      } else if (localFormData.value.salaryType === 'negotiable') {
        return 'Salario a convenir'
      } else if (localFormData.value.salaryType === 'hidden') {
        return 'Salario no visible'
      }
      return 'Configura la compensación'

    case 'vacancies':
      return `${localFormData.value.vacancies || 1} ${localFormData.value.vacancies === 1 ? 'vacante' : 'vacantes'} disponible${localFormData.value.vacancies === 1 ? '' : 's'}`

    case 'contact':
      if (localFormData.value.email && localFormData.value.whatsapp) {
        return `${localFormData.value.email} - +591 ${localFormData.value.whatsapp}`
      }
      return 'Agrega información de contacto'

    case 'screening':
      const count = localFormData.value.screeningQuestions?.length || 0
      return count > 0 ? `${count} pregunta${count !== 1 ? 's' : ''} de filtrado` : 'Sin preguntas de filtrado'

    default:
      return ''
  }
}

// ========== NAVEGACIÓN ==========
const handleNext = () => {
  if (validate()) {
    emit('next')
  }
}

const handleBack = () => {
  emit('back')
}

// ========== VALIDACIÓN ==========
const validate = () => {
  const errors = []
  
  if (!localFormData.value.title) {
    errors.push('El título del puesto es requerido')
  }
  
  // Validar empresa solo si NO es anónima
  if (!localFormData.value.companyAnonymous && !localFormData.value.companyName) {
    errors.push('El nombre de la empresa es requerido (o marca como anónima)')
  }
  
  if (!localFormData.value.description || localFormData.value.description.length < 50) {
    errors.push('La descripción debe tener al menos 50 caracteres')
  }
  
  if (!localFormData.value.jobCategory) {
    errors.push('La categoría es requerida')
  }
  
  if (!localFormData.value.city) {
    errors.push('La ciudad es requerida')
  }
  
  if (!localFormData.value.contractType) {
    errors.push('El tipo de contrato es requerido')
  }
  
  if (!localFormData.value.expiryDate) {
    errors.push('La fecha de vencimiento es requerida')
  }
  
  if (!localFormData.value.requirements) {
    errors.push('Los requisitos son requeridos')
  }
  
  // Validación de salario
  if (localFormData.value.salaryType === 'range') {
    if (!localFormData.value.salaryMin) {
      errors.push('El salario mínimo es requerido')
    }
    if (!localFormData.value.salaryMax) {
      errors.push('El salario máximo es requerido')
    }
    if (localFormData.value.salaryMin && localFormData.value.salaryMax && 
        localFormData.value.salaryMin >= localFormData.value.salaryMax) {
      errors.push('El salario máximo debe ser mayor al mínimo')
    }
  }
  
  if (localFormData.value.salaryType === 'fixed' && !localFormData.value.salaryFixed) {
    errors.push('El salario es requerido')
  }
  
  if (!localFormData.value.email) {
    errors.push('El email de contacto es requerido')
  } else if (!/.+@.+\..+/.test(localFormData.value.email)) {
    errors.push('El email no es válido')
  }
  
  if (!localFormData.value.whatsapp) {
    errors.push('El WhatsApp es requerido')
  } else if (!/^[67]\d{7}$/.test(localFormData.value.whatsapp)) {
    errors.push('El número de WhatsApp debe ser válido (8 dígitos, empezar con 6 o 7)')
  }
  
  // Validación de website (opcional pero si lo llena debe ser válido)
  if (localFormData.value.website && 
      !localFormData.value.website.startsWith('http://') && 
      !localFormData.value.website.startsWith('https://')) {
    errors.push('La URL del sitio web debe empezar con http:// o https://')
  }
  
  if (errors.length > 0) {
    console.error('❌ ERRORES DE VALIDACIÓN:', errors)
    console.log('📋 Datos actuales:', localFormData.value)
    
    // Mostrar alert con los errores
    const errorMessage = errors.join('\n• ')
    alert(`⚠️ Por favor completa los siguientes campos:\n\n• ${errorMessage}`)
    
    return false
  }
  
  console.log('✅ Validación exitosa - todos los campos obligatorios completos')
  return true
}

// ========== EXPONER MÉTODOS AL PADRE ==========
defineExpose({
  validate
})
</script>

<style scoped>
.information-step-job {
  width: 100%;
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  min-height: 100vh;
  padding: 2rem;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  max-width: 1100px;
  margin-left: auto;
  margin-right: auto;
  padding: 2.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border-top: 3px solid #7C3AED;
  width: 100%;
}

.header-icon {
  width: 72px;
  height: 72px;
  border-radius: 12px;
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.step-title {
  font-size: 2rem;
  font-weight: 800;
  color: #0F172A;
  margin: 0;
  letter-spacing: -0.5px;
}

.step-subtitle {
  font-size: 0.95rem;
  color: #64748B;
  margin: 0.5rem 0 0 0;
  line-height: 1.5;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  max-width: 1100px;
  margin: 0 auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
  background: #F8FAFC;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  position: relative;
}

.form-section::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #7C3AED 0%, #A855F7 100%);
  border-radius: 12px 0 0 12px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: #1E293B;
  margin: 0;
  padding-bottom: 0.75rem;
}

.section-description {
  color: #666;
  font-size: 0.95rem;
  margin: -0.5rem 0 0.5rem 0;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #1E293B;
  font-size: 0.95rem;
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #475569;
  padding: 0.75rem 1rem;
  background: #E0E7FF;
  border-radius: 8px;
  border-left: 3px solid #7C3AED;
  line-height: 1.4;
}

.success-hint {
  background: #ECFDF5;
  color: #047857;
  border-left-color: #10B981;
}

.whatsapp-prefix {
  font-weight: 700;
  color: #7C3AED;
  padding: 0.5rem 0.75rem;
  background: #E0E7FF;
  border-radius: 6px;
  font-size: 0.9rem;
}

.currency-symbol {
  font-weight: 700;
  color: #7C3AED;
  padding: 0.5rem 0.75rem;
  background: #E0E7FF;
  border-radius: 6px;
  font-size: 0.9rem;
}

/* ========== Logo Preview ========== */
.logo-preview-container {
  margin-top: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px dashed #E2E8F0;
}

.logo-preview-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #7C3AED;
  margin: 0 0 1rem 0;
}

.logo-preview-image {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  object-fit: cover;
  border: 3px solid #7C3AED;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}

/* ========== Salary Section ========== */
.salary-tip {
  display: flex;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #FEF3C7 0%, #FEE2B8 100%);
  border-left: 4px solid #F59E0B;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
  color: #78350F;
  line-height: 1.6;
}

.salary-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  background: #F8FAFC;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
}

.salary-inputs {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
}

.salary-separator {
  font-size: 1.5rem;
  font-weight: 700;
  color: #7C3AED;
  padding-bottom: 0.5rem;
}

/* ========== Screening Questions ========== */
.screening-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.screening-tip-box {
  display: flex;
  gap: 1.25rem;
  padding: 1.75rem;
  background: linear-gradient(135deg, #FEF3C7 0%, #FEE2B8 100%);
  border-left: 4px solid #F59E0B;
  border-radius: 12px;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.tip-content {
  flex: 1;
}

.tip-content strong {
  display: block;
  color: #B45309;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.tip-content p {
  margin: 0;
  color: #78350F;
  font-size: 0.95rem;
  line-height: 1.6;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.screening-question {
  padding: 2rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.screening-question:hover {
  border-color: #7C3AED;
  box-shadow: 0 4px 16px rgba(124, 58, 237, 0.12);
  transform: translateY(-2px);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.question-number-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  white-space: nowrap;
  flex-shrink: 0;
}

.question-field {
  margin-bottom: 1.5rem;
}

.question-settings {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  align-items: flex-end;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: #F8FAFC;
  border-radius: 8px;
  border: 1px solid #E2E8F0;
}

.question-type-select {
  min-width: auto;
}

.required-switch {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

/* Opciones Múltiples */
.multiple-options-section {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px dashed #CBD5E1;
  transition: all 0.3s ease;
}

.multiple-options-section:hover {
  border-color: #7C3AED;
  background: #F9F5FF;
}

.options-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  color: #1E293B;
  margin-bottom: 1.25rem;
  font-size: 1rem;
}

.options-manager {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.option-item:hover {
  border-color: #7C3AED;
  background: #F9F5FF;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.1);
}

.option-text {
  flex: 1;
  color: #1E293B;
  font-size: 0.95rem;
  word-break: break-word;
}

.add-option-input {
  margin-top: 0.5rem;
}

.no-options-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #FFF3E0;
  border-radius: 8px;
  color: #F57C00;
  font-size: 0.9rem;
}

.add-question-btn {
  width: 100%;
  margin-top: 1.5rem;
  font-weight: 600;
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
  margin-top: 1.5rem;
}

/* ========== Vacantes ========== */
.vacancy-input-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.vacancy-btn {
  width: 44px;
  height: 44px;
  border: 2px solid #E2E8F0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  color: #7C3AED;
  font-size: 1.25rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.vacancy-btn:hover:not(:disabled) {
  background: #F8FAFC;
  border-color: #7C3AED;
  box-shadow: 0 2px 4px rgba(124, 58, 237, 0.2);
}

.vacancy-btn:disabled {
  color: #CBD5E1;
  cursor: not-allowed;
  border-color: #E2E8F0;
}

.vacancy-input {
  width: 100px;
  padding: 0.75rem;
  border: 2px solid #E2E8F0;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 700;
  text-align: center;
  color: #7C3AED;
  transition: all 0.2s;
}

.vacancy-input:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.vacancy-tracker {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  margin-top: 1rem;
}

.vacancy-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  border-radius: 8px;
  color: white;
  font-size: 1.25rem;
  transition: all 0.2s;
}

.vacancy-icon:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.2);
}

.vacancy-more {
  padding: 0.5rem 1rem;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-weight: 700;
  color: #7C3AED;
  font-size: 0.9rem;
}

/* ========== Responsive ========== */
@media (max-width: 1024px) {
  .information-step-job {
    padding: 1.5rem;
  }

  .form-content {
    padding: 1.5rem;
  }

  .form-section {
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .information-step-job {
    max-width: 100%;
    padding: 1rem;
  }

  .step-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 1.5rem;
  }

  .header-icon {
    width: 64px;
    height: 64px;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .step-subtitle {
    font-size: 0.95rem;
  }

  .form-content {
    padding: 1.25rem;
    gap: 1.5rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-section {
    padding: 1rem;
  }

  .section-title {
    font-size: 1rem;
  }

  .salary-inputs {
    flex-direction: column;
    align-items: stretch;
  }

  .salary-separator {
    display: none;
  }

  .question-settings {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .information-step-job {
    padding: 0.5rem;
  }

  .step-header {
    padding: 1rem;
  }

  .header-icon {
    width: 56px;
    height: 56px;
  }

  .step-title {
    font-size: 1.25rem;
  }

  .step-subtitle {
    font-size: 0.9rem;
  }

  .form-content {
    padding: 1rem;
    gap: 1rem;
  }

  .form-section {
    padding: 0.75rem;
  }

  .section-title {
    font-size: 1rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

/* ========== Checkbox Anónimo ========== */
.anonymous-checkbox {
  margin-top: 1rem;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #FEF3C7 0%, #FEE2B8 100%);
  border-left: 4px solid #F59E0B;
  border-radius: 12px;
}

/* ========== Vista Previa de Screening Questions ========== */
.screening-preview {
  margin-top: 2.5rem;
  padding: 2rem;
  background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
  border-radius: 16px;
  border: 2px solid #0EA5E9;
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.1);
}

.preview-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.preview-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0EA5E9;
  margin: 0 0 0.25rem 0;
}

.preview-description {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.preview-questions {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.preview-question {
  padding: 1.75rem;
  background: white;
  border-radius: 12px;
  border: 2px solid #E0E0E0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.preview-label {
  display: block;
  font-weight: 600;
  font-size: 1rem;
  color: #333;
  margin-bottom: 1rem;
}

.required-mark {
  color: #EF4444;
  margin-left: 0.25rem;
  font-weight: 700;
}

.preview-input input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  font-size: 0.95rem;
  background: #F9FAFB;
  color: #999;
  transition: border-color 0.2s ease;
}

.preview-input input:focus {
  outline: none;
  border-color: #5C0099;
}

.preview-radio {
  display: flex;
  gap: 2rem;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  padding: 0.75rem 1.25rem;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  transition: all 0.2s ease;
  background: white;
}

.radio-option:hover {
  border-color: #5C0099;
  background: #F8F4FF;
}

/* Radio button personalizado */
.custom-radio {
  width: 20px;
  height: 20px;
  border: 2px solid #9E9E9E;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  background: white;
}

.radio-option:hover .custom-radio {
  border-color: #5C0099;
}

.radio-circle {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #9E9E9E;
  opacity: 0.3;
}

.radio-option:hover .radio-circle {
  background: #5C0099;
  opacity: 1;
}

.radio-option span {
  color: #555;
  font-size: 1rem;
}

.preview-select select {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  font-size: 0.95rem;
  background: #F9FAFB;
  color: #555;
  cursor: not-allowed;
  transition: border-color 0.2s ease;
}

.preview-select select:focus {
  outline: none;
  border-color: #5C0099;
}

.preview-warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #FFF3E0;
  border-radius: 8px;
  color: #F57C00;
  font-size: 0.9rem;
  font-weight: 500;
}

.preview-hint {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  margin-top: 0.75rem;
  background: #FFF9E6;
  border-radius: 8px;
  border: 2px dashed #FFC107;
  color: #F57C00;
  font-size: 0.9rem;
  font-weight: 500;
}

/* ========== Botones de Navegación ========== */
.navigation-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: space-between;
  align-items: center;
  margin-top: 2.5rem;
  padding-top: 2rem;
  border-top: 2px solid #E2E8F0;
}

.navigation-buttons .next-button {
  margin-left: auto;
}

@media (max-width: 768px) {
  .navigation-buttons {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .navigation-buttons button {
    width: 100%;
  }

  .navigation-buttons .next-button {
    margin-left: 0;
  }
}

/* ========== ACCORDION STYLES ========== */
.accordion-section {
  background: white;
  border-radius: 16px;
  border: 2px solid #E2E8F0;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-bottom: 1.5rem;
}

.accordion-section:hover {
  border-color: #CBD5E1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.accordion-section.expanded {
  border-color: #7C3AED;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.12);
}

.accordion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  cursor: pointer;
  background: white;
  transition: all 0.3s ease;
  user-select: none;
  gap: 1.5rem;
}

.accordion-header:hover {
  background: #F8FAFC;
}

.accordion-section.expanded .accordion-header {
  background: linear-gradient(135deg, #F9F5FF 0%, #F3E8FF 100%);
  border-bottom: 2px solid #E9D5FF;
}

.accordion-header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
  min-width: 0;
}

.accordion-header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.accordion-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: linear-gradient(135deg, #E0E7FF 0%, #DDD6FE 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7C3AED;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.accordion-section.expanded .accordion-icon {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.accordion-title-group {
  flex: 1;
  min-width: 0;
}

.accordion-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1E293B;
  margin: 0;
  transition: color 0.3s ease;
}

.accordion-section.expanded .accordion-title {
  color: #7C3AED;
}

.accordion-summary {
  font-size: 0.9rem;
  color: #64748B;
  margin: 0.25rem 0 0 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: all 0.3s ease;
}

.accordion-chevron {
  color: #94A3B8;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
}

.accordion-section.expanded .accordion-chevron {
  color: #7C3AED;
  transform: rotate(180deg);
}

.accordion-content {
  padding: 2rem;
  background: white;
  animation: accordionSlideDown 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes accordionSlideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile accordion adjustments */
@media (max-width: 768px) {
  .accordion-header {
    padding: 1.25rem 1.5rem;
    gap: 1rem;
  }

  .accordion-header-left {
    gap: 1rem;
  }

  .accordion-icon {
    width: 48px;
    height: 48px;
  }

  .accordion-title {
    font-size: 1.1rem;
  }

  .accordion-summary {
    font-size: 0.85rem;
  }

  .accordion-content {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .accordion-header {
    padding: 1rem;
  }

  .accordion-header-left {
    gap: 0.75rem;
  }

  .accordion-icon {
    width: 40px;
    height: 40px;
  }

  .accordion-title {
    font-size: 1rem;
  }

  .accordion-summary {
    font-size: 0.8rem;
  }

  .accordion-content {
    padding: 1rem;
  }

  .accordion-header-right {
    gap: 0.5rem;
  }
}
</style>