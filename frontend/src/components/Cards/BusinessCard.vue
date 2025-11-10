<!-- frontend/src/components/Guide/BusinessCard.vue -->
<!-- VERSIÓN SIN ERRORES - CSS LIMPIO Y FUNCIONAL -->
<template>
  <div class="business-card" @click="goToDetail">
    <!-- Imagen/Banner -->
    <div class="card-image">
      <img 
        v-if="business.banner" 
        :src="business.banner" 
        :alt="business.name"
        @error="handleImageError"
      />
      <div v-else class="placeholder-image">
        <va-icon name="business" size="3rem" color="#999" />
      </div>
      
      <!-- Badge Plan -->
      <div v-if="business.plan === 'top'" class="badge-destacado">
        <va-icon name="star" size="small" />
        TOP
      </div>
      <div v-else-if="business.plan === 'destacado'" class="badge-destacado">
        <va-icon name="trending_up" size="small" />
        Destacado
      </div>

      <!-- Badge Verificado -->
      <div v-if="business.verified" class="badge-verified">
        <va-icon name="verified" size="small" />
      </div>
    </div>

    <!-- Contenido -->
    <div class="card-content">
      <!-- Nombre del Negocio -->
      <h3 class="business-name">{{ business.name }}</h3>
      
      <!-- Categoría -->
      <p class="business-category">
        <va-icon name="category" size="small" />
        {{ business.category || 'Negocio' }}
      </p>

      <!-- Descripción corta -->
      <p class="business-description">
        {{ truncatedDescription }}
      </p>

      <!-- Meta información -->
      <div class="meta-info">
        <!-- Ciudad -->
        <div class="meta-item">
          <va-icon name="place" size="small" />
          <span>{{ business.city }}</span>
        </div>

        <!-- Teléfono -->
        <div v-if="business.phone" class="meta-item">
          <va-icon name="phone" size="small" />
          <span>{{ business.phone }}</span>
        </div>
      </div>

      <!-- Tags -->
      <div v-if="business.tags && business.tags.length > 0" class="tags">
        <span 
          v-for="(tag, index) in visibleTags" 
          :key="index"
          class="tag"
        >
          {{ tag }}
        </span>
        <span v-if="business.tags.length > 3" class="tag more-tags">
          +{{ business.tags.length - 3 }}
        </span>
      </div>

      <!-- Features Row -->
      <div class="features-row">
        <div v-if="business.verified" class="feature-item verified">
          <va-icon name="verified" size="small" color="success" />
          <span>Verificado</span>
        </div>
        <div v-if="business.nit" class="feature-item">
          <va-icon name="badge" size="small" />
          <span>NIT: {{ business.nit }}</span>
        </div>
      </div>

      <!-- Botón -->
      <button class="view-business-btn" @click.stop="goToDetail">
        Ver Negocio
        <va-icon name="arrow_forward" size="small" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  business: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const goToDetail = () => {
  router.push(`/guias/negocios/${props.business.slug}`)
}

const handleImageError = (e) => {
  console.warn('Error cargando imagen:', e.target.src)
  // Ocultar imagen rota
  e.target.style.display = 'none'
}

const truncatedDescription = computed(() => {
  const maxLength = 100
  if (!props.business.description) return ''
  if (props.business.description.length <= maxLength) {
    return props.business.description
  }
  return props.business.description.substring(0, maxLength) + '...'
})

const visibleTags = computed(() => {
  return props.business.tags?.slice(0, 3) || []
})
</script>

<style scoped>
/* ========== Card Container ========== */
.business-card {
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

.business-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

/* ========== Image Section ========== */
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

.business-card:hover .card-image img {
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

/* ========== Badges ========== */
.badge-destacado {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #FFD93D;
  color: #1a1a1a;
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

.badge-verified {
  position: absolute;
  top: 12px;
  left: 12px;
  background: #4CAF50;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.4);
  z-index: 2;
}

/* ========== Content Section ========== */
.card-content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

/* ========== Title ========== */
.business-name {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #5C0099;
  line-height: 1.3;
  max-height: 3.3rem;
  overflow: hidden;
}

/* ========== Category ========== */
.business-category {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 500;
}

/* ========== Description ========== */
.business-description {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  max-height: 2.7rem;
  overflow: hidden;
}

/* ========== Meta Info ========== */
.meta-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 0.75rem 0;
  border-top: 1px solid #F0F0F0;
  border-bottom: 1px solid #F0F0F0;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #666;
  font-size: 0.9rem;
}

/* ========== Tags ========== */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.35rem 0.75rem;
  background: rgba(92, 0, 153, 0.08);
  color: #5C0099;
  border-radius: 16px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid rgba(92, 0, 153, 0.15);
  transition: all 0.2s ease;
}

.tag:hover {
  background: rgba(92, 0, 153, 0.12);
  transform: translateY(-1px);
}

.more-tags {
  background: #F5F5F5;
  color: #666;
  border: 1px solid #DDD;
}

/* ========== Features Row ========== */
.features-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.85rem;
  color: #666;
}

.feature-item.verified {
  color: #4CAF50;
  font-weight: 600;
}

/* ========== Button ========== */
.view-business-btn {
  width: 100%;
  margin-top: auto;
  padding: 0.875rem 1.5rem;
  background: #5C0099;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-business-btn:hover {
  background: #7B1FA2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

.view-business-btn:active {
  transform: translateY(0);
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .card-image {
    height: 180px;
  }

  .card-content {
    padding: 1rem;
  }

  .business-name {
    font-size: 1.1rem;
  }

  .business-description {
    font-size: 0.85rem;
  }

  .view-business-btn {
    font-size: 0.95rem;
    padding: 0.75rem 1.25rem;
  }
}
</style>