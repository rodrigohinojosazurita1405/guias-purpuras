<!-- frontend/src/views/NotFoundView.vue -->
<template>
  <MainLayout>
    <section class="not-found-section">
      <div class="not-found-content">
        <div class="error-icon">
          <va-icon name="search_off" size="6rem" color="purple" />
        </div>

        <h1 class="error-code">404</h1>
        <h2 class="error-title">Página no encontrada</h2>
        <p class="error-description">
          Lo sentimos, la página que buscas no existe o ha sido movida.
        </p>

        <div class="error-actions">
          <va-button
            @click="goHome"
            color="purple"
            size="large"
          >
            <va-icon name="home" />
            Volver al inicio
          </va-button>

          <va-button
            @click="goBack"
            color="yellow-primary"
            size="large"
          >
            <va-icon name="arrow_back" />
            Página anterior
          </va-button>
        </div>

        <!-- Links útiles -->
        <div class="useful-links">
          <p class="links-title">Enlaces útiles:</p>
          <div class="links-grid">
            <router-link to="/guias/profesionales" class="link-item">
              <va-icon name="work" />
              Profesionales
            </router-link>
            <router-link to="/guias/gastronomia" class="link-item">
              <va-icon name="restaurant" />
              Gastronomía
            </router-link>
            <router-link to="/guias/trabajos" class="link-item">
              <va-icon name="business_center" />
              Trabajos
            </router-link>
            <router-link to="/guias/servicios" class="link-item">
              <va-icon name="build" />
              Servicios
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import MainLayout from '../components/Layout/MainLayout.vue'

// ==========================================
// COMPOSABLES
// ==========================================
const router = useRouter()

// ==========================================
// MÉTODOS
// ==========================================
const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
/* ==========================================
   NOT FOUND SECTION
   ========================================== */
.not-found-section {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
}

.not-found-content {
  max-width: 600px;
  text-align: center;
}

/* ==========================================
   ERROR CONTENT
   ========================================== */
.error-icon {
  margin-bottom: 2rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.error-code {
  font-size: 6rem;
  font-weight: 900;
  color: var(--color-purple);
  margin: 0;
  line-height: 1;
}

.error-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 1rem 0;
}

.error-description {
  font-size: 1.125rem;
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

/* ==========================================
   ACTIONS
   ========================================== */
.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 3rem;
  flex-wrap: wrap;
}

/* ==========================================
   USEFUL LINKS
   ========================================== */
.useful-links {
  padding-top: 2rem;
  border-top: 2px solid #E0E0E0;
}

.links-title {
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin-bottom: 1rem;
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.link-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: white;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  color: var(--color-purple);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.link-item:hover {
  border-color: var(--color-purple);
  background: var(--color-purple);
  color: white;
  transform: translateY(-2px);
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
  .error-code {
    font-size: 4rem;
  }

  .error-title {
    font-size: 1.5rem;
  }

  .error-actions {
    flex-direction: column;
  }

  .error-actions button {
    width: 100%;
  }

  .links-grid {
    grid-template-columns: 1fr;
  }
}
</style>