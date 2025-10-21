<template>
  <!-- 
    CTABanner.vue - Llamado a la acción final
    
    Propósito: Banner final para incentivar registro o publicación
    Conecta con: HomeView.vue (componente padre)
    Emite: publish-click, explore-click
    Datos: Ninguno (estático)
  -->
  <section class="cta-banner">
    <div class="cta-content">
      <div class="cta-text">
        <h2>¿Listo para Empezar?</h2>
        <p>Únete a miles de bolivianos que ya encontraron lo que buscaban</p>
      </div>
      <div class="cta-buttons">
        <VaButton size="large" class="cta-primary" @click="handlePublish">
          <VaIcon name="add_circle" />
          Publicar Gratis
        </VaButton>
        <VaButton size="large" preset="outline" class="cta-secondary" @click="handleExplore">
          <VaIcon name="explore" />
          Explorar Anuncios
        </VaButton>
      </div>
    </div>
  </section>
</template>

<script>
/**
 * CTABanner Component
 * 
 * Props: Ninguno
 * 
 * Emits:
 * - publish-click: cuando se hace clic en publicar
 * - explore-click: cuando se hace clic en explorar
 */

export default {
  name: 'CTABanner',
  emits: ['publish-click', 'explore-click'],
  methods: {
    handlePublish() {
      this.$emit('publish-click')
      console.log('Publicar desde CTA')
      // TODO: Redirigir a /publicar
    },
    
    handleExplore() {
      this.$emit('explore-click')
      console.log('Explorar desde CTA')
      // TODO: Redirigir a /guias o /explorar
    }
  }
}
</script>

<style scoped>
/**
 * Estilos de CTA Banner
 * Full width con gradiente púrpura
 */

.cta-banner {
  width: 100%;
  padding: 5rem 3rem;
  background: linear-gradient(135deg, var(--color-purple-dark) 0%, var(--color-purple) 100%);
  position: relative;
  overflow: hidden;
}

.cta-banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
  background-size: cover;
  opacity: 0.3;
}

.cta-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
  gap: 3rem;
  flex-wrap: wrap;
}

.cta-text h2 {
  font-size: 3rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.cta-text p {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.9);
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  color: var(--color-yellow-primary) !important;
  flex-wrap: wrap;
}

.cta-primary {
  background: #ffffff !important;
  color: var(--color-yellow-primary) !important;
  font-weight: 700 !important;
  padding: 1rem 2rem !important;
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.3);
}

.cta-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(255, 255, 255, 0.4);
}

.cta-secondary {
  background: transparent !important;
  border: 2px solid #ffffff !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  padding: 1rem 2rem !important;
}

.cta-secondary:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  transform: translateY(-3px);
}

/* Responsive */
@media (max-width: 768px) {
  .cta-banner {
    padding: 4rem 1.5rem;
  }

  .cta-content {
    flex-direction: column;
    text-align: center;
  }

  .cta-text h2 {
    font-size: 2rem;
  }

  .cta-text p {
    font-size: 1.1rem;
  }

  .cta-buttons {
    justify-content: center;
    width: 100%;
  }

  .cta-primary,
  .cta-secondary {
    width: 100%;
  }
}
</style>