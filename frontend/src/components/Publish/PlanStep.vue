<!-- frontend/src/components/Publish/PlanStep.vue -->
<template>
  <div class="plan-step">
    <div class="plan-container">
      <div class="header-section">
        <h2 class="step-title">Elige tu Plan</h2>
        <p class="step-description">
          Selecciona el plan que mejor se adapte a tus necesidades de publicación
        </p>
      </div>

      <!-- Grid de Planes -->
      <div class="plans-grid">
        <!-- Plan Escencial (35 Bs) -->
        <div
          @click="selectPlan('escencial')"
          class="plan-card"
          :class="{ selected: selectedPlan === 'escencial' }"
        >
          <div class="plan-tier">Plan</div>
          <h3 class="plan-name">Escencial</h3>
          <div class="plan-price-block">
            <span class="plan-price">35</span>
            <span class="plan-currency">Bs.</span>
          </div>
          <p class="plan-period">15 días</p>

          <div class="plan-divider"></div>

          <!-- Badges de características -->
          <div class="plan-badges">
            <span class="badge badge-basic">Básico</span>
          </div>

          <ul class="plan-features">
            <li>Visibilidad Normal</li>
            <li>1 Aviso de Trabajo</li>
            <li>1 Post en Redes</li>
          </ul>

          <button
            @click.stop="selectPlan('escencial')"
            class="plan-select-btn"
            :class="{ active: selectedPlan === 'escencial' }"
          >
            {{ selectedPlan === 'escencial' ? 'Seleccionado' : 'Seleccionar' }}
          </button>
        </div>

        <!-- Plan Púrpura (79 Bs) - DESTACADO -->
        <div
          @click="selectPlan('purpura')"
          class="plan-card featured"
          :class="{ selected: selectedPlan === 'purpura' }"
        >
          <div class="plan-badge">Recomendado</div>
          <div class="plan-tier">Plan</div>
          <h3 class="plan-name">Púrpura</h3>
          <div class="plan-price-block">
            <span class="plan-price">79</span>
            <span class="plan-currency">Bs.</span>
          </div>
          <p class="plan-period">30 días</p>

          <div class="plan-divider"></div>

          <!-- Badges de características -->
          <div class="plan-badges">
            <span class="badge badge-featured">Destacado</span>
            <span class="badge badge-urgent">Urgente</span>
          </div>

          <ul class="plan-features">
            <li>Destacado (10 días)</li>
            <li>1 Aviso de Trabajo</li>
            <li>4 Posts en Redes</li>
            <li>Etiqueta Urgente</li>
            <li>1 Cambio Incluido</li>
          </ul>

          <button
            @click.stop="selectPlan('purpura')"
            class="plan-select-btn"
            :class="{ active: selectedPlan === 'purpura' }"
          >
            {{ selectedPlan === 'purpura' ? 'Seleccionado' : 'Seleccionar' }}
          </button>
        </div>

        <!-- Plan Impulso Pro (169 Bs) -->
        <div
          @click="selectPlan('impulso')"
          class="plan-card"
          :class="{ selected: selectedPlan === 'impulso' }"
        >
          <div class="plan-tier">Plan</div>
          <h3 class="plan-name">Impulso Pro</h3>
          <div class="plan-price-block">
            <span class="plan-price">169</span>
            <span class="plan-currency">Bs.</span>
          </div>
          <p class="plan-period">30 días</p>

          <div class="plan-divider"></div>

          <!-- Badges de características -->
          <div class="plan-badges">
            <span class="badge badge-sponsored">Patrocinado</span>
            <span class="badge badge-urgent">Urgente</span>
          </div>

          <ul class="plan-features">
            <li>Patrocinado (10 días)</li>
            <li>Hasta 3 Avisos</li>
            <li>6 Posts en Redes</li>
            <li>Etiqueta Urgente</li>
            <li>1 Cambio por Aviso</li>
          </ul>

          <button
            @click.stop="selectPlan('impulso')"
            class="plan-select-btn"
            :class="{ active: selectedPlan === 'impulso' }"
          >
            {{ selectedPlan === 'impulso' ? 'Seleccionado' : 'Seleccionar' }}
          </button>
        </div>
      </div>

      <!-- Comparison Table -->
      <div class="comparison-section">
        <h3 class="comparison-title">Comparación de Planes</h3>

        <div class="comparison-table">
          <div class="comparison-row header">
            <div class="feature-name">Característica</div>
            <div class="plan-col">Escencial</div>
            <div class="plan-col">Púrpura</div>
            <div class="plan-col">Impulso Pro</div>
          </div>

          <div class="comparison-row">
            <div class="feature-name">Precio</div>
            <div class="plan-col">35 Bs.</div>
            <div class="plan-col featured-text">79 Bs.</div>
            <div class="plan-col">169 Bs.</div>
          </div>

          <div class="comparison-row">
            <div class="feature-name">Duración</div>
            <div class="plan-col">15 días</div>
            <div class="plan-col featured-text">30 días</div>
            <div class="plan-col">30 días</div>
          </div>

          <div class="comparison-row">
            <div class="feature-name">Avisos</div>
            <div class="plan-col">1</div>
            <div class="plan-col featured-text">1</div>
            <div class="plan-col">Hasta 3</div>
          </div>

          <div class="comparison-row">
            <div class="feature-name">Visibilidad en la Web (Anchado)</div>
            <div class="plan-col">Normal</div>
            <div class="plan-col featured-text">Destacado</div>
            <div class="plan-col">Patrocinado</div>
          </div>

          <div class="comparison-row">
            <div class="feature-name">Posts Redes</div>
            <div class="plan-col">1</div>
            <div class="plan-col featured-text">4</div>
            <div class="plan-col">6</div>
          </div>

          <div class="comparison-row">
            <div class="feature-name">Etiqueta Urgente</div>
            <div class="plan-col">No</div>
            <div class="plan-col featured-text">Sí</div>
            <div class="plan-col">Sí</div>
          </div>

          <div class="comparison-row">
            <div class="feature-name">Cambios</div>
            <div class="plan-col">No</div>
            <div class="plan-col featured-text">1 cambio</div>
            <div class="plan-col">1 por aviso</div>
          </div>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="navigation-buttons">
        <button class="btn btn-secondary" @click="$emit('back')">
          Atrás
        </button>
        <button class="btn btn-primary" @click="handleNext">
          Siguiente
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'escencial'
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])

const selectedPlan = ref(props.modelValue)

const selectPlan = (plan) => {
  selectedPlan.value = plan
  emit('update:modelValue', plan)
}

const validate = () => {
  return !!selectedPlan.value
}

const handleNext = () => {
  if (validate()) {
    emit('next')
  }
}

watch(() => props.modelValue, (newValue) => {
  selectedPlan.value = newValue
})

defineExpose({
  validate
})
</script>

<style scoped>
.plan-step {
  padding: 2rem;
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  min-height: 100vh;
}

.plan-container {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  background: white;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.step-title {
  font-size: 2rem;
  font-weight: 800;
  color: #1F2937;
  margin: 0 0 0.75rem 0;
  letter-spacing: -0.5px;
}

.step-description {
  color: #6B7280;
  font-size: 1rem;
  margin: 0;
  line-height: 1.6;
  font-weight: 500;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem;
  margin-bottom: 3rem;
  padding: 0 0.5rem;
}

.plan-card {
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 20px;
  padding: 2.5rem 2rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.plan-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.15);
  border-color: #D1D5DB;
}

.plan-card.selected {
  border-color: var(--color-purple);
  box-shadow: 0 16px 40px rgba(124, 58, 237, 0.2);
  background: linear-gradient(135deg, #FAFBFF 0%, #F5F3FF 100%);
}

.plan-card.featured {
  border: 2px solid var(--color-purple);
  background: linear-gradient(135deg, #FAFBFF 0%, #F5F3FF 100%);
  transform: scale(1.04);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.12);
}

.plan-card.featured:hover {
  transform: scale(1.04) translateY(-12px);
  box-shadow: 0 32px 64px rgba(124, 58, 237, 0.2);
  border-color: var(--color-purple);
}

.plan-card.featured.selected {
  border-color: var(--color-purple);
  box-shadow: 0 24px 48px rgba(124, 58, 237, 0.25);
}

.plan-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 0.6rem 1.25rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 900;
  white-space: nowrap;
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
  animation: float-badge 3s ease-in-out infinite;
}

@keyframes float-badge {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-4px);
  }
}

/* BADGES DE CARACTERÍSTICAS */
.plan-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 1rem 0;
  justify-content: center;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.badge-basic {
  background: #F0F4F8;
  color: #475569;
  border: 1px solid #CBD5E1;
}

.badge-featured {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  color: white;
  border: 1px solid rgba(124, 58, 237, 0.5);
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.badge-sponsored {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
  border: 1px solid rgba(16, 185, 129, 0.5);
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.badge-urgent {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  color: white;
  border: 1px solid rgba(220, 38, 38, 0.5);
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
}

.plan-tier {
  font-size: 0.75rem;
  font-weight: 700;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
}

.plan-name {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1F2937;
  margin: 0 0 1rem 0;
  letter-spacing: -0.3px;
}

.plan-price-block {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin: 1rem 0 0.75rem 0;
  padding: 1.5rem 0;
  background: linear-gradient(135deg, #F5F3FF 0%, #FAFBFF 100%);
  border-radius: 12px;
  justify-content: center;
}

.plan-price {
  font-size: 3.5rem;
  font-weight: 900;
  color: var(--color-purple);
  line-height: 1;
  letter-spacing: -1px;
}

.plan-currency {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-purple);
  margin-top: 0.75rem;
  opacity: 0.8;
}

.plan-period {
  font-size: 0.85rem;
  color: #9CA3AF;
  margin: 0 0 1.5rem 0;
  font-weight: 500;
}

.plan-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, #E5E7EB, transparent);
  margin: 1.5rem 0;
}

/* Glow effect for featured card */
.plan-card.featured::after {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), transparent);
  border-radius: 20px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.plan-features {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.plan-features li {
  font-size: 0.9rem;
  color: #4B5563;
  font-weight: 500;
  line-height: 1.6;
  padding-left: 1.5rem;
  position: relative;
}

.plan-features li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--color-purple);
  font-weight: 700;
  font-size: 1.1rem;
}

.plan-select-btn {
  width: 100%;
  padding: 1rem 1.5rem;
  background: white;
  border: 2px solid var(--color-purple);
  color: var(--color-purple);
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.plan-select-btn:hover {
  background: var(--color-purple);
  color: white;
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35);
  transform: translateY(-2px);
}

.plan-select-btn.active {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35);
  border-color: transparent;
}

/* Comparison Section */
.comparison-section {
  background: #F9FAFB;
  border-radius: 16px;
  padding: 2.5rem;
  margin-bottom: 2rem;
  border: 1px solid #E5E7EB;
}

.comparison-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 2rem 0;
  text-align: center;
}

.comparison-table {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.comparison-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1.25rem 1rem;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  align-items: center;
}

.comparison-row:last-child {
  border-bottom: none;
}

.comparison-row.header {
  background: var(--color-purple);
  color: white;
  font-weight: 700;
  border-bottom: none;
  border-radius: 8px 8px 0 0;
}

.feature-name {
  font-weight: 600;
  color: #374151;
}

.comparison-row.header .feature-name {
  color: white;
  font-weight: 700;
}

.plan-col {
  text-align: center;
  color: #6B7280;
  font-weight: 500;
}

.comparison-row.header .plan-col {
  color: white;
  font-weight: 700;
}

.plan-col.featured-text {
  color: var(--color-purple);
  font-weight: 700;
}

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  margin-top: 2rem;
  border-top: 1px solid #E5E7EB;
}

.btn {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.3);
}

.btn-secondary {
  background: #F3F4F6;
  color: #1F2937;
  border: 2px solid #E5E7EB;
  font-weight: 600;
}

.btn-secondary:hover {
  background: #E5E7EB;
  border-color: #D1D5DB;
}

@media (max-width: 1024px) {
  .plans-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .plan-card.featured {
    transform: scale(1);
  }
}

@media (max-width: 768px) {
  .plan-container {
    padding: 2rem 1.5rem;
  }

  .header-section {
    margin-bottom: 2rem;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .step-description {
    font-size: 0.9rem;
  }

  .plans-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .plan-card {
    padding: 2rem 1.5rem;
  }

  .plan-name {
    font-size: 1.5rem;
  }

  .plan-price {
    font-size: 2.25rem;
  }

  .plan-features {
    margin-bottom: 1.5rem;
    gap: 0.6rem;
  }

  .plan-features li {
    font-size: 0.85rem;
  }

  .comparison-section {
    padding: 1.5rem;
  }

  .comparison-row {
    grid-template-columns: 1.5fr repeat(3, 1fr);
    padding: 0.875rem 0.75rem;
    font-size: 0.85rem;
  }

  .comparison-title {
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
  }

  .navigation-buttons {
    flex-direction: column;
    padding-top: 1.5rem;
    margin-top: 1.5rem;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>