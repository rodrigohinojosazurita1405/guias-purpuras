<template>
  <div class="star-rating">
    <button
      v-for="star in 5"
      :key="star"
      @click="setRating(star)"
      @mouseenter="hoveredRating = star"
      @mouseleave="hoveredRating = 0"
      class="star-btn"
      :class="{ 'filled': star <= (hoveredRating || modelValue) }"
      :disabled="disabled"
      type="button"
    >
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"
          :fill="star <= (hoveredRating || modelValue) ? '#7C3AED' : 'none'"
          :stroke="star <= (hoveredRating || modelValue) ? '#7C3AED' : '#D1D5DB'"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>
    <span v-if="showLabel && modelValue" class="rating-label">
      {{ modelValue }} / 5
    </span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    default: null
  },
  disabled: {
    type: Boolean,
    default: false
  },
  showLabel: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue'])

const hoveredRating = ref(0)

const setRating = (rating) => {
  if (props.disabled) return

  // Si se hace click en la misma estrella, quitar el rating
  if (rating === props.modelValue) {
    emit('update:modelValue', null)
  } else {
    emit('update:modelValue', rating)
  }
}
</script>

<style scoped>
.star-rating {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.star-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.star-btn:hover:not(:disabled) {
  transform: scale(1.2);
}

.star-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.star-btn.filled svg path {
  filter: drop-shadow(0 2px 4px rgba(124, 58, 237, 0.3));
}

.rating-label {
  margin-left: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #7C3AED;
}
</style>
