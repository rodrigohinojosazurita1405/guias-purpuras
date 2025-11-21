<!-- Navbar - Clean & Minimal Version -->
<template>
  <nav class="navbar">
    <div class="navbar-content">
      <!-- Logo -->
      <router-link to="/" class="logo" @click="closeMobileMenu">
        <img src="/src/assets/guiaspurpuras.ico" alt="Logo" class="logo-image" />
        <div class="logo-text-wrapper">
          <span class="logo-text">Guías Púrpuras</span>
          <span class="logo-country">Bolivia</span>
        </div>
      </router-link>

      <!-- Desktop Navigation -->
      <div class="nav-links desktop-only">
        <router-link to="/" class="nav-link" exact-active-class="active">
          <va-icon name="home" size="small" />
          <span>Inicio</span>
        </router-link>

        <router-link to="/guias/trabajos" class="nav-link" active-class="active">
          <va-icon name="business_center" size="small" />
          <span>Empleos</span>
        </router-link>

        <router-link to="/nosotros" class="nav-link" active-class="active">
          <va-icon name="info" size="small" />
          <span>Sobre Nosotros</span>
        </router-link>
      </div>

      <!-- Actions -->
      <div class="nav-actions">
        <!-- Publish Button -->
        <va-button @click="handlePublish" class="publish-btn">
          <va-icon name="add_circle" size="small" />
          <span class="btn-text">Publicar empleo</span>
          <span class="btn-text-short">Publicar</span>
        </va-button>

        <!-- NOT Authenticated: Show Login Button -->
        <router-link v-if="!authStore.isAuthenticated" to="/login" class="login-btn desktop-only">
          <va-icon name="login" size="small" />
          <span>Ingresar</span>
        </router-link>

        <!-- Authenticated: Show Avatar Button (Simple - No Dropdown) -->
        <button v-else @click="doLogout" class="user-avatar-btn desktop-only" title="Click para cerrar sesión">
          <div class="user-avatar">{{ authStore.userInitials }}</div>
          <va-icon name="logout" size="small" class="logout-icon" />
        </button>

        <!-- Mobile Menu Button -->
        <button @click="toggleMobileMenu" class="mobile-menu-btn" :class="{ active: mobileMenuOpen }">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
    </div>

    <!-- Mobile Overlay -->
    <transition name="fade">
      <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
    </transition>

    <!-- Mobile Menu -->
    <transition name="slide-in">
      <div v-if="mobileMenuOpen" class="mobile-menu">
        <div class="mobile-menu-header">
          <span>Menú</span>
          <button @click="closeMobileMenu" class="close-btn">
            <va-icon name="close" />
          </button>
        </div>

        <!-- Mobile Navigation -->
        <div class="mobile-nav-section">
          <router-link to="/" class="mobile-link" @click="closeMobileMenu" exact-active-class="active">
            <va-icon name="home" />
            <span>Inicio</span>
          </router-link>

          <router-link to="/guias/trabajos" class="mobile-link" @click="closeMobileMenu" active-class="active">
            <va-icon name="business_center" />
            <span>Empleos</span>
          </router-link>

          <router-link to="/nosotros" class="mobile-link" @click="closeMobileMenu" active-class="active">
            <va-icon name="info" />
            <span>Sobre Nosotros</span>
          </router-link>

          <router-link to="/publicar" class="mobile-link" @click="closeMobileMenu" active-class="active">
            <va-icon name="add_circle" />
            <span>Publicar</span>
          </router-link>
        </div>

        <!-- Mobile Auth Section -->
        <div class="mobile-auth-section">
          <!-- If Logged In -->
          <div v-if="authStore.isAuthenticated" class="mobile-user-info">
            <div class="user-avatar-mobile">{{ authStore.userInitials }}</div>
            <div class="user-details">
              <div class="mobile-user-name">{{ authStore.user?.name }}</div>
              <div class="mobile-user-email">{{ authStore.user?.email }}</div>
            </div>
          </div>

          <button v-if="authStore.isAuthenticated" @click="doLogout" class="mobile-logout-btn">
            <va-icon name="logout" />
            <span>Cerrar Sesión</span>
          </button>

          <!-- If NOT Logged In -->
          <router-link v-else to="/login" class="mobile-login-link" @click="closeMobileMenu">
            <va-icon name="login" />
            <span>Ingresar</span>
          </router-link>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'

const router = useRouter()
const authStore = useAuthStore()
const { init: notify } = useToast()
const mobileMenuOpen = ref(false)

// Publish Button Handler
const handlePublish = () => {
  if (!authStore.isAuthenticated) {
    notify({ message: 'Debes iniciar sesión para publicar', color: 'info' })
    router.push('/login')
    return
  }
  router.push('/publicar')
  closeMobileMenu()
}

// LOGOUT - Simple and Direct
const doLogout = () => {
  console.log('🚪 LOGOUT - Clearing everything...')

  authStore.logout()
  console.log('✅ Logout completed')

  notify({ message: 'Sesión cerrada', color: 'info', duration: 2000 })
  closeMobileMenu()

  setTimeout(() => {
    window.location.href = '/'
  }, 300)
}

// Mobile Menu Helpers
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
  document.body.style.overflow = mobileMenuOpen.value ? 'hidden' : ''
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
  document.body.style.overflow = ''
}
</script>

<style scoped>
/* NAVBAR */
.navbar {
  background-color: var(--color-purple);
  color: white;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.navbar-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

/* LOGO */
.logo {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  text-decoration: none;
  color: white;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.logo:hover {
  transform: scale(1.02);
}

.logo-image {
  height: 36px;
  width: auto;
}

.logo-text-wrapper {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.logo-text {
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
}

.logo-country {
  color: var(--color-yellow-primary);
  font-size: 0.75rem;
  font-weight: 600;
}

/* NAVIGATION LINKS */
.nav-links {
  display: flex;
  gap: 1rem;
  flex: 1;
  justify-content: center;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
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
  font-weight: 600;
}

/* ACTIONS SECTION */
.nav-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-shrink: 0;
}

.publish-btn {
  --va-background-color: var(--color-yellow-primary) !important;
  --va-text-color: var(--color-purple-darkest) !important;
  color: var(--color-purple-darkest) !important;
  font-weight: 700 !important;
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3) !important;
  transition: all 0.3s ease !important;
}

.publish-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(253, 197, 0, 0.4) !important;
}

.btn-text-short {
  display: none;
}

/* LOGIN BUTTON */
.login-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: rgba(255, 255, 255, 0.12);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  cursor: pointer;
  white-space: nowrap;
}

.login-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

/* USER AVATAR BUTTON */
.user-avatar-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 44px;
  height: 44px;
  padding: 0;
  background: rgba(255, 255, 255, 0.12);
  border: 2px solid rgba(255, 255, 255, 0.25);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  position: relative;
  flex-shrink: 0;
}

.user-avatar-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
  transform: scale(1.1);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}

.logout-icon {
  position: absolute;
  top: -8px;
  right: -8px;
  background: var(--color-yellow-primary);
  border-radius: 50%;
  padding: 2px;
  color: var(--color-purple-darkest) !important;
}

/* MOBILE MENU BUTTON */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  gap: 6px;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
}

.hamburger-line {
  width: 100%;
  height: 3px;
  background: white;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.mobile-menu-btn.active .hamburger-line:nth-child(1) {
  transform: translateY(9px) rotate(45deg);
}

.mobile-menu-btn.active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn.active .hamburger-line:nth-child(3) {
  transform: translateY(-9px) rotate(-45deg);
}

/* MOBILE OVERLAY */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

/* MOBILE MENU */
.mobile-menu {
  position: fixed;
  top: 0;
  right: 0;
  width: 85%;
  max-width: 320px;
  height: 100vh;
  background: var(--color-purple-dark);
  z-index: 1001;
  overflow-y: auto;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.3);
}

.mobile-menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  font-weight: 700;
  font-size: 1.25rem;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

.mobile-nav-section {
  padding: 0;
  margin: 0;
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  color: white;
  text-decoration: none;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  font-weight: 500;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.mobile-link:hover {
  background: rgba(255, 255, 255, 0.1);
  padding-left: 2rem;
}

/* MOBILE AUTH SECTION */
.mobile-auth-section {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 1rem;
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-bottom: 1rem;
}

.user-avatar-mobile {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.mobile-user-name {
  font-weight: 600;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 0.25rem;
}

.mobile-user-email {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mobile-logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1rem;
  background: rgba(227, 75, 74, 0.2);
  color: #ffb3b3;
  border: 1px solid rgba(227, 75, 74, 0.3);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.mobile-logout-btn:hover {
  background: rgba(227, 75, 74, 0.3);
  border-color: rgba(227, 75, 74, 0.5);
}

.mobile-login-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1rem;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  border: none;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.mobile-login-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3);
}

/* TRANSITIONS */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-in-enter-active,
.slide-in-leave-active {
  transition: transform 0.3s ease;
}

.slide-in-enter-from,
.slide-in-leave-to {
  transform: translateX(100%);
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .publish-btn {
    padding: 0.5rem 0.75rem !important;
  }

  .btn-text {
    display: none;
  }

  .btn-text-short {
    display: inline;
  }
}

@media (max-width: 768px) {
  .navbar-content {
    padding: 0.75rem 1rem;
    gap: 1rem;
  }

  .desktop-only {
    display: none !important;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .publish-btn {
    padding: 0.5rem 0.75rem !important;
  }
}
</style>
