<!-- frontend/src/components/Common/TabNavigation.vue -->
<template>
  <div class="tab-navigation">
    <div class="tab-buttons">
      <button
        v-for="(tab, index) in tabs"
        :key="index"
        class="tab-button"
        :class="{ active: modelValue === index }"
        @click="emit('update:modelValue', index)"
      >
        <va-icon v-if="tab.icon" :name="tab.icon" size="small" />
        {{ tab.label }}
      </button>
    </div>
    
    <div class="tab-content">
      <slot :name="`tab-${modelValue}`"></slot>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  tabs: {
    type: Array,
    required: true,
    // Example: [{ label: 'Tab 1', icon: 'info' }, { label: 'Tab 2', icon: 'settings' }]
  },
  modelValue: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update:modelValue'])
</script>

<style scoped>
.tab-navigation {
  width: 100%;
}

.tab-buttons {
  display: flex;
  gap: 0.5rem;
  border-bottom: 2px solid #E0E0E0;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  color: #666;
  transition: all 0.3s ease;
  margin-bottom: -2px;
}

.tab-button:hover {
  color: var(--color-purple);
  background: rgba(92, 0, 153, 0.05);
}

.tab-button.active {
  color: var(--color-purple);
  border-bottom-color: var(--color-purple);
}

.tab-content {
  animation: fadeIn 0.3s ease;
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

@media (max-width: 768px) {
  .tab-buttons {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .tab-buttons::-webkit-scrollbar {
    display: none;
  }

  .tab-button {
    padding: 0.875rem 1.25rem;
    font-size: 0.9rem;
    white-space: nowrap;
  }
}
</style>