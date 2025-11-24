<!-- frontend/src/components/Publish/PlanStep.vue -->
<template>
  <div class="plan-step">
    <h2 class="step-title">
      <va-icon name="workspace_premium" color="purple" size="large" />
      Elige tu Plan
    </h2>

    <p class="step-description">
      Selecciona el plan que mejor se adapte a tus necesidades
    </p>

    <!-- Grid de Planes -->
    <div class="plans-grid">
      <!-- Plan Escencial (35 Bs) -->
      <div
        @click="selectPlan('escencial')"
        class="plan-card"
        :class="{ selected: selectedPlan === 'escencial' }"
      >
        <div class="plan-header">
          <va-icon name="workspace_premium" size="2.5rem" color="success" />
          <h3 class="plan-name">Escencial</h3>
          <div class="plan-price">
            <span class="currency">Bs.</span>
            <span class="amount">35</span>
          </div>
          <span class="plan-duration">15 días (1 aviso)</span>
        </div>

        <div class="plan-features">
          <div class="feature-item">
            <va-icon name="check" size="small" color="success" />
            <span>Visibilidad Normal</span>
          </div>
          <div class="feature-item">
            <va-icon name="check" size="small" color="success" />
            <span>1 post en Facebook/Instagram</span>
          </div>
          <div class="feature-item">
            <va-icon name="remove" size="small" />
            <span>Etiqueta Urgente no incluida</span>
          </div>
          <div class="feature-item">
            <va-icon name="remove" size="small" />
            <span>Sin sustitución de aviso</span>
          </div>
        </div>

        <button
          @click.stop="selectPlan('escencial')"
          class="plan-button"
          :class="{ active: selectedPlan === 'escencial' }"
        >
          <va-icon v-if="selectedPlan === 'escencial'" name="check_circle" />
          {{ selectedPlan === 'escencial' ? 'Seleccionado' : 'Seleccionar' }}
        </button>
      </div>

      <!-- Plan Púrpura (79 Bs) -->
      <div
        @click="selectPlan('purpura')"
        class="plan-card featured"
        :class="{ selected: selectedPlan === 'purpura' }"
      >
        <div class="plan-badge">
          <va-icon name="star" size="small" />
          Recomendado
        </div>

        <div class="plan-header">
          <va-icon name="star" size="2.5rem" color="warning" />
          <h3 class="plan-name">Púrpura</h3>
          <div class="plan-price">
            <span class="currency">Bs.</span>
            <span class="amount">79</span>
          </div>
          <span class="plan-duration">30 días (1 aviso)</span>
        </div>

        <div class="plan-features">
          <div class="feature-item highlight">
            <va-icon name="check" size="small" color="warning" />
            <span>Destacado (10 días)</span>
          </div>
          <div class="feature-item highlight">
            <va-icon name="check" size="small" color="warning" />
            <span>1 FB/IG + 1 LinkedIn + 1 TikTok</span>
          </div>
          <div class="feature-item highlight">
            <va-icon name="check" size="small" color="warning" />
            <span>Etiqueta "Urgente"</span>
          </div>
          <div class="feature-item highlight">
            <va-icon name="check" size="small" color="warning" />
            <span>1 cambio permitido</span>
          </div>
        </div>

        <button
          @click.stop="selectPlan('purpura')"
          class="plan-button featured"
          :class="{ active: selectedPlan === 'purpura' }"
        >
          <va-icon v-if="selectedPlan === 'purpura'" name="check_circle" />
          {{ selectedPlan === 'purpura' ? 'Seleccionado' : 'Seleccionar' }}
        </button>
      </div>

      <!-- Plan Impulso Pro (169 Bs) -->
      <div
        @click="selectPlan('impulso')"
        class="plan-card premium"
        :class="{ selected: selectedPlan === 'impulso' }"
      >
        <div class="plan-badge premium">
          <va-icon name="trending_up" size="small" />
          Premium
        </div>

        <div class="plan-header">
          <va-icon name="bolt" size="2.5rem" color="yellow-primary" />
          <h3 class="plan-name">Impulso Pro</h3>
          <div class="plan-price">
            <span class="currency">Bs.</span>
            <span class="amount">169</span>
          </div>
          <span class="plan-duration">30 días (hasta 3 avisos)</span>
        </div>

        <div class="plan-features">
          <div class="feature-item highlight premium">
            <va-icon name="check" size="small" color="yellow-primary" />
            <span>Patrocinado (10 días)</span>
          </div>
          <div class="feature-item highlight premium">
            <va-icon name="check" size="small" color="yellow-primary" />
            <span>3 FB/IG + 2 LinkedIn + 1 TikTok</span>
          </div>
          <div class="feature-item highlight premium">
            <va-icon name="check" size="small" color="yellow-primary" />
            <span>Etiqueta "Urgente"</span>
          </div>
          <div class="feature-item highlight premium">
            <va-icon name="check" size="small" color="yellow-primary" />
            <span>1 cambio por aviso</span>
          </div>
        </div>

        <button
          @click.stop="selectPlan('impulso')"
          class="plan-button premium"
          :class="{ active: selectedPlan === 'impulso' }"
        >
          <va-icon v-if="selectedPlan === 'impulso'" name="check_circle" />
          {{ selectedPlan === 'impulso' ? 'Seleccionado' : 'Seleccionar' }}
        </button>
      </div>
    </div>

    <!-- Comparación de Planes -->
    <div class="comparison-section">
      <h3 class="comparison-title">
        <va-icon name="compare_arrows" />
        Comparación de Planes
      </h3>

      <div class="comparison-table">
        <div class="comparison-row header">
          <div class="feature-name">Característica</div>
          <div class="plan-col">Escencial</div>
          <div class="plan-col">Púrpura</div>
          <div class="plan-col">Impulso Pro</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Precio (Bs.)</div>
          <div class="plan-col">35</div>
          <div class="plan-col">79</div>
          <div class="plan-col premium-text">169</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Duración</div>
          <div class="plan-col">15 días</div>
          <div class="plan-col">30 días</div>
          <div class="plan-col premium-text">30 días</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Cantidad de Avisos</div>
          <div class="plan-col">1</div>
          <div class="plan-col">1</div>
          <div class="plan-col premium-text">Hasta 3</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Visibilidad Web</div>
          <div class="plan-col">Normal</div>
          <div class="plan-col">Destacado (10d)</div>
          <div class="plan-col premium-text">Patrocinado (10d)</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Redes Sociales</div>
          <div class="plan-col">1 post</div>
          <div class="plan-col">4 posts</div>
          <div class="plan-col premium-text">6 posts</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Etiqueta Urgente</div>
          <div class="plan-col">
            <va-icon name="close" size="small" color="danger" />
          </div>
          <div class="plan-col">
            <va-icon name="check" size="small" color="success" />
          </div>
          <div class="plan-col premium-text">
            <va-icon name="check" size="small" color="success" />
          </div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Sustitución de Aviso</div>
          <div class="plan-col">No</div>
          <div class="plan-col">1 cambio</div>
          <div class="plan-col premium-text">1 por aviso</div>
        </div>
      </div>
    </div>

    <!-- Información de Pago -->
    <div v-if="selectedPlan !== 'free'" class="payment-info">
      <va-icon name="info" color="info" size="large" />
      <div class="payment-info-content">
        <h4 class="payment-info-title">Métodos de pago disponibles</h4>
        <p class="payment-info-text">
          Después de confirmar, serás redirigido a nuestra pasarela de pago segura donde podrás pagar con:
        </p>
        <div class="payment-methods">
          <div class="payment-method">
            <va-icon name="qr_code_2" />
            <span>QR Simple</span>
          </div>
          <div class="payment-method">
            <va-icon name="credit_card" />
            <span>Tarjetas</span>
          </div>
          <div class="payment-method">
            <va-icon name="account_balance" />
            <span>Tigo Money</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Mensaje de advertencia -->
    <div v-if="!selectedPlan" class="warning-message">
      <va-icon name="info" color="warning" />
      <span>Selecciona un plan para continuar</span>
    </div>

    <!-- Navigation Buttons -->
    <div class="navigation-buttons">
      <button class="btn btn-secondary" @click="$emit('back')">
        <va-icon name="arrow_back" size="small" />
        Atrás
      </button>
      <button class="btn btn-primary" @click="handleNext">
        Siguiente
        <va-icon name="arrow_forward" size="small" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'free'
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])

const selectedPlan = ref(props.modelValue)

const selectPlan = (plan) => {
  selectedPlan.value = plan
  emit('update:modelValue', plan)
}

const validate = () => {
  if (!selectedPlan.value) {
    return false
  }
  return true
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
  padding: 1rem 0;
}

.step-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 0.5rem;
}

.step-description {
  color: #666;
  font-size: 1rem;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.plan-card {
  background: white;
  border: 3px solid #E0E0E0;
  border-radius: 16px;
  padding: 2rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  flex-direction: column;
}

.plan-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.plan-card.selected {
  border-color: var(--color-purple);
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.2);
}

.plan-card.featured {
  border-color: #FFB300;
}

.plan-card.featured.selected {
  border-color: #FF8F00;
  box-shadow: 0 8px 24px rgba(255, 143, 0, 0.3);
}

.plan-card.premium {
  border-color: var(--color-yellow-primary);
  background: linear-gradient(135deg, #FFFEF7 0%, #FFF9E6 100%);
}

.plan-card.premium.selected {
  border-color: var(--color-yellow-primary);
  box-shadow: 0 12px 32px rgba(253, 197, 0, 0.4);
}

.plan-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #FF8F00;
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.plan-badge.premium {
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

.plan-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #E0E0E0;
}

.plan-name {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0;
}

.plan-price {
  display: flex;
  align-items: flex-start;
  gap: 0.25rem;
}

.currency {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-purple);
  margin-top: 0.5rem;
}

.amount {
  font-size: 3rem;
  font-weight: 800;
  color: var(--color-purple);
  line-height: 1;
}

.plan-duration {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.plan-features {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex: 1;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #666;
  font-size: 0.95rem;
}

.feature-item.highlight {
  color: var(--color-purple-darkest);
  font-weight: 600;
}

.feature-item.highlight.premium {
  color: var(--color-purple-dark);
}

.plan-button {
  width: 100%;
  padding: 1rem;
  border: 2px solid var(--color-purple);
  background: white;
  color: var(--color-purple);
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.plan-button:hover {
  background: var(--color-purple);
  color: white;
}

.plan-button.active {
  background: var(--color-purple);
  color: white;
}

.plan-button.featured {
  border-color: #FF8F00;
  color: #FF8F00;
}

.plan-button.featured:hover,
.plan-button.featured.active {
  background: #FF8F00;
  color: white;
}

.plan-button.premium {
  border-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

.plan-button.premium:hover,
.plan-button.premium.active {
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

.comparison-section {
  background: #F8F9FA;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.comparison-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 1.5rem;
}

.comparison-table {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.comparison-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  align-items: center;
}

.comparison-row.header {
  background: var(--color-purple);
  color: white;
  font-weight: 700;
}

.feature-name {
  font-weight: 600;
  color: var(--color-purple-darkest);
}

.comparison-row.header .feature-name {
  color: white;
}

.plan-col {
  text-align: center;
  color: #666;
}

.comparison-row.header .plan-col {
  color: white;
}

.premium-text {
  color: var(--color-purple);
  font-weight: 700;
}

.payment-info {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: #E3F2FD;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.payment-info-content {
  flex: 1;
}

.payment-info-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1565C0;
  margin: 0 0 0.5rem 0;
}

.payment-info-text {
  color: #1976D2;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.payment-methods {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.payment-method {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border-radius: 8px;
  color: #1565C0;
  font-weight: 600;
  font-size: 0.9rem;
}

.warning-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #FFF9E6;
  border: 1px solid #FFD54F;
  border-radius: 8px;
  color: #F57C00;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .plans-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .plan-card {
    max-width: 500px;
    margin: 0 auto;
  }

  .comparison-row {
    grid-template-columns: 1.5fr repeat(3, 1fr);
    font-size: 0.9rem;
  }
}

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  margin-top: 2rem;
  border-top: 2px solid #E0E0E0;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-secondary {
  background: #F3F4F6;
  color: #1F2937;
  border: 2px solid #E5E7EB;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

@media (max-width: 768px) {
  .step-title {
    font-size: 1.5rem;
  }

  .comparison-section {
    padding: 1.5rem;
  }

  .comparison-row {
    grid-template-columns: 1fr;
    text-align: left;
    gap: 0.5rem;
  }

  .plan-col {
    text-align: left;
  }

  .comparison-row.header {
    display: none;
  }

  .navigation-buttons {
    flex-direction: column;
  }

  .btn {
    justify-content: center;
  }
}
</style>