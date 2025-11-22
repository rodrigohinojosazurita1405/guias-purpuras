<!-- frontend/src/components/Guide/ProfessionalCard.vue -->
<template>
  <div class="professional-card" @click="goToDetail">
    <!-- Contenedor principal -->
    <div class="card-body">
      <!-- Badges encima del contenido -->
      <div class="badges-row">
        <div v-if="listing.verified" class="badge-verified">
          <va-icon name="verified" size="small" />
          Verificado
        </div>

        <div v-if="listing.plan === 'premium' || listing.plan === 'destacado'" class="badge-destacado">
          <va-icon name="star" size="small" />
          Destacado
        </div>
      </div>

      <!-- Logo circular pequeño + Título clickeable -->
      <div class="header-section">
        <div class="logo-circle">
          <img 
            v-if="listing.images && listing.images.length > 0" 
            :src="listing.images[0].url" 
            :alt="listing.title"
          />
          <va-icon v-else name="person" size="2rem" color="#999" />
        </div>
        
        <div class="header-text">
          <h3 class="professional-name">{{ listing.title }}</h3>
          <p class="professional-title">{{ listing.professionalTitle }}</p>
        </div>
      </div>

      <!-- Metadata con iconos -->
      <div class="metadata-grid">
        <div class="meta-item">
          <va-icon name="place" size="small" color="#6B7280" />
          <span>{{ listing.city }}</span>
        </div>
        
        <div class="meta-item">
          <va-icon name="work_history" size="small" color="#6B7280" />
          <span>{{ listing.yearsExperience }} años de experiencia</span>
        </div>
      </div>

      <!-- Rating -->
      <div class="rating-section">
        <div class="stars">
          <va-icon name="star" size="small" color="#FDC500" />
          <va-icon name="star" size="small" color="#FDC500" />
          <va-icon name="star" size="small" color="#FDC500" />
          <va-icon name="star" size="small" color="#FDC500" />
          <va-icon name="star" size="small" color="#FDC500" />
        </div>
        <span class="rating-value">(4.8)</span>
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
  router.push(`/guias/profesionales/${props.listing.slug}`)
}
</script>

<style scoped>
.professional-card {
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

.professional-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.15);
}

.professional-card:hover .professional-name {
  color: var(--color-purple);
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

/* ========== BODY ========== */
.card-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* ========== HEADER SECTION ========== */
.header-section {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.logo-circle {
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

.logo-circle img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.header-text {
  flex: 1;
  min-width: 0;
}

.professional-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
  transition: color 0.3s ease;
}

.professional-title {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
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

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .card-body {
    padding: 1.25rem;
  }

  .logo-circle {
    width: 70px;
    height: 70px;
    min-width: 70px;
  }

  .professional-name {
    font-size: 1.25rem;
  }

  .professional-title {
    font-size: 0.9375rem;
  }

  .badge-destacado {
    font-size: 0.8125rem;
    padding: 0.3125rem 0.75rem;
  }

  .badge-verified {
    width: 32px;
    height: 32px;
  }
}

@media (max-width: 480px) {
  .professional-card {
    max-width: 100%;
  }

  .card-body {
    padding: 1rem;
  }

  .professional-name {
    font-size: 1.125rem;
  }
}
</style>