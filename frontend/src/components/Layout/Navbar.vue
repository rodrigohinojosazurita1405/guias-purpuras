<template>
  <!-- 
    Navbar.vue - Barra de navegación principal
    
    Propósito: Navegación principal del sitio con logo, menú y acciones
    Conecta con: MainLayout.vue (componente padre)
    Emite: change-location (cuando se hace clic en ubicación)
    Ubicación: Sticky debajo del TopBar
  -->
  <nav class="main-navbar" :class="{ 'scrolled': isScrolled }">
    <div class="navbar-container">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <div class="logo-icon">
          <VaIcon name="bookmark" size="large" />
        </div>
        <div class="logo-text">
          <h1>Guías Púrpuras</h1>
          <span>Bolivia</span>
        </div>
      </router-link>

      <!-- Selector de Ubicación -->
      <div class="location-display" @click="$emit('change-location')">
        <VaIcon name="location_on" color="var(--color-orange-primary)" />
        <div class="location-text">
          <span class="location-label">Tu ubicación</span>
          <span class="location-value">{{ currentLocation }}</span>
        </div>
        <VaIcon name="expand_more" size="small" />
      </div>

      <!-- Menú Principal -->
      <div class="main-menu" :class="{ 'mobile-open': mobileMenuOpen }">
        <a href="#" class="menu-item" :class="{ active: activeMenu === 'inicio' }">
          <VaIcon name="home" size="small" />
          Inicio
        </a>
        <a href="#" class="menu-item" :class="{ active: activeMenu === 'profesionales' }">
          <VaIcon name="business_center" size="small" />
          Profesionales
        </a>
        <a href="#" class="menu-item" :class="{ active: activeMenu === 'gastronomia' }">
          <VaIcon name="restaurant" size="small" />
          Gastronomía
        </a>
        <a href="#" class="menu-item" :class="{ active: activeMenu === 'trabajos' }">
          <VaIcon name="work" size="small" />
          Trabajos
        </a>
        <a href="#" class="menu-item" :class="{ active: activeMenu === 'servicios' }">
          <VaIcon name="build" size="small" />
          Servicios
        </a>
      </div>

      <!-- Botones de Acción -->
      <div class="nav-actions">
        <VaButton 
          preset="plain" 
          icon="person" 
          class="login-btn"
          @click="handleLogin"
        >
          Ingresar
        </VaButton>
        <VaButton 
          class="publish-btn"
          icon="add_circle"
          @click="handlePublish"
        >
          Publicar Gratis
        </VaButton>
      </div>

      <!-- Toggle Mobile Menu -->
      <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen">
        <VaIcon :name="mobileMenuOpen ? 'close' : 'menu'" />
      </button>
    </div>
  </nav>
</template>

<script>
/**
 * Navbar Component
 * 
 * Props:
 * - currentLocation: String (ubicación actual del usuario)
 * 
 * Emits:
 * - change-location: cuando se hace clic en el selector de ubicación
 * 
 * State:
 * - isScrolled: detecta si el usuario hizo scroll
 * - mobileMenuOpen: estado del menú móvil
 * - activeMenu: item activo del menú
 */

export default {
  name: 'Navbar',
  props: {
    currentLocation: {
      type: String,
      default: 'Cochabamba, Bolivia'
    }
  },
  emits: ['change-location'],
  data() {
    return {
      isScrolled: false,
      mobileMenuOpen: false,
      activeMenu: 'inicio'
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 50
    },
    handleLogin() {
      console.log('Login clicked')
      // TODO: Conectar con sistema de autenticación Django
    },
    handlePublish() {
      console.log('Publish clicked')
      // TODO: Redirigir a PublishView.vue
    }
  }
}
</script>

<style scoped>
/**
 * Estilos del Navbar
 * Usa variables CSS de App.vue
 */

.main-navbar {
  background: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s;
  width: 100%;
}

.main-navbar.scrolled {
  box-shadow: 0 4px 20px rgba(26, 11, 61, 0.15);
}

.navbar-container {
  max-width: 100%;
  padding: 1rem 3rem;
  display: flex;
  align-items: center;
  gap: 2rem;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, var(--color-purple-dark) 0%, var(--color-purple) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
}

.logo-text h1 {
  font-size: 1.4rem;
  color: var(--color-purple-dark);
  margin: 0;
  font-weight: 700;
  line-height: 1;
}

.logo-text span {
  font-size: 0.75rem;
  color: var(--color-purple);
  display: block;
  margin-top: 2px;
}

/* Location Display */
.location-display {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  background: #FEF3C7;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  flex-shrink: 0;
}

.location-display:hover {
  background: #FDE68A;
  transform: translateY(-2px);
}

.location-text {
  display: flex;
  flex-direction: column;
}

.location-label {
  font-size: 0.7rem;
  color: #92400E;
  font-weight: 500;
}

.location-value {
  font-size: 0.9rem;
  color: var(--color-gray-900);
  font-weight: 600;
}

/* Main Menu */
.main-menu {
  display: flex;
  gap: 0.5rem;
  flex: 1;
  justify-content: center;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  color: var(--color-gray-600);
  text-decoration: none;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s;
  white-space: nowrap;
}

.menu-item:hover,
.menu-item.active {
  background: var(--color-gray-100);
  color: var(--color-purple-dark);
}

/* Action Buttons */
.nav-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-shrink: 0;
}

.login-btn {
  color: var(--color-gray-600) !important;
  font-weight: 500 !important;
}

.publish-btn {
  background: linear-gradient(135deg, var(--color-orange-primary) 0%, var(--color-orange-light) 100%) !important;
  color: #ffffff !important;
  font-weight: 600 !important;
  padding: 0.75rem 1.5rem !important;
  box-shadow: 0 4px 15px rgba(255, 140, 0, 0.3);
  border-radius: 10px !important;
}

.publish-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 140, 0, 0.4);
}

/* Mobile Toggle */
.mobile-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--color-purple-dark);
  cursor: pointer;
}

/* Responsive */
@media (max-width: 1200px) {
  .main-menu {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }

  .main-menu.mobile-open {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #ffffff;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    padding: 1rem;
    gap: 0;
  }

  .menu-item {
    padding: 1rem;
    border-radius: 0;
    border-bottom: 1px solid var(--color-gray-100);
  }
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 1rem 1.5rem;
    flex-wrap: wrap;
  }

  .location-display {
    order: 3;
    width: 100%;
    margin-top: 1rem;
  }

  .nav-actions {
    gap: 0.5rem;
  }

  .login-btn span {
    display: none;
  }

  .publish-btn {
    padding: 0.75rem 1rem !important;
    font-size: 0.9rem !important;
  }
}
</style>