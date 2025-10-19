<template>
  <!-- 
    TestimonialsSection.vue - Testimonios de usuarios
    
    Propósito: Mostrar reseñas de usuarios satisfechos
    Conecta con: HomeView.vue (componente padre)
    Emite: Ninguno
    Datos: Solo 3 testimonios de ejemplo
  -->
  <section class="testimonials-section">
    <div class="section-container">
      <!-- Header -->
      <div class="section-header centered">
        <div class="section-title-block">
          <h2 class="section-title">Lo que Dicen Nuestros Usuarios</h2>
          <p class="section-subtitle">Miles de personas confían en Guías Púrpuras</p>
        </div>
      </div>

      <!-- Grid de Testimonios -->
      <div class="testimonials-grid">
        <div 
          v-for="testimonial in testimonials" 
          :key="testimonial.id"
          class="testimonial-card"
        >
          <!-- Rating con Estrellas -->
          <div class="testimonial-rating">
            <VaIcon 
              v-for="star in 5" 
              :key="star"
              name="star"
              size="small"
              color="var(--color-orange-primary)"
            />
          </div>

          <!-- Texto del Testimonio -->
          <p class="testimonial-text">"{{ testimonial.text }}"</p>

          <!-- Autor -->
          <div class="testimonial-author">
            <div class="author-avatar" :style="{ background: testimonial.color }">
              {{ testimonial.initials }}
            </div>
            <div class="author-info">
              <h4>{{ testimonial.name }}</h4>
              <p>{{ testimonial.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
/**
 * TestimonialsSection Component
 * 
 * Props: Ninguno (testimonios estáticos)
 * 
 * Emits: Ninguno
 * 
 * State:
 * - testimonials: array de 3 testimonios (estático)
 * 
 * TODO: 
 * - Si se implementa sistema de reviews, obtener desde Django /api/reviews/top/
 */

export default {
  name: 'TestimonialsSection',
  data() {
    return {
      // Testimonios (estático - solo 3 ejemplos)
      testimonials: [
        {
          id: 1,
          name: 'Juan Pérez',
          role: 'Propietario de Restaurante',
          text: 'Gracias a Guías Púrpuras aumentamos nuestras reservas en un 300%. La plataforma es muy fácil de usar y los resultados son increíbles.',
          initials: 'JP',
          color: 'var(--color-purple-dark)'
        },
        {
          id: 2,
          name: 'María González',
          role: 'Abogada',
          text: 'Como profesional, esta plataforma me ayudó a conseguir más clientes en menos tiempo. El plan destacado realmente vale la pena.',
          initials: 'MG',
          color: 'var(--color-orange-primary)'
        },
        {
          id: 3,
          name: 'Roberto Sánchez',
          role: 'Ingeniero Electricista',
          text: 'Publiqué mi servicio hace una semana y ya he recibido más de 20 contactos. Definitivamente la mejor plataforma de clasificados en Bolivia.',
          initials: 'RS',
          color: 'var(--color-success)'
        }
      ]
    }
  }
}
</script>

<style scoped>
/**
 * Estilos de Testimonials Section
 * Cards con avatares y texto destacado
 */

.testimonials-section {
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

/* Testimonials Grid */
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.testimonial-card {
  background: #ffffff;
  padding: 2rem;
  border-radius: 16px;
  border: 2px solid var(--color-gray-100);
  transition: all 0.3s;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  border-color: var(--color-purple-dark);
}

/* Rating */
.testimonial-rating {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

/* Texto */
.testimonial-text {
  color: var(--color-gray-600);
  line-height: 1.8;
  font-size: 1.05rem;
  margin-bottom: 1.5rem;
  font-style: italic;
}

/* Autor */
.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 700;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.author-info h4 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin: 0 0 0.25rem 0;
}

.author-info p {
  font-size: 0.85rem;
  color: var(--color-gray-500);
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .testimonials-section {
    padding: 4rem 1.5rem;
  }

  .testimonials-grid {
    grid-template-columns: 1fr;
  }

  .section-title {
    font-size: 2rem;
  }
}
</style>