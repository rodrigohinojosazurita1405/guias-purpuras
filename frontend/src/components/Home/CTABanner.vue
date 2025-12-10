<!-- frontend/src/components/Home/CTABanner.vue -->
<template>
  <section class="cta-banner">
    <div class="cta-container">
      <div class="cta-content">
        <h2 class="cta-title">¿Estás buscando talento para tu empresa?</h2>
        <p class="cta-subtitle">Publica tus ofertas de empleo y encuentra a los mejores candidatos en Bolivia</p>
        <button class="cta-button" @click="handleRegister">
          Publicar empleo ahora
          <va-icon name="arrow_forward" size="20px" />
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'

const router = useRouter()
const authStore = useAuthStore()
const { init: notify } = useToast()

const handleRegister = () => {
  if (authStore.isAuthenticated) {
    // Si ya está autenticado, ir al dashboard
    router.push('/dashboard')
    notify({
      message: '¡Ya tienes una cuenta activa!',
      color: 'success'
    })
    return
  }

  // Si no está autenticado, ir al login/register
  router.push('/login')
}
</script>

<style scoped>
/* ==========================================
   CTA BANNER - MINIMALISTA
   ========================================== */
.cta-banner {
  width: 100%;
  padding: 4rem 2rem;
  background: #F9FAFB;
  border-top: 1px solid #E5E7EB;
}

.cta-container {
  max-width: 1400px;
  margin: 0 auto;
}

.cta-content {
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* Patrón decorativo sutil */
.cta-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(253, 197, 0, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

/* Contenido */
.cta-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.75rem 0;
  position: relative;
  z-index: 1;
}

.cta-subtitle {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 2rem 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  z-index: 1;
}

/* Botón amarillo destacado */
.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2.5rem;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  border: none;
  border-radius: 8px;
  font-size: 1.125rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 15px rgba(253, 197, 0, 0.3);
  position: relative;
  z-index: 1;
}

.cta-button:hover {
  background: var(--color-yellow-light);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(253, 197, 0, 0.4);
}

.cta-button:active {
  transform: translateY(0);
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
  .cta-banner {
    padding: 3rem 1rem;
  }

  .cta-content {
    padding: 2.5rem 1.5rem;
  }

  .cta-title {
    font-size: 1.5rem;
  }

  .cta-subtitle {
    font-size: 1rem;
    margin-bottom: 1.5rem;
  }

  .cta-button {
    padding: 0.875rem 2rem;
    font-size: 1rem;
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .cta-banner {
    padding: 2.5rem 0.75rem;
  }

  .cta-content {
    padding: 2rem 1rem;
    border-radius: 12px;
  }

  .cta-title {
    font-size: 1.375rem;
  }

  .cta-subtitle {
    font-size: 0.9375rem;
  }

  .cta-button {
    padding: 0.75rem 1.5rem;
    font-size: 0.9375rem;
  }
}
</style>
