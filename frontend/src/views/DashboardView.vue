<!-- frontend/src/views/DashboardView.vue -->
<template>
  <div class="dashboard-layout">
    <Dashboard :active-section="activeSection">
      <!-- Home/Tablero Section -->
      <div v-if="activeSection === 'home'" class="dashboard-section">
        <DashboardHome />
      </div>

      <!-- Profile Section -->
      <div v-else-if="activeSection === 'profile'" class="dashboard-section">
        <UserProfileEdit
          :user-profile-id="userProfileId"
          @close="closeEditor"
          @updated="handleProfileUpdated"
        />
      </div>

      <!-- Company Profile Section -->
      <div v-else-if="activeSection === 'company'" class="dashboard-section">
        <CompanyProfileEdit
          :user-profile-id="userProfileId"
          :company-profile-id="companyProfileId"
          @close="closeEditor"
          @created="handleCompanyCreated"
          @updated="handleCompanyUpdated"
        />
      </div>

      <!-- Mis Órdenes Section -->
      <div v-else-if="activeSection === 'jobs'" class="dashboard-section">
        <MisOrdenes :user-profile-id="userProfileId" />
      </div>

      <!-- Jobs Manager Section -->
      <div v-else-if="activeSection === 'jobs_manager'" class="dashboard-section">
        <JobsManager :user-profile-id="userProfileId" />
      </div>

      <!-- Candidates Section -->
      <div v-else-if="activeSection === 'candidates'" class="dashboard-section">
        <CandidatesView />
      </div>

      <!-- CV Section (Applicant Only) -->
      <div v-else-if="activeSection === 'cv'" class="dashboard-section">
        <CVManager />
      </div>

      <!-- Applications Section (Applicant Only) -->
      <div v-else-if="activeSection === 'applications'" class="dashboard-section">
        <ApplicationsView />
      </div>

      <!-- Shortlisted/Favorites Section (Applicant Only) -->
      <div v-else-if="activeSection === 'shortlisted'" class="dashboard-section">
        <ShortlistedView />
      </div>

      <!-- Blocked Users Section (Company Only) -->
      <div v-else-if="activeSection === 'blocked'" class="dashboard-section">
        <BlockedUsersList :user-profile-id="userProfileId" />
      </div>

      <!-- Messages Section -->
      <div v-else-if="activeSection === 'messages'" class="dashboard-section">
        <MessagesView :user-profile-id="userProfileId" />
      </div>

      <!-- Placeholder Sections -->
      <div v-else class="dashboard-placeholder">
        <va-icon :name="getSectionIcon(activeSection)" size="3rem" color="purple" />
        <h2>{{ getSectionTitle(activeSection) }}</h2>
        <p>Esta sección estará disponible próximamente</p>
      </div>
    </Dashboard>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import Dashboard from '@/components/Profile/Dashboard.vue'
import UserProfileEdit from '@/components/Profile/UserProfileEdit.vue'
import CompanyProfileEdit from '@/components/Profile/CompanyProfileEdit.vue'
import DashboardHome from '@/components/Dashboard/DashboardHome.vue'
import JobsManager from '@/components/Dashboard/JobsManager.vue'
import MisOrdenes from '@/components/Dashboard/MisOrdenes.vue'
import CandidatesView from '@/components/Dashboard/CandidatesView.vue'
import BlockedUsersList from '@/components/Dashboard/BlockedUsersList.vue'
import MessagesView from '@/components/Dashboard/MessagesView.vue'
import CVManager from '@/components/Dashboard/CVManager.vue'
import ApplicationsView from '@/components/Dashboard/ApplicationsView.vue'
import ShortlistedView from '@/components/Dashboard/ShortlistedView.vue'

// ========== COMPOSABLES ==========
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// ========== DATA ==========
const activeSection = ref('home')
const userProfileId = ref(null)
const companyProfileId = ref(null)

// ========== LIFECYCLE ==========
onMounted(async () => {
  // ¡IMPORTANTE! NO volver a llamar initAuth() aquí
  // Ya se ejecutó en main.js al startup
  // initAuth() solo debe ejecutarse UNA VEZ
  console.log('📋 DashboardView mounted - authStore.isInitialized:', authStore.isInitialized)
  console.log('📋 DashboardView mounted - authStore.isAuthenticated:', authStore.isAuthenticated)

  // Luego cargar el perfil del usuario
  await loadUserProfile()

  // Cargar empresa ANTES de inicializar la ruta (para evitar race condition)
  await loadUserCompany()

  // Finalmente inicializar la ruta (cambiar activeSection)
  initializeFromRoute()
})

// Observar cambios en la ruta
watch(() => route.path, () => {
  initializeFromRoute()
})

watch(() => route.query.tab, () => {
  initializeFromRoute()
})

// Recargar empresa cuando se cambia a la sección de empresa
watch(() => activeSection.value, async (newSection) => {
  if (newSection === 'company') {
    await loadUserCompany()
  }
})

// ========== METHODS ==========
const initializeFromRoute = () => {
  // Soportar tanto /dashboard?tab=profile como /dashboard/profile
  let tab = route.query.tab || 'home'

  // Si la ruta es /dashboard/profile, /dashboard/company, etc.
  if (route.path.includes('/dashboard/')) {
    const pathParts = route.path.split('/')
    let section = pathParts[pathParts.length - 1]
    if (section && section !== 'dashboard') {
      // Convertir guiones a guiones bajos (jobs-manager -> jobs_manager)
      section = section.replace(/-/g, '_')
      tab = section
    }
  }

  activeSection.value = tab
}

const loadUserProfile = async () => {
  try {
    if (!authStore.accessToken) {
      return
    }

    // Llamar al endpoint /api/profiles/me/ con autenticación
    const url = 'http://localhost:8000/api/profiles/me/'
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.accessToken}`
    }

    const response = await fetch(url, {
      method: 'GET',
      headers: headers
    })

    if (response.ok) {
      const data = await response.json()
      if (data.success && data.profile) {
        userProfileId.value = data.profile.id
        // Guardar en localStorage para futuras referencias
        localStorage.setItem('userProfileId', data.profile.id)
      }
    } else {
      const errorData = await response.json()
      console.error('Error al obtener el perfil:', response.status, errorData)
    }

    // Cargar empresa del usuario si existe
    await loadUserCompany()
  } catch (err) {
    console.error('Error cargando perfil:', err)
  }
}

const loadUserCompany = async () => {
  try {
    if (!authStore.accessToken) {
      console.log('⚠️ No access token available')
      return
    }

    const url = 'http://localhost:8000/api/profiles/company/me/'
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.accessToken}`
    }

    console.log('📦 Llamando a loadUserCompany:', url)
    const response = await fetch(url, {
      method: 'GET',
      headers: headers
    })

    console.log('📦 Response status:', response.status)
    if (response.ok) {
      const data = await response.json()
      console.log('📦 Company data:', data)
      if (data.success && data.company) {
        console.log('✅ Company found:', data.company.id)
        companyProfileId.value = data.company.id
        localStorage.setItem('companyProfileId', data.company.id)
      } else {
        console.log('⚠️ No company found:', data)
      }
    } else {
      const errorData = await response.json()
      console.error('❌ Error response:', response.status, errorData)
    }
  } catch (err) {
    console.error('❌ Error cargando empresa:', err)
  }
}

const getSectionIcon = (section) => {
  const icons = {
    'home': 'home',
    'profile': 'person',
    'company': 'business',
    'jobs': 'work',
    'jobs_manager': 'folder',
    'candidates': 'people',
    'messages': 'mail',
    'users': 'people',
    'history': 'history',
    'notifications': 'notifications',
    'blocked': 'block',
    'shortlisted': 'bookmark',
    'password': 'lock'
  }
  return icons[section] || 'dashboard'
}

const getSectionTitle = (section) => {
  const titles = {
    'home': 'Tablero',
    'profile': 'Mi Perfil',
    'company': 'Perfil De La Empresa',
    'jobs': 'Mis Órdenes',
    'jobs_manager': 'Mis Publicaciones',
    'candidates': 'Candidatos Guardados',
    'messages': 'Comunicaciones',
    'users': 'Gestionar Usuarios',
    'history': 'Registro De Actividad',
    'notifications': 'Alertas',
    'blocked': 'Usuarios Bloqueados',
    'shortlisted': 'Favoritos',
    'password': 'Cambiar Contraseña'
  }
  return titles[section] || 'Dashboard'
}

const closeEditor = () => {
  activeSection.value = 'home'
  router.push('/dashboard')
}

const handleProfileUpdated = (profile) => {
  console.log('Perfil actualizado:', profile)
  // Actualizar el authStore con el nuevo nombre
  if (authStore.user) {
    authStore.user.name = profile.fullName || profile.name
    authStore.user.email = profile.email
  }
  // Actualizar también en localStorage
  const storedUser = localStorage.getItem('authUser')
  if (storedUser) {
    const user = JSON.parse(storedUser)
    user.name = profile.fullName || profile.name
    localStorage.setItem('authUser', JSON.stringify(user))
  }
  // Ir al home para ver los cambios
  closeEditor()
}

const handleCompanyCreated = (company) => {
  console.log('Empresa creada:', company)
  companyProfileId.value = company.id
}

const handleCompanyUpdated = (company) => {
  console.log('Empresa actualizada:', company)
}
</script>

<style scoped>
.dashboard-layout {
  min-height: calc(100vh - 70px);
  background: #f5f5f5;
}

.dashboard-section {
  animation: fadeIn 0.3s ease-in-out;
}

.dashboard-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin: 2rem;
}

.dashboard-placeholder h2 {
  margin: 1rem 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a1a1a;
}

.dashboard-placeholder p {
  color: #666;
  margin-bottom: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
