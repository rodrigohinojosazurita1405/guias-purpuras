<!-- frontend/src/views/ProfessionalDetailView.vue -->
<template>
  <MainLayout>
    <section class="professional-detail-section">
      <div class="container">
        <!-- Breadcrumb -->
        <nav class="breadcrumb">
          <router-link to="/">Inicio</router-link>
          <span class="separator">/</span>
          <router-link to="/profesionales">Profesionales</router-link>
          <span class="separator">/</span>
          <span class="current">{{ professional.title }}</span>
        </nav>

        <!-- Header Card -->
        <div class="professional-header">
          <!-- Imagen de perfil -->
          <div class="professional-image">
            <img 
              v-if="professional.imageUrl" 
              :src="professional.imageUrl" 
              :alt="professional.title"
              class="profile-image"
            />
            <div v-else class="placeholder-image">
              <va-icon name="person" size="5rem" color="#999" />
            </div>
          </div>

          <!-- Info principal -->
          <div class="professional-info">
            <div class="badges-row">
              <div v-if="professional.verified" class="badge-verified">
                <va-icon name="verified" size="small" />
                Verificado
              </div>
              <div v-if="professional.plan === 'destacado'" class="badge-destacado">
                <va-icon name="star" size="small" />
                Destacado
              </div>
            </div>

            <h1 class="professional-name">{{ professional.title }}</h1>
            <p class="professional-title">{{ professional.professionalTitle }}</p>

            <!-- ✅ Rating y experiencia CON SISTEMA DINÁMICO -->
            <div class="meta-row">
              <div class="rating-stars">
                <RatingStars :rating="averageRating" :size="'small'" />
                <span class="rating-value">({{ averageRating.toFixed(1) }})</span>
                <span v-if="totalReviews > 0" class="reviews-count">
                  · {{ totalReviews }} {{ totalReviews === 1 ? 'reseña' : 'reseñas' }}
                </span>
              </div>
              <div class="divider">|</div>
              <div class="experience">
                <va-icon name="work_history" size="small" />
                {{ professional.yearsExperience }} años de experiencia
              </div>
            </div>

            <!-- Especialidades -->
            <div class="specialties-row">
              <span 
                v-for="(specialty, index) in professional.specialties" 
                :key="index"
                class="specialty-badge"
              >
                {{ specialty }}
              </span>
            </div>

            <!-- Ubicación -->
            <div class="location-row">
              <va-icon name="place" size="small" />
              {{ professional.city }}, Bolivia
            </div>
          </div>

          <!-- Botones de contacto -->
          <div class="contact-actions">
            <a 
              :href="`https://wa.me/591${professional.whatsapp}`"
              target="_blank"
              class="btn-whatsapp"
            >
              <va-icon name="phone" />
              Contactar por WhatsApp
            </a>
            
            <a 
              v-if="professional.email"
              :href="`mailto:${professional.email}`"
              class="btn-email"
            >
              <va-icon name="email" />
              Enviar Email
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
            <!-- Tab 1: Servicios -->
            <template #tab-0>
              <div class="tab-content">
                <!-- Descripción -->
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="description" size="1.5rem" color="purple" />
                    Descripción de servicios
                  </h3>
                  <p class="block-text">{{ professional.services }}</p>
                </div>

                <!-- ¿Por qué elegirme? -->
                <div v-if="professional.whyChooseMe" class="content-block highlight-block">
                  <h3 class="block-title">
                    <va-icon name="thumb_up" size="1.5rem" color="purple" />
                    ¿Por qué elegirme?
                  </h3>
                  <p class="block-text">{{ professional.whyChooseMe }}</p>
                </div>

                <!-- Detalles -->
                <div class="content-block">
                  <div class="details-grid">
                    <!-- Idiomas -->
                    <div class="detail-item">
                      <div class="detail-label">
                        <va-icon name="language" size="small" />
                        Idiomas
                      </div>
                      <div class="detail-value">
                        {{ professional.languages.join(', ') }}
                      </div>
                    </div>

                    <!-- Tarifa -->
                    <div class="detail-item">
                      <div class="detail-label">
                        <va-icon name="payments" size="small" />
                        Tarifa
                      </div>
                      <div class="detail-value">
                        <span v-if="professional.priceType === 'desde'">
                          Desde Bs. {{ professional.price }}
                        </span>
                        <span v-else>A consultar</span>
                      </div>
                    </div>

                    <!-- Horario -->
                    <div class="detail-item" v-if="professional.schedule">
                      <div class="detail-label">
                        <va-icon name="schedule" size="small" />
                        Horario
                      </div>
                      <div class="detail-value">
                        {{ professional.schedule }}
                      </div>
                    </div>

                    <!-- Ubicación -->
                    <div class="detail-item">
                      <div class="detail-label">
                        <va-icon name="place" size="small" />
                        Ubicación
                      </div>
                      <div class="detail-value">
                        {{ professional.city }}, Bolivia
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <!-- Tab 2: Experiencia -->
            <template #tab-1>
              <div class="tab-content">
                <!-- Años de experiencia -->
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="trending_up" size="1.5rem" color="purple" />
                    Experiencia profesional
                  </h3>
                  <div class="experience-highlight">
                    <div class="experience-number">{{ professional.yearsExperience }}</div>
                    <div class="experience-label">años de experiencia</div>
                  </div>
                </div>

                <!-- Logros destacados -->
                <div v-if="professional.successCases" class="content-block highlight-block">
                  <h3 class="block-title">
                    <va-icon name="emoji_events" size="1.5rem" color="purple" />
                    Logros destacados
                  </h3>
                  <p class="block-text">{{ professional.successCases }}</p>
                </div>

                <!-- Especialidades -->
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="category" size="1.5rem" color="purple" />
                    Especialidades
                  </h3>
                  <ul class="specialties-list">
                    <li 
                      v-for="(specialty, index) in professional.specialties" 
                      :key="index"
                    >
                      <va-icon name="check_circle" size="small" color="success" />
                      {{ specialty }}
                    </li>
                  </ul>
                </div>
              </div>
            </template>

            <!-- Tab 3: Contacto -->
            <template #tab-2>
              <div class="tab-content">
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="contact_mail" size="1.5rem" color="purple" />
                    Información de contacto
                  </h3>

                  <div class="contact-grid">
                    <!-- WhatsApp -->
                    <div class="contact-item">
                      <div class="contact-icon whatsapp">
                        <va-icon name="phone" size="1.5rem" />
                      </div>
                      <div class="contact-info">
                        <div class="contact-label">WhatsApp</div>
                        <div class="contact-value">+591 {{ professional.whatsapp }}</div>
                        <a 
                          :href="`https://wa.me/591${professional.whatsapp}`"
                          target="_blank"
                          class="contact-link"
                        >
                          Enviar mensaje →
                        </a>
                      </div>
                    </div>

                    <!-- Email -->
                    <div v-if="professional.email" class="contact-item">
                      <div class="contact-icon email">
                        <va-icon name="email" size="1.5rem" />
                      </div>
                      <div class="contact-info">
                        <div class="contact-label">Email</div>
                        <div class="contact-value">{{ professional.email }}</div>
                        <a 
                          :href="`mailto:${professional.email}`"
                          class="contact-link"
                        >
                          Enviar correo →
                        </a>
                      </div>
                    </div>

                    <!-- Sitio web -->
                    <div v-if="professional.website" class="contact-item">
                      <div class="contact-icon website">
                        <va-icon name="public" size="1.5rem" />
                      </div>
                      <div class="contact-info">
                        <div class="contact-label">Sitio web</div>
                        <div class="contact-value">{{ professional.website }}</div>
                        <a 
                          :href="professional.website"
                          target="_blank"
                          class="contact-link"
                        >
                          Visitar sitio →
                        </a>
                      </div>
                    </div>

                    <!-- Ubicación -->
                    <div class="contact-item">
                      <div class="contact-icon location">
                        <va-icon name="place" size="1.5rem" />
                      </div>
                      <div class="contact-info">
                        <div class="contact-label">Ubicación</div>
                        <div class="contact-value">{{ professional.city }}, Bolivia</div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Ubicación con mapa -->
                <div class="content-block location-map-section">
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
                      <p class="address-main">{{ professional.gpsAddress || professional.city }}</p>
                      <p class="address-city">{{ professional.city }}, Bolivia</p>
                    </div>
                  </div>
                  
                  <!-- Mapa elegante -->
                  <div v-if="professionalCoordinates" class="map-wrapper-elegant">
                    <MapLocation
                      :coordinates="professionalCoordinates"
                      :address="professional.gpsAddress || `${professional.city}, Bolivia`"
                      :title="professional.title"
                      :zoom="16"
                      :height="'400px'"
                      :hide-header="true"
                    />
                  </div>
                  <div v-else class="map-placeholder-simple">
                    <va-icon name="map" size="4rem" color="#D1D5DB" />
                    <p>Ubicación no disponible</p>
                  </div>
                </div>

                <!-- CTA final -->
                <div class="content-block cta-block">
                  <h3>¿Listo para contactar?</h3>
                  <p>Obtén una respuesta rápida contactando directamente</p>
                  <a 
                    :href="`https://wa.me/591${professional.whatsapp}`"
                    target="_blank"
                    class="cta-button"
                  >
                    <va-icon name="phone" />
                    Contactar por WhatsApp
                  </a>
                </div>
              </div>
            </template>

            <!-- ✅ TAB 4: RESEÑAS (NUEVO) -->
            <template #tab-3>
              <div class="tab-content">
                <RatingSystem
                  entity-type="professional"
                  :entity-id="professionalId"
                  :entity-title="professional.title"
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
import { useRoute } from 'vue-router'
import MainLayout from '@/components/Layout/MainLayout.vue'
import TabNavigation from '@/components/Common/TabNavigation.vue'
import MapLocation from '@/components/Publish/MapLocation.vue'

// ✅ IMPORTS DEL RATING SYSTEM
import RatingSystem from '@/components/Rating/RatingSystem.vue'
import RatingStars from '@/components/Rating/RatingStars.vue'
import { useRating } from '@/composables/useRating'

const route = useRoute()
const activeTab = ref(0)

// Mock data (reemplazar con API)
const professional = ref({
  id: 1,
  slug: 'juan-perez-abogado',
  title: 'Dr. Juan Pérez',
  professionalTitle: 'Abogado especializado en derecho civil y familiar',
  imageUrl: 'https://via.placeholder.com/250x250/5C0099/FFFFFF?text=Dr.+Juan+P%C3%A9rez',
  yearsExperience: 15,
  specialties: ['Derecho Civil', 'Derecho Familiar', 'Mediación', 'Contratos'],
  services: 'Ofrezco asesoría legal especializada en casos de derecho civil y familiar. Mi enfoque es personalizado, buscando siempre la mejor solución para cada cliente. Cuento con amplia experiencia en mediación y resolución de conflictos. Trabajo con transparencia, honestidad y compromiso total con mis clientes.',
  successCases: '+200 casos ganados en los últimos 5 años. Reconocido por el Colegio de Abogados de Cochabamba. Especialista en casos complejos de herencias y divorcios. 98% de clientes satisfechos.',
  whyChooseMe: 'Atención personalizada 24/7. Primera consulta completamente gratis. Planes de pago flexibles adaptados a tu situación. Experiencia comprobada con casos reales. Compromiso total con la defensa de tus derechos.',
  languages: ['Español', 'Inglés'],
  priceType: 'desde',
  price: 500,
  schedule: 'Lun-Vie 9:00-18:00, Sáb 9:00-13:00',
  whatsapp: '71234567',
  email: 'juan.perez@abogado.com',
  website: 'https://juanperezabogado.com',
  city: 'Cochabamba',
  verified: true,
  coordinates: '-17.3895, -66.1568',
  gpsAddress: 'Av. Papa Paulo 123, Cochabamba, Bolivia',
  socialMedia: {
    facebook: 'https://facebook.com/juanperezabogado',
    instagram: 'https://instagram.com/juanperezabogado',
    linkedin: 'https://linkedin.com/in/juanperez',
    twitter: 'https://twitter.com/juanperezabo'
  },
  plan: 'destacado'
})

// ✅ COMPUTED: ID del profesional
const professionalId = computed(() => {
  return professional.value.id || 1
})

// ✅ INICIALIZAR RATING SYSTEM
const {
  averageRating,
  totalReviews,
  reviews,
  isLoading: ratingsLoading
} = useRating('professional', professionalId)

// ✅ TABS CON NUEVO TAB DE RESEÑAS
const tabs = [
  { label: 'Servicios', icon: 'description' },
  { label: 'Experiencia', icon: 'work_history' },
  { label: 'Contacto', icon: 'contact_mail' },
  { label: 'Reseñas', icon: 'star' } // ← NUEVO
]

// Convertir coordenadas de string a objeto { lat, lng }
const professionalCoordinates = computed(() => {
  if (professional.value?.coordinates) {
    const coords = professional.value.coordinates.replace(/ /g, '').split(',')
    if (coords.length === 2) {
      return {
        lat: parseFloat(coords[0]),
        lng: parseFloat(coords[1])
      }
    }
  }
  return null
})

const fetchProfessional = async () => {
  const slug = route.params.slug
  
  try {
    // TODO: Reemplazar con llamada real a la API
    // const response = await fetch(`/api/professionals/${slug}/`)
    // professional.value = await response.json()
    
    console.log('Cargando profesional:', slug)
  } catch (error) {
    console.error('Error cargando profesional:', error)
  }
}

onMounted(() => {
  fetchProfessional()
})
</script>

<style scoped>
<style scoped>
.professional-detail-section {
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
.professional-header {
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

.professional-image {
  width: 250px;
  height: 250px;
  border-radius: 12px;
  overflow: hidden;
  background: #F5F5F5;
  position: relative;
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
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
}

.professional-info {
  flex: 1;
}

.badges-row {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.badge-verified,
.badge-destacado {
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

.professional-name {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.professional-title {
  font-size: 1.125rem;
  color: #666;
  margin: 0 0 1rem 0;
  line-height: 1.4;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.95rem;
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

.experience {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
}

.specialties-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.specialty-badge {
  padding: 0.5rem 1rem;
  background: rgba(92, 0, 153, 0.1);
  color: var(--color-purple);
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
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

.highlight-block {
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.05) 0%, rgba(253, 197, 0, 0.05) 100%);
  border-left: 4px solid var(--color-purple);
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

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #666;
}

.detail-value {
  font-size: 1.05rem;
  color: #333;
  font-weight: 600;
}

.experience-highlight {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 0.5rem;
  padding: 2rem;
}

.experience-number {
  font-size: 4rem;
  font-weight: 800;
  color: var(--color-purple);
}

.experience-label {
  font-size: 1.25rem;
  color: #666;
}

.specialties-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.specialties-list li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.05rem;
  color: #333;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.contact-item {
  display: flex;
  gap: 1.5rem;
  align-items: start;
}

.contact-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.contact-icon.whatsapp {
  background: #25D366;
}

.contact-icon.email {
  background: var(--color-purple);
}

.contact-icon.website {
  background: #2196F3;
}

.contact-icon.location {
  background: #FF5722;
}

.contact-info {
  flex: 1;
}

.contact-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.35rem;
}

.contact-value {
  font-size: 1.05rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.contact-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  color: var(--color-purple);
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 600;
}

.contact-link:hover {
  text-decoration: underline;
}

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
  .professional-header {
    grid-template-columns: 200px 1fr;
    gap: 2rem;
  }

  .professional-image-slider {
    width: 200px;
    height: 200px;
  }

  .contact-actions {
    grid-column: 1 / -1;
    flex-direction: row;
    min-width: auto;
  }

  .details-grid,
  .contact-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .professional-detail-section {
    padding: 1.5rem 1rem;
  }

  .professional-header {
    grid-template-columns: 1fr;
    padding: 1.5rem;
    gap: 1.5rem;
  }

  .professional-image-slider {
    width: 100%;
    height: 250px;
    margin: 0 auto;
  }

  .professional-name {
    font-size: 1.5rem;
  }

  .professional-title {
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

  .experience-number {
    font-size: 3rem;
  }

  .cta-block {
    padding: 2rem 1.5rem;
  }

  .cta-block h3 {
    font-size: 1.5rem;
  }
}


/* ====================================
   🎨 SOCIAL MEDIA SECTION
   ==================================== */

.social-media-section {
  background: linear-gradient(135deg, #F8F4FF 0%, #FFF 100%);
  padding: 2rem;
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.social-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.social-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  color: white;
}

.social-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.social-btn svg {
  flex-shrink: 0;
}

.social-btn.facebook {
  background: linear-gradient(135deg, #1877F2, #0C63D4);
}

.social-btn.facebook:hover {
  background: linear-gradient(135deg, #0C63D4, #084FA0);
}

.social-btn.instagram {
  background: linear-gradient(135deg, #E4405F, #C13584, #833AB4);
}

.social-btn.instagram:hover {
  background: linear-gradient(135deg, #C13584, #833AB4, #5B51D8);
}

.social-btn.linkedin {
  background: linear-gradient(135deg, #0A66C2, #004182);
}

.social-btn.linkedin:hover {
  background: linear-gradient(135deg, #004182, #003366);
}

.social-btn.twitter {
  background: linear-gradient(135deg, #000000, #333333);
}

.social-btn.twitter:hover {
  background: linear-gradient(135deg, #333333, #1DA1F2);
}

/* ====================================
   📍 LOCATION MAP SECTION
   ==================================== */

.location-map-section {
  margin-top: 2rem;
}

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
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border: 3px solid rgba(92, 0, 153, 0.15);
  transition: all 0.3s ease;
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
  .social-buttons {
    grid-template-columns: 1fr;
  }
  
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
</style>