<!-- frontend/src/components/Home/GuidesSection.vue -->
<template>
  <section class="marketing-guides">
    <!-- Hero Section Full Width -->
    <div class="compact-hero">
      <div class="hero-container">
        <div class="hero-content">
          <div class="hero-badge">
            <va-icon name="verified" size="1rem" />
            <span>La plataforma #1 en Bolivia</span>
          </div>
          
          <h1 class="hero-title">
            Descubre las 
            <span class="title-highlight">Mejores Oportunidades</span>
          </h1>
          
          <p class="hero-subtitle">
            Anuncios <strong>destacados y verificados</strong> en empleos, profesionales, 
            gastronomía y negocios. Tu próximo éxito comienza aquí.
          </p>

          <!-- Stats con animación al hacer scroll -->
          <div class="hero-stats" ref="statsSection">
            <div 
              v-for="(stat, index) in stats" 
              :key="index"
              class="stat"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="stat-number">{{ stat.number }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="hero-actions">
            <button class="btn btn-primary" @click="goToPublish">
              <va-icon name="add_circle" size="1.1rem" />
              ¡Anuncia ahora!
            </button>
            <button class="btn btn-secondary" @click="scrollToContent">
              <va-icon name="explore" size="1.1rem" />
              Explorar
            </button>
          </div>
        </div>

        <!-- Cards flotantes mejoradas -->
        <div class="hero-visual">
          <div class="floating-cards">
            <div 
              v-for="(category, index) in categories" 
              :key="category.id"
              class="card card-large"
              :class="`card-${index + 1}`"
              @click="goToCategory(category.id)"
            >
              <div class="card-icon">
                <va-icon :name="category.icon" size="2.5rem" />
              </div>
              <span class="card-title">{{ category.label }}</span>
              <span class="card-count">{{ category.count }}+ anuncios</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ==========================================
// DATA
// ==========================================
const stats = [
  { number: '+2,500', label: 'Empleos' },
  { number: '+3,200', label: 'Profesionales' },
  { number: '+2,100', label: 'Restaurantes' },
  { number: '+2,500', label: 'Negocios' }
]

const categories = [
  { 
    id: 'trabajos', 
    label: 'Trabajos', 
    icon: 'work',
    count: '2.5k'
  },
  { 
    id: 'profesionales', 
    label: 'Profesionales', 
    icon: 'business_center',
    count: '3.2k'
  },
  { 
    id: 'gastronomia', 
    label: 'Gastronomía', 
    icon: 'restaurant',
    count: '2.1k'
  },
  { 
    id: 'negocios', 
    label: 'Negocios', 
    icon: 'store',
    count: '2.5k'
  }
]

const statsSection = ref(null)

// ==========================================
// METHODS
// ==========================================
const scrollToContent = () => {
  window.scrollTo({ 
    top: window.innerHeight, 
    behavior: 'smooth' 
  })
}

const goToPublish = () => {
  router.push({ name: 'Publish' })
}

const goToCategory = (categoryId) => {
  router.push(`/guias/${categoryId}`)
}

// ==========================================
// INTERSECTION OBSERVER (Animación al scroll)
// ==========================================
let observer = null

onMounted(() => {
  // Configurar Intersection Observer para animar stats
  if (statsSection.value) {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in')
          }
        })
      },
      { threshold: 0.2 }
    )
    
    observer.observe(statsSection.value)
  }
})

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.marketing-guides {
  width: 100%;
  margin: 0;
  padding: 0;
}

/* ==========================================
   HERO SECTION
   ========================================== */
.compact-hero {
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  color: white;
  padding: 5rem 0;
  position: relative;
  overflow: hidden;
  width: 100%;
}

.compact-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" opacity="0.05"><polygon fill="white" points="0,1000 1000,0 1000,1000"/></svg>');
  background-size: cover;
  animation: subtle-move 20s ease-in-out infinite;
}

@keyframes subtle-move {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-10px, -10px); }
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  position: relative;
  z-index: 2;
}

/* ==========================================
   CONTENIDO HERO
   ========================================== */
.hero-content {
  max-width: 100%;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.15);
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: badge-pulse 2s ease-in-out infinite;
}

@keyframes badge-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  color: white;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.title-highlight {
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, var(--color-yellow-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.hero-subtitle {
  font-size: 1.3rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  opacity: 0.95;
  font-weight: 400;
  animation: fadeInUp 0.8s ease-out 0.2s backwards;
}

.hero-subtitle strong {
  color: var(--color-yellow-primary);
  font-weight: 600;
}

/* ==========================================
   STATS CON ANIMACIÓN
   ========================================== */
.hero-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease-out;
}

.hero-stats.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.stat {
  text-align: center;
  padding: 1.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  cursor: default;
}

.stat:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-yellow-primary);
  margin-bottom: 0.5rem;
  display: block;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 600;
}

/* ==========================================
   BOTONES
   ========================================== */
.hero-actions {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  animation: fadeInUp 0.8s ease-out 0.4s backwards;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1.2rem 2.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, var(--color-yellow-light) 100%);
  color: var(--color-purple-darkest);
  box-shadow: 0 4px 15px rgba(253, 197, 0, 0.3);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(253, 197, 0, 0.5);
}

.btn-primary:active {
  transform: translateY(-1px);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-3px);
}

/* ==========================================
   CARDS FLOTANTES MEJORADAS
   ========================================== */
.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.floating-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  width: 100%;
  max-width: 450px;
}

.card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 2.5rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: var(--color-purple-darkest);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  text-align: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #ffd755, #ffc403);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.card:hover::before {
  transform: scaleX(1);
}

.card-large {
  min-height: 180px;
  justify-content: center;
}

.card-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.1) 0%, rgba(156, 17, 249, 0.1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.card:hover .card-icon {
  transform: scale(1.1) rotate(5deg);
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.2) 0%, rgba(156, 17, 249, 0.2) 100%);
}

.card-icon :deep(svg) {
  color: var(--color-purple);
}

.card-title {
  font-weight: 700;
  font-size: 1.2rem;
  color: var(--color-purple-darkest);
}

.card-count {
  font-size: 0.85rem;
  color: #666;
  font-weight: 500;
}

.card:hover {
  transform: translateY(-10px) scale(1.05);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

/* Animaciones de flotación específicas por card */
.card-1 {
  animation: float-1 4s ease-in-out infinite;
}
.card-2 {
  animation: float-2 4.5s ease-in-out infinite;
}
.card-3 {
  animation: float-3 5s ease-in-out infinite;
}
.card-4 {
  animation: float-4 4.2s ease-in-out infinite;
}

@keyframes float-1 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(2deg); }
}

@keyframes float-2 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-18px) rotate(-1deg); }
}

@keyframes float-3 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-12px) rotate(1deg); }
}

@keyframes float-4 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-16px) rotate(-2deg); }
}

.card:hover {
  animation-play-state: paused;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1200px) {
  .hero-container {
    gap: 3rem;
    padding: 0 2rem;
  }
  
  .hero-title {
    font-size: 2.6rem;
  }
  
  .floating-cards {
    max-width: 380px;
  }
}

@media (max-width: 968px) {
  .compact-hero {
    padding: 4rem 0;
  }
  
  .hero-container {
    grid-template-columns: 1fr;
    gap: 3rem;
    text-align: center;
    padding: 0 1.5rem;
  }
  
  .hero-title {
    font-size: 2.3rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .hero-stats {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .hero-actions {
    justify-content: center;
  }
  
  .floating-cards {
    max-width: 400px;
    margin: 0 auto;
  }
  
  .card {
    padding: 2rem 1.5rem;
    min-height: 160px;
  }
}

@media (max-width: 640px) {
  .compact-hero {
    padding: 3rem 0;
  }

  .hero-container {
    padding: 0 1rem;
  }
  
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }
  
  .hero-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .hero-stats {
    grid-template-columns: 1fr;
  }
  
  .floating-cards {
    grid-template-columns: 1fr;
    max-width: 280px;
  }
  
  .stat {
    padding: 1.2rem 0.5rem;
  }

  .card-icon {
    width: 60px;
    height: 60px;
  }

  .card-icon :deep(svg) {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .hero-badge {
    font-size: 0.8rem;
    padding: 0.5rem 1rem;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .hero-subtitle {
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
  }

  .btn {
    padding: 1rem 2rem;
    font-size: 1rem;
  }

  .card {
    padding: 1.5rem 1rem;
    min-height: 140px;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .card-count {
    font-size: 0.8rem;
  }
}
</style>