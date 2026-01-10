<!-- frontend/src/components/Dashboard/DashboardHome.vue -->
<template>
  <div class="dashboard-home">
    <!-- Header -->
    <div class="dashboard-header">
      <div>
        <h1 class="header-title">{{ greeting }}, {{ userName }}</h1>
        <p class="header-subtitle">Aquí está tu resumen de tus actividades</p>
      </div>
      <div class="header-date">
        {{ currentDate }}
      </div>
    </div>

    <!-- Alerta de Perfil Incompleto - POSTULANTE -->
    <div
      v-if="authStore.user?.role === 'applicant' && !stats.profileComplete && stats.profilePercentage < 80"
      class="profile-warning-alert"
    >
      <div class="alert-icon">
        <va-icon name="warning" size="large" />
      </div>
      <div class="alert-content">
        <h3 class="alert-title">⚠️ Completa tu perfil para postular</h3>
        <p class="alert-message">
          Tu perfil está completo al <strong>{{ stats.profilePercentage }}%</strong>.
          Necesitas al menos <strong>80%</strong> para poder postular a ofertas laborales.
        </p>
        <p class="alert-info">
          <strong>Campos obligatorios:</strong> Foto de perfil, Nombre completo, Cédula de Identidad (C.I.), Nacionalidad y WhatsApp
        </p>
      </div>
      <button class="alert-btn" @click="goToSection('profile')">
        <va-icon name="person" />
        <span>Completar Perfil</span>
      </button>
    </div>

    <!-- Stats Grid - EMPRESA -->
    <div v-if="authStore.user?.role === 'company'" class="stats-grid">
      <!-- Card: Publicaciones -->
      <div class="stat-card stat-card-with-chart" @click="goToSection('jobs')">
        <div class="stat-icon jobs">
          <va-icon name="list_alt" />
        </div>
        <div class="stat-content">
          <h3>Publicaciones</h3>
          <div class="stat-number">{{ stats.totalPublished }}</div>
          <p class="stat-subtitle">{{ stats.activeListings }} activas</p>
        </div>
        <div class="stat-chart">
          <mini-donut-chart
            :value="stats.activeListings"
            :total="stats.totalPublished || 1"
            color="#7c3aed"
          />
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Interacciones -->
      <div class="stat-card stat-card-with-chart" @click="goToSection('candidates')">
        <div class="stat-icon applications">
          <va-icon name="people" />
        </div>
        <div class="stat-content">
          <h3>Interacciones</h3>
          <div class="stat-number">{{ stats.totalApplications }}</div>
          <p class="stat-subtitle">{{ stats.newApplications }} nuevas</p>
        </div>
        <div class="stat-chart">
          <mini-donut-chart
            :value="stats.newApplications"
            :total="stats.totalApplications || 1"
            color="#3B82F6"
          />
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Vistas -->
      <div class="stat-card stat-card-with-chart">
        <div class="stat-icon views">
          <va-icon name="visibility" />
        </div>
        <div class="stat-content">
          <h3>Vistas Totales</h3>
          <div class="stat-number">{{ stats.totalViews }}</div>
          <p class="stat-subtitle">Esta semana</p>
        </div>
        <div class="stat-chart">
          <mini-bar-chart
            :value="stats.totalViews"
            :total="500"
            color="#F59E0B"
          />
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Perfil Completado -->
      <div class="stat-card stat-card-with-chart" :class="{ incomplete: !stats.profileComplete }" @click="goToSection('profile')">
        <div class="stat-icon profile" :class="{ incomplete: !stats.profileComplete }">
          <va-icon :name="stats.profileComplete ? 'check_circle' : 'person'" />
        </div>
        <div class="stat-content">
          <h3>Perfil</h3>
          <div class="stat-number">{{ stats.profilePercentage }}%</div>
          <p class="stat-subtitle" v-if="!stats.profileComplete">Completa tu perfil</p>
          <p class="stat-subtitle" v-else>Perfil completo</p>
        </div>
        <div class="stat-chart">
          <mini-bar-chart
            :value="stats.profilePercentage"
            :total="100"
            color="#10B981"
          />
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>
    </div>

    <!-- Stats Grid - POSTULANTE -->
    <div v-else-if="authStore.user?.role === 'applicant'" class="stats-grid">
      <!-- Card: Mis Postulaciones -->
      <div class="stat-card stat-card-with-chart" @click="goToSection('applications')">
        <div class="stat-icon applications">
          <va-icon name="assignment" />
        </div>
        <div class="stat-content">
          <h3>Mis Postulaciones</h3>
          <div class="stat-number">{{ stats.totalApplications }}</div>
          <p class="stat-subtitle">{{ stats.pendingApplications }} pendientes</p>
        </div>
        <div class="stat-chart">
          <mini-donut-chart
            :value="stats.pendingApplications"
            :total="stats.totalApplications || 1"
            color="#7c3aed"
          />
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Favoritos -->
      <div class="stat-card stat-card-with-chart" @click="goToSection('shortlisted')">
        <div class="stat-icon views">
          <va-icon name="bookmark" />
        </div>
        <div class="stat-content">
          <h3>Favoritos</h3>
          <div class="stat-number">{{ stats.savedJobs }}</div>
          <p class="stat-subtitle">Anuncios guardados</p>
        </div>
        <div class="stat-chart">
          <mini-bar-chart
            :value="stats.savedJobs"
            :total="10"
            color="#F59E0B"
          />
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Perfil Completado -->
      <div class="stat-card stat-card-with-chart" :class="{ incomplete: !stats.profileComplete }" @click="goToSection('profile')">
        <div class="stat-icon profile" :class="{ incomplete: !stats.profileComplete }">
          <va-icon :name="stats.profileComplete ? 'check_circle' : 'person'" />
        </div>
        <div class="stat-content">
          <h3>Perfil</h3>
          <div class="stat-number">{{ stats.profilePercentage }}%</div>
          <p class="stat-subtitle" v-if="!stats.profileComplete">Completa tu perfil</p>
          <p class="stat-subtitle" v-else>Perfil completo</p>
        </div>
        <div class="stat-chart">
          <mini-bar-chart
            :value="stats.profilePercentage"
            :total="100"
            color="#10B981"
          />
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: CV -->
      <div class="stat-card stat-card-with-chart" @click="goToSection('cv')">
        <div class="stat-icon jobs">
          <va-icon name="description" />
        </div>
        <div class="stat-content">
          <h3>Mi CV</h3>
          <div class="stat-number">{{ stats.cvCount }}</div>
          <p class="stat-subtitle">CV creados</p>
        </div>
        <div class="stat-chart">
          <mini-donut-chart
            :value="stats.cvCount"
            :total="2"
            color="#7c3aed"
          />
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>
    </div>

    <!-- Charts Section - POSTULANTE -->
    <!-- TEMPORALMENTE COMENTADO PARA DEBUGGING
    <div v-if="authStore.user?.role === 'applicant'" class="charts-section">
      <div class="charts-grid">
        <profile-progress
          :percentage="stats.profilePercentage"
          :required-fields="profileFields"
          @go-to-profile="goToSection('profile')"
        />

        <div class="chart-card">
          <h3 class="chart-title">
            <va-icon name="pie_chart" size="small" />
            <span>Estado de Postulaciones</span>
          </h3>
          <doughnut-chart :data="applicationsChartData" />
        </div>
      </div>

      <div class="chart-card chart-wide">
        <h3 class="chart-title">
          <va-icon name="bar_chart" size="small" />
          <span>Actividad del Último Mes</span>
        </h3>
        <bar-chart :data="activityChartData" />
      </div>
    </div>

    <div v-else-if="authStore.user?.role === 'company'" class="charts-section">
      <div class="charts-grid">
        <div class="chart-card">
          <h3 class="chart-title">
            <va-icon name="pie_chart" size="small" />
            <span>Estado de Publicaciones</span>
          </h3>
          <doughnut-chart :data="jobsChartData" />
        </div>

        <div class="chart-card">
          <h3 class="chart-title">
            <va-icon name="pie_chart" size="small" />
            <span>Candidatos por Estado</span>
          </h3>
          <doughnut-chart :data="candidatesChartData" />
        </div>
      </div>

      <div class="chart-card chart-wide">
        <h3 class="chart-title">
          <va-icon name="bar_chart" size="small" />
          <span>Vistas del Último Mes</span>
        </h3>
        <bar-chart :data="viewsChartData" />
      </div>
    </div>
    -->

    <!-- Quick Actions - EMPRESA -->
    <div v-if="authStore.user?.role === 'company'" class="quick-actions">
      <h2>Acciones Rápidas</h2>
      <div class="actions-grid">
        <button class="action-btn" @click="goToPublish">
          <va-icon name="add_circle" />
          <span>Publicar Nuevo Anuncio </span>
        </button>
        <button class="action-btn" @click="goToSection('jobs_manager')">
          <va-icon name="folder" />
          <span>Ver Anuncios creados</span>
        </button>
        <button class="action-btn" @click="goToSection('candidates')">
          <va-icon name="people" />
          <span>Ver Postulaciones</span>
        </button>
        <button class="action-btn" @click="goToSection('profile')">
          <va-icon name="person" />
          <span>Perfil Empresa</span>
        </button>
      </div>
    </div>

    <!-- Quick Actions - POSTULANTE -->
    <div v-else-if="authStore.user?.role === 'applicant'" class="quick-actions">
      <h2>Acciones Rápidas</h2>
      <div class="actions-grid">
        <button class="action-btn" @click="goToPublish">
          <va-icon name="search" />
          <span>Buscar Trabajos</span>
        </button>
        <button class="action-btn" @click="goToSection('applications')">
          <va-icon name="assignment" />
          <span>Ver Postulaciones</span>
        </button>
        <button class="action-btn" @click="goToSection('cv')">
          <va-icon name="description" />
          <span>Mi CV</span>
        </button>
        <button class="action-btn" @click="goToSection('profile')">
          <va-icon name="person" />
          <span>Mi Perfil</span>
        </button>
      </div>
    </div>

    <!-- Tips Section - POSTULANTE -->
    <div v-if="authStore.user?.role === 'applicant'" class="tips-section">
      <h2>Consejos para Postulantes</h2>
      <div class="tips-grid">
        <div class="tip-card">
          <h4>Perfil completo</h4>
          <p>Un perfil con toda la información aumenta tus posibilidades de ser contactado</p>
        </div>
        <div class="tip-card">
          <h4>CV actualizado</h4>
          <p>Mantén tu CV actualizado con tu experiencia y habilidades más recientes</p>
        </div>
        <div class="tip-card">
          <h4>Postula con criterio</h4>
          <p>Lee bien los requisitos antes de postular y personaliza tu postulación</p>
        </div>
      </div>
    </div>

    <!-- Tips Section - EMPRESA -->
    <div v-else-if="authStore.user?.role === 'company'" class="tips-section">
      <h2>Consejos para Empresas</h2>
      <div class="tips-grid">
        <div class="tip-card">
          <h4>Contenido de calidad</h4>
          <p>Las publicaciones completas reciben más interacciones y vistas</p>
        </div>
        <div class="tip-card">
          <h4>Descripción clara</h4>
          <p>Describe bien lo que ofreces para atraer mejores candidatos</p>
        </div>
        <div class="tip-card">
          <h4>Responde rápido</h4>
          <p>Los candidatos valoran las respuestas inmediatas a sus postulaciones</p>
        </div>
      </div>
    </div>

    <!-- Coming Soon Section - Other Guides -->
    <div class="coming-soon-section">
      <div class="coming-soon-header">
        <h2>Próximas Guías</h2>
        <p>Estamos trabajando en expandir Guías Púrpuras</p>
      </div>
      <div class="coming-soon-grid">
        <div class="coming-soon-card">
          <div class="coming-soon-icon gastronomy">
            <va-icon name="restaurant" />
          </div>
          <h3>Guías Gastronomía</h3>
          <p>Descubre y publica los mejores restaurantes</p>
          <div class="coming-soon-badge">Próximamente</div>
        </div>
        <div class="coming-soon-card">
          <div class="coming-soon-icon business">
            <va-icon name="business" />
          </div>
          <h3>Guías Negocios</h3>
          <p>Promociona y gestiona tu negocio</p>
          <div class="coming-soon-badge">Próximamente</div>
        </div>
        <div class="coming-soon-card">
          <div class="coming-soon-icon professionals">
            <va-icon name="person" />
          </div>
          <h3>Guías Profesionales</h3>
          <p>Conecta con los mejores profesionales</p>
          <div class="coming-soon-badge">Próximamente</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import { useAuthStore } from '@/stores/useAuthStore'
import { useDashboardStats } from '@/composables/useDashboardStats'
import { useDashboardActivities } from '@/composables/useDashboardActivities'
import MiniDonutChart from './MiniDonutChart.vue'
import MiniBarChart from './MiniBarChart.vue'
// import DoughnutChart from './Charts/DoughnutChart.vue'
// import BarChart from './Charts/BarChart.vue'
// import ProfileProgress from './ProfileProgress.vue'

// ========== COMPOSABLES ==========
const router = useRouter()
const { init: notify } = useToast()
const authStore = useAuthStore()
const dashboardStats = useDashboardStats()
const dashboardActivities = useDashboardActivities()

// ========== DATA ==========
const userName = ref('Usuario')
const currentDate = ref('')
const greeting = ref('Bienvenido')

// Variables para asegurar reactividad
const stats = ref({
  totalPublished: 0,
  activeListings: 0,
  totalApplications: 0,
  newApplications: 0,
  totalViews: 0,
  profileComplete: false,
  profilePercentage: 0,
  pendingApplications: 0,
  savedJobs: 0,
  cvCount: 0
})

const activities = ref([])

// ========== COMPUTED - DATOS DE GRÁFICOS ==========

// Campos obligatorios del perfil para el componente ProfileProgress
// Estimación basada en el porcentaje (cada campo vale 20%)
const profileFields = computed(() => {
  const percentage = stats.value.profilePercentage || 0
  const completedCount = Math.round(percentage / 20)

  return [
    {
      key: 'profilePhoto',
      label: 'Foto de perfil',
      completed: completedCount >= 1
    },
    {
      key: 'fullName',
      label: 'Nombre completo',
      completed: completedCount >= 2
    },
    {
      key: 'ci',
      label: 'Cédula de Identidad',
      completed: completedCount >= 3
    },
    {
      key: 'nationality',
      label: 'Nacionalidad',
      completed: completedCount >= 4
    },
    {
      key: 'phone',
      label: 'WhatsApp',
      completed: completedCount >= 5
    }
  ]
})

// Gráfico de postulaciones para postulantes
const applicationsChartData = computed(() => {
  const total = stats.value.totalApplications || 0
  // Si no hay datos reales, usar datos de ejemplo
  if (total === 0) {
    return {
      labels: ['Pendientes', 'En Revisión', 'Entrevista', 'Aceptadas', 'Rechazadas'],
      values: [5, 3, 2, 1, 1],
      colors: ['#7c3aed', '#3B82F6', '#F59E0B', '#10B981', '#EF4444']
    }
  }

  return {
    labels: ['Pendientes', 'En Revisión', 'Entrevista', 'Aceptadas', 'Rechazadas'],
    values: [
      stats.value.pendingApplications || Math.floor(total * 0.4),
      Math.floor(total * 0.3),
      Math.floor(total * 0.2),
      Math.floor(total * 0.06),
      Math.floor(total * 0.04)
    ],
    colors: ['#7c3aed', '#3B82F6', '#F59E0B', '#10B981', '#EF4444']
  }
})

// Gráfico de publicaciones para empresas
const jobsChartData = computed(() => ({
  labels: ['Activas', 'Pausadas', 'Vencidas'],
  values: [
    stats.value.activeListings || 2,
    Math.max(stats.value.totalPublished - stats.value.activeListings - 1, 1),
    1
  ],
  colors: ['#10B981', '#F59E0B', '#EF4444']
}))

// Gráfico de candidatos para empresas
const candidatesChartData = computed(() => ({
  labels: ['Nuevos', 'En Revisión', 'Entrevista', 'Seleccionados'],
  values: [
    stats.value.newApplications || 3,
    Math.floor(stats.value.totalApplications * 0.4) || 5,
    Math.floor(stats.value.totalApplications * 0.3) || 3,
    Math.floor(stats.value.totalApplications * 0.2) || 2
  ],
  colors: ['#7c3aed', '#3B82F6', '#F59E0B', '#10B981']
}))

// Gráfico de actividad mensual para postulantes
const activityChartData = computed(() => {
  const labels = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
  return {
    labels,
    datasets: [
      {
        label: 'Postulaciones',
        data: [3, 5, 4, 8],
        color: '#7c3aed'
      },
      {
        label: 'Favoritos',
        data: [2, 4, 3, 6],
        color: '#F59E0B'
      }
    ]
  }
})

// Gráfico de vistas para empresas
const viewsChartData = computed(() => {
  const labels = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
  return {
    labels,
    datasets: [
      {
        label: 'Vistas',
        data: [120, 180, 150, 250],
        color: '#3B82F6'
      },
      {
        label: 'Aplicaciones',
        data: [15, 25, 20, 35],
        color: '#10B981'
      }
    ]
  }
})

// ========== LIFECYCLE ==========
onMounted(() => {
  initializeDashboard()
  setCurrentDate()
  setGreeting()
})

// Observar cambios en el nombre del usuario
watch(() => authStore.user?.name, (newName) => {
  if (newName) {
    userName.value = newName
  }
})

// ========== METHODS ==========

const initializeDashboard = async () => {
  try {
    // Obtener nombre del usuario desde authStore (tiene prioridad)
    // El backend ahora envía el nombre directamente desde UserProfile.fullName
    if (authStore.user?.name) {
      userName.value = authStore.user.name
    } else {
      // Fallback a localStorage
      const storedUser = localStorage.getItem('auth_user')
      if (storedUser) {
        const user = JSON.parse(storedUser)
        userName.value = user.name || 'Usuario'
      } else {
        userName.value = 'Usuario'
      }
    }

    // Cargar estadísticas
    await dashboardStats.loadStats()
    // Copiar datos a nuestra variable local reactiva Y agregar campos que no vienen del backend
    stats.value = {
      ...dashboardStats.stats.value,
      // Mantener valores por defecto para campos que no vienen del backend
      pendingApplications: dashboardStats.stats.value.pendingApplications || 0,
      savedJobs: dashboardStats.stats.value.savedJobs || 0,
      cvCount: dashboardStats.stats.value.cvCount || 0
    }

    // Cargar actividades (con manejo seguro)
    try {
      await dashboardActivities.loadActivities(5)
      // Copiar datos de forma segura
      if (Array.isArray(dashboardActivities.activities)) {
        activities.value = [...dashboardActivities.activities]
      } else {
        activities.value = []
      }
    } catch (actErr) {
      console.warn('⚠️ [Dashboard] Error cargando actividades (no crítico):', actErr)
      activities.value = []
    }
  } catch (err) {
    console.error('❌ [Dashboard] Error crítico inicializando dashboard:', err)
    // No establecer dummy data aquí, dejar que stats mantenga sus valores por defecto
  }
}

const setCurrentDate = () => {
  const options = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }
  const today = new Date()
  currentDate.value = today.toLocaleDateString('es-ES', options)
}

const setGreeting = () => {
  // Obtener hora en La Paz, Bolivia (UTC-4)
  const now = new Date()
  const laPazTime = new Date(now.toLocaleString('en-US', { timeZone: 'America/La_Paz' }))
  const hour = laPazTime.getHours()

  if (hour >= 5 && hour < 12) {
    greeting.value = 'Buenos días'
  } else if (hour >= 12 && hour < 19) {
    greeting.value = 'Buenas tardes'
  } else {
    greeting.value = 'Buenas noches'
  }
}

const goToSection = (section) => {
  const routes = {
    jobs_manager: '/dashboard/jobs-manager',
    candidates: '/dashboard/candidates',
    profile: '/dashboard/profile',
    applications: '/dashboard/applications',
    cv: '/dashboard/cv',
    shortlisted: '/dashboard/shortlisted'
  }
  if (routes[section]) {
    router.push(routes[section])
  } else {
    console.warn(`Ruta no encontrada para sección: ${section}`)
  }
}

const goToPublish = () => {
  // Para empresa: ir a publicar anuncio
  // Para postulante: ir a buscar trabajos
  if (authStore.user?.role === 'company') {
    router.push('/publicar')
  } else {
    router.push('/guias/trabajos')
  }
}
</script>

<style scoped>
.dashboard-home {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* ========== HEADER ========== */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  padding: 2rem 2.5rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.25);
  position: relative;
  overflow: hidden;
}

/* Efecto de brillo sutil en el header */
.dashboard-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  animation: shine 3s infinite;
}

@keyframes shine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.header-title {
  margin: 0 0 0.5rem;
  font-size: 2rem;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 1;
}

.header-subtitle {
  margin: 0;
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.header-date {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
  white-space: nowrap;
  background: rgba(255, 255, 255, 0.15);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;
}

/* ========== PROFILE WARNING ALERT ========== */
.profile-warning-alert {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #F3E8FF 0%, #EDE9FE 100%);
  border-left: 4px solid #7c3aed;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.15);
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.alert-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  border-radius: 12px;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.alert-content {
  flex: 1;
}

.alert-title {
  margin: 0 0 0.75rem 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: #4C1D95;
}

.alert-message {
  margin: 0 0 0.75rem 0;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #6D28D9;
}

.alert-message strong {
  color: #5B21B6;
  font-weight: 700;
}

.alert-info {
  margin: 0;
  font-size: 0.875rem;
  color: #7C3AED;
  font-style: italic;
}

.alert-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
  white-space: nowrap;
  flex-shrink: 0;
}

.alert-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
}

.alert-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(124, 58, 237, 0.3);
}

/* ========== STATS GRID ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.stat-card {
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #E4E7EC;
  cursor: pointer;
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: var(--color-purple);
  box-shadow: 0 2px 8px rgba(92, 0, 153, 0.1);
}

.stat-card.incomplete {
  opacity: 0.7;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 8px;
  font-size: 1.6rem;
  color: white;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.stat-card:hover .stat-icon {
  transform: scale(1.05);
}

.stat-icon.jobs {
  background: var(--color-purple);
}

.stat-icon.applications {
  background: #3B82F6;
}

.stat-icon.views {
  background: #F59E0B;
}

.stat-icon.profile {
  background: #10B981;
}

.stat-icon.profile.incomplete {
  background: #F59E0B;
}

.stat-content {
  flex: 1;
}

.stat-content h3 {
  margin: 0;
  font-size: 0.8rem;
  color: #6B7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-number {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0.5rem 0 0;
}

.stat-subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: #9CA3AF;
  font-weight: 500;
}

.stat-arrow {
  color: transparent;
  transition: all 0.2s ease;
  font-size: 1.25rem;
  margin-top: 0.25rem;
}

.stat-card:hover .stat-arrow {
  color: var(--color-purple);
}

/* ========== MINI CHART IN STAT CARD ========== */
.stat-card-with-chart {
  position: relative;
}

.stat-chart {
  position: absolute;
  top: 1rem;
  right: 3.5rem;
  opacity: 0.15;
  transition: opacity 0.2s ease;
}

.stat-card-with-chart:hover .stat-chart {
  opacity: 0.25;
}

/* ========== CHARTS SECTION ========== */
.charts-section {
  margin-bottom: 2.5rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #E5E7EB;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.chart-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.chart-wide {
  grid-column: 1 / -1;
}

.chart-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0 0 1.25rem 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1F2937;
}

.chart-title .va-icon {
  color: #7c3aed;
}

/* ========== QUICK ACTIONS ========== */
.quick-actions {
  margin-bottom: 2.5rem;
}

.quick-actions h2 {
  margin: 0 0 1.25rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1F2937;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}

.action-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
}

.action-btn va-icon {
  font-size: 1.5rem;
  color: white;
  transition: all 0.2s ease;
}

.action-btn:hover va-icon {
  transform: scale(1.1);
}

/* ========== RECENT ACTIVITY ========== */
.recent-activity {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  border: 1px solid #E4E7EC;
  margin-bottom: 2.5rem;
}

.recent-activity h2 {
  margin: 0 0 1.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1F2937;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-left: 3px solid transparent;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.activity-item:hover {
  background: #F3F4F6;
  border-left-color: var(--color-purple);
}

.activity-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 6px;
  color: white;
  flex-shrink: 0;
  transition: all 0.2s ease;
  font-size: 1.25rem;
}

.activity-item:hover .activity-icon {
  transform: scale(1.08);
}

.activity-icon.job {
  background: var(--color-purple);
}

.activity-icon.application {
  background: #3B82F6;
}

.activity-icon.message {
  background: #F59E0B;
}

.activity-icon.profile {
  background: #10B981;
}

.activity-content {
  flex: 1;
}

.activity-title {
  margin: 0;
  font-weight: 600;
  color: #1F2937;
  font-size: 0.9rem;
}

.activity-time {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: #9CA3AF;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 2.5rem 2rem;
  color: #9CA3AF;
  font-size: 0.9rem;
}

/* ========== TIPS SECTION ========== */
.tips-section {
  margin-bottom: 2rem;
}

.tips-section h2 {
  margin: 0 0 1.25rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1F2937;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}

.tip-card {
  background: white;
  border: 1px solid #E4E7EC;
  border-left: 3px solid var(--color-purple);
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.tip-card:hover {
  box-shadow: 0 2px 8px rgba(92, 0, 153, 0.08);
  border-left-color: var(--color-purple);
}

.tip-card h4 {
  margin: 0 0 0.5rem;
  color: #1F2937;
  font-size: 1rem;
  font-weight: 700;
}

.tip-card p {
  margin: 0;
  color: #6B7280;
  font-size: 0.9rem;
  line-height: 1.5;
  font-weight: 500;
}

/* ========== COMING SOON SECTION ========== */
.coming-soon-section {
  margin-bottom: 2rem;
}

.coming-soon-header {
  margin-bottom: 2rem;
}

.coming-soon-header h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
}

.coming-soon-header p {
  margin: 0;
  font-size: 0.95rem;
  color: #6B7280;
}

.coming-soon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}

.coming-soon-card {
  position: relative;
  background: white;
  border: 2px solid #E4E7EC;
  border-radius: 12px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  overflow: hidden;
}

.coming-soon-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #7c3aed, #6d28d9);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.coming-soon-card:hover::before {
  transform: scaleX(1);
}

.coming-soon-card:hover {
  border-color: var(--color-purple);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
  transform: translateY(-4px);
}

.coming-soon-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 12px;
  margin: 0 auto 1rem;
  font-size: 2rem;
  color: white;
  transition: all 0.3s ease;
}

.coming-soon-card:hover .coming-soon-icon {
  transform: scale(1.1) rotate(5deg);
}

.coming-soon-icon.gastronomy {
  background: linear-gradient(135deg, #F59E0B, #F97316);
}

.coming-soon-icon.business {
  background: linear-gradient(135deg, #8B5CF6, #7c3aed);
}

.coming-soon-icon.professionals {
  background: linear-gradient(135deg, #06B6D4, #3B82F6);
}

.coming-soon-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: #1F2937;
}

.coming-soon-card p {
  margin: 0 0 1rem;
  font-size: 0.9rem;
  color: #6B7280;
  line-height: 1.5;
}

.coming-soon-badge {
  display: inline-block;
  padding: 0.4rem 0.875rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.3px;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .dashboard-home {
    padding: 1rem;
  }

  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 1.5rem;
  }

  .header-title {
    font-size: 1.5rem;
  }

  .header-date {
    font-size: 0.85rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .stat-card {
    gap: 1rem;
    padding: 1.25rem;
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    font-size: 1.4rem;
  }

  .stat-number {
    font-size: 1.5rem;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .action-btn {
    padding: 1rem;
    font-size: 0.85rem;
    gap: 0.5rem;
  }

  .action-btn va-icon {
    font-size: 1.25rem;
  }

  .recent-activity {
    padding: 1.5rem;
  }

  .activity-item {
    padding: 0.75rem;
  }

  .tips-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .tip-card {
    padding: 1.25rem;
  }

  .coming-soon-grid {
    grid-template-columns: 1fr;
  }

  .coming-soon-card {
    padding: 1.5rem 1.25rem;
  }

  .coming-soon-icon {
    width: 56px;
    height: 56px;
    font-size: 1.75rem;
  }

  .coming-soon-card h3 {
    font-size: 1rem;
  }

  .coming-soon-card p {
    font-size: 0.85rem;
  }
}
</style>
