<!-- frontend/src/components/Home/CTABanner.vue -->
<template>
  <section class="cta-banner">
    <div class="cta-content">
      <div class="cta-text">
        <div class="cta-badge">
          <va-icon name="stars" size="small" />
          <span>¡Únete a la comunidad!</span>
        </div>
        <h2>¿Listo para Empezar?</h2>
        <p>Únete a miles de bolivianos que ya encontraron lo que buscaban</p>
        
        <!-- Stats rápidas -->
        <div class="cta-stats">
          <div class="stat-mini">
            <va-icon name="people" />
            <span>+45K usuarios</span>
          </div>
          <div class="stat-mini">
            <va-icon name="verified" />
            <span>+3K verificados</span>
          </div>
          <div class="stat-mini">
            <va-icon name="star" />
            <span>4.8★ calificación</span>
          </div>
        </div>
      </div>
      
      <div class="cta-actions">
        <va-button 
          size="large" 
          class="cta-primary" 
          @click="handlePublish"
        >
          <va-icon name="add_circle" />
           ¡Publica tu anuncio!
        </va-button>
        
        <va-button 
          size="large" 
          class="cta-secondary" 
          @click="handleRegister"
        >
          <va-icon name="person_add"/>
           Regístrate GRATIS
        </va-button>
        
        <p class="cta-help-text">
          Sin costos ocultos · Proceso rápido · Resultados reales
        </p>
      </div>
    </div>

    <!-- Auth Modal -->
    <AuthModal 
      v-model="showAuthModal"
      :initial-tab="modalTab"
      @success="handleAuthSuccess" 
    />
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'
import AuthModal from '@/components/Auth/AuthModal.vue'

const router = useRouter()
const authStore = useAuthStore()
const { init: notify } = useToast()

// State
const showAuthModal = ref(false)
const modalTab = ref('register') // Tab dinámico

/**
 * Manejar click en "Publicar Gratis"
 */
const handlePublish = () => {
  // Si no está autenticado, mostrar modal
  if (!authStore.isAuthenticated) {
    modalTab.value = 'login' // Abrir en Login (asume que ya tiene cuenta)
    showAuthModal.value = true
    notify({
      message: 'Inicia sesión o crea una cuenta para publicar',
      color: 'info',
      duration: 3000
    })
    return
  }
  
  // Si ya está autenticado, ir directo a publicar
  router.push('/publicar')
}

/**
 * Manejar click en "Regístrate Ahora"
 */
const handleRegister = () => {
  // Si ya está autenticado, redirigir al perfil o dashboard
  if (authStore.isAuthenticated) {
    notify({
      message: '¡Ya tienes una cuenta activa! 🎉',
      color: 'success',
      duration: 3000
    })
    // TODO: Redirigir a /perfil o /dashboard cuando exista
    return
  }
  
  // Mostrar modal de auth en tab de registro
  modalTab.value = 'register'
  showAuthModal.value = true
}

/**
 * Manejar éxito en autenticación
 */
const handleAuthSuccess = () => {
  notify({
    message: '¡Bienvenido a Guías Púrpuras! 🎉',
    color: 'success',
    duration: 4000
  })
  
  // Opcional: redirigir automáticamente a publicar después de registro
  setTimeout(() => {
    router.push('/publicar')
  }, 1500)
}
</script>

<style scoped>
/* ==========================================
   CTA BANNER
   ========================================== */
.cta-banner {
  width: 100%;
  padding: 5rem 3rem;
  background: linear-gradient(135deg, #3D0066 0%, #9C11F9 100%);
  position: relative;
  overflow: hidden;
}

/* Patrón de fondo animado */
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
  animation: wave 15s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% { transform: translateX(0) scale(1); }
  50% { transform: translateX(-20px) scale(1.05); }
}

.cta-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

/* ==========================================
   CTA TEXT
   ========================================== */
.cta-text {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cta-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.15);
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: fit-content;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.cta-text h2 {
  font-size: 3rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
  line-height: 1.2;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.cta-text p {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.95);
  line-height: 1.6;
  margin: 0;
}

/* Stats mini */
.cta-stats {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}

.stat-mini {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-yellow-primary);
  font-weight: 600;
  font-size: 0.95rem;
}

.stat-mini :deep(svg) {
  font-size: 1.1rem;
}

/* ==========================================
   CTA ACTIONS
   ========================================== */
.cta-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-start;
}

.cta-primary {
  width: 100%;
  /* 1. SOLUCIÓN AL PROBLEMA DEL MORADO:
     Forzamos el color deseado usando tu variable en la propiedad de mayor prioridad 
     del framework que estaba causando el morado. */
  --va-background-color: var(--color-yellow-primary) !important;
  /* 2. COLOR DE FONDO PRINCIPAL:
     Configuramos el background con un color sólido usando tu variable. */
  background: var(--color-yellow-primary) !important; 
  /* 3. ESTILOS ADICIONALES (Tal como los tenías) */
  color: #ffffff !important;
  font-weight: 700 !important;
  padding: 1.25rem 2rem !important;
  font-size: 1.1rem !important;
  border-radius: 12px !important;
  /* Ajustamos la sombra para que use el color primario (opcional, pero mejora la consistencia) */
  box-shadow: 0 8px 25px rgba(253, 197, 0, 0.4); 
  transition: all 0.3s ease !important;
  border: none !important;
}
.cta-secondary {
  width: 100%;
  background: rgba(255, 255, 255, 0.15) !important;
  border: 2px solid rgba(255, 255, 255, 0.4) !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  padding: 1.25rem 2rem !important;
  font-size: 1.1rem !important;
  border-radius: 12px !important;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease !important;
  border: none;
}

.cta-secondary:hover {
  background: rgba(255, 255, 255, 0.25) !important;
  border-color: rgba(255, 255, 255, 0.6) !important;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.3);
}

.cta-help-text {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.8);
  text-align: center;
  margin: 0.5rem 0 0 0;
  width: 100%;
  font-weight: 500;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1024px) {
  .cta-banner {
    padding: 4rem 2rem;
  }

  .cta-content {
    gap: 3rem;
  }

  .cta-text h2 {
    font-size: 2.5rem;
  }

  .cta-text p {
    font-size: 1.15rem;
  }
}

@media (max-width: 768px) {
  .cta-banner {
    padding: 4rem 1.5rem;
  }

  .cta-content {
    grid-template-columns: 1fr;
    gap: 2.5rem;
    text-align: center;
  }

  .cta-text {
    align-items: center;
  }

  .cta-badge {
    margin: 0 auto;
  }

  .cta-text h2 {
    font-size: 2rem;
  }

  .cta-text p {
    font-size: 1.1rem;
  }

  .cta-stats {
    justify-content: center;
    width: 100%;
  }

  .cta-actions {
    width: 100%;
    align-items: stretch;
  }

  .cta-primary,
  .cta-secondary {
    padding: 1.1rem 1.75rem !important;
    font-size: 1rem !important;
  }
}

@media (max-width: 480px) {
  .cta-banner {
    padding: 3rem 1rem;
  }

  .cta-text h2 {
    font-size: 1.75rem;
  }

  .cta-text p {
    font-size: 1rem;
  }

  .cta-stats {
    flex-direction: column;
    gap: 0.75rem;
    align-items: center;
  }

  .cta-primary,
  .cta-secondary {
    padding: 1rem 1.5rem !important;
    font-size: 0.95rem !important;
  }

  .cta-help-text {
    font-size: 0.8rem;
  }
}
</style>