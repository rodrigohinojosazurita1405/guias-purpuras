// composables/useRating.js
import { ref, computed, watch } from 'vue'
import { useRatingStore } from '@/stores/useRatingStore'
import { useAuthStore } from '@/stores/useAuthStore'

/**
 * 🔗 DJANGO API INTEGRATION
 * Composable para manejar la lógica de calificaciones
 * 
 * @param {string} entityType - 'professional', 'business', 'restaurant', 'job'
 * @param {number|string} entityId - ID de la entidad a calificar
 * @returns {object} Objeto con métodos y estado reactivo
 */
export function useRating(entityType, entityId) {
  // ✅ Validar entityType
  const validTypes = ['professional', 'business', 'restaurant', 'job']
  
  if (!validTypes.includes(entityType)) {
    console.error(`[useRating] Invalid entityType: "${entityType}". Must be one of: ${validTypes.join(', ')}`)
    throw new Error(`entityType must be one of: ${validTypes.join(', ')}`)
  }

  const ratingStore = useRatingStore()
  const authStore = useAuthStore()

  // ========== ESTADO LOCAL ==========
  const isSubmittingRating = ref(false)
  const showReviewForm = ref(false)
  const localRating = ref(0)
  const localReview = ref('')
  const error = ref(null)

  // ========== COMPUTED ==========
  const entityKey = computed(() => `${entityType}_${entityId}`)
  
  // ✅ Usar getLoadingState del store
  const isLoading = computed(() => 
    ratingStore.getLoadingState(entityType, entityId)
  )
  
  const ratingData = computed(() => 
    ratingStore.getRatingData(entityType, entityId)
  )
  
  const userRating = computed(() => 
    ratingStore.getUserRating(entityType, entityId, authStore.user?.id)
  )
  
  const reviews = computed(() => 
    ratingStore.getReviews(entityType, entityId)
  )
  
  const averageRating = computed(() => 
    ratingData.value?.average_rating || 0
  )
  
  const totalReviews = computed(() => 
    ratingData.value?.total_reviews || 0
  )
  
  const ratingDistribution = computed(() => 
    ratingData.value?.rating_distribution || { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 }
  )
  
  const canUserRate = computed(() => {
    return authStore.isAuthenticated && !userRating.value
  })
  
  const hasUserRated = computed(() => !!userRating.value)

  // ========== MÉTODOS ==========

  /**
   * 🔗 DJANGO API INTEGRATION
   * Cargar ratings y reseñas desde el servidor
   * 
   * @param {boolean} forceRefresh - Forzar recarga desde servidor (ignora cache)
   * 
   * TODO: El store manejará las llamadas reales a Django API:
   * - GET /api/ratings/{entityType}/{entityId}/
   * - GET /api/reviews/{entityType}/{entityId}/
   */
  const loadRatings = async (forceRefresh = false) => {
    if (!entityType || !entityId) {
      console.warn('[useRating] Cannot load ratings: entityType or entityId is missing')
      return
    }

    error.value = null
    
    try {
      await ratingStore.fetchRatings(entityType, entityId, forceRefresh)
      await ratingStore.fetchReviews(entityType, entityId, forceRefresh)
    } catch (err) {
      error.value = {
        type: 'fetch',
        message: 'Error cargando calificaciones',
        details: err.message
      }
      console.error('[useRating] Error loading ratings:', err)
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Enviar nueva calificación
   * 
   * @param {number} rating - Calificación de 1 a 5 estrellas
   * @param {string} review - Comentario opcional (máx 500 caracteres)
   * @returns {Promise<boolean>} Success
   * 
   * Django endpoint: POST /api/ratings/
   * Body: {
   *   entity_type: string,
   *   entity_id: number,
   *   rating: number,
   *   comment: string
   * }
   */
  const submitRating = async (rating, review = '') => {
    // Validación de autenticación
    if (!authStore.isAuthenticated) {
      error.value = {
        type: 'auth',
        message: 'Debes iniciar sesión para calificar'
      }
      return false
    }

    // Validación de permisos
    if (!canUserRate.value) {
      error.value = {
        type: 'permission',
        message: 'Ya has calificado este elemento'
      }
      return false
    }

    // Validación de rating
    if (rating < 1 || rating > 5) {
      error.value = {
        type: 'validation',
        message: 'La calificación debe ser entre 1 y 5 estrellas'
      }
      return false
    }

    // Validación de contenido del review
    const validationErrors = validateReviewContent(review)
    if (validationErrors.length > 0) {
      error.value = {
        type: 'validation',
        message: validationErrors[0]
      }
      return false
    }

    isSubmittingRating.value = true
    error.value = null

    try {
      const success = await ratingStore.submitRating({
        entity_type: entityType,
        entity_id: entityId,
        user_id: authStore.user.id,
        rating: rating,
        review: review.trim(),
        user_name: authStore.user.name,
        user_avatar: authStore.user.avatar
      })

      if (success) {
        localRating.value = 0
        localReview.value = ''
        showReviewForm.value = false
        
        // ✅ Recargar datos con forceRefresh
        await loadRatings(true)
        
        return true
      } else {
        error.value = {
          type: 'submit',
          message: 'Error enviando calificación'
        }
        return false
      }
    } catch (err) {
      error.value = {
        type: 'submit',
        message: 'Error enviando calificación',
        details: err.message
      }
      console.error('[useRating] Error submitting rating:', err)
      return false
    } finally {
      isSubmittingRating.value = false
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Eliminar calificación del usuario actual
   * 
   * Django endpoint: DELETE /api/ratings/{reviewId}/
   */
  const deleteUserRating = async () => {
    if (!userRating.value) {
      console.warn('[useRating] No user rating to delete')
      return false
    }

    try {
      const success = await ratingStore.deleteRating(userRating.value.id)
      if (success) {
        await loadRatings(true)
        return true
      }
      return false
    } catch (err) {
      error.value = {
        type: 'delete',
        message: 'Error eliminando calificación',
        details: err.message
      }
      console.error('[useRating] Error deleting rating:', err)
      return false
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION  
   * Actualizar calificación existente
   * 
   * Django endpoint: PUT /api/ratings/{reviewId}/
   * Body: { rating: number, comment: string }
   */
  const updateUserRating = async (rating, review = '') => {
    if (!userRating.value) {
      console.warn('[useRating] No user rating to update')
      return false
    }

    // Validar contenido
    const validationErrors = validateReviewContent(review)
    if (validationErrors.length > 0) {
      error.value = {
        type: 'validation',
        message: validationErrors[0]
      }
      return false
    }

    try {
      const success = await ratingStore.updateRating(userRating.value.id, {
        rating,
        review: review.trim()
      })
      
      if (success) {
        await loadRatings(true)
        return true
      }
      return false
    } catch (err) {
      error.value = {
        type: 'update',
        message: 'Error actualizando calificación',
        details: err.message
      }
      console.error('[useRating] Error updating rating:', err)
      return false
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Marcar reseña como útil
   * 
   * Django endpoint: POST /api/reviews/{reviewId}/helpful/
   */
  const markReviewHelpful = async (reviewId) => {
    if (!authStore.isAuthenticated) {
      error.value = {
        type: 'auth',
        message: 'Debes iniciar sesión para marcar como útil'
      }
      return false
    }

    try {
      return await ratingStore.markReviewHelpful(reviewId, authStore.user?.id)
    } catch (err) {
      console.error('[useRating] Error marking review helpful:', err)
      return false
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Reportar reseña inapropiada  
   * 
   * Django endpoint: POST /api/reviews/{reviewId}/report/
   * Body: { reason: string, details: string }
   */
  const reportReview = async (reviewId, reason) => {
    if (!authStore.isAuthenticated) {
      error.value = {
        type: 'auth',
        message: 'Debes iniciar sesión para reportar'
      }
      return false
    }

    try {
      return await ratingStore.reportReview(reviewId, {
        reported_by: authStore.user?.id,
        reason
      })
    } catch (err) {
      console.error('[useRating] Error reporting review:', err)
      return false
    }
  }

  /**
   * Obtener estadísticas detalladas
   */
  const getStats = computed(() => {
    const total = totalReviews.value
    if (total === 0) return null

    const distribution = ratingDistribution.value
    
    return {
      average: averageRating.value,
      total: total,
      percentages: {
        5: Math.round((distribution[5] / total) * 100),
        4: Math.round((distribution[4] / total) * 100),
        3: Math.round((distribution[3] / total) * 100),
        2: Math.round((distribution[2] / total) * 100),
        1: Math.round((distribution[1] / total) * 100)
      },
      mostCommon: Object.entries(distribution)
        .sort(([,a], [,b]) => b - a)[0]?.[0] || 5
    }
  })

  /**
   * Limpiar errores
   */
  const clearError = () => {
    error.value = null
    ratingStore.clearError()
  }

  /**
   * Abrir formulario de reseña
   */
  const openReviewForm = () => {
    if (!authStore.isAuthenticated) {
      error.value = {
        type: 'auth',
        message: 'Debes iniciar sesión para calificar'
      }
      return
    }
    
    if (hasUserRated.value) {
      // Pre-llenar con calificación existente
      localRating.value = userRating.value.rating
      localReview.value = userRating.value.review || ''
    }
    
    showReviewForm.value = true
  }

  /**
   * Cerrar formulario de reseña
   */
  const closeReviewForm = () => {
    showReviewForm.value = false
    localRating.value = 0
    localReview.value = ''
    clearError()
  }

  // ========== WATCHERS ==========
  
  // Cargar datos cuando cambien los parámetros
  watch([() => entityType, () => entityId], () => {
    if (entityType && entityId) {
      loadRatings()
    }
  }, { immediate: true })

  // ========== RETURN ==========
  return {
    // Estado
    isLoading,
    isSubmittingRating,
    showReviewForm,
    localRating,
    localReview,
    error,
    
    // Datos computados
    ratingData,
    userRating,
    reviews,
    averageRating,
    totalReviews,
    ratingDistribution,
    canUserRate,
    hasUserRated,
    getStats,
    
    // Métodos
    loadRatings,
    submitRating,
    deleteUserRating,
    updateUserRating,
    markReviewHelpful,
    reportReview,
    clearError,
    openReviewForm,
    closeReviewForm
  }
}

// ========== HELPER FUNCTIONS ==========

/**
 * 🔗 DJANGO SYNC
 * Helper para formatear fechas de forma amigable
 * 
 * ⚠️ IMPORTANTE: Esta función debe coincidir con el formato de fechas de Django
 * Django envía fechas en formato ISO: "2024-01-15T10:30:00Z"
 */
export function formatRelativeDate(dateString) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const now = new Date()
  const diffInMs = now.getTime() - date.getTime()
  const diffInMinutes = Math.floor(diffInMs / (1000 * 60))
  const diffInHours = Math.floor(diffInMinutes / 60)
  const diffInDays = Math.floor(diffInHours / 24)
  const diffInWeeks = Math.floor(diffInDays / 7)
  const diffInMonths = Math.floor(diffInDays / 30)
  
  if (diffInMinutes < 1) return 'Ahora mismo'
  if (diffInMinutes < 60) return `Hace ${diffInMinutes} minuto${diffInMinutes > 1 ? 's' : ''}`
  if (diffInHours < 24) return `Hace ${diffInHours} hora${diffInHours > 1 ? 's' : ''}`
  if (diffInDays === 1) return 'Ayer'
  if (diffInDays < 7) return `Hace ${diffInDays} día${diffInDays > 1 ? 's' : ''}`
  if (diffInWeeks < 4) return `Hace ${diffInWeeks} semana${diffInWeeks > 1 ? 's' : ''}`
  if (diffInMonths < 12) return `Hace ${diffInMonths} mes${diffInMonths > 1 ? 'es' : ''}`
  
  return date.toLocaleDateString('es-ES', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

/**
 * ✅ Alias para compatibilidad con código existente
 */
export const formatDate = formatRelativeDate

/**
 * 🔗 DJANGO SYNC
 * Helper para validar contenido de reseñas
 * 
 * ⚠️ CRÍTICO: Estas reglas DEBEN coincidir EXACTAMENTE con Django backend
 * Backend validation location: /api/validators/review.py (o similar)
 * 
 * Reglas actuales:
 * - Longitud mínima: 10 caracteres (si no está vacío)
 * - Longitud máxima: 500 caracteres
 * - No permitir: teléfonos, emails, URLs
 * 
 * TODO: Sincronizar con Django cuando se implemente backend
 */
export function validateReviewContent(content) {
  const errors = []
  
  // Reseña es opcional
  if (!content || content.trim().length === 0) {
    return errors
  }
  
  // Longitud mínima
  if (content.trim().length < 10) {
    errors.push('La reseña debe tener al menos 10 caracteres')
  }
  
  // Longitud máxima
  if (content.length > 500) {
    errors.push('La reseña no puede exceder 500 caracteres')
  }
  
  // Contenido inapropiado básico
  const inappropriatePatterns = [
    { 
      pattern: /\b(telefono|celular|whatsapp|email|@)\b/i,
      message: 'No incluyas información de contacto en tu reseña'
    },
    { 
      pattern: /\b\d{7,}\b/,
      message: 'No incluyas números de teléfono en tu reseña'
    },
    { 
      pattern: /@\w+\.\w+/,
      message: 'No incluyas direcciones de correo en tu reseña'
    },
    { 
      pattern: /\b(http|www)\b/i,
      message: 'No incluyas enlaces en tu reseña'
    }
  ]
  
  for (const { pattern, message } of inappropriatePatterns) {
    if (pattern.test(content)) {
      errors.push(message)
      break // Solo mostrar el primer error de este tipo
    }
  }
  
  return errors
}

/**
 * Helper para obtener el color del rating
 */
export function getRatingColor(rating) {
  if (rating >= 4.5) return '#10B981' // verde
  if (rating >= 4.0) return '#F59E0B' // amarillo
  if (rating >= 3.0) return '#F97316' // naranja  
  if (rating >= 2.0) return '#EF4444' // rojo
  return '#6B7280' // gris
}

/**
 * Helper para obtener etiqueta de rating
 */
export function getRatingLabel(rating) {
  if (rating === 0) return 'Sin calificación'
  if (rating <= 1.5) return 'Muy malo'
  if (rating <= 2.5) return 'Malo'
  if (rating <= 3.5) return 'Regular'
  if (rating <= 4.5) return 'Bueno'
  return 'Excelente'
}