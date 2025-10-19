<template>
  <!-- 
    GuidesSection.vue - Grid de las 4 guías principales
    
    Propósito: Mostrar las 4 categorías principales con estadísticas
    Conecta con: HomeView.vue (componente padre)
    Emite: guide-click (cuando se hace clic en una guía)
    Datos: Array de guías (mock, después desde Django)
  -->
  <section class="guides-section">
    <div class="section-container">
      <!-- Header de la Sección -->
      <div class="section-header">
        <div class="section-title-block">
          <h2 class="section-title">Explora Nuestras Guías</h2>
          <p class="section-subtitle">Encuentra lo que necesitas en las mejores categorías</p>
        </div>
      </div>

      <!-- Grid de Guías -->
      <div class="guides-grid">
        <div 
          v-for="guide in guides" 
          :key="guide.id"
          class="guide-card"
          @click="handleGuideClick(guide)"
        >
          <!-- Ícono de la Guía -->
          <div class="guide-icon" :style="{ background: guide.gradient }">
            <VaIcon :name="guide.icon" size="60px" color="#ffffff" />
          </div>

          <!-- Contenido -->
          <div class="guide-content">
            <h3>{{ guide.name }}</h3>
            <p>{{ guide.description }}</p>

            <!-- Estadísticas -->
            <div class="guide-stats">
              <span class="stat-badge">
                <VaIcon name="article" size="small" />
                {{ guide.count }} anuncios
              </span>
              <span class="stat-badge">
                <VaIcon name="trending_up" size="small" />
                +{{ guide.growth }}% esta semana
              </span>
            </div>

            <!-- Footer con enlace -->
            <div class="guide-footer">
              <span class="explore-link">
                Explorar
                <VaIcon name="arrow_forward" size="small" />
              </span>
            </div>
          </div>

          <div class="guide-overlay"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
/**
 * GuidesSection Component
 * 
 * Props: Ninguno (datos locales por ahora)
 * 
 * Emits:
 * - guide-click: { guide } cuando se hace clic en una guía
 * 
 * State:
 * - guides: array de 4 guías principales
 * 
 * TODO: 
 * - Obtener guías desde Django API /api/guides/
 * - Obtener estadísticas reales (count, growth)
 */

export default {
  name: 'GuidesSection',
  emits: ['guide-click'],
  data() {
    return {
      // Guías principales (mock - solo 4 para ejemplo)
      // TODO: Obtener desde Django /api/guides/
      guides: [
        {
          id: 1,
          slug: 'profesionales',
          name: 'Guías Profesionales',
          description: 'Abogados, Contadores, Arquitectos y más profesionales certificados',
          icon: 'business_center',
          gradient: 'linear-gradient(135deg, var(--color-purple-dark) 0%, var(--color-purple) 100%)',
          count: 1245,  // TODO: Desde Django
          growth: 12    // TODO: Calcular en Django
        },
        {
          id: 2,
          slug: 'gastronomicas',
          name: 'Guías Gastronómicas',
          description: 'Restaurantes, Cafeterías y lugares para disfrutar',
          icon: 'restaurant',
          gradient: 'linear-gradient(135deg, var(--color-orange-primary) 0%, var(--color-orange-light) 100%)',
          count: 892,
          growth: 18
        },
        {
          id: 3,
          slug: 'trabajos',
          name: 'Guías de Trabajos',
          description: 'Empleos formales, ofertas laborales y oportunidades',
          icon: 'work',
          gradient: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
          count: 678,
          growth: 25
        },
        {
          id: 4,
          slug: 'servicios',
          name: 'Guías de Servicios',
          description: 'Plomeros, Electricistas, Diseñadores y servicios varios',
          icon: 'build',
          gradient: 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)',
          count: 1523,
          growth: 15
        }
      ]
    }
  },
  methods: {
    handleGuideClick(guide) {
      // Emitir evento al componente padre
      this.$emit('guide-click', guide)
      
      console.log('Guía seleccionada:', guide.slug)
      
      // TODO: Redirigir a /guia/:slug usando Vue Router
      // this.$router.push(`/guia/${guide.slug}`)
    }
  }
}
</script>

<style scoped>
/**
 * Estilos de Guides Section
 * Full width, cards interactivas con hover effects
 */

.guides-section {
  width: 100%;
  padding: 6rem 3rem;
  background: var(--color-gray-50);
}

.section-container {
  max-width: 100%;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
}

.section-title-block {
  text-align: center;
  width: 100%;
}

.section-title {
  font-size: 2.75rem;
  font-weight: 800;
  color: var(--color-gray-900);
  margin-bottom: 0.5rem;
}

.section-subtitle {
  font-size: 1.2rem;
  color: var(--color-gray-500);
}

/* Guides Grid */
.guides-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.guide-card {
  position: relative;
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 2px solid transparent;
  min-height: 350px;
  display: flex;
  flex-direction: column;
}

.guide-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(26, 11, 61, 0.2);
  border-color: var(--color-purple-dark);
}

.guide-icon {
  width: 100%;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.guide-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.1);
  opacity: 0;
  transition: opacity 0.3s;
}

.guide-card:hover .guide-icon::before {
  opacity: 1;
}

.guide-content {
  padding: 2rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.guide-content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 0.75rem;
}

.guide-content p {
  color: var(--color-gray-500);
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex: 1;
}

.guide-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.stat-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: var(--color-gray-100);
  border-radius: 8px;
  font-size: 0.9rem;
  color: var(--color-gray-600);
  font-weight: 500;
}

.guide-footer {
  display: flex;
  justify-content: flex-end;
}

.explore-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-purple-dark);
  font-weight: 600;
  transition: gap 0.3s;
}

.guide-card:hover .explore-link {
  gap: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .guides-section {
    padding: 4rem 1.5rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .guides-grid {
    grid-template-columns: 1fr;
  }
}
</style>