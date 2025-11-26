<!-- 
  ==========================================
  SUMMARYCARD.VUE - ACTUALIZADO
  ==========================================
  
  Resumen completo del anuncio antes de publicar.
  Incluye sección especial para mostrar los platos del menú (gastronomía).
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
          
          <!-- Campo SERVICES para profesionales -->
          <div v-if="formData.category === 'profesionales' && formData.services" class="info-row full-width">
            <span class="label">Descripción de servicios:</span>
            <p class="value description">{{ formData.services }}</p>
          </div>
          
          <!-- Campo DESCRIPTION para otros -->
          <div v-else-if="formData.description" class="info-row full-width">
            <span class="label">Descripción:</span>
            <p class="value description">{{ formData.description }}</p>
          </div>

          <!-- Campos específicos de GASTRONOMÍA -->
          <template v-if="formData.category === 'gastronomia'">
            <div class="info-row">
              <span class="label">Rango de precios:</span>
              <span class="value">{{ formData.priceRange || 'N/A' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Delivery:</span>
              <span class="value">{{ formData.deliveryAvailable ? '✅ Disponible' : '❌ No disponible' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Horarios:</span>
              <span class="value">{{ formData.schedule || 'N/A' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Capacidad:</span>
              <span class="value">{{ formData.capacity ? `${formData.capacity} personas` : 'N/A' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Estacionamiento:</span>
              <span class="value">{{ formData.parking ? '✅ Disponible' : '❌ No disponible' }}</span>
            </div>
            <div v-if="formData.features && formData.features.length > 0" class="info-row full-width">
              <span class="label">Características:</span>
              <div class="features-list">
                <va-chip
                  v-for="feature in formData.features"
                  :key="feature"
                  size="small"
                  color="success"
                >
                  {{ feature }}
                </va-chip>
              </div>
            </div>
          </template>

          <!-- Campos específicos de PROFESIONALES -->
          <template v-if="formData.category === 'profesionales'">
            <div class="info-row">
              <span class="label">Título profesional:</span>
              <span class="value">{{ formData.professionalTitle || 'N/A' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Años de experiencia:</span>
              <span class="value">{{ formData.yearsExperience || 'N/A' }}</span>
            </div>
            <div v-if="formData.university" class="info-row">
              <span class="label">Universidad:</span>
              <span class="value">{{ formData.university }}</span>
            </div>
            <div v-if="formData.specialties && formData.specialties.length > 0" class="info-row full-width">
              <span class="label">Especialidades:</span>
              <div class="features-list">
                <va-chip
                  v-for="specialty in formData.specialties"
                  :key="specialty"
                  size="small"
                  color="primary"
                >
                  {{ specialty }}
                </va-chip>
              </div>
            </div>
            <div v-if="formData.successCases" class="info-row full-width">
              <span class="label">Casos de éxito / Logros:</span>
              <p class="value description">{{ formData.successCases }}</p>
            </div>
            <div v-if="formData.whyChooseMe" class="info-row full-width">
              <span class="label">¿Por qué elegirme?:</span>
              <p class="value description">{{ formData.whyChooseMe }}</p>
            </div>
            <div v-if="formData.languages && formData.languages.length > 0" class="info-row full-width">
              <span class="label">Idiomas:</span>
              <div class="features-list">
                <va-chip
                  v-for="language in formData.languages"
                  :key="language"
                  size="small"
                  color="success"
                >
                  {{ language }}
                </va-chip>
              </div>
            </div>
            <div class="info-row">
              <span class="label">Tarifa:</span>
              <span class="value">
                {{ formData.priceType === 'desde' && formData.price ? `Desde Bs. ${formData.price}` : 'A consultar' }}
              </span>
            </div>
            <div v-if="formData.schedule" class="info-row">
              <span class="label">Horario de atención:</span>
              <span class="value">{{ formData.schedule }}</span>
            </div>
          </template>

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

      <!-- GPS / UBICACIÓN (Solo profesionales y gastronomía, NO para jobs) -->
      <div v-if="type !== 'job' && ['profesionales', 'gastronomia'].includes(formData.category)" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="location_on" size="1.25rem" />
            Ubicación GPS
          </h3>
          <va-button
            v-if="editable"
            size="small"
            preset="plain"
            @click="$emit('edit-step', formData.category === 'profesionales' ? 2 : 4)"
          >
            Editar
          </va-button>
        </div>
        
        <div class="section-content">
          <div v-if="formData.coordinates" class="info-row">
            <span class="label">Coordenadas:</span>
            <span class="value">{{ formData.coordinates }}</span>
          </div>
          <div v-if="formData.gpsAddress" class="info-row full-width">
            <span class="label">Dirección GPS:</span>
            <span class="value">{{ formData.gpsAddress }}</span>
          </div>
          
          <!-- Mapa Preview -->
          <div v-if="formData.coordinates" class="map-preview-container">
            <div id="map-preview" class="map-preview"></div>
          </div>
          
          <p v-if="!formData.coordinates && !formData.gpsAddress" class="empty-message">
            <va-icon name="info" color="warning" />
            No se ha agregado ubicación GPS
          </p>
        </div>
      </div>

      <!-- SEO (Solo profesionales y gastronomía, NO para jobs) -->
      <div v-if="type !== 'job' && ['profesionales', 'gastronomia'].includes(formData.category) && formData.seoData" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="search" size="1.25rem" />
            SEO y Visibilidad
          </h3>
          <va-button
            v-if="editable"
            size="small"
            preset="plain"
            @click="$emit('edit-step', formData.category === 'profesionales' ? 3 : 5)"
          >
            Editar
          </va-button>
        </div>
        
        <div class="section-content">
          <div v-if="formData.seoData.title" class="info-row">
            <span class="label">Título SEO:</span>
            <span class="value">{{ formData.seoData.title }}</span>
          </div>
          <div v-if="formData.seoData.slug" class="info-row">
            <span class="label">URL:</span>
            <span class="value url">guiaspurpuras.com/{{ formData.seoData.slug }}</span>
          </div>
          <div v-if="formData.seoData.mainKeyword" class="info-row">
            <span class="label">Palabra clave:</span>
            <span class="value">{{ formData.seoData.mainKeyword }}</span>
          </div>
          <div v-if="formData.seoData.metaDescription" class="info-row full-width">
            <span class="label">Meta descripción:</span>
            <p class="value description">{{ formData.seoData.metaDescription }}</p>
          </div>
          <div v-if="formData.seoData.tags && formData.seoData.tags.length > 0" class="info-row full-width">
            <span class="label">Tags SEO:</span>
            <div class="features-list">
              <va-chip
                v-for="tag in formData.seoData.tags"
                :key="tag"
                size="small"
                color="purple"
              >
                {{ tag }}
              </va-chip>
            </div>
          </div>
          <div v-if="formData.seoData.locationKeywords" class="info-row">
            <span class="label">Keywords de ubicación:</span>
            <span class="value">{{ formData.seoData.locationKeywords }}</span>
          </div>
        </div>
      </div>

      <!-- 
        ==========================================
        MENÚ / PLATOS (SOLO GASTRONOMÍA)
        ==========================================
      -->
      <div v-if="formData.category === 'gastronomia'" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="restaurant_menu" size="1.25rem" />
            Menú / Platos
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
          <div v-if="formData.menuItems && formData.menuItems.length > 0">
            <p class="menu-count">
              <va-icon name="fastfood" color="purple" />
              <strong>{{ formData.menuItems.length }}</strong> 
              {{ formData.menuItems.length === 1 ? 'plato agregado' : 'platos agregados' }}
            </p>
            
            <!-- Grid de platos -->
            <div class="menu-items-grid">
              <div
                v-for="(item, index) in formData.menuItems"
                :key="index"
                class="menu-item-preview"
              >
                <!-- Imagen del plato -->
                <div class="menu-item-image">
                  <img 
                    v-if="item.image || item.imagePreview" 
                    :src="item.imagePreview || getImageUrl(item.image)" 
                    :alt="item.name"
                  />
                  <div v-else class="no-image">
                    <va-icon name="restaurant" size="2rem" color="#CCC" />
                  </div>
                  <div v-if="item.featured" class="featured-star">⭐</div>
                </div>

                <!-- Info del plato -->
                <div class="menu-item-info">
                  <h4 class="menu-item-name">{{ item.name }}</h4>
                  <p class="menu-item-price">Bs. {{ formatPrice(item.price) }}</p>
                  
                  <p v-if="item.description" class="menu-item-desc">
                    {{ item.description }}
                  </p>
                  
                  <div v-if="item.ingredients && item.ingredients.length > 0" class="menu-item-ingredients">
                    <va-icon name="eco" size="small" color="success" />
                    <span>{{ formatIngredients(item.ingredients) }}</span>
                  </div>

                  <div v-if="item.tags && item.tags.length > 0" class="menu-item-tags">
                    <va-chip
                      v-for="tag in item.tags"
                      :key="tag"
                      size="small"
                      color="purple"
                      outline
                    >
                      {{ tag }}
                    </va-chip>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <p v-else class="empty-message">
            <va-icon name="info" color="warning" />
            No se han agregado platos al menú
          </p>
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
          <div class="info-row full-width">
            <span class="label">Descripción:</span>
            <p class="value description">{{ jobData.description }}</p>
          </div>
        </div>
      </div>

      <!-- REQUISITOS Y COMPETENCIAS (ACORDEÓN 2) -->
      <div v-if="type === 'job' && jobData" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="assignment_ind" size="1.25rem" />
            Requisitos y Competencias
          </h3>
        </div>

        <div class="section-content">
          <div class="info-row full-width">
            <span class="label">Requisitos:</span>
            <p class="value description">{{ jobData.requirements }}</p>
          </div>
          <div v-if="jobData.responsibilities" class="info-row full-width">
            <span class="label">Responsabilidades:</span>
            <p class="value description">{{ jobData.responsibilities }}</p>
          </div>
          <div v-if="jobData.education" class="info-row">
            <span class="label">Formación:</span>
            <span class="value">{{ jobData.education }}</span>
          </div>
          <div v-if="jobData.experience" class="info-row">
            <span class="label">Experiencia:</span>
            <span class="value">{{ jobData.experience }}</span>
          </div>
          <div v-if="jobData.languages" class="info-row">
            <span class="label">Idiomas:</span>
            <span class="value">{{ jobData.languages }}</span>
          </div>
          <div v-if="jobData.technicalSkills" class="info-row full-width">
            <span class="label">Habilidades Técnicas:</span>
            <p class="value description">{{ jobData.technicalSkills }}</p>
          </div>
          <div v-if="jobData.softSkills" class="info-row full-width">
            <span class="label">Habilidades Blandas:</span>
            <p class="value description">{{ jobData.softSkills }}</p>
          </div>
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
            <span class="label">Fecha de Vencimiento:</span>
            <span class="value">{{ jobData.expiryDate }}</span>
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
              <template v-else>
                No mostrado
              </template>
            </span>
          </div>
          <div v-if="jobData.benefits" class="info-row full-width">
            <span class="label">Beneficios:</span>
            <p class="value description">{{ jobData.benefits }}</p>
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
            <span class="value url">{{ jobData.externalApplicationUrl }}</span>
          </div>
          <div v-if="jobData.screeningQuestions && jobData.screeningQuestions.length > 0" class="info-row full-width">
            <span class="label">Preguntas de Filtrado:</span>
            <div class="screening-list">
              <div v-for="(q, idx) in jobData.screeningQuestions" :key="idx" class="screening-item">
                <strong>{{ idx + 1 }}. {{ q.text }}</strong>
                <span class="question-type">({{ getQuestionTypeLabel(q.type) }})</span>
              </div>
            </div>
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
            @click="$emit('edit-step', formData.category === 'gastronomia' ? 5 : 4)"
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
            <div class="badges-top-row">
              <span class="badge badge-plan" :class="`plan-${jobData.selectedPlan}`">
                {{ getJobPlanName(jobData.selectedPlan).replace('Plan ', '') }}
              </span>
              <span v-for="planBadge in planBadges" :key="planBadge" class="badge" :class="`badge-${getBadgeClass(planBadge)}`">
                <va-icon v-if="getBadgeIcon(planBadge)" :name="getBadgeIcon(planBadge)" size="small" class="badge-icon" />
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
                    <va-icon name="business" size="4rem" />
                  </div>
                </div>
              </div>

              <!-- COLUMNA 2: INFORMACIÓN PRINCIPAL -->
              <div class="info-column">
                <!-- Título del Puesto (Grande) -->
                <div class="job-title-wrapper">
                  <span class="job-title-label">Oferta laboral:</span>
                  <h1 class="job-title">{{ jobData.title }}</h1>
                </div>

                <!-- Grid de Información: 2x2 -->
                <div class="info-grid">
                  <div class="info-item">
                    <div class="info-content">
                      <span class="info-label">
                        <va-icon name="business" size="small" />
                        Empresa:
                      </span>
                      <span class="info-value">
                        {{ jobData.companyAnonymous ? 'Empresa Confidencial' : jobData.companyName }}
                      </span>
                    </div>
                  </div>

                  <div class="info-item">
                    <div class="info-content">
                      <span class="info-label">
                        <va-icon name="work_history" size="small" />
                        Contrato:
                      </span>
                      <span class="info-value">{{ jobData.contractType }}</span>
                    </div>
                  </div>

                  <div class="info-item">
                    <div class="info-content">
                      <span class="info-label">
                        <va-icon name="location_on" size="small" />
                        Ubicación:
                      </span>
                      <span class="info-value">
                        {{ jobData.municipality ? `${jobData.city} - ${jobData.municipality}` : jobData.city }}
                      </span>
                    </div>
                  </div>

                  <div class="info-item">
                    <div class="info-content">
                      <span class="info-label">
                        <va-icon name="calendar_today" size="small" />
                        Vencimiento:
                      </span>
                      <span class="info-value" :class="{ 'expired-text': isExpired }">
                        {{ isExpired ? 'CONVOCATORIA CERRADA' : formatDate(jobData.expiryDate) }}
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
                Descripción del Puesto
              </h2>
              <p class="block-text">{{ jobData.description }}</p>
            </section>

            <!-- ===== REQUISITOS ===== -->
            <section class="content-block requirements-block">
              <h2 class="block-title">
                <va-icon name="checklist" size="small" />
                Requisitos
              </h2>
              <p v-if="jobData.requirements" class="block-text">{{ jobData.requirements }}</p>

              <!-- Detalles de Requisitos como viñetas -->
              <ul v-if="jobData.education || jobData.experience || jobData.languages || jobData.technicalSkills" class="requirements-list">
                <li v-if="jobData.education" class="requirement-item">
                  <va-icon name="school" class="requirement-icon" />
                  <div>
                    <strong>Formación:</strong> {{ jobData.education }}
                  </div>
                </li>
                <li v-if="jobData.experience" class="requirement-item">
                  <va-icon name="work_history" class="requirement-icon" />
                  <div>
                    <strong>Experiencia:</strong> {{ jobData.experience }}
                  </div>
                </li>
                <li v-if="jobData.languages" class="requirement-item">
                  <va-icon name="language" class="requirement-icon" />
                  <div>
                    <strong>Idiomas:</strong> {{ jobData.languages }}
                  </div>
                </li>
                <li v-if="jobData.technicalSkills" class="requirement-item">
                  <va-icon name="build" class="requirement-icon" />
                  <div>
                    <strong>Habilidades:</strong> {{ jobData.technicalSkills }}
                  </div>
                </li>
              </ul>
            </section>

            <!-- ===== BENEFICIOS ===== -->
            <section v-if="jobData.benefits" class="content-block benefits-block">
              <h2 class="block-title">
                <va-icon name="card_giftcard" size="small" />
                Beneficios
              </h2>
              <ul class="benefits-list">
                <li v-for="(benefit, idx) in jobData.benefits.split('\n').filter(b => b.trim())" :key="idx" class="benefit-item">
                  <va-icon name="check_circle" class="benefit-icon" />
                  {{ benefit.trim() }}
                </li>
              </ul>
            </section>

            <!-- ===== COMPENSACIÓN ===== -->
            <section class="content-block salary-block">
              <h2 class="block-title">
                <va-icon name="attach_money" size="small" />
                Compensación
              </h2>

              <!-- Salario Destacado -->
              <div class="salary-container">
                <p class="salary-label">Rango Salarial:</p>
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
                  <template v-else>
                    No especificado
                  </template>
                </p>
              </div>
              <!-- ===== INFORMACIÓN ADICIONAL (Sin fondo diferenciado) ===== -->
              <div class="info-additional">
                <h3 class="additional-title">Más Información</h3>

                <div class="additional-grid">
                  <div class="additional-item">
                    <span class="additional-label">Categoría:</span>
                    <span class="additional-value">{{ jobData.jobCategory }}</span>
                  </div>
                  <div class="additional-item">
                    <span class="additional-label">Tipo de Aplicación:</span>
                    <span class="additional-value">
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
                  <div v-if="jobData.vacancies" class="additional-item">
                    <span class="additional-label">Vacantes:</span>
                    <span class="additional-value">{{ jobData.vacancies }}</span>
                  </div>
                  <div v-if="jobData.email" class="additional-item">
                    <span class="additional-label">Email de Contacto:</span>
                    <a :href="`mailto:${jobData.email}`" class="additional-link">{{ jobData.email }}</a>
                  </div>
                </div>

                <!-- URL de Aplicación Externa (si aplica) -->
                <div v-if="['external', 'both'].includes(jobData.applicationType)" class="additional-external">
                  <span class="additional-label">URL de Aplicación:</span>
                  <a :href="jobData.externalApplicationUrl" target="_blank" class="additional-link">
                    {{ jobData.externalApplicationUrl }}
                    <va-icon name="open_in_new" size="small" />
                  </a>
                </div>
              </div>
            </section>

            <!-- ===== SECCIÓN PAGO Y COMPROBANTE (ACORDEÓN) ===== -->
            <section class="content-block payment-section">
              <div class="payment-accordion">
                <!-- Header del Acordeón -->
                <div @click="togglePaymentAccordion" class="accordion-header">
                  <div class="accordion-title">
                    <va-icon name="payment" size="small" />
                    <span>Información y método de pago de su anuncio</span>
                    <span class="accordion-hint">• Haz clic para desplegar</span>
                  </div>
                  <va-icon
                    :name="paymentAccordionOpen ? 'expand_less' : 'expand_more'"
                    size="small"
                    class="accordion-icon"
                  />
                </div>

                <!-- Contenido del Acordeón -->
                <transition name="slide-accordion">
                  <div v-if="paymentAccordionOpen" class="accordion-content">
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
                  </div>
                </transition>
              </div>
            </section>

            <!-- ===== INFORMACIÓN DE FACTURACIÓN (ACORDEÓN) ===== -->
            <section class="content-block billing-section">
              <div class="billing-accordion">
                <!-- Header del Acordeón -->
                <div @click="toggleBillingAccordion" class="accordion-header">
                  <div class="accordion-title">
                    <va-icon name="receipt" size="small" />
                    <span>Información de Facturación (Opcional)</span>
                    <span class="accordion-hint">• Haz clic para desplegar</span>
                  </div>
                  <va-icon
                    :name="billingAccordionOpen ? 'expand_less' : 'expand_more'"
                    size="small"
                    class="accordion-icon"
                  />
                </div>

                <!-- Contenido del Acordeón -->
                <transition name="slide-accordion">
                  <div v-if="billingAccordionOpen" class="accordion-content">
                    <div class="billing-form-group">
                      <!-- Razón Social -->
                      <div class="billing-field">
                        <label class="billing-label">Razón Social</label>
                        <input
                          v-model="billingData.businessName"
                          type="text"
                          placeholder="Nombre de tu empresa"
                          class="billing-input"
                        />
                      </div>

                      <!-- NIT -->
                      <div class="billing-field">
                        <label class="billing-label">NIT</label>
                        <input
                          v-model="billingData.nit"
                          type="text"
                          placeholder="Tu número de NIT"
                          class="billing-input"
                        />
                      </div>

                      <!-- Email para Factura -->
                      <div class="billing-field">
                        <label class="billing-label">Email para Factura</label>
                        <input
                          v-model="billingData.invoiceEmail"
                          type="email"
                          placeholder="correo@empresa.com"
                          class="billing-input"
                        />
                      </div>
                    </div>

                    <!-- Aviso de privacidad -->
                    <div class="billing-disclaimer">
                      <va-icon name="info" size="x-small" />
                      <span>Esta información es opcional y se utilizará únicamente para emitir facturas</span>
                    </div>
                  </div>
                </transition>
              </div>
            </section>
          </div>
        </div>
      </template>

    <!-- BOTONES DE ACCIÓN (JOBS ONLY) -->
    <div v-if="type === 'job'" class="action-buttons">
      <button class="btn btn-secondary" @click="$emit('back')">
        <va-icon name="arrow_back" size="small" />
        ATRÁS
      </button>
      <button class="btn btn-primary" @click="$emit('submit')">
        <va-icon name="publish" size="small" />
        PUBLICAR OFERTA
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, nextTick, computed, ref } from 'vue'
import { PAYMENT_CONFIG } from '@/config/paymentConfig'

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
  }
})

const emit = defineEmits(['edit-step', 'submit'])

// ==========================================
// REFERENCIAS Y STATE
// ==========================================
const proofFileInput = ref(null)
const proofOfPaymentPreview = ref(null)
const paymentAccordionOpen = ref(true) // Abierto por defecto
const billingAccordionOpen = ref(false) // Cerrado por defecto
const billingData = ref({
  businessName: '',
  nit: '',
  invoiceEmail: ''
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
  if (!props.jobData?.expiryDate) return false
  const expiryDate = new Date(props.jobData.expiryDate)
  return expiryDate < new Date()
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
    profesionales: 'Profesionales',
    gastronomia: 'Gastronomía',
    trabajos: 'Trabajos',
    servicios: 'Servicios'
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

const getJobPlanName = (plan) => {
  const plans = {
    escencial: 'Plan Escencial',
    purpura: 'Plan Púrpura',
    impulso: 'Plan Impulso Pro'
  }
  return plans[plan] || plan
}

const getJobPlanIcon = (plan) => {
  const icons = {
    escencial: 'check_circle',
    purpura: 'star',
    impulso: 'workspace_premium'
  }
  return icons[plan] || 'check_circle'
}

const getJobPlanDescription = (plan) => {
  const descriptions = {
    escencial: 'Plan Escencial - 35 Bs. Tu oferta de trabajo estará visible por 30 días.',
    purpura: 'Plan Púrpura - 79 Bs. Tu oferta será destacada con mayor visibilidad por 30 días.',
    impulso: 'Plan Impulso Pro - 169 Bs. Tu oferta tendrá máxima visibilidad y aparecerá primero por 30 días.'
  }
  return descriptions[plan] || ''
}

// Obtener badges del plan seleccionado
const getPlanBadges = (plan) => {
  const badges = {
    escencial: ['Básico'],
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
}

// Limpiar carga de comprobante
const clearProofUpload = () => {
  proofOfPaymentPreview.value = null
  if (proofFileInput.value) {
    proofFileInput.value.value = ''
  }
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

// Toggle del acordeón de pagos
const togglePaymentAccordion = () => {
  paymentAccordionOpen.value = !paymentAccordionOpen.value
}

// Toggle del acordeón de facturación
const toggleBillingAccordion = () => {
  billingAccordionOpen.value = !billingAccordionOpen.value
}

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
onMounted(() => {
  if (props.formData.coordinates) {
    initMap()
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
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
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
  background: #F5F5F5;
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
  background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
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

.plan-card.plan-escencial {
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
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
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
  padding: 2rem 3rem 3rem 3rem;
  border-bottom: 2px solid #F0F3FF;
  background: white;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
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
  grid-template-columns: 200px 1fr auto;
  gap: 2rem 2.5rem;
  align-items: flex-start;
}

/* COLUMNA 1: LOGO GRANDE */
.logo-column {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 3.2rem;
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
  object-fit: cover;
  border-radius: 11px;
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
  gap: 1.2rem;
}

/* TÍTULO DEL PUESTO */
.job-title-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.job-title-label {
  font: 2.2rem;
  font-weight: 700;
  color: #7C3AED;
  letter-spacing: -0.3px;
  margin: 0;
}

.job-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #0F172A;
  margin: 0;
  line-height: 1.2;
  letter-spacing: -0.3px;
}

/* GRID DE INFORMACIÓN 2x2 */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2.5rem 2rem;
  margin-top: 1rem;
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
  gap: 0.5rem;
  padding: 0.65rem 1.25rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: none;
  transition: all 0.2s ease;
  min-width: 140px;
  text-align: center;
}

.badge-plan {
  background: linear-gradient(135deg, #F5F0FF 0%, #EDE9FE 100%);
  color: #7C3AED;
  border: 2px solid rgba(124, 58, 237, 0.3);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.15);
}

.badge-plan.plan-escencial {
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

/* ===== SECCIÓN BENEFICIOS ===== */
.benefits-list {
  list-style: none;
  padding: 0;
  margin: 1.25rem 0 0 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.benefit-item {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  padding: 1rem 1.25rem;
  background: #FAFBFF;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #334155;
  line-height: 1.6;
  border-left: 3px solid #10B981;
  transition: all 0.2s ease;
}

.benefit-item:hover {
  background: #F0FDF4;
}

.benefit-icon {
  color: #10B981;
  font-size: 1.2rem;
  flex-shrink: 0;
  margin-right: 0.5rem;
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
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.05);
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
    padding: 2rem;
    background: linear-gradient(135deg, #FAFBFF 0%, #F5F3FF 100%);
  }

  .company-section {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1rem;
  }

  .company-logo {
    width: 85px;
    height: 85px;
  }

  .company-logo-placeholder {
    width: 85px;
    height: 85px;
    font-size: 2.1rem;
  }

  .company-name {
    font-size: 1.35rem;
  }

  .job-title {
    font-size: 1.5rem;
    line-height: 1.3;
  }

  .header-badges {
    justify-content: center;
  }

  .header-meta {
    justify-content: center;
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

  .benefits-list {
    gap: 0.5rem;
  }

  .benefit-item {
    padding: 0.85rem 1rem;
    gap: 0.6rem;
  }

  .salary-amount {
    font-size: 1.6rem;
    padding: 1.25rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
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
    gap: 1.5rem;
  }

  .payment-qr-column {
    justify-content: flex-start;
  }

  .qr-card {
    max-width: 100%;
  }

  .payment-support-compact {
    flex-direction: column;
    gap: 0.75rem;
  }

  .support-text {
    font-size: 0.8rem;
  }

  .additional-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .info-technical {
    margin-left: -2rem;
    margin-right: -2rem;
    margin-bottom: -2rem;
    padding: 1.75rem 2rem;
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
    border-radius: 8px;
    margin-top: 1rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  }

  .job-header {
    padding: 1.5rem;
    gap: 1.25rem;
  }

  .company-section {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.8rem;
  }

  .company-logo {
    width: 75px;
    height: 75px;
  }

  .company-logo-placeholder {
    width: 75px;
    height: 75px;
    font-size: 1.9rem;
  }

  .company-name {
    font-size: 1.25rem;
  }

  .job-title {
    font-size: 1.25rem;
    font-weight: 800;
    line-height: 1.25;
  }

  .header-meta {
    gap: 0.75rem;
    padding-top: 0.5rem;
  }

  .meta-item {
    font-size: 0.8rem;
  }

  .header-badges {
    gap: 0.5rem;
  }

  .badge {
    padding: 0.35rem 0.7rem;
    font-size: 0.7rem;
  }

  .job-content {
    padding: 1.5rem;
  }

  .content-block {
    padding-bottom: 1.5rem;
  }

  .content-block:not(:last-child) {
    border-bottom: 1px solid #E2E8F0;
  }

  .block-title {
    font-size: 1rem;
    margin: 0 0 1rem 0;
  }

  .block-text {
    font-size: 0.9rem;
    line-height: 1.7;
  }

  .requirements-list {
    margin: 1rem 0 0 0;
    gap: 0.75rem;
  }

  .requirement-item {
    padding: 1rem;
    gap: 0.75rem;
    font-size: 0.9rem;
  }

  .requirement-icon {
    font-size: 1.1rem;
    margin-right: 0.3rem;
  }

  .benefits-list {
    margin: 1rem 0 0 0;
    gap: 0.5rem;
  }

  .benefit-item {
    padding: 0.85rem 1rem;
    gap: 0.6rem;
    font-size: 0.9rem;
  }

  .benefit-icon {
    font-size: 1rem;
    margin-right: 0.3rem;
  }

  .salary-label {
    font-size: 0.8rem;
  }

  .salary-amount {
    font-size: 1.4rem;
    padding: 1rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .info-group {
    gap: 1rem;
  }

  .info-item {
    gap: 0.3rem;
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
  color: var(--color-purple-dark);
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

.billing-form-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.billing-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.billing-label {
  font-weight: 600;
  color: var(--color-purple-dark);
  font-size: 0.95rem;
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

.billing-disclaimer {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: #F0F4FF;
  border-radius: 8px;
  border-left: 3px solid var(--color-purple);
  font-size: 0.9rem;
  color: #333;
  margin-top: 1rem;
}

.billing-disclaimer i {
  flex-shrink: 0;
  margin-top: 0.1rem;
  color: var(--color-purple);
}
</style>