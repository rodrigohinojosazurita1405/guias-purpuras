<!-- frontend/src/components/Publish/PlanStep.vue -->
<template>
  <div class="plan-step">
    <!-- 
      ==========================================
      PASO 4: SELECCIÓN DE PLAN
      ==========================================
      Permite elegir entre:
        - Plan Gratis (Bs. 0 - 7 días)
        - Plan Destacado (Bs. 25 - 30 días)
        - Plan TOP (Bs. 60 - 60 días)
      
      TODO Django:
        - POST /api/payments/create-order/ - Crear orden de pago
        - Integrar con pasarela (QR, Pagosnet, etc.)
        - Webhook para confirmar pago
        - Activar anuncio después del pago
        - Enviar email de confirmación
    -->

    <h2 class="step-title">
      <va-icon name="workspace_premium" color="purple" size="large" />
      Elige tu Plan
    </h2>

    <p class="step-description">
      Selecciona el plan que mejor se adapte a tus necesidades
    </p>

    <!-- ==========================================
         GRID DE PLANES
         ========================================== -->
    <div class="plans-grid">
      <!-- Plan Gratis -->
      <div 
        @click="selectPlan('free')"
        class="plan-card"
        :class="{ selected: selectedPlan === 'free' }"
      >
        <div class="plan-header">
          <va-icon name="check_circle" size="2.5rem" color="success" />
          <h3 class="plan-name">Gratis</h3>
          <div class="plan-price">
            <span class="currency">Bs.</span>
            <span class="amount">0</span>
          </div>
          <span class="plan-duration">7 días activo</span>
        </div>

        <div class="plan-features">
          <div class="feature-item">
            <va-icon name="check" size="small" color="success" />
            <span>Publicación por 7 días</span>
          </div>
          <div class="feature-item">
            <va-icon name="check" size="small" color="success" />
            <span>Hasta 3 imágenes</span>
          </div>
          <div class="feature-item">
            <va-icon name="check" size="small" color="success" />
            <span>Información básica</span>
          </div>
          <div class="feature-item">
            <va-icon name="check" size="small" color="success" />
            <span>Visible en búsquedas</span>
          </div>
        </div>

        <button 
          @click.stop="selectPlan('free')"
          class="plan-button"
          :class="{ active: selectedPlan === 'free' }"
        >
          <va-icon v-if="selectedPlan === 'free'" name="check_circle" />
          {{ selectedPlan === 'free' ? 'Seleccionado' : 'Seleccionar' }}
        </button>
      </div>

      <!-- Plan Destacado -->
      <div 
        @click="selectPlan('featured')"
        class="plan-card featured"
        :class="{ selected: selectedPlan === 'featured' }"
      >
        <div class="plan-badge">⭐ Recomendado</div>
        
        <div class="plan-header">
          <va-icon name="star" size="2.5rem" color="warning" />
          <h3 class="plan-name">Destacado</h3>
          <div class="plan-price">
            <span class="currency">Bs.</span>
            <span class="amount">25</span>
          </div>
          <span class="plan-duration">30 días activo</span>
        </div>

        <div class="plan-features">
          <div class="feature-item">
            <va-icon name="check" size="small" color="success" />
            <span>Todo lo del plan Gratis</span>
          </div>
          <div class="feature-item highlight">
            <va-icon name="check" size="small" color="warning" />
            <span>Hasta 5 imágenes</span>
          </div>
          <div class="feature-item highlight">
            <va-icon name="check" size="small" color="warning" />
            <span>Aparece destacado</span>
          </div>
          <div class="feature-item highlight">
            <va-icon name="check" size="small" color="warning" />
            <span>3x más visibilidad</span>
          </div>
          <div class="feature-item highlight">
            <va-icon name="check" size="small" color="warning" />
            <span>Badge "Destacado"</span>
          </div>
        </div>

        <button 
          @click.stop="selectPlan('featured')"
          class="plan-button featured"
          :class="{ active: selectedPlan === 'featured' }"
        >
          <va-icon v-if="selectedPlan === 'featured'" name="check_circle" />
          {{ selectedPlan === 'featured' ? 'Seleccionado' : 'Seleccionar' }}
        </button>
      </div>

      <!-- Plan TOP -->
      <div 
        @click="selectPlan('top')"
        class="plan-card premium"
        :class="{ selected: selectedPlan === 'top' }"
      >
        <div class="plan-badge premium">🏆 Premium</div>
        
        <div class="plan-header">
          <va-icon name="stars" size="2.5rem" color="yellow-primary" />
          <h3 class="plan-name">TOP</h3>
          <div class="plan-price">
            <span class="currency">Bs.</span>
            <span class="amount">60</span>
          </div>
          <span class="plan-duration">60 días activo</span>
        </div>

        <div class="plan-features">
          <div class="feature-item">
            <va-icon name="check" size="small" color="success" />
            <span>Todo lo del plan Destacado</span>
          </div>
          <div class="feature-item highlight premium">
            <va-icon name="check" size="small" color="yellow-primary" />
            <span>Imágenes ilimitadas</span>
          </div>
          <div class="feature-item highlight premium">
            <va-icon name="check" size="small" color="yellow-primary" />
            <span>Aparece en TOP</span>
          </div>
          <div class="feature-item highlight premium">
            <va-icon name="check" size="small" color="yellow-primary" />
            <span>10x más visibilidad</span>
          </div>
          <div class="feature-item highlight premium">
            <va-icon name="check" size="small" color="yellow-primary" />
            <span>Badge "TOP"</span>
          </div>
          <div class="feature-item highlight premium">
            <va-icon name="check" size="small" color="yellow-primary" />
            <span>Soporte prioritario</span>
          </div>
        </div>

        <button 
          @click.stop="selectPlan('top')"
          class="plan-button premium"
          :class="{ active: selectedPlan === 'top' }"
        >
          <va-icon v-if="selectedPlan === 'top'" name="check_circle" />
          {{ selectedPlan === 'top' ? 'Seleccionado' : 'Seleccionar' }}
        </button>
      </div>
    </div>

    <!-- ==========================================
         COMPARACIÓN DE PLANES
         ========================================== -->
    <div class="comparison-section">
      <h3 class="comparison-title">
        <va-icon name="compare_arrows" />
        Comparación de Planes
      </h3>

      <div class="comparison-table">
        <div class="comparison-row header">
          <div class="feature-name">Característica</div>
          <div class="plan-col">Gratis</div>
          <div class="plan-col">Destacado</div>
          <div class="plan-col">TOP</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Duración</div>
          <div class="plan-col">7 días</div>
          <div class="plan-col">30 días</div>
          <div class="plan-col premium-text">60 días</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Imágenes</div>
          <div class="plan-col">Hasta 3</div>
          <div class="plan-col">Hasta 5</div>
          <div class="plan-col premium-text">Ilimitadas ∞</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Posición</div>
          <div class="plan-col">Normal</div>
          <div class="plan-col">Destacado</div>
          <div class="plan-col premium-text">TOP</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Visibilidad</div>
          <div class="plan-col">1x</div>
          <div class="plan-col">3x</div>
          <div class="plan-col premium-text">10x</div>
        </div>

        <div class="comparison-row">
          <div class="feature-name">Soporte</div>
          <div class="plan-col">Estándar</div>
          <div class="plan-col">Estándar</div>
          <div class="plan-col premium-text">Prioritario</div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         INFORMACIÓN DE PAGO
         ========================================== -->
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

    <!-- ==========================================
         MENSAJE DE CONFIRMACIÓN
         ========================================== -->
    <div v-if="!selectedPlan" class="warning-message">
      <va-icon name="info" color="warning" />
      <span>Selecciona un plan para continuar</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// ==========================================
// PROPS
// ==========================================
const props = defineProps({
  modelValue: {
    type: String,
    default: 'free'
  }
})

// ==========================================
// EMITS
// ==========================================
const emit = defineEmits(['update:modelValue'])

// ==========================================
// STATE
// ==========================================
const selectedPlan = ref(props.modelValue)

// ==========================================
// MÉTODOS
// ==========================================
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

// ==========================================
// WATCHERS
// ==========================================
watch(() => props.modelValue, (newValue) => {
  selectedPlan.value = newValue
})

// ==========================================
// EXPOSE
// ==========================================
defineExpose({
  validate
})
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.plan-step {
  padding: 1rem 0;
}

/* ==========================================
   TÍTULO Y DESCRIPCIÓN
   ========================================== */
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

/* ==========================================
   GRID DE PLANES
   ========================================== */
.plans-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

/* ==========================================
   TARJETA DE PLAN
   ========================================== */
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

/* ==========================================
   BADGE DEL PLAN
   ========================================== */
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

/* ==========================================
   HEADER DEL PLAN
   ========================================== */
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

/* ==========================================
   CARACTERÍSTICAS
   ========================================== */
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

/* ==========================================
   BOTÓN DEL PLAN
   ========================================== */
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

/* ==========================================
   SECCIÓN DE COMPARACIÓN
   ========================================== */
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

/* ==========================================
   INFORMACIÓN DE PAGO
   ========================================== */
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

/* ==========================================
   MENSAJE DE ADVERTENCIA
   ========================================== */
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

/* ==========================================
   RESPONSIVE
   ========================================== */
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

  .comparison-row::before {
    content: attr(data-label);
    font-weight: 700;
    color: var(--color-purple);
  }
}
</style>