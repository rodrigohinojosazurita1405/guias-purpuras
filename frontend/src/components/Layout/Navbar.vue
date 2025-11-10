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
          to="/guias/negocios" 
          class="nav-link"
          active-class="active"
        >
          <va-icon name="build" size="small" />
          Negocios
        </router-link>
      </div>

      <!-- Actions: Publicar + Auth -->
      <div class="nav-actions">
        <!-- Botón Publicar -->
        <va-button
          @click="goToPublish"
          color="yellow-primary"
          class="publish-btn"
        >
          <va-icon name="add_circle" />
          <span class="btn-text">Publica tu anuncio</span>
        </va-button>

        <!-- Auth Buttons (cuando NO está logueado) -->
        <div v-if="!authStore.isAuthenticated" class="auth-buttons">
          <va-button
            @click="showAuthModal = true"
            color="yellow-primary"
            class="login-btn desktop-only"
          >
            <va-icon name="login" />
            <span>Ingresar</span>
          </va-button>
        </div>

        <!-- User Menu (cuando SÍ está logueado) -->
        <VaDropdown v-else class="user-menu" placement="bottom-end">
          <template #anchor>
            <button class="user-avatar-btn">
              <div class="user-avatar">
                {{ authStore.userInitials }}
              </div>
              <span class="user-name-desktop desktop-only">{{ authStore.user.name }}</span>
              <va-icon name="expand_more" size="small" />
            </button>
          </template>

          <VaDropdownContent class="user-dropdown">
            <div class="user-info">
              <div class="user-name">{{ authStore.user.name }}</div>
              <div class="user-email">{{ authStore.user.email }}</div>
            </div>
            
            <VaDivider />
            
            <button class="dropdown-item" @click="goToProfile">
              <va-icon name="person" />
              Mi Perfil
            </button>
            
            <button class="dropdown-item" @click="goToMyListings">
              <va-icon name="list" />
              Mis Anuncios
            </button>
            
            <VaDivider />
            
            <button class="dropdown-item logout" @click="handleLogout">
              <va-icon name="logout" />
              Cerrar Sesión
            </button>
          </VaDropdownContent>
        </VaDropdown>

        <!-- Mobile Menu Toggle -->
        <va-button
          @click="toggleMobileMenu"
          icon="menu"
          color="white"
          text-color="purple"
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
          to="/guias/negocios" 
          class="mobile-link"
          @click="closeMobileMenu"
          active-class="active"
        >
          <va-icon name="build" />
          Negocios
        </router-link>

        <!-- Auth en mobile (NO logueado) -->
        <div v-if="!authStore.isAuthenticated" class="mobile-auth">
          <va-button
            @click="openAuthModalAndCloseMenu"
            color="yellow-primary"
            block
          >
            <va-icon name="login" />
            Ingresar
          </va-button>
        </div>
        
        <!-- User section en mobile (SÍ logueado) -->
        <div v-else class="mobile-user-section">
          <div class="mobile-user-info">
            <div class="user-avatar-mobile">
              {{ authStore.userInitials }}
            </div>
            <div>
              <div class="mobile-user-name">{{ authStore.user.name }}</div>
              <div class="mobile-user-email">{{ authStore.user.email }}</div>
            </div>
          </div>
          
          <button class="mobile-link" @click="goToProfileAndClose">
            <va-icon name="person" />
            Mi Perfil
          </button>
          
          <button class="mobile-link" @click="goToMyListingsAndClose">
            <va-icon name="list" />
            Mis Anuncios
          </button>
          
          <button class="mobile-link logout" @click="handleLogoutAndClose">
            <va-icon name="logout" />
            Cerrar Sesión
          </button>
        </div>
      </div>
    </transition>

    <!-- Auth Modal -->
    <AuthModal 
      v-model="showAuthModal" 
      @success="handleAuthSuccess" 
    />
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'
import AuthModal from '@/components/Auth/AuthModal.vue'

// ========== COMPOSABLES ==========
const router = useRouter()
const authStore = useAuthStore()
const route = useRoute()
const { init: notify } = useToast()

// ========== STATE ==========
const mobileMenuOpen = ref(false)
const showAuthModal = ref(false)

// ========== METHODS ==========
const goToPublish = () => {
  // Si no está autenticado, mostrar modal
  if (!authStore.isAuthenticated) {
    showAuthModal.value = true
    notify({
      message: 'Debes iniciar sesión para publicar un anuncio',
      color: 'info'
    })
    return
  }
  
  // SIEMPRE ir al formulario genérico /publicar
  router.push('/publicar')
  closeMobileMenu()
}

const goToProfile = () => {
  notify({
    message: '🚧 Ruta de perfil próximamente',
    color: 'info'
  })
  // TODO: router.push('/perfil')
}

const goToMyListings = () => {
  notify({
    message: '🚧 Ruta de mis anuncios próximamente',
    color: 'info'
  })
  // TODO: router.push('/mis-anuncios')
}

const goToProfileAndClose = () => {
  goToProfile()
  closeMobileMenu()
}

const goToMyListingsAndClose = () => {
  goToMyListings()
  closeMobileMenu()
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

const handleAuthSuccess = () => {
  // Después de login/register exitoso
  notify({
    message: '¡Bienvenido a Guías Púrpuras! 🎉',
    color: 'success'
  })
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const openAuthModalAndCloseMenu = () => {
  showAuthModal.value = true
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

/* ========== LOGO ========== */
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
  height: 32px;
  width: auto;
}

.logo-text {
  color: white;
}

.logo-country {
  color: var(--color-yellow-primary);
  font-size: 0.9rem;
}

/* ========== NAVEGACIÓN DESKTOP ========== */
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

/* ========== ACTIONS ========== */
.nav-actions {
  display: flex;
  gap: 0.75rem;
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

/* ========== AUTH BUTTONS ========== */
.auth-buttons {
  display: flex;
  gap: 0.5rem;
}

.login-btn {
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(253, 197, 0, 0.2);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.4);
}

/* ========== USER MENU ========== */
.user-avatar-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.user-avatar-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.user-name-desktop {
  font-weight: 600;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-dropdown {
  min-width: 240px;
  padding: 0.5rem;
}

.user-info {
  padding: 0.75rem 1rem;
}

.user-name {
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin-bottom: 0.25rem;
}

.user-email {
  font-size: 0.85rem;
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
  transition: background 0.2s ease;
  font-size: 0.95rem;
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

/* ========== MOBILE MENU ========== */
.mobile-menu-btn {
  display: none;
}

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
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 1rem;
}

.mobile-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.mobile-link.active {
  background-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

.mobile-link.logout {
  color: #FFB3B3;
}

.mobile-auth {
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 0.5rem;
}

.mobile-user-section {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 0.5rem;
  padding-top: 1rem;
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 0.5rem;
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

.mobile-user-name {
  font-weight: 600;
  color: white;
  margin-bottom: 0.25rem;
}

.mobile-user-email {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
}

/* ========== TRANSICIONES ========== */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .nav-links {
    gap: 0.25rem;
  }
  
  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
  
  .user-name-desktop {
    display: none;
  }
}

@media (max-width: 768px) {
  .desktop-only {
    display: none !important;
  }
  
  .mobile-menu-btn {
    display: flex;
  }
  
  .publish-btn .btn-text {
    display: none;
  }
}
</style>