<!-- components/Rating/ReviewItem.vue -->
<template>
  <article class="review-item" :class="{ 'verified': review.is_verified, 'highlighted': isHighlighted }">
    <!-- Header de la reseña -->
    <header class="review-header">
      <!-- Avatar y nombre del usuario -->
      <div class="reviewer-info">
        <div class="reviewer-avatar">
          <img 
            v-if="review.user_avatar" 
            :src="review.user_avatar" 
            :alt="review.user_name"
            class="avatar-image"
          />
          <div v-else class="avatar-placeholder">
            {{ getInitials(review.user_name) }}
          </div>
        </div>
        
        <div class="reviewer-details">
          <h4 class="reviewer-name">
            {{ review.user_name }}
            <span v-if="review.is_verified" class="verified-badge" title="Usuario verificado">
              <va-icon name="verified" size="small" color="success" />
            </span>
          </h4>
          <time class="review-date" :datetime="review.created_at">
            {{ formatDate(review.created_at) }}
          </time>
        </div>
      </div>

      <!-- Rating y acciones -->
      <div class="review-meta">
        <RatingStars
          :rating="review.rating"
          :read-only="true"
          size="1rem"
          class="review-rating"
        />
        
        <!-- Menú de acciones -->
        <va-dropdown class="review-actions">
          <template #anchor>
            <va-button 
              preset="plain" 
              size="small"
              icon="more_vert"
              color="secondary"
            />
          </template>
          
          <va-dropdown-content>
            <!-- Marcar como útil -->
            <button 
              v-if="canMarkHelpful"
              @click="handleMarkHelpful"
              class="dropdown-action"
              :disabled="isMarkingHelpful"
            >
              <va-icon name="thumb_up" size="small" />
              Marcar como útil
            </button>
            
            <!-- Reportar -->
            <button 
              v-if="canReport"
              @click="showReportModal = true"
              class="dropdown-action report-action"
            >
              <va-icon name="flag" size="small" />
              Reportar
            </button>
            
            <!-- Editar (solo autor) -->
            <button 
              v-if="isAuthor"
              @click="$emit('edit-review')"
              class="dropdown-action"
            >
              <va-icon name="edit" size="small" />
              Editar
            </button>
            
            <!-- Eliminar (solo autor) -->
            <button 
              v-if="isAuthor"
              @click="$emit('delete-review')"
              class="dropdown-action delete-action"
            >
              <va-icon name="delete" size="small" />
              Eliminar
            </button>
          </va-dropdown-content>
        </va-dropdown>
      </div>
    </header>

    <!-- Contenido de la reseña -->
    <div v-if="review.review" class="review-content">
      <p class="review-text" :class="{ 'expanded': isExpanded }">
        {{ isExpanded ? review.review : truncatedReview }}
      </p>
      
      <!-- Botón Ver más/menos -->
      <button 
        v-if="needsTruncation"
        @click="toggleExpanded"
        class="expand-btn"
      >
        {{ isExpanded ? 'Ver menos' : 'Ver más' }}
      </button>
    </div>

    <!-- Footer con estadísticas -->
    <footer class="review-footer">
      <!-- Votos útiles -->
      <div v-if="review.helpful_votes > 0" class="helpful-votes">
        <va-icon name="thumb_up" size="small" />
        <span>{{ review.helpful_votes }} {{ review.helpful_votes === 1 ? 'persona encontró' : 'personas encontraron' }} esto útil</span>
      </div>
      
      <!-- Respuesta del propietario (si existe) -->
      <div v-if="review.owner_response" class="owner-response">
        <div class="response-header">
          <va-icon name="store" size="small" />
          <span class="response-label">Respuesta del propietario</span>
          <time class="response-date">{{ formatDate(review.owner_response.created_at) }}</time>
        </div>
        <p class="response-text">{{ review.owner_response.message }}</p>
      </div>
    </footer>

    <!-- Modal de reporte -->
    <va-modal
      v-model="showReportModal"
      title="Reportar reseña"
      size="small"
      hide-default-actions
      @close="resetReportForm"
    >
      <div class="report-form">
        <p class="report-description">
          ¿Por qué quieres reportar esta reseña?
        </p>
        
        <va-radio
          v-for="reason in reportReasons"
          :key="reason.value"
          v-model="selectedReportReason"
          :option="reason"
          class="report-reason"
        />
        
        <va-textarea
          v-if="selectedReportReason === 'other'"
          v-model="customReportReason"
          placeholder="Describe el problema..."
          :max-length="200"
          class="report-details"
        />
        
        <div class="report-actions">
          <va-button 
            color="secondary" 
            @click="resetReportForm"
          >
            Cancelar
          </va-button>
          <va-button 
            color="danger"
            @click="handleReport"
            :loading="isReporting"
            :disabled="!selectedReportReason"
          >
            Reportar
          </va-button>
        </div>
      </div>
    </va-modal>
  </article>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'
import RatingStars from './RatingStars.vue'
import { formatRelativeDate as formatDate } from '@/composables/useRating' // ✅ Importado

// ========== PROPS ==========
const props = defineProps({
  // Objeto de reseña
  review: {
    type: Object,
    required: true
  },
  
  // Destacar esta reseña
  isHighlighted: {
    type: Boolean,
    default: false
  },
  
  // Longitud máxima antes de truncar
  maxLength: {
    type: Number,
    default: 200
  },
  
  // Permitir reportar
  allowReporting: {
    type: Boolean,
    default: true
  },
  
  // Permitir marcar como útil
  allowHelpful: {
    type: Boolean,
    default: true
  }
})

// ========== EMITS ==========
const emit = defineEmits(['mark-helpful', 'report', 'edit-review', 'delete-review'])

// ========== DEPENDENCIES ==========
const authStore = useAuthStore()

// ========== STATE ==========
const isExpanded = ref(false)
const showReportModal = ref(false)
const selectedReportReason = ref('')
const customReportReason = ref('')
const isMarkingHelpful = ref(false)
const isReporting = ref(false)

// ========== COMPUTED ==========

/**
 * ✅ Validación mejorada de autoría
 * Verifica que tanto el usuario actual como el user_id de la review existan
 */
const isAuthor = computed(() => {
  if (!authStore.user?.id || !props.review.user_id) {
    return false
  }
  return authStore.user.id === props.review.user_id
})

/**
 * Verificar si el usuario puede marcar como útil
 * - Debe estar autenticado
 * - No debe ser el autor
 * - No debe haberlo marcado antes
 */
const canMarkHelpful = computed(() => {
  return props.allowHelpful && 
         authStore.isAuthenticated && 
         !isAuthor.value &&
         !hasMarkedHelpful.value
})

/**
 * Verificar si el usuario puede reportar
 */
const canReport = computed(() => {
  return props.allowReporting && 
         authStore.isAuthenticated && 
         !isAuthor.value
})

/**
 * ✅ Verificar si el usuario ya marcó como útil
 * Usa la lista helpful_by del backend
 */
const hasMarkedHelpful = computed(() => {
  if (!authStore.user?.id || !props.review.helpful_by) {
    return false
  }
  return props.review.helpful_by.includes(authStore.user.id)
})

/**
 * Texto truncado de la reseña
 */
const truncatedReview = computed(() => {
  if (!props.review.review || props.review.review.length <= props.maxLength) {
    return props.review.review
  }
  return props.review.review.substring(0, props.maxLength) + '...'
})

/**
 * Verificar si necesita truncamiento
 */
const needsTruncation = computed(() => {
  return props.review.review && props.review.review.length > props.maxLength
})

// ========== DATA ==========
const reportReasons = [
  { text: 'Contenido inapropiado', value: 'inappropriate' },
  { text: 'Spam o publicidad', value: 'spam' },
  { text: 'Información falsa', value: 'fake' },
  { text: 'Lenguaje ofensivo', value: 'offensive' },
  { text: 'Información personal', value: 'personal_info' },
  { text: 'Otro motivo', value: 'other' }
]

// ========== METHODS ==========

/**
 * Obtener iniciales del nombre para el avatar
 */
const getInitials = (name) => {
  if (!name) return '?'
  const names = name.trim().split(' ')
  if (names.length > 1) {
    return `${names[0][0]}${names[1][0]}`.toUpperCase()
  }
  return names[0][0].toUpperCase()
}

/**
 * Alternar expansión del texto
 */
const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}

/**
 * Manejar marcar como útil
 */
const handleMarkHelpful = async () => {
  if (!canMarkHelpful.value) {
    return
  }
  
  isMarkingHelpful.value = true
  
  try {
    emit('mark-helpful', props.review.id)
  } finally {
    // Esperar un poco antes de habilitar el botón nuevamente
    setTimeout(() => {
      isMarkingHelpful.value = false
    }, 500)
  }
}

/**
 * Manejar reporte de reseña
 */
const handleReport = async () => {
  if (!selectedReportReason.value) {
    return
  }
  
  isReporting.value = true
  
  try {
    const reportData = {
      reason: selectedReportReason.value,
      details: selectedReportReason.value === 'other' ? customReportReason.value : null
    }
    
    emit('report', props.review.id, reportData)
    resetReportForm()
    
  } finally {
    isReporting.value = false
  }
}

/**
 * Resetear formulario de reporte
 */
const resetReportForm = () => {
  showReportModal.value = false
  selectedReportReason.value = ''
  customReportReason.value = ''
}
</script>

<style scoped>
/* ========== Container ========== */
.review-item {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
  transition: all 0.2s ease;
}

.review-item:hover {
  border-color: #D1D5DB;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.review-item.verified {
  border-left: 4px solid #10B981;
}

.review-item.highlighted {
  border-color: #3B82F6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
  background: #F8FAFF;
}

/* ========== Header ========== */
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  flex: 1;
}

.reviewer-avatar {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  color: white;
  font-weight: 600;
  font-size: 1.125rem;
}

.reviewer-details {
  flex: 1;
  min-width: 0;
}

.reviewer-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1F2937;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.verified-badge {
  display: flex;
  align-items: center;
}

.review-date {
  font-size: 0.875rem;
  color: #6B7280;
  margin-top: 0.125rem;
  display: block;
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.review-rating {
  flex-shrink: 0;
}

/* ========== Actions ========== */
.review-actions {
  position: relative;
}

.dropdown-action {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  text-align: left;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-action:hover {
  background: #F3F4F6;
  color: #1F2937;
}

.dropdown-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.report-action:hover {
  background: #FEF2F2;
  color: #DC2626;
}

.delete-action:hover {
  background: #FEF2F2;
  color: #DC2626;
}

/* ========== Content ========== */
.review-content {
  margin: 0.5rem 0;
}

.review-text {
  margin: 0 0 0.75rem 0;
  color: #374151;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.review-text.expanded {
  /* Estilos para texto expandido si necesario */
}

.expand-btn {
  background: none;
  border: none;
  color: #3B82F6;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s ease;
}

.expand-btn:hover {
  color: #2563EB;
  text-decoration: underline;
}

/* ========== Footer ========== */
.review-footer {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 0.5rem;
}

.helpful-votes {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6B7280;
  font-size: 0.875rem;
}

/* ========== Owner Response ========== */
.owner-response {
  padding: 1rem;
  background: #F8FAFC;
  border-radius: 8px;
  border-left: 3px solid #3B82F6;
}

.response-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.response-label {
  font-weight: 600;
  color: #1E40AF;
  font-size: 0.875rem;
}

.response-date {
  font-size: 0.8125rem;
  color: #6B7280;
  margin-left: auto;
}

.response-text {
  margin: 0;
  color: #374151;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* ========== Report Modal ========== */
.report-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.report-description {
  margin: 0;
  color: #6B7280;
  font-size: 0.95rem;
}

.report-reason {
  margin-bottom: 0.75rem;
}

.report-details {
  margin-top: 0.75rem;
}

.report-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .review-item {
    padding: 1rem;
  }
  
  .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .review-meta {
    align-self: flex-end;
    order: -1;
  }
  
  .reviewer-info {
    gap: 0.75rem;
  }
  
  .reviewer-avatar {
    width: 40px;
    height: 40px;
  }
  
  .avatar-placeholder {
    font-size: 1rem;
  }
  
  .reviewer-name {
    font-size: 0.95rem;
  }
  
  .review-date {
    font-size: 0.8125rem;
  }
  
  .report-actions {
    flex-direction: column-reverse;
  }
  
  .report-actions .va-button {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .review-item {
    padding: 0.875rem;
  }
  
  .reviewer-info {
    gap: 0.625rem;
  }
  
  .reviewer-avatar {
    width: 36px;
    height: 36px;
  }
  
  .avatar-placeholder {
    font-size: 0.875rem;
  }
  
  .review-text {
    font-size: 0.95rem;
  }
}

/* ========== Animation ========== */
.review-item {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>