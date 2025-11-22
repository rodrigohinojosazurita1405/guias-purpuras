<!-- components/Rating/ReviewsTab.vue -->
<template>
  <div class="reviews-tab">
    <!-- Header con estadísticas -->
    <header class="reviews-header">
      <div class="reviews-stats">
        <h2 class="reviews-title">
          <va-icon name="star" size="1.5rem" />
          Reseñas y calificaciones
        </h2>
        
        <div class="stats-summary">
          <div class="stat-item">
            <span class="stat-number">{{ formattedAverage }}</span>
            <span class="stat-label">Promedio</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">{{ totalReviews }}</span>
            <span class="stat-label">{{ totalReviews === 1 ? 'Reseña' : 'Reseñas' }}</span>
          </div>
        </div>
      </div>

      <div class="rating-widget">
        <!-- ✅ Sin props inexistentes, con eventos correctos -->
        <va-button
          v-if="canUserRate"
          @click="openRatingForm"
          color="primary"
          icon="rate_review"
        >
          Escribir reseña
        </va-button>
      </div>
    </header>

    <!-- Filtros simples -->
    <div class="reviews-controls">
      <div class="simple-filters">
        <span class="filter-label">Mostrar:</span>
        
        <div class="filter-buttons">
          <button
            :class="['filter-tab', { active: activeRatingFilter === '' }]"
            @click="activeRatingFilter = ''"
          >
            Todas ({{ totalReviews }})
          </button>
          <button
            :class="['filter-tab', { active: activeRatingFilter === 5 }]"
            @click="activeRatingFilter = 5"
          >
            5★ ({{ getFilterCount(5) }})
          </button>
          <button
            :class="['filter-tab', { active: activeRatingFilter === 4 }]"
            @click="activeRatingFilter = 4"
          >
            4★ ({{ getFilterCount(4) }})
          </button>
          <button
            :class="['filter-tab', { active: activeRatingFilter === 3 }]"
            @click="activeRatingFilter = 3"
          >
            3★ ({{ getFilterCount(3) }})
          </button>
        </div>
      </div>

      <div class="sort-simple">
        <va-select
          v-model="sortBy"
          :options="sortOptions"
          size="small"
          style="min-width: 140px;"
          class="sort-select"
        />
      </div>
    </div>

    <!-- Loading optimizado -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-skeleton">
        <div v-for="i in 3" :key="i" class="review-skeleton">
          <div class="skeleton-avatar"></div>
          <div class="skeleton-content">
            <div class="skeleton-line skeleton-name"></div>
            <div class="skeleton-line skeleton-stars"></div>
            <div class="skeleton-line skeleton-text"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista de reseñas -->
    <div v-else-if="filteredReviews.length > 0" class="reviews-list">
      <!-- Reseña del usuario si existe -->
      <ReviewItem
        v-if="userReview && !isUserReviewInFiltered"
        :review="userReview"
        :is-highlighted="true"
        @mark-helpful="handleMarkHelpful"
        @report="handleReportReview"
        @edit-review="handleEditReview"
        @delete-review="handleDeleteReview"
        class="user-review-highlight"
      />

      <!-- Separador -->
      <div v-if="userReview && !isUserReviewInFiltered" class="reviews-separator">
        <span>Otras reseñas</span>
      </div>

      <!-- Lista principal -->
      <ReviewItem
        v-for="review in paginatedReviews"
        :key="`review-${review.id}`"
        :review="review"
        @mark-helpful="handleMarkHelpful"
        @report="handleReportReview"
        @edit-review="handleEditReview"
        @delete-review="handleDeleteReview"
        class="review-item"
      />

      <!-- Paginación -->
      <div v-if="totalPages > 1" class="pagination-section">
        <va-pagination
          v-model="currentPage"
          :pages="totalPages"
          :visible-pages="5"
          buttons-preset="secondary"
          border-color="primary"
        />
      </div>
    </div>

    <!-- Estado vacío -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <va-icon name="rate_review" size="3rem" color="#9CA3AF" />
      </div>
      <h3 class="empty-title">
        {{ hasActiveFilters ? 'No hay reseñas con este filtro' : 'Aún no hay reseñas' }}
      </h3>
      <p class="empty-description">
        {{ hasActiveFilters 
          ? 'Prueba con otros filtros para ver más reseñas.'
          : '¡Sé el primero en escribir una reseña!' 
        }}
      </p>
      
      <va-button
        v-if="!hasActiveFilters && canUserRate"
        @click="openRatingForm"
        color="primary"
        class="first-review-btn"
      >
        <va-icon name="edit" />
        Escribir reseña
      </va-button>
      
      <va-button
        v-else-if="hasActiveFilters"
        @click="clearFilters"
        color="secondary"
        class="clear-filters-btn"
      >
        Ver todas
      </va-button>
    </div>

    <!-- Notificación -->
    <va-toast 
      v-model="showToast"
      :message="toastMessage"
      :color="toastColor"
      position="top-right"
      :duration="3000"
      class="custom-toast"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRating } from '@/composables/useRating'
import { useAuthStore } from '@/stores/useAuthStore'
import ReviewItem from './ReviewItem.vue'

// ========== PROPS ==========
const props = defineProps({
  entityType: {
    type: String,
    required: true,
    validator: (value) => ['professional', 'business', 'restaurant', 'job'].includes(value)
  },
  entityId: {
    type: [String, Number],
    required: true
  },
  perPage: {
    type: Number,
    default: 10
  }
})

// ========== EMITS ==========
const emit = defineEmits(['review-added', 'review-updated', 'review-deleted'])

// ========== DEPENDENCIES ==========
const authStore = useAuthStore()

// ✅ Usar composable useRating
const {
  isLoading,
  reviews,
  userRating,
  averageRating,
  totalReviews,
  ratingDistribution,
  canUserRate,
  loadRatings,
  markReviewHelpful,
  reportReview,
  deleteUserRating,
  openReviewForm
} = useRating(props.entityType, props.entityId)

// ========== STATE ==========
const currentPage = ref(1)
const activeRatingFilter = ref('')
const sortBy = ref('newest')
const showToast = ref(false)
const toastMessage = ref('')
const toastColor = ref('success')

// ========== COMPUTED ==========
const formattedAverage = computed(() => {
  return averageRating.value > 0 ? averageRating.value.toFixed(1) : '0.0'
})

const userReview = computed(() => {
  return userRating.value
})

/**
 * ✅ Reviews filtradas y ordenadas
 */
const filteredReviews = computed(() => {
  let filtered = [...reviews.value]
  
  // Excluir reseña del usuario
  if (userReview.value) {
    filtered = filtered.filter(review => review.id !== userReview.value.id)
  }
  
  // Filtro por rating
  if (activeRatingFilter.value) {
    filtered = filtered.filter(review => {
      // ✅ Considerar ratings que redondean al valor seleccionado
      const roundedRating = Math.round(review.rating)
      return roundedRating === activeRatingFilter.value || review.rating === activeRatingFilter.value
    })
  }
  
  // Ordenamiento
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'newest':
        return new Date(b.created_at) - new Date(a.created_at)
      case 'oldest':
        return new Date(a.created_at) - new Date(b.created_at)
      case 'highest':
        if (b.rating !== a.rating) {
          return b.rating - a.rating
        }
        return new Date(b.created_at) - new Date(a.created_at)
      case 'lowest':
        if (a.rating !== b.rating) {
          return a.rating - b.rating
        }
        return new Date(b.created_at) - new Date(a.created_at)
      default:
        return new Date(b.created_at) - new Date(a.created_at)
    }
  })
  
  return filtered
})

const isUserReviewInFiltered = computed(() => {
  if (!userReview.value) return false
  return activeRatingFilter.value ? userReview.value.rating === activeRatingFilter.value : true
})

const paginatedReviews = computed(() => {
  const startIndex = (currentPage.value - 1) * props.perPage
  const endIndex = startIndex + props.perPage
  return filteredReviews.value.slice(startIndex, endIndex)
})

const totalPages = computed(() => {
  return Math.ceil(filteredReviews.value.length / props.perPage)
})

const hasActiveFilters = computed(() => {
  return activeRatingFilter.value !== ''
})

const getFilterCount = (star) => {
  return ratingDistribution.value[star] || 0
}

// ========== DATA ==========
const sortOptions = [
  { text: 'Más recientes', value: 'newest' },
  { text: 'Más antiguas', value: 'oldest' },
  { text: 'Mejor calificadas', value: 'highest' },
  { text: 'Peor calificadas', value: 'lowest' }
]

// ========== METHODS ==========

/**
 * Abrir formulario de calificación
 */
const openRatingForm = () => {
  openReviewForm()
}

/**
 * Manejar marcar como útil
 */
const handleMarkHelpful = async (reviewId) => {
  try {
    const success = await markReviewHelpful(reviewId)
    if (success) {
      showNotification('Marcado como útil', 'success')
      await loadRatings(true)
    } else {
      showNotification('Ya has marcado esta reseña como útil', 'info')
    }
  } catch (error) {
    showNotification('Error al marcar como útil', 'danger')
  }
}

/**
 * Manejar reporte de reseña
 */
const handleReportReview = async (reviewId, reportData) => {
  try {
    const success = await reportReview(reviewId, reportData)
    if (success) {
      showNotification('Reseña reportada', 'success')
    } else {
      showNotification('Error al reportar reseña', 'danger')
    }
  } catch (error) {
    showNotification('Error al reportar reseña', 'danger')
  }
}

/**
 * Manejar edición de reseña
 */
const handleEditReview = () => {
  openReviewForm()
  emit('review-updated')
}

/**
 * Manejar eliminación de reseña
 */
const handleDeleteReview = async () => {
  if (confirm('¿Estás seguro de eliminar tu reseña?')) {
    try {
      const success = await deleteUserRating()
      if (success) {
        showNotification('Reseña eliminada', 'success')
        emit('review-deleted')
        await loadRatings(true)
      }
    } catch (error) {
      showNotification('Error al eliminar reseña', 'danger')
    }
  }
}

/**
 * Limpiar filtros
 */
const clearFilters = () => {
  activeRatingFilter.value = ''
  sortBy.value = 'newest'
  currentPage.value = 1
}

/**
 * Mostrar notificación
 */
const showNotification = (message, color = 'success') => {
  toastMessage.value = message
  toastColor.value = color
  showToast.value = true
}

// ========== WATCHERS ==========

// Resetear página cuando cambian los filtros
watch([activeRatingFilter, sortBy], () => {
  currentPage.value = 1
})
</script>

<style scoped>
/* ========== Container ========== */
.reviews-tab {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem 0;
}

/* ========== Header ========== */
.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFF 100%);
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.reviews-stats {
  flex: 1;
}

.reviews-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0 0 1.5rem 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1F2937;
}

.stats-summary {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-purple);
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
  margin-top: 0.25rem;
}

.stat-divider {
  width: 1px;
  height: 2rem;
  background: #D1D5DB;
}

.rating-widget {
  flex-shrink: 0;
}

/* ========== Controles ========== */
.reviews-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  margin: 0 0.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
  flex-wrap: wrap;
}

.simple-filters {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.filter-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
  white-space: nowrap;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-tab {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  background: white;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.filter-tab:hover {
  border-color: var(--color-purple);
  background: rgba(92, 0, 153, 0.05);
}

.filter-tab.active {
  background: var(--color-purple);
  color: white;
  border-color: var(--color-purple);
}

.sort-simple {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* ========== Loading Skeleton ========== */
.loading-state {
  padding: 1rem;
}

.loading-skeleton {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-skeleton {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
}

.skeleton-avatar {
  width: 50px;
  height: 50px;
  background: linear-gradient(90deg, #F3F4F6, #E5E7EB, #F3F4F6);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: 50%;
  flex-shrink: 0;
}

.skeleton-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.skeleton-line {
  height: 14px;
  background: linear-gradient(90deg, #F3F4F6, #E5E7EB, #F3F4F6);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: 4px;
}

.skeleton-name { width: 120px; height: 16px; }
.skeleton-stars { width: 100px; height: 12px; }
.skeleton-text { width: 100%; }

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* ========== Reviews List ========== */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin: 0 0.5rem;
}

.user-review-highlight {
  border-color: #3B82F6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.review-item {
  opacity: 0;
  animation: fadeInUp 0.4s ease forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.reviews-separator {
  position: relative;
  text-align: center;
  margin: 1rem 0;
}

.reviews-separator::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #E5E7EB;
}

.reviews-separator span {
  background: white;
  color: #6B7280;
  padding: 0 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

/* ========== Pagination ========== */
.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #E5E7EB;
}

/* ========== Empty State ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 3rem 2rem;
  text-align: center;
  background: #F9FAFB;
  border-radius: 16px;
  border: 2px dashed #D1D5DB;
  margin: 0 0.5rem;
}

.empty-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
}

.empty-description {
  margin: 0;
  color: #6B7280;
  font-size: 1rem;
  line-height: 1.5;
  max-width: 400px;
}

/* ========== Toast ========== */
:deep(.custom-toast .va-toast__content) {
  color: white !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
}

:deep(.custom-toast.va-toast--color-success) {
  background-color: #10B981 !important;
  border-color: #059669 !important;
}

:deep(.custom-toast.va-toast--color-danger) {
  background-color: #EF4444 !important;
  border-color: #DC2626 !important;
}

:deep(.custom-toast.va-toast--color-info) {
  background-color: #3B82F6 !important;
  border-color: #2563EB !important;
}

/* ========== Responsive ========== */
@media (max-width: 1024px) {
  .reviews-header {
    flex-direction: column;
    gap: 2rem;
  }
  
  .stats-summary {
    justify-content: center;
  }
  
  .reviews-controls {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    margin: 0;
  }
  
  .simple-filters {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .reviews-tab {
    padding: 1rem 0.5rem;
    gap: 1.25rem;
  }
  
  .reviews-header {
    padding: 1.5rem;
  }
  
  .reviews-title {
    font-size: 1.5rem;
    text-align: center;
  }
  
  .reviews-controls {
    padding: 1rem;
  }
  
  .filter-buttons {
    justify-content: center;
  }
  
  .filter-tab {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
  
  .reviews-list {
    margin: 0;
  }
  
  .empty-state {
    margin: 0;
    padding: 2rem 1rem;
  }
}

@media (max-width: 640px) {
  .filter-buttons {
    gap: 0.25rem;
  }
  
  .filter-tab {
    padding: 0.3rem 0.6rem;
    font-size: 0.75rem;
  }
  
  .empty-title {
    font-size: 1.125rem;
  }
}
</style>