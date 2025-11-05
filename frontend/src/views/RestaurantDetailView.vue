<!-- frontend/src/views/RestaurantDetailView.vue -->
<template>
  <MainLayout>
    <section class="restaurant-detail-section">
      <div class="container">
        <!-- Breadcrumb -->
        <nav class="breadcrumb">
          <router-link to="/">Inicio</router-link>
          <span class="separator">/</span>
          <router-link to="/gastronomia">Gastronomía</router-link>
          <span class="separator">/</span>
          <span class="current">{{ restaurant.title }}</span>
        </nav>

        <!-- Header Card -->
        <div class="restaurant-header">
          <!-- Imagen/Logo -->
          <div class="restaurant-image">
            <img 
              v-if="restaurant.images && restaurant.images.length > 0"
              :src="restaurant.images[0].url"
              :alt="restaurant.title"
            />
            <div v-else class="placeholder-image">
              <va-icon name="restaurant" size="5rem" color="#999" />
            </div>
          </div>

          <!-- Info principal -->
          <div class="restaurant-info">
            <div class="badges-row">
              <div v-if="restaurant.verified" class="badge-verified">
                <va-icon name="verified" size="small" />
                Verificado
              </div>
              <div v-if="restaurant.plan === 'destacado'" class="badge-destacado">
                <va-icon name="star" size="small" />
                Destacado
              </div>
              <div v-if="restaurant.deliveryAvailable" class="badge-delivery">
                <va-icon name="delivery_dining" size="small" />
                Delivery Disponible
              </div>
            </div>

            <h1 class="restaurant-name">{{ restaurant.title }}</h1>
            <p class="restaurant-type">{{ restaurant.subcategory || 'Restaurante' }}</p>

            <!-- Rating y precio -->
            <div class="meta-row">
              <div class="rating-stars">
                <va-icon name="star" size="small" color="#FFC107" />
                <va-icon name="star" size="small" color="#FFC107" />
                <va-icon name="star" size="small" color="#FFC107" />
                <va-icon name="star" size="small" color="#FFC107" />
                <va-icon name="star_half" size="small" color="#FFC107" />
                <span class="rating-value">(4.5)</span>
              </div>
              <div class="divider">|</div>
              <div class="price-info">
                <span class="price-label">Rango de precios:</span>
                <span class="price-range">
                  <span v-if="restaurant.priceRange === 'economico'">💵 Económico</span>
                  <span v-else-if="restaurant.priceRange === 'moderado'">💵💵 Moderado</span>
                  <span v-else-if="restaurant.priceRange === 'alto'">💵💵💵 Alto</span>
                  <span v-else>💵💵💵💵 Premium</span>
                </span>
              </div>
            </div>

            <!-- Features rápidos -->
            <div class="quick-features">
              <div class="feature-chip">
                <va-icon name="schedule" size="small" />
                {{ restaurant.schedule }}
              </div>
              <div class="feature-chip" v-if="restaurant.capacity">
                <va-icon name="people" size="small" />
                {{ restaurant.capacity }} personas
              </div>
              <div class="feature-chip" v-if="restaurant.parking">
                <va-icon name="local_parking" size="small" />
                Estacionamiento
              </div>
            </div>

            <!-- Ubicación -->
            <div class="location-row">
              <va-icon name="place" size="small" />
              {{ restaurant.city }}, Bolivia
            </div>
          </div>

          <!-- Botones de contacto -->
          <div class="contact-actions">
            <a 
              :href="`https://wa.me/591${restaurant.whatsapp}`"
              target="_blank"
              class="btn-whatsapp"
            >
              <va-icon name="phone" />
              Contactar por WhatsApp
            </a>
            
            <a 
              v-if="restaurant.email"
              :href="`mailto:${restaurant.email}`"
              class="btn-email"
            >
              <va-icon name="email" />
              Enviar Email
            </a>

            <a 
              v-if="restaurant.website"
              :href="restaurant.website"
              target="_blank"
              class="btn-website"
            >
              <va-icon name="public" />
              Visitar Sitio Web
            </a>

            <button class="btn-share">
              <va-icon name="share" />
              Compartir
            </button>
          </div>
        </div>

        <!-- Tabs de contenido -->
        <div class="content-section">
          <TabNavigation
            v-model="activeTab"
            :tabs="tabs"
          >
            <!-- Tab 1: Detalle -->
            <template #tab-0>
              <div class="tab-content">
                <!-- Descripción -->
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="description" size="1.5rem" color="purple" />
                    Sobre el restaurante
                  </h3>
                  <p class="block-text">{{ restaurant.description }}</p>
                </div>

                <!-- Información general -->
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="info" size="1.5rem" color="purple" />
                    Información general
                  </h3>
                  <div class="info-grid">
                    <!-- Horarios -->
                    <div class="info-item">
                      <div class="info-icon">
                        <va-icon name="schedule" size="1.5rem" />
                      </div>
                      <div class="info-content">
                        <div class="info-label">Horarios de atención</div>
                        <div class="info-value">{{ restaurant.schedule }}</div>
                      </div>
                    </div>

                    <!-- Capacidad -->
                    <div class="info-item" v-if="restaurant.capacity">
                      <div class="info-icon">
                        <va-icon name="people" size="1.5rem" />
                      </div>
                      <div class="info-content">
                        <div class="info-label">Capacidad</div>
                        <div class="info-value">{{ restaurant.capacity }} personas</div>
                      </div>
                    </div>

                    <!-- Rango de precios -->
                    <div class="info-item">
                      <div class="info-icon">
                        <va-icon name="payments" size="1.5rem" />
                      </div>
                      <div class="info-content">
                        <div class="info-label">Rango de precios</div>
                        <div class="info-value">
                          <span v-if="restaurant.priceRange === 'economico'">Bs. 10 - 30</span>
                          <span v-else-if="restaurant.priceRange === 'moderado'">Bs. 30 - 60</span>
                          <span v-else-if="restaurant.priceRange === 'alto'">Bs. 60 - 100</span>
                          <span v-else>Bs. 100+</span>
                        </div>
                      </div>
                    </div>

                    <!-- Delivery -->
                    <div class="info-item">
                      <div class="info-icon">
                        <va-icon name="delivery_dining" size="1.5rem" />
                      </div>
                      <div class="info-content">
                        <div class="info-label">Servicio de delivery</div>
                        <div class="info-value">
                          <span v-if="restaurant.deliveryAvailable" class="status-yes">
                            <va-icon name="check_circle" size="small" color="success" />
                            Disponible
                          </span>
                          <span v-else class="status-no">
                            <va-icon name="cancel" size="small" color="danger" />
                            No disponible
                          </span>
                        </div>
                      </div>
                    </div>

                    <!-- Estacionamiento -->
                    <div class="info-item">
                      <div class="info-icon">
                        <va-icon name="local_parking" size="1.5rem" />
                      </div>
                      <div class="info-content">
                        <div class="info-label">Estacionamiento</div>
                        <div class="info-value">
                          <span v-if="restaurant.parking" class="status-yes">
                            <va-icon name="check_circle" size="small" color="success" />
                            Disponible
                          </span>
                          <span v-else class="status-no">
                            <va-icon name="cancel" size="small" color="danger" />
                            No disponible
                          </span>
                        </div>
                      </div>
                    </div>

                    <!-- Ubicación -->
                    <div class="info-item">
                      <div class="info-icon">
                        <va-icon name="place" size="1.5rem" />
                      </div>
                      <div class="info-content">
                        <div class="info-label">Ubicación</div>
                        <div class="info-value">{{ restaurant.city }}, Bolivia</div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Características adicionales -->
                <div class="content-block" v-if="restaurant.features && restaurant.features.length > 0">
                  <h3 class="block-title">
                    <va-icon name="verified" size="1.5rem" color="purple" />
                    Características adicionales
                  </h3>
                  <ul class="features-list">
                    <li 
                      v-for="(feature, index) in restaurant.features" 
                      :key="index"
                    >
                      <va-icon name="check_circle" size="small" color="success" />
                      {{ feature }}
                    </li>
                  </ul>
                </div>
              </div>
            </template>

            <!-- Tab 2: Menú -->
            <template #tab-1>
              <div class="tab-content">
                <div class="content-block">
                  <div class="menu-header">
                    <h3 class="block-title">
                      <va-icon name="restaurant_menu" size="1.5rem" color="purple" />
                      Nuestro Menú
                    </h3>
                    <div class="menu-count">
                      {{ restaurant.menuItems.length }} {{ restaurant.menuItems.length === 1 ? 'plato' : 'platos' }}
                    </div>
                  </div>

                  <!-- Grid de platos -->
                  <div v-if="restaurant.menuItems && restaurant.menuItems.length > 0" class="menu-grid">
                    <MenuItemCard
                      v-for="(item, index) in restaurant.menuItems"
                      :key="index"
                      :item="item"
                      :editable="false"
                      :show-view-more="false"
                    />
                  </div>

                  <!-- Estado vacío -->
                  <div v-else class="empty-menu">
                    <va-icon name="restaurant" size="4rem" color="#CCC" />
                    <p>Este restaurante aún no ha agregado su menú</p>
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
                  
                  <!-- Info de ubicación -->
                  <div class="location-info">
                    <div class="location-text">
                      <va-icon name="location_on" size="2rem" color="purple" />
                      <div>
                        <div class="location-name">{{ restaurant.title }}</div>
                        <div class="location-address">
                          {{ restaurant.gpsAddress || `${restaurant.city}, Bolivia` }}
                        </div>
                        <div v-if="restaurant.coordinates" class="location-coords">
                          📍 {{ restaurant.coordinates.lat }}, {{ restaurant.coordinates.lng }}
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Mapa GPS -->
                  <div v-if="restaurant.coordinates" class="map-container">
                    <MapLocation
                      :coordinates="restaurant.coordinates"
                      :address="restaurant.gpsAddress || `${restaurant.city}, Bolivia`"
                      :title="restaurant.title"
                      :zoom="16"
                      readonly
                    />
                  </div>

                  <div v-else class="map-placeholder">
                    <va-icon name="map" size="60px" color="#999" />
                    <p class="map-text">{{ restaurant.city }}</p>
                  </div>

                </div>

                <!-- CTA de contacto -->
                <div class="cta-block">
                  <h3>¿Listo para visitarnos?</h3>
                  <p>Contáctanos para hacer tu reserva o pedir delivery</p>
                  <a 
                    :href="`https://wa.me/591${restaurant.whatsapp}`"
                    target="_blank"
                    class="cta-button"
                  >
                    <va-icon name="phone" />
                    Contactar por WhatsApp
                  </a>
                </div>
              </div>
            </template>
          </TabNavigation>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from '@/components/Layout/MainLayout.vue'
import TabNavigation from '@/components/Common/TabNavigation.vue'
import MenuItemCard from '@/components/Publish/MenuItemCard.vue'
import MapLocation from '@/components/Publish/MapLocation.vue'

const route = useRoute()
const activeTab = ref(0)

const tabs = [
  { label: 'Detalle', icon: 'info' },
  { label: 'Menú', icon: 'restaurant_menu' },
  { label: 'Ubicación', icon: 'place' }
]

// Mock data (reemplazar con API)
const restaurant = ref({
  id: 1,
  slug: 'el-sabor-boliviano',
  title: 'Restaurante El Sabor Boliviano',
  subcategory: 'Comida Tradicional',
  description: 'Restaurante familiar especializado en comida tradicional boliviana. Ofrecemos los mejores platillos típicos de nuestra tierra, preparados con recetas originales y los ingredientes más frescos. Nuestro ambiente acogedor y el servicio de primera te harán sentir como en casa. Ven y disfruta de la auténtica sazón boliviana.',
  priceRange: 'moderado',
  schedule: 'Lun-Dom: 12:00 - 22:00',
  capacity: 80,
  parking: true,
  deliveryAvailable: true,
  whatsapp: '71234567',
  email: 'contacto@elsaborboliviano.com',
  website: 'https://elsaborboliviano.com',
  coordinates: { lat: -17.3935, lng: -66.1570 },
  gpsAddress: 'Av. Heroínas 456, Cochabamba, Bolivia',
  city: 'Cochabamba',
  verified: true,
  plan: 'destacado',
  images: [
    { url: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800' }
  ],
  features: [
    'WiFi Gratis',
    'Aire Acondicionado',
    'Música en vivo los fines de semana',
    'Área para niños',
    'Aceptamos tarjetas'
  ],
  menuItems: [
    {
      name: 'Pique Macho',
      price: 45,
      description: 'Delicioso plato con carne de res, salchicha, papa frita, cebolla, tomate y locoto',
      image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400',
      ingredients: ['Carne de res', 'Papa', 'Salchicha', 'Cebolla', 'Tomate', 'Locoto'],
      tags: ['Picante', 'Especialidad de la casa'],
      featured: true
    },
    {
      name: 'Silpancho',
      price: 35,
      description: 'Carne apanada sobre arroz, papa, huevo frito y ensalada fresca',
      image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400',
      ingredients: ['Carne', 'Arroz', 'Papa', 'Huevo', 'Ensalada'],
      tags: ['Tradicional'],
      featured: false
    },
    {
      name: 'Sajta de Pollo',
      price: 40,
      description: 'Pollo en salsa de ají amarillo con chuño, papa y ensalada',
      image: 'https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400',
      ingredients: ['Pollo', 'Ají amarillo', 'Chuño', 'Papa'],
      tags: ['Picante', 'Más vendido'],
      featured: true
    },
    {
      name: 'Ranga Ranga',
      price: 50,
      description: 'Mondongo en salsa espesa con mote, chuño y papa',
      image: 'https://images.unsplash.com/photo-1547592180-85f173990554?w=400',
      ingredients: ['Mondongo', 'Mote', 'Chuño', 'Papa'],
      tags: ['Tradicional', 'Picante'],
      featured: false
    }
  ]
})

const openInMaps = () => {
  // Si hay coordenadas GPS exactas, usarlas
  if (restaurant.value.coordinates) {
    const { lat, lng } = restaurant.value.coordinates
    window.open(`https://www.google.com/maps/search/?api=1&query=${lat},${lng}`, '_blank')
  } else {
    // Fallback: búsqueda por nombre y ciudad
    const query = encodeURIComponent(`${restaurant.value.title}, ${restaurant.value.city}, Bolivia`)
    window.open(`https://www.google.com/maps/search/?api=1&query=${query}`, '_blank')
  }
}

const fetchRestaurant = async () => {
  const slug = route.params.slug
  
  try {
    // TODO: Reemplazar con llamada real a la API
    // const response = await fetch(`/api/restaurants/${slug}/`)
    // restaurant.value = await response.json()
    
    console.log('Cargando restaurante:', slug)
  } catch (error) {
    console.error('Error cargando restaurante:', error)
  }
}

onMounted(() => {
  fetchRestaurant()
})
</script>

<style scoped>
.restaurant-detail-section {
  min-height: calc(100vh - 200px);
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

.breadcrumb a {
  color: var(--color-purple);
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.breadcrumb .separator {
  color: #999;
}

.breadcrumb .current {
  color: #666;
}

/* Header Card */
.restaurant-header {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  margin-bottom: 2rem;
  display: grid;
  grid-template-columns: 250px 1fr auto;
  gap: 2.5rem;
  align-items: start;
}

.restaurant-image {
  width: 250px;
  height: 250px;
  border-radius: 12px;
  overflow: hidden;
  background: #F5F5F5;
}

.restaurant-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
}

.restaurant-info {
  flex: 1;
}

.badges-row {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.badge-verified,
.badge-destacado,
.badge-delivery {
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

.badge-delivery {
  background: #E8F5E9;
  color: #2E7D32;
}

.restaurant-name {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.restaurant-type {
  font-size: 1.125rem;
  color: #666;
  margin: 0 0 1rem 0;
  font-weight: 500;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  flex-wrap: wrap;
}

.rating-stars {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.rating-value {
  margin-left: 0.35rem;
  font-weight: 600;
  color: #333;
}

.divider {
  color: #E0E0E0;
}

.price-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price-label {
  color: #666;
}

.price-range {
  font-weight: 600;
  color: #333;
}

.quick-features {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.feature-chip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #F5F5F5;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #666;
}

.location-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.95rem;
}

/* Contact Actions */
.contact-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 250px;
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

/* Content Section */
.content-section {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.content-block {
  padding: 2rem;
  background: #FAFAFA;
  border-radius: 12px;
}

.block-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1.5rem 0;
}

.block-text {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #333;
  margin: 0;
}

/* Info Grid */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.info-item {
  display: flex;
  gap: 1rem;
  align-items: start;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  border: 2px solid #F0F0F0;
}

.info-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.1) 0%, rgba(92, 0, 153, 0.05) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-purple);
  flex-shrink: 0;
}

.info-content {
  flex: 1;
}

.info-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.35rem;
}

.info-value {
  font-size: 1.05rem;
  font-weight: 600;
  color: #333;
}

.status-yes,
.status-no {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

/* Features List */
.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.features-list li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.05rem;
  color: #333;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
}

/* Menu */
.menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.menu-count {
  padding: 0.5rem 1rem;
  background: var(--color-purple);
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.empty-menu {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: #999;
}

.empty-menu p {
  margin-top: 1rem;
  font-size: 1.1rem;
}

/* Ubicación */
.location-info {
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.location-text {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.location-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 0.25rem;
}

.location-address {
  font-size: 1rem;
  color: #666;
}
.location-coords {
  font-size: 0.85rem;
  color: #5C0099;
  font-family: monospace;
  margin-top: 0.25rem;
}


.map-container {
  margin: 2rem 0;
}

.map-placeholder {
  width: 100%;
  height: 400px;
  background: white;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  border: 2px dashed #E0E0E0;
  margin-bottom: 1.5rem;
}

.map-text {
  font-size: 1.125rem;
  font-weight: 600;
  color: #666;
  margin: 0;
}

.directions-info {
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
}

.directions-info h4 {
  color: var(--color-purple-darkest);
  margin: 0 0 0.75rem 0;
  font-size: 1.125rem;
}

.directions-info p {
  color: #666;
  margin: 0;
  line-height: 1.6;
}

/* CTA Block */
.cta-block {
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  color: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
}

.cta-block h3 {
  font-size: 1.75rem;
  margin: 0 0 0.5rem 0;
}

.cta-block p {
  font-size: 1.05rem;
  margin: 0 0 2rem 0;
  opacity: 0.9;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1.25rem 2.5rem;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  border-radius: 8px;
  font-size: 1.125rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(253, 197, 0, 0.4);
}

@media (max-width: 1024px) {
  .restaurant-header {
    grid-template-columns: 200px 1fr;
    gap: 2rem;
  }

  .restaurant-image {
    width: 200px;
    height: 200px;
  }

  .contact-actions {
    grid-column: 1 / -1;
    flex-direction: row;
    min-width: auto;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .features-list {
    grid-template-columns: 1fr;
  }

  .menu-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .restaurant-detail-section {
    padding: 1.5rem 1rem;
  }

  .restaurant-header {
    grid-template-columns: 1fr;
    padding: 1.5rem;
    gap: 1.5rem;
  }

  .restaurant-image {
    width: 100%;
    height: 250px;
  }

  .restaurant-name {
    font-size: 1.5rem;
  }

  .restaurant-type {
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

  .menu-grid {
    grid-template-columns: 1fr;
  }

  .map-placeholder {
    height: 300px;
  }

  .cta-block {
    padding: 2rem 1.5rem;
  }

  .cta-block h3 {
    font-size: 1.5rem;
  }
}
</style>