<!-- frontend/src/components/Guide/RestaurantCard.vue -->
<template>
  <div class="restaurant-card" @click="goToDetail">
    <!-- Imagen/Logo -->
    <div class="card-image">
      <img 
        v-if="listing.images && listing.images.length > 0" 
        :src="listing.images[0].url" 
        :alt="listing.title"
      />
      <div v-else class="placeholder-image">
        <va-icon name="restaurant" size="3rem" color="#999" />
      </div>
      
      <!-- Badge destacado -->
      <div v-if="listing.plan === 'premium' || listing.plan === 'destacado'" class="badge-destacado">
        <va-icon name="star" size="small" />
        Destacado
      </div>

      <!-- Badge delivery -->
      <div v-if="listing.deliveryAvailable" class="badge-delivery">
        <va-icon name="delivery_dining" size="small" />
        Delivery
      </div>
    </div>

    <!-- Contenido -->
    <div class="card-content">
      <!-- Nombre del restaurante -->
      <h3 class="restaurant-name">{{ listing.title }}</h3>
      
      <!-- Tipo de cocina -->
      <p class="restaurant-type">{{ listing.subcategory || 'Restaurante' }}</p>
      
      <!-- Rating y rango de precio -->
      <div class="meta-info">
        <div class="rating">
          <va-icon name="star" size="small" color="#FFC107" />
          <va-icon name="star" size="small" color="#FFC107" />
          <va-icon name="star" size="small" color="#FFC107" />
          <va-icon name="star" size="small" color="#FFC107" />
          <va-icon name="star_half" size="small" color="#FFC107" />
          <span class="rating-value">(4.5)</span>
        </div>
        <div class="divider">|</div>
        <div class="price-range">
          <span v-if="listing.priceRange === 'economico'">💵</span>
          <span v-else-if="listing.priceRange === 'moderado'">💵💵</span>
          <span v-else-if="listing.priceRange === 'alto'">💵💵💵</span>
          <span v-else>💵💵💵💵</span>
        </div>
      </div>

      <!-- Características rápidas -->
      <div class="features-row">
        <div class="feature-item" v-if="listing.schedule">
          <va-icon name="schedule" size="small" />
          <span>{{ getSchedulePreview(listing.schedule) }}</span>
        </div>
        <div class="feature-item" v-if="listing.capacity">
          <va-icon name="people" size="small" />
          <span>{{ listing.capacity }} personas</span>
        </div>
        <div class="feature-item" v-if="listing.parking">
          <va-icon name="local_parking" size="small" color="success" />
          <span>Parking</span>
        </div>
      </div>

      <!-- Menú preview (si tiene platos) -->
      <div v-if="listing.menuItems && listing.menuItems.length > 0" class="menu-preview">
        <div class="menu-preview-header">
          <va-icon name="restaurant_menu" size="small" />
          <span>{{ listing.menuItems.length }} platos en el menú</span>
        </div>
        <div class="menu-items-mini">
          <div 
            v-for="(item, index) in listing.menuItems.slice(0, 3)" 
            :key="index"
            class="mini-item"
          >
            <img v-if="item.image" :src="item.image" :alt="item.name" />
            <div v-else class="mini-placeholder">
              <va-icon name="fastfood" size="small" />
            </div>
          </div>
          <div v-if="listing.menuItems.length > 3" class="more-items">
            +{{ listing.menuItems.length - 3 }}
          </div>
        </div>
      </div>

      <!-- Ciudad -->
      <div class="location">
        <va-icon name="place" size="small" />
        {{ listing.city }}
      </div>

      <!-- Botón -->
      <button class="view-menu-btn">
        Ver Menú
        <va-icon name="arrow_forward" size="small" />
      </button>
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

const getSchedulePreview = (schedule) => {
  // Acorta el horario si es muy largo
  if (schedule.length > 20) {
    return schedule.substring(0, 20) + '...'
  }
  return schedule
}
</script>

<style scoped>
.restaurant-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.restaurant-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.card-image {
  position: relative;
  width: 100%;
  height: 220px;
  overflow: hidden;
  background: #F5F5F5;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.restaurant-card:hover .card-image img {
  transform: scale(1.05);
}

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
}

.badge-destacado {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 2;
}

.badge-delivery {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(46, 125, 50, 0.95);
  color: white;
  padding: 0.4rem 0.875rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(4px);
}

.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

.restaurant-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
  line-height: 1.3;
}

.restaurant-type {
  font-size: 0.95rem;
  color: #666;
  margin: 0;
  font-weight: 500;
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  color: #666;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.15rem;
}

.rating-value {
  margin-left: 0.35rem;
  font-weight: 600;
  color: #333;
}

.divider {
  color: #E0E0E0;
}

.price-range {
  font-size: 1.1rem;
}

.features-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-top: 1px solid #F0F0F0;
  border-bottom: 1px solid #F0F0F0;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  color: #666;
}

.menu-preview {
  background: #F8F8F8;
  padding: 0.875rem;
  border-radius: 8px;
}

.menu-preview-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-purple);
  margin-bottom: 0.75rem;
}

.menu-items-mini {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.mini-item {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  border: 2px solid #E0E0E0;
}

.mini-item img {
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
  background: #F0F0F0;
  color: #999;
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
  font-size: 0.75rem;
  font-weight: 700;
}

.location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.95rem;
}

.view-menu-btn {
  margin-top: auto;
  padding: 0.875rem 1.5rem;
  background: var(--color-purple);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.view-menu-btn:hover {
  background: var(--color-purple-dark);
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .card-image {
    height: 200px;
  }

  .card-content {
    padding: 1.25rem;
  }

  .restaurant-name {
    font-size: 1.1rem;
  }

  .restaurant-type {
    font-size: 0.9rem;
  }

  .features-row {
    gap: 0.5rem;
  }

  .feature-item {
    font-size: 0.8rem;
  }
}
</style>