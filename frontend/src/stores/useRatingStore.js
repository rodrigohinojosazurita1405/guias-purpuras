// stores/useRatingStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * 🔗 DJANGO API ENDPOINTS
 * Este store está preparado para integrarse con Django REST API
 * 
 * Endpoints necesarios:
 * - GET    /api/ratings/{entityType}/{entityId}/     - Obtener ratings y distribución
 * - GET    /api/reviews/{entityType}/{entityId}/     - Obtener reseñas
 * - POST   /api/ratings/                             - Crear nueva calificación
 * - PUT    /api/ratings/{reviewId}/                  - Actualizar calificación
 * - DELETE /api/ratings/{reviewId}/                  - Eliminar calificación
 * - POST   /api/reviews/{reviewId}/helpful/          - Marcar como útil
 * - POST   /api/reviews/{reviewId}/report/           - Reportar reseña
 */

export const useRatingStore = defineStore('rating', () => {
  // ========== STATE ==========
  const ratingsData = ref(new Map())
  const reviewsData = ref(new Map())
  const loadingStates = ref(new Map()) // ✅ Ahora por entidad
  const error = ref(null)

  // ========== GETTERS ==========
  
  /**
   * Obtener datos de rating para una entidad
   */
  const getRatingData = (entityType, entityId) => {
    const key = `${entityType}_${entityId}`
    return ratingsData.value.get(key) || null
  }

  /**
   * Obtener reseñas para una entidad
   */
  const getReviews = (entityType, entityId) => {
    const key = `${entityType}_${entityId}`
    return reviewsData.value.get(key) || []
  }

  /**
   * Obtener la calificación de un usuario específico
   */
  const getUserRating = (entityType, entityId, userId) => {
    if (!userId) return null
    const reviews = getReviews(entityType, entityId)
    return reviews.find(review => review.user_id === userId) || null
  }

  /**
   * ✅ NUEVO: Obtener estado de carga por entidad
   */
  const getLoadingState = (entityType, entityId) => {
    const key = `${entityType}_${entityId}`
    return loadingStates.value.get(key) || false
  }

  // ========== ACTIONS ==========
  
  /**
   * 🔗 DJANGO API INTEGRATION
   * Cargar ratings desde el servidor
   * 
   * @param {string} entityType - Tipo de entidad
   * @param {string|number} entityId - ID de la entidad
   * @param {boolean} forceRefresh - Forzar recarga desde servidor
   * @returns {Promise<object>} Datos de ratings
   * 
   * Django endpoint: GET /api/ratings/{entityType}/{entityId}/
   * Response: {
   *   average_rating: number,
   *   total_reviews: number,
   *   rating_distribution: { 1: n, 2: n, 3: n, 4: n, 5: n }
   * }
   */
  const fetchRatings = async (entityType, entityId, forceRefresh = false) => {
    const key = `${entityType}_${entityId}`
    
    // ✅ Usar cache si existe y no se fuerza refresh
    if (!forceRefresh && ratingsData.value.has(key)) {
      return ratingsData.value.get(key)
    }

    loadingStates.value.set(key, true)
    error.value = null

    try {
      // TODO: Reemplazar con llamada real a Django
      // const response = await fetch(`/api/ratings/${entityType}/${entityId}/`)
      // if (!response.ok) throw new Error('Error fetching ratings')
      // const data = await response.json()
      
      // Simulación temporal
      await new Promise(resolve => setTimeout(resolve, 150))
      const mockData = generateMockRatings(entityType, entityId)
      
      ratingsData.value.set(key, mockData)
      return mockData
      
    } catch (err) {
      error.value = err.message
      console.error('Error fetching ratings:', err)
      throw err
    } finally {
      loadingStates.value.set(key, false)
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Cargar reseñas desde el servidor
   * 
   * @param {string} entityType - Tipo de entidad
   * @param {string|number} entityId - ID de la entidad
   * @param {boolean} forceRefresh - Forzar recarga desde servidor
   * @returns {Promise<array>} Array de reseñas
   * 
   * Django endpoint: GET /api/reviews/{entityType}/{entityId}/
   * Response: Array de objetos Review
   */
  const fetchReviews = async (entityType, entityId, forceRefresh = false) => {
    const key = `${entityType}_${entityId}`
    
    // ✅ Usar cache si existe y no se fuerza refresh
    if (!forceRefresh && reviewsData.value.has(key)) {
      return reviewsData.value.get(key)
    }

    try {
      // TODO: Reemplazar con llamada real a Django
      // const response = await fetch(`/api/reviews/${entityType}/${entityId}/`)
      // if (!response.ok) throw new Error('Error fetching reviews')
      // const data = await response.json()
      
      // Simulación temporal
      await new Promise(resolve => setTimeout(resolve, 100))
      const mockReviews = generateMockReviews(entityType, entityId)
      
      reviewsData.value.set(key, mockReviews)
      return mockReviews
      
    } catch (err) {
      error.value = err.message
      console.error('Error fetching reviews:', err)
      throw err
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Enviar nueva calificación
   * 
   * @param {object} ratingData - Datos de la calificación
   * @returns {Promise<boolean>} Success
   * 
   * Django endpoint: POST /api/ratings/
   * Body: {
   *   entity_type: string,
   *   entity_id: number,
   *   rating: number (1-5),
   *   comment: string
   * }
   */
  const submitRating = async (ratingData) => {
    try {
      // TODO: Reemplazar con llamada real a Django
      // const response = await fetch('/api/ratings/', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     entity_type: ratingData.entity_type,
      //     entity_id: ratingData.entity_id,
      //     rating: ratingData.rating,
      //     comment: ratingData.review
      //   })
      // })
      // if (!response.ok) throw new Error('Error submitting rating')
      // const newReview = await response.json()
      
      // Simulación temporal
      await new Promise(resolve => setTimeout(resolve, 800))
      
      const key = `${ratingData.entity_type}_${ratingData.entity_id}`
      
      // ✅ Estructura corregida con helpful_by
      const newReview = {
        id: Date.now(),
        user_id: ratingData.user_id,
        user_name: ratingData.user_name,
        user_avatar: ratingData.user_avatar || null,
        rating: ratingData.rating,
        review: ratingData.review,
        is_verified: Math.random() > 0.3,
        helpful_votes: 0,
        helpful_by: [], // ✅ AGREGADO
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
      
      const currentReviews = reviewsData.value.get(key) || []
      const updatedReviews = [newReview, ...currentReviews]
      reviewsData.value.set(key, updatedReviews)
      
      await updateRatingsStats(ratingData.entity_type, ratingData.entity_id)
      
      return true
    } catch (err) {
      error.value = err.message
      console.error('Error submitting rating:', err)
      return false
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Actualizar calificación existente
   * 
   * @param {number} reviewId - ID de la review
   * @param {object} updateData - Datos a actualizar
   * @returns {Promise<boolean>} Success
   * 
   * Django endpoint: PUT /api/ratings/{reviewId}/
   * Body: {
   *   rating: number,
   *   comment: string
   * }
   */
  const updateRating = async (reviewId, updateData) => {
    try {
      // TODO: Reemplazar con llamada real a Django
      // const response = await fetch(`/api/ratings/${reviewId}/`, {
      //   method: 'PUT',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(updateData)
      // })
      // if (!response.ok) throw new Error('Error updating rating')
      
      await new Promise(resolve => setTimeout(resolve, 600))
      
      // Actualizar en el store local
      for (const [key, reviews] of reviewsData.value.entries()) {
        const reviewIndex = reviews.findIndex(r => r.id === reviewId)
        if (reviewIndex !== -1) {
          // ✅ Crear nuevo array en lugar de mutar
          const updatedReviews = [...reviews]
          updatedReviews[reviewIndex] = {
            ...updatedReviews[reviewIndex],
            ...updateData,
            updated_at: new Date().toISOString()
          }
          
          reviewsData.value.set(key, updatedReviews)
          
          const [entityType, entityId] = key.split('_')
          await updateRatingsStats(entityType, parseInt(entityId))
          break
        }
      }
      
      return true
    } catch (err) {
      error.value = err.message
      console.error('Error updating rating:', err)
      return false
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Eliminar calificación
   * 
   * @param {number} reviewId - ID de la review
   * @returns {Promise<boolean>} Success
   * 
   * Django endpoint: DELETE /api/ratings/{reviewId}/
   */
  const deleteRating = async (reviewId) => {
    try {
      // TODO: Reemplazar con llamada real a Django
      // const response = await fetch(`/api/ratings/${reviewId}/`, {
      //   method: 'DELETE'
      // })
      // if (!response.ok) throw new Error('Error deleting rating')
      
      await new Promise(resolve => setTimeout(resolve, 400))
      
      for (const [key, reviews] of reviewsData.value.entries()) {
        const reviewIndex = reviews.findIndex(r => r.id === reviewId)
        if (reviewIndex !== -1) {
          // ✅ Crear nuevo array sin el elemento
          const updatedReviews = reviews.filter(r => r.id !== reviewId)
          reviewsData.value.set(key, updatedReviews)
          
          const [entityType, entityId] = key.split('_')
          await updateRatingsStats(entityType, parseInt(entityId))
          break
        }
      }
      
      return true
    } catch (err) {
      error.value = err.message
      console.error('Error deleting rating:', err)
      return false
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Marcar reseña como útil
   * 
   * @param {number} reviewId - ID de la review
   * @param {number} userId - ID del usuario
   * @returns {Promise<boolean>} Success
   * 
   * Django endpoint: POST /api/reviews/{reviewId}/helpful/
   * Body: {} (userId viene del token de autenticación)
   */
  const markReviewHelpful = async (reviewId, userId) => {
    if (!userId) {
      console.error('userId is required to mark review as helpful')
      return false
    }
    
    try {
      // TODO: Reemplazar con llamada real a Django
      // const response = await fetch(`/api/reviews/${reviewId}/helpful/`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' }
      // })
      // if (!response.ok) throw new Error('Error marking review helpful')
      
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // ✅ Lógica corregida con validación
      for (const [key, reviews] of reviewsData.value.entries()) {
        const review = reviews.find(r => r.id === reviewId)
        if (review) {
          // ✅ Inicializar helpful_by si no existe
          if (!review.helpful_by) {
            review.helpful_by = []
          }
          
          // ✅ Verificar si ya marcó como útil
          if (review.helpful_by.includes(userId)) {
            console.log('User already marked this review as helpful')
            return false
          }
          
          // ✅ Agregar usuario y incrementar contador
          review.helpful_by.push(userId)
          review.helpful_votes = (review.helpful_votes || 0) + 1
          
          // Crear nuevo array para reactividad
          const updatedReviews = [...reviews]
          reviewsData.value.set(key, updatedReviews)
          break
        }
      }
      
      return true
    } catch (err) {
      console.error('Error marking review helpful:', err)
      return false
    }
  }

  /**
   * 🔗 DJANGO API INTEGRATION
   * Reportar reseña inapropiada
   * 
   * @param {number} reviewId - ID de la review
   * @param {object} reportData - Datos del reporte
   * @returns {Promise<boolean>} Success
   * 
   * Django endpoint: POST /api/reviews/{reviewId}/report/
   * Body: {
   *   reason: string,
   *   details: string (optional)
   * }
   */
  const reportReview = async (reviewId, reportData) => {
    try {
      // TODO: Reemplazar con llamada real a Django
      // const response = await fetch(`/api/reviews/${reviewId}/report/`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(reportData)
      // })
      // if (!response.ok) throw new Error('Error reporting review')
      
      await new Promise(resolve => setTimeout(resolve, 400))
      console.log('Reseña reportada:', reviewId, reportData)
      return true
    } catch (err) {
      console.error('Error reporting review:', err)
      return false
    }
  }

  /**
   * Actualizar estadísticas de ratings
   * Esta función se ejecuta automáticamente después de agregar/actualizar/eliminar reviews
   */
  const updateRatingsStats = async (entityType, entityId) => {
    const key = `${entityType}_${entityId}`
    const reviews = reviewsData.value.get(key) || []
    
    if (reviews.length === 0) {
      ratingsData.value.set(key, {
        average_rating: 0,
        total_reviews: 0,
        rating_distribution: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 }
      })
      return
    }
    
    const totalRating = reviews.reduce((sum, review) => sum + review.rating, 0)
    const averageRating = totalRating / reviews.length
    
    const distribution = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 }
    reviews.forEach(review => {
      distribution[review.rating]++
    })
    
    ratingsData.value.set(key, {
      average_rating: Number(averageRating.toFixed(1)),
      total_reviews: reviews.length,
      rating_distribution: distribution
    })
  }

  /**
   * ✅ NUEVO: Limpiar errores
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * Limpiar datos de una entidad específica
   */
  const clearEntityData = (entityType, entityId) => {
    const key = `${entityType}_${entityId}`
    ratingsData.value.delete(key)
    reviewsData.value.delete(key)
    loadingStates.value.delete(key)
  }

  return {
    // State
    ratingsData,
    reviewsData,
    loadingStates,
    error,
    
    // Getters
    getRatingData,
    getReviews,
    getUserRating,
    getLoadingState, // ✅ NUEVO
    
    // Actions
    fetchRatings,
    fetchReviews,
    submitRating,
    updateRating,
    deleteRating,
    markReviewHelpful,
    reportReview,
    clearError, // ✅ NUEVO
    clearEntityData
  }
})

// ========== MOCK GENERATORS (TEMPORAL) ==========

/**
 * ✅ GENERADOR DE RATINGS MOCK
 * TODO: Eliminar cuando se conecte con Django
 */
function generateMockRatings(entityType, entityId) {
  const seed = parseInt(entityId) || 1
  
  // Solo 3 distribuciones simples
  const distributions = [
    { 5: 2, 4: 1, 3: 0, 2: 0, 1: 0 }, // 3 reseñas total
    { 5: 1, 4: 1, 3: 1, 2: 0, 1: 0 }, // 3 reseñas total
    { 5: 1, 4: 0, 3: 1, 2: 1, 1: 0 }  // 3 reseñas total
  ]
  
  const distribution = distributions[seed % 3]
  const totalReviews = 3
  
  let totalRating = 0
  for (let star = 1; star <= 5; star++) {
    totalRating += star * distribution[star]
  }
  
  const averageRating = totalReviews > 0 ? totalRating / totalReviews : 0
  
  return {
    average_rating: Number(averageRating.toFixed(1)),
    total_reviews: totalReviews,
    rating_distribution: distribution
  }
}

/**
 * ✅ GENERADOR DE REVIEWS MOCK CON helpful_by
 * TODO: Eliminar cuando se conecte con Django
 */
function generateMockReviews(entityType, entityId) {
  const ratingData = generateMockRatings(entityType, entityId)
  
  const names = ['Carlos Mamani', 'María Quispe', 'José Condori']
  
  const comments = {
    professional: [
      'Excelente atención profesional. Muy recomendable.',
      'Buen trabajo, aunque demoró un poco más de lo esperado.',
      'Regular atención. El trabajo estuvo bien pero sin destacar.'
    ],
    business: [
      'Excelente servicio y productos de calidad.',
      'Buen servicio aunque podrían mejorar los tiempos.',
      'Productos aceptables pero la atención podría ser mejor.'
    ],
    restaurant: [
      'Comida deliciosa y excelente atención.',
      'Rica comida pero el servicio podría ser más rápido.',
      'Comida regular y servicio lento.'
    ],
    job: [
      'Excelente oportunidad laboral con buen ambiente.',
      'Trabajo aceptable pero con algunas limitaciones.',
      'Condiciones laborales básicas sin mayores beneficios.'
    ]
  }
  
  const entityComments = comments[entityType] || comments.professional
  const reviews = []
  let reviewId = parseInt(entityId) * 100
  
  let index = 0
  for (let rating = 5; rating >= 1; rating--) {
    const count = ratingData.rating_distribution[rating]
    
    for (let i = 0; i < count && index < 3; i++) {
      const nameIndex = index % names.length
      const commentIndex = index % entityComments.length
      
      const daysAgo = Math.floor(Math.random() * 30) + 1
      const createdAt = new Date()
      createdAt.setDate(createdAt.getDate() - daysAgo)
      
      reviews.push({
        id: reviewId + index,
        user_id: 1000 + index,
        user_name: names[nameIndex],
        user_avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${names[nameIndex]}`,
        rating: rating,
        review: entityComments[commentIndex],
        is_verified: Math.random() > 0.3,
        helpful_votes: Math.floor(Math.random() * 3),
        helpful_by: [], // ✅ AGREGADO
        created_at: createdAt.toISOString(),
        updated_at: createdAt.toISOString()
      })
      
      index++
    }
  }
  
  return reviews.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
}