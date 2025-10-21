<!-- frontend/src/components/Layout/Navbar.vue -->
<template>
  <nav class="navbar">
    <div class="navbar-content">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <img src="/src/assets/guiaspurpuras.ico" alt="Logo Guías Púrpuras" class="logo-image" />
        <span class="logo-text">Guías Púrpuras</span>
        <span class="logo-country">Bolivia</span>
      </router-link>

      <!-- Desktop Navigation -->
      <div class="nav-links desktop-only">
        <router-link 
          to="/" 
          class="nav-link"
          exact-active-class="active"
        >
          <va-icon name="home" size="small" />
          Inicio
        </router-link>
        
        <router-link 
          to="/guias/profesionales" 
          class="nav-link"
          active-class="active"
        >
          <va-icon name="work" size="small" />
          Profesionales
        </router-link>
        
        <router-link 
          to="/guias/gastronomia" 
          class="nav-link"
          active-class="active"
        >
          <va-icon name="restaurant" size="small" />
          Gastronomía
        </router-link>
        
        <router-link 
          to="/guias/trabajos" 
          class="nav-link"
          active-class="active"
        >
          <va-icon name="business_center" size="small" />
          Trabajos
        </router-link>
        
        <router-link 
          to="/guias/servicios" 
          class="nav-link"
          active-class="active"
        >
          <va-icon name="build" size="small" />
          Servicios
        </router-link>
      </div>

      <!-- Botón Publicar -->
      <div class="nav-actions">
        <va-button
          @click="goToPublish"
          color="yellow-primary"
          class="publish-btn"
        >
          <va-icon name="add_circle" />
          Publicar Gratis
        </va-button>

        <!-- Mobile Menu Toggle -->
        <va-button
          @click="toggleMobileMenu"
          icon="menu"
          color="purple"
          class="mobile-menu-btn"
          flat
        />
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition name="slide">
      <div v-if="mobileMenuOpen" class="mobile-menu">
        <router-link 
          to="/" 
          class="mobile-link"
          @click="closeMobileMenu"
          exact-active-class="active"
        >
          <va-icon name="home" />
          Inicio
        </router-link>
        
        <router-link 
          to="/guias/profesionales" 
          class="mobile-link"
          @click="closeMobileMenu"
          active-class="active"
        >
          <va-icon name="work" />
          Profesionales
        </router-link>
        
        <router-link 
          to="/guias/gastronomia" 
          class="mobile-link"
          @click="closeMobileMenu"
          active-class="active"
        >
          <va-icon name="restaurant" />
          Gastronomía
        </router-link>
        
        <router-link 
          to="/guias/trabajos" 
          class="mobile-link"
          @click="closeMobileMenu"
          active-class="active"
        >
          <va-icon name="business_center" />
          Trabajos
        </router-link>
        
        <router-link 
          to="/guias/servicios" 
          class="mobile-link"
          @click="closeMobileMenu"
          active-class="active"
        >
          <va-icon name="build" />
          Servicios
        </router-link>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// ==========================================
// COMPOSABLES
// ==========================================
const router = useRouter()
const mobileMenuOpen = ref(false)

// ==========================================
// MÉTODOS
// ==========================================
const goToPublish = () => {
  router.push('/publicar')
  closeMobileMenu()
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}
</script>

<style scoped>
/* ==========================================
   NAVBAR PRINCIPAL
   ========================================== */
.navbar {
  background-color: var(--color-purple);
  color: white;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.navbar-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

/* ==========================================
   LOGO
   ========================================== */
.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: white;
  font-weight: 700;
  font-size: 1.25rem;
  white-space: nowrap;
}

.logo-image {
  height: 32px; /* Ajusta este valor al tamaño que desees para el icono */
  width: auto;
}
.logo-text {
  color: white;
}

.logo-country {
  color: var(--color-yellow-primary);
  font-size: 0.9rem;
}

/* ==========================================
   NAVEGACIÓN DESKTOP
   ========================================== */
.nav-links {
  display: flex;
  gap: 0.5rem;
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1rem;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.nav-link.active {
  background-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

/* ==========================================
   BOTÓN PUBLICAR
   ========================================== */
.nav-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.publish-btn {
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3);
  transition: all 0.3s ease;
}

.publish-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(253, 197, 0, 0.4);
}

.mobile-menu-btn {
  display: none;
}

/* ==========================================
   MENÚ MÓVIL
   ========================================== */
.mobile-menu {
  background-color: var(--color-purple-dark);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.mobile-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.mobile-link.active {
  background-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

/* ==========================================
   TRANSICIONES
   ========================================== */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1024px) {
  .nav-links {
    gap: 0.25rem;
  }
  
  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 768px) {
  .desktop-only {
    display: none;
  }
  
  .mobile-menu-btn {
    display: flex;
  }
  
  .publish-btn span {
    display: none;
  }
}
</style>