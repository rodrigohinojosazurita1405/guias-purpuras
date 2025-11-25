<!-- frontend/src/components/Home/TestimonialsSection.vue -->
<template>
  <section class="testimonials-section">
    <div class="section-container">
      <!-- Header Mejorado -->
      <div class="section-header">
        <div class="header-content">
          <span class="section-badge">Testimonios</span>
          <h2 class="section-title">Lo que Dicen Nuestros Usuarios</h2>
          <p class="section-subtitle">
            Más de <strong>10,000 usuarios</strong> confían en Guías Púrpuras cada mes
          </p>
        </div>
        
        <!-- Controles del Slider -->
        <div class="slider-controls">
          <button @click="prevSlide" class="control-btn" :disabled="currentSlide === 0">
            <va-icon name="chevron_left" size="1.5rem" />
          </button>
          <button @click="nextSlide" class="control-btn" :disabled="currentSlide === maxSlide">
            <va-icon name="chevron_right" size="1.5rem" />
          </button>
        </div>
      </div>

      <!-- Slider de Testimonios -->
      <div class="testimonials-slider">
        <div 
          class="slider-track" 
          :style="{ transform: `translateX(-${currentSlide * slideWidth}%)` }"
        >
          <div
            v-for="testimonial in testimonials"
            :key="testimonial.id"
            class="testimonial-card"
          >
            <!-- Icono de Quote -->
            <div class="quote-icon">
              <svg viewBox="0 0 24 24" width="48" height="48">
                <path fill="currentColor" d="M6,17h3l2-4V7H5v6h3L6,17z M18,17h3l2-4V7h-6v6h3L18,17z"/>
              </svg>
            </div>

            <!-- Rating con Estrellas -->
            <div class="testimonial-rating">
              <va-icon 
                v-for="star in 5" 
                :key="star"
                name="star"
                size="small"
                :color="star <= testimonial.rating ? 'var(--color-yellow-primary)' : '#E0E0E0'"
              />
              <span class="rating-number">{{ testimonial.rating }}.0</span>
            </div>

            <!-- Texto del Testimonio -->
            <p class="testimonial-text">"{{ testimonial.text }}"</p>

            <!-- Autor con Imagen Real -->
            <div class="testimonial-author">
              <div class="author-image-wrapper">
                <img 
                  :src="testimonial.image" 
                  :alt="testimonial.name"
                  class="author-image"
                />
                <div class="verified-badge" v-if="testimonial.verified">
                  <va-icon name="verified" size="16px" />
                </div>
              </div>
              <div class="author-info">
                <h4 class="author-name">{{ testimonial.name }}</h4>
                <p class="author-role">{{ testimonial.role }}</p>
                <p class="author-location" v-if="testimonial.city">
                  <va-icon name="location_on" size="12px" />
                  {{ testimonial.city }}
                </p>
              </div>
            </div>

            <!-- Badge del Plan -->
            <div class="plan-badge" v-if="testimonial.plan">
              <va-icon name="workspace_premium" size="14px" />
              Plan {{ testimonial.plan }}
            </div>
          </div>
        </div>
      </div>

      <!-- Dots Indicadores -->
      <div class="slider-dots">
        <button
          v-for="(_, index) in totalSlides"
          :key="index"
          @click="goToSlide(index)"
          :class="['dot', { active: currentSlide === index }]"
          :aria-label="`Ir a testimonio ${index + 1}`"
        />
      </div>

      <!-- Stats Section -->
      <div class="testimonials-stats">
        <div class="stat-item">
          <div class="stat-icon">
            <va-icon name="star" size="2rem" color="var(--color-yellow-primary)" />
          </div>
          <div class="stat-content">
            <span class="stat-number">4.9</span>
            <span class="stat-label">Calificación promedio</span>
          </div>
        </div>
        
        <div class="stat-item">
          <div class="stat-icon">
            <va-icon name="groups" size="2rem" color="var(--color-purple)" />
          </div>
          <div class="stat-content">
            <span class="stat-number">10,000+</span>
            <span class="stat-label">Usuarios activos</span>
          </div>
        </div>
        
        <div class="stat-item">
          <div class="stat-icon">
            <va-icon name="verified" size="2rem" color="var(--color-success)" />
          </div>
          <div class="stat-content">
            <span class="stat-number">98%</span>
            <span class="stat-label">Satisfacción</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// ==========================================
// STATE
// ==========================================
const currentSlide = ref(0)
const autoplayInterval = ref(null)

// ==========================================
// DATA - Testimonios con imágenes reales
// ==========================================
const testimonials = [
  {
    id: 1,
    name: 'Juan Pérez',
    role: 'Propietario de Restaurante El Fogón',
    city: 'La Paz',
    text: 'Gracias a Guías Púrpuras aumentamos nuestras reservas en un 300% en solo 3 meses. La plataforma es muy fácil de usar y el soporte es excepcional. ¡Totalmente recomendado!',
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop',
    rating: 5,
    verified: true,
    plan: 'TOP'
  },
  {
    id: 2,
    name: 'María González',
    role: 'Abogada Especialista',
    city: 'Cochabamba',
    text: 'Como profesional independiente, esta plataforma me ayudó a conseguir más de 50 clientes nuevos en menos de 2 meses. El plan destacado realmente vale cada boliviano invertido.',
    image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=300&h=300&fit=crop',
    rating: 5,
    verified: true,
    plan: 'Destacado'
  },
  {
    id: 3,
    name: 'Roberto Sánchez',
    role: 'Ingeniero Electricista',
    city: 'Santa Cruz',
    text: 'Publiqué mi servicio hace una semana y ya recibí más de 20 contactos reales. La mejor inversión que he hecho para mi negocio. Definitivamente la plataforma #1 en Bolivia.',
    image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&h=300&fit=crop',
    rating: 5,
    verified: true,
    plan: 'Premium'
  },
  {
    id: 4,
    name: 'Ana Martínez',
    role: 'Dueña de Cafetería Aroma',
    city: 'Tarija',
    text: 'Increíble plataforma. Nuestro local pasó de estar vacío a tener filas de espera. El sistema de reseñas nos ayudó a generar confianza con nuevos clientes. ¡Gracias Guías Púrpuras!',
    image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=300&h=300&fit=crop',
    rating: 5,
    verified: true,
    plan: 'TOP'
  },
  {
    id: 5,
    name: 'Carlos Mendoza',
    role: 'Contador Público',
    city: 'Oruro',
    text: 'La mejor decisión fue crear mi perfil profesional aquí. He conseguido clientes corporativos importantes que nunca hubiera alcanzado de otra forma. Excelente ROI.',
    image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop',
    rating: 5,
    verified: true,
    plan: 'Destacado'
  },
  {
    id: 6,
    name: 'Lucía Flores',
    role: 'Doctora Pediatra',
    city: 'Sucre',
    text: 'Como médica recién establecida, necesitaba dar a conocer mi consultorio. En 3 semanas ya tenía mi agenda llena. La plataforma es profesional y confiable. 100% recomendada.',
    image: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop',
    rating: 5,
    verified: true,
    plan: 'Premium'
  }
]

// ==========================================
// COMPUTED
// ==========================================
const slideWidth = computed(() => {
  // En desktop: 33.33% (3 cards visibles)
  // En tablet: 50% (2 cards visibles)
  // En mobile: 100% (1 card visible)
  if (window.innerWidth >= 1024) return 33.33
  if (window.innerWidth >= 768) return 50
  return 100
})

const cardsPerView = computed(() => {
  if (window.innerWidth >= 1024) return 3
  if (window.innerWidth >= 768) return 2
  return 1
})

const totalSlides = computed(() => {
  return Math.ceil(testimonials.length / cardsPerView.value)
})

const maxSlide = computed(() => {
  return totalSlides.value - 1
})

// ==========================================
// MÉTODOS
// ==========================================
const nextSlide = () => {
  if (currentSlide.value < maxSlide.value) {
    currentSlide.value++
  } else {
    currentSlide.value = 0 // Loop
  }
}

const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--
  } else {
    currentSlide.value = maxSlide.value // Loop inverso
  }
}

const goToSlide = (index) => {
  currentSlide.value = index
}

// Autoplay
const startAutoplay = () => {
  autoplayInterval.value = setInterval(() => {
    nextSlide()
  }, 5000) // Cada 5 segundos
}

const stopAutoplay = () => {
  if (autoplayInterval.value) {
    clearInterval(autoplayInterval.value)
  }
}

// Keyboard navigation
const handleKeyPress = (event) => {
  if (event.key === 'ArrowLeft') {
    prevSlide()
  } else if (event.key === 'ArrowRight') {
    nextSlide()
  }
}

// ==========================================
// LIFECYCLE
// ==========================================
onMounted(() => {
  startAutoplay()
  document.addEventListener('keydown', handleKeyPress)
})

onUnmounted(() => {
  stopAutoplay()
  document.removeEventListener('keydown', handleKeyPress)
})
</script>

<style scoped>
/* ==========================================
   SECTION BASE
   ========================================== */
.testimonials-section {
  width: 100%;
  padding: 6rem 2rem;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFFFFF 100%);
  position: relative;
  overflow: hidden;
}

/* Patrón de fondo sutil */
.testimonials-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(92, 0, 153, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(253, 197, 0, 0.03) 0%, transparent 50%);
  pointer-events: none;
}

.section-container {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* ==========================================
   HEADER MEJORADO
   ========================================== */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4rem;
  gap: 2rem;
  flex-wrap: wrap;
}

.header-content {
  flex: 1;
  text-align: center;
}

.section-badge {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 1rem;
}

.section-title {
  font-size: 2.75rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin-bottom: 1rem;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #666;
  line-height: 1.6;
}

.section-subtitle strong {
  color: var(--color-purple);
  font-weight: 700;
}

/* ==========================================
   SLIDER CONTROLS
   ========================================== */
.slider-controls {
  display: flex;
  gap: 1rem;
}

.control-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid var(--color-purple);
  background: white;
  color: var(--color-purple);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-btn:hover:not(:disabled) {
  background: var(--color-purple);
  color: white;
  transform: scale(1.1);
}

.control-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* ==========================================
   SLIDER
   ========================================== */
.testimonials-slider {
  overflow: hidden;
  margin-bottom: 2rem;
}

.slider-track {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  gap: 2rem;
}

/* ==========================================
   TESTIMONIAL CARDS
   ========================================== */
.testimonial-card {
  min-width: calc(33.33% - 1.33rem);
  background: white;
  padding: 2.5rem;
  border-radius: 20px;
  border: 2px solid transparent;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

/* Gradiente en el borde al hover */
.testimonial-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 20px;
  padding: 2px;
  background: linear-gradient(135deg, var(--color-purple) 70%, var(--color-yellow-primary) 30%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.testimonial-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 40px rgba(92, 0, 153, 0.2);
}

.testimonial-card:hover::before {
  opacity: 1;
}

/* Quote Icon */
.quote-icon {
  color: var(--color-purple);
  opacity: 0.15;
  margin-bottom: 1rem;
}

/* Rating */
.testimonial-rating {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-bottom: 1.25rem;
}

.rating-number {
  margin-left: 0.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  font-size: 0.95rem;
}

/* Texto */
.testimonial-text {
  color: #555;
  line-height: 1.8;
  font-size: 1.05rem;
  margin-bottom: 2rem;
  font-style: italic;
  position: relative;
  padding-left: 1rem;
  border-left: 3px solid var(--color-yellow-primary);
}

/* Autor */
.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 1rem;
}

.author-image-wrapper {
  position: relative;
  flex-shrink: 0;
}

.author-image {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.verified-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 24px;
  height: 24px;
  background: var(--color-success);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  border: 2px solid white;
}

.author-info {
  flex: 1;
}

.author-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.25rem 0;
}

.author-role {
  font-size: 0.9rem;
  color: #666;
  margin: 0 0 0.25rem 0;
}

.author-location {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  color: #999;
  margin: 0;
}

/* Plan Badge */
.plan-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, var(--color-yellow-light) 100%);
  color: var(--color-purple-darkest);
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
}

/* ==========================================
   DOTS INDICADORES
   ========================================== */
.slider-dots {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 2rem 0 3rem 0;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: none;
  background: #D0D0D0;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.dot:hover {
  background: var(--color-purple);
  transform: scale(1.3);
}

.dot.active {
  background: linear-gradient(135deg, var(--color-yellow-primary) 100%);
  width: 32px;
  border-radius: 6px;
}

/* ==========================================
   STATS SECTION
   ========================================== */
.testimonials-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  max-width: 900px;
  margin: 0 auto;
  padding: 3rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(92, 0, 153, 0.1);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.05) 0%, rgba(253, 197, 0, 0.05) 100%);
  transform: translateY(-4px);
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFF 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1024px) {
  .testimonial-card {
    min-width: calc(50% - 1rem);
  }

  .testimonials-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .testimonials-section {
    padding: 4rem 1.5rem;
  }

  .section-header {
    flex-direction: column;
    text-align: center;
  }

  .section-title {
    font-size: 2rem;
  }

  .slider-controls {
    order: -1;
    width: 100%;
    justify-content: center;
  }

  .testimonial-card {
    min-width: 100%;
    padding: 2rem;
  }

  .testimonials-stats {
    grid-template-columns: 1fr;
    padding: 2rem 1.5rem;
  }

  .stat-item {
    justify-content: center;
  }
}

/* Animaciones de entrada */
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

.testimonial-card {
  animation: fadeInUp 0.6s ease backwards;
}

.testimonial-card:nth-child(1) { animation-delay: 0.1s; }
.testimonial-card:nth-child(2) { animation-delay: 0.2s; }
.testimonial-card:nth-child(3) { animation-delay: 0.3s; }
</style>