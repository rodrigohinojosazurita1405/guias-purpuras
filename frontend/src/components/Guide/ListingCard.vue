<!-- frontend/src/components/Guide/ListingCard.vue -->
<template>
  <div 
    @click="goToDetail"
    class="listing-card"
    :class="{ 'is-featured': listing.featured, 'is-top': listing.top }"
  >
    <!-- Badge Premium -->
    <div v-if="listing.top || listing.featured" class="premium-badge">
      <va-icon :name="listing.top ? 'stars' : 'star'" size="small" />
      {{ listing.top ? 'TOP' : 'DESTACADO' }}
    </div>

    <!-- Imagen -->
    <div class="listing-image">
      <img :src="listing.image" :alt="listing.title" />
      
      <!-- Badge de Categoría -->
      <div class="category-badge">
        <va-icon :name="getCategoryIcon(listing.category)" size="small" />
        {{ listing.category }}
      </div>
    </div>

    <!-- Contenido -->
    <div class="listing-content">
      <!-- Título -->
      <h3 class="listing-title">{{ listing.title }}</h3>

      <!-- Descripción -->
      <p class="listing-description">{{ listing.description }}</p>

      <!-- Info -->
      <div class="listing-info">
        <div class="info-item">
          <va-icon name="location_on" size="small" color="purple" />
          <span>{{ listing.city }}</span>
        </div>

        <div v-if="listing.phone" class="info-item">
          <va-icon name="phone" size="small" color="purple" />
          <span>{{ listing.phone }}</span>
        </div>
      </div>

      <!-- Footer -->
      <div class="listing-footer">
        <div class="listing-meta">
          <va-icon name="schedule" size="small" />
          <span>{{ listing.publishedDate }}</span>
        </div>

        <va-button
          @click.stop="goToDetail"
          color="purple"
          size="small"
          class="view-btn"
        >
          Ver detalles
          <va-icon name="arrow_forward" size="small" />
        </va-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

// ==========================================
// PROPS
// ==========================================
const props = defineProps({
  listing: {
    type: Object,
    required: true
  }
})

// ==========================================
// COMPOSABLES
// ==========================================
const router = useRouter()

// ==========================================
// MÉTODOS
// ==========================================
const goToDetail = () => {
  router.push({
    name: 'listing-detail',
    params: { id: props.listing.id }
  })
}

const getCategoryIcon = (category) => {
  const icons = {
    'Profesionales': 'work',
    'Gastronomía': 'restaurant',
    'Trabajos': 'business_center',
    'Servicios': 'build'
  }
  return icons[category] || 'category'
}
</script>

<style scoped>
/* ==========================================
   LISTING CARD
   ========================================== */
.listing-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.listing-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(92, 0, 153, 0.15);
}

/* ==========================================
   PREMIUM STYLES
   ========================================== */
.listing-card.is-top {
  border: 2px solid var(--color-yellow-primary);
  box-shadow: 0 4px 16px rgba(253, 197, 0, 0.3);
}

.listing-card.is-featured {
  border: 2px solid var(--color-purple);
}

.premium-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, #FFB800 100%);
  color: var(--color-purple-darkest);
  padding: 0.4rem 0.75rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.75rem;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* ==========================================
   IMAGEN
   ========================================== */
.listing-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  position: relative;
  background-color: #F5F5F5;
}

.listing-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.listing-card:hover .listing-image img {
  transform: scale(1.05);
}

.category-badge {
  position: absolute;
  bottom: 0.75rem;
  left: 0.75rem;
  background: rgba(92, 0, 153, 0.9);
  backdrop-filter: blur(10px);
  color: white;
  padding: 0.4rem 0.75rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

/* ==========================================
   CONTENIDO
   ========================================== */
.listing-content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

.listing-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.listing-description {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

/* ==========================================
   INFO
   ========================================== */
.listing-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

/* ==========================================
   FOOTER
   ========================================== */
.listing-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid #E0E0E0;
  margin-top: auto;
}

.listing-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #999;
  font-size: 0.85rem;
}

.view-btn {
  font-weight: 600;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
  .listing-image {
    height: 180px;
  }

  .listing-title {
    font-size: 1.1rem;
  }

  .listing-footer {
    flex-direction: column;
    gap: 0.75rem;
    align-items: stretch;
  }

  .view-btn {
    width: 100%;
  }
}
</style>