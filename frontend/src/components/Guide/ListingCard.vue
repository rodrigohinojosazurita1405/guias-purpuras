<template>
  <!-- 
    ═══════════════════════════════════════════════════════════
    ListingCard.vue - Tarjeta de anuncio
    ═══════════════════════════════════════════════════════════
    
    Propósito: Card reutilizable para mostrar un anuncio
    Props: listing (objeto con datos del anuncio)
    Emits: click (cuando se hace clic en la card)
  -->
  <div class="listing-card" @click="$emit('click', listing)">
    <!-- Imagen -->
    <div class="listing-image">
      <img :src="listing.image" :alt="listing.title" />
      <div class="listing-badges">
        <VaBadge v-if="listing.plan === 'top'" text="TOP" color="danger" />
        <VaBadge v-if="listing.verified" text="Verificado" color="success" />
      </div>
    </div>

    <!-- Contenido -->
    <div class="listing-content">
      <div class="listing-category">{{ listing.category }}</div>
      <h3 class="listing-title">{{ listing.title }}</h3>

      <!-- Rating -->
      <div class="listing-rating" v-if="listing.rating">
        <div class="stars">
          <VaIcon 
            v-for="star in 5" 
            :key="star"
            :name="star <= listing.rating ? 'star' : 'star_border'"
            size="small"
            :color="star <= listing.rating ? 'var(--color-yellow-primary)' : 'var(--color-gray-300)'"
          />
        </div>
        <span>({{ listing.reviews }})</span>
      </div>

      <!-- Metadata -->
      <div class="listing-meta">
        <div class="meta-item">
          <VaIcon name="location_on" size="small" />
          <span>{{ listing.location }}</span>
        </div>
        <div class="meta-item">
          <VaIcon name="schedule" size="small" />
          <span>{{ listing.timeAgo }}</span>
        </div>
      </div>

      <!-- Footer -->
      <div class="listing-footer">
        <span class="views">{{ listing.views }} vistas</span>
        <VaButton size="small" color="var(--color-purple-dark)" @click.stop>
          Ver Detalles
        </VaButton>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * ListingCard Component
 * 
 * Props:
 * - listing: Object con { id, title, image, category, rating, etc. }
 * 
 * Emits:
 * - click: (listing) cuando se hace clic en la card
 */

export default {
  name: 'ListingCard',
  props: {
    listing: {
      type: Object,
      required: true
    }
  },
  emits: ['click']
}
</script>

<style scoped>
.listing-card {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid var(--color-gray-100);
}

.listing-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: var(--color-purple-dark);
}

.listing-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: var(--color-gray-200);
}

.listing-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.listing-badges {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.listing-content {
  padding: 1.5rem;
}

.listing-category {
  color: var(--color-purple-dark);
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
}

.listing-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin: 0 0 0.75rem 0;
  line-height: 1.3;
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
}

.views {
  color: var(--color-gray-400);
  font-size: 0.85rem;
}
</style>