<!-- frontend/src/views/BusinessDetail.vue -->
<template>
  <MainLayout>
    <section class="business-detail-section">
      <div class="container">
        <!-- Breadcrumb -->
        <nav class="breadcrumb">
          <router-link to="/">Inicio</router-link>
          <span class="separator">/</span>
          <router-link to="/guias/negocios">Negocios</router-link>
          <span class="separator">/</span>
          <span class="current">{{ business.name }}</span>
        </nav>

        <!-- Header Card -->
        <div class="business-header">
          <!-- Foto de perfil única -->
          <div class="business-profile-image">
            <div v-if="business.logo" class="profile-image-container">
              <img 
                :src="business.logo" 
                :alt="`Logo de ${business.name}`"
                class="profile-image"
              />
            </div>
            <!-- Placeholder si no hay imagen -->
            <div v-else class="placeholder-image">
              <va-icon name="business" size="5rem" color="#999" />
            </div>
          </div>

          <!-- Información Principal -->
          <div class="business-info">
            <!-- ✅ BADGES MEJORADOS -->
            <div class="badges-row">
              <div v-if="business.verified" class="badge-verified">
                <va-icon name="verified" size="small" />
                Verificado
              </div>
              <div v-if="business.plan === 'destacado'" class="badge-destacado">
                <va-icon name="star" size="small" />
                Destacado
              </div>
              <div v-if="business.plan === 'premium'" class="badge-premium">
                <va-icon name="star" size="small" />
                Premium
              </div>
              <div v-if="business.featured" class="badge-featured">
                <va-icon name="workspace_premium" size="small" />
                Destacado del mes
              </div>
            </div>

            <h1 class="business-title">{{ business.name }}</h1>
            <p class="business-category">{{ business.category }}</p>

            <!-- Info Grid -->
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Categoría:</span>
                <span class="info-value">{{ business.category }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Ciudad:</span>
                <span class="info-value">{{ business.city }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Horario:</span>
                <span class="info-value">{{ business.schedule || 'No especificado' }}</span>
              </div>
              <div v-if="business.address" class="info-item">
                <span class="info-label">Dirección:</span>
                <span class="info-value">{{ business.address }}</span>
              </div>
            </div>

            <!-- Características destacadas -->
            <div v-if="business.features && business.features.length > 0" class="features-row">
              <span class="features-label">Características:</span>
              <div class="features">
                <span 
                  v-for="(feature, index) in business.features.slice(0, 3)" 
                  :key="index"
                  class="feature"
                >
                  {{ feature }}
                </span>
              </div>
            </div>
          </div>

          <!-- ✅ BOTONES DE ACCIÓN REDISEÑADOS -->
          <div class="contact-actions">
            <a 
              v-if="business.whatsapp"
              :href="`https://wa.me/591${business.whatsapp}`"
              target="_blank"
              class="btn-whatsapp"
            >
              <va-icon name="phone" />
              Contactar por WhatsApp
            </a>
            
            <a 
              v-if="business.email"
              :href="`mailto:${business.email}`"
              class="btn-email"
            >
              <va-icon name="email" />
              Enviar Email
            </a>

            <a 
              v-if="business.website"
              :href="business.website"
              target="_blank"
              class="btn-website"
            >
              <va-icon name="public" />
              Visitar Sitio Web
            </a>

            <button class="btn-share" @click="compartirNegocio">
              <va-icon name="share" />
              Compartir
            </button>
          </div>
        </div>

        <!-- Contenido con Tabs -->
        <div class="content-section">
          <TabNavigation
            v-model="activeTab"
            :tabs="tabs"
          >
            <!-- Tab 1: Información -->
            <template #tab-0>
              <div class="tab-content">
                <!-- Descripción -->
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="description" size="1.5rem" color="purple" />
                    Sobre el negocio
                  </h3>
                  <p class="block-text">{{ business.description }}</p>
                </div>

                <!-- Información general -->
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="info" size="1.5rem" color="purple" />
                    Información general
                  </h3>
                  <div class="info-grid-detailed">
                    <!-- Horarios -->
                    <div class="info-item-detailed">
                      <div class="info-icon">
                        <va-icon name="schedule" size="1.5rem" />
                      </div>
                      <div class="info-content">
                        <div class="info-label">Horarios de atención</div>
                        <div class="info-value">{{ business.schedule || 'No especificado' }}</div>
                      </div>
                    </div>

                    <!-- Categoría -->
                    <div class="info-item-detailed">
                      <div class="info-icon">
                        <va-icon name="category" size="1.5rem" />
                      </div>
                      <div class="info-content">
                        <div class="info-label">Categoría</div>
                        <div class="info-value">{{ business.category }}</div>
                      </div>
                    </div>

                    <!-- Ubicación -->
                    <div class="info-item-detailed">
                      <div class="info-icon">
                        <va-icon name="place" size="1.5rem" />
                      </div>
                      <div class="info-content">
                        <div class="info-label">Ubicación</div>
                        <div class="info-value">{{ business.city }}, Bolivia</div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Características destacadas -->
                <div v-if="business.features && business.features.length > 0" class="content-block">
                  <h3 class="block-title">
                    <va-icon name="star" size="1.5rem" color="purple" />
                    Características destacadas
                  </h3>
                  <ul class="features-list">
                    <li 
                      v-for="(feature, index) in business.features" 
                      :key="index"
                    >
                      <va-icon name="check_circle" size="small" color="success" />
                      {{ feature }}
                    </li>
                  </ul>
                </div>
              </div>
            </template>

            <!-- Tab 2: Productos/Servicios -->
            <template #tab-1>
              <div class="tab-content">
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="inventory" size="1.5rem" color="purple" />
                    Productos y Servicios
                  </h3>
                  
                  <div v-if="business.products && business.products.length > 0" class="products-grid">
                    <div v-for="product in business.products" :key="product.id" class="product-card">
                      <div v-if="product.image" class="product-image">
                        <img :src="product.image" :alt="product.name" />
                      </div>
                      <div v-else class="product-image-placeholder">
                        <va-icon name="inventory" size="3rem" color="#999" />
                      </div>
                      <div class="product-info">
                        <h4 class="product-name">{{ product.name }}</h4>
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
            </template>

            <!-- Tab 3: Ubicación -->
            <template #tab-2>
              <div class="tab-content">
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="place" size="1.5rem" color="purple" />
                    Ubicación
                  </h3>
                  
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
            </template>

            <!-- Tab 4: Reseñas -->
            <template #tab-3>
              <div class="tab-content">
                <RatingSystem
                  entity-type="business"
                  :entity-id="business.id"
                  :entity-title="business.name"
                />
              </div>
            </template>
          </TabNavigation>
        </div>

      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vuestic-ui'
import MainLayout from '@/components/Layout/MainLayout.vue'
import TabNavigation from '@/components/Common/TabNavigation.vue'
import MapLocation from '@/components/Publish/MapLocation.vue'
import RatingSystem from '@/components/Rating/RatingSystem.vue'

// ========== COMPOSABLES ==========
const router = useRouter()
const route = useRoute()
const { init: notify } = useToast()

// ========== DATA ==========
const activeTab = ref(0)

const business = ref({
  id: route.params.id || '1',
  name: 'TechSolutions Bolivia',
  category: 'Tecnología y Servicios',
  city: 'La Paz',
  description: 'Empresa especializada en soluciones tecnológicas para pequeñas y medianas empresas. Ofrecemos desarrollo de software, consultoría IT y soporte técnico.',
  logo: 'https://via.placeholder.com/800x800/5C0099/FFFFFF?text=TechSolutions',
  schedule: 'Lunes a Viernes: 8:00 AM - 6:00 PM',
  address: 'Av. Arce 2345, Edif. Plaza Torre, Piso 8',
  phone: '22501234',
  whatsapp: '70123456',
  email: 'contacto@techsolutions.bo',
  website: 'https://techsolutions.bo',
  verified: true,
  plan: 'destacado',
  featured: true,
  features: [
    'Consultoría especializada',
    'Soporte técnico 24/7',
    'Desarrollo a medida',
    'Precios competitivos'
  ],
  products: [
    {
      id: 1,
      name: 'Sistema de Gestión Empresarial',
      description: 'Software completo para administrar inventarios, ventas y contabilidad.',
      price: 1500,
      image: 'https://via.placeholder.com/300x200/E0E0E0/666?text=Sistema+ERP'
    },
    {
      id: 2,
      name: 'Página Web Profesional',
      description: 'Diseño y desarrollo de sitios web responsivos y optimizados.',
      price: 800,
      image: 'https://via.placeholder.com/300x200/E0E0E0/666?text=Web+Design'
    },
    {
      id: 3,
      name: 'Soporte Técnico Mensual',
      description: 'Mantenimiento y soporte técnico para todos tus equipos.',
      price: 300
    }
  ]
})

const tabs = ref([
  {
    id: 0,
    label: 'Información',
    icon: 'info'
  },
  {
    id: 1,
    label: 'Productos/Servicios',
    icon: 'inventory'
  },
  {
    id: 2,
    label: 'Ubicación',
    icon: 'place'
  },
  {
    id: 3,
    label: 'Reseñas',
    icon: 'star'
  }
])

// ========== COMPUTED ==========
const businessCoordinates = computed(() => {
  // Coordenadas de La Paz para el ejemplo
  return {
    lat: -16.5000,
    lng: -68.1193
  }
})

// ========== METHODS ==========
const compartirNegocio = () => {
  if (navigator.share) {
    navigator.share({
      title: business.value.name,
      text: `Conoce ${business.value.name} en Guías Púrpuras`,
      url: window.location.href
    })
  } else {
    // Fallback: copiar URL al portapapeles
    navigator.clipboard.writeText(window.location.href)
    notify({
      message: '🔗 Enlace copiado al portapapeles',
      color: 'success'
    })
  }
}

// ========== LIFECYCLE ==========
onMounted(() => {
  // Aquí cargarías los datos del negocio desde la API
  console.log('Cargando negocio ID:', route.params.id)
})
</script>

<style scoped>
/* ========== Variables CSS ========== */
:root {
  --color-purple: #5C0099;
  --color-purple-light: #8B00CC;
  --color-purple-dark: #4A0077;
  --color-purple-darkest: #2D1B69;
  --color-yellow-primary: #FDC500;
  --border-radius: 12px;
  --shadow-light: 0 2px 8px rgba(0,0,0,0.1);
  --shadow-medium: 0 4px 16px rgba(0,0,0,0.15);
}

/* ========== Layout Principal ========== */
.business-detail-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFFFFF 100%);
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
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
  transition: color 0.2s ease;
}

.breadcrumb a:hover {
  color: var(--color-purple-light);
}

.separator {
  color: #999;
}

.current {
  font-weight: 600;
  color: #333;
}

/* ========== Header Card ========== */
.business-header {
  display: grid;
  grid-template-columns: 250px 1fr 300px;
  gap: 2.5rem;
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: var(--shadow-medium);
  margin-bottom: 2rem;
  border: 2px solid rgba(92, 0, 153, 0.1);
  position: relative;
  overflow: hidden;
}

/* ========== Foto de Perfil ========== */
.business-profile-image {
  position: relative;
  width: 250px;
  height: 250px;
  margin: 0 auto;
}

.profile-image-container {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow-medium);
  border: 3px solid rgba(92, 0, 153, 0.15);
  transition: all 0.3s ease;
}

.profile-image-container:hover {
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.2);
  border-color: rgba(92, 0, 153, 0.3);
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #F0F0F0 0%, #E0E0E0 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #CCC;
}

/* ========== Información Principal ========== */
.business-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* ✅ BADGES MEJORADOS */
.badges-row {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.badge-verified,
.badge-destacado,
.badge-premium,
.badge-featured {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge-verified {
  background: #E8F5E9;
  color: #2E7D32;
}

.badge-destacado {
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

.badge-premium {
  background: linear-gradient(135deg, #9C27B0, #7B1FA2);
  color: white;
}

.badge-featured {
  background: linear-gradient(135deg, #FF6B6B, #EE5A6F);
  color: white;
}

.business-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.business-category {
  font-size: 1.25rem;
  color: var(--color-purple);
  font-weight: 500;
  margin: 0 0 1.5rem 0;
}

/* ========== Info Grid ========== */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #F8F8F8;
  border-radius: 8px;
}

.info-label {
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
}

.info-value {
  color: #333;
  font-size: 0.9rem;
  text-align: right;
}

/* ========== Features ========== */
.features-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.features-label {
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
}

.features {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.feature {
  padding: 0.35rem 0.75rem;
  background: rgba(92, 0, 153, 0.1);
  color: var(--color-purple);
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* ✅ BOTONES DE ACCIÓN REDISEÑADOS (COMO RESTAURANTDETAILVIEW) */
.contact-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 300px;
}

.btn-whatsapp,
.btn-email,
.btn-website,
.btn-share {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  border: none;
}

.btn-whatsapp {
  background: #25D366;
  color: white;
}

.btn-whatsapp:hover {
  background: #1EBE5B;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
}

.btn-email {
  background: var(--color-purple);
  color: white;
}

.btn-email:hover {
  background: var(--color-purple-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

.btn-website {
  background: #2196F3;
  color: white;
}

.btn-website:hover {
  background: #1976D2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

.btn-share {
  background: #F5F5F5;
  color: #666;
}

.btn-share:hover {
  background: #E0E0E0;
}

/* ========== Content Section ========== */
.content-section {
  background: white;
  border-radius: 20px;
  box-shadow: var(--shadow-medium);
  padding: 2rem;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.tab-content {
  margin-top: 2rem;
}

.content-block {
  background: #FAFAFA;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  border: 1px solid #E0E0E0;
}

.content-block:last-child {
  margin-bottom: 0;
}

.block-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #E0E0E0;
}

.block-text {
  color: #333;
  line-height: 1.7;
  font-size: 1rem;
  margin: 0;
}

/* ========== Info Grid Detailed ========== */
.info-grid-detailed {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.info-item-detailed {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: var(--shadow-light);
  border: 1px solid #E0E0E0;
  transition: all 0.3s ease;
}

.info-item-detailed:hover {
  box-shadow: var(--shadow-medium);
  border-color: rgba(92, 0, 153, 0.2);
}

.info-icon {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, var(--color-purple), var(--color-purple-light));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.info-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.info-content .info-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.info-content .info-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

/* ========== Features List ========== */
.features-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0 0 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.features-list li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: var(--shadow-light);
  font-size: 1rem;
  color: #333;
}

/* ========== Products Grid ========== */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-light);
  border: 1px solid #E0E0E0;
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-medium);
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
}

.product-image-placeholder {
  width: 100%;
  height: 200px;
  background: #F5F5F5;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #E0E0E0;
}

.product-info {
  padding: 1.5rem;
}

.product-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.75rem 0;
}

.product-description {
  color: #666;
  line-height: 1.6;
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
}

.product-price {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price-label {
  font-size: 0.9rem;
  color: #666;
}

.price-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple);
}

/* ========== Empty Products ========== */
.empty-products {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: #999;
  margin-top: 1.5rem;
}

.empty-products p {
  margin: 1rem 0 0 0;
  font-size: 1.1rem;
}

/* ========== Location ========== */
.location-address-card {
  display: flex;
  gap: 1.25rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFF 100%);
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
  margin: 1.5rem 0;
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
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border: 3px solid rgba(92, 0, 153, 0.15);
  transition: all 0.3s ease;
  margin: 1.5rem 0;
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
  margin: 1.5rem 0;
}

.map-placeholder-simple p {
  margin: 1rem 0 0 0;
  color: #6B7280;
  font-size: 0.95rem;
}

/* ========== Responsive ========== */
@media (max-width: 1024px) {
  .business-header {
    grid-template-columns: 200px 1fr;
    gap: 2rem;
  }

  .business-profile-image {
    width: 200px;
    height: 200px;
  }

  .contact-actions {
    grid-column: 1 / -1;
    flex-direction: row;
    min-width: auto;
    flex-wrap: wrap;
  }

  .info-grid,
  .info-grid-detailed {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .business-detail-section {
    padding: 1.5rem 0;
  }

  .container {
    padding: 0 1rem;
  }

  .business-header {
    grid-template-columns: 1fr;
    padding: 1.5rem;
    gap: 1.5rem;
  }

  .business-profile-image {
    width: 100%;
    height: 250px;
    max-width: 300px;
  }

  .business-title {
    font-size: 1.5rem;
  }

  .business-category {
    font-size: 1rem;
  }

  .contact-actions {
    flex-direction: column;
  }

  .content-section {
    padding: 1.5rem;
  }

  .content-block {
    padding: 1.5rem;
  }

  .block-title {
    font-size: 1.25rem;
  }

  .block-text {
    font-size: 1rem;
  }

  .products-grid {
    grid-template-columns: 1fr;
  }

  .features-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .business-header {
    padding: 1rem;
  }

  .business-profile-image {
    height: 200px;
  }

  .content-section {
    padding: 1rem;
  }

  .content-block {
    padding: 1rem;
  }

  .info-item-detailed {
    padding: 1rem;
  }

  .location-address-card {
    padding: 1rem;
  }
}
</style>