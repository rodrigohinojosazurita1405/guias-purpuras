<template>
  <!-- 
    HowItWorksSection.vue - Cómo funciona la plataforma
    
    Propósito: Explicar en 4 pasos simples cómo usar Guías Púrpuras
    Conecta con: HomeView.vue (componente padre)
    Emite: publish-click (cuando el usuario hace clic en publicar)
    Datos: 4 pasos estáticos
  -->
  <section class="how-it-works">
    <div class="section-container">
      <!-- Header -->
      <div class="section-header centered">
        <div class="section-title-block">
          <h2 class="section-title">¿Cómo Funciona?</h2>
          <p class="section-subtitle">Publica o encuentra lo que buscas en 4 simples pasos</p>
        </div>
      </div>

      <!-- Grid de Pasos -->
      <div class="steps-grid">
        <div v-for="step in steps" :key="step.number" class="step-card">
          <div class="step-number">{{ step.number }}</div>
          <div class="step-icon">
            <VaIcon :name="step.icon" size="50px" color="var(--color-purple-dark)" />
          </div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.description }}</p>
        </div>
      </div>

      <!-- CTA Button -->
      <div class="cta-center">
        <VaButton size="large" class="cta-button" @click="handlePublish">
          <VaIcon name="add_circle" />
          Publicar Anuncio Gratis
        </VaButton>
      </div>
    </div>
  </section>
</template>

<script>
/**
 * HowItWorksSection Component
 * 
 * Props: Ninguno (pasos estáticos)
 * 
 * Emits:
 * - publish-click: cuando el usuario hace clic en publicar
 * 
 * State:
 * - steps: array de 4 pasos (estático, no necesita Django)
 */

export default {
  name: 'HowItWorksSection',
  emits: ['publish-click'],
  data() {
    return {
      // Pasos del proceso (estático)
      steps: [
        {
          number: 1,
          icon: 'location_searching',
          title: 'Elige tu Ciudad',
          description: 'Selecciona tu ubicación o permite que la detectemos automáticamente'
        },
        {
          number: 2,
          icon: 'category',
          title: 'Selecciona una Guía',
          description: 'Explora entre nuestras 4 categorías principales especializadas'
        },
        {
          number: 3,
          icon: 'add_circle',
          title: 'Publica tu Anuncio',
          description: 'Crea tu anuncio gratis en menos de 2 minutos con fotos y detalles'
        },
        {
          number: 4,
          icon: 'handshake',
          title: 'Conecta y Cierra',
          description: 'Recibe contactos interesados y completa tu transacción de forma segura'
        }
      ]
    }
  },
  methods: {
    handlePublish() {
      this.$emit('publish-click')
      console.log('Publicar anuncio')
      // TODO: Redirigir a /publicar
    }
  }
}
</script>

<style scoped>
/**
 * Estilos de How It Works Section
 * Grid de pasos con números grandes
 */

.how-it-works {
  width: 100%;
  padding: 6rem 3rem;
  background: linear-gradient(135deg, var(--color-gray-50) 0%, #ffffff 100%);
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

/* Steps Grid */
.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

.step-card {
  text-align: center;
  position: relative;
  padding: 2rem;
  background: #ffffff;
  border-radius: 16px;
  border: 2px solid var(--color-gray-100);
  transition: all 0.3s;
}

.step-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  border-color: var(--color-purple-dark);
}

.step-number {
  position: absolute;
  top: -1rem;
  right: 1.5rem;
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, var(--color-purple-dark) 0%, var(--color-purple) 100%);
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 800;
  box-shadow: 0 4px 15px rgba(26, 11, 61, 0.3);
}

.step-icon {
  width: 100px;
  height: 100px;
  background: var(--color-gray-100);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.step-card h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 1rem;
}

.step-card p {
  color: var(--color-gray-500);
  line-height: 1.6;
}

/* CTA Button */
.cta-center {
  display: flex;
  justify-content: center;
}

.cta-button {
  background: linear-gradient(135deg, var(--color-orange-primary) 0%, var(--color-orange-light) 100%) !important;
  padding: 1rem 3rem !important;
  font-size: 1.2rem !important;
  font-weight: 700 !important;
  box-shadow: 0 8px 25px rgba(255, 140, 0, 0.4);
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(255, 140, 0, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
  .how-it-works {
    padding: 4rem 1.5rem;
  }

  .steps-grid {
    grid-template-columns: 1fr;
  }

  .section-title {
    font-size: 2rem;
  }
}
</style>