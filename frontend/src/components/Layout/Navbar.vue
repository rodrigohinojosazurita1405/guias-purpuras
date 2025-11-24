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

      <!-- Desktop Navigation - Simplificado -->
      <div class="nav-links desktop-only">
        <router-link to="/" class="nav-link" exact-active-class="active">
          <span>Inicio</span>
        </router-link>

        <router-link to="/guias/trabajos" class="nav-link" active-class="active">
          <span>Empleos</span>
        </router-link>

        <router-link to="/about" class="nav-link" active-class="active">
          <span>Nosotros</span>
        </router-link>
      </div>

      <!-- Actions -->
      <div class="nav-actions">
        <!-- NOT Authenticated: Show Register & Login Buttons -->
        <router-link v-if="!authStore.isAuthenticated" to="/login" class="login-btn desktop-only">
          <span>Registrarse</span>
        </router-link>

        <router-link v-if="!authStore.isAuthenticated" to="/login" class="login-btn desktop-only login-link">
          <span>Ingresar</span>
        </router-link>

        <!-- Authenticated: Show Avatar Dropdown Menu -->
        <div v-else class="user-dropdown desktop-only">
          <button @click="toggleDropdown" class="user-avatar-btn" :class="{ active: dropdownOpen }">
            <div class="user-avatar">{{ authStore.userInitials }}</div>
            <va-icon name="expand_more" size="small" class="dropdown-arrow" :class="{ rotated: dropdownOpen }" />
          </button>

          <!-- Dropdown Menu -->
          <transition name="dropdown">
            <div v-if="dropdownOpen" class="dropdown-menu">
              <!-- User Info -->
              <div class="dropdown-header">
                <div class="dropdown-user-avatar">{{ authStore.userInitials }}</div>
                <div class="dropdown-user-info">
                  <div class="dropdown-user-name">{{ authStore.user?.name }}</div>
                  <div class="dropdown-user-email">{{ authStore.user?.email }}</div>
                </div>
              </div>

              <div class="dropdown-divider"></div>

              <!-- Menu Items -->
              <router-link to="/dashboard" class="dropdown-item" @click="closeDropdown">
                <va-icon name="dashboard" size="small" />
                <span>Mi Dashboard</span>
              </router-link>

              <router-link to="/dashboard/jobs-manager" class="dropdown-item" @click="closeDropdown">
                <va-icon name="list_alt" size="small" />
                <span>Mis Anuncios</span>
              </router-link>

              <div class="dropdown-divider"></div>

              <!-- Logout -->
              <button @click="handleDropdownLogout" class="dropdown-item logout-item">
                <va-icon name="logout" size="small" />
                <span>Cerrar Sesión</span>
              </button>
            </div>
          </transition>

          <!-- Backdrop to close dropdown -->
          <transition name="fade">
            <div v-if="dropdownOpen" class="dropdown-backdrop" @click="closeDropdown"></div>
          </transition>
        </div>

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

        <!-- Mobile Navigation - Simplificado -->
        <div class="mobile-nav-section">
          <router-link to="/" class="mobile-link" @click="closeMobileMenu" exact-active-class="active">
            <span>Inicio</span>
          </router-link>

          <router-link to="/guias/trabajos" class="mobile-link" @click="closeMobileMenu" active-class="active">
            <span>Empleos</span>
          </router-link>
        </div>

        <!-- Mobile Auth Section -->
        <div class="mobile-auth-section">
          <!-- If Logged In -->
          <div v-if="authStore.isAuthenticated">
            <div class="mobile-user-info">
              <div class="user-avatar-mobile">{{ authStore.userInitials }}</div>
              <div class="user-details">
                <div class="mobile-user-name">{{ authStore.user?.name }}</div>
                <div class="mobile-user-email">{{ authStore.user?.email }}</div>
              </div>
            </div>

            <!-- User Menu Items for Mobile -->
            <router-link to="/dashboard" class="mobile-link" @click="closeMobileMenu">
              <va-icon name="dashboard" />
              <span>Mi Dashboard</span>
            </router-link>

            <router-link to="/dashboard/jobs-manager" class="mobile-link" @click="closeMobileMenu">
              <va-icon name="list_alt" />
              <span>Mis Anuncios</span>
            </router-link>

            <button @click="doLogout" class="mobile-logout-btn">
              <va-icon name="logout" />
              <span>Cerrar Sesión</span>
            </button>
          </div>

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
const dropdownOpen = ref(false)

// Dropdown Menu Handlers
const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

// Logout from dropdown
const handleDropdownLogout = () => {
  closeDropdown()
  doLogout()
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
  background: var(--color-purple-dark);
  color: white;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: none;
  border: none;
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

.btn-text-short {
  display: none;
}

/* LOGIN BUTTON - Registrarse */
.login-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  border: none;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 700;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  cursor: pointer;
  white-space: nowrap;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(253, 197, 0, 0.6), 0 4px 12px rgba(253, 197, 0, 0.3);
}

/* LOGIN BUTTON - Ingresar (variante outline) */
.login-btn.login-link {
  background: transparent;
  color: white;
  border: 2px solid white;
  padding: 0.5rem 1.25rem;
}

.login-btn.login-link:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.8);
}

/* USER DROPDOWN */
.user-dropdown {
  position: relative;
}

/* USER AVATAR BUTTON */
.user-avatar-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.12);
  border: 2px solid rgba(255, 255, 255, 0.25);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  flex-shrink: 0;
}

.user-avatar-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
}

.user-avatar-btn.active {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
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

.dropdown-arrow {
  transition: transform 0.3s ease;
  color: white !important;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

/* DROPDOWN MENU */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  min-width: 280px;
  z-index: 1000;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #eff2f7 100%);
  border-bottom: 1px solid #e8ebf0;
}

.dropdown-user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.95rem;
  flex-shrink: 0;
}

.dropdown-user-info {
  flex: 1;
  min-width: 0;
}

.dropdown-user-name {
  font-weight: 600;
  color: #1a1a2e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 0.25rem;
}

.dropdown-user-email {
  font-size: 0.8rem;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-divider {
  height: 1px;
  background: #e8ebf0;
  margin: 0.5rem 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.875rem 1rem;
  background: none;
  border: none;
  color: #333;
  text-decoration: none;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 0.95rem;
}

.dropdown-item:hover {
  background: #f5f7fa;
  padding-left: 1.25rem;
}

.dropdown-item :deep(svg) {
  color: var(--color-purple) !important;
  flex-shrink: 0;
}

.dropdown-item.logout-item {
  color: #e34b4a;
  border-top: 1px solid #e8ebf0;
}

.dropdown-item.logout-item:hover {
  background: rgba(227, 75, 74, 0.08);
}

.dropdown-item.logout-item :deep(svg) {
  color: #e34b4a !important;
}

/* DROPDOWN BACKDROP */
.dropdown-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
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

/* DROPDOWN TRANSITIONS */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px) scaleY(0.95);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scaleY(0.95);
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
