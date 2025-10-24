<!-- frontend/src/components/Guide/JobCard.vue -->
<template>
  <div class="job-card" @click="goToDetail">
    <!-- Logo de la Empresa -->
    <div class="card-logo">
      <img 
        v-if="!listing.confidential && listing.companyLogo" 
        :src="listing.companyLogo" 
        :alt="listing.companyName"
      />
      <div v-else class="placeholder-logo">
        <va-icon 
          :name="listing.confidential ? 'visibility_off' : 'business'" 
          size="2.5rem" 
          color="#999" 
        />
      </div>
      
      <!-- Badge de Publicación Confidencial -->
      <div v-if="listing.confidential" class="badge-confidential">
        <va-icon name="visibility_off" size="small" />
        Confidencial
      </div>

      <!-- Badge Destacado -->
      <div v-else-if="listing.plan === 'destacado' || listing.plan === 'premium'" class="badge-destacado">
        <va-icon name="star" size="small" />
        {{ listing.plan === 'premium' ? 'Premium' : 'Destacado' }}
      </div>
    </div>

    <!-- Contenido -->
    <div class="card-content">
      <!-- Título del Puesto -->
      <h3 class="job-title">{{ listing.title }}</h3>
      
      <!-- Nombre de la Empresa -->
      <p class="company-name">
        <va-icon 
          v-if="listing.verified && !listing.confidential" 
          name="verified" 
          size="small" 
          color="success" 
        />
        {{ getCompanyDisplayName }}
      </p>

      <!-- Meta información -->
      <div class="meta-info">
        <!-- Ciudad -->
        <div class="meta-item">
          <va-icon name="place" size="small" />
          <span>{{ listing.city }}</span>
        </div>

        <!-- Tipo de Contrato -->
        <div v-if="listing.contractType" class="meta-item">
          <va-icon name="work" size="small" />
          <span>{{ listing.contractType }}</span>
        </div>

        <!-- Modalidad -->
        <div v-if="listing.modality" class="meta-item">
          <va-icon 
            :name="getModalityIcon" 
            size="small" 
          />
          <span>{{ listing.modality }}</span>
        </div>
      </div>

      <!-- Salario -->
      <div v-if="listing.salary && listing.salary !== 'No Declarado'" class="salary-info">
        <va-icon name="payments" size="small" />
        <span class="salary-text">{{ listing.salary }}</span>
      </div>

      <!-- Tags/Etiquetas -->
      <div v-if="listing.tags && listing.tags.length > 0" class="tags">
        <span 
          v-for="(tag, index) in listing.tags.slice(0, 3)" 
          :key="index"
          class="tag"
        >
          {{ tag }}
        </span>
        <span v-if="listing.tags.length > 3" class="tag more-tags">
          +{{ listing.tags.length - 3 }}
        </span>
      </div>

      <!-- Fecha de Publicación -->
      <div class="publish-date">
        <va-icon name="schedule" size="small" />
        <span>{{ getPublishDate }}</span>
      </div>

      <!-- Badges Adicionales -->
      <div class="badges-row">
        <span v-if="listing.urgent" class="badge urgent">
          <va-icon name="error" size="small" />
          Urgente
        </span>
        <span v-if="listing.featured" class="badge featured">
          <va-icon name="emoji_events" size="small" />
          Destacada
        </span>
      </div>

      <!-- Botón -->
      <button class="view-job-btn">
        Ver oferta completa
        <va-icon name="arrow_forward" size="small" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  listing: {
    type: Object,
    required: true
  }
})

const router = useRouter()

/**
 * Nombre de la empresa a mostrar
 */
const getCompanyDisplayName = computed(() => {
  if (props.listing.confidential) {
    return 'Publicación Confidencial'
  }
  if (props.listing.importantCompany) {
    return 'Importante Empresa'
  }
  return props.listing.companyName || 'Empresa'
})

/**
 * Icono según modalidad
 */
const getModalityIcon = computed(() => {
  const modality = props.listing.modality?.toLowerCase()
  if (modality?.includes('remoto')) return 'home'
  if (modality?.includes('híbrido')) return 'apartment'
  return 'location_city'
})

/**
 * Formato de fecha de publicación
 */
const getPublishDate = computed(() => {
  if (props.listing.publishedDaysAgo !== undefined) {
    const days = props.listing.publishedDaysAgo
    if (days === 0) return 'Publicado hoy'
    if (days === 1) return 'Publicado hace 1 día'
    return `Publicado hace ${days} días`
  }
  return props.listing.publishDate || 'Reciente'
})

/**
 * Navegar al detalle
 */
const goToDetail = () => {
  router.push(`/guias/trabajos/${props.listing.id}`)
}
</script>

<style scoped>
.job-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 2px solid transparent;
}

.job-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
  border-color: var(--color-purple-light);
}

/* ========== Logo ========== */
.card-logo {
  position: relative;
  width: 100%;
  height: 140px;
  background: #F5F5F5;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 2px solid #E0E0E0;
}

.card-logo img {
  max-width: 120px;
  max-height: 100px;
  object-fit: contain;
  padding: 1rem;
}

.placeholder-logo {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
}

/* ========== Badges ========== */
.badge-confidencial {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(158, 158, 158, 0.95);
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

.badge-destacado {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  padding: 0.4rem 0.875rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  box-shadow: 0 2px 8px rgba(253, 197, 0, 0.4);
}

/* ========== Contenido ========== */
.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
  flex: 1;
}

.job-title {
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

.company-name {
  font-size: 1rem;
  color: #666;
  margin: 0;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
  gap: 0.35rem;
  font-size: 0.875rem;
  color: #666;
}

/* ========== Salario ========== */
.salary-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(46, 125, 50, 0.05) 100%);
  border-left: 3px solid #4CAF50;
  border-radius: 6px;
}

.salary-text {
  font-size: 0.95rem;
  font-weight: 700;
  color: #2E7D32;
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
  color: var(--color-purple);
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.more-tags {
  background: #F0F0F0;
  color: #666;
}

/* ========== Fecha ========== */
.publish-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #999;
}

/* ========== Badges Adicionales ========== */
.badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.badge {
  padding: 0.35rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.badge.urgent {
  background: rgba(244, 67, 54, 0.1);
  color: #D32F2F;
}

.badge.featured {
  background: rgba(255, 193, 7, 0.15);
  color: #F57C00;
}

/* ========== Botón ========== */
.view-job-btn {
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

.view-job-btn:hover {
  background: var(--color-purple-dark);
  transform: translateX(4px);
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .card-logo {
    height: 120px;
  }

  .card-content {
    padding: 1.25rem;
  }

  .job-title {
    font-size: 1.1rem;
  }

  .company-name {
    font-size: 0.95rem;
  }

  .meta-info {
    gap: 0.75rem;
  }

  .meta-item {
    font-size: 0.8rem;
  }
}
</style>