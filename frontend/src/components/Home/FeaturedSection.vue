<template>
  <!-- 
    FeaturedSection.vue - Anuncios destacados
    
    Propósito: Mostrar anuncios TOP y Destacados como ejemplo
    Conecta con: HomeView.vue (componente padre)
    Emite: listing-click (cuando se hace clic en un anuncio)
    Datos: Solo 2-3 anuncios de ejemplo, después desde Django
  -->
  <section class="featured-section">
    <div class="section-container">
      <!-- Header -->
      <div class="section-header">
        <div class="section-title-block">
          <h2 class="section-title">Anuncios Destacados</h2>
          <p class="section-subtitle">Los mejores anuncios seleccionados para ti</p>
        </div>
        <VaButton preset="plain" icon-right="arrow_forward" @click="viewAll">
          Ver Todos
        </VaButton>
      </div>

      <!-- Grid de Anuncios (solo 3 de ejemplo) -->
      <div class="listings-grid">
        <div 
          v-for="listing in featuredListings" 
          :key="listing.id"
          class="listing-card"
          @click="handleListingClick(listing)"
        >
          <!-- Imagen -->
          <div class="listing-image">
            <img :src="listing.image" :alt="listing.title" />
            <div class="listing-badges">
              <VaBadge 
                v-if="listing.plan === 'top'" 
                text="TOP" 
                color="danger"
              />
              <VaBadge 
                v-if="listing.plan === 'featured'" 
                text="Destacado" 
                color="warning"
              />
            </div>
            <button class="favorite-btn" @click.stop="toggleFavorite(listing.id)">
              <VaIcon :name="listing.isFavorite ? 'favorite' : 'favorite_border'" />
            </button>
          </div>

          <!-- Contenido -->
          <div class="listing-content">
            <div class="listing-category">
              <VaIcon :name="getCategoryIcon(listing.guide)" size="small" />
              <span>{{ listing.category }}</span>
            </div>

            <h3 class="listing-title">{{ listing.title }}</h3>

            <div class="listing-rating" v-if="listing.rating">
              <div class="stars">
                <VaIcon 
                  v-for="star in 5" 
                  :key="star"
                  :name="star <= listing.rating ? 'star' : 'star_border'"
                  size="small"
                  :color="star <= listing.rating ? 'var(--color-orange-primary)' : 'var(--color-gray-300)'"
                />
              </div>
              <span class="rating-text">({{ listing.reviews }} reseñas)</span>
            </div>

            <div class="listing-meta">
              <div class="meta-item">
                <VaIcon name="location_on" size="small" />
                <span>{{ listing.location }}</span>
              </div>
              <div class="meta-item" v-if="listing.price">
                <VaIcon name="attach_money" size="small" />
                <span>{{ formatPrice(listing.price) }}</span>
              </div>
              <div class="meta-item">
                <VaIcon name="schedule" size="small" />
                <span>{{ listing.timeAgo }}</span>
              </div>
            </div>

            <div class="listing-footer">
              <div class="listing-views">
                <VaIcon name="visibility" size="small" />
                <span>{{ listing.views }} vistas</span>
              </div>
              <VaButton size="small" color="var(--color-purple-dark)" @click.stop="contactListing(listing)">
                Contactar
              </VaButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
/**
 * FeaturedSection Component
 * 
 * Props: Ninguno (datos locales mínimos)
 * 
 * Emits:
 * - listing-click: { listing } cuando se hace clic en un anuncio
 * 
 * State:
 * - featuredListings: array con SOLO 3 anuncios de ejemplo
 * 
 * TODO: 
 * - Obtener anuncios destacados desde Django API /api/listings/featured/
 * - Implementar sistema de favoritos con backend
 */

export default {
  name: 'FeaturedSection',
  emits: ['listing-click'],
  data() {
    return {
      // SOLO 3 anuncios de ejemplo (no más)
      // TODO: Reemplazar con datos desde Django /api/listings/featured/
      featuredListings: [
        {
          id: 1,
          guide: 'profesionales',
          category: 'Abogados',
          title: 'Dr. Carlos Mendoza - Abogado Especialista',
          image: 'https://images.unsplash.com/photo-1556157382-97eda2d62296?w=500',
          location: 'Cochabamba, Centro',
          price: null,
          timeAgo: 'Hace 2 horas',
          plan: 'top',
          rating: 5,
          reviews: 48,
          views: 234,
          isFavorite: false
        },
        {
          id: 2,
          guide: 'gastronomicas',
          category: 'Restaurantes',
          title: 'Restaurante El Fogón - Comida Típica',
          image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500',
          location: 'La Paz, Sopocachi',
          price: 50,
          timeAgo: 'Hace 5 horas',
          plan: 'featured',
          rating: 4,
          reviews: 125,
          views: 567,
          isFavorite: false
        },
        {
          id: 3,
          guide: 'trabajos',
          category: 'Tecnología',
          title: 'Desarrollador Full Stack - Remoto',
          image: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=500',
          location: 'Santa Cruz (Remoto)',
          price: 7000,
          timeAgo: 'Hace 1 día',
          plan: 'top',
          rating: null,
          reviews: 0,
          views: 892,
          isFavorite: false
        }
      ]
    }
  },
  methods: {
    getCategoryIcon(guide) {
      const icons = {
        profesionales: 'business_center',
        gastronomicas: 'restaurant',
        trabajos: 'work',
        servicios: 'build'
      }
      return icons[guide] || 'category'
    },
    
    formatPrice(price) {
      if (!price) return 'Consultar'
      return `Bs. ${price.toLocaleString()}`
    },
    
    handleListingClick(listing) {
      this.$emit('listing-click', listing)
      console.log('Ver anuncio:', listing.id)
      // TODO: Redirigir a /anuncio/:id
    },
    
    toggleFavorite(id) {
      const listing = this.featuredListings.find(l => l.id === id)
      if (listing) {
        listing.isFavorite = !listing.isFavorite
        // TODO: Guardar en Django API /api/favorites/toggle/
      }
    },
    
    contactListing(listing) {
      console.log('Contactar:', listing.id)
      // TODO: Mostrar modal de contacto o redirigir
    },
    
    viewAll() {
      console.log('Ver todos los anuncios')
      // TODO: Redirigir a página de listados
    }
  }
}
</script>

<style scoped>
/**
 * Estilos de Featured Section
 * Cards de anuncios con imágenes y metadata
 */

.featured-section {
  width: 100%;
  padding: 6rem 3rem;
  background: #ffffff;
}

.section-container {
  max-width: 100%;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
}

.section-title-block {
  text-align: left;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 0.5rem;
}

.section-subtitle {
  font-size: 1.1rem;
  color: var(--color-gray-500);
}

/* Listings Grid */
.listings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 2rem;
}

.listing-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid var(--color-gray-100);
}

.listing-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
  border-color: var(--color-purple-dark);
}

.listing-image {
  position: relative;
  width: 100%;
  height: 240px;
  overflow: hidden;
  background: var(--color-gray-200);
}

.listing-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.listing-card:hover .listing-image img {
  transform: scale(1.1);
}

.listing-badges {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 10;
}

.favorite-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 40px;
  height: 40px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 50%;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.favorite-btn:hover {
  background: var(--color-danger);
  transform: scale(1.1);
}

.listing-content {
  padding: 1.5rem;
}

.listing-category {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-purple-dark);
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
}

.listing-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin: 0 0 1rem 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.listing-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.stars {
  display: flex;
  gap: 0.125rem;
}

.rating-text {
  font-size: 0.85rem;
  color: var(--color-gray-500);
}

.listing-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-gray-100);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-gray-500);
  font-size: 0.9rem;
}

.listing-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid var(--color-gray-100);
}

.listing-views {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-gray-400);
  font-size: 0.85rem;
}

/* Responsive */
@media (max-width: 768px) {
  .featured-section {
    padding: 4rem 1.5rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .listings-grid {
    grid-template-columns: 1fr;
  }
}
</style>