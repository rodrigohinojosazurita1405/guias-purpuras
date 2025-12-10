<!-- frontend/src/components/Home/TestimonialsSection.vue -->
<template>
  <section class="testimonials-section">
    <div class="section-container">
      <!-- Header Simple -->
      <div class="section-header">
        <h2 class="section-title">Lo que dicen nuestros usuarios</h2>
        <p class="section-subtitle">Historias reales de éxito en Bolivia</p>
      </div>

      <!-- Testimonios Grid -->
      <div class="testimonials-grid">
        <div
          v-for="testimonial in testimonials"
          :key="testimonial.id"
          class="testimonial-card"
        >
          <!-- Avatar y Info -->
          <div class="testimonial-header">
            <img
              :src="testimonial.image"
              :alt="testimonial.name"
              class="testimonial-avatar"
            />
            <div class="testimonial-info">
              <h3 class="testimonial-name">{{ testimonial.name }}</h3>
              <p class="testimonial-role">{{ testimonial.role }}</p>
              <p class="testimonial-location">
                <va-icon name="location_on" size="12px" />
                {{ testimonial.city }}
              </p>
            </div>
          </div>

          <!-- Texto breve -->
          <p class="testimonial-text">"{{ testimonial.text }}"</p>

          <!-- Rating -->
          <div class="testimonial-rating">
            <va-icon
              v-for="star in 5"
              :key="star"
              name="star"
              size="16px"
              :color="star <= testimonial.rating ? 'var(--color-yellow-primary)' : '#E5E7EB'"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

// Solo 3 testimonios reales y concisos
const testimonials = ref([
  {
    id: 1,
    name: 'Juan Pérez',
    role: 'Propietario de Restaurante',
    city: 'La Paz',
    text: 'En 3 meses aumentamos nuestras reservas un 300%. La plataforma es fácil de usar y el soporte excepcional.',
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop',
    rating: 5
  },
  {
    id: 2,
    name: 'María González',
    role: 'Abogada Independiente',
    city: 'Cochabamba',
    text: 'Conseguí más de 50 clientes nuevos en 2 meses. El plan destacado vale cada boliviano invertido.',
    image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&h=150&fit=crop',
    rating: 5
  },
  {
    id: 3,
    name: 'Roberto Sánchez',
    role: 'Ingeniero Electricista',
    city: 'Santa Cruz',
    text: 'En una semana recibí más de 20 contactos reales. La mejor inversión para mi negocio.',
    image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop',
    rating: 5
  }
])
</script>

<style scoped>
/* ==========================================
   SECTION
   ========================================== */
.testimonials-section {
  width: 100%;
  padding: 4rem 2rem;
  background: white;
}

.section-container {
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.5rem 0;
}

.section-subtitle {
  font-size: 0.9375rem;
  color: #6B7280;
  margin: 0;
}

/* ==========================================
   TESTIMONIALS GRID
   ========================================== */
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.testimonial-card {
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 2rem;
  transition: all 0.2s ease;
}

.testimonial-card:hover {
  border-color: var(--color-purple);
  box-shadow: 0 8px 20px rgba(92, 0, 153, 0.1);
  transform: translateY(-4px);
}

/* Header */
.testimonial-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.testimonial-avatar {
  width: 56px;
  height: 56px;
  min-width: 56px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.testimonial-info {
  flex: 1;
  min-width: 0;
}

.testimonial-name {
  font-size: 1rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.25rem 0;
}

.testimonial-role {
  font-size: 0.875rem;
  color: #6B7280;
  margin: 0 0 0.25rem 0;
}

.testimonial-location {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8125rem;
  color: #9CA3AF;
  margin: 0;
}

/* Texto */
.testimonial-text {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: #374151;
  margin: 0 0 1rem 0;
  font-style: italic;
}

/* Rating */
.testimonial-rating {
  display: flex;
  gap: 0.25rem;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1024px) {
  .testimonials-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .testimonial-card {
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .testimonials-section {
    padding: 3rem 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .section-subtitle {
    font-size: 0.875rem;
  }

  .section-header {
    margin-bottom: 2rem;
  }

  .testimonial-card {
    padding: 1.25rem;
  }

  .testimonial-avatar {
    width: 48px;
    height: 48px;
    min-width: 48px;
  }

  .testimonial-name {
    font-size: 0.9375rem;
  }

  .testimonial-role {
    font-size: 0.8125rem;
  }

  .testimonial-text {
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .testimonials-section {
    padding: 2.5rem 0.75rem;
  }

  .section-title {
    font-size: 1.375rem;
  }

  .testimonial-card {
    padding: 1rem;
  }
}
</style>
