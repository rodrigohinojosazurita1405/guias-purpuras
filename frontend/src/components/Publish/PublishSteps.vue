<!-- frontend/src/components/Publish/PublishSteps.vue -->
<template>
  <div class="publish-steps">
    <!-- 
      ==========================================
      INDICADOR DE PASOS DEL FORMULARIO
      ==========================================
      Muestra visualmente en qué paso está el usuario
      Props:
        - currentStep: Número del paso actual (1-4)
        - steps: Array con nombres de los pasos
    -->
    
    <div 
      v-for="(step, index) in steps" 
      :key="index"
      class="step-item"
      :class="{ 
        active: currentStep === index + 1, 
        completed: currentStep > index + 1 
      }"
    >
      <!-- Número o check del paso -->
      <div class="step-number">
        <va-icon v-if="currentStep > index + 1" name="check" size="small" />
        <span v-else>{{ index + 1 }}</span>
      </div>

      <!-- Nombre del paso -->
      <span class="step-label">{{ step }}</span>

      <!-- Línea conectora (excepto en el último) -->
      <div v-if="index < steps.length - 1" class="step-line"></div>
    </div>
  </div>
</template>

<script setup>
// ==========================================
// PROPS
// ==========================================
defineProps({
  currentStep: {
    type: Number,
    required: true,
    default: 1,
    validator: (value) => value >= 1 && value <= 4
  },
  steps: {
    type: Array,
    required: true,
    default: () => ['Categoría', 'Información', 'Imágenes', 'Plan']
  }
})
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.publish-steps {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  position: relative;
  padding: 0 1rem;
}

/* ==========================================
   ITEM DE PASO
   ========================================== */
.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  position: relative;
  flex: 1;
  z-index: 2;
}

/* ==========================================
   NÚMERO/ICONO DEL PASO
   ========================================== */
.step-number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: white;
  border: 3px solid #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.125rem;
  color: #999;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* Paso activo */
.step-item.active .step-number {
  background: var(--color-purple);
  border-color: var(--color-purple);
  color: white;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

/* Paso completado */
.step-item.completed .step-number {
  background: var(--color-yellow-primary);
  border-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3);
}

/* ==========================================
   ETIQUETA DEL PASO
   ========================================== */
.step-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #999;
  transition: color 0.3s ease;
  text-align: center;
}

.step-item.active .step-label {
  color: var(--color-purple);
  font-weight: 700;
}

.step-item.completed .step-label {
  color: var(--color-purple-dark);
}

/* ==========================================
   LÍNEA CONECTORA
   ========================================== */
.step-line {
  position: absolute;
  top: 24px;
  left: calc(50% + 24px);
  width: calc(100% - 48px);
  height: 3px;
  background: #E0E0E0;
  z-index: 1;
  transition: background 0.3s ease;
}

.step-item.completed .step-line {
  background: var(--color-yellow-primary);
}

/* ==========================================
   RESPONSIVE - MOBILE
   ========================================== */
@media (max-width: 768px) {
  .publish-steps {
    margin-bottom: 2rem;
  }

  .step-number {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }

  .step-label {
    font-size: 0.8rem;
  }

  .step-line {
    top: 20px;
    left: calc(50% + 20px);
    width: calc(100% - 40px);
  }
}

@media (max-width: 480px) {
  .step-label {
    display: none; /* Oculta etiquetas en móviles muy pequeños */
  }

  .step-number {
    width: 36px;
    height: 36px;
  }
}
</style>