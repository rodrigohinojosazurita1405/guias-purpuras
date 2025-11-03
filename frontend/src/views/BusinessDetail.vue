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
              
              <!-- About Tab -->
              <div v-show="activeTab === 'about'" class="tab-panel">
                <div class="content-section">
                  <h2 class="section-title">
                    <va-icon name="info" />
                    Acerca de la Empresa
                  </h2>
                  <p class="section-text">{{ business.description }}</p>
                </div>

                <!-- Tags -->
                <div v-if="business.tags && business.tags.length > 0" class="content-section">
                  <h2 class="section-title">
                    <va-icon name="tag" />
                    Etiquetas
                  </h2>
                  <div class="tags-cloud">
                    <VaChip
                      v-for="(tag, index) in business.tags"
                      :key="index"
                      color="purple"
                      outline
                      size="large"
                    >
                      {{ tag }}
                    </VaChip>
                  </div>
                </div>
              </div>

              <!-- Products Tab -->
              <div v-show="activeTab === 'products'" class="tab-panel">
                <div v-if="business.products && business.products.length > 0" class="content-section">
                  <h2 class="section-title">
                    <va-icon name="inventory" />
                    Productos y Servicios
                  </h2>
                  <div class="products-showcase">
                    <div 
                      v-for="(product, index) in business.products" 
                      :key="index" 
                      class="product-item"
                    >
                      <div v-if="product.image" class="product-img">
                        <img :src="product.image" :alt="product.name" />
                      </div>
                      <div class="product-details">
                        <h4>{{ product.name }}</h4>
                        <p>{{ product.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="empty-state">
                  <va-icon name="inventory_2" size="3rem" color="#CCC" />
                  <p>No hay productos registrados</p>
                </div>
              </div>

              <!-- Contact Tab -->
              <div v-show="activeTab === 'contact'" class="tab-panel">
                <div class="content-section">
                  <h2 class="section-title">
                    <va-icon name="place" />
                    Ubicación
                  </h2>
                  <div class="location-info">
                    <div class="info-row">
                      <va-icon name="home" />
                      <span>{{ business.address || 'Dirección no disponible' }}</span>
                    </div>
                    <div class="info-row">
                      <va-icon name="location_city" />
                      <span>{{ business.city || 'Bolivia' }}</span>
                    </div>
                  </div>
                  <VaButton
                    v-if="business.coordinates"
                    color="purple"
                    icon="open_in_new"
                    class="map-btn"
                    @click="openInGoogleMaps"
                  >
                    Ver en Google Maps
                  </VaButton>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import MainLayout from '@/components/Layout/MainLayout.vue'
import { getBusinessBySlug } from '@/data/mockBusinesses'

const route = useRoute()
const router = useRouter()
const { init: notify } = useToast()

const business = ref(null)
const loading = ref(true)
const isFavorite = ref(false)
const activeTab = ref('about')

const tabs = [
  { id: 'about', label: 'Información', icon: 'info' },
  { id: 'products', label: 'Productos', icon: 'inventory' },
  { id: 'contact', label: 'Contacto', icon: 'place' }
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
</style>