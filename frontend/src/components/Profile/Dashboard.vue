<!-- frontend/src/components/Profile/Dashboard.vue -->
<template>
  <div class="dashboard-container">
    <!-- Sidebar Navigation -->
    <div class="dashboard-sidebar">
      <div class="sidebar-header">
        <h2>Mi Cuenta</h2>
      </div>

      <nav class="sidebar-menu">
        <!-- Main Sections -->
        <router-link
          to="/dashboard"
          class="menu-item"
          :class="{ active: activeSection === 'home' }"
        >
          <va-icon name="home" />
          <span>Tablero</span>
        </router-link>

        <router-link
          to="/dashboard/profile"
          class="menu-item"
          :class="{ active: activeSection === 'profile' }"
        >
          <va-icon name="person" />
          <span>Mi Perfil</span>
        </router-link>

        <router-link
          to="/dashboard/company"
          class="menu-item"
          :class="{ active: activeSection === 'company' }"
        >
          <va-icon name="business" />
          <span>Perfil De La Empresa</span>
        </router-link>

        <router-link
          to="/dashboard/jobs"
          class="menu-item"
          :class="{ active: activeSection === 'jobs' }"
        >
          <va-icon name="work" />
          <span>Mis Órdenes</span>
        </router-link>

        <router-link
          to="/publicar"
          class="menu-item highlight"
          :class="{ active: activeSection === 'publish' }"
        >
          <va-icon name="add_circle" />
          <span>Publicar Un Nuevo Trabajo</span>
        </router-link>

        <router-link
          to="/dashboard/jobs-manager"
          class="menu-item"
          :class="{ active: activeSection === 'jobs_manager' }"
        >
          <va-icon name="folder" />
          <span>Mis Publicaciones</span>
        </router-link>

        <!-- Divider -->
        <div class="menu-divider"></div>

        <!-- Additional Options -->
        <router-link
          to="/dashboard/candidates"
          class="menu-item"
          :class="{ active: activeSection === 'candidates' }"
        >
          <va-icon name="people" />
          <span>Candidatos Guardados</span>
        </router-link>

        <router-link
          to="/dashboard/blocked"
          class="menu-item"
          :class="{ active: activeSection === 'blocked' }"
        >
          <va-icon name="block" />
          <span>Usuarios Bloqueados</span>
        </router-link>

        <router-link
          to="/dashboard/shortlisted"
          class="menu-item"
          :class="{ active: activeSection === 'shortlisted' }"
        >
          <va-icon name="bookmark" />
          <span>Favoritos</span>
        </router-link>

        <router-link
          to="/dashboard/messages"
          class="menu-item"
          :class="{ active: activeSection === 'messages' }"
        >
          <va-icon name="mail" />
          <span>Comunicaciones</span>
        </router-link>

        <!-- Divider -->
        <div class="menu-divider"></div>

        <!-- Settings -->
        <router-link
          to="/dashboard/users"
          class="menu-item"
          :class="{ active: activeSection === 'users' }"
        >
          <va-icon name="people" />
          <span>Gestionar Usuarios</span>
        </router-link>

        <router-link
          to="/dashboard/history"
          class="menu-item"
          :class="{ active: activeSection === 'history' }"
        >
          <va-icon name="history" />
          <span>Registro De Actividad</span>
        </router-link>

        <router-link
          to="/dashboard/notifications"
          class="menu-item"
          :class="{ active: activeSection === 'notifications' }"
        >
          <va-icon name="notifications" />
          <span>Alertas</span>
        </router-link>

        <!-- Account Settings -->
        <div class="menu-divider"></div>

        <div
          @click="showChangePassword = true"
          class="menu-item"
          :class="{ active: activeSection === 'password' }"
        >
          <va-icon name="lock" />
          <span>Cambiar Contraseña</span>
        </div>

        <div
          @click="handleLogout"
          class="menu-item"
        >
          <va-icon name="logout" />
          <span>Cerrar Sesión</span>
        </div>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="dashboard-content">
      <slot></slot>
    </div>

    <!-- Change Password Modal -->
    <va-modal
      v-model="showChangePassword"
      title="Cambiar Contraseña"
      ok-text="Cambiar"
      cancel-text="Cancelar"
    >
      <p>Funcionalidad disponible próximamente</p>
    </va-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vuestic-ui'

// ========== COMPOSABLES ==========
const router = useRouter()
const route = useRoute()
const { init: notify } = useToast()

// ========== DATA ==========
const activeSection = ref('home')
const showChangePassword = ref(false)

// ========== LIFECYCLE ==========
onMounted(() => {
  updateActiveSection()
})

watch(() => route.path, () => {
  updateActiveSection()
})

// ========== METHODS ==========
const updateActiveSection = () => {
  const path = route.path
  if (path.includes('/profile')) {
    activeSection.value = 'profile'
  } else if (path.includes('/company')) {
    activeSection.value = 'company'
  } else if (path.includes('/publish')) {
    activeSection.value = 'publish'
  } else if (path.includes('/jobs-manager')) {
    activeSection.value = 'jobs_manager'
  } else if (path.includes('/jobs')) {
    activeSection.value = 'jobs'
  } else if (path.includes('/candidates')) {
    activeSection.value = 'candidates'
  } else if (path.includes('/messages')) {
    activeSection.value = 'messages'
  } else if (path.includes('/users')) {
    activeSection.value = 'users'
  } else if (path.includes('/history')) {
    activeSection.value = 'history'
  } else if (path.includes('/notifications')) {
    activeSection.value = 'notifications'
  } else if (path.includes('/blocked')) {
    activeSection.value = 'blocked'
  } else if (path.includes('/shortlisted')) {
    activeSection.value = 'shortlisted'
  } else {
    activeSection.value = 'home'
  }
}

const handleLogout = () => {
  notify({
    message: 'Cerrando sesión...',
    color: 'info'
  })
  // TODO: Implementar logout
  setTimeout(() => {
    router.push('/')
  }, 1000)
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
  padding: 0.5rem 0;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.5rem;
  color: #6B7280;
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all 0.2s ease;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
}

.menu-item:hover {
  background: #F3F4F6;
  color: var(--color-purple);
}

.menu-item.active {
  background: white;
  color: var(--color-purple);
  border-left-color: var(--color-purple);
  border-left-width: 3px;
  font-weight: 600;
}

.menu-item.highlight {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  margin: 0.5rem 0.5rem;
  font-weight: 600;
  border-radius: 6px;
  border-left: none;
  padding-left: 1.5rem;
  transition: all 0.3s ease;
}

.menu-item.highlight:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
}

.menu-item.highlight.active {
  color: white;
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
}

.menu-divider {
  height: 1px;
  background: #E5E7EB;
  margin: 0.75rem 0;
}

/* ========== MAIN CONTENT ========== */
.dashboard-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }

  .dashboard-sidebar {
    width: 100%;
    max-height: 400px;
    border-right: none;
    border-bottom: 1px solid var(--color-gray-medium);
    position: relative;
    top: 0;
    height: auto;
  }

  .dashboard-content {
    padding: 1rem;
  }

  .menu-item {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
