<!-- frontend/src/components/Home/GuidesSection.vue -->
<template>
  <section class="guides-section">
    <div class="container">
      <!-- Encabezado -->
      <div class="section-header">
        <h2 class="section-title">Explora Nuestras Guías</h2>
        <p class="section-subtitle">
          Encuentra lo que necesitas en cuatro categorías principales
        </p>
      </div>

      <!-- Grid de Guías -->
      <div class="guides-grid">
        <div
          v-for="guide in guides"
          :key="guide.id"
          @click="goToGuide(guide.route)"
          class="guide-card"
        >
          <div class="guide-icon-wrapper">
            <va-icon :name="guide.icon" size="3rem" :color="guide.color" />
          </div>
          
          <h3 class="guide-title">{{ guide.title }}</h3>
          <p class="guide-description">{{ guide.description }}</p>
          
          <div class="guide-stats">
            <span class="guide-count">{{ guide.count }} anuncios</span>
          </div>

          <div class="guide-cta">
            <span>Ver guía</span>
            <va-icon name="arrow_forward" size="small" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router'

// ==========================================
// COMPOSABLES
// ==========================================
const router = useRouter()

// ==========================================
// DATA
// ==========================================
const guides = [
  {
    id: 'profesionales',
    title: '📋 Guías Profesionales',
    description: 'Encuentra abogados, doctores, contadores y más profesionales certificados',
    icon: 'work',
    color: 'purple',
    count: '3,245',
    route: 'guias-profesionales'
  },
  {
    id: 'gastronomia',
    title: '🍽️ Guías Gastronómicas',
    description: 'Descubre los mejores restaurantes, cafeterías y opciones de comida',
    icon: 'restaurant',
    color: 'yellow-primary',
    count: '2,189',
    route: 'guias-gastronomia'
  },
  {
    id: 'trabajos',
    title: '💼 Guías de Trabajos',
    description: 'Encuentra ofertas laborales y oportunidades de empleo en tu ciudad',
    icon: 'business_center',
    color: 'purple-dark',
    count: '4,512',
    route: 'guias-trabajos'
  },
  {
    id: 'Negocios',
    title: '🛠️ Guías de Negocios',
    description: 'Plomeros, electricistas, carpinteros y servicios para tu hogar',
    icon: 'build',
    color: 'yellow-light',
    count: '2,510',
    route: 'guias-servicios'
  }
]

// ==========================================
// MÉTODOS
// ==========================================
const goToGuide = (routeName) => {
  router.push({ name: routeName })
}
</script>

<style scoped>
/* ==========================================
   SECTION
   ========================================== */
.guides-section {
  padding: 5rem 1rem;
  background-color: #FAFAFA;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* ==========================================
   ENCABEZADO
   ========================================== */
.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

/* ==========================================
   GRID DE GUÍAS
   ========================================== */
.guides-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.guide-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.guide-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(92, 0, 153, 0.15);
}

/* ==========================================
   CONTENIDO DE TARJETA
   ========================================== */
.guide-icon-wrapper {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.guide-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
}

.guide-description {
  color: #666;
  line-height: 1.6;
  flex: 1;
  margin: 0;
}

.guide-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #E0E0E0;
}

.guide-count {
  font-weight: 600;
  color: var(--color-purple);
  font-size: 0.95rem;
}

.guide-cta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-yellow-primary);
  font-weight: 600;
  font-size: 1rem;
}

/* ==========================================
   HOVER EFFECTS
   ========================================== */
.guide-card:hover .guide-icon-wrapper {
  transform: scale(1.1) rotate(5deg);
}

.guide-card:hover .guide-cta {
  gap: 0.75rem;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
  .guides-section {
    padding: 3rem 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .guides-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>