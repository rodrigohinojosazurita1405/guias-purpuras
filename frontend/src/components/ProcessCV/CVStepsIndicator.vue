<!-- frontend/src/components/CV/CVStepsIndicator.vue -->
<template>
  <div class="cv-steps-indicator">
    <div class="steps-container">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="step-item"
        :class="getStepClass(index)"
      >
        <!-- Círculo del paso -->
        <div class="step-circle">
          <div v-if="isCompleted(index)" class="step-check">
            <va-icon name="check" size="small" />
          </div>
          <span v-else class="step-number">{{ index + 1 }}</span>
        </div>

        <!-- Línea conectora -->
        <div v-if="index < steps.length - 1" class="step-line" :class="getLineClass(index)" />

        <!-- Nombre del paso -->
        <div class="step-info">
          <p class="step-name">{{ step.name }}</p>
          <p class="step-description">{{ step.description }}</p>
        </div>
      </div>
    </div>

    <!-- Barra de progreso -->
    <div class="progress-bar-container">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
      <p class="progress-text">Paso {{ currentStep + 1 }} de {{ steps.length }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentStep: {
    type: Number,
    required: true
  },
  steps: {
    type: Array,
    required: true
  }
})

const progressPercent = computed(() => {
  return ((props.currentStep + 1) / props.steps.length) * 100
})

const isCompleted = (index) => {
  return index < props.currentStep
}

const getStepClass = (index) => {
  return {
    active: index === props.currentStep,
    completed: index < props.currentStep,
    pending: index > props.currentStep
  }
}

const getLineClass = (index) => {
  return {
    completed: index < props.currentStep
  }
}
</script>

<style scoped>
.cv-steps-indicator {
  background: linear-gradient(135deg, #FFFFFF 0%, #F9F5FF 100%);
  padding: 1.5rem 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(124, 58, 237, 0.08);
  border: 1px solid rgba(124, 58, 237, 0.1);
  margin: 0 auto 2rem auto;
  max-width: 1200px;
  width: 100%;
}

.steps-container {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  padding: 1rem 0.5rem;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: fit-content;
  position: relative;
  flex: 0 0 auto;
  padding: 0.5rem 0;
  transition: all 0.3s ease;
}

/* Círculo del paso */
.step-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #E2E8F0;
  border: 2px solid #CBD5E1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  color: #64748B;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.step-item.completed .step-circle {
  background: #10B981;
  border-color: #059669;
  color: white;
}

.step-item.active .step-circle {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  border-color: #6D28D9;
  color: white;
  box-shadow: 0 0 0 8px rgba(124, 58, 237, 0.12), 0 4px 12px rgba(124, 58, 237, 0.25);
  transform: scale(1.05);
}

.step-item.pending .step-circle {
  background: #F8FAFC;
  border-color: #E2E8F0;
  color: #94A3B8;
}

.step-check {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Línea conectora */
.step-line {
  height: 3px;
  flex: 1;
  min-width: 30px;
  background: #E2E8F0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin: 0 -0.5rem;
  border-radius: 2px;
}

.step-line.completed {
  background: linear-gradient(90deg, #10B981 0%, #10B981 100%);
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

/* Información del paso */
.step-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.step-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: #1E293B;
  margin: 0;
  transition: color 0.3s ease;
}

.step-description {
  font-size: 0.8rem;
  color: #94A3B8;
  margin: 0;
}

.step-item.active .step-name {
  color: #7C3AED;
}

.step-item.completed .step-name {
  color: #10B981;
}

.step-item.pending .step-name {
  color: #CBD5E1;
}

/* Barra de progreso */
.progress-bar-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #E2E8F0;
  border-radius: 999px;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #7C3AED 0%, #A855F7 100%);
  border-radius: 999px;
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(124, 58, 237, 0.3);
}

.progress-text {
  font-size: 0.9rem;
  font-weight: 700;
  color: #7C3AED;
  margin: 0;
  text-align: center;
}

/* Responsive */
@media (max-width: 1024px) {
  .steps-container {
    gap: 0.5rem;
  }

  .step-circle {
    width: 40px;
    height: 40px;
    font-size: 0.9rem;
  }

  .step-info {
    max-width: 100px;
  }

  .step-name {
    font-size: 0.8rem;
  }

  .step-description {
    font-size: 0.7rem;
  }

  .step-line {
    min-width: 20px;
  }
}

@media (max-width: 768px) {
  .cv-steps-indicator {
    padding: 1rem;
    margin-bottom: 1rem;
  }

  .steps-container {
    gap: 0.25rem;
  }

  .step-circle {
    width: 32px;
    height: 32px;
    font-size: 0.8rem;
  }

  .step-info {
    max-width: 70px;
  }

  .step-name {
    font-size: 0.7rem;
  }

  .step-description {
    display: none;
  }

  .step-line {
    min-width: 10px;
  }
}
</style>
