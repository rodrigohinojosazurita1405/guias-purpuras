<!-- frontend/src/components/Profile/Dashboard.vue -->
<template>
  <div class="dashboard-container">
    <!-- Mobile Menu Toggle Button -->
    <button class="mobile-menu-toggle" @click="sidebarOpen = !sidebarOpen">
      <va-icon :name="sidebarOpen ? 'close' : 'menu'" size="large" />
    </button>

    <!-- Sidebar Navigation -->
    <div class="dashboard-sidebar" :class="{ 'mobile-open': sidebarOpen }">
      <div class="sidebar-header">
        <h2>Panel de Control</h2>
      </div>

      <nav class="sidebar-menu">
        <!-- ========== SECCIÓN PRINCIPAL ========== -->
        <div class="menu-section-title">NAVEGACIÓN</div>

        <router-link
          to="/dashboard"
          class="menu-item"
          :class="{ active: activeSection === 'home' }"
        >
          <va-icon name="home" />
          <span>Tablero</span>
        </router-link>

        <!-- ========== SECCIÓN PERFIL ========== -->
        <div class="menu-section-title">MI PERFIL</div>

        <!-- Perfil Personal: Solo para postulantes -->
        <router-link
          v-if="authStore.user?.role === 'applicant'"
          to="/dashboard/profile"
          class="menu-item"
          :class="{ active: activeSection === 'profile' }"
        >
          <va-icon name="person" />
          <span>Perfil</span>
        </router-link>

        <!-- Mi CV: Solo para postulantes -->
        <router-link
          v-if="authStore.user?.role === 'applicant'"
          to="/dashboard/cv"
          class="menu-item"
          :class="{ active: activeSection === 'cv' }"
        >
          <va-icon name="description" />
          <span>Mi CV</span>
        </router-link>

        <!-- Mis Postulaciones: Solo para postulantes -->
        <router-link
          v-if="authStore.user?.role === 'applicant'"
          to="/dashboard/applications"
          class="menu-item"
          :class="{ active: activeSection === 'applications' }"
        >
          <va-icon name="assignment" />
          <span>Mis Postulaciones</span>
        </router-link>

        <!-- Perfil Empresa: Solo para empresas -->
        <router-link
          v-if="authStore.user?.role === 'company'"
          to="/dashboard/company"
          class="menu-item"
          :class="{ active: activeSection === 'company' }"
        >
          <va-icon name="business" />
          <span>Perfil De La Empresa</span>
        </router-link>

        <!-- ========== SECCIÓN PUBLICACIONES (SOLO EMPRESAS) ========== -->
        <template v-if="authStore.user?.role === 'company'">
          <div class="menu-section-title">PUBLICACIONES</div>

          <router-link
            to="/dashboard/jobs-manager"
            class="menu-item"
            :class="{ active: activeSection === 'jobs_manager' }"
          >
            <va-icon name="folder" />
            <span>Mis Anuncios</span>
          </router-link>

          <router-link
            to="/dashboard/candidates"
            class="menu-item"
            :class="{ active: activeSection === 'candidates' }"
          >
            <va-icon name="people" />
            <span>Solicitudes Recibidas</span>
            <span v-if="newApplications > 0" class="notification-badge applications-badge">{{ newApplications }}</span>
          </router-link>

          <router-link
            to="/dashboard/jobs"
            class="menu-item"
            :class="{ active: activeSection === 'jobs' }"
          >
            <va-icon name="work" />
            <span>Órdenes de Facturación</span>
            <span v-if="pendingOrders > 0" class="notification-badge orders-badge">{{ pendingOrders }}</span>
          </router-link>
        </template>

        <!-- ========== SECCIÓN INTERACCIONES ========== -->
        <div class="menu-section-title">INTERACCIONES</div>

        <!-- Favoritos: Solo para postulantes -->
        <router-link
          v-if="authStore.user?.role === 'applicant'"
          to="/dashboard/shortlisted"
          class="menu-item"
          :class="{ active: activeSection === 'shortlisted' }"
        >
          <va-icon name="bookmark" />
          <span>Favoritos</span>
        </router-link>

        <router-link
          to="/dashboard/notifications"
          class="menu-item"
          :class="{ active: activeSection === 'notifications' }"
        >
          <va-icon name="notifications" />
          <span>Notificaciones</span>
          <span v-if="unreadNotifications > 0" class="notification-badge">{{ unreadNotifications }}</span>
        </router-link>

        <!-- Bloqueados: Solo para empresas -->
        <router-link
          v-if="authStore.user?.role === 'company'"
          to="/dashboard/blocked"
          class="menu-item"
          :class="{ active: activeSection === 'blocked' }"
        >
          <va-icon name="block" />
          <span>Bloqueados</span>
        </router-link>

        <!-- ========== SECCIÓN ADMINISTRACIÓN ========== -->
        <div class="menu-section-title">ADMINISTRACIÓN</div>

        <router-link
          to="/dashboard/history"
          class="menu-item"
          :class="{ active: activeSection === 'history' }"
        >
          <va-icon name="history" />
          <span>Registro De Actividad</span>
        </router-link>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="dashboard-content">
      <!-- Dashboard Navbar -->
      <div class="dashboard-navbar">
        <div class="navbar-actions">
          <!-- Botón Publicar: Solo para empresas -->
          <router-link
            v-if="authStore.user?.role === 'company'"
            to="/publicar"
            class="navbar-btn navbar-btn-primary"
          >
            <va-icon name="add_circle" />
            <span>Publicar Nuevo Anuncio</span>
          </router-link>

          <!-- Botón diferente según el rol del usuario -->
          <router-link
            v-if="authStore.user?.role === 'applicant'"
            to="/guias/trabajos"
            class="navbar-btn navbar-btn-secondary"
          >
            <va-icon name="work" />
            <span>Buscar Trabajos</span>
          </router-link>

          <router-link
            v-else
            to="/"
            class="navbar-btn navbar-btn-secondary"
          >
            <va-icon name="home" />
            <span>Volver a Inicio</span>
          </router-link>
        </div>

        <div class="navbar-menu">
          <div class="dropdown-wrapper">
            <button class="navbar-btn navbar-btn-config" @click="showMenu = !showMenu">
              <va-icon name="person" />
              <span>Cuenta</span>
              <va-icon name="expand_more" class="dropdown-arrow" :class="{ open: showMenu }" />
            </button>
            <div v-if="showMenu" class="dropdown-content">
              <div
                class="dropdown-item"
                :class="{ 'dropdown-item-alerts': unreadNotifications > 0 }"
                @click="goToAlerts; showMenu = false"
              >
                <va-icon name="notifications" size="small" />
                <span>Alertas</span>
                <span v-if="unreadNotifications > 0" class="dropdown-badge">{{ unreadNotifications }}</span>
              </div>

              <div class="dropdown-item" @click="showChangePassword = true; showMenu = false">
                <va-icon name="lock" size="small" />
                <span>Cambiar Contraseña</span>
              </div>

              <div class="dropdown-item dropdown-item-logout" @click="handleLogout">
                <va-icon name="logout" size="small" />
                <span>Cerrar Sesión</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <slot></slot>
    </div>

    <!-- Change Password Modal -->
    <va-modal
      v-model="showChangePassword"
      title="Cambiar Contraseña"
      size="small"
      :before-ok="handleChangePassword"
      ok-text="Cambiar"
      cancel-text="Cancelar"
    >
      <div class="password-form">
        <div class="password-field">
          <va-input
            v-model="passwordForm.current"
            type="password"
            label="Contraseña Actual"
            placeholder="Ingresa tu contraseña actual"
          />
        </div>

        <div class="password-field">
          <va-input
            v-model="passwordForm.new"
            type="password"
            label="Nueva Contraseña"
            placeholder="Mínimo 6 caracteres"
          />
        </div>

        <div class="password-field">
          <va-input
            v-model="passwordForm.confirm"
            type="password"
            label="Confirmar Nueva Contraseña"
            placeholder="Repite la nueva contraseña"
          />
        </div>
      </div>
    </va-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vuestic-ui'
import { useAuthStore } from '@/stores/useAuthStore'

// ========== PROPS ==========
const props = defineProps({
  activeSection: {
    type: String,
    default: 'home'
  }
})

// ========== COMPOSABLES ==========
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { init: notify } = useToast()

// ========== DATA ==========
// REMOVED: Usar el prop en lugar de un ref local
// const activeSection = ref('home')
const showChangePassword = ref(false)
const showMenu = ref(false)
const sidebarOpen = ref(false)
const unreadNotifications = ref(0)
const pendingOrders = ref(0)
const newApplications = ref(0)
const passwordForm = ref({
  current: '',
  new: '',
  confirm: ''
})

// ========== LIFECYCLE ==========
onMounted(() => {
  // Cerrar dropdown al hacer clic fuera
  document.addEventListener('click', handleClickOutside)

  // Cargar contador de notificaciones no leídas
  fetchUnreadCount()

  // Cargar contadores solo para empresas
  if (authStore.user?.role === 'company') {
    fetchPendingOrdersCount()
    fetchNewApplicationsCount()
  }

  // Actualizar contadores cada 30 segundos
  const intervalId = setInterval(() => {
    fetchUnreadCount()
    if (authStore.user?.role === 'company') {
      fetchPendingOrdersCount()
      fetchNewApplicationsCount()
    }
  }, 30000)

  // Limpiar intervalo al desmontar
  onUnmounted(() => {
    clearInterval(intervalId)
  })
})

onUnmounted(() => {
  // Cleanup: remover event listener
  document.removeEventListener('click', handleClickOutside)
})

watch(() => route.path, () => {
  // REMOVED: updateActiveSection() - el activeSection se maneja en DashboardView.vue
  sidebarOpen.value = false // Cerrar sidebar al cambiar de ruta
  showChangePassword.value = false // Cerrar modal de cambiar contraseña al navegar
  showMenu.value = false // Cerrar menú dropdown
})

// ========== METHODS ==========
const handleClickOutside = (event) => {
  const dropdown = event.target.closest('.dropdown-wrapper')
  if (!dropdown && showMenu.value) {
    showMenu.value = false
  }
}

const goToAlerts = () => {
  // REMOVED: Ya no modificamos activeSection directamente (es prop del padre)
  // El router.push() hará que DashboardView actualice activeSection
  router.push('/dashboard/notifications')
}

const fetchUnreadCount = async () => {
  try {
    const response = await fetch('/api/notifications/unread-count/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      unreadNotifications.value = data.count || 0
    }
  } catch (error) {
    console.error('Error al obtener contador de notificaciones:', error)
  }
}

const fetchPendingOrdersCount = async () => {
  try {
    const response = await fetch('/api/user/orders/pending-count/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      pendingOrders.value = data.count || 0
    }
  } catch (error) {
    console.error('Error al obtener contador de órdenes pendientes:', error)
  }
}

const fetchNewApplicationsCount = async () => {
  try {
    const response = await fetch('/api/applications/unviewed-count/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      newApplications.value = data.count || 0
    }
  } catch (error) {
    console.error('Error al obtener contador de nuevas aplicaciones:', error)
  }
}

const handleChangePassword = async () => {
  try {
    // Validaciones en el frontend
    if (!passwordForm.value.current) {
      notify({
        message: 'Ingresa tu contraseña actual',
        color: 'warning',
        duration: 3000
      })
      return false
    }

    if (!passwordForm.value.new) {
      notify({
        message: 'Ingresa una nueva contraseña',
        color: 'warning',
        duration: 3000
      })
      return false
    }

    if (passwordForm.value.new.length < 6) {
      notify({
        message: 'La nueva contraseña debe tener al menos 6 caracteres',
        color: 'warning',
        duration: 3000
      })
      return false
    }

    if (passwordForm.value.new !== passwordForm.value.confirm) {
      notify({
        message: 'Las contraseñas no coinciden',
        color: 'warning',
        duration: 3000
      })
      return false
    }

    // Llamar al endpoint
    const response = await fetch('http://localhost:8000/api/auth/change-password', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        current_password: passwordForm.value.current,
        new_password: passwordForm.value.new,
        confirm_password: passwordForm.value.confirm
      })
    })

    const data = await response.json()

    if (response.ok && data.success) {
      // Limpiar el formulario
      passwordForm.value = {
        current: '',
        new: '',
        confirm: ''
      }

      // Cerrar el modal primero
      showChangePassword.value = false

      // Mostrar mensaje de éxito después de cerrar
      setTimeout(() => {
        notify({
          message: 'Contraseña cambiada exitosamente',
          color: 'success',
          duration: 3000
        })
      }, 300)

      return true
    } else {
      notify({
        message: data.message || 'Error al cambiar la contraseña',
        color: 'danger',
        duration: 4000
      })
      return false // Mantener el modal abierto
    }
  } catch (error) {
    console.error('Error changing password:', error)
    notify({
      message: 'Error al cambiar la contraseña. Intenta nuevamente.',
      color: 'danger',
      duration: 4000
    })
    return false
  }
}

const handleLogout = () => {
  console.log('🚪 LOGOUT desde Dashboard - Clearing everything...')

  authStore.logout()
  console.log('✅ Logout completado')

  notify({ message: 'Sesión cerrada', color: 'info', duration: 2000 })

  setTimeout(() => {
    window.location.href = '/'
  }, 300)
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: calc(100vh - 70px);
  background: #F3F4F6;
}

/* ========== SIDEBAR ========== */
.dashboard-sidebar {
  width: 280px;
  background: #F9FAFB;
  border-right: 1px solid #E5E7EB;
  overflow-y: auto;
  position: sticky;
  top: 70px;
  height: calc(100vh - 70px);
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid #E5E7EB;
  background: white;
  color: #1F2937;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1F2937;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sidebar-menu {
  padding: 1rem 0;
}

/* ========== SECTION TITLES ========== */
.menu-section-title {
  padding: 1rem 1.5rem 0.5rem 1.5rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  display: block;
}

.menu-section-title:first-child {
  margin-top: 0;
}

/* ========== MENU ITEMS ========== */
.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: #6B7280;
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all 0.2s ease;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  position: relative;
}

.menu-item:hover {
  background: #F3F4F6;
  color: #7c3aed;
  border-left-color: #7c3aed;
}

.menu-item.active {
  background: white;
  color: #7c3aed;
  border-left-color: #7c3aed;
  border-left-width: 3px;
  font-weight: 600;
}

/* ========== PRIMARY HIGHLIGHT BUTTON (PUBLICAR) ========== */
.menu-item.highlight-primary {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  margin: 0.75rem 0.5rem;
  font-weight: 700;
  border-radius: 8px;
  border-left: none;
  padding: 1.1rem 1.5rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
  position: relative;
  gap: 0.75rem;
  font-size: 0.95rem;
}

.menu-item.highlight-primary:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35);
}

.menu-item.highlight-primary.active {
  color: white;
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
}

.menu-item.menu-item-cta {
  align-items: center;
  justify-content: space-between;
}

.menu-item-badge {
  position: relative;
  color: currentColor;
}

/* ========== LOGOUT BUTTON ========== */
.menu-item.menu-item-logout {
  color: #DC2626;
  border-left: 3px solid transparent;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #E5E7EB;
}

.menu-item.menu-item-logout:hover {
  background: #FEE2E2;
  color: #991B1B;
  border-left-color: #DC2626;
}

/* ========== MAIN CONTENT ========== */
.dashboard-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

/* ========== DASHBOARD NAVBAR ========== */
.dashboard-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  margin-bottom: 2rem;
  border-radius: 8px;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.navbar-menu {
  display: flex;
  align-items: center;
}

.navbar-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  color: white;
  
}

.navbar-btn-primary {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.2);
}

.navbar-btn-primary:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
}

.navbar-btn-secondary {
  background: #F3F4F6;
  color: #1F2937;
  border: 1px solid #E5E7EB;
}

.navbar-btn-secondary:hover {
  background: #E5E7EB;
  border-color: #D1D5DB;
}

.navbar-btn-config {
  background: #F3F4F6;
  color: #1F2937;
  border: 1px solid #E5E7EB;
  gap: 0.5rem;
}

.navbar-btn-config:hover {
  background: #E5E7EB;
  border-color: #D1D5DB;
}

.navbar-btn-config span {
  font-weight: 600;
}

.dropdown-arrow {
  font-size: 1.25rem;
  transition: transform 0.2s ease;
  margin-left: 0.25rem;
}

.dropdown-arrow.open {
  transform: rotate(180deg);
}

.dropdown-wrapper {
  position: relative;
}

.dropdown-content {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 220px;
  z-index: 1000;
  margin-top: 0.5rem;
  overflow: hidden;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1rem;
  background: #F9FAFB;
  border-bottom: 1px solid #E5E7EB;
  color: #6B7280;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dropdown-header va-icon {
  color: #7c3aed;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #1F2937;
  font-size: 0.9rem;
  font-weight: 500;
  border-bottom: 1px solid #F3F4F6;
  position: relative;
  overflow: hidden;
}

.dropdown-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background: #F9FAFB;
  padding-left: 1.25rem;
}

.dropdown-item:hover::before {
  transform: translateX(0);
}

.dropdown-item:hover .va-icon {
  color: #9333EA;
  transform: scale(1.1);
}

.dropdown-item .va-icon {
  transition: all 0.3s ease;
}

.dropdown-item-logout {
  color: #DC2626;
}

.dropdown-item-logout::before {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
}

.dropdown-item-logout:hover {
  background: #FEF2F2;
  color: #B91C1C;
}

.dropdown-item-logout:hover .va-icon {
  color: #DC2626;
}

/* Badge para Alertas con notificaciones */
.dropdown-item-alerts {
  background: linear-gradient(90deg, #fef2f2 0%, #fee2e2 100%);
  border-left: 3px solid #ef4444;
  animation: pulse-alert 2s ease-in-out infinite;
}

.dropdown-item-alerts::before {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  transform: translateX(0);
}

.dropdown-item-alerts .va-icon {
  color: #ef4444;
}

.dropdown-item-alerts span:first-of-type {
  color: #dc2626;
  font-weight: 600;
}

.dropdown-item-alerts:hover {
  background: linear-gradient(90deg, #fee2e2 0%, #fecaca 100%);
}

.dropdown-item-alerts:hover .va-icon {
  color: #dc2626;
  transform: scale(1.15);
}

@keyframes pulse-alert {
  0%, 100% {
    box-shadow: inset 0 0 0 0 rgba(239, 68, 68, 0.1);
  }
  50% {
    box-shadow: inset 0 0 15px 0 rgba(239, 68, 68, 0.2);
  }
}

/* ========== MOBILE MENU TOGGLE ========== */
.mobile-menu-toggle {
  display: none;
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 1001;
  background: #7c3aed;
  color: white;
  border: none;
  border-radius: 50%;
  width: 56px;
  height: 56px;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(124, 58, 237, 0.4);
  transition: all 0.3s ease;
}

.mobile-menu-toggle:hover {
  background: #6d28d9;
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
}

.mobile-menu-toggle:active {
  transform: scale(0.95);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .dashboard-container {
    flex-direction: column;
  }

  .dashboard-sidebar {
    position: fixed;
    top: 70px;
    left: -100%;
    width: 280px;
    height: calc(100vh - 70px);
    background: #F9FAFB;
    border-right: 1px solid #E5E7EB;
    z-index: 1000;
    transition: left 0.3s ease;
    overflow-y: auto;
  }

  .dashboard-sidebar.mobile-open {
    left: 0;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  }

  .dashboard-content {
    padding: 1rem;
    width: 100%;
  }

  .menu-item {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }

  .dashboard-navbar {
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0.75rem;
    margin-bottom: 1rem;
  }

  .navbar-actions {
    width: 100%;
    flex-direction: row;
    gap: 0.5rem;
    justify-content: space-between;
  }

  .navbar-btn {
    flex: 1;
    padding: 0.625rem;
    font-size: 0.75rem;
    min-width: 0;
    flex-direction: column;
    gap: 0.25rem;
  }

  .navbar-btn span {
    font-size: 0.7rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
  }

  .navbar-btn :deep(.va-icon) {
    margin: 0;
    font-size: 1.25rem;
  }

  .navbar-menu {
    width: 100%;
  }

  .dropdown-wrapper {
    width: 100%;
  }

  .navbar-btn-config {
    width: 100%;
    justify-content: center;
    flex-direction: row !important; /* Mantener horizontal en móvil */
    padding: 0.75rem 1rem;
  }

  .navbar-btn-config span {
    font-size: 0.9rem !important; /* Texto normal para el botón Cuenta */
  }

  .dropdown-content {
    left: 0;
    right: 0;
    width: 100%;
    min-width: auto;
  }
}

/* Estilos para el formulario de cambio de contraseña */
.password-form {
  padding: 0.5rem 0 1rem 0;
}

.password-field {
  margin-bottom: 2rem !important;
}

.password-field:last-child {
  margin-bottom: 1rem !important;
}

/* Darle más espacio a los labels */
.password-field :deep(.va-input__label) {
  margin-bottom: 0.75rem !important;
  font-weight: 500 !important;
  color: #374151 !important;
}

/* Más altura al input */
.password-field :deep(.va-input-wrapper__field) {
  padding: 0.75rem !important;
  font-size: 0.95rem !important;
}

/* Estilo personalizado para los botones del modal */
:deep(.va-modal__dialog .va-modal__footer .va-button) {
  padding: 0.4rem 1.25rem !important;
  font-weight: 500 !important;
  border-radius: 6px !important;
  transition: all 0.3s ease !important;
  font-size: 0.9rem !important;
  line-height: 1.4 !important;
}

:deep(.va-modal__dialog .va-modal__footer .va-button:first-child) {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
  border: none !important;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.25) !important;
  color: white !important;
}

:deep(.va-modal__dialog .va-modal__footer .va-button:first-child:hover) {
  background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35) !important;
  transform: translateY(-1px) !important;
}

:deep(.va-modal__dialog .va-modal__footer .va-button:first-child:active) {
  transform: translateY(0) !important;
  box-shadow: 0 1px 4px rgba(16, 185, 129, 0.25) !important;
}

/* Badge de notificaciones no leídas */
.notification-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  margin-left: auto;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 700;
  line-height: 1;
}

.notification-badge.orders-badge {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  animation: pulse-orders 2s ease-in-out infinite;
}

@keyframes pulse-orders {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(239, 68, 68, 0);
  }
}

.notification-badge.applications-badge {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  animation: pulse-applications 2s ease-in-out infinite;
}

@keyframes pulse-applications {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(59, 130, 246, 0);
  }
}

.menu-item {
  position: relative;
}

.menu-item .notification-badge {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
}

/* Badge para dropdown de Alertas */
.dropdown-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  margin-left: auto;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 700;
  line-height: 1;
  animation: pulse-badge 2s ease-in-out infinite;
}

@keyframes pulse-badge {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    box-shadow: 0 0 0 4px rgba(239, 68, 68, 0);
  }
}

.dropdown-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
</style>
