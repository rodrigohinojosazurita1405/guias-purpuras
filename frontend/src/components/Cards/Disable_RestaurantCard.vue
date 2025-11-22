<!-- frontend/src/components/Guide/RestaurantCard.vue -->
<template>
  <div class="restaurant-card" @click="goToDetail">
    <!-- Contenedor principal -->
    <div class="card-body">
      <!-- Badges encima del contenido -->
      <div class="badges-row">
        <div v-if="listing.deliveryAvailable" class="badge-delivery">
          <va-icon name="delivery_dining" size="small" />
          Delivery
        </div>

        <div v-if="listing.plan === 'premium' || listing.plan === 'destacado'" class="badge-destacado">
          <va-icon name="star" size="small" />
          Destacado
        </div>
      </div>

      <!-- Logo cuadrado + Título clickeable -->
      <div class="header-section">
        <div class="logo-square">
          <img 
            v-if="listing.images && listing.images.length > 0" 
            :src="listing.images[0].url" 
            :alt="listing.title"
          />
          <va-icon v-else name="restaurant" size="2rem" color="#999" />
        </div>
        
        <div class="header-text">
          <h3 class="restaurant-name">{{ listing.title }}</h3>
          <p class="restaurant-type">{{ listing.subcategory || 'Restaurante' }}</p>
        </div>
      </div>

      <!-- Metadata con iconos -->
      <div class="metadata-grid">
        <div class="meta-item">
          <va-icon name="place" size="small" color="#6B7280" />
          <span>{{ listing.city }}</span>
        </div>
        
        <div class="meta-item">
          <span class="price-range">
            <span v-if="listing.priceRange === 'economico'">💵</span>
            <span v-else-if="listing.priceRange === 'moderado'">💵💵</span>
            <span v-else-if="listing.priceRange === 'alto'">💵💵💵</span>
            <span v-else>💵💵💵💵</span>
          </span>
        </div>

        <div class="meta-item" v-if="listing.capacity">
          <va-icon name="people" size="small" color="#6B7280" />
          <span>{{ listing.capacity }} personas</span>
        </div>
      </div>

      <!-- Rating -->
      <div class="rating-section">
        <div class="stars">
          <va-icon name="star" size="small" color="#FDC500" />
          <va-icon name="star" size="small" color="#FDC500" />
          <va-icon name="star" size="small" color="#FDC500" />
          <va-icon name="star" size="small" color="#FDC500" />
          <va-icon name="star_half" size="small" color="#FDC500" />
        </div>
        <span class="rating-value">(4.5)</span>
      </div>

      <!-- Menú preview (si tiene platos) -->
      <div v-if="listing.menuItems && listing.menuItems.length > 0" class="menu-preview">
        <div class="menu-preview-header">
          <va-icon name="restaurant_menu" size="small" color="#5C0099" />
          <span>{{ listing.menuItems.length }} platos en el menú</span>
        </div>
        <div class="menu-items-grid">
          <div 
            v-for="(item, index) in listing.menuItems.slice(0, 4)" 
            :key="index"
            class="menu-item-mini"
          >
            <img v-if="item.image" :src="item.image" :alt="item.name" />
            <div v-else class="mini-placeholder">
              <va-icon name="fastfood" size="small" />
            </div>
          </div>
          <div v-if="listing.menuItems.length > 4" class="more-items">
            +{{ listing.menuItems.length - 4 }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  listing: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const goToDetail = () => {
  router.push(`/guias/gastronomia/${props.listing.slug}`)
}
</script>

<style scoped>
.restaurant-card {
  position: relative;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  overflow: hidden;
  max-width: 370px;
  width: 100%;
}

.restaurant-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.15);
}

.restaurant-card:hover .restaurant-name {
  color: var(--color-purple);
}

/* ========== BODY ========== */
.card-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* ========== BADGES ========== */
.badges-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.badge-delivery {
  background: #10B981;
  color: white;
  padding: 0.375rem 0.875rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.badge-destacado {
  background: linear-gradient(135deg, #FDC500, #FFA500);
  color: #5C0099;
  padding: 0.375rem 0.875rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 2px 8px rgba(253, 197, 0, 0.3);
}

/* ========== HEADER SECTION ========== */
.header-section {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.logo-square {
  width: 80px;
  height: 80px;
  min-width: 80px;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F9FAFB;
}

.logo-square img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.header-text {
  flex: 1;
  min-width: 0;
}

.restaurant-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
  transition: color 0.3s ease;
}

.restaurant-type {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
  line-height: 1.4;
}

/* ========== METADATA GRID ========== */
.metadata-grid {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.price-range {
  font-size: 1rem;
  line-height: 1;
}

/* ========== RATING ========== */
.rating-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stars {
  display: flex;
  gap: 0.125rem;
}

.rating-value {
  font-size: 0.875rem;
  font-weight: 700;
  color: #1F2937;
}

/* ========== MENU PREVIEW ========== */
.menu-preview {
  background: #F9FAFB;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
}

.menu-preview-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #5C0099;
  margin-bottom: 0.75rem;
}

.menu-items-grid {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.menu-item-mini {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  border: 2px solid #E5E7EB;
}

.menu-item-mini img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mini-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  color: #9CA3AF;
}

.more-items {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-purple);
  color: white;
  font-size: 0.8125rem;
  font-weight: 700;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .card-body {
    padding: 1.25rem;
  }

  .logo-square {
    width: 70px;
    height: 70px;
    min-width: 70px;
  }

  .restaurant-name {
    font-size: 1.25rem;
  }

  .restaurant-type {
    font-size: 0.9375rem;
  }

  .badge-delivery,
  .badge-destacado {
    font-size: 0.8125rem;
    padding: 0.3125rem 0.75rem;
  }
}

@media (max-width: 480px) {
  .restaurant-card {
    max-width: 100%;
  }

  .card-body {
    padding: 1rem;
  }

  .restaurant-name {
    font-size: 1.125rem;
  }

  .menu-items-grid {
    overflow-x: auto;
    padding-bottom: 0.25rem;
  }
}
</style>