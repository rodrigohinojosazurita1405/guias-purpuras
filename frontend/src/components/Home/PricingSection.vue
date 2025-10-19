<template>
  <!-- 
    PricingSection.vue - Planes y precios
    
    Propósito: Mostrar los 3 planes (Gratis, Destacado, TOP)
    Conecta con: HomeView.vue (componente padre)
    Emite: plan-select (cuando se selecciona un plan)
    Datos: 3 planes estáticos
  -->
  <section class="pricing-section">
    <div class="section-container">
      <!-- Header -->
      <div class="section-header centered">
        <div class="section-title-block">
          <h2 class="section-title">Planes y Precios</h2>
          <p class="section-subtitle">Elige el plan que mejor se adapte a tus necesidades</p>
        </div>
      </div>

      <!-- Grid de Planes -->
      <div class="pricing-grid">
        <div 
          v-for="plan in pricingPlans" 
          :key="plan.id"
          :class="['pricing-card', { featured: plan.featured }]"
        >
          <!-- Badge de destacado -->
          <div v-if="plan.featured" class="featured-badge">
            <VaIcon name="star" size="small" />
            Más Popular
          </div>

          <!-- Ícono del Plan -->
          <div class="plan-icon" :style="{ background: plan.color }">
            <VaIcon :name="plan.icon" size="large" color="#ffffff" />
          </div>

          <!-- Nombre del Plan -->
          <h3 class="plan-name">{{ plan.name }}</h3>

          <!-- Precio -->
          <div class="plan-price">
            <span class="currency">Bs.</span>
            <span class="amount">{{ plan.price }}</span>
            <span class="period" v-if="plan.price > 0">/ {{ plan.duration }} días</span>
          </div>

          <!-- Características -->
          <ul class="plan-features">
            <li v-for="(feature, index) in plan.features" :key="index">
              <VaIcon name="check_circle" size="small" color="var(--color-success)" />
              <span>{{ feature }}</span>
            </li>
          </ul>

          <!-- Botón de Acción -->
          <VaButton 
            block 
            :class="plan.featured ? 'featured-btn' : ''"
            @click="selectPlan(plan)"
          >
            {{ plan.buttonText }}
          </VaButton>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
/**
 * PricingSection Component
 * 
 * Props: Ninguno (planes estáticos)
 * 
 * Emits:
 * - plan-select: { plan } cuando se selecciona un plan
 * 
 * State:
 * - pricingPlans: array de 3 planes (estático)
 * 
 * TODO: 
 * - Si los precios cambian, obtenerlos desde Django /api/plans/
 */

export default {
  name: 'PricingSection',
  emits: ['plan-select'],
  data() {
    return {
      // Planes de precios (estático - solo 3)
      pricingPlans: [
        {
          id: 1,
          name: 'Plan Gratis',
          price: 0,
          duration: 7,
          icon: 'article',
          color: 'var(--color-gray-500)',
          featured: false,
          buttonText: 'Comenzar Gratis',
          features: [
            '7 días de vigencia',
            '1 foto incluida',
            'Publicación básica',
            'Visible en búsquedas',
            'Datos de contacto'
          ]
        },
        {
          id: 2,
          name: 'Plan Destacado',
          price: 25,
          duration: 15,
          icon: 'star',
          color: 'var(--color-orange-primary)',
          featured: true,
          buttonText: 'Elegir Destacado',
          features: [
            '15 días de vigencia',
            'Hasta 5 fotos',
            'Badge "Destacado"',
            'Aparece en sección destacados',
            'Estadísticas de vistas',
            'Soporte prioritario'
          ]
        },
        {
          id: 3,
          name: 'Plan TOP',
          price: 60,
          duration: 30,
          icon: 'workspace_premium',
          color: 'var(--color-danger)',
          featured: false,
          buttonText: 'Elegir TOP',
          features: [
            '30 días de vigencia',
            'Hasta 10 fotos',
            'Badge "TOP" premium',
            'Aparece PRIMERO siempre',
            'Estadísticas avanzadas',
            'Redes sociales incluidas',
            'Renovación automática',
            'Soporte VIP 24/7'
          ]
        }
      ]
    }
  },
  methods: {
    selectPlan(plan) {
      this.$emit('plan-select', plan)
      console.log('Plan seleccionado:', plan.name)
      // TODO: Redirigir a proceso de pago o publicación
    }
  }
}
</script>

<style scoped>
/**
 * Estilos de Pricing Section
 * Cards de planes con destacado en el centro
 */

.pricing-section {
  width: 100%;
  padding: 6rem 3rem;
  background: #ffffff;
}

.section-container {
  max-width: 100%;
  margin: 0 auto;
}

.section-header {
  margin-bottom: 4rem;
}

.section-header.centered {
  text-align: center;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 0.5rem;
}

.section-subtitle {
  font-size: 1.1rem;
  color: var(--color-gray-500);
}

/* Pricing Grid */
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.pricing-card {
  background: #ffffff;
  border: 2px solid var(--color-gray-200);
  border-radius: 20px;
  padding: 2.5rem;
  position: relative;
  transition: all 0.3s;
  text-align: center;
}

.pricing-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.pricing-card.featured {
  border-color: var(--color-orange-primary);
  box-shadow: 0 10px 30px rgba(255, 140, 0, 0.2);
  transform: scale(1.05);
}

.pricing-card.featured:hover {
  transform: translateY(-10px) scale(1.05);
}

/* Featured Badge */
.featured-badge {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, var(--color-orange-primary) 0%, var(--color-orange-light) 100%);
  color: #ffffff;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 15px rgba(255, 140, 0, 0.3);
}

/* Plan Icon */
.plan-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.plan-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 1rem;
}

/* Price */
.plan-price {
  margin-bottom: 2rem;
}

.currency {
  font-size: 1.5rem;
  color: var(--color-gray-500);
  vertical-align: super;
}

.amount {
  font-size: 4rem;
  font-weight: 800;
  color: var(--color-purple-dark);
  line-height: 1;
}

.period {
  font-size: 1rem;
  color: var(--color-gray-500);
  margin-left: 0.5rem;
}

/* Features List */
.plan-features {
  list-style: none;
  margin-bottom: 2rem;
  text-align: left;
}

.plan-features li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: var(--color-gray-600);
  line-height: 1.6;
}

/* Buttons */
.pricing-card button {
  background: var(--color-purple-dark) !important;
  color: #ffffff !important;
  font-weight: 600 !important;
}

.featured-btn {
  background: linear-gradient(135deg, var(--color-orange-primary) 0%, var(--color-orange-light) 100%) !important;
  font-weight: 700 !important;
  box-shadow: 0 4px 15px rgba(255, 140, 0, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .pricing-section {
    padding: 4rem 1.5rem;
  }

  .pricing-grid {
    grid-template-columns: 1fr;
  }

  .pricing-card.featured {
    transform: scale(1);
  }

  .pricing-card.featured:hover {
    transform: translateY(-10px) scale(1);
  }

  .section-title {
    font-size: 2rem;
  }

  .amount {
    font-size: 3rem;
  }
}
</style>