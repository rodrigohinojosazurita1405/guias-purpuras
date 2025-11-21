<!-- frontend/src/components/Layout/Navbar.vue -->
<template>
  <nav class="navbar">
    <div class="navbar-content">
      <!-- Logo -->
      <router-link to="/" class="logo" @click="closeMobileMenu">
        <img src="/src/assets/guiaspurpuras.ico" alt="Logo Guías Púrpuras" class="logo-image" />
        <div class="logo-text-wrapper">
          <span class="logo-text">Guías Púrpuras</span>
          <span class="logo-country">Bolivia</span>
        </div>
      </router-link>

      <!-- Desktop Navigation -->
      <div class="nav-links desktop-only">
        <router-link
          to="/"
          class="nav-link"
          exact-active-class="active"
        >
          <va-icon name="home" size="small" />
          <span>Inicio</span>
        </router-link>

        <!-- Guías Dropdown -->
        <VaDropdown class="guias-dropdown" placement="bottom-start">
          <template #anchor>
            <button class="nav-link dropdown-anchor">
              <va-icon name="category" size="small" />
              <span>Guías</span>
              <va-icon name="expand_more" size="small" />
            </button>
          </template>

          <VaDropdownContent class="guias-dropdown-content">
            <router-link to="/guias/trabajos" class="dropdown-item" @click="$event.stopPropagation()">
              <va-icon name="business_center" size="small" />
              <span>Empleos</span>
            </router-link>

            <button class="dropdown-item disabled" disabled>
              <va-icon name="person" size="small" />
              <span>Profesionales</span>
              <span class="coming-soon">Próximamente</span>
            </button>

            <button class="dropdown-item disabled" disabled>
              <va-icon name="storefront" size="small" />
              <span>Negocios</span>
              <span class="coming-soon">Próximamente</span>
            </button>

            <button class="dropdown-item disabled" disabled>
              <va-icon name="restaurant" size="small" />
              <span>Restaurantes</span>
              <span class="coming-soon">Próximamente</span>
            </button>
          </VaDropdownContent>
        </VaDropdown>

        <!-- Sobre Nosotros Link -->
        <router-link
          to="/nosotros"
          class="nav-link"
          active-class="active"
        >
          <va-icon name="info" size="small" />
          <span>Sobre Nosotros</span>
        </router-link>
      </div>

      <!-- Actions -->
      <div class="nav-actions">
        <!-- Botón Publicar Empleo (destacado) -->
        <va-button
          @click="goToPublish"
          class="publish-btn"
        >
          <va-icon name="add_circle" size="small" />
          <span class="btn-text">Publicar empleo</span>
          <span class="btn-text-short">Publicar</span>
        </va-button>

        <!-- Auth: Login (NO logueado) -->
        <router-link
          v-if="!authStore.isAuthenticated"
          to="/login"
          class="login-btn desktop-only"
        >
          <va-icon name="login" size="small" />
          <span>Ingresar</span>
        </router-link>

        <!-- User Menu (SÍ logueado) -->
        <VaDropdown v-else class="user-menu" placement="bottom-end">
          <template #anchor>
            <button class="user-avatar-btn">
              <div class="user-avatar">
                {{ authStore.userInitials }}
              </div>
              <span class="user-name desktop-only">{{ authStore.user.name }}</span>
              <va-icon name="expand_more" size="small" />
            </button>
          </template>

          <VaDropdownContent class="user-dropdown">
            <div class="user-info">
              <div class="user-name-full">{{ authStore.user.name }}</div>
              <div class="user-email">{{ authStore.user.email }}</div>
            </div>

            <VaDivider style="margin: 0.5rem 0;" />

            <button class="dropdown-item" @click="goToDashboard">
              <va-icon name="dashboard" size="small" />
              <span>Mi Dashboard</span>
            </button>

            <button class="dropdown-item" @click="goToProfile">
              <va-icon name="person" size="small" />
              <span>Mi Perfil</span>
            </button>
            
            <button class="dropdown-item" @click="goToMyListings">
              <va-icon name="list" size="small" />
              <span>Mis Anuncios</span>
            </button>
            
            <VaDivider style="margin: 0.5rem 0;" />
            
            <button class="dropdown-item logout" @click="handleLogout">
              <va-icon name="logout" size="small" />
              <span>Cerrar Sesión</span>
            </button>
          </VaDropdownContent>
        </VaDropdown>

        <!-- Mobile Menu Toggle -->
        <button
          @click="toggleMobileMenu"
          class="mobile-menu-btn"
          :class="{ active: mobileMenuOpen }"
          aria-label="Menú"
        >
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
    </div>

    <!-- Mobile Menu Overlay -->
    <transition name="fade">
      <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
    </transition>

    <!-- Mobile Menu Drawer -->
    <transition name="slide-in">
      <div v-if="mobileMenuOpen" class="mobile-menu">
        <div class="mobile-menu-header">
          <span class="mobile-menu-title">Menú</span>
          <button @click="closeMobileMenu" class="close-btn">
            <va-icon name="close" />
          </button>
        </div>

        <div class="mobile-menu-content">
          <!-- User section (si está logueado) -->
          <div v-if="authStore.isAuthenticated" class="mobile-user-section">
            <div class="mobile-user-info">
              <div class="user-avatar-mobile">
                {{ authStore.userInitials }}
              </div>
              <div class="user-details">
                <div class="mobile-user-name">{{ authStore.user.name }}</div>
                <div class="mobile-user-email">{{ authStore.user.email }}</div>
              </div>
            </div>
          </div>

          <!-- Navigation Links -->
          <div class="mobile-nav-section">
            <router-link
              to="/"
              class="mobile-link"
              @click="closeMobileMenu"
              exact-active-class="active"
            >
              <va-icon name="home" />
              <span>Inicio</span>
            </router-link>

            <!-- Guías Submenu (Expandible) -->
            <button
              class="mobile-link guias-toggle"
              @click="toggleGuiasMenu"
            >
              <va-icon name="category" />
              <span>Guías</span>
              <va-icon
                name="expand_more"
                size="small"
                :class="{ rotate: guiasOpen }"
                class="expand-icon"
              />
            </button>

            <transition name="expand">
              <div v-if="guiasOpen" class="mobile-submenu">
                <router-link
                  to="/guias/trabajos"
                  class="mobile-sublink"
                  @click="closeMobileMenuAndGuias"
                  active-class="active"
                >
                  <va-icon name="business_center" />
                  <span>Empleos</span>
                </router-link>

                <button class="mobile-sublink disabled" disabled>
                  <va-icon name="person" />
                  <span>Profesionales</span>
                  <span class="coming-soon-mobile">Próximamente</span>
                </button>

                <button class="mobile-sublink disabled" disabled>
                  <va-icon name="storefront" />
                  <span>Negocios</span>
                  <span class="coming-soon-mobile">Próximamente</span>
                </button>

                <button class="mobile-sublink disabled" disabled>
                  <va-icon name="restaurant" />
                  <span>Restaurantes</span>
                  <span class="coming-soon-mobile">Próximamente</span>
                </button>
              </div>
            </transition>

            <!-- Sobre Nosotros Link -->
            <router-link
              to="/nosotros"
              class="mobile-link"
              @click="closeMobileMenu"
              active-class="active"
            >
              <va-icon name="info" />
              <span>Sobre Nosotros</span>
            </router-link>

            <router-link
              to="/publicar"
              class="mobile-link"
              @click="closeMobileMenu"
              active-class="active"
            >
              <va-icon name="add_circle" />
              <span>Publicar empleo</span>
            </router-link>
          </div>

          <!-- User actions (si está logueado) -->
          <div v-if="authStore.isAuthenticated" class="mobile-nav-section">
            <button class="mobile-link" @click="goToDashboard">
              <va-icon name="dashboard" />
              <span>Mi Dashboard</span>
            </button>

            <button class="mobile-link" @click="goToProfileAndClose">
              <va-icon name="person" />
              <span>Mi Perfil</span>
            </button>
            
            <button class="mobile-link" @click="goToMyListingsAndClose">
              <va-icon name="list" />
              <span>Mis Anuncios</span>
            </button>
            
            <button class="mobile-link logout" @click="handleLogoutAndClose">
              <va-icon name="logout" />
              <span>Cerrar Sesión</span>
            </button>
          </div>

          <!-- Auth button (si NO está logueado) -->
          <div v-else class="mobile-auth">
            <router-link
              to="/login"
              class="mobile-login-link"
              @click="closeMobileMenu"
            >
              <va-icon name="login" />
              <span>Ingresar</span>
            </router-link>
          </div>
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

// State
const mobileMenuOpen = ref(false)
const guiasOpen = ref(false)

// Methods
const goToPublish = () => {
  if (!authStore.isAuthenticated) {
    notify({
      message: 'Debes iniciar sesión para publicar un anuncio',
      color: 'info'
    })
    router.push('/login')
    return
  }

  router.push('/publicar')
  closeMobileMenu()
}

const goToDashboard = () => {
  router.push({ path: '/dashboard', query: { tab: 'home' } })
  closeMobileMenu()
}

const goToProfile = () => {
  router.push({ path: '/dashboard', query: { tab: 'profile' } })
  closeMobileMenu()
}

const goToMyListings = () => {
  router.push({ path: '/dashboard', query: { tab: 'jobs' } })
  closeMobileMenu()
}

const goToProfileAndClose = () => {
  goToProfile()
}

const goToMyListingsAndClose = () => {
  goToMyListings()
}

const handleLogout = () => {
  authStore.logout()
  notify({
    message: '✅ Sesión cerrada correctamente',
    color: 'success'
  })
  router.push('/')
}

const handleLogoutAndClose = () => {
  handleLogout()
  closeMobileMenu()
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
  
  // Prevenir scroll del body cuando el menú está abierto
  if (mobileMenuOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
  guiasOpen.value = false
  document.body.style.overflow = ''
}

const toggleGuiasMenu = () => {
  guiasOpen.value = !guiasOpen.value
}

const closeMobileMenuAndGuias = () => {
  closeMobileMenu()
}
</script>

<style scoped>
/* ========== NAVBAR PRINCIPAL ========== */
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
  padding: 0.875rem 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

/* ========== LOGO ========== */
.logo {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  text-decoration: none;
  color: white;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.02);
}

.logo-image {
  height: 36px;
  width: auto;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
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
  letter-spacing: 0.5px;
}

/* ========== NAVEGACIÓN DESKTOP ========== */
.nav-links {
  display: flex;
  gap: 0.5rem;
  flex: 1;
  justify-content: center;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  color: white;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: var(--color-yellow-primary);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.nav-link:hover::after {
  width: 80%;
}

.nav-link.active {
  background-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  font-weight: 600;
}

.nav-link.active::after {
  display: none;
}

/* ========== ACTIONS ========== */
.nav-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.publish-btn {
  --va-background-color: var(--color-yellow-primary) !important;
  color: var(--color-purple-darkest) !important;
  font-weight: 700 !important;
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.35);
  transition: all 0.3s ease !important;
  border: none !important;
}

.publish-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(253, 197, 0, 0.5);
}

.btn-text-short {
  display: none;
}

.login-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  font-weight: 600;
  transition: all 0.3s ease;
  border-radius: 8px;
  text-decoration: none;
}

.login-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.mobile-login-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  color: white;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 500;
  transition: all 0.3s ease;
  background: var(--color-yellow-primary);
  width: 100%;
  text-align: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1rem;
  border: none;
}

/* ========== USER MENU ========== */
.user-avatar-btn {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.5rem 0.875rem;
  background: rgba(255, 255, 255, 0.12);
  border: 2px solid rgba(255, 255, 255, 0.25);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.user-avatar-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
  transform: scale(1.05);
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
  flex-shrink: 0;
}

.user-name {
  font-weight: 600;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.9rem;
}

.user-dropdown {
  min-width: 240px;
  padding: 0.5rem;
}

.user-info {
  padding: 0.875rem 1rem;
}

.user-name-full {
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin-bottom: 0.25rem;
}

.user-email {
  font-size: 0.8rem;
  color: #666;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  border-radius: 8px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  color: #333;
}

.dropdown-item:hover {
  background: #F5F5F5;
}

.dropdown-item.logout {
  color: #E34B4A;
}

.dropdown-item.logout:hover {
  background: rgba(227, 75, 74, 0.1);
}

/* ========== MOBILE MENU BUTTON ========== */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 10;
}

.hamburger-line {
  width: 100%;
  height: 3px;
  background: white;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.mobile-menu-btn.active .hamburger-line:nth-child(1) {
  transform: translateY(10px) rotate(45deg);
}

.mobile-menu-btn.active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn.active .hamburger-line:nth-child(3) {
  transform: translateY(-10px) rotate(-45deg);
}

/* ========== MOBILE OVERLAY ========== */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  backdrop-filter: blur(2px);
}

/* ========== MOBILE MENU DRAWER ========== */
.mobile-menu {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 85%;
  max-width: 320px;
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
}

.mobile-menu-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
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

.mobile-menu-content {
  padding: 1rem;
}

.mobile-user-section {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
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
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mobile-user-email {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mobile-nav-section {
  margin-bottom: 1rem;
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  color: white;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 500;
  transition: all 0.3s ease;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.mobile-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.mobile-link.active {
  background-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  font-weight: 600;
}

.mobile-link.logout {
  color: #FFB3B3;
}

.mobile-link.logout:hover {
  background-color: rgba(255, 75, 75, 0.15);
}

.mobile-auth {
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* ========== TRANSICIONES ========== */
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

/* ========== RESPONSIVE ========== */
@media (max-width: 1200px) {
  .navbar-content {
    padding: 0.875rem 2rem;
  }

  .nav-links {
    gap: 0.25rem;
  }

  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 1024px) {
  .btn-text {
    display: none;
  }

  .btn-text-short {
    display: inline;
  }

  .user-name {
    display: none;
  }
}

/* ========== GUÍAS DROPDOWN (DESKTOP) ========== */
.guias-dropdown {
  position: relative;
}

.dropdown-anchor {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: none;
  border: none;
  padding: 0.625rem 1rem;
  color: white;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.95rem;
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  position: relative;
}

.dropdown-anchor::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: var(--color-yellow-primary);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.dropdown-anchor:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.dropdown-anchor:hover::after {
  width: 80%;
}

.guias-dropdown-content {
  min-width: 220px;
  padding: 0.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  width: 100%;
  border: none;
  background: none;
  border-radius: 8px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  color: #333;
  text-decoration: none;
  position: relative;
}

.dropdown-item:not(.disabled):hover {
  background: #F5F5F5;
}

.dropdown-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.coming-soon {
  font-size: 0.75rem;
  color: #999;
  margin-left: auto;
}

/* ========== MOBILE SUBMENU (GUÍAS) ========== */
.guias-toggle {
  justify-content: space-between;
}

.expand-icon {
  transition: transform 0.3s ease;
  margin-left: auto;
}

.expand-icon.rotate {
  transform: rotate(180deg);
}

.mobile-submenu {
  padding-left: 1rem;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  border-left: 2px solid rgba(255, 255, 255, 0.2);
}

.mobile-sublink {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem 1.25rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  border-radius: 8px;
  font-weight: 400;
  transition: all 0.3s ease;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.mobile-sublink:hover:not(.disabled) {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(3px);
}

.mobile-sublink.active {
  background-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  font-weight: 600;
}

.mobile-sublink.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.coming-soon-mobile {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.5);
  margin-left: auto;
}

/* ========== EXPAND TRANSITION ========== */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 500px;
}

@media (max-width: 768px) {
  .navbar-content {
    padding: 0.75rem 1rem;
  }

  .desktop-only {
    display: none !important;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .btn-text-short {
    display: none;
  }

  .publish-btn {
    padding: 0.5rem 0.75rem;
  }
}
</style>