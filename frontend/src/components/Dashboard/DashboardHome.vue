<!-- frontend/src/components/Dashboard/DashboardHome.vue -->
<template>
  <div class="dashboard-home">
    <!-- Header -->
    <div class="dashboard-header">
      <div>
        <h1 class="header-title">{{ greeting }}, {{ userName }}</h1>
        <p class="header-subtitle">Aquí está tu resumen de actividad</p>
      </div>
      <div class="header-date">
        {{ currentDate }}
      </div>
    </div>

    <!-- Stats Grid - EMPRESA -->
    <div v-if="authStore.user?.role === 'company'" class="stats-grid">
      <!-- Card: Publicaciones -->
      <div class="stat-card" @click="goToSection('jobs')">
        <div class="stat-icon jobs">
          <va-icon name="list_alt" />
        </div>
        <div class="stat-content">
          <h3>Publicaciones</h3>
          <div class="stat-number">{{ stats.totalPublished }}</div>
          <p class="stat-subtitle">{{ stats.activeListings }} activas</p>
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Interacciones -->
      <div class="stat-card" @click="goToSection('candidates')">
        <div class="stat-icon applications">
          <va-icon name="people" />
        </div>
        <div class="stat-content">
          <h3>Interacciones</h3>
          <div class="stat-number">{{ stats.totalApplications }}</div>
          <p class="stat-subtitle">{{ stats.newApplications }} nuevas</p>
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Vistas -->
      <div class="stat-card">
        <div class="stat-icon views">
          <va-icon name="visibility" />
        </div>
        <div class="stat-content">
          <h3>Vistas Totales</h3>
          <div class="stat-number">{{ stats.totalViews }}</div>
          <p class="stat-subtitle">Esta semana</p>
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Perfil Completado -->
      <div class="stat-card" :class="{ incomplete: !stats.profileComplete }">
        <div class="stat-icon profile" :class="{ incomplete: !stats.profileComplete }">
          <va-icon :name="stats.profileComplete ? 'check_circle' : 'person'" />
        </div>
        <div class="stat-content">
          <h3>Perfil</h3>
          <div class="stat-number">{{ stats.profilePercentage }}%</div>
          <p class="stat-subtitle" v-if="!stats.profileComplete">Completa tu perfil</p>
          <p class="stat-subtitle" v-else>Perfil completo</p>
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>
    </div>

    <!-- Stats Grid - POSTULANTE -->
    <div v-else-if="authStore.user?.role === 'applicant'" class="stats-grid">
      <!-- Card: Mis Postulaciones -->
      <div class="stat-card" @click="goToSection('applications')">
        <div class="stat-icon applications">
          <va-icon name="assignment" />
        </div>
        <div class="stat-content">
          <h3>Mis Postulaciones</h3>
          <div class="stat-number">{{ stats.totalApplications }}</div>
          <p class="stat-subtitle">{{ stats.pendingApplications }} pendientes</p>
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Favoritos -->
      <div class="stat-card" @click="goToSection('shortlisted')">
        <div class="stat-icon views">
          <va-icon name="bookmark" />
        </div>
        <div class="stat-content">
          <h3>Favoritos</h3>
          <div class="stat-number">{{ stats.savedJobs }}</div>
          <p class="stat-subtitle">Anuncios guardados</p>
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Perfil Completado -->
      <div class="stat-card" :class="{ incomplete: !stats.profileComplete }">
        <div class="stat-icon profile" :class="{ incomplete: !stats.profileComplete }">
          <va-icon :name="stats.profileComplete ? 'check_circle' : 'person'" />
        </div>
        <div class="stat-content">
          <h3>Perfil</h3>
          <div class="stat-number">{{ stats.profilePercentage }}%</div>
          <p class="stat-subtitle" v-if="!stats.profileComplete">Completa tu perfil</p>
          <p class="stat-subtitle" v-else>Perfil completo</p>
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: CV -->
      <div class="stat-card" @click="goToSection('cv')">
        <div class="stat-icon jobs">
          <va-icon name="description" />
        </div>
        <div class="stat-content">
          <h3>Mi CV</h3>
          <div class="stat-number">{{ stats.cvCount }}</div>
          <p class="stat-subtitle">CV creados</p>
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>
    </div>

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

    <!-- Recent Activity -->
    <div class="recent-activity">
      <h2>Actividad Reciente</h2>
      <div v-if="activities.length > 0" class="activity-list">
        <div v-for="activity in activities.slice(0, 5)" :key="activity.id" class="activity-item">
          <div class="activity-icon" :class="activity.type">
            <va-icon :name="dashboardActivities.getActivityIcon(activity.type)" />
          </div>
          <div class="activity-content">
            <p class="activity-title">{{ activity.title }}</p>
            <p class="activity-time">{{ dashboardActivities.formatTime(activity.date) }}</p>
          </div>
        </div>
      </div>
      <div v-else class="empty-state">
        <va-icon name="history" size="2rem" />
        <p>No hay actividad aún</p>
      </div>
    </div>

    <!-- Tips Section -->
    <div class="tips-section">
      <h2>Consejos</h2>
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
          <p>Los usuarios valoran las respuestas inmediatas</p>
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
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import { useAuthStore } from '@/stores/useAuthStore'
import { useDashboardStats } from '@/composables/useDashboardStats'
import { useDashboardActivities } from '@/composables/useDashboardActivities'

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
  profilePercentage: 0
})

const activities = ref([])

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
    console.log('Nombre actualizado en DashboardHome:', newName)
  }
})

// ========== METHODS ==========
const initializeDashboard = async () => {
  try {
    // Obtener nombre del usuario desde authStore (tiene prioridad)
    if (authStore.user?.name) {
      userName.value = authStore.user.name
    } else {
      // Fallback a localStorage
      const storedUser = localStorage.getItem('auth_user')
      if (storedUser) {
        const user = JSON.parse(storedUser)
        userName.value = user.name || 'Usuario'
      }
    }

    // Cargar estadísticas
    await dashboardStats.loadStats()
    console.log('📊 [DashboardHome] Stats después de loadStats:', JSON.parse(JSON.stringify(dashboardStats.stats.value)))
    // Copiar datos a nuestra variable local reactiva
    stats.value = { ...dashboardStats.stats.value }

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
    cv: '/dashboard/cv'
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
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #E4E7EC;
}

.header-title {
  margin: 0 0 0.5rem;
  font-size: 2rem;
  font-weight: 700;
  color: #1F2937;
  letter-spacing: -0.5px;
}

.header-subtitle {
  margin: 0;
  font-size: 0.95rem;
  color: #6B7280;
  font-weight: 500;
}

.header-date {
  font-size: 0.95rem;
  color: #9CA3AF;
  font-weight: 500;
  white-space: nowrap;
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
