<!-- components/Rating/RatingStars.vue -->
<template>
  <div class="rating-stars-container" :class="{ 'compact-mode': compact }">
    <!-- Stars principales -->
    <div class="stars-wrapper">
      <button
        v-for="star in 5"
        :key="`star-${star}`"
        type="button"
        class="star-button"
        :class="{
          filled: star <= Math.floor(rating),
          half: star === Math.floor(rating) + 1 && hasHalfStar,
          interactive: !readOnly,
          compact: compact
        }"
        :disabled="readOnly"
        @click="handleStarClick(star)"
        @mouseenter="!readOnly && handleStarHover(star)"
        @mouseleave="!readOnly && resetPreview()"
        :aria-label="`${star} de 5 estrellas`"
      >
        <va-icon 
          name="star" 
          :size="starSize"
          :color="getStarColor(star)"
          class="star-icon"
        />
      </button>
    </div>

    <!-- Información adicional -->
    <div v-if="showValue || showTotal || showLabel" class="rating-info" :class="{ compact: compact }">
      <!-- Valor numérico -->
      <span v-if="showValue && rating > 0" class="rating-value" :class="{ compact: compact }">
        {{ formattedRating }}
      </span>

      <!-- Total de reseñas -->
      <span v-if="showTotal && totalReviews > 0" class="rating-total" :class="{ compact: compact }">
        ({{ totalReviews }} {{ totalReviews === 1 ? 'reseña' : 'reseñas' }})
      </span>

      <!-- Etiqueta descriptiva -->
      <span v-if="showLabel && !compact" class="rating-label">
        {{ ratingLabel }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// ========== PROPS ==========
const props = defineProps({
  // Valor del rating (0-5)
  rating: {
    type: Number,
    default: 0,
    validator: (value) => value >= 0 && value <= 5
  },
  
  // Total de reseñas
  totalReviews: {
    type: Number,
    default: 0
  },
  
  // Solo lectura
  readOnly: {
    type: Boolean,
    default: false
  },
  
  // Tamaño de las estrellas
  size: {
    type: String,
    default: '1.25rem',
    validator: (value) => ['small', 'medium', 'large'].includes(value) || value.includes('rem') || value.includes('px')
  },
  
  // Mostrar valor numérico
  showValue: {
    type: Boolean,
    default: true
  },
  
  // Mostrar total de reseñas
  showTotal: {
    type: Boolean,
    default: false
  },
  
  // Mostrar etiqueta descriptiva
  showLabel: {
    type: Boolean,
    default: false
  },
  
  // Modo compacto
  compact: {
    type: Boolean,
    default: false
  }
})

// ========== EMITS ==========
const emit = defineEmits(['rating-change', 'rating-hover'])

// ========== STATE ==========
const hoverRating = ref(0)

// ========== COMPUTED ==========
const starSize = computed(() => {
  if (props.compact) return '1rem'
  
  const sizeMap = {
    'small': '1rem',
    'medium': '1.25rem', 
    'large': '1.5rem'
  }
  
  return sizeMap[props.size] || props.size
})

const formattedRating = computed(() => {
  if (props.rating === 0) return '0.0'
  return props.rating % 1 === 0 ? props.rating.toFixed(0) : props.rating.toFixed(1)
})

const hasHalfStar = computed(() => {
  return props.rating % 1 !== 0 && props.rating % 1 >= 0.5
})

const ratingLabel = computed(() => {
  if (props.rating === 0) return 'Sin calificación'
  if (props.rating <= 1.5) return 'Muy malo'
  if (props.rating <= 2.5) return 'Malo'
  if (props.rating <= 3.5) return 'Regular'
  if (props.rating <= 4.5) return 'Bueno'
  return 'Excelente'
})

// ========== METHODS ==========
const getStarColor = (starNumber) => {
  const currentRating = hoverRating.value || props.rating
  
  if (starNumber <= currentRating) {
    // Estrella llena - usar color púrpura
    return 'var(--color-purple)'
  } else if (starNumber === Math.floor(currentRating) + 1 && hasHalfStar.value) {
    // Media estrella
    return 'var(--color-yellow-primary)'
  } else {
    // Estrella vacía
    return '#D1D5DB'
  }
}

const handleStarClick = (rating) => {
  if (props.readOnly) return
  emit('rating-change', rating)
}

const handleStarHover = (rating) => {
  if (props.readOnly) return
  hoverRating.value = rating
  emit('rating-hover', rating)
}

const resetPreview = () => {
  if (props.readOnly) return
  hoverRating.value = 0
  emit('rating-hover', 0)
}
</script>

<style scoped>
/* ========== Container ========== */
.rating-stars-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.rating-stars-container.compact-mode {
  gap: 0.5rem;
}

/* ========== Stars Wrapper ========== */
.stars-wrapper {
  display: flex;
  gap: 0.25rem;
}

.rating-stars-container.compact-mode .stars-wrapper {
  gap: 0.125rem;
}

/* ========== Star Buttons ========== */
.star-button {
  background: none;
  border: none;
  padding: 0.125rem;
  cursor: default;
  transition: all 0.2s ease;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.star-button.compact {
  padding: 0.0625rem;
}

.star-button.interactive {
  cursor: pointer;
}

.star-button.interactive:hover {
  transform: scale(1.1);
  background: rgba(92, 0, 153, 0.1);
}

.star-button:focus {
  outline: 2px solid var(--color-purple);
  outline-offset: 2px;
}

/* ========== Star Icons ========== */
.star-icon {
  transition: all 0.2s ease;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.star-button.filled .star-icon {
  color: var(--color-purple) !important;
}

.star-button.half .star-icon {
  background: linear-gradient(90deg, var(--color-purple) 50%, #D1D5DB 50%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ========== Rating Info ========== */
.rating-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.rating-info.compact {
  gap: 0.375rem;
}

.rating-value {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-purple);
  line-height: 1;
}

.rating-value.compact {
  font-size: 0.875rem;
}

.rating-total {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.rating-total.compact {
  font-size: 0.75rem;
}

.rating-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
  text-transform: capitalize;
}

/* ========== No Rating State ========== */
.rating-stars-container:has(.rating-value:contains('0.0')) .rating-total {
  color: #9CA3AF;
}

/* ========== Responsive ========== */
@media (max-width: 640px) {
  .rating-stars-container {
    gap: 0.5rem;
  }
  
  .rating-value {
    font-size: 0.875rem;
  }
  
  .rating-total {
    font-size: 0.75rem;
  }
  
  .rating-label {
    display: none; /* Ocultar en móvil para ahorrar espacio */
  }
}

/* ========== Animation ========== */
@keyframes starPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.star-button.interactive:active .star-icon {
  animation: starPulse 0.3s ease;
}

/* ========== High Contrast Mode ========== */
@media (prefers-contrast: high) {
  .star-button.filled .star-icon {
    color: #000000 !important;
  }
  
  .rating-value {
    color: #000000;
  }
}

/* ========== Reduced Motion ========== */
@media (prefers-reduced-motion: reduce) {
  .star-button,
  .star-icon {
    transition: none;
  }
  
  .star-button.interactive:active .star-icon {
    animation: none;
  }
}
</style>