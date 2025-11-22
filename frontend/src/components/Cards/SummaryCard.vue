<!-- 
  ==========================================
  SUMMARYCARD.VUE - ACTUALIZADO
  ==========================================
  
  Resumen completo del anuncio antes de publicar.
  Incluye sección especial para mostrar los platos del menú (gastronomía).
-->

<template>
  <div class="summary-card">
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
      
      <!-- CATEGORÍA Y UBICACIÓN -->
      <div class="summary-section">
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

      <!-- INFORMACIÓN GENERAL -->
      <div class="summary-section">
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

      <!-- IMÁGENES DEL NEGOCIO -->
      <div class="summary-section">
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

      <!-- INFORMACIÓN DEL TRABAJO (JOBS ONLY) -->
      <div v-if="type === 'job' && jobData" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="work" size="1.25rem" />
            Información del Trabajo
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
          <div class="info-row">
            <span class="label">Categoría:</span>
            <span class="value">{{ jobData.jobCategory }}</span>
          </div>
          <div class="info-row">
            <span class="label">Tipo de Contrato:</span>
            <span class="value">{{ jobData.contractType }}</span>
          </div>
          <div class="info-row">
            <span class="label">Ciudad:</span>
            <span class="value">{{ jobData.city }}</span>
          </div>
          <div class="info-row full-width">
            <span class="label">Descripción:</span>
            <p class="value description">{{ jobData.description }}</p>
          </div>
        </div>
      </div>

      <!-- REQUISITOS (JOBS ONLY) -->
      <div v-if="type === 'job' && jobData" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="assignment" size="1.25rem" />
            Requisitos
          </h3>
        </div>

        <div class="section-content">
          <div class="info-row full-width">
            <span class="label">Requisitos:</span>
            <p class="value description">{{ jobData.requirements }}</p>
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
          <div v-if="jobData.technicalSkills" class="info-row">
            <span class="label">Habilidades Técnicas:</span>
            <span class="value">{{ jobData.technicalSkills }}</span>
          </div>
        </div>
      </div>

      <!-- COMPENSACIÓN (JOBS ONLY) -->
      <div v-if="type === 'job' && jobData" class="summary-section">
        <div class="section-header">
          <h3 class="section-title">
            <va-icon name="attach_money" size="1.25rem" />
            Compensación
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

      <!-- PLAN SELECCIONADO -->
      <div class="summary-section">
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

    <!-- BOTÓN PUBLICAR (JOBS ONLY) -->
    <div v-if="type === 'job'" class="action-buttons">
      <button class="btn btn-primary" @click="$emit('submit')">
        <va-icon name="publish" size="small" />
        PUBLICAR OFERTA
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, nextTick } from 'vue'

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
// METHODS
// ==========================================

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
}

/* ==========================================
   HEADER
   ========================================== */
.summary-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #E0E0E0;
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
  background: #F8F8F8;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #E0E0E0;
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
  padding: 1.5rem;
  border: 2px solid #E0E0E0;
}

.plan-card.plan-free {
  border-color: var(--va-success);
}

.plan-card.plan-featured {
  border-color: var(--color-yellow-primary);
  background: #FFFBF0;
}

.plan-card.plan-top {
  border-color: var(--color-purple);
  background: linear-gradient(135deg, #F5F0FF 0%, #FFFFFF 100%);
}

.plan-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 0.5rem;
}

.plan-description {
  font-size: 0.95rem;
  color: #666;
  margin: 0;
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
  justify-content: center;
  padding: 2.5rem;
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  border-top: 2px solid #E2E8F0;
  margin-top: 2rem;
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

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
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
}
</style>