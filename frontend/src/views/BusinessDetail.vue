<!-- frontend/src/views/BusinessDetail.vue -->
<!-- 🔥 VERSIÓN PRO - ELITE DESIGN -->
<template>
  <MainLayout>
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner">
        <VaProgressCircle indeterminate size="large" color="purple" />
        <p>Cargando negocio...</p>
      </div>
    </div>

    <div v-else-if="business" class="business-detail">
      
      <!-- Hero Banner with Overlay -->
      <div class="detail-hero">
        <div v-if="business.banner" class="hero-image">
          <img :src="business.banner" :alt="`Banner de ${business.name}`" />
          <div class="hero-overlay"></div>
        </div>
        <div v-else class="hero-placeholder">
          <va-icon name="business" size="8rem" color="rgba(255,255,255,0.3)" />
        </div>
        
        <!-- Plan Badge -->
        <div v-if="business.plan !== 'basico'" class="plan-badge-hero" :class="`badge-${business.plan}`">
          <va-icon :name="planIcon" />
          <span>{{ planLabel }}</span>
        </div>

        <!-- Hero Content -->
        <div class="hero-content">
          <div class="hero-wrapper">
            <div class="hero-logo">
              <div v-if="business.logo" class="logo-image">
                <img :src="business.logo" :alt="`Logo de ${business.name}`" />
              </div>
              <div v-else class="logo-placeholder">
                <va-icon name="business" size="3rem" />
              </div>
            </div>
            
            <div class="hero-info">
              <h1 class="hero-title">{{ business.name }}</h1>
              <div class="hero-meta">
                <VaChip color="purple" size="large">
                  <va-icon name="category" size="small" />
                  {{ business.category }}
                </VaChip>
                <VaChip v-if="business.verified" color="success" size="large">
                  <va-icon name="verified" size="small" />
                  Verificado
                </VaChip>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="detail-content">
        <div class="content-wrapper">
          
          <!-- Left Column - Tabs -->
          <div class="detail-main">
            
            <!-- Quick Actions Bar -->
            <div class="quick-actions">
              <VaButton
                color="success"
                icon="phone"
                @click="callBusiness"
              >
                Llamar Ahora
              </VaButton>
              <VaButton
                color="primary"
                icon="email"
                preset="secondary"
                @click="emailBusiness"
              >
                Enviar Email
              </VaButton>
              <VaButton
                v-if="business.website"
                color="purple"
                icon="language"
                preset="secondary"
                @click="visitWebsite"
              >
                Visitar Web
              </VaButton>
            </div>

            <!-- Tabs Navigation -->
            <div class="tabs-nav">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                class="tab-btn"
                :class="{ active: activeTab === tab.id }"
                @click="activeTab = tab.id"
              >
                <va-icon :name="tab.icon" />
                <span>{{ tab.label }}</span>
              </button>
            </div>

            <!-- Tab Content -->
            <div class="tab-content">
              
                            <!-- About Tab - Información -->
              <div v-show="activeTab === 'about'" class="tab-panel">
                <div class="content-section">
                  <h2 class="section-title">
                    <va-icon name="business" />
                    Acerca del negocio
                  </h2>
                  <p class="business-description">{{ business.description }}</p>
                </div>
                
                <div class="content-section" v-if="business.category">
                  <h2 class="section-title">
                    <va-icon name="category" />
                    Categoría
                  </h2>
                  <VaChip size="large" color="purple">{{ business.category }}</VaChip>
                </div>
                
                <div class="content-section" v-if="business.schedule">
                  <h2 class="section-title">
                    <va-icon name="schedule" />
                    Horario de atención
                  </h2>
                  <p class="business-info-text">{{ business.schedule }}</p>
                </div>
                
                <div class="content-section" v-if="business.features && business.features.length > 0">
                  <h2 class="section-title">
                    <va-icon name="star" />
                    Características destacadas
                  </h2>
                  <div class="features-grid">
                    <div v-for="(feature, index) in business.features" :key="index" class="feature-item">
                      <va-icon name="check_circle" color="success" />
                      <span>{{ feature }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Products Tab -->
              <div v-show="activeTab === 'products'" class="tab-panel">
                <div class="content-section">
                  <h2 class="section-title">
                    <va-icon name="inventory" />
                    Productos y Servicios
                  </h2>
                  
                  <div v-if="business.products && business.products.length > 0" class="products-grid">
                    <div v-for="product in business.products" :key="product.id" class="product-card">
                      <div v-if="product.image" class="product-image">
                        <img :src="product.image" :alt="product.name" />
                      </div>
                      <div v-else class="product-image-placeholder">
                        <va-icon name="inventory" size="3rem" color="#999" />
                      </div>
                      <div class="product-info">
                        <h3 class="product-name">{{ product.name }}</h3>
                        <p class="product-description">{{ product.description }}</p>
                        <div class="product-price" v-if="product.price">
                          <span class="price-label">Precio:</span>
                          <span class="price-value">Bs. {{ product.price }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div v-else class="empty-products">
                    <va-icon name="inventory" size="5rem" color="#CCC" />
                    <p>No hay productos o servicios disponibles en este momento</p>
                  </div>
                </div>
              </div>
              <!-- Location Tab - Ubicación -->
              <div v-show="activeTab === 'location'" class="tab-panel">
                <div class="content-section">
                  <h2 class="section-title">
                    <va-icon name="place" />
                    Ubicación
                  </h2>
                  
                  <!-- Info de dirección -->
                  <div class="location-address-card">
                    <div class="address-icon">
                      <va-icon name="location_on" size="large" />
                    </div>
                    <div class="address-content">
                      <p class="address-main">{{ business.address || 'Dirección no disponible' }}</p>
                      <p class="address-city">{{ business.city }}, Bolivia</p>
                    </div>
                  </div>
                  
                  <!-- Mapa simple y elegante -->
                  <div v-if="businessCoordinates" class="map-wrapper-elegant">
                    <MapLocation
                      ref="mapLocationRef"
                      :coordinates="businessCoordinates"
                      :address="business.address || `${business.city}, Bolivia`"
                      :title="business.name"
                      :zoom="16"
                      :height="'400px'"
                      :hide-header="true"
                      readonly
                    />
                  </div>
                  
                  <!-- Fallback sin mapa -->
                  <div v-else class="map-placeholder-simple">
                    <va-icon name="map" size="4rem" color="#999" />
                    <p>Ubicación en {{ business.city }}, Bolivia</p>
                  </div>
                </div>
              </div>

            </div>

          </div>

          <!-- Right Sidebar - Sticky -->
          <div class="detail-sidebar">
            
            <!-- Contact Card Premium -->
            <div class="sidebar-card premium-card">
              <div class="card-header">
                <va-icon name="contact_phone" size="large" />
                <h3>Contacto</h3>
              </div>
              
              <div class="contact-items">
                <a :href="`tel:${business.phone}`" class="contact-link">
                  <div class="contact-icon phone">
                    <va-icon name="phone" />
                  </div>
                  <div class="contact-info">
                    <span class="contact-label">Teléfono</span>
                    <span class="contact-value">{{ business.phone }}</span>
                  </div>
                </a>

                <a :href="`mailto:${business.email}`" class="contact-link">
                  <div class="contact-icon email">
                    <va-icon name="email" />
                  </div>
                  <div class="contact-info">
                    <span class="contact-label">Email</span>
                    <span class="contact-value">{{ business.email }}</span>
                  </div>
                </a>

                <a 
                  v-if="business.website" 
                  :href="`https://${business.website}`" 
                  target="_blank"
                  class="contact-link"
                >
                  <div class="contact-icon web">
                    <va-icon name="language" />
                  </div>
                  <div class="contact-info">
                    <span class="contact-label">Sitio Web</span>
                    <span class="contact-value">{{ business.website }}</span>
                  </div>
                </a>
              </div>
            </div>

            <!-- Share Card -->
            <div class="sidebar-card">
              <div class="card-header">
                <va-icon name="share" />
                <h3>Compartir</h3>
              </div>
              
              <div class="share-grid">
                <VaButton
                  preset="secondary"
                  icon="link"
                  @click="copyLink"
                >
                  Copiar
                </VaButton>
                <VaButton
                  preset="secondary"
                  :icon="isFavorite ? 'favorite' : 'favorite_border'"
                  :color="isFavorite ? 'danger' : undefined"
                  @click="toggleFavorite"
                >
                  {{ isFavorite ? 'Guardado' : 'Guardar' }}
                </VaButton>
              </div>
            </div>

            <!-- Info Card -->
            <div class="sidebar-card">
              <div class="card-header">
                <va-icon name="business" />
                <h3>Información</h3>
              </div>
              
              <div class="info-items">
                <div class="info-row">
                  <span class="info-label">NIT / RUC</span>
                  <span class="info-value">{{ business.nit }}</span>
                </div>
                <div v-if="business.createdAt" class="info-row">
                  <span class="info-label">En Guías Púrpuras desde</span>
                  <span class="info-value">{{ formatDate(business.createdAt) }}</span>
                </div>
              </div>
            </div>

          </div>

        </div>
      </div>

      <!-- WhatsApp Floating Button -->
      <button 
        v-if="business.phone"
        class="whatsapp-float"
        @click="openWhatsApp"
      >
        <svg viewBox="0 0 24 24" width="28" height="28">
          <path fill="white" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
        </svg>
        <span>WhatsApp</span>
      </button>

    </div>

    <div v-else class="error-container">
      <va-icon name="error" size="5rem" color="#CCC" />
      <h2>Negocio no encontrado</h2>
      <p>El negocio que buscas no existe o fue eliminado</p>
      <VaButton color="purple" @click="goBack">
        Volver al Listado
      </VaButton>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import MainLayout from '@/components/Layout/MainLayout.vue'
import { getBusinessBySlug } from '@/data/mockBusinesses'
import MapLocation from '@/components/Publish/MapLocation.vue'

const route = useRoute()
const router = useRouter()
const { init: notify } = useToast()

const business = ref(null)
const mapLocationRef = ref(null)

// NOTA: Los datos de 'business' vienen de getBusinessBySlug()
// Asegúrate de que el objeto incluya estos campos:
// - description: string
// - schedule: string  
// - features: array de strings
// - products: array de objetos con { id, name, description, price, image }
// - address: string
// - coordinates: string (formato: "lat, lng")
// Ejemplo:
// {
//   name: "Mi Negocio",
//   description: "Descripción del negocio...",
//   schedule: "Lun-Vie: 9:00-18:00",
//   features: ["WiFi gratis", "Parking"],
//   products: [
//     { id: 1, name: "Producto 1", description: "...", price: 100, image: "..." }
//   ],
//   address: "Av. Ejemplo 123",
//   coordinates: "-17.3935, -66.1570"
// }

const loading = ref(true)
const isFavorite = ref(false)
const activeTab = ref('about')

const tabs = [
  { id: 'about', label: 'Información', icon: 'info' },
  { id: 'products', label: 'Productos', icon: 'inventory' },
  { id: 'location', label: 'Ubicación', icon: 'place' }
]

const planIcon = computed(() => {
  switch (business.value?.plan) {
    case 'top': return 'star'
    case 'destacado': return 'trending_up'
    case 'sugerido': return 'thumb_up'
    default: return 'business'
  }
})

const planLabel = computed(() => {
  switch (business.value?.plan) {
    case 'top': return 'TOP'
    case 'destacado': return 'Destacado'
    case 'sugerido': return 'Sugerido'
    default: return ''
  }
})

// Convertir coordenadas de string a objeto { lat, lng }
const businessCoordinates = computed(() => {
  if (business.value?.coordinates) {
    const coords = business.value.coordinates.replace(/ /g, '').split(',')
    if (coords.length === 2) {
      return {
        lat: parseFloat(coords[0]),
        lng: parseFloat(coords[1])
      }
    }
  }
  return null
})

// Refrescar el mapa cuando se cambia al tab de ubicación
watch(activeTab, (newTab) => {
  if (newTab === 'location') {
    setTimeout(() => {
      if (mapLocationRef.value?.refreshMapSize) {
        mapLocationRef.value.refreshMapSize()
      }
    }, 100)
  }
})


const fetchBusiness = async () => {
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 500))
  const slug = route.params.slug
  business.value = getBusinessBySlug(slug)
  loading.value = false
}

const callBusiness = () => {
  window.location.href = `tel:${business.value.phone}`
}

const emailBusiness = () => {
  window.location.href = `mailto:${business.value.email}`
}

const visitWebsite = () => {
  window.open(`https://${business.value.website}`, '_blank')
}

const openWhatsApp = () => {
  const phone = business.value.phone.replace(/[^0-9]/g, '')
  const message = encodeURIComponent(`Hola! Vi tu negocio "${business.value.name}" en Guías Púrpuras y me gustaría obtener más información.`)
  window.open(`https://wa.me/591${phone}?text=${message}`, '_blank')
}

const copyLink = () => {
  navigator.clipboard.writeText(window.location.href)
  notify({
    message: '🔗 Enlace copiado al portapapeles',
    color: 'success',
    duration: 2000
  })
}

const toggleFavorite = () => {
  isFavorite.value = !isFavorite.value
  notify({
    message: isFavorite.value ? '❤️ Agregado a favoritos' : '💔 Eliminado de favoritos',
    color: isFavorite.value ? 'success' : 'info',
    duration: 2000
  })
}

const openInGoogleMaps = () => {
  if (business.value?.coordinates) {
    const coords = business.value.coordinates.replace(/ /g, '')
    window.open(`https://www.google.com/maps/search/?api=1&query=${coords}`, '_blank')
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'long' })
}

const goBack = () => {
  router.push('/guias/negocios')
}

onMounted(() => {
  fetchBusiness()
})
</script>

<style scoped>
/* Loading */
.loading-container {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-spinner p {
  color: #666;
  font-weight: 500;
}

/* Error */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 1.5rem;
  text-align: center;
}

/* Hero */
.detail-hero {
  position: relative;
  height: 400px;
  overflow: hidden;
  background: linear-gradient(135deg, #5C0099 0%, #8B00CC 100%);
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, 
    rgba(0,0,0,0.3) 0%, 
    rgba(92,0,153,0.8) 100%);
}

.hero-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.plan-badge-hero {
  position: absolute;
  top: 2rem;
  right: 2rem;
  padding: 0.75rem 1.5rem;
  border-radius: 30px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  font-size: 1rem;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
  z-index: 10;
}

.badge-top {
  background: rgba(255,215,0,0.95);
  color: #000;
}

.badge-destacado {
  background: rgba(139,0,204,0.95);
  color: white;
}

.badge-sugerido {
  background: rgba(76,175,80,0.95);
  color: white;
}

.hero-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2rem;
}

.hero-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  gap: 2rem;
  align-items: flex-end;
}

.hero-logo {
  width: 120px;
  height: 120px;
  flex-shrink: 0;
  border-radius: 20px;
  overflow: hidden;
  background: white;
  border: 4px solid white;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.logo-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 0.5rem;
}

.logo-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-info {
  flex: 1;
}

.hero-title {
  margin: 0 0 1rem 0;
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.hero-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Content */
.detail-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 2rem;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

/* Tabs */
.tabs-nav {
  display: flex;
  gap: 0.5rem;
  padding: 0.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  margin-bottom: 1.5rem;
}

.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  background: transparent;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  color: #666;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background: rgba(92,0,153,0.05);
}

.tab-btn.active {
  background: linear-gradient(135deg, #5C0099 0%, #7B1FA2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(92,0,153,0.3);
}

/* Tab Content */
.tab-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 2rem;
}

.tab-panel {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.content-section {
  margin-bottom: 2rem;
}

.content-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #5C0099;
  margin: 0 0 1.5rem 0;
}

.section-text {
  margin: 0;
  color: #666;
  font-size: 1.05rem;
  line-height: 1.8;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

/* Products */
.products-showcase {
  display: grid;
  gap: 1.5rem;
}

.product-item {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  background: #F8F8F8;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.product-item:hover {
  transform: translateX(8px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.product-img {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.product-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-details h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.1rem;
}

.product-details p {
  margin: 0;
  color: #666;
}

/* Location */
.location-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #666;
}

.map-btn {
  width: 100%;
}

/* Sidebar */
.detail-sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.sidebar-card {
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  margin-bottom: 1.5rem;
}

.premium-card {
  background: linear-gradient(135deg, 
    rgba(92,0,153,0.03) 0%, 
    rgba(92,0,153,0.01) 100%);
  border: 2px solid rgba(92,0,153,0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #5C0099;
}

/* Contact Items */
.contact-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contact-link {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.05);
}

.contact-link:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(92,0,153,0.15);
}

.contact-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.contact-icon.phone {
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
}

.contact-icon.email {
  background: linear-gradient(135deg, #2196F3 0%, #42A5F5 100%);
}

.contact-icon.web {
  background: linear-gradient(135deg, #5C0099 0%, #7B1FA2 100%);
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.contact-label {
  font-size: 0.75rem;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
}

.contact-value {
  color: #333;
  font-weight: 500;
}

/* Share */
.share-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

/* Info */
.info-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.info-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-label {
  font-size: 0.75rem;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
}

.info-value {
  color: #333;
  font-weight: 500;
}

/* WhatsApp Float */
.whatsapp-float {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: auto;
  padding: 1rem 1.5rem;
  background: #25D366;
  color: white;
  border: none;
  border-radius: 50px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  font-size: 1rem;
  box-shadow: 0 8px 24px rgba(37,211,102,0.4);
  cursor: pointer;
  z-index: 1000;
  transition: all 0.3s ease;
  animation: whatsappPulse 2s ease-in-out infinite;
}

.whatsapp-float:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 32px rgba(37,211,102,0.5);
}

@keyframes whatsappPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem;
  color: #999;
}

/* Responsive */
@media (max-width: 1024px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }

  .detail-sidebar {
    position: relative;
    top: 0;
  }
}

@media (max-width: 768px) {
  .detail-hero {
    height: 300px;
  }

  .hero-wrapper {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .detail-content {
    padding: 1rem;
  }

  .quick-actions {
    flex-direction: column;
  }

  .tabs-nav {
    flex-direction: column;
  }

  .whatsapp-float {
    bottom: 1rem;
    right: 1rem;
  }

  .whatsapp-float span {
    display: none;
  }

  .whatsapp-float {
    width: 60px;
    height: 60px;
    padding: 0;
    border-radius: 50%;
    justify-content: center;
  }
}


/* ====================================
   📍 LOCATION SECTION - ELEGANT & SIMPLE
   ==================================== */

.location-address-card {
  display: flex;
  gap: 1.25rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFF 100%);
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.location-address-card:hover {
  border-color: rgba(92, 0, 153, 0.3);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.1);
}

.address-icon {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #5C0099, #8B00CC);
  border-radius: 12px;
  color: white;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

.address-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.address-main {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1F2937;
  margin: 0 0 0.25rem 0;
  line-height: 1.4;
}

.address-city {
  font-size: 0.95rem;
  color: #6B7280;
  margin: 0;
}

.map-wrapper-elegant {
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border: 3px solid rgba(92, 0, 153, 0.15);
  transition: all 0.3s ease;
}

.map-wrapper-elegant :deep(.map-location) {
  border-radius: 16px;
  display: flex;
  flex-direction: column;
}

.map-wrapper-elegant :deep(.map-container) {
  height: 400px !important;
  width: 100%;
  overflow: hidden;
  border-radius: 0;
}

.map-wrapper-elegant :deep(.leaflet-map) {
  height: 100% !important;
  width: 100%;
}

.map-wrapper-elegant :deep(.map-footer) {
  flex-shrink: 0;
}

.map-wrapper-elegant:hover {
  box-shadow: 0 12px 32px rgba(92, 0, 153, 0.2);
  border-color: rgba(92, 0, 153, 0.3);
}

.map-placeholder-simple {
  padding: 4rem 2rem;
  text-align: center;
  background: #F9FAFB;
  border-radius: 16px;
  border: 2px dashed #D1D5DB;
}

.map-placeholder-simple p {
  margin: 1rem 0 0 0;
  color: #6B7280;
  font-size: 0.95rem;
}

/* Responsive */
@media (max-width: 768px) {
  .location-address-card {
    padding: 1.25rem;
  }
  
  .address-icon {
    width: 50px;
    height: 50px;
  }
  
  .address-main {
    font-size: 1rem;
  }

}


/* ====================================
   📝 TAB ABOUT - INFORMACIÓN
   ==================================== */

.business-description {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #374151;
  margin: 0;
}

.business-info-text {
  font-size: 1rem;
  color: #4B5563;
  margin: 0;
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 8px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFF 100%);
  border-radius: 10px;
  border: 2px solid rgba(92, 0, 153, 0.1);
  transition: all 0.3s ease;
}

.feature-item:hover {
  border-color: rgba(92, 0, 153, 0.3);
  transform: translateX(5px);
}

.feature-item span {
  font-size: 0.95rem;
  color: #374151;
  font-weight: 500;
}

/* ====================================
   📦 TAB PRODUCTS - PRODUCTOS
   ==================================== */

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.product-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(92, 0, 153, 0.2);
  border-color: rgba(92, 0, 153, 0.3);
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.1);
}

.product-image-placeholder {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F3F4F6, #E5E7EB);
}

.product-info {
  padding: 1.5rem;
}

.product-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.5rem 0;
}

.product-description {
  font-size: 0.9rem;
  color: #6B7280;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.product-price {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-top: 1rem;
  border-top: 2px solid rgba(92, 0, 153, 0.1);
}

.price-label {
  font-size: 0.85rem;
  color: #6B7280;
  font-weight: 500;
}

.price-value {
  font-size: 1.3rem;
  font-weight: 700;
  color: #5C0099;
}

.empty-products {
  padding: 4rem 2rem;
  text-align: center;
  color: #9CA3AF;
}

.empty-products p {
  margin: 1rem 0 0 0;
  font-size: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>