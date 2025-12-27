<!-- 
  ==========================================
  SUMMARYCARD.VUE - ACTUALIZADO
  ==========================================

  Resumen completo del anuncio antes de publicar.
  Enfocado exclusivamente en Trabajos.
-->

<template>
  <div class="summary-card">
    <!-- Para tipos no-job, mostrar el resumen antiguo -->
    <template v-if="type !== 'job'">
      <!--
        ==========================================
        HEADER
        ==========================================
      -->
      <div class="summary-header">
        <div class="header-icon">
          <va-icon name="assignment" size="2rem" color="purple" />
        </div>
        <div>
          <h2 class="summary-title">Resumen de tu Anuncio</h2>
          <p class="summary-subtitle">
            Verifica que toda la información sea correcta antes de publicar
          </p>
        </div>
      </div>

      <!--
        ==========================================
        SECCIONES DE RESUMEN
        ==========================================
      -->
      <div class="summary-content">

      <!-- SELECCIÓN INICIAL (JOBS ONLY) -->
      <div v-if="type === 'job' && jobData && (jobData.subcategory || jobData.city)" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="check_circle" size="1.25rem" />
            Selección Inicial
          </h3>
        </div>

        <div class="section-content">
          <div v-if="jobData.subcategory" class="info-row">
            <span class="label">Tipo de Empleo:</span>
            <span class="value">{{ jobData.subcategory }}</span>
          </div>
          <div v-if="jobData.city" class="info-row">
            <span class="label">Ubicación:</span>
            <span class="value">{{ jobData.city }}</span>
          </div>
        </div>
      </div>

      <!-- CATEGORÍA Y UBICACIÓN -->
      <div v-if="type !== 'job'" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="category" size="1.25rem" />
            Categoría y Ubicación
          </h3>
          <va-button
            v-if="editable"
            size="small"
            preset="plain"
            @click="$emit('edit-step', 1)"
          >
            Editar
          </va-button>
        </div>
        
        <div class="section-content">
          <div class="info-row">
            <span class="label">Categoría:</span>
            <span class="value">{{ getCategoryName(formData.category) }}</span>
          </div>
          <div class="info-row">
            <span class="label">Subcategoría:</span>
            <span class="value">{{ formData.subcategory || 'N/A' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Ciudad:</span>
            <span class="value">{{ formData.city }}</span>
          </div>
          <div class="info-row">
            <span class="label">Dirección:</span>
            <span class="value">{{ formData.address }}</span>
          </div>
        </div>
      </div>

      <!-- INFORMACIÓN GENERAL (NO para jobs) -->
      <div v-if="type !== 'job'" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="info" size="1.25rem" />
            Información General
          </h3>
          <va-button
            v-if="editable"
            size="small"
            preset="plain"
            @click="$emit('edit-step', 2)"
          >
            Editar
          </va-button>
        </div>
        
        <div class="section-content">
          <div class="info-row">
            <span class="label">Título:</span>
            <span class="value bold">{{ formData.title }}</span>
          </div>

          <!-- Campo DESCRIPTION -->
          <div v-if="formData.description" class="info-row full-width">
            <span class="label">Descripción:</span>
            <p class="value description">{{ formData.description }}</p>
          </div>

          <!-- Contacto (común para todos) -->
          <div class="info-row">
            <span class="label">WhatsApp:</span>
            <span class="value">+591 {{ formData.whatsapp }}</span>
          </div>
          <div v-if="formData.email" class="info-row">
            <span class="label">Email:</span>
            <span class="value">{{ formData.email }}</span>
          </div>
          <div v-if="formData.website" class="info-row">
            <span class="label">Sitio web:</span>
            <span class="value">{{ formData.website }}</span>
          </div>
        </div>
      </div>

      <!-- IMÁGENES DEL NEGOCIO (NO para jobs) -->
      <div v-if="type !== 'job'" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="image" size="1.25rem" />
            Imágenes del Negocio
          </h3>
          <va-button
            v-if="editable"
            size="small"
            preset="plain"
            @click="$emit('edit-step', 3)"
          >
            Editar
          </va-button>
        </div>

        <div class="section-content">
          <div v-if="formData.images && formData.images.length > 0" class="images-grid">
            <div
              v-for="(img, index) in formData.images"
              :key="index"
              class="image-preview"
            >
              <img
                :src="getImageUrl(img)"
                :alt="`Imagen ${index + 1}`"
              />
              <div v-if="index === 0" class="main-badge">Principal</div>
            </div>
          </div>
          <p v-else class="empty-message">No se han agregado imágenes</p>
        </div>
      </div>

      <!-- INFORMACIÓN ESENCIAL (ACORDEÓN 1) -->
      <div v-if="type === 'job' && jobData" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="work" size="1.25rem" />
            Información Esencial
          </h3>
        </div>

        <div class="section-content">
          <div class="info-row">
            <span class="label">Título:</span>
            <span class="value bold">{{ jobData.title }}</span>
          </div>
          <div class="info-row">
            <span class="label">Empresa:</span>
            <span class="value">{{ jobData.companyAnonymous ? 'Empresa Confidencial' : jobData.companyName }}</span>
          </div>
          <section class="content-block description-block">
            <h2 class="block-title">
              <va-icon name="description" size="small" />
              Descripción del Puesto
            </h2>
            <p class="block-text">{{ jobData.description }}</p>
          </section>
        </div>
      </div>

      <!-- UBICACIÓN (ACORDEÓN 3) -->
      <div v-if="type === 'job' && jobData" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="location_on" size="1.25rem" />
            Ubicación
          </h3>
        </div>

        <div class="section-content">
          <div class="info-row">
            <span class="label">Categoría:</span>
            <span class="value">{{ jobData.jobCategory }}</span>
          </div>
          <div class="info-row">
            <span class="label">Ciudad:</span>
            <span class="value">{{ jobData.city }}</span>
          </div>
          <div v-if="jobData.municipality" class="info-row">
            <span class="label">Provincia/Municipio:</span>
            <span class="value">{{ jobData.municipality }}</span>
          </div>
          <div class="info-row">
            <span class="label">Tipo de Contrato:</span>
            <span class="value">{{ jobData.contractType }}</span>
          </div>
          <div class="info-row">
            <span class="label">Modalidad:</span>
            <span class="value">{{ getModalityValue(jobData.modality) }}</span>
          </div>
          <div class="info-row">
            <span class="label">Fecha Límite Postulación:</span>
            <span class="value">{{ jobData.applicationDeadline || jobData.expiryDate }}</span>
          </div>
        </div>
      </div>

      <!-- COMPENSACIÓN Y VACANTES (ACORDEÓN 4) -->
      <div v-if="type === 'job' && jobData" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="attach_money" size="1.25rem" />
            Compensación y Vacantes
          </h3>
        </div>

        <div class="section-content">
          <div class="info-row">
            <span class="label">Salario:</span>
            <span class="value bold">
              <template v-if="jobData.salaryType === 'range'">
                Bs. {{ jobData.salaryMin }} - {{ jobData.salaryMax }}
              </template>
              <template v-else-if="jobData.salaryType === 'fixed'">
                Bs. {{ jobData.salaryFixed }}
              </template>
              <template v-else-if="jobData.salaryType === 'negotiable'">
                A convenir
              </template>
              <template v-else-if="jobData.salaryType === 'pretension_salarial'">
                Indique su pretensión salarial
              </template>
              <template v-else>
                No mostrado
              </template>
            </span>
          </div>
          <div v-if="jobData.vacancies" class="info-row">
            <span class="label">Número de Vacantes:</span>
            <span class="value bold">{{ jobData.vacancies }} {{ jobData.vacancies === 1 ? 'vacante' : 'vacantes' }}</span>
          </div>
        </div>
      </div>

      <!-- CONFIGURACIÓN DE APLICACIÓN (JOBS ONLY) -->
      <div v-if="type === 'job' && jobData" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="how_to_reg" size="1.25rem" />
            Configuración de Aplicación
          </h3>
        </div>

        <div class="section-content">
          <div class="info-row">
            <span class="label">Tipo de Aplicación:</span>
            <span class="value">
              <template v-if="jobData.applicationType === 'internal'">
                Interna (en Guías Púrpuras)
              </template>
              <template v-else-if="jobData.applicationType === 'external'">
                Externa
              </template>
              <template v-else>
                Ambas
              </template>
            </span>
          </div>
          <div v-if="['external', 'both'].includes(jobData.applicationType)" class="info-row full-width">
            <span class="label">URL Externa:</span>
            <span class="value url">{{ jobData.externalApplicationUrl || 'No especificada' }}</span>
          </div>

          <!-- INFORMACIÓN DE CONTACTO PARA APLICACIÓN EXTERNA -->
          <template v-if="jobData.applicationType === 'external'">
            <div v-if="jobData.email" class="info-row">
              <span class="label">Email de Contacto:</span>
              <span class="value">{{ jobData.email }}</span>
            </div>
            <div v-if="jobData.whatsapp" class="info-row">
              <span class="label">WhatsApp/Teléfono:</span>
              <span class="value">{{ jobData.whatsapp }}</span>
            </div>
            <div v-if="jobData.website" class="info-row full-width">
              <span class="label">Sitio Web:</span>
              <span class="value url">{{ jobData.website }}</span>
            </div>
            <div v-if="jobData.applicationInstructions" class="info-row full-width">
              <span class="label">Instrucciones de Aplicación:</span>
              <span class="value">{{ jobData.applicationInstructions }}</span>
            </div>
          </template>

          <!-- PREGUNTAS DE FILTRADO (solo para aplicación interna) -->
          <div v-if="jobData.applicationType === 'internal'" class="info-row full-width">
            <span class="label">Preguntas de Filtrado:</span>
            <template v-if="jobData.screeningQuestions?.length">
              <div class="screening-list">
                <div v-for="(question, qIndex) in jobData.screeningQuestions" :key="qIndex" class="screening-item">
                  <strong>{{ qIndex + 1 }}. {{ question.text }}</strong>
                  <span class="question-type">({{ getQuestionTypeLabel(question.type) }})</span>
                </div>
              </div>
            </template>
            <span v-else class="value text-muted" style="color: #94a3b8; font-style: italic;">
              No se agregaron preguntas de filtrado
            </span>
          </div>
        </div>
      </div>

      <!-- PLAN SELECCIONADO (GENERIC) -->
      <div v-if="type !== 'job' && formData.plan" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="workspace_premium" size="1.25rem" />
            Plan Seleccionado
          </h3>
          <va-button
            v-if="editable"
            size="small"
            preset="plain"
            @click="$emit('edit-step', 4)"
          >
            Editar
          </va-button>
        </div>

        <div class="section-content">
          <div class="plan-card" :class="`plan-${formData.plan}`">
            <div class="plan-badge">
              <va-icon :name="getPlanIcon(formData.plan)" />
              {{ getPlanName(formData.plan) }}
            </div>
            <p class="plan-description">{{ getPlanDescription(formData.plan) }}</p>
          </div>
        </div>
      </div>
      </div>
    </template>

    <!-- ==========================================
      LAYOUT PRINCIPAL PARA JOBS (Estilo Trabajito)
      ========================================== -->
      <template v-if="type === 'job'">
        <!-- TÍTULO GENERAL -->
        <div class="job-summary-header">
          <h2 class="job-summary-title">Resumen y Configuración de Pago de tu Anuncio</h2>
          <p class="job-summary-subtitle">Revisa los detalles de tu publicación antes de completar el pago por favor</p>
        </div>

        <div class="job-listing-card">
          <!-- ========== HEADER PROFESIONAL: BADGES ARRIBA + INFORMACIÓN EN GRID ========== -->
          <div class="job-header">
            <!-- TOP: BADGES EN LÍNEA HORIZONTAL -->
            <div v-if="planBadges.length > 0" class="badges-top-row">
              <span v-for="planBadge in planBadges" :key="planBadge" class="badge" :class="`badge-${getBadgeClass(planBadge)}`">
                {{ planBadge }}
              </span>
            </div>

            <!-- MIDDLE: GRID DE 3 COLUMNAS (LOGO + INFO + METADATA) -->
            <div class="header-grid">
              <!-- COLUMNA 1: LOGO GRANDE -->
              <div class="logo-column">
                <div class="company-logo-container">
                  <div v-if="jobData.logo && !jobData.companyAnonymous" class="company-logo">
                    <img :src="jobData.logo" :alt="jobData.companyName" class="logo-image" />
                  </div>
                  <div v-else class="company-logo-placeholder">
                    <va-icon name="business" :size="isMobile ? '3.5rem' : '4rem'" />
                  </div>
                </div>
              </div>

              <!-- COLUMNA 2: INFORMACIÓN PRINCIPAL -->
              <div class="info-column">
                <!-- Título del Puesto (Grande) -->
                <div class="job-title-wrapper">
                  <span class="job-title-label">Oferta laboral</span>
                  <h1 class="job-title">{{ jobData.title }}</h1>
                </div>

                <!-- Empresa destacada -->
                <div class="company-name-section">
                  <va-icon name="business" class="company-icon" />
                  <span class="company-name-text">
                    {{ jobData.companyAnonymous ? 'Empresa Confidencial' : jobData.companyName }}
                  </span>
                </div>

                <!-- Grid de Información Compacto: 3 columnas -->
                <div class="info-grid-compact">
                  <div class="info-item-compact">
                    <va-icon name="location_on" size="small" class="info-icon" />
                    <div class="info-text">
                      <span class="info-label-compact">Ubicación</span>
                      <span class="info-value-compact">
                        {{ jobData.municipality ? `${jobData.city}, ${jobData.municipality}` : jobData.city }}
                      </span>
                    </div>
                  </div>

                  <div class="info-item-compact">
                    <va-icon name="work_history" size="small" class="info-icon" />
                    <div class="info-text">
                      <span class="info-label-compact">Contrato</span>
                      <span class="info-value-compact">{{ jobData.contractType }}</span>
                    </div>
                  </div>

                  <div class="info-item-compact">
                    <va-icon name="laptop" size="small" class="info-icon" />
                    <div class="info-text">
                      <span class="info-label-compact">Modalidad</span>
                      <span class="info-value-compact">{{ getModalityValue(jobData.modality) }}</span>
                    </div>
                  </div>

                  <div class="info-item-compact">
                    <va-icon name="category" size="small" class="info-icon" />
                    <div class="info-text">
                      <span class="info-label-compact">Categoría</span>
                      <span class="info-value-compact">{{ jobData.jobCategory }}</span>
                    </div>
                  </div>

                  <div class="info-item-compact">
                    <va-icon name="calendar_today" size="small" class="info-icon" />
                    <div class="info-text">
                      <span class="info-label-compact">Cierra</span>
                      <span class="info-value-compact" :class="{ 'expired-text': isExpired }">
                        {{ isExpired ? 'CERRADA' : formatDate(jobData.applicationDeadline || jobData.expiryDate) }}
                      </span>
                    </div>
                  </div>

                  <div class="info-item-compact">
                    <va-icon name="how_to_reg" size="small" class="info-icon" />
                    <div class="info-text">
                      <span class="info-label-compact">Aplicación</span>
                      <span class="info-value-compact">
                        <template v-if="jobData.applicationType === 'internal'">
                          Interna
                        </template>
                        <template v-else-if="jobData.applicationType === 'external'">
                          Externa
                        </template>
                        <template v-else>
                          Ambas
                        </template>
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- COLUMNA 3: METADATA -->
              <div class="metadata-column">
                <div class="metadata-container">
                  <div v-if="jobData.vacancies" class="meta-item">
                    <va-icon name="person" size="small" />
                    <span>{{ jobData.vacancies }} {{ jobData.vacancies === 1 ? 'vacante' : 'vacantes' }}</span>
                  </div>
                  <div v-if="jobData.publishedDate" class="meta-item">
                    <va-icon name="schedule" size="small" />
                    <span>Publicado {{ formatPublishedDate(jobData.publishedDate) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ========== CONTENIDO PRINCIPAL (Secciones fluidas) ========== -->
          <div class="job-content">
            <!-- ===== DESCRIPCIÓN ===== -->
            <section class="content-block description-block">
              <h2 class="block-title">
                <va-icon name="description" size="small" />
                Descripción del Puesto Laboral
              </h2>
             <div class="block-text job-description-html" v-html="jobData.description"></div>
            </section>

            <!-- ===== COMPENSACIÓN ===== -->
            <section class="content-block salary-block">
              <h2 class="block-title">
                <va-icon name="attach_money" size="small" />
                Compensación
              </h2>

              <!-- Salario Destacado -->
              <div class="salary-container">
                <p class="salary-label">Salario:</p>
                <p class="salary-amount">
                  <template v-if="jobData.salaryType === 'range'">
                    Bs. {{ jobData.salaryMin?.toLocaleString() }} - {{ jobData.salaryMax?.toLocaleString() }}
                  </template>
                  <template v-else-if="jobData.salaryType === 'fixed'">
                    Bs. {{ jobData.salaryFixed?.toLocaleString() }}
                  </template>
                  <template v-else-if="jobData.salaryType === 'negotiable'">
                    A convenir
                  </template>
                  <template v-else-if="jobData.salaryType === 'pretension_salarial'">
                    Indique su pretensión salarial
                  </template>
                  <template v-else>
                    No especificado
                  </template>
                </p>
              </div>
            </section>

            <!-- ===== PREGUNTAS DE FILTRADO ===== -->
            <section v-if="jobData.applicationType === 'internal' && jobData.screeningQuestions?.length" class="content-block screening-block">
              <h2 class="block-title">
                <va-icon name="quiz" size="small" />
                Preguntas de Filtrado
              </h2>
              <div class="screening-list">
                <div v-for="(question, qIndex) in jobData.screeningQuestions" :key="qIndex" class="screening-item">
                  <div class="question-number">{{ qIndex + 1 }}.</div>
                  <div class="question-content">
                    <strong class="question-text">{{ question.text }}</strong>
                    <span class="question-type">({{ getQuestionTypeLabel(question.type) }})</span>
                    <span v-if="question.required" class="question-required">• Requerida</span>
                  </div>
                </div>
              </div>
            </section>

            <!-- ===== INFORMACIÓN DE APLICACIÓN EXTERNA ===== -->
            <section v-if="jobData.applicationType === 'external'" class="content-block application-external-block">
              <h2 class="block-title">
                <va-icon name="open_in_new" size="small" color="purple" />
                Información de Aplicación Externa
              </h2>
              <div class="external-application-info">
                <div v-if="jobData.externalApplicationUrl" class="info-item-external">
                  <span class="info-label-external">
                    <va-icon name="link" size="small" color="purple" />
                    URL del Formulario:
                  </span>
                  <a :href="jobData.externalApplicationUrl" target="_blank" class="info-value-external url-link">
                    {{ jobData.externalApplicationUrl }}
                    <va-icon name="open_in_new" size="x-small" color="purple" />
                  </a>
                </div>
                <div v-if="jobData.applicationInstructions" class="info-item-external">
                  <span class="info-label-external">
                    <va-icon name="description" size="small" color="purple" />
                    Instrucciones:
                  </span>
                  <p class="info-value-external instructions-text">{{ jobData.applicationInstructions }}</p>
                </div>
                <div v-if="jobData.email" class="info-item-external">
                  <span class="info-label-external">
                    <va-icon name="email" size="small" color="purple" />
                    Email de Contacto:
                  </span>
                  <span class="info-value-external">{{ jobData.email }}</span>
                </div>
                <div v-if="jobData.whatsapp" class="info-item-external">
                  <span class="info-label-external">
                    <va-icon name="phone" size="small" color="purple" />
                    WhatsApp/Teléfono:
                  </span>
                  <span class="info-value-external">{{ jobData.whatsapp }}</span>
                </div>
                <div v-if="jobData.website" class="info-item-external">
                  <span class="info-label-external">
                    <va-icon name="language" size="small" color="purple" />
                    Sitio Web:
                  </span>
                  <a :href="jobData.website" target="_blank" class="info-value-external url-link">
                    {{ jobData.website }}
                    <va-icon name="open_in_new" size="x-small" color="purple" />
                  </a>
                </div>
              </div>
            </section>

            <!-- ===== SECCIÓN PAGO Y COMPROBANTE (SIEMPRE VISIBLE) ===== -->
            <section class="content-block payment-section">
              <div class="payment-accordion always-open">
                <!-- Header (sin interacción) -->
                <div class="accordion-header static-header">
                  <div class="accordion-title">
                    <va-icon name="payment" size="small" />
                    <span>Información y método de pago de su anuncio</span>
                  </div>
                </div>

                <!-- Contenido SIEMPRE visible -->
                <div class="accordion-content">
                    <!-- Resumen compacto -->
                    <div class="payment-summary">
                      <div class="summary-item">
                        <span class="summary-label">Plan:</span>
                        <span class="summary-value">{{ getJobPlanName(jobData.selectedPlan) }}</span>
                      </div>
                      <div class="summary-item">
                        <span class="summary-label">Monto:</span>
                        <span class="summary-value bold">{{ getPaymentAmount(jobData.selectedPlan) }}</span>
                      </div>
                      <div class="summary-item">
                        <span class="summary-label">Ref:</span>
                        <code class="summary-ref">{{ paymentReference }}</code>
                        <button @click="copyToClipboard(paymentReference)" class="copy-btn-small" title="Copiar">
                          <va-icon name="content_copy" size="x-small" />
                        </button>
                      </div>
                    </div>

                    <!-- Contenedor de dos columnas -->
                    <div class="payment-container">
                      <!-- Columna 1: QR -->
                      <div class="payment-qr-column">
                        <div class="qr-card-compact">
                          <div class="qr-label">Escanea para pagar</div>
                          <div class="qr-image-container">
                            <img
                              :src="getPaymentQRPath(jobData.selectedPlan)"
                              :alt="`QR - ${getJobPlanName(jobData.selectedPlan)}`"
                              class="qr-image"
                            />
                          </div>
                        </div>
                      </div>

                      <!-- Columna 2: Comprobante -->
                      <div class="payment-proof-column">
                        <div class="proof-card-compact">
                          <div class="proof-label">Sube tu comprobante</div>

                          <!-- Zona de carga -->
                          <div v-if="!proofOfPaymentPreview" class="proof-upload-zone-compact">
                            <input
                              type="file"
                              ref="proofFileInput"
                              accept="image/*"
                              @change="handleProofUpload"
                              class="hidden-input"
                            />
                            <div @click="$refs.proofFileInput?.click()" class="upload-area-compact">
                              <va-icon name="cloud_upload" size="small" color="purple" />
                              <p class="upload-text-compact">Arrastra o haz clic</p>
                              <small class="upload-hint-compact">PNG, JPG - Máx 5MB</small>
                            </div>
                          </div>

                          <!-- Preview -->
                          <div v-else class="proof-preview-compact">
                            <img :src="proofOfPaymentPreview" :alt="'Comprobante'" class="preview-image-compact" />
                            <button @click="clearProofUpload" class="remove-btn-compact">
                              <va-icon name="close" size="x-small" />
                            </button>
                          </div>

                          <!-- Estado -->
                          <div v-if="proofOfPaymentPreview" class="proof-status-compact">
                            <va-icon name="check_circle" color="success" size="small" />
                            <span>Cargado</span>
                          </div>
                          <div v-else class="proof-required-compact">
                            <va-icon name="info" color="warning" size="small" />
                            <span>Requerido</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Aviso -->
                    <div class="payment-notice-compact">
                      <va-icon name="info" size="x-small" />
                      <span>Escanea el QR, realiza el pago y sube el comprobante</span>
                    </div>

                    <!-- Información de Contacto para Ayuda -->
                    <div class="payment-support-compact">
                      <div class="support-icon">
                        <va-icon name="help_outline" size="small" />
                      </div>
                      <div class="support-content">
                        <p class="support-title">¿Tienes dificultad con el pago?</p>
                        <p class="support-text">
                          Contáctanos por
                          <a href="https://wa.me/59165324767" target="_blank" class="support-link">
                            WhatsApp: 6532-4767
                          </a>
                          o envía el comprobante a
                          <a href="mailto:info@guiaspurpuras.com.bo" class="support-link">
                            info@guiaspurpuras.com.bo
                          </a>
                          para su verificación.
                        </p>
                      </div>
                    </div>

                    <!-- ===== SEPARADOR ===== -->
                    <div class="billing-separator">
                      <div class="separator-line"></div>
                      <div class="separator-text">
                        <va-icon name="receipt" size="small" />
                        Información de Facturación
                      </div>
                      <div class="separator-line"></div>
                    </div>

                    <!-- ===== CHECKBOX "SOY CONTRIBUYENTE" ===== -->
                    <div class="contributor-checkbox-container">
                      <label class="contributor-checkbox">
                        <input
                          type="checkbox"
                          v-model="isContributor"
                          class="checkbox-input"
                        />
                        <span class="checkbox-custom"></span>
                        <span class="checkbox-label">
                          <va-icon name="account_balance" size="small" />
                          Soy contribuyente (Requiero factura)
                        </span>
                      </label>
                      <p class="checkbox-hint">
                        Marca esta opción si necesitas factura para tu compra
                      </p>
                    </div>

                    <!-- ===== FORMULARIO DE FACTURACIÓN (Habilitado solo si es contribuyente) ===== -->
                    <div v-if="isContributor" class="billing-form-group">
                      <!-- Fila 1: Razón Social (span completo) -->
                      <div class="billing-field full-width">
                        <label class="billing-label">Razón Social / Nombre Completo</label>
                        <input
                          v-model="billingData.businessName"
                          type="text"
                          placeholder="Nombre de tu empresa o tu nombre completo"
                          class="billing-input"
                        />
                      </div>

                      <!-- Fila 2: NIT y CI -->
                      <div class="billing-field">
                        <label class="billing-label">NIT (opcional si tiene CI)</label>
                        <input
                          v-model="billingData.nit"
                          type="text"
                          placeholder="Número de NIT"
                          class="billing-input"
                        />
                      </div>

                      <div class="billing-field">
                        <label class="billing-label">N.º C.I. (Cédula de Identidad)</label>
                        <input
                          v-model="billingData.ci"
                          type="text"
                          placeholder="Número de Cédula de Identidad"
                          class="billing-input"
                        />
                      </div>

                      <!-- Fila 3: Complemento CI (span completo) -->
                      <div class="billing-field full-width">
                        <label class="billing-label">Complemento C.I. (opcional)</label>
                        <input
                          v-model="billingData.ciComplement"
                          type="text"
                          placeholder="Ej: 1A, 2B"
                          class="billing-input"
                          maxlength="3"
                        />
                      </div>

                      <!-- Fila 4: MÉTODO DE ENVÍO DE FACTURA -->
                      <div class="billing-field full-width delivery-method-section">
                        <label class="billing-label delivery-method-title">
                          <va-icon name="send" size="small" />
                          ¿Cómo deseas recibir tu factura electrónica?
                        </label>
                        <p class="delivery-method-hint">Selecciona al menos un método de envío</p>

                        <div class="delivery-checkboxes">
                          <!-- Checkbox: Email -->
                          <label class="delivery-checkbox">
                            <input
                              type="checkbox"
                              v-model="sendByEmail"
                              class="checkbox-input"
                            />
                            <span class="checkbox-custom"></span>
                            <span class="checkbox-label">
                              <va-icon name="email" size="small" />
                              Por Email
                            </span>
                          </label>

                          <!-- Checkbox: WhatsApp -->
                          <label class="delivery-checkbox">
                            <input
                              type="checkbox"
                              v-model="sendByWhatsApp"
                              class="checkbox-input"
                            />
                            <span class="checkbox-custom"></span>
                            <span class="checkbox-label">
                              <va-icon name="whatsapp" size="small" />
                              Por WhatsApp
                            </span>
                          </label>
                        </div>
                      </div>

                      <!-- Fila 5: Email (solo si sendByEmail está marcado) -->
                      <div v-if="sendByEmail" class="billing-field full-width">
                        <label class="billing-label required-field">Email para Factura Electrónica</label>
                        <input
                          v-model="billingData.invoiceEmail"
                          type="email"
                          placeholder="correo@ejemplo.com"
                          class="billing-input"
                          required
                        />
                      </div>

                      <!-- Fila 6: WhatsApp (solo si sendByWhatsApp está marcado) -->
                      <div v-if="sendByWhatsApp" class="billing-field full-width">
                        <label class="billing-label required-field">Celular / WhatsApp</label>
                        <input
                          v-model="billingData.whatsapp"
                          type="tel"
                          placeholder="+591 7XXXXXXX"
                          class="billing-input"
                          required
                        />
                      </div>
                    </div>

                    <!-- Aviso de responsabilidad (fuera del grid) -->
                    <div class="billing-alert">
                      <va-icon name="warning" size="small" color="warning" />
                      <div class="alert-content">
                        <strong>Importante:</strong> Guías Púrpuras Bolivia no se hará responsable por errores tipograficos o númericos en los datos de facturación ingresados por el usuario (Razón Social, NIT/CI, Complemento, Email, Celular).
                        el, usuario tiene la obligación deverificar que todos los datos sean correctos antes de publicar el anuncio, ya que estos se utilizarán para la emisión de facturas electrónicas según el SIN. Una vez ingresado todos los datos y verificado el pago
                        por nuestro equipo, le enviaremos su factura digital al medio solicitado por el usuario en un plazo máximo de 24 horas desde la aprobación del anuncio.
                      </div>
                    </div>
                  </div>
              </div>
            </section>
          </div>
        </div>
      </template>

    <!-- BOTONES DE ACCIÓN (JOBS ONLY) -->
    <div v-if="type === 'job'" class="action-buttons">
      <button class="btn btn-secondary" @click="$emit('back')" :disabled="isSubmitting">
        <va-icon name="arrow_back" size="small" />
        ATRÁS
      </button>
      <button
        class="btn btn-primary"
        @click="$emit('submit')"
        :disabled="isSubmitting"
      >
        <va-icon v-if="!isSubmitting" name="publish" size="small" />
        <va-icon v-else name="hourglass_empty" size="small" class="rotating" />
        {{ isSubmitting ? 'PUBLICANDO...' : 'PUBLICAR OFERTA' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, nextTick, computed, ref } from 'vue'
import { PAYMENT_CONFIG } from '@/config/paymentConfig'
import { usePublishStore } from '@/stores/usePublishStore'

// ==========================================
// PROPS & EMITS
// ==========================================
const props = defineProps({
  formData: {
    type: Object,
    required: true
  },
  editable: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'generic', // 'job', 'restaurant', 'professional', 'business', 'generic'
  },
  jobData: {
    type: Object,
    default: null
  },
  isSubmitting: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['edit-step', 'submit'])

// ==========================================
// STORES
// ==========================================
const publishStore = usePublishStore()

// ==========================================
// REFERENCIAS Y STATE
// ==========================================
const isMobile = ref(window.innerWidth <= 480)
const proofFileInput = ref(null)
const proofOfPaymentPreview = ref(null)
const isContributor = ref(false) // Estado del checkbox "Soy contribuyente"
const sendByEmail = ref(false) // Checkbox: Enviar factura por Email
const sendByWhatsApp = ref(false) // Checkbox: Enviar factura por WhatsApp
const billingData = ref({
  businessName: '',
  nit: '',
  ci: '',
  ciComplement: '',
  invoiceEmail: '',
  whatsapp: ''
})
const paymentReference = computed(() => {
  if (!props.jobData?.selectedPlan) return ''
  return PAYMENT_CONFIG.generatePaymentReference(props.jobData.selectedPlan)
})

// ==========================================
// COMPUTED PROPERTIES Y MÉTODOS
// ==========================================

// Verificar si la convocatoria está cerrada
const isExpired = computed(() => {
  // CRÍTICO: Usar applicationDeadline (fecha límite de postulación) NO expiryDate
  const deadline = props.jobData?.applicationDeadline || props.jobData?.expiryDate
  if (!deadline) return false
  const deadlineDate = new Date(deadline)
  return deadlineDate < new Date()
})

// Formatear fecha de vencimiento
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('es-BO', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

// Formatear fecha de publicación con texto relativo
const formatPublishedDate = (date) => {
  if (!date) return ''
  const published = new Date(date)
  const now = new Date()
  const diffMs = now - published
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'hace unos momentos'
  if (diffMins < 60) return `hace ${diffMins} min`
  if (diffHours < 24) return `hace ${diffHours}h`
  if (diffDays < 1) return 'hoy'
  if (diffDays === 1) return 'ayer'
  return `hace ${diffDays} días`
}

const getCategoryName = (category) => {
  const categories = {
    trabajos: 'Trabajos'
  }
  return categories[category] || category
}

const getPlanName = (plan) => {
  const plans = {
    free: 'Plan Gratis',
    featured: 'Plan Destacado',
    top: 'Plan TOP'
  }
  return plans[plan] || plan
}

// Obtener el valor de modalidad (puede venir como objeto o string)
const getModalityValue = (modality) => {
  if (!modality) return 'Presencial'
  // Si es un objeto de va-select, extraer el valor
  if (typeof modality === 'object' && modality.value) {
    return modality.value
  }
  // Si es un objeto de va-select con text, extraer el text
  if (typeof modality === 'object' && modality.text) {
    return modality.text
  }
  // Si ya es un string, devolverlo directamente
  return modality
}

const getPlanIcon = (plan) => {
  const icons = {
    free: 'check_circle',
    featured: 'star',
    top: 'workspace_premium'
  }
  return icons[plan] || 'check_circle'
}

const getPlanDescription = (plan) => {
  const descriptions = {
    free: 'Tu anuncio estará visible por 7 días con 2 imágenes',
    featured: 'Tu anuncio aparecerá destacado por 30 días con 5 imágenes',
    top: 'Tu anuncio siempre aparecerá primero por 30 días con 10 imágenes'
  }
  return descriptions[plan] || ''
}

const getImageUrl = (image) => {
  if (!image) return ''
  
  if (image instanceof File) {
    return URL.createObjectURL(image)
  }
  
  if (typeof image === 'string') {
    return image
  }
  
  if (image.file instanceof File) {
    return URL.createObjectURL(image.file)
  }
  
  if (image.url) {
    return image.url
  }
  
  return ''
}

const formatPrice = (price) => {
  if (!price && price !== 0) return '0.00'
  return parseFloat(price).toFixed(2)
}

const formatIngredients = (ingredients) => {
  if (Array.isArray(ingredients)) {
    return ingredients.join(', ')
  }
  return ingredients
}

const getQuestionTypeLabel = (type) => {
  const labels = {
    text: 'Texto corto',
    yesno: 'Sí / No',
    multiple: 'Opción múltiple'
  }
  return labels[type] || type
}

const getJobPlanName = (planKey) => {
  const normalizedKey = planKey?.toLowerCase()
  const planInfo = PAYMENT_CONFIG.getPlanInfo(normalizedKey)
  return planInfo ? `Plan ${planInfo.name}` : planKey
}

const getJobPlanIcon = (plan) => {
  const icons = {
    estandar: 'check_circle',
    escencial: 'check_circle',
    purpura: 'star',
    impulso: 'workspace_premium'
  }
  const normalizedKey = plan?.toLowerCase()
  return icons[normalizedKey] || 'check_circle'
}

const getJobPlanDescription = (planKey) => {
  const normalizedKey = planKey?.toLowerCase()
  const planInfo = PAYMENT_CONFIG.getPlanInfo(normalizedKey)
  if (!planInfo) return ''
  return `Plan ${planInfo.name} - ${planInfo.price} ${planInfo.currency} Tu oferta de trabajo estará visible por ${planInfo.duration}.`
}

// Obtener badges del plan seleccionado
// Solo mostrar features adicionales, no el plan base
const getPlanBadges = (plan) => {
  const badges = {
    estandar: [],
    purpura: ['Destacado', 'Urgente'],
    impulso: ['Patrocinado', 'Urgente']
  }
  return badges[plan] || []
}

// Computar badges a mostrar
const planBadges = computed(() => {
  return getPlanBadges(props.jobData?.selectedPlan)
})

// Obtener clase CSS para el badge basado en su tipo
const getBadgeClass = (badgeText) => {
  const classList = {
    'Básico': 'basic',
    'Destacado': 'featured',
    'Patrocinado': 'sponsored',
    'Urgente': 'urgent'
  }
  return classList[badgeText] || 'basic'
}

// Obtener ícono para cada badge
const getBadgeIcon = (badgeText) => {
  const icons = {
    'Básico': 'verified',
    'Destacado': 'verified_user',
    'Patrocinado': 'workspace_premium',
    'Urgente': 'priority_high'
  }
  return icons[badgeText] || null
}

// Obtener ruta del QR del plan
const getPaymentQRPath = (planKey) => {
  return PAYMENT_CONFIG.getQRPath(planKey)
}

// Obtener monto a pagar
const getPaymentAmount = (planKey) => {
  return PAYMENT_CONFIG.getPlanPrice(planKey)
}

// Manejar carga de archivo de comprobante
const handleProofUpload = (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  // Validar tamaño (máx 5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('El archivo es muy grande. Máximo 5MB')
    return
  }

  // Validar tipo de archivo
  if (!file.type.startsWith('image/')) {
    alert('Por favor, selecciona una imagen válida (PNG, JPG, JPEG)')
    return
  }

  // Crear preview
  const reader = new FileReader()
  reader.onload = (e) => {
    proofOfPaymentPreview.value = e.target?.result
  }
  reader.readAsDataURL(file)

  // FASE 7.1: Almacenar el archivo en la store para envío al backend
  publishStore.setProofOfPaymentFile(file)
}

// Limpiar carga de comprobante
const clearProofUpload = () => {
  proofOfPaymentPreview.value = null
  if (proofFileInput.value) {
    proofFileInput.value.value = ''
  }
  // FASE 7.1: Limpiar el archivo de la store
  publishStore.setProofOfPaymentFile(null)
}

// Copiar referencia de pago al portapapeles
const copyToClipboard = (text) => {
  if (!text) return
  navigator.clipboard.writeText(text).then(() => {
    alert('Referencia de pago copiada al portapapeles')
  }).catch(() => {
    alert('No se pudo copiar al portapapeles')
  })
}

// Sincronizar billingData con publishStore cuando cambie
watch(billingData, (newBillingData) => {
  if (isContributor.value) {
    publishStore.setJobData({
      billingData: { ...newBillingData }
    })
  }
}, { deep: true })

// Limpiar datos de facturación cuando se desmarca "Soy contribuyente"
// Y sincronizar cuando se marca
watch(isContributor, (newValue) => {
  if (!newValue) {
    // Limpiar todos los campos de facturación
    billingData.value = {
      businessName: '',
      nit: '',
      ci: '',
      ciComplement: '',
      invoiceEmail: '',
      whatsapp: ''
    }
    // Limpiar checkboxes de método de envío
    sendByEmail.value = false
    sendByWhatsApp.value = false
    // Limpiar en la store también
    publishStore.setJobData({
      billingData: null
    })
  } else {
    // Cuando se marca el checkbox, sincronizar datos actuales (aunque estén vacíos)
    publishStore.setJobData({
      billingData: { ...billingData.value }
    })
  }
})

// Limpiar invoiceEmail cuando se desmarca el checkbox de Email
watch(sendByEmail, (newValue) => {
  if (!newValue) {
    // Limpiar el campo de email si se desmarca
    billingData.value.invoiceEmail = ''
  }
})

// Limpiar whatsapp cuando se desmarca el checkbox de WhatsApp
watch(sendByWhatsApp, (newValue) => {
  if (!newValue) {
    // Limpiar el campo de whatsapp si se desmarca
    billingData.value.whatsapp = ''
  }
})

// ==========================================
// MAPA PREVIEW
// ==========================================
let mapInstance = null

const initMap = async () => {
  if (!props.formData.coordinates) return
  
  // Esperar a que el DOM esté listo
  await nextTick()
  
  const mapElement = document.getElementById('map-preview')
  if (!mapElement) return
  
  // Cargar Leaflet dinámicamente
  if (!window.L) {
    // Agregar CSS de Leaflet
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(link)
    
    // Cargar script de Leaflet
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.onload = () => createMap()
    document.head.appendChild(script)
  } else {
    createMap()
  }
}

const createMap = () => {
  const mapElement = document.getElementById('map-preview')
  if (!mapElement || !props.formData.coordinates) return
  
  try {
    // Parsear coordenadas (formato: "lat,lng" o "lat, lng")
    const [lat, lng] = props.formData.coordinates.split(',').map(coord => parseFloat(coord.trim()))
    
    if (isNaN(lat) || isNaN(lng)) {
      console.error('Coordenadas inválidas:', props.formData.coordinates)
      return
    }
    
    // Limpiar mapa existente
    if (mapInstance) {
      mapInstance.remove()
    }
    
    // Crear mapa
    mapInstance = window.L.map('map-preview').setView([lat, lng], 15)
    
    // Agregar tiles de OpenStreetMap
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(mapInstance)
    
    // Agregar marker
    window.L.marker([lat, lng]).addTo(mapInstance)
      .bindPopup(props.formData.gpsAddress || 'Ubicación del negocio')
      .openPopup()
  } catch (error) {
    console.error('Error al crear mapa:', error)
  }
}

// Inicializar mapa cuando el componente se monta
onMounted(async () => {
  // Cargar planes desde backend para sincronizar con Django Admin
  await PAYMENT_CONFIG.loadPlansFromBackend()

  // DEBUG: Ver qué datos de aplicación externa están llegando
  if (props.type === 'job') {
    console.log('🔍 SummaryCard - jobData recibido:', {
      applicationType: props.jobData?.applicationType,
      externalApplicationUrl: props.jobData?.externalApplicationUrl,
      email: props.jobData?.email,
      whatsapp: props.jobData?.whatsapp,
      website: props.jobData?.website,
      applicationInstructions: props.jobData?.applicationInstructions,
      todosLosDatos: props.jobData
    })
  }

  if (props.formData.coordinates) {
    initMap()
  }

  // Detectar cambios de tamaño de pantalla
  const handleResize = () => {
    isMobile.value = window.innerWidth <= 480
  }
  window.addEventListener('resize', handleResize)

  // Cleanup
  return () => {
    window.removeEventListener('resize', handleResize)
  }
})

// Re-inicializar si cambian las coordenadas
watch(() => props.formData.coordinates, (newCoords) => {
  if (newCoords) {
    setTimeout(() => initMap(), 100)
  }
})
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.summary-card {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background: linear-gradient(135deg, #FBFAFF 0%, #f8f6fb 100%);
  min-height: 100vh;
}

/* ==========================================
   HEADER
   ========================================== */
.summary-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  padding: 2.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border-top: 3px solid #7C3AED;
}

.header-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(92, 0, 153, 0.2);
}

.summary-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
}

.summary-subtitle {
  font-size: 1rem;
  color: #666;
  margin: 0.25rem 0 0 0;
}

/* ==========================================
   CONTENIDO
   ========================================== */
.summary-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ==========================================
   SECCIONES
   ========================================== */
.summary-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  border: 1px solid #E2E8F0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-dark);
  margin: 0;
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* ==========================================
   INFO ROWS
   ========================================== */
.info-row {
  display: flex;
  gap: 1rem;
  padding: 0.5rem 0;
}

.info-row.full-width {
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.info-row .label {
  font-weight: 600;
  color: #666;
  min-width: 150px;
}

.info-row .value {
  color: var(--color-purple-darkest);
  flex: 1;
}

.info-row .value.bold {
  font-weight: 700;
  font-size: 1.125rem;
}

.info-row .value.description {
  line-height: 1.6;
  margin: 0;
}

.info-row .value.url {
  font-family: 'Courier New', monospace;
  color: var(--color-purple);
  font-weight: 600;
  word-break: break-all;
}

/* ==========================================
   FEATURES/CHIPS
   ========================================== */
.features-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

/* ==========================================
   IMÁGENES
   ========================================== */
.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.image-preview {
  position: relative;
  width: 100%;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.main-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
}

/* ==========================================
   MENÚ / PLATOS
   ========================================== */
.menu-count {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
}

.menu-items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.menu-item-preview {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.menu-item-image {
  position: relative;
  width: 100%;
  height: 160px;
  background: #F5F3F8;
}

.menu-item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F5F3F8 0%, #F1ECFF 100%);
}

.featured-star {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 1.5rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.menu-item-info {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu-item-name {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
}

.menu-item-price {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-purple);
  margin: 0;
}

.menu-item-desc {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.menu-item-ingredients {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #666;
  line-height: 1.3;
}

.menu-item-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  margin-top: 0.25rem;
}

/* ==========================================
   PLAN
   ========================================== */
.plan-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  border: 2px solid #E0E0E0;
}

.plan-card.plan-free {
  border-color: #4CAF50;
  background: #F1F8F4;
}

.plan-card.plan-featured {
  border-color: var(--color-yellow-primary);
  background: #FFFBF0;
}

.plan-card.plan-top {
  border-color: var(--color-purple);
  background: linear-gradient(135deg, #F5F0FF 0%, #FFFFFF 100%);
}

.plan-card.plan-estandar {
  border-color: #4CAF50;
  background: #F1F8F4;
}

.plan-card.plan-purpura {
  border-color: var(--color-purple);
  background: linear-gradient(135deg, #F5F0FF 0%, #FFFFFF 100%);
}

.plan-card.plan-impulso {
  border-color: var(--color-purple-dark);
  background: linear-gradient(135deg, #EDE9FE 0%, #F3E8FF 100%);
}

.plan-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 1rem;
}

.plan-description {
  font-size: 0.95rem;
  color: #666;
  margin: 0;
  line-height: 1.6;
}

/* ==========================================
   EMPTY STATES
   ========================================== */
.empty-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  color: #999;
  font-style: italic;
  margin: 0;
}

/* ==========================================
   MAPA PREVIEW
   ========================================== */
.map-preview-container {
  width: 100%;
  margin-top: 1rem;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.map-preview {
  width: 100%;
  height: 300px;
  border-radius: 12px;
}

/* ==========================================
   SCREENING (JOBS)
   ========================================== */
.screening-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.screening-item {
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border-left: 3px solid var(--color-purple);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.question-type {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  background: #E0E7FF;
  color: var(--color-purple);
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}

/* ==========================================
   BOTONES DE ACCIÓN (JOBS)
   ========================================== */
.action-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: flex-end;
  padding: 2rem 2.5rem;
  background: white;
  border-top: 2px solid #E2E8F0;
  margin-top: 0;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  border-radius: 0 0 8px 8px;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
  font-size: 1rem;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(124, 58, 237, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn-primary:disabled:hover,
.btn-secondary:disabled:hover {
  transform: none !important;
  box-shadow: none !important;
}

/* Animación de rotación para el ícono de carga */
@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.rotating {
  animation: rotate 1s linear infinite;
}

.btn-secondary {
  background: #F3F4F6;
  color: #4B5563;
  font-size: 1rem;
  border: 1px solid #D1D5DB;
}

.btn-secondary:hover {
  background: #E5E7EB;
  border-color: #9CA3AF;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-secondary:active {
  transform: translateY(0);
}

/* ==========================================
   JOB LISTING STYLE - FLUIDO Y SIN DIVISIONES
   ========================================== */

/* CONTENEDOR PRINCIPAL */
.job-listing-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  overflow: hidden;
  transition: box-shadow 0.3s ease;
}

.job-listing-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

/* ========== TÍTULO GENERAL ========== */
.job-summary-header {
  margin-bottom: 2rem;
  padding: 0;
}

.job-summary-title {
  font-size: 2rem;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.3px;
}

.job-summary-subtitle {
  font-size: 1rem;
  color: #64748B;
  margin: 0;
  font-weight: 500;
}

/* ========== HEADER - LAYOUT PROFESIONAL ========== */
.job-header {
  padding: 1.5rem 2.5rem 2.25rem 2.5rem;
  border-bottom: 2px solid #E9D5FF;
  background: linear-gradient(135deg, #FAFBFC 0%, #F8F6FB 100%);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* BADGES TOP ROW */
.badges-top-row {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: center;
}

.header-grid {
  display: grid;
  grid-template-columns: 160px 1fr auto;
  gap: 1.5rem 2rem;
  align-items: flex-start;
}

/* COLUMNA 1: LOGO GRANDE */
.logo-column {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 2.2rem;
}

.company-logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.company-logo {
  width: 160px;
  height: 160px;
  border-radius: 10px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E5E7EB;
  overflow: hidden;
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 11px;
  padding: 0.5rem;
}

.company-logo-placeholder {
  width: 160px;
  height: 160px;
  border-radius: 10px;
  background: #F9FAFB;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #D1D5DB;
  border: 1px solid #E5E7EB;
}

/* COLUMNA 2: INFORMACIÓN */
.info-column {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

/* TÍTULO DEL PUESTO */
.job-title-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.75rem;
}

.job-title-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #7C3AED;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin: 0;
}

.job-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
  line-height: 1.3;
  letter-spacing: -0.5px;
}

/* Empresa destacada */
.company-name-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  margin-bottom: 0.75rem;
  border-bottom: 1px solid #E5E7EB;
}

.company-icon {
  color: #7C3AED;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.company-name-text {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  line-height: 1.4;
}

/* GRID DE INFORMACIÓN COMPACTO - Layout 3 columnas */
.info-grid-compact {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem 1rem;
}

.info-item-compact {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 6px;
  background: #F9FAFB;
  transition: all 0.2s ease;
}

.info-item-compact:hover {
  background: #F3F4F6;
  transform: translateY(-1px);
}

.info-icon {
  color: #7C3AED;
  font-size: 0.95rem;
  margin-top: 0.15rem;
  flex-shrink: 0;
}

.info-text {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  min-width: 0;
}

.info-label-compact {
  font-size: 0.7rem;
  font-weight: 700;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  line-height: 1;
}

.info-value-compact {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1F2937;
  line-height: 1.35;
  word-break: break-word;
}

.info-value-compact.expired-text {
  color: #DC2626;
  font-weight: 700;
}

/* GRID DE INFORMACIÓN ANTIGUO - Mantener para compatibilidad */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 0.5rem;
}

.info-column-left,
.info-column-right {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 0;
  transition: none;
  box-shadow: none;
}

.info-item:hover {
  border-color: transparent;
  box-shadow: none;
  background: transparent;
}

.email-item {
  margin-top: 0.5rem;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  flex: 1;
}

.info-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 0.7px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-label :deep(.va-icon) {
  color: #7C3AED;
  opacity: 1;
  font-size: 0.85rem;
}

.info-value {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1E293B;
  line-height: 1.4;
}

.info-value.expired-text {
  color: #DC2626;
  font-weight: 800;
}

/* COLUMNA 3: METADATA */
.metadata-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: flex-end;
  justify-content: flex-start;
}

.metadata-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-end;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 0;
}


.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.4rem 0.9rem;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  border: none;
  transition: all 0.2s ease;
  min-width: 100px;
  text-align: center;
}

.badge-plan {
  background: linear-gradient(135deg, #F5F0FF 0%, #EDE9FE 100%);
  color: #7C3AED;
  border: 2px solid rgba(124, 58, 237, 0.3);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.15);
}

.badge-plan.plan-estandar {
  background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
  color: #16A34A;
  border: 2px solid rgba(22, 163, 74, 0.3);
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.15);
}

.badge-plan.plan-purpura {
  background: linear-gradient(135deg, #F5F0FF 0%, #EDE9FE 100%);
  color: #7C3AED;
  border: 2px solid rgba(124, 58, 237, 0.3);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.15);
}

.badge-plan.plan-impulso {
  background: linear-gradient(135deg, #FEF3C7 0%, #FEE08F 100%);
  color: #D97706;
  border: 2px solid rgba(217, 119, 6, 0.3);
  box-shadow: 0 2px 8px rgba(217, 119, 6, 0.15);
}

.badge-type {
  background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
  color: #475569;
  border: 2px solid #D1D5DB;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.badge-location {
  background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
  color: #0369A1;
  border: 2px solid rgba(3, 105, 161, 0.3);
  box-shadow: 0 2px 8px rgba(3, 105, 161, 0.15);
}

.badge-basic {
  background: linear-gradient(135deg, #F0F4F8 0%, #E2E8F0 100%);
  color: #475569;
  border: 2px solid #CBD5E1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.badge-featured {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  color: white;
  border: 2px solid rgba(124, 58, 237, 0.7);
  font-weight: 800;
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.4);
}

.badge-sponsored {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
  border: 2px solid rgba(16, 185, 129, 0.7);
  font-weight: 800;
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}

.badge-urgent {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  color: white;
  border: 2px solid rgba(220, 38, 38, 0.7);
  font-weight: 800;
  box-shadow: 0 6px 16px rgba(220, 38, 38, 0.4);
}

.badge-icon {
  margin-right: 0.35rem;
  font-size: 0.95rem;
  font-weight: 700;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.95rem;
  color: #475569;
  font-weight: 600;
}

.meta-item :deep(.va-icon) {
  color: #7C3AED;
  font-size: 1.1rem;
}

/* ========== CONTENIDO PRINCIPAL ========== */
.job-content {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.content-block {
  padding-bottom: 2.5rem;
  margin-bottom: 0;
  border-bottom: 1px solid #E2E8F0;
}

.content-block:last-child {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
}

/* TÍTULO DE SECCIÓN */
.block-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 1.1rem;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 1.25rem 0;
  letter-spacing: -0.3px;
}

.block-title :deep(.va-icon) {
  color: #7C3AED;
  font-size: 1.2rem;
}

/* TEXTO DE BLOQUES */
.block-text {
  font-size: 0.95rem;
  line-height: 1.8;
  color: #475569;
  margin: 0 0 1rem 0;
}

/* ===== SECCIÓN REQUISITOS ===== */
.requirements-list {
  list-style: none;
  padding: 0;
  margin: 1.25rem 0 0 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.requirement-item {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: #F9FAFB;
  border-left: 3px solid #7C3AED;
  border-radius: 0 8px 8px 0;
  font-size: 0.95rem;
  color: #334155;
  line-height: 1.6;
  transition: all 0.2s ease;
}

.requirement-item:hover {
  background: #F3F4F6;
  border-left-color: #6D28D9;
}

.requirement-icon {
  color: #7C3AED;
  font-size: 1.3rem;
  flex-shrink: 0;
  margin-right: 0.5rem;
}

.requirement-item strong {
  color: #0F172A;
  font-weight: 700;
  margin-right: 0.5rem;
}

.requirements-list .requirement-item div {
  flex: 1;
}

.salary-container {
  margin-top: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #F5F0FF 0%, #FAF5FF 100%);
  border-radius: 12px;
  border: 2px solid rgba(124, 58, 237, 0.15);
  box-shadow: 0 2px 12px rgba(124, 58, 237, 0.08);
}

.salary-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #7C3AED;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin: 0;
}

.salary-amount {
  font-size: 1.75rem;
  font-weight: 800;
  color: #7C3AED;
  margin: 0;
  letter-spacing: -0.3px;
  padding: 0;
  background: transparent;
  border-radius: 0;
  border: none;
  display: inline;
  min-width: fit-content;
}

/* ===== SECCIÓN PAGO Y COMPROBANTE (ACORDEÓN) ===== */
.payment-section {
  background: transparent;
}

.payment-accordion {
  border: 1px solid #E9D5FF;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(135deg, #FAFBFC 0%, #F8F6FB 100%);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.05);
}

/* Acordeón siempre abierto */
.payment-accordion.always-open .accordion-content {
  display: block !important;
}

.accordion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
  border-bottom: 1px solid #E2E8F0;
}

/* Header estático (sin hover, sin cursor) */
.accordion-header.static-header {
  cursor: default;
  background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
}

.accordion-header.static-header:hover {
  background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
}

.accordion-header:hover {
  background: #F9FAFB;
}

.accordion-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  color: #1F2937;
  font-size: 1rem;
}

.accordion-title :deep(.va-icon) {
  color: #7C3AED;
}

.accordion-hint {
  font-size: 0.75rem;
  font-weight: 500;
  color: #9CA3AF;
  margin-left: auto;
  white-space: nowrap;
}

.accordion-icon {
  color: #9CA3AF;
  transition: transform 0.3s ease;
}

.accordion-content {
  padding: 1.5rem;
}

/* Resumen compacto */
.payment-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #E2E8F0;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
}

.summary-label {
  font-weight: 700;
  color: #6B7280;
  min-width: 50px;
}

.summary-value {
  color: #1F2937;
  font-weight: 600;
}

.summary-value.bold {
  color: #7C3AED;
  font-size: 1.1rem;
}

.summary-ref {
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  color: #7C3AED;
  background: #F3F4F6;
  padding: 0.35rem 0.6rem;
  border-radius: 4px;
  font-weight: 700;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.copy-btn-small {
  background: #7C3AED;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.35rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.copy-btn-small:hover {
  background: #6D28D9;
  transform: scale(1.05);
}

.payment-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.payment-qr-column {
  display: flex;
  justify-content: center;
}

.qr-card-compact {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.qr-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.qr-image-container {
  display: flex;
  justify-content: center;
  padding: 0.75rem;
  background: #F9FAFB;
  border-radius: 10px;
  border: 1px solid #E2E8F0;
}

.qr-image {
  width: 160px;
  height: 160px;
  object-fit: contain;
  border-radius: 6px;
}

/* Proof of Payment Card */
.payment-proof-column {
  display: flex;
  flex-direction: column;
}

.proof-card-compact {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.proof-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.hidden-input {
  display: none;
}

.proof-upload-zone-compact {
  margin: 0;
}

.upload-area-compact {
  border: 2px dashed #E5E7EB;
  border-radius: 8px;
  padding: 1.25rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #F9FAFB;
}

.upload-area-compact:hover {
  border-color: #7C3AED;
  background: #F5F3FF;
  border-style: solid;
}

.upload-area-compact :deep(.va-icon) {
  color: #7C3AED;
  margin-bottom: 0.5rem;
}

.upload-text-compact {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1F2937;
  margin: 0.5rem 0 0.25rem 0;
}

.upload-hint-compact {
  font-size: 0.75rem;
  color: #9CA3AF;
  display: block;
}

.proof-preview-compact {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  max-height: 150px;
}

.preview-image-compact {
  width: 100%;
  height: 100%;
  max-height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.remove-btn-compact {
  position: absolute;
  top: 6px;
  right: 6px;
  background: rgba(220, 38, 38, 0.9);
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.remove-btn-compact:hover {
  background: rgba(220, 38, 38, 1);
  transform: scale(1.1);
}

.proof-status-compact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #F0FDF4;
  border: 1px solid #86EFAC;
  border-radius: 6px;
  color: #16A34A;
  font-weight: 600;
  font-size: 0.8rem;
}

.proof-required-compact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #FEF3C7;
  border: 1px solid #FCD34D;
  border-radius: 6px;
  color: #92400E;
  font-weight: 600;
  font-size: 0.8rem;
}

.payment-notice-compact {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: #EEF2FF;
  border-radius: 8px;
  border-left: 3px solid #7C3AED;
  color: #3730A3;
  font-size: 0.85rem;
  line-height: 1.5;
  align-items: flex-start;
}

.payment-notice-compact :deep(.va-icon) {
  flex-shrink: 0;
  margin-top: 0.15rem;
  color: #7C3AED;
}

.payment-support-compact {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #F0F9FF;
  border-radius: 8px;
  border: 1px solid #BFE7FF;
  margin-top: 1rem;
}

.support-icon {
  flex-shrink: 0;
  display: flex;
  align-items: flex-start;
  padding-top: 0.15rem;
}

.support-icon :deep(.va-icon) {
  color: #0369A1;
  font-size: 1rem;
}

.support-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.support-title {
  margin: 0;
  font-weight: 700;
  color: #0C4A6E;
  font-size: 0.9rem;
}

.support-text {
  margin: 0;
  color: #164E63;
  font-size: 0.85rem;
  line-height: 1.6;
}

.support-link {
  color: #0369A1;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.support-link:hover {
  color: #0C4A6E;
  text-decoration: underline;
}

/* ===== INFORMACIÓN ADICIONAL (Sin divisiones) ===== */
.info-additional {
  margin-top: 2rem;
  padding: 1.75rem;
  background: linear-gradient(135deg, #F8FAFC 0%, #FFFBFE 100%);
  border: 2px solid rgba(124, 58, 237, 0.1);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.05);
}

.additional-title {
  margin: 0 0 1.25rem 0;
  font-size: 0.9rem;
  font-weight: 800;
  color: #7C3AED;
  text-transform: uppercase;
  letter-spacing: 0.7px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.additional-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.75rem;
  margin-bottom: 1rem;
}

.additional-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #E2E8F0;
  transition: all 0.2s ease;
}

.additional-item:hover {
  border-color: #7C3AED;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.1);
}

.additional-label {
  font-size: 0.7rem;
  font-weight: 800;
  color: #7C3AED;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.additional-value {
  font-size: 1rem;
  color: #1E293B;
  font-weight: 700;
}

.additional-external {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #E2E8F0;
}

.additional-link {
  color: #7C3AED;
  text-decoration: none;
  font-weight: 600;
  word-break: break-all;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.95rem;
}

.additional-link:hover {
  color: #6D28D9;
  text-decoration: underline;
}

.additional-link :deep(.va-icon) {
  font-size: 0.8rem;
}

/* ===== SECCIÓN INFORMACIÓN TÉCNICA ===== */
.info-technical {
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  padding: 2rem;
  margin-left: -2.5rem;
  margin-right: -2.5rem;
  margin-bottom: -2.5rem;
  margin-top: 0;
  border-top: 2px solid #CBD5E1;
  border-bottom: none;
  border-radius: 0 0 12px 12px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2.5rem;
  margin-bottom: 2rem;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.info-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 0.95rem;
  color: #334155;
  font-weight: 600;
}

.info-external {
  padding-top: 2rem;
  border-top: 1px solid #CBD5E1;
}

.info-external p {
  margin: 0 0 0.5rem 0;
}

/* ========== LINKS ========== */
.info-link {
  color: #7C3AED;
  text-decoration: none;
  font-weight: 600;
  word-break: break-all;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.info-link:hover {
  color: #6D28D9;
  text-decoration: underline;
}

.external-link {
  font-size: 0.9rem;
}

.external-link :deep(.va-icon) {
  font-size: 0.8rem;
}

/* ===== ACCORDION TRANSITION ANIMATION ===== */
.slide-accordion-enter-active {
  transition: all 0.3s ease;
}

.slide-accordion-leave-active {
  transition: all 0.3s ease;
}

.slide-accordion-enter-from {
  max-height: 0;
  opacity: 0;
}

.slide-accordion-leave-to {
  max-height: 0;
  opacity: 0;
}

.slide-accordion-enter-to,
.slide-accordion-leave-from {
  max-height: 500px;
  opacity: 1;
}

/* ==========================================
   RESPONSIVE DESIGN
   ========================================== */

/* TABLET: 768px y menor */
@media (max-width: 768px) {
  /* GENERIC SUMMARY STYLES */
  .summary-header {
    flex-direction: column;
    text-align: center;
  }

  .summary-title {
    font-size: 1.5rem;
  }

  .info-row {
    flex-direction: column;
    gap: 0.25rem;
  }

  .info-row .label {
    min-width: auto;
  }

  .images-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }

  .menu-items-grid {
    grid-template-columns: 1fr;
  }

  .map-preview {
    height: 250px;
  }

  /* JOB LISTING RESPONSIVE */
  .job-listing-card {
    border-radius: 8px;
    margin-top: 1.5rem;
  }

  .job-header {
    padding: 1.5rem;
    background: white;
    gap: 1rem;
  }

  .header-grid {
    grid-template-columns: 1fr;
    gap: 1rem 0;
  }

  .logo-column {
    padding-top: 0;
    justify-content: flex-start;
  }

  .company-logo-container {
    justify-content: flex-start;
  }

  .company-logo {
    width: 120px;
    height: 120px;
  }

  .company-logo-placeholder {
    width: 120px;
    height: 120px;
    font-size: 3rem;
  }

  .company-name {
    font-size: 1.2rem;
  }

  .job-title {
    font-size: 1.3rem;
    line-height: 1.3;
    margin-top: 0.5rem;
  }

  .job-title-label {
    font-size: 0.75rem;
    font-weight: 600;
  }

  .info-column {
    gap: 0.5rem;
  }

  .metadata-column {
    gap: 0.5rem;
    align-items: center;
    justify-content: center;
    flex-direction: row;
    flex-wrap: wrap;
  }

  .metadata-container {
    gap: 0.5rem;
    flex-direction: row;
    justify-content: center;
  }

  .badges-top-row {
    gap: 0.4rem;
  }

  .badge,
  .badge-basic,
  .badge-featured,
  .badge-sponsored,
  .badge-urgent {
    padding: 0.25rem 0.5rem !important;
    font-size: 0.6rem !important;
    min-width: auto !important;
    gap: 0.2rem !important;
  }

  .job-content {
    padding: 2rem;
  }

  .content-block {
    padding-bottom: 2rem;
  }

  .requirements-list {
    gap: 0.75rem;
  }

  .requirement-item {
    padding: 1rem;
    gap: 0.75rem;
  }

  .salary-amount {
    font-size: 1.6rem;
    padding: 1.25rem;
  }

  .info-grid {
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }

  .info-column-left,
  .info-column-right {
    gap: 0.75rem;
  }

  .payment-summary {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .summary-item {
    flex-wrap: wrap;
  }

  .summary-ref {
    font-size: 0.7rem;
  }

  .accordion-hint {
    display: none;
  }

  .payment-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .payment-qr-column {
    justify-content: flex-start;
  }

  .qr-card {
    max-width: 100%;
  }

  .payment-support-compact {
    flex-direction: column;
    gap: 0.5rem;
  }

  .support-text {
    font-size: 0.75rem;
  }

  .additional-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .info-technical {
    margin-left: -1.25rem;
    margin-right: -1.25rem;
    margin-bottom: -1.25rem;
    padding: 1.25rem;
  }

  .block-title {
    font-size: 1rem;
  }

  .block-text {
    font-size: 0.9rem;
    line-height: 1.7;
  }
}

/* MOBILE: 480px y menor */
@media (max-width: 480px) {
  /* JOB LISTING MOBILE */
  .job-listing-card {
    border-radius: 6px;
    margin-top: 0.75rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    padding: 0;
  }

  .job-header {
    padding: 1.25rem;
    gap: 0.75rem;
    border-radius: 6px;
    border-bottom: 1px solid #E5E7EB;
  }

  .header-grid {
    grid-template-columns: 140px 1fr;
    gap: 1rem;
    align-items: flex-start;
  }

  .logo-column {
    padding-top: 0;
    margin-bottom: 0;
    order: 1;
  }

  .info-column {
    order: 2;
    gap: 0.5rem;
  }

  .metadata-column {
    order: 3;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.5rem;
    padding-top: 0.75rem;
    border-top: 1px solid #E5E7EB;
  }

  .metadata-container {
    flex-direction: row;
    gap: 1rem;
    align-items: center;
  }

  .company-logo-container {
    width: auto;
    justify-content: flex-start;
    margin-bottom: 0;
  }

  .company-logo {
    width: 140px;
    height: 140px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.12);
    border: 2px solid #E5E7EB;
    flex-shrink: 0;
  }

  .company-logo-placeholder {
    width: 140px;
    height: 140px;
    font-size: 3.5rem;
    border-radius: 12px;
    border: 2px solid #E5E7EB;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F9FAFB;
  }

  .job-title-wrapper {
    text-align: left;
    margin-bottom: 0.5rem;
  }

  .job-title-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #7C3AED;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .job-title {
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.25;
    margin: 0.25rem 0 0 0;
    color: #1F2937;
  }

  .company-name-section {
    padding: 0.5rem 0;
    margin-bottom: 0.75rem;
    justify-content: flex-start;
    border-bottom: 1px solid #E5E7EB;
  }

  .company-name-text {
    font-size: 1rem;
    text-align: left;
  }

  .info-grid-compact {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .info-item-compact {
    padding: 0.5rem 0.6rem;
  }

  .info-label-compact {
    font-size: 0.65rem;
  }

  .info-value-compact {
    font-size: 0.875rem;
  }

  .badges-top-row {
    gap: 0.25rem !important;
    justify-content: center;
    flex-wrap: wrap;
  }

  .badges-top-row .badge,
  .badge,
  .badge-basic,
  .badge-featured,
  .badge-sponsored,
  .badge-urgent {
    padding: 0.15rem 0.35rem !important;
    font-size: 0.5rem !important;
    font-weight: 600 !important;
    border-radius: 3px !important;
    line-height: 1 !important;
    letter-spacing: 0.01em !important;
    white-space: nowrap !important;
    min-width: auto !important;
    max-width: none !important;
    gap: 0.2rem !important;
    text-transform: uppercase !important;
    border-width: 1px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
  }

  .badges-top-row .badge-icon,
  .badge-icon,
  .badge .va-icon,
  .badge :deep(.va-icon) {
    font-size: 0.6rem !important;
    width: 0.6rem !important;
    height: 0.6rem !important;
    margin-right: 0.15rem !important;
  }

  /* Forzar tamaño de ícono dentro de badge */
  .badges-top-row :deep(.va-icon),
  .badge :deep(.va-icon__content) {
    font-size: 0.6rem !important;
    width: 0.6rem !important;
    height: 0.6rem !important;
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    margin-top: 0;
  }

  .info-column-left,
  .info-column-right {
    gap: 0.75rem;
  }

  .info-item {
    padding: 0;
    background: transparent;
  }

  .info-label {
    font-size: 0.6rem;
  }

  .info-value {
    font-size: 0.85rem;
  }

  .metadata-column {
    gap: 0.5rem;
    align-items: flex-start;
  }

  .badges-top-row {
    gap: 0.3rem;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .header-badges {
    gap: 0.3rem;
    flex-wrap: wrap;
  }

  .badge {
    padding: 0.2rem 0.4rem;
    font-size: 0.5rem;
    font-weight: 600;
    border-radius: 2px;
    line-height: 1;
    white-space: nowrap;
    min-width: auto;
    flex: 0 1 auto;
  }

  .meta-item {
    font-size: 0.8rem;
    padding: 0;
    background: transparent;
    border-radius: 0;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    white-space: nowrap;
    color: #64748B;
  }

  .meta-item span {
    font-weight: 500;
    color: #1E293B;
  }

  .job-content {
    padding: 1.25rem;
  }

  .content-block {
    padding-bottom: 1rem;
  }

  .content-block:not(:last-child) {
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 1rem;
  }

  .block-title {
    font-size: 0.95rem;
    margin: 0 0 0.75rem 0;
    font-weight: 700;
  }

  .block-text {
    font-size: 0.85rem;
    line-height: 1.6;
  }

  .requirements-list {
    margin: 0.75rem 0 0 0;
    gap: 0.5rem;
  }

  .requirement-item {
    padding: 0.75rem;
    gap: 0.5rem;
    font-size: 0.85rem;
  }

  .requirement-icon {
    font-size: 1.1rem;
    margin-right: 0.3rem;
  }

  .salary-label {
    font-size: 0.75rem;
  }

  .salary-amount {
    font-size: 1.25rem;
    padding: 0.85rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .info-group {
    gap: 0.75rem;
  }

  .info-item {
    gap: 0.2rem;
  }

  .info-label {
    font-size: 0.75rem;
    color: #64748B;
  }

  .info-value {
    font-size: 0.9rem;
  }

  .info-link {
    font-size: 0.9rem;
  }

  .info-technical {
    margin-left: -1.5rem;
    margin-right: -1.5rem;
    margin-bottom: -1.5rem;
    padding: 1.5rem;
    border-radius: 0 0 8px 8px;
  }

  .info-external {
    padding-top: 1.5rem;
  }

  .external-link {
    font-size: 0.85rem;
    word-break: break-word;
  }
}

/* ==========================================
   SECCIÓN DE FACTURACIÓN
   ========================================== */
.billing-section {
  margin-top: 2rem;
}

.billing-accordion {
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  overflow: hidden;
  background: white;
}

.billing-accordion .accordion-header {
  padding: 1.25rem;
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  border-bottom: 1px solid #E2E8F0;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.billing-accordion .accordion-header:hover {
  background: linear-gradient(135deg, #F1F5F9 0%, #E8EEF5 100%);
}

.billing-accordion .accordion-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  color: #1F2937;
  margin: 0;
}

.billing-accordion .accordion-hint {
  font-size: 0.85rem;
  color: #999;
  margin-left: auto;
  margin-right: 0.5rem;
}

.billing-accordion .accordion-icon {
  transition: transform 0.3s ease;
}

.billing-accordion .accordion-content {
  padding: 1.5rem;
  background: white;
}

/* Separador de facturación */
.billing-separator {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0 1.5rem 0;
  padding: 0 0.5rem;
}

.separator-line {
  flex: 1;
  height: 2px;
  background: linear-gradient(to right, transparent, #E9D5FF, transparent);
}

.separator-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  font-size: 1rem;
  color: #7C3AED;
  white-space: nowrap;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
  border-radius: 20px;
  border: 2px solid #DDD6FE;
}

.separator-text :deep(.va-icon) {
  color: #7C3AED;
  font-size: 1.1rem;
}

/* Checkbox "Soy contribuyente" */
.contributor-checkbox-container {
  margin: 1.5rem 0;
  padding: 1.25rem;
  background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
  border-radius: 12px;
  border: 2px solid #E5E7EB;
}

.contributor-checkbox {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  user-select: none;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkbox-custom {
  position: relative;
  width: 24px;
  height: 24px;
  border: 2px solid #7C3AED;
  border-radius: 6px;
  background: white;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.checkbox-input:checked + .checkbox-custom {
  background: #7C3AED;
  border-color: #7C3AED;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  font-size: 16px;
}

.checkbox-custom:hover {
  border-color: #6D28D9;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  color: #374151;
}

.checkbox-label :deep(.va-icon) {
  color: #7C3AED;
  font-size: 1.2rem;
}

.checkbox-hint {
  margin: 0.5rem 0 0 2.5rem;
  font-size: 0.8rem;
  color: #9CA3AF;
  font-weight: 400;
  line-height: 1.4;
}

.billing-form-group {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem 1.5rem;
  margin-bottom: 1rem;
}

.billing-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.billing-field.full-width {
  grid-column: 1 / -1;
}

/* Responsive: 1 columna en móvil */
@media (max-width: 768px) {
  .billing-form-group {
    grid-template-columns: 1fr;
  }

  .billing-field.full-width {
    grid-column: 1;
  }
}

.billing-label {
  font-weight: 600;
  color: var(--color-purple-dark);
  font-size: 0.95rem;
}

.billing-label.required-field::after {
  content: ' *';
  color: #EF4444;
  font-weight: 700;
}

.billing-input {
  padding: 0.75rem 1rem;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: white;
  color: #333;
}

.billing-input:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.billing-input::placeholder {
  color: #999;
}

/* Sección de método de envío */
.delivery-method-section {
  padding: 1.25rem;
  background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
  border-radius: 12px;
  border: 2px solid #C7D2FE;
  margin: 1rem 0;
}

.delivery-method-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 700;
  color: #1E40AF;
  margin-bottom: 0.5rem;
}

.delivery-method-title :deep(.va-icon) {
  color: #4F46E5;
  font-size: 1.2rem;
}

.delivery-method-hint {
  font-size: 0.85rem;
  color: #6366F1;
  margin: 0 0 1rem 0;
  font-weight: 500;
}

.delivery-checkboxes {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

@media (max-width: 480px) {
  .delivery-checkboxes {
    grid-template-columns: 1fr;
  }
}

.delivery-checkbox {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: white;
  border: 2px solid #C7D2FE;
  border-radius: 10px;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s ease;
}

.delivery-checkbox:hover {
  border-color: #818CF8;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.15);
  transform: translateY(-2px);
}

.delivery-checkbox .checkbox-input:checked + .checkbox-custom {
  background: #4F46E5;
  border-color: #4F46E5;
}

.delivery-checkbox .checkbox-custom {
  border-color: #818CF8;
}

.delivery-checkbox .checkbox-custom:hover {
  border-color: #4F46E5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.delivery-checkbox .checkbox-label {
  color: #1E3A8A;
  font-weight: 600;
  font-size: 0.95rem;
}

.delivery-checkbox .checkbox-label :deep(.va-icon) {
  color: #4F46E5;
  font-size: 1.1rem;
}

.billing-alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1rem;
  background: linear-gradient(135deg, #F3E8FF 0%, #EDE9FE 100%);
  border-radius: 8px;
  border: 2px solid #E9D5FF;
  border-left: 4px solid #7C3AED;
  margin-top: 1.25rem;
}

.billing-alert :deep(.va-icon) {
  font-size: 1.1rem;
  flex-shrink: 0;
  color: #7C3AED;
}

.alert-content {
  flex: 1;
  font-size: 0.8rem;
  color: #5B21B6;
  line-height: 1.5;
  font-weight: 400;
}

.alert-content strong {
  color: #7C3AED;
  font-weight: 600;
}
/* Estilos para renderizar HTML de CKEditor */
.job-description-html :deep(p) {
  margin-bottom: 0.75rem;
}

.job-description-html :deep(strong) {
  font-weight: 700;
  color: #1E293B;
}

.job-description-html :deep(em) {
  font-style: italic;
}

.job-description-html :deep(s) {
  text-decoration: line-through;
}

.job-description-html :deep(u) {
  text-decoration: underline;
}

.job-description-html :deep(ul),
.job-description-html :deep(ol) {
  margin-left: 1.5rem;
  margin-bottom: 0.75rem;
}

.job-description-html :deep(li) {
  margin-bottom: 0.5rem;
}

.job-description-html :deep(blockquote) {
  border-left: 4px solid #7C3AED;
  padding-left: 1rem;
  margin: 1rem 0;
  font-style: italic;
  color: #64748B;
  background: #F5F3FF;
  padding: 0.75rem 1rem;
  border-radius: 4px;
}

.job-description-html :deep(a) {
  color: #7C3AED;
  text-decoration: underline;
}

/* Neutralizar headers - forzar estilo de párrafo normal (como en Quill editor) */
.job-description-html :deep(h1),
.job-description-html :deep(h2),
.job-description-html :deep(h3),
.job-description-html :deep(h4),
.job-description-html :deep(h5),
.job-description-html :deep(h6) {
  font-size: 1rem !important;
  font-weight: normal !important;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.5 !important;
  color: #475569 !important;
  margin-bottom: 0.75rem !important;
}

/* ===== PREGUNTAS DE FILTRADO ===== */
.screening-block {
  background: #FEFCFF;
}

.screening-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.screening-item {
  display: flex;
  gap: 0.6rem;
  padding: 0.65rem 0.85rem;
  background: white;
  border-radius: 6px;
  border: 1px solid #F3E8FF;
  transition: all 0.15s ease;
  align-items: flex-start;
}

.screening-item:hover {
  border-color: #E9D5FF;
  background: #FEFCFF;
}

.question-number {
  font-weight: 600;
  color: #7C3AED;
  font-size: 0.875rem;
  min-width: 1.5rem;
  line-height: 1.4;
  flex-shrink: 0;
}

.question-content {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.4rem;
}

.question-text {
  color: #1E293B;
  font-size: 0.9rem;
  line-height: 1.4;
  font-weight: 500;
}

.question-type {
  color: #94a3b8;
  font-size: 0.8rem;
  font-style: italic;
  white-space: nowrap;
}

.question-required {
  color: #7C3AED;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

/* ===== INFORMACIÓN DE APLICACIÓN EXTERNA ===== */
.application-external-block {
  background: linear-gradient(135deg, #FEFCFF 0%, #F9FAFB 100%);
  border: 1px solid #E9D5FF;
}

.external-application-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item-external {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #F3E8FF;
  transition: all 0.2s ease;
}

.info-item-external:hover {
  border-color: #E9D5FF;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.08);
}

.info-label-external {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #7C3AED;
  font-size: 0.875rem;
}

.info-value-external {
  color: #1E293B;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-left: 1.75rem;
}

.info-value-external.url-link {
  color: #7C3AED;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  transition: all 0.2s ease;
  word-break: break-all;
}

.info-value-external.url-link:hover {
  color: #6D28D9;
  text-decoration: underline;
}

.info-value-external.instructions-text {
  margin: 0;
  padding: 0.75rem;
  background: #FEFCFF;
  border-radius: 6px;
  border-left: 3px solid #7C3AED;
  font-style: italic;
  color: #475569;
}

</style>