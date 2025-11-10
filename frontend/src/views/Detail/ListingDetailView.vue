<template>
  <!--
  ═══════════════════════════════════════════════════════════
  ListingDetailView.vue - Detalle completo de un anuncio
  ═══════════════════════════════════════════════════════════
  Propósito: Mostrar información detallada de un anuncio
  Componentes: ImageGallery, ContactCard, RelatedListings
  Conexión Django: GET /api/listings/:id/
  Props desde Vue Router: this.$route.params.id
  -->
  
  <MainLayout>
    <!-- ========== Breadcrumb ========== -->
    <section class="breadcrumb-section">
      <div class="breadcrumb-container">
        <div class="breadcrumb">
          <a href="#" @click.prevent="goHome">Inicio</a>
          <VaIcon name="chevron_right" size="small" />
          <a href="#" @click.prevent="goToGuide">{{ listing.guideName }}</a>
          <VaIcon name="chevron_right" size="small" />
          <span class="current">{{ listing.title }}</span>
        </div>
        <button class="back-btn" @click="goBack">
          <VaIcon name="arrow_back" size="small" />
          Volver
        </button>
      </div>
    </section>

    <!-- ========== Contenido Principal ========== -->
    <section class="detail-content">
      <div class="detail-container">
        
        <!-- ========== COLUMNA PRINCIPAL ========== -->
        <div class="main-column">
          
          <!-- Galería de Imágenes -->
          <ImageGallery
            :images="listing.images"
            :plan="listing.plan"
            :verified="listing.verified"
          />
          
          <!-- ========== Título y Metadata ========== -->
          <div class="title-section">
            <span class="category-badge">{{ listing.category }}</span>
            <h1>{{ listing.title }}</h1>
            
            <!-- Info Rápida -->
            <div class="quick-info">
              <div class="info-item">
                <VaIcon name="location_on" color="var(--color-yellow-primary)" />
                <span>{{ listing.location }}</span>
              </div>
              <div class="info-item">
                <VaIcon name="schedule" color="var(--color-gray-500)" />
                <span>Publicado {{ listing.timeAgo }}</span>
              </div>
              <div class="info-item">
                <VaIcon name="visibility" color="var(--color-gray-500)" />
                <span>{{ listing.views }} vistas</span>
              </div>
            </div>
            
            <!-- Rating (si existe) -->
            <div v-if="listing.rating" class="rating-section">
              <div class="stars-large">
                <VaIcon
                  v-for="star in 5"
                  :key="star"
                  :name="star <= listing.rating ? 'star' : 'star_border'"
                  size="large"
                  :color="star <= listing.rating ? 'var(--color-yellow-primary)' : 'var(--color-gray-300)'"
                />
              </div>
              <span class="rating-text">{{ listing.rating }}.0 ({{ listing.reviews }} reseñas)</span>
            </div>
          </div>
          
          <!-- ========== Descripción ========== -->
          <div class="description-section">
            <h2>Descripción</h2>
            <p>{{ listing.description }}</p>
          </div>
          
          <!-- ========== Características (si existen) ========== -->
          <div v-if="listing.features" class="features-section">
            <h2>Características</h2>
            <div class="features-grid">
              <div v-for="feature in listing.features" :key="feature" class="feature-item">
                <VaIcon name="check_circle" color="var(--color-success)" />
                <span>{{ feature }}</span>
              </div>
            </div>
          </div>
          
          <!-- ========== Ubicación ========== -->
          <div class="map-section">
            <h2>Ubicación</h2>
            <div class="map-placeholder">
              <VaIcon name="map" size="60px" color="var(--color-gray-500)" />
              <p>{{ listing.location }}</p>
              <VaButton preset="plain" @click="openInMaps">
                Abrir en Google Maps
              </VaButton>
            </div>
          </div>
          
          <!-- ========== Anuncios Relacionados ========== -->
          <RelatedListings
            :related-listings="relatedListings"
            @listing-click="viewListing"
          />
        </div>

        <!-- ========== SIDEBAR ========== -->
        <aside class="sidebar">
          <ContactCard
            :listing="listing"
            @contact="handleContact"
          />
          
          <!-- Botón Reportar -->
          <button class="report-btn" @click="reportAd">
            <VaIcon name="flag" size="small" />
            Reportar Anuncio
          </button>
        </aside>
        
      </div>
    </section>

    <!-- ========== Modal de Contacto ========== -->
    <VaModal v-model="showContactModal">
      <template #header>
        <h3>Información de Contacto</h3>
      </template>
      <div class="contact-modal-content">
        <div class="contact-info-item">
          <VaIcon name="phone" size="large" color="var(--color-purple-dark)" />
          <div>
            <div class="contact-label">Teléfono</div>
            <div class="contact-value">{{ listing.phone }}</div>
          </div>
        </div>
        <div v-if="listing.email" class="contact-info-item">
          <VaIcon name="email" size="large" color="var(--color-purple-dark)" />
          <div>
            <div class="contact-label">Email</div>
            <div class="contact-value">{{ listing.email }}</div>
          </div>
        </div>
      </div>
      <template #footer>
        <VaButton @click="showContactModal = false">Cerrar</VaButton>
      </template>
    </VaModal>
    
  </MainLayout>
</template>

<script>
/**
 * ═══════════════════════════════════════════════════════════
 * ListingDetailView - Script
 * ═══════════════════════════════════════════════════════════
 */
import MainLayout from '@/components/Layout/MainLayout.vue'
import ImageGallery from '@/components/Gallery/ImageGallery.vue'
import ContactCard from '@/components/Cards/ContactCard.vue'
import RelatedListings from '@/components/Lists/RelatedListings.vue'

export default {
  name: 'ListingDetailView',
  components: {
    MainLayout,
    ImageGallery,
    ContactCard,
    RelatedListings
  },
  
  data() {
    return {
      showContactModal: false,
      
      // ====== DATOS MOCK (1 EJEMPLO) ======
      // TODO: Obtener desde Django API:
      // async fetchListing() {
      //   const id = this.$route.params.id
      //   const response = await axios.get(`/api/listings/${id}/`)
      //   this.listing = response.data
      // }
      listing: {
        id: 1,
        guideName: 'Guías Profesionales',
        category: 'Abogados',
        title: 'Dr. Carlos Mendoza - Abogado Especialista en Derecho Civil',
        description: 'Abogado con más de 15 años de experiencia en casos civiles, penales y familiares. Brindo asesoría legal integral y representación en juicios. Atención personalizada, ética profesional y compromiso con cada caso.',
        images: [
          'https://images.unsplash.com/photo-1556157382-97eda2d62296?w=800',
          'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800',
          'https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=800'
        ],
        location: 'Cochabamba, Zona Centro',
        price: null,
        timeAgo: 'hace 2 horas',
        views: 234,
        plan: 'top',
        verified: true,
        rating: 5,
        reviews: 48,
        sellerName: 'Carlos Mendoza',
        memberSince: 'Enero 2020',
        phone: '+591 4-412-3456',
        email: 'carlos.mendoza@example.com',
        features: [
          'Derecho Civil',
          'Derecho Penal',
          'Derecho de Familia',
          '15 años de experiencia',
          'Consultas presenciales y virtuales'
        ]
      },
      
      // ====== ANUNCIOS RELACIONADOS (3 EJEMPLOS) ======
      // TODO: Obtener desde Django /api/listings/related/:id/
      relatedListings: [
        {
          id: 2,
          title: 'Lic. María Torres - Contadora',
          image: 'https://images.unsplash.com/photo-1554224311-beee2c0c2d98?w=400',
          location: 'Cochabamba',
          price: null
        },
        {
          id: 3,
          title: 'Arq. Roberto Sánchez',
          image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
          location: 'Cochabamba',
          price: null
        },
        {
          id: 4,
          title: 'Dra. Ana Gutiérrez - Médico',
          image: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400',
          location: 'Cochabamba',
          price: 80
        }
      ]
    }
  },
  
  methods: {
    /**
     * Maneja el contacto según el tipo
     * @param {String} type - 'phone' | 'whatsapp' | 'email'
     */
    handleContact(type) {
      if (type === 'phone') {
        this.showContactModal = true
      } else if (type === 'whatsapp') {
        const phone = this.listing.phone.replace(/[^0-9]/g, '')
        window.open(`https://wa.me/${phone}`, '_blank')
      } else if (type === 'email') {
        window.location.href = `mailto:${this.listing.email}`
      }
    },
    
    /**
     * Navega a otro anuncio relacionado
     * TODO: this.$router.push(`/anuncio/${listing.id}`)
     */
    viewListing(listing) {
      console.log('Ver anuncio:', listing.id)
    },
    
    openInMaps() {
      console.log('Abrir en Google Maps')
    },
    
    reportAd() {
      console.log('Reportar anuncio')
    },
    
    goBack() {
      window.history.back()
    },
    
    goHome() {
      console.log('Ir a inicio')
    },
    
    goToGuide() {
      console.log('Ir a guía')
    }
  }
}
</script>

<style scoped>
/**
 * ═══════════════════════════════════════════════════════════
 * Estilos ListingDetailView
 * ═══════════════════════════════════════════════════════════
 */

/* ========== Breadcrumb ========== */
.breadcrumb-section {
  width: 100%;
  background: var(--color-gray-50);
border-bottom: 1px solid var(--color-gray-200);
padding: 1rem 0;
}
.breadcrumb-container {
max-width: 100%;
padding: 0 3rem;
display: flex;
justify-content: space-between;
align-items: center;
}
.breadcrumb {
display: flex;
align-items: center;
gap: 0.5rem;
font-size: 0.9rem;
flex: 1;
overflow: hidden;
}
.breadcrumb a {
color: var(--color-gray-500);
text-decoration: none;
white-space: nowrap;
}
.breadcrumb a:hover {
color: var(--color-purple-dark);
}
.breadcrumb .current {
color: var(--color-purple-dark);
font-weight: 600;
white-space: nowrap;
overflow: hidden;
text-overflow: ellipsis;
}
.back-btn {
display: flex;
align-items: center;
gap: 0.5rem;
padding: 0.5rem 1rem;
background: #ffffff;
border: 2px solid var(--color-gray-200);
border-radius: 8px;
color: var(--color-gray-600);
font-weight: 500;
cursor: pointer;
transition: all 0.3s;
}
.back-btn:hover {
background: var(--color-gray-50);
border-color: var(--color-purple-dark);
color: var(--color-purple-dark);
}
/* ========== Layout Principal ========== */
.detail-content {
width: 100%;
padding: 2rem 0;
background: #ffffff;
}
.detail-container {
max-width: 100%;
padding: 0 3rem;
display: grid;
grid-template-columns: 1fr 400px;
gap: 3rem;
}
/* ========== Columna Principal ========== */
.main-column {
width: 100%;
}
/* ========== Título y Metadata ========== */
.title-section {
margin-bottom: 2rem;
}
.category-badge {
display: inline-block;
padding: 0.5rem 1rem;
background: var(--color-gray-100);
color: var(--color-purple-dark);
font-size: 0.85rem;
font-weight: 600;
border-radius: 20px;
text-transform: uppercase;
margin-bottom: 1rem;
}
.title-section h1 {
font-size: 2.5rem;
font-weight: 800;
color: var(--color-gray-900);
margin: 0 0 1.5rem 0;
line-height: 1.3;
}
.quick-info {
display: flex;
flex-wrap: wrap;
gap: 2rem;
margin-bottom: 1.5rem;
}
.info-item {
display: flex;
align-items: center;
gap: 0.5rem;
color: var(--color-gray-600);
font-size: 0.95rem;
}
.rating-section {
display: flex;
align-items: center;
gap: 1rem;
padding: 1.5rem;
background: var(--color-gray-50);
border-radius: 12px;
}
.stars-large {
display: flex;
gap: 0.25rem;
}
.rating-text {
font-size: 1.5rem;
font-weight: 700;
color: var(--color-gray-900);
}
/* ========== Descripción ========== */
.description-section {
margin-bottom: 3rem;
padding-bottom: 3rem;
border-bottom: 1px solid var(--color-gray-200);
}
.description-section h2,
.features-section h2,
.map-section h2 {
font-size: 1.8rem;
font-weight: 700;
color: var(--color-gray-900);
margin-bottom: 1.5rem;
}
.description-section p {
color: var(--color-gray-600);
font-size: 1.05rem;
line-height: 1.8;
}
/* ========== Características ========== */
.features-section {
margin-bottom: 3rem;
padding-bottom: 3rem;
border-bottom: 1px solid var(--color-gray-200);
}
.features-grid {
display: grid;
grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
gap: 1rem;
}
.feature-item {
display: flex;
align-items: center;
gap: 0.75rem;
padding: 1rem;
background: var(--color-gray-50);
border-radius: 8px;
color: var(--color-gray-600);
font-weight: 500;
}
/* ========== Mapa ========== */
.map-section {
margin-bottom: 3rem;
padding-bottom: 3rem;
border-bottom: 1px solid var(--color-gray-200);
}
.map-placeholder {
width: 100%;
height: 300px;
background: var(--color-gray-50);
border-radius: 12px;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
gap: 1rem;
border: 2px dashed var(--color-gray-300);
}
.map-placeholder p {
color: var(--color-gray-600);
font-weight: 600;
font-size: 1.1rem;
}
/* ========== Sidebar ========== */
.sidebar {
display: flex;
flex-direction: column;
gap: 1.5rem;
}
.report-btn {
display: flex;
align-items: center;
justify-content: center;
gap: 0.5rem;
padding: 0.75rem;
background: transparent;
border: 2px solid var(--color-gray-200);
border-radius: 8px;
color: var(--color-danger);
font-weight: 600;
cursor: pointer;
transition: all 0.3s;
}
.report-btn:hover {
background: var(--color-gray-50);
border-color: var(--color-danger);
}
/* ========== Modal de Contacto ========== */
.contact-modal-content {
padding: 1rem 0;
display: flex;
flex-direction: column;
gap: 1.5rem;
}
.contact-info-item {
display: flex;
align-items: center;
gap: 1rem;
padding: 1rem;
background: var(--color-gray-50);
border-radius: 8px;
}
.contact-label {
font-size: 0.85rem;
color: var(--color-gray-500);
margin-bottom: 0.25rem;
}
.contact-value {
font-size: 1.1rem;
font-weight: 700;
color: var(--color-gray-900);
}
/* ========== Responsive ========== */
@media (max-width: 1024px) {
.detail-container {
grid-template-columns: 1fr;
}
.sidebar {
order: -1;
}
}
@media (max-width: 768px) {
.breadcrumb-container,
.detail-container {
padding: 0 1.5rem;
}
.title-section h1 {
font-size: 1.8rem;
}
.quick-info {
flex-direction: column;
gap: 1rem;
}
.features-grid {
grid-template-columns: 1fr;
}
}
</style>