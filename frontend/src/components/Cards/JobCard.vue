<!-- frontend/src/components/Guide/JobCard.vue -->
<template>
  <div class="job-card" @click="goToDetail">
    <!-- Contenedor principal -->
    <div class="card-body">
      <!-- Badges encima del contenido -->
      <div class="badges-row">
        <div v-if="listing.confidential" class="badge-confidential">
          <va-icon name="visibility_off" size="small" />
          Confidencial
        </div>

        <div v-else-if="listing.plan === 'destacado' || listing.plan === 'premium'" class="badge-destacado">
          <va-icon name="star" size="small" />
          {{ listing.plan === 'premium' ? 'Premium' : 'Destacado' }}
        </div>
      </div>

      <!-- Logo cuadrado + Título clickeable -->
      <div class="header-section">
        <div class="logo-square">
          <img 
            v-if="!listing.confidential && listing.companyLogo" 
            :src="listing.companyLogo" 
            :alt="listing.companyName"
          />
          <va-icon 
            v-else
            :name="listing.confidential ? 'visibility_off' : 'business'" 
            size="2rem" 
            color="#999" 
          />
        </div>
        
        <div class="header-text">
          <h3 class="job-title">{{ listing.title }}</h3>
          <p class="company-name">
            <va-icon 
              v-if="listing.verified && !listing.confidential" 
              name="verified" 
              size="small" 
              color="#10B981" 
            />
            {{ getCompanyDisplayName }}
          </p>
        </div>
      </div>

      <!-- Metadata con iconos -->
      <div class="metadata-grid">
        <div class="meta-item">
          <va-icon name="place" size="small" color="#6B7280" />
          <span>{{ listing.city }}</span>
        </div>
        
        <div v-if="listing.contractType" class="meta-item">
          <va-icon name="work" size="small" color="#6B7280" />
          <span>{{ listing.contractType }}</span>
        </div>

        <div v-if="listing.modality" class="meta-item">
          <va-icon :name="getModalityIcon" size="small" color="#6B7280" />
          <span>{{ listing.modality }}</span>
        </div>

        <div v-if="listing.jobCategory" class="meta-item">
          <va-icon name="category" size="small" color="#6B7280" />
          <span>{{ listing.jobCategory }}</span>
        </div>
      </div>

      <!-- Salario destacado -->
      <div v-if="listing.salary && listing.salary !== 'No Declarado'" class="salary-highlight">
        <va-icon name="payments" size="small" color="#10B981" />
        <span class="salary-text">{{ listing.salary }}</span>
      </div>

      <!-- Fecha de publicación -->
      <div class="publish-date">
        <va-icon name="schedule" size="small" color="#9CA3AF" />
        <span>{{ getPublishDate }}</span>
      </div>
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

.job-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.15);
}

.job-card:hover .job-title {
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

.badge-confidential {
  background: #6B7280;
  color: white;
  padding: 0.375rem 0.875rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 2px 8px rgba(107, 114, 128, 0.3);
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
  object-fit: contain;
  padding: 0.5rem;
}

.header-text {
  flex: 1;
  min-width: 0;
}

.job-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
  transition: color 0.3s ease;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.company-name {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
  line-height: 1.4;
  display: flex;
  align-items: center;
  gap: 0.35rem;
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

/* ========== SALARIO DESTACADO ========== */
.salary-highlight {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
  border-left: 4px solid #10B981;
  border-radius: 8px;
}

.salary-text {
  font-size: 1rem;
  font-weight: 700;
  color: #059669;
}

/* ========== FECHA ========== */
.publish-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #9CA3AF;
  font-weight: 500;
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

  .job-title {
    font-size: 1.25rem;
  }

  .company-name {
    font-size: 0.9375rem;
  }

  .badge-confidential,
  .badge-destacado {
    font-size: 0.8125rem;
    padding: 0.3125rem 0.75rem;
  }
}

@media (max-width: 480px) {
  .job-card {
    max-width: 100%;
  }

  .card-body {
    padding: 1rem;
  }

  .job-title {
    font-size: 1.125rem;
  }

  .salary-text {
    font-size: 0.9375rem;
  }
}
</style>