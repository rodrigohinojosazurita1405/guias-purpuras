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

      <!-- Grid de Planes (Dinámico desde API) -->
      <div v-if="isLoading" class="loading-state">
        <p>Cargando planes...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>Error: {{ error }}</p>
        <p style="font-size: 0.9rem; color: #6B7280;">Usando planes predeterminados</p>
      </div>

      <div class="plans-grid">
        <div
          v-for="plan in plans"
          :key="plan.id"
          @click="selectPlan(plan.name)"
          class="plan-card"
          :class="{
            selected: selectedPlan === plan.name,
            featured: plan.order === 2
          }"
        >
          <div v-if="plan.order === 2" class="plan-badge">Recomendado</div>
          <div class="plan-tier">Plan</div>
          <h3 class="plan-name">{{ plan.label.split('(')[0].trim() }}</h3>
          <div class="plan-price-block">
            <span class="plan-price">{{ Math.floor(plan.price) }}</span>
            <span class="plan-currency">{{ plan.currency }}.</span>
          </div>
          <p class="plan-period">{{ plan.durationDays }} días</p>

          <div class="plan-divider"></div>

          <!-- Badges (Dinámicos desde Django y características) -->
          <div class="plan-badges">
            <span v-if="plan.badgeLabel" class="badge" :class="getBadgeClass(plan)">
              {{ plan.badgeLabel }}
            </span>
            <span
              v-if="plan.features.highlightedResults"
              class="badge badge-urgent"
            >
              Urgente
            </span>
          </div>

          <ul class="plan-features">
            <li>{{ plan.features.maxAnnouncements }} Aviso{{ plan.features.maxAnnouncements > 1 ? 's' : '' }}</li>
            <li v-if="plan.features.featured">Visibilidad Destacada</li>
            <li v-else>Visibilidad Normal</li>
          </ul>

          <button
            @click.stop="selectPlan(plan.name)"
            class="plan-select-btn"
            :class="{ active: selectedPlan === plan.name }"
          >
            {{ selectedPlan === plan.name ? 'Seleccionado' : 'Seleccionar' }}
          </button>
        </div>
      </div>

      <!-- Comparison Table (Dinámico) -->
      <div v-if="!isLoading" class="comparison-section">
        <h3 class="comparison-title">Comparación de Planes</h3>

        <div class="comparison-table-wrapper">
          <table class="comparison-table">
            <thead>
              <tr class="table-header">
                <th class="header-feature">Característica</th>
                <th
                  v-for="plan in plans"
                  :key="`header-${plan.id}`"
                  class="header-plan"
                  :class="{ 'featured': plan.order === 2 }"
                >
                  {{ plan.label.split('(')[0].trim() }}
                </th>
              </tr>
            </thead>
            <tbody>
              <!-- Precio -->
              <tr class="table-row">
                <td class="row-feature">Precio</td>
                <td
                  v-for="plan in plans"
                  :key="`price-${plan.id}`"
                  class="row-data"
                  :class="{ 'featured': plan.order === 2 }"
                >
                  {{ Math.floor(plan.price) }} {{ plan.currency }}.
                </td>
              </tr>

              <!-- Duración y Cantidad -->
              <tr class="table-row">
                <td class="row-feature">Duración y Cantidad</td>
                <td
                  v-for="plan in plans"
                  :key="`duration-${plan.id}`"
                  class="row-data"
                  :class="{ 'featured': plan.order === 2 }"
                >
                  {{ plan.durationDays }} días ({{ plan.features.maxAnnouncements }} aviso{{ plan.features.maxAnnouncements > 1 ? 's' : '' }})
                </td>
              </tr>

              <!-- Visibilidad en Web (Anclado) -->
              <tr class="table-row">
                <td class="row-feature">Visibilidad en Web (Anclado)</td>
                <td
                  v-for="plan in plans"
                  :key="`visibility-${plan.id}`"
                  class="row-data"
                  :class="{ 'featured': plan.order === 2 }"
                >
                  {{ plan.features.featured ? (plan.order === 3 ? `Patrocinado (${plan.features.featuredDays} días)` : `Destacado (${plan.features.featuredDays} días)`) : 'Normal' }}
                </td>
              </tr>

              <!-- Sustitución de Aviso -->
              <tr class="table-row">
                <td class="row-feature">Sustitución de Aviso (Si cubres la vacante antes)</td>
                <td
                  v-for="plan in plans"
                  :key="`substitution-${plan.id}`"
                  class="row-data"
                  :class="{ 'featured': plan.order === 2 }"
                >
                  {{ plan.features.announcementSubstitutions === 0 ? 'No incluido' : (plan.features.announcementSubstitutions === 1 ? '1 cambio permitido' : `1 cambio por aviso (${plan.features.announcementSubstitutions} total)`) }}
                </td>
              </tr>

              <!-- Difusión en Redes Sociales -->
              <tr class="table-row">
                <td class="row-feature">Difusión en Redes Sociales</td>
                <td
                  v-for="plan in plans"
                  :key="`social-${plan.id}`"
                  class="row-data"
                  :class="{ 'featured': plan.order === 2 }"
                >
                  <span v-if="plan.features.socialMedia">
                    {{ plan.features.socialMedia.facebook }} post FB/IG<br>
                    <span v-if="plan.features.socialMedia.linkedin > 0">+ {{ plan.features.socialMedia.linkedin }} LinkedIn<br></span>
                    <span v-if="plan.features.socialMedia.tiktok > 0">+ {{ plan.features.socialMedia.tiktok }} TikTok</span>
                  </span>
                  <span v-else>1 post en Facebook/IG</span>
                </td>
              </tr>

              <!-- Etiqueta Urgente -->
              <tr class="table-row">
                <td class="row-feature">Etiqueta "Urgente"</td>
                <td
                  v-for="plan in plans"
                  :key="`urgent-${plan.id}`"
                  class="row-data"
                  :class="{ 'featured': plan.order === 2 }"
                >
                  {{ plan.features.highlightedResults ? 'Sí' : 'No' }}
                </td>
              </tr>
            </tbody>
          </table>
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
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'escencial'
  }
})

const emit = defineEmits(['update:modelValue', 'next', 'back'])

const selectedPlan = ref(props.modelValue)
const plans = ref([])
const isLoading = ref(true)
const error = ref(null)

// Cargar planes desde API
const loadPlans = async () => {
  try {
    isLoading.value = true
    error.value = null
    // Agregar timestamp para evitar cache
    const timestamp = new Date().getTime()
    const response = await fetch(`/api/plans/?_t=${timestamp}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('No se pudieron cargar los planes')
    }

    const data = await response.json()
    if (data.success && data.data) {
      plans.value = data.data
    } else {
      throw new Error('Formato de respuesta inválido')
    }
  } catch (err) {
    console.error('Error cargando planes:', err)
    error.value = err.message
    // Fallback a planes hardcodeados
    plans.value = [
      {
        id: 1,
        name: 'escencial',
        label: 'Escencial (35 Bs)',
        price: 35,
        currency: 'Bs',
        durationDays: 15,
        features: { maxAnnouncements: 1 }
      },
      {
        id: 2,
        name: 'purpura',
        label: 'Púrpura (79 Bs)',
        price: 79,
        currency: 'Bs',
        durationDays: 30,
        features: { maxAnnouncements: 1 }
      },
      {
        id: 3,
        name: 'impulso',
        label: 'Impulso Pro (169 Bs)',
        price: 169,
        currency: 'Bs',
        durationDays: 30,
        features: { maxAnnouncements: 3 }
      }
    ]
  } finally {
    isLoading.value = false
  }
}

const selectPlan = (planName) => {
  selectedPlan.value = planName
  emit('update:modelValue', planName)
}

const validate = () => {
  return !!selectedPlan.value
}

const handleNext = () => {
  if (validate()) {
    emit('next')
  }
}

// Determinar la clase CSS del badge basado en el orden del plan
const getBadgeClass = (plan) => {
  if (plan.order === 1) return 'badge-basic'      // Primer plan (Básico)
  if (plan.order === 2) return 'badge-featured'   // Segundo plan (Destacado/Recomendado)
  if (plan.order === 3) return 'badge-sponsored'  // Tercer plan (Patrocinado)
  return 'badge-basic'                            // Por defecto
}

watch(() => props.modelValue, (newValue) => {
  selectedPlan.value = newValue
})

onMounted(() => {
  loadPlans()
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

.loading-state,
.error-state {
  text-align: center;
  padding: 3rem 2rem;
  background: white;
  border-radius: 16px;
  margin-bottom: 2rem;
}

.loading-state p,
.error-state p {
  color: #6B7280;
  font-size: 1rem;
  margin: 0.5rem 0;
}

.error-state {
  background: #FEE2E2;
  border: 1px solid #FECACA;
}

.error-state p {
  color: #991B1B;
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
  background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
  color: white;
  border: 1px solid rgba(245, 158, 11, 0.5);
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
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

.comparison-table-wrapper {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
  background: white;
  -webkit-overflow-scrolling: touch;

  /* Scrollbar styling */
  scrollbar-width: thin;
  scrollbar-color: #D1D5DB #F3F4F6;
}

.comparison-table-wrapper::-webkit-scrollbar {
  height: 8px;
}

.comparison-table-wrapper::-webkit-scrollbar-track {
  background: #F3F4F6;
  border-radius: 10px;
}

.comparison-table-wrapper::-webkit-scrollbar-thumb {
  background: #D1D5DB;
  border-radius: 10px;
}

.comparison-table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #9CA3AF;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

/* Header Styling */
.comparison-table thead {
  background: var(--color-purple);
}

.comparison-table .table-header {
  background: var(--color-purple);
}

.comparison-table .table-header th {
  color: white;
  font-weight: 700;
  padding: 1.25rem 1rem;
  text-align: center;
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 0.95rem;
}

.comparison-table .table-header th:last-child {
  border-right: none;
}

.comparison-table .header-feature {
  text-align: left;
}

/* Body Row Styling */
.comparison-table tbody tr {
  border-bottom: 1px solid #E5E7EB;
}

.comparison-table tbody tr:last-child {
  border-bottom: none;
}

/* Alternating row backgrounds */
.comparison-table tbody tr:nth-child(odd) {
  background: #FFFFFF;
}

.comparison-table tbody tr:nth-child(even) {
  background: #F9FAFB;
}

.comparison-table tbody td {
  padding: 1.25rem 1rem;
  text-align: center;
  border-right: 1px solid #E5E7EB;
  font-size: 0.95rem;
  color: #374151;
}

.comparison-table tbody td:last-child {
  border-right: none;
}

.comparison-table .row-feature {
  text-align: left;
  font-weight: 600;
  color: #1F2937;
  background: inherit !important;
  min-width: 250px;
}

.comparison-table .row-data {
  text-align: center;
  color: #6B7280;
  font-weight: 500;
}

/* Featured plan (Púrpura) styling - same as other plans */
.comparison-table .row-data.featured {
  background: inherit;
  color: #6B7280;
  font-weight: 500;
}

.comparison-table .header-plan.featured {
  background: var(--color-purple);
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