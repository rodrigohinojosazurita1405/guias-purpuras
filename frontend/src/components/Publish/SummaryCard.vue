<!-- frontend/src/components/Publish/SummaryCard.vue -->
<template>
  <div class="summary-card">
    <!-- 
      ==========================================
      RESUMEN Y PREVIEW DEL ANUNCIO
      ==========================================
      Muestra cómo se verá el anuncio publicado:
        - Información completa
        - Vista previa de imágenes
        - Badge del plan seleccionado
        - Datos de contacto
        - Botón para editar cada sección
      
      Props:
        - formData: Objeto con todos los datos del formulario
        - editable: Boolean para mostrar/ocultar botones de editar
      
      TODO Django:
        - Usar este mismo diseño para mostrar el anuncio real
        - Mantener consistencia visual
    -->

    <div class="summary-header">
      <h3 class="summary-title">
        <va-icon name="preview" color="purple" />
        Vista Previa de tu Anuncio
      </h3>
      <p class="summary-subtitle">
        Así es como verán tu anuncio los usuarios
      </p>
    </div>

    <!-- ==========================================
         PREVIEW DEL ANUNCIO (Como ListingCard)
         ========================================== -->
    <div class="listing-preview" :class="previewClass">
      <!-- Badge Premium -->
      <div v-if="formData.plan !== 'free'" class="premium-badge">
        <va-icon :name="badgeIcon" size="small" />
        {{ badgeText }}
      </div>

      <!-- Galería de Imágenes -->
      <div class="listing-images">
        <div v-if="formData.images && formData.images.length > 0" class="image-gallery">
          <img 
            :src="formData.images[0].preview" 
            :alt="formData.title"
            class="main-image"
          />
          <div v-if="formData.images.length > 1" class="image-counter">
            <va-icon name="photo_library" size="small" />
            {{ formData.images.length }} fotos
          </div>
        </div>
        <div v-else class="no-image">
          <va-icon name="image" size="3rem" color="gray" />
          <span>Sin imágenes</span>
        </div>

        <!-- Badge de Categoría -->
        <div class="category-badge">
          <va-icon :name="categoryIcon" size="small" />
          {{ formData.category || 'Sin categoría' }}
        </div>
      </div>

      <!-- Contenido del Anuncio -->
      <div class="listing-content">
        <!-- Título -->
        <h2 class="listing-title">
          {{ formData.title || 'Título del anuncio' }}
        </h2>

        <!-- Precio (si existe) -->
        <div v-if="formData.price" class="listing-price">
          <va-icon name="payments" size="small" color="success" />
          <span class="price-amount">Bs. {{ formatPrice(formData.price) }}</span>
        </div>

        <!-- Descripción -->
        <p class="listing-description">
          {{ formData.description || 'Descripción del anuncio' }}
        </p>

        <!-- Información de Contacto -->
        <div class="listing-info">
          <div class="info-item">
            <va-icon name="location_on" size="small" color="purple" />
            <span>{{ formData.address || 'Dirección' }}, {{ getCityName(formData.city) }}</span>
          </div>

          <div v-if="formData.whatsapp" class="info-item whatsapp-item">
            <va-icon name="whatsapp" size="small" style="color: #25D366;" />
            <a :href="getWhatsAppLink(formData.whatsapp)" target="_blank" class="whatsapp-link">
              {{ formData.whatsapp }}
            </a>
          </div>

          <div v-if="formData.email" class="info-item">
            <va-icon name="email" size="small" color="purple" />
            <span>{{ formData.email }}</span>
          </div>

          <div v-if="formData.website" class="info-item">
            <va-icon name="link" size="small" color="purple" />
            <span>{{ formData.website }}</span>
          </div>
        </div>

        <!-- Metadata del Anuncio -->
        <div class="listing-meta">
          <div class="meta-item">
            <va-icon name="category" size="small" />
            <span>{{ formData.subcategory || 'Subcategoría' }}</span>
          </div>
          <div class="meta-item">
            <va-icon name="schedule" size="small" />
            <span>Publicado: Hoy</span>
          </div>
          <div class="meta-item">
            <va-icon name="visibility" size="small" />
            <span>{{ visibilityText }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         DETALLES DEL RESUMEN
         ========================================== -->
    <div class="summary-details">
      <h4 class="details-title">
        <va-icon name="checklist" />
        Resumen de Publicación
      </h4>

      <!-- Sección 1: Categorización -->
      <div class="detail-section">
        <div class="detail-header">
          <va-icon name="category" color="purple" />
          <span class="detail-label">Categorización</span>
          <button 
            v-if="editable"
            @click="$emit('edit-step', 1)"
            class="edit-btn"
          >
            <va-icon name="edit" size="small" />
            Editar
          </button>
        </div>
        <div class="detail-items">
          <div class="detail-item">
            <span class="detail-key">Categoría:</span>
            <span class="detail-value">{{ getCategoryName(formData.category) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-key">Subcategoría:</span>
            <span class="detail-value">{{ formData.subcategory || '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-key">Ubicación:</span>
            <span class="detail-value">{{ formData.address }}, {{ getCityName(formData.city) }}</span>
          </div>
        </div>
      </div>

      <!-- Sección 2: Información -->
      <div class="detail-section">
        <div class="detail-header">
          <va-icon name="description" color="purple" />
          <span class="detail-label">Información</span>
          <button 
            v-if="editable"
            @click="$emit('edit-step', 2)"
            class="edit-btn"
          >
            <va-icon name="edit" size="small" />
            Editar
          </button>
        </div>
        <div class="detail-items">
          <div class="detail-item">
            <span class="detail-key">Título:</span>
            <span class="detail-value">{{ formData.title || '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-key">Descripción:</span>
            <span class="detail-value truncate">{{ formData.description || '-' }}</span>
          </div>
          <div v-if="formData.price" class="detail-item">
            <span class="detail-key">Precio:</span>
            <span class="detail-value price-highlight">Bs. {{ formatPrice(formData.price) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-key">WhatsApp:</span>
            <span class="detail-value whatsapp-detail">
              <a :href="getWhatsAppLink(formData.whatsapp)" target="_blank" class="whatsapp-link">
                {{ formData.whatsapp || '-' }}
              </a>
            </span>
          </div>
        </div>
      </div>

      <!-- Sección 3: Imágenes -->
      <div class="detail-section">
        <div class="detail-header">
          <va-icon name="image" color="purple" />
          <span class="detail-label">Imágenes</span>
          <button 
            v-if="editable"
            @click="$emit('edit-step', 3)"
            class="edit-btn"
          >
            <va-icon name="edit" size="small" />
            Editar
          </button>
        </div>
        <div class="detail-items">
          <div class="detail-item">
            <span class="detail-key">Total de imágenes:</span>
            <span class="detail-value">{{ formData.images?.length || 0 }}</span>
          </div>
          <div v-if="formData.images && formData.images.length > 0" class="images-thumbnails">
            <div 
              v-for="(img, index) in formData.images.slice(0, 4)" 
              :key="index"
              class="thumbnail"
            >
              <img :src="img.preview" :alt="`Imagen ${index + 1}`" />
              <span v-if="index === 0" class="main-indicator">Principal</span>
            </div>
            <div v-if="formData.images.length > 4" class="more-images">
              +{{ formData.images.length - 4 }}
            </div>
          </div>
        </div>
      </div>

      <!-- Sección 4: Plan -->
      <div class="detail-section plan-section" :class="`plan-${formData.plan}`">
        <div class="detail-header">
          <va-icon name="workspace_premium" color="purple" />
          <span class="detail-label">Plan Seleccionado</span>
          <button 
            v-if="editable"
            @click="$emit('edit-step', 4)"
            class="edit-btn"
          >
            <va-icon name="edit" size="small" />
            Cambiar
          </button>
        </div>
        <div class="plan-details">
          <div class="plan-info-item">
            <span class="plan-name">{{ planName }}</span>
            <span class="plan-price">{{ planPrice }}</span>
          </div>
          <div class="plan-features-summary">
            <span><va-icon name="schedule" size="small" /> {{ planDuration }}</span>
            <span><va-icon name="image" size="small" /> {{ planImages }}</span>
            <span><va-icon name="visibility" size="small" /> {{ planVisibility }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         ALERTAS Y NOTAS
         ========================================== -->
    <div class="summary-alerts">
      <!-- Alerta de datos faltantes -->
      <div v-if="!isComplete" class="alert warning">
        <va-icon name="warning" />
        <div class="alert-content">
          <strong>Información incompleta</strong>
          <span>Revisa que todos los campos obligatorios estén llenos</span>
        </div>
      </div>

      <!-- Alerta de plan de pago -->
      <div v-if="formData.plan !== 'free'" class="alert info">
        <va-icon name="info" />
        <div class="alert-content">
          <strong>Pago requerido</strong>
          <span>Serás redirigido a la pasarela de pago después de confirmar</span>
        </div>
      </div>

      <!-- Nota de confirmación -->
      <div class="alert success">
        <va-icon name="check_circle" />
        <div class="alert-content">
          <strong>Todo listo</strong>
          <span>Tu anuncio se verá así una vez publicado</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// ==========================================
// PROPS
// ==========================================
const props = defineProps({
  formData: {
    type: Object,
    required: true,
    default: () => ({
      category: '',
      subcategory: '',
      department: '',
      city: '',
      title: '',
      description: '',
      price: null,
      phone: '',
      email: '',
      website: '',
      images: [],
      plan: 'free'
    })
  },
  editable: {
    type: Boolean,
    default: true
  }
})

// ==========================================
// EMITS
// ==========================================
defineEmits(['edit-step'])

// ==========================================
// COMPUTED - Información del Plan
// ==========================================
const planName = computed(() => {
  const names = {
    free: '🆓 Plan Gratis',
    featured: '⭐ Plan Destacado',
    top: '🏆 Plan TOP'
  }
  return names[props.formData.plan] || 'Sin plan'
})

const planPrice = computed(() => {
  const prices = {
    free: 'Bs. 0',
    featured: 'Bs. 25',
    top: 'Bs. 60'
  }
  return prices[props.formData.plan] || 'Bs. 0'
})

const planDuration = computed(() => {
  // CAMBIO: Si es Profesionales y plan gratis, es permanente
  if (props.formData.category === 'profesionales' && props.formData.plan === 'free') {
    return '♾️ Permanente'
  }
  
  const durations = {
    free: '7 días',
    featured: '30 días',
    top: '60 días'
  }
  return durations[props.formData.plan] || '7 días'
})

const planImages = computed(() => {
  const images = {
    free: 'Hasta 3 imágenes',
    featured: 'Hasta 5 imágenes',
    top: 'Ilimitadas'
  }
  return images[props.formData.plan] || 'Hasta 3'
})

const planVisibility = computed(() => {
  const visibility = {
    free: '1x visibilidad',
    featured: '3x visibilidad',
    top: '10x visibilidad'
  }
  return visibility[props.formData.plan] || '1x'
})

const visibilityText = computed(() => {
  const text = {
    free: 'Visibilidad normal',
    featured: '3x más visible',
    top: '10x más visible'
  }
  return text[props.formData.plan] || 'Normal'
})

// ==========================================
// COMPUTED - Estilos y Clases
// ==========================================
const previewClass = computed(() => {
  return {
    'is-featured': props.formData.plan === 'featured',
    'is-top': props.formData.plan === 'top'
  }
})

const badgeIcon = computed(() => {
  return props.formData.plan === 'top' ? 'stars' : 'star'
})

const badgeText = computed(() => {
  return props.formData.plan === 'top' ? 'TOP' : 'DESTACADO'
})

const categoryIcon = computed(() => {
  const icons = {
    profesionales: 'work',
    gastronomia: 'restaurant',
    trabajos: 'business_center',
    servicios: 'build'
  }
  return icons[props.formData.category] || 'category'
})

// ==========================================
// COMPUTED - Validación
// ==========================================
const isComplete = computed(() => {
  return (
    props.formData.category &&
    props.formData.subcategory &&
    props.formData.department &&
    props.formData.city &&
    props.formData.title &&
    props.formData.description &&
    props.formData.phone &&
    props.formData.plan
  )
})

// ==========================================
// MÉTODOS AUXILIARES
// ==========================================
const formatPrice = (price) => {
  if (!price) return '0.00'
  return Number(price).toFixed(2)
}

const getCategoryName = (id) => {
  const names = {
    profesionales: '📋 Profesionales',
    gastronomia: '🍽️ Gastronomía',
    trabajos: '💼 Trabajos',
    servicios: '🛠️ Servicios'
  }
  return names[id] || '-'
}

// CAMBIO: Renombrado de getDepartmentName a getCityName
const getCityName = (id) => {
  const names = {
    'la-paz': 'La Paz',
    'el-alto': 'El Alto',
    'cochabamba': 'Cochabamba',
    'santa-cruz': 'Santa Cruz',
    'oruro': 'Oruro',
    'potosi': 'Potosí',
    'tarija': 'Tarija',
    'sucre': 'Sucre',
    'trinidad': 'Trinidad',
    'cobija': 'Cobija',
    'quillacollo': 'Quillacollo',
    'sacaba': 'Sacaba',
    'montero': 'Montero',
    'warnes': 'Warnes'
  }
  return names[id] || id || '-'
}

// NUEVO: Generar link de WhatsApp
const getWhatsAppLink = (whatsapp) => {
  if (!whatsapp) return '#'
  // Remover el + y espacios para el link
  const cleanNumber = whatsapp.replace(/\+/g, '').replace(/\s/g, '')
  return `https://wa.me/${cleanNumber}`
}
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.summary-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

/* ==========================================
   HEADER
   ========================================== */
.summary-header {
  margin-bottom: 2rem;
  text-align: center;
}

.summary-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 0.5rem;
}

.summary-subtitle {
  color: #666;
  font-size: 1rem;
}

/* ==========================================
   PREVIEW DEL ANUNCIO
   ========================================== */
.listing-preview {
  background: #FAFAFA;
  border: 2px solid #E0E0E0;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 2rem;
  position: relative;
  transition: all 0.3s ease;
}

.listing-preview.is-featured {
  border-color: var(--color-purple);
  box-shadow: 0 4px 16px rgba(92, 0, 153, 0.15);
}

.listing-preview.is-top {
  border-color: var(--color-yellow-primary);
  box-shadow: 0 6px 20px rgba(253, 197, 0, 0.3);
}

/* Premium Badge */
.premium-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, #FFB800 100%);
  color: var(--color-purple-darkest);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.8rem;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Imágenes */
.listing-images {
  width: 100%;
  height: 250px;
  position: relative;
  background: #F5F5F5;
}

.image-gallery {
  width: 100%;
  height: 100%;
  position: relative;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-counter {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #999;
}

.category-badge {
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  background: rgba(92, 0, 153, 0.95);
  backdrop-filter: blur(10px);
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-transform: capitalize;
}

/* Contenido */
.listing-content {
  padding: 1.5rem;
  background: white;
}

.listing-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.75rem 0;
  line-height: 1.3;
}

.listing-price {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.price-amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2E7D32;
}

.listing-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.listing-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #E0E0E0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #666;
  font-size: 0.95rem;
}

.info-item.whatsapp-item {
  color: #25D366;
}

.whatsapp-link {
  color: #25D366;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.whatsapp-link:hover {
  color: #128C7E;
  text-decoration: underline;
}

.whatsapp-detail .whatsapp-link {
  color: #25D366;
  font-weight: 700;
}

.listing-meta {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #999;
  font-size: 0.9rem;
}

/* ==========================================
   DETALLES DEL RESUMEN
   ========================================== */
.summary-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.details-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 0.5rem;
}

/* Secciones de Detalle */
.detail-section {
  background: #F8F9FA;
  border-radius: 12px;
  padding: 1.5rem;
  border: 2px solid #E0E0E0;
}

.detail-section.plan-section {
  background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
}

.detail-section.plan-section.plan-featured {
  border-color: var(--color-purple);
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.03) 0%, #FFFFFF 100%);
}

.detail-section.plan-section.plan-top {
  border-color: var(--color-yellow-primary);
  background: linear-gradient(135deg, rgba(253, 197, 0, 0.05) 0%, #FFFFFF 100%);
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.detail-label {
  flex: 1;
  font-weight: 700;
  color: var(--color-purple-darkest);
  font-size: 1.05rem;
}

.edit-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid var(--color-purple);
  border-radius: 8px;
  color: var(--color-purple);
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: var(--color-purple);
  color: white;
}

/* Items de Detalle */
.detail-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-item {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 1rem;
  align-items: start;
}

.detail-key {
  font-weight: 600;
  color: #666;
}

.detail-value {
  color: var(--color-purple-darkest);
}

.detail-value.truncate {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.detail-value.price-highlight {
  color: #2E7D32;
  font-weight: 700;
  font-size: 1.1rem;
}

/* Thumbnails de Imágenes */
.images-thumbnails {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.thumbnail {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  border: 2px solid #E0E0E0;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.main-indicator {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  font-size: 0.7rem;
  font-weight: 700;
  text-align: center;
  padding: 0.25rem;
}

.more-images {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  background: #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #666;
  font-size: 1.25rem;
}

/* Detalles del Plan */
.plan-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.plan-info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plan-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
}

.plan-price {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-purple);
}

.plan-features-summary {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  color: #666;
  font-size: 0.95rem;
}

.plan-features-summary span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* ==========================================
   ALERTAS
   ========================================== */
.summary-alerts {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.alert {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid;
}

.alert.warning {
  background: #FFF9E6;
  border-color: #FFD54F;
  color: #F57C00;
}

.alert.info {
  background: #E3F2FD;
  border-color: #90CAF9;
  color: #1565C0;
}

.alert.success {
  background: #E8F5E9;
  border-color: #81C784;
  color: #2E7D32;
}

.alert-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.alert-content strong {
  font-weight: 700;
}

.alert-content span {
  font-size: 0.95rem;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
  .summary-card {
    padding: 1.5rem;
  }

  .summary-title {
    font-size: 1.5rem;
  }

  .listing-images {
    height: 200px;
  }

  .listing-title {
    font-size: 1.25rem;
  }

  .detail-item {
    grid-template-columns: 1fr;
    gap: 0.25rem;
  }

  .plan-features-summary {
    flex-direction: column;
    gap: 0.5rem;
  }

  .edit-btn span {
    display: none;
  }
}
</style>