<!-- frontend/src/components/Guide/BusinessCard.vue -->
<template>
  <div class="business-card" @click="goToDetail">
    <!-- Contenedor principal -->
    <div class="card-body">
      <!-- Badges encima del contenido -->
      <div class="badges-row">
        <div v-if="business.verified" class="badge-verified">
          <va-icon name="verified" size="small" />
          Verificado
        </div>

        <div v-if="business.plan === 'top'" class="badge-destacado">
          <va-icon name="star" size="small" />
          TOP
        </div>
        <div v-else-if="business.plan === 'destacado'" class="badge-destacado">
          <va-icon name="trending_up" size="small" />
          Destacado
        </div>
      </div>

      <!-- Logo cuadrado + Título clickeable -->
      <div class="header-section">
        <div class="logo-square">
          <img 
            v-if="business.banner" 
            :src="business.banner" 
            :alt="business.name"
            @error="handleImageError"
          />
          <va-icon v-else name="business" size="2rem" color="#999" />
        </div>
        
        <div class="header-text">
          <h3 class="business-name">{{ business.name }}</h3>
          <p class="business-category">
            <va-icon name="category" size="small" />
            {{ business.category || 'Negocio' }}
          </p>
        </div>
      </div>

      <!-- Descripción corta -->
      <p class="business-description">
        {{ truncatedDescription }}
      </p>

      <!-- Metadata con iconos -->
      <div class="metadata-grid">
        <div class="meta-item">
          <va-icon name="place" size="small" color="#6B7280" />
          <span>{{ business.city }}</span>
        </div>
        
        <div v-if="business.phone" class="meta-item">
          <va-icon name="phone" size="small" color="#6B7280" />
          <span>{{ business.phone }}</span>
        </div>

        <div v-if="business.nit" class="meta-item">
          <va-icon name="badge" size="small" color="#6B7280" />
          <span>NIT: {{ business.nit }}</span>
        </div>
      </div>

      <!-- Tags hashtag style -->
      <div v-if="business.tags && business.tags.length > 0" class="tags-section">
        <span 
          v-for="(tag, index) in visibleTags" 
          :key="index"
          class="tag-hashtag"
        >
          #{{ tag }}
        </span>
        <span v-if="business.tags.length > 3" class="tag-more">
          +{{ business.tags.length - 3 }}
        </span>
      </div>
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
  e.target.style.display = 'none'
}

const truncatedDescription = computed(() => {
  const maxLength = 80
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
.business-card {
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

.business-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.15);
}

.business-card:hover .business-name {
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

.badge-verified {
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

.business-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
  transition: color 0.3s ease;
}

.business-category {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
  line-height: 1.4;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

/* ========== DESCRIPTION ========== */
.business-description {
  font-size: 0.9375rem;
  color: #6B7280;
  margin: 0;
  line-height: 1.5;
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

/* ========== TAGS HASHTAG STYLE ========== */
.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-hashtag {
  padding: 0.375rem 0.875rem;
  background: rgba(147, 51, 234, 0.08);
  color: #9333EA;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  white-space: nowrap;
}

.tag-more {
  padding: 0.375rem 0.875rem;
  background: #F3F4F6;
  color: #6B7280;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
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

  .business-name {
    font-size: 1.25rem;
  }

  .business-category {
    font-size: 0.9375rem;
  }

  .business-description {
    font-size: 0.875rem;
  }

  .badge-verified,
  .badge-destacado {
    font-size: 0.8125rem;
    padding: 0.3125rem 0.75rem;
  }
}

@media (max-width: 480px) {
  .business-card {
    max-width: 100%;
  }

  .card-body {
    padding: 1rem;
  }

  .business-name {
    font-size: 1.125rem;
  }
}
</style>