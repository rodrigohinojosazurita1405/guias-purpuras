<!-- components/Rating/RatingSystem.vue -->
<template>
  <div class="rating-system">
    <!-- Header con rating principal -->
    <div class="rating-header">
      <div class="rating-info">
        <div class="rating-number">4.0</div>
        <div class="stars-wrapper">
          <div class="stars-clickeable" @click="handleCalificar" title="Calificar este servicio">
            <span class="star filled">★</span>
            <span class="star filled">★</span>
            <span class="star filled">★</span>
            <span class="star filled">★</span>
            <span class="star">☆</span>
          </div>
          <span class="total-text">Basado en 3 opiniones</span>
        </div>
      </div>
      <button @click="handleCalificar" class="btn-calificar">
        <va-icon name="rate_review" size="small" />
        <span>Escribir reseña</span>
      </button>
    </div>

    <!-- Distribución de calificaciones -->
    <div class="distribucion">
      <div v-for="star in [5, 4, 3, 2, 1]" :key="star" class="dist-fila">
        <span class="star-label">{{ star }}</span>
        <va-icon name="star" size="small" color="#FFC107" />
        <div class="barra-container">
          <div class="barra-fill" :style="{ width: getPercentage(star) + '%' }"></div>
        </div>
        <span class="star-count">{{ getCount(star) }}</span>
      </div>
    </div>

    <!-- Lista de reseñas -->
    <div class="reviews-section">
      <div class="section-header">
        <h3>Reseñas verificadas</h3>
        <div class="filter-options">
          <va-select
            v-model="filtroOrden"
            :options="ordenOptions"
            placeholder="Ordenar por"
            size="small"
            class="order-select"
          />
        </div>
      </div>
      
      <div class="reviews-list">
        <!-- ✅ Review del usuario destacada -->
        <article 
          v-if="userReview"
          :key="userReview.id"
          class="review-item user-review-highlight"
        >
          <!-- Badge "Tu reseña" -->
          <div class="user-review-badge">
            <va-icon name="person" size="small" />
            Tu reseña
          </div>

          <!-- Header -->
          <div class="review-header">
            <div class="reviewer-info">
              <div class="avatar">
                <img :src="userReview.user_avatar" :alt="userReview.user_name">
              </div>
              <div class="reviewer-details">
                <div class="reviewer-name-row">
                  <h4 class="reviewer-name">{{ userReview.user_name }}</h4>
                </div>
                <time class="review-date">{{ formatDate(userReview.created_at) }}</time>
              </div>
            </div>
            
            <div class="review-rating-stars">
              <span v-for="n in 5" :key="n" class="star" :class="{ filled: n <= userReview.rating }">
                ★
              </span>
            </div>
          </div>

          <!-- Content -->
          <div class="review-content">
            <p class="review-text">{{ userReview.review }}</p>
          </div>

          <!-- Footer con acciones -->
          <div class="review-footer">
            <div class="review-stats">
              <span v-if="userReview.helpful_count > 0" class="helpful-count">
                <va-icon name="thumb_up" size="small" />
                {{ userReview.helpful_count }} {{ userReview.helpful_count === 1 ? 'persona' : 'personas' }}
              </span>
            </div>
            
            <div class="review-actions">
              <va-dropdown placement="bottom-end">
                <template #anchor>
                  <button class="action-btn more-btn">
                    <va-icon name="more_vert" size="small" />
                  </button>
                </template>
                <va-dropdown-content class="actions-dropdown">
                  <button @click="handleEdit(userReview.id)" class="dropdown-item">
                    <va-icon name="edit" size="small" />
                    <span>Editar</span>
                  </button>
                  <button @click="handleDelete(userReview.id)" class="dropdown-item danger">
                    <va-icon name="delete" size="small" />
                    <span>Eliminar</span>
                  </button>
                </va-dropdown-content>
              </va-dropdown>
            </div>
          </div>
        </article>

        <!-- ✅ Separador si hay review del usuario -->
        <div v-if="userReview && otherReviews.length > 0" class="reviews-separator">
          <span>Otras reseñas</span>
        </div>

        <!-- ✅ Otras reviews -->
        <article 
          v-for="review in otherReviews" 
          :key="review.id"
          class="review-item"
        >
          <!-- Header -->
          <div class="review-header">
            <div class="reviewer-info">
              <div class="avatar">
                <img :src="review.user_avatar" :alt="review.user_name">
              </div>
              <div class="reviewer-details">
                <div class="reviewer-name-row">
                  <h4 class="reviewer-name">{{ review.user_name }}</h4>
                  
                </div>
                <time class="review-date">{{ formatDate(review.created_at) }}</time>
              </div>
            </div>
            
            <div class="review-rating-stars" @click="handleCalificar" title="Calificar este servicio">
              <span v-for="n in 5" :key="n" class="star" :class="{ filled: n <= review.rating }">
                ★
              </span>
            </div>
          </div>

          <!-- Content -->
          <div class="review-content">
            <p class="review-text">{{ review.review }}</p>
          </div>

          <!-- Footer con acciones -->
          <div class="review-footer">
            <div class="review-stats">
              <span v-if="review.helpful_count > 0" class="helpful-count">
                <va-icon name="thumb_up" size="small" />
                {{ review.helpful_count }} {{ review.helpful_count === 1 ? 'persona' : 'personas' }}
              </span>
            </div>
            
            <div class="review-actions">
              <button 
                @click="toggleHelpful(review.id)" 
                :class="['action-btn', 'helpful-btn', { active: isMarkedHelpful(review.id) }]"
              >
                <va-icon :name="isMarkedHelpful(review.id) ? 'thumb_up' : 'thumb_up_outline'" size="small" />
                <span>{{ isMarkedHelpful(review.id) ? 'Útil' : 'Marcar útil' }}</span>
              </button>
              
              <va-dropdown placement="bottom-end">
                <template #anchor>
                  <button class="action-btn more-btn">
                    <va-icon name="more_vert" size="small" />
                  </button>
                </template>
                <va-dropdown-content class="actions-dropdown">
                  <button @click="handleReport(review.id)" class="dropdown-item">
                    <va-icon name="flag" size="small" />
                    <span>Reportar</span>
                  </button>
                  <button v-if="review.is_mine" @click="handleEdit(review.id)" class="dropdown-item">
                    <va-icon name="edit" size="small" />
                    <span>Editar</span>
                  </button>
                  <button v-if="review.is_mine" @click="handleDelete(review.id)" class="dropdown-item danger">
                    <va-icon name="delete" size="small" />
                    <span>Eliminar</span>
                  </button>
                </va-dropdown-content>
              </va-dropdown>
            </div>
          </div>
        </article>
      </div>
    </div>

    <!-- Modal de calificación -->
    <Teleport to="body">
    <va-modal
      v-model="mostrarFormulario"
      size="medium"
      :hide-default-actions="true"
      no-padding
    >
      <div class="rating-modal">
        <div class="modal-header">
          <h3>Escribe tu reseña</h3>
          <p class="modal-subtitle">Comparte tu experiencia para ayudar a otros</p>
        </div>

        <div class="modal-body">
          <!-- Calificación con estrellas -->
          <div class="rating-input-section">
            <label class="input-label">Tu calificación</label>
            <div class="star-input">
              <button 
                v-for="n in 5" 
                :key="n"
                @click="ratingSeleccionado = n"
                type="button"
                class="star-input-btn"
                :class="{ active: n <= ratingSeleccionado }"
              >
                <va-icon :name="n <= ratingSeleccionado ? 'star' : 'star_outline'" size="2.5rem" />
              </button>
            </div>
            <span v-if="ratingSeleccionado > 0" class="rating-text">
              {{ getRatingText(ratingSeleccionado) }}
            </span>
          </div>

          <!-- Comentario -->
          <div class="comment-section">
            <label class="input-label">Tu opinión (opcional)</label>
            <va-textarea
              v-model="comentario"
              placeholder="Cuéntanos más sobre tu experiencia..."
              :max-length="500"
              :min-rows="4"
              counter
              class="full-width-textarea"
            />
          </div>

          <!-- Guías -->
          <div class="guidelines">
            <va-icon name="info" size="small" color="info" />
            <span>Describe tu experiencia, sé específico y mantén un lenguaje respetuoso.</span>
          </div>
        </div>

        <div class="modal-footer">
          <va-button preset="secondary" @click="cerrarFormulario">
            Cancelar
          </va-button>
          <va-button 
            @click="enviarCalificacion"
            :disabled="ratingSeleccionado === 0"
            :loading="enviando"
          >
            Publicar reseña
          </va-button>
        </div>
      </div>
    </va-modal>
    </Teleport>

    <!-- Modal de reporte -->
    <Teleport to="body">
    <va-modal
      v-model="mostrarModalReporte"
      title="Reportar reseña"
      size="small"
      :hide-default-actions="true"
    >
      <div class="report-modal">
        <p class="report-description">¿Por qué quieres reportar esta reseña?</p>
        
        <va-radio
          v-for="reason in reportReasons"
          :key="reason.value"
          v-model="motivoReporte"
          :option="reason"
          class="report-option"
        />

        <div class="report-actions">
          <va-button preset="secondary" @click="mostrarModalReporte = false">
            Cancelar
          </va-button>
          <va-button 
            @click="enviarReporte"
            :disabled="!motivoReporte"
            :loading="enviandoReporte"
          >
            Enviar reporte
          </va-button>
        </div>
      </div>
    </va-modal>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'

const props = defineProps({
  entityType: { type: String, required: true },
  entityId: { type: [String, Number], required: true },
  entityTitle: { type: String, default: '' }
})

const authStore = useAuthStore()

// Estados
const mostrarFormulario = ref(false)
const mostrarModalReporte = ref(false)
const ratingSeleccionado = ref(0)
const comentario = ref('')
const enviando = ref(false)
const enviandoReporte = ref(false)
const filtroOrden = ref('recientes')
const motivoReporte = ref('')
const reviewIdReporte = ref(null)

// Data mock
const resenasUtiles = ref([]) // IDs de reviews marcadas como útiles por este usuario
const reviews = ref([
  {
    id: 1,
    user_id: 100, // ✅ AGREGADO: ID diferente al usuario actual
    user_name: 'Carlos Mamani',
    user_avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Carlos',
    rating: 5,
    review: 'Excelente atención profesional. Muy recomendable. El servicio fue impecable y cumplieron con todos los tiempos establecidos.',
    created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    helpful_count: 12,
    is_verified: true,
    is_mine: false,
    helpful_users: []
  },
  {
    id: 2,
    user_id: 101, // ✅ AGREGADO
    user_name: 'María Quispe',
    user_avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Maria',
    rating: 4,
    review: 'Buen trabajo, aunque demoró un poco más de lo esperado. Sin embargo, el resultado final fue satisfactorio.',
    created_at: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(),
    helpful_count: 8,
    is_verified: false,
    is_mine: false,
    helpful_users: []
  },
  {
    id: 3,
    user_id: 102, // ✅ AGREGADO
    user_name: 'José Condori',
    user_avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jose',
    rating: 3,
    review: 'Regular atención. El trabajo estuvo bien pero sin destacar.',
    created_at: new Date(Date.now() - 23 * 24 * 60 * 60 * 1000).toISOString(),
    helpful_count: 3,
    is_verified: true,
    is_mine: false,
    helpful_users: []
  }
])

const ordenOptions = [
  { text: 'Más recientes', value: 'recientes' },
  { text: 'Más antiguas', value: 'antiguas' },
  { text: 'Mejor calificadas', value: 'mejor' },
  { text: 'Más útiles', value: 'utiles' }
]

const reportReasons = [
  { text: 'Spam o contenido irrelevante', value: 'spam' },
  { text: 'Lenguaje ofensivo o inapropiado', value: 'offensive' },
  { text: 'Información falsa o engañosa', value: 'false_info' },
  { text: 'Conflicto de interés', value: 'conflict' },
  { text: 'Otro motivo', value: 'other' }
]

// Computed
const estaLogueado = computed(() => authStore.isAuthenticated)

// ✅ NUEVO: Separar review del usuario
const userReview = computed(() => {
  if (!estaLogueado.value || !authStore.user?.id) return null
  return reviews.value.find(r => r.user_id === authStore.user.id)
})

// ✅ NUEVO: Reviews sin la del usuario (para mostrar después)
const otherReviews = computed(() => {
  if (!userReview.value) return reviews.value
  return reviews.value.filter(r => r.id !== userReview.value.id)
})

// Métodos
const getCount = (star) => {
  return reviews.value.filter(r => r.rating === star).length
}

const getPercentage = (star) => {
  const total = reviews.value.length
  if (total === 0) return 0
  return Math.round((getCount(star) / total) * 100)
}

const isMarkedHelpful = (reviewId) => {
  return resenasUtiles.value.includes(reviewId)
}

const handleCalificar = () => {
  if (!estaLogueado.value) {
    mostrarAuthModal.value = true
  } else {
    abrirFormulario()
  }
}

const abrirFormulario = () => {
  mostrarFormulario.value = true
  ratingSeleccionado.value = 0
  comentario.value = ''
}

const cerrarFormulario = () => {
  mostrarFormulario.value = false
  ratingSeleccionado.value = 0
  comentario.value = ''
}

const handleLoginSuccess = () => {
  mostrarAuthModal.value = false
  setTimeout(() => {
    abrirFormulario()
  }, 300)
}

const getRatingText = (rating) => {
  const texts = {
    1: 'Muy insatisfecho',
    2: 'Insatisfecho',
    3: 'Neutral',
    4: 'Satisfecho',
    5: 'Muy satisfecho'
  }
  return texts[rating] || ''
}

const toggleHelpful = (reviewId) => {
  if (!estaLogueado.value) {
    mostrarAuthModal.value = true
    return
  }
  
  const index = resenasUtiles.value.indexOf(reviewId)
  const review = reviews.value.find(r => r.id === reviewId)
  
  if (index > -1) {
    // Desmarcar
    resenasUtiles.value.splice(index, 1)
    review.helpful_count--
    console.log('❌ Desmarcado como útil:', {
      review_id: reviewId,
      user_id: authStore.user?.id
    })
  } else {
    // Marcar
    resenasUtiles.value.push(reviewId)
    review.helpful_count++
    console.log('✅ Marcado como útil:', {
      review_id: reviewId,
      user_id: authStore.user?.id
    })
  }
  
  // TODO: POST /api/ratings/{reviewId}/helpful/
}

const handleReport = (reviewId) => {
  if (!estaLogueado.value) {
    mostrarAuthModal.value = true
    return
  }
  
  reviewIdReporte.value = reviewId
  mostrarModalReporte.value = true
}

const enviarReporte = async () => {
  enviandoReporte.value = true
  
  console.log('🚨 Reporte enviado:', {
    review_id: reviewIdReporte.value,
    user_id: authStore.user?.id,
    reason: motivoReporte.value
  })
  
  // TODO: POST /api/ratings/{reviewId}/report/
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  enviandoReporte.value = false
  mostrarModalReporte.value = false
  motivoReporte.value = ''
}

const handleEdit = (reviewId) => {
  const review = reviews.value.find(r => r.id === reviewId)
  if (!review) return
  
  // Pre-llenar formulario con datos existentes
  ratingSeleccionado.value = review.rating
  comentario.value = review.review || ''
  
  // Abrir formulario
  mostrarFormulario.value = true
  
  console.log('✏️ Editando reseña:', reviewId)
}

const handleDelete = (reviewId) => {
  if (confirm('¿Estás seguro de eliminar tu reseña?')) {
    // Eliminar del array
    const index = reviews.value.findIndex(r => r.id === reviewId)
    if (index > -1) {
      reviews.value.splice(index, 1)
      console.log('🗑️ Reseña eliminada:', reviewId)
    }
    
    // TODO: DELETE /api/ratings/{reviewId}/ cuando se conecte Django
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'Hoy'
  if (diffDays === 1) return 'Ayer'
  if (diffDays < 7) return `Hace ${diffDays} días`
  if (diffDays < 30) return `Hace ${Math.floor(diffDays / 7)} semanas`
  if (diffDays < 365) return `Hace ${Math.floor(diffDays / 30)} meses`
  return `Hace ${Math.floor(diffDays / 365)} años`
}

const enviarCalificacion = async () => {
  if (ratingSeleccionado.value === 0) return
  
  enviando.value = true
  
  // Buscar si ya existe una review del usuario
  const existingReviewIndex = reviews.value.findIndex(r => r.user_id === authStore.user?.id)
  const isEditing = existingReviewIndex > -1
  
  console.log(isEditing ? '✏️ Actualizando calificación:' : '📊 Enviando calificación:', {
    entity_type: props.entityType,
    entity_id: props.entityId,
    rating: ratingSeleccionado.value,
    review: comentario.value,
    user_id: authStore.user?.id,
    user_name: authStore.user?.name
  })
  
  // TODO: POST /api/ratings/ (crear) o PUT /api/ratings/{id}/ (actualizar)
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  if (isEditing) {
    // ✅ ACTUALIZAR: Modificar review existente
    reviews.value[existingReviewIndex] = {
      ...reviews.value[existingReviewIndex],
      rating: ratingSeleccionado.value,
      review: comentario.value,
      created_at: reviews.value[existingReviewIndex].created_at, // Mantener fecha original
      updated_at: new Date().toISOString() // Nueva fecha de actualización
    }
    console.log('✅ Review actualizada')
  } else {
    // ✅ CREAR: Nueva review
    const nuevaReview = {
      id: Date.now(),
      user_id: authStore.user?.id,
      user_name: authStore.user?.name || 'Usuario',
      user_avatar: authStore.user?.avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${authStore.user?.name}`,
      rating: ratingSeleccionado.value,
      review: comentario.value,
      created_at: new Date().toISOString(),
      helpful_count: 0,
      is_verified: false,
      is_mine: true,
      helpful_users: []
    }
    
    reviews.value.unshift(nuevaReview)
    console.log('✅ Review creada')
  }
  
  enviando.value = false
  cerrarFormulario()
}
</script>

<style scoped>
.rating-system {
  width: 100%;
}

/* Header */
.rating-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.rating-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.rating-number {
  font-size: 3rem;
  font-weight: 700;
  color: #1F2937;
  line-height: 1;
}

.stars-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stars-clickeable {
  font-size: 1.25rem;
  cursor: pointer;
  display: flex;
  gap: 2px;
  transition: all 0.2s;
}

.stars-clickeable:hover {
  transform: scale(1.05);
}

.stars-clickeable .star {
  color: #E5E7EB;
  transition: color 0.2s;
}

.stars-clickeable .star.filled {
  color: #FFC107;
}

.total-text {
  font-size: 0.875rem;
  color: #6B7280;
}

.btn-calificar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #5C0099;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-calificar:hover {
  background: #7B00CC;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

/* Distribución */
.distribucion {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.5rem;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.dist-fila {
  display: grid;
  grid-template-columns: 20px 20px 1fr 40px;
  align-items: center;
  gap: 0.75rem;
}

.star-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  text-align: right;
}

.barra-container {
  height: 8px;
  background: #F3F4F6;
  border-radius: 4px;
  overflow: hidden;
}

.barra-fill {
  height: 100%;
  background: linear-gradient(90deg, #5C0099, #8B00CC);
  transition: width 0.5s ease;
}

.star-count {
  font-size: 0.875rem;
  color: #6B7280;
  text-align: center;
}

/* Reviews Section */
.reviews-section {
  margin-top: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1F2937;
}

.order-select {
  min-width: 180px;
}

/* Review Item */
.review-item {
  padding: 1.5rem;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  margin-bottom: 1rem;
  transition: all 0.3s;
}

.review-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border-color: #D1D5DB;
}

/* ✅ Review del usuario destacada */
.user-review-highlight {
  border: 2px solid #3B82F6;
  background: linear-gradient(135deg, #F8FAFF 0%, #FFFFFF 100%);
  position: relative;
}

.user-review-highlight:hover {
  border-color: #2563EB;
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.15);
}

.user-review-badge {
  position: absolute;
  top: -12px;
  left: 20px;
  background: #3B82F6;
  color: white;
  padding: 0.35rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

/* ✅ Separador de reviews */
.reviews-separator {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
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

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.reviewer-info {
  display: flex;
  gap: 0.75rem;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #E5E7EB;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.reviewer-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.reviewer-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.reviewer-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1F2937;
}

.review-date {
  font-size: 0.875rem;
  color: #6B7280;
}

.review-rating-stars {
  font-size: 1rem;
  color: #FFC107;
  cursor: pointer;
  transition: transform 0.2s;
}

.review-rating-stars:hover {
  transform: scale(1.05);
}

.review-rating-stars .star {
  color: #E5E7EB;
}

.review-rating-stars .star.filled {
  color: #FFC107;
}

.review-content {
  margin-bottom: 1rem;
}

.review-text {
  margin: 0;
  color: #374151;
  line-height: 1.6;
  font-size: 0.9375rem;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #F3F4F6;
}

.review-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.helpful-count {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  color: #6B7280;
}

.review-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.75rem;
  background: transparent;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.action-btn:hover {
  background: #F9FAFB;
  border-color: #D1D5DB;
}

.helpful-btn.active {
  background: #EFF6FF;
  border-color: #3B82F6;
  color: #3B82F6;
}

.more-btn {
  padding: 0.5rem;
}

.actions-dropdown {
  min-width: 160px;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  text-align: left;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #F3F4F6;
}

.dropdown-item.danger {
  color: #DC2626;
}

.dropdown-item.danger:hover {
  background: #FEF2F2;
}

/* Modal */
.rating-modal {
  background: white;
}

.modal-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid #E5E7EB;
}

.modal-header h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1F2937;
}

.modal-subtitle {
  margin: 0;
  font-size: 0.875rem;
  color: #6B7280;
}

.modal-body {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rating-input-section {
  margin-bottom: 2rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.input-label {
  display: block;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #374151;
  font-size: 1rem;
}

.star-input {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  justify-content: center;
}

.star-input-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #D1D5DB;
  transition: all 0.2s;
  padding: 0.25rem;
}

.star-input-btn:hover,
.star-input-btn.active {
  color: #FFC107;
  transform: scale(1.15);
}

.rating-text {
  font-size: 1rem;
  color: #5C0099;
  font-weight: 600;
}

.comment-section {
  margin-bottom: 1.5rem;
  width: 100%;
}

.comment-section .input-label {
  text-align: left;
}

.full-width-textarea {
  width: 100% !important;
}

:deep(.full-width-textarea .va-input-wrapper) {
  width: 100% !important;
}

:deep(.full-width-textarea textarea) {
  width: 100% !important;
  box-sizing: border-box;
}

.guidelines {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1.25rem;
  background: #F0F9FF;
  border-left: 4px solid #3B82F6;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #1E40AF;
  width: 100%;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1rem 2rem 2rem;
}

/* Report Modal */
.report-modal {
  padding: 1.5rem 0;
}

.report-description {
  margin: 0 0 1.5rem 0;
  color: #374151;
}

.report-option {
  margin-bottom: 0.75rem;
}

.report-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E5E7EB;
}

@media (max-width: 768px) {
  .rating-header {
    flex-direction: column;
    gap: 1.5rem;
  }

  .btn-calificar {
    width: 100%;
    justify-content: center;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .review-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .review-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style>