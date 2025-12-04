<!-- frontend/src/components/Cards/JobListItem.vue -->
<template>
  <div
    class="job-list-item"
    :class="cardPlanClass"
    @click="goToDetail"
  >
    <!-- Logo de empresa -->
    <div class="logo-container">
      <div class="logo-square">
        <img
          v-if="!listing.confidential && listing.companyLogo"
          :src="getCompanyLogoUrl"
          :alt="listing.companyName"
          @error="handleImageError"
        />
        <va-icon
          v-else
          :name="listing.confidential ? 'visibility_off' : 'business'"
          size="2.5rem"
          color="#999"
        />
      </div>
    </div>

    <!-- Contenido principal -->
    <div class="content-section">
      <!-- Badges -->
      <div class="badges-row">
        <div v-if="listing.confidential" class="badge-confidential">
          <va-icon name="visibility_off" size="small" />
          Confidencial
        </div>

        <!-- Plan Impulso -->
        <div v-if="listing.plan === 'impulso'" class="badge-patrocinado">
          Patrocinado
        </div>
        <div v-if="listing.plan === 'impulso'" class="badge-urgente">
          Urgente
        </div>

        <!-- Plan Púrpura -->
        <div v-if="listing.plan === 'purpura'" class="badge-destacado">
          Destacado
        </div>
        <div v-if="listing.plan === 'purpura'" class="badge-urgente">
          Urgente
        </div>
      </div>

      <!-- Título y empresa -->
      <div class="header-info">
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

      <!-- Metadata -->
      <div class="metadata-row">
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

        <div v-if="listing.salary" class="meta-item salary">
          <va-icon name="payments" size="small" color="#10B981" />
          <span>{{ listing.salary }}</span>
        </div>
      </div>
    </div>

    <!-- Fecha de publicación -->
    <div class="date-section">
      <span class="publish-date">{{ getPublishDate }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  listing: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const imageError = ref(false)

/**
 * Navegar al detalle del trabajo
 */
const goToDetail = () => {
  router.push(`/guias/trabajos/${props.listing.id}`)
}

/**
 * Nombre de empresa a mostrar
 */
const getCompanyDisplayName = computed(() => {
  return props.listing.confidential
    ? 'Empresa Confidencial'
    : props.listing.companyName
})

/**
 * URL completa del logo de la empresa
 */
const getCompanyLogoUrl = computed(() => {
  if (!props.listing.companyLogo || imageError.value) return null

  if (props.listing.companyLogo.startsWith('http')) {
    return props.listing.companyLogo
  }

  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
  return `${baseURL}${props.listing.companyLogo}`
})

/**
 * Manejar error de carga de imagen
 */
const handleImageError = () => {
  imageError.value = true
}

/**
 * Clase CSS según el plan del anuncio
 */
const cardPlanClass = computed(() => {
  const plan = props.listing.plan?.toLowerCase()
  if (plan === 'impulso') return 'plan-impulso'
  if (plan === 'purpura') return 'plan-purpura'
  if (plan === 'estandar') return 'plan-estandar'
  return ''
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
    if (days === 0) return 'Hoy'
    if (days === 1) return 'Hace 1 día'
    return `Hace ${days} días`
  }
  return props.listing.publishDate || 'Reciente'
})
</script>

<style scoped>
.job-list-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: white;
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
}

.job-list-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* Logo */
.logo-container {
  flex-shrink: 0;
}

.logo-square {
  width: 80px;
  height: 80px;
  min-width: 80px;
  min-height: 80px;
  border-radius: 10px;
  border: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: #F9FAFB;
  position: relative;
}

.logo-square img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  position: absolute;
  top: 0;
  left: 0;
}

/* Contenido */
.content-section {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Badges */
.badges-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge-confidential,
.badge-destacado,
.badge-patrocinado,
.badge-urgente {
  padding: 0.25rem 0.625rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.badge-confidential {
  background: linear-gradient(135deg, #6B7280 0%, #4B5563 100%);
  color: white;
}

.badge-destacado {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.badge-patrocinado {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.badge-urgente {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  color: white;
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3); }
  50% { box-shadow: 0 4px 16px rgba(220, 38, 38, 0.6); }
}

/* Header info */
.header-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.job-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
  line-height: 1.3;
}

.company-name {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  color: #6B7280;
  margin: 0;
}

/* Metadata */
.metadata-row {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  color: #6B7280;
}

.meta-item.salary {
  font-weight: 600;
  color: #10B981;
}

/* Fecha */
.date-section {
  flex-shrink: 0;
  text-align: right;
}

.publish-date {
  font-size: 0.875rem;
  color: #9CA3AF;
  white-space: nowrap;
}

/* Plan-specific styling */
.job-list-item.plan-impulso {
  border: 2px solid #10B981;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.03) 0%, white 100%);
  box-shadow: 0 2px 12px rgba(16, 185, 129, 0.15);
}

.job-list-item.plan-purpura {
  border: 2px solid #7C3AED;
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.03) 0%, white 100%);
  box-shadow: 0 2px 10px rgba(124, 58, 237, 0.12);
}

.job-list-item.plan-estandar {
  border: 1px solid #E5E7EB;
}

/* Responsive */
@media (max-width: 768px) {
  .job-list-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
  }

  .logo-square {
    width: 60px;
    height: 60px;
  }

  .job-title {
    font-size: 1rem;
  }

  .metadata-row {
    gap: 1rem;
  }

  .date-section {
    width: 100%;
    text-align: left;
  }
}
</style>
