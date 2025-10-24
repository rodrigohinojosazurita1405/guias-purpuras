<!-- frontend/src/components/Guide/ProfessionalCard.vue -->
<template>
  <div class="professional-card" @click="goToDetail">
    <!-- Imagen/Logo -->
    <div class="card-image">
      <img 
        v-if="listing.images && listing.images.length > 0" 
        :src="listing.images[0].url" 
        :alt="listing.title"
      />
      <div v-else class="placeholder-image">
        <va-icon name="person" size="3rem" color="#999" />
      </div>
      
      <!-- Badge destacado -->
      <div v-if="listing.plan === 'premium' || listing.plan === 'destacado'" class="badge-destacado">
        <va-icon name="star" size="small" />
        Destacado
      </div>

      <!-- Badge verificado -->
      <div v-if="listing.verified" class="badge-verified">
        <va-icon name="verified" size="small" />
      </div>
    </div>

    <!-- Contenido -->
    <div class="card-content">
      <!-- Nombre profesional -->
      <h3 class="professional-name">{{ listing.title }}</h3>
      
      <!-- Título profesional -->
      <p class="professional-title">{{ listing.professionalTitle }}</p>
      
      <!-- Rating y experiencia -->
      <div class="meta-info">
        <div class="rating">
          <va-icon name="star" size="small" color="#FFC107" />
          <va-icon name="star" size="small" color="#FFC107" />
          <va-icon name="star" size="small" color="#FFC107" />
          <va-icon name="star" size="small" color="#FFC107" />
          <va-icon name="star" size="small" color="#FFC107" />
          <span class="rating-value">(4.8)</span>
        </div>
        <div class="divider">|</div>
        <div class="experience">
          <va-icon name="work_history" size="small" />
          {{ listing.yearsExperience }} años
        </div>
      </div>

      <!-- Especialidades -->
      <div class="specialties">
        <span 
          v-for="(specialty, index) in listing.specialties.slice(0, 3)" 
          :key="index"
          class="specialty-badge"
        >
          {{ specialty }}
        </span>
        <span v-if="listing.specialties.length > 3" class="more-badge">
          +{{ listing.specialties.length - 3 }}
        </span>
      </div>

      <!-- Ciudad -->
      <div class="location">
        <va-icon name="place" size="small" />
        {{ listing.city }}
      </div>

      <!-- Botón -->
      <button class="view-profile-btn">
        Ver perfil
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
  // ✅ CORREGIDO: Ahora usa /guias/profesionales/
  router.push(`/guias/profesionales/${props.listing.slug}`)
}
</script>

<style scoped>
.professional-card {
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

.professional-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.card-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #F5F5F5;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

.badge-verified {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 32px;
  height: 32px;
  background: rgba(46, 125, 50, 0.95);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

.professional-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
  line-height: 1.3;
}

.professional-title {
  font-size: 1rem;
  color: #666;
  margin: 0;
  line-height: 1.4;
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
  gap: 0.25rem;
}

.rating-value {
  margin-left: 0.25rem;
  font-weight: 600;
  color: #333;
}

.divider {
  color: #E0E0E0;
}

.experience {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.specialties {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.specialty-badge {
  padding: 0.35rem 0.75rem;
  background: rgba(92, 0, 153, 0.1);
  color: var(--color-purple);
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.more-badge {
  padding: 0.35rem 0.75rem;
  background: #F5F5F5;
  color: #666;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.95rem;
}

.view-profile-btn {
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

.view-profile-btn:hover {
  background: var(--color-purple-dark);
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .card-image {
    height: 180px;
  }

  .card-content {
    padding: 1.25rem;
  }

  .professional-name {
    font-size: 1.1rem;
  }

  .professional-title {
    font-size: 0.95rem;
  }
}
</style>