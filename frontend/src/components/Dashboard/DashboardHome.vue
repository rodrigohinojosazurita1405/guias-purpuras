<!-- frontend/src/components/Dashboard/DashboardHome.vue -->
<template>
  <div class="dashboard-home">
    <!-- Header -->
    <div class="dashboard-header">
      <div>
        <h1 class="header-title">Bienvenido, {{ userName }}</h1>
        <p class="header-subtitle">Aquí está tu resumen de actividad</p>
      </div>
      <div class="header-date">
        {{ currentDate }}
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <!-- Card: Trabajos Publicados -->
      <div class="stat-card" @click="goToSection('jobs')">
        <div class="stat-icon jobs">
          <va-icon name="work" />
        </div>
        <div class="stat-content">
          <h3>Trabajos Publicados</h3>
          <div class="stat-number">{{ stats.jobsPublished }}</div>
          <p class="stat-subtitle">{{ stats.jobsActive }} activos</p>
        </div>
        <va-icon name="arrow_forward" class="stat-arrow" />
      </div>

      <!-- Card: Aplicaciones -->
      <div class="stat-card" @click="goToSection('candidates')">
        <div class="stat-icon applications">
          <va-icon name="people" />
        </div>
        <div class="stat-content">
          <h3>Aplicaciones</h3>
          <div class="stat-number">{{ stats.applications }}</div>
          <p class="stat-subtitle">{{ stats.applicationsNew }} nuevas</p>
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

    <!-- Quick Actions -->
    <div class="quick-actions">
      <h2>Acciones Rápidas</h2>
      <div class="actions-grid">
        <button class="action-btn" @click="goToPublish">
          <va-icon name="add_circle" />
          <span>Publicar Trabajo</span>
        </button>
        <button class="action-btn" @click="goToSection('jobs')">
          <va-icon name="folder" />
          <span>Ver Publicaciones</span>
        </button>
        <button class="action-btn" @click="goToSection('candidates')">
          <va-icon name="people" />
          <span>Ver Candidatos</span>
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
            <va-icon :name="getActivityIcon(activity.type)" />
          </div>
          <div class="activity-content">
            <p class="activity-title">{{ activity.title }}</p>
            <p class="activity-time">{{ formatTime(activity.date) }}</p>
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
          <h4>Agrega un logo</h4>
          <p>Las publicaciones con logo reciben 3x más vistas</p>
        </div>
        <div class="tip-card">
          <h4>Descripción clara</h4>
          <p>Describe bien el puesto para atraer mejores candidatos</p>
        </div>
        <div class="tip-card">
          <h4>Responde rápido</h4>
          <p>Los candidatos valoran las respuestas inmediatas</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vuestic-ui'
import { useAuthStore } from '@/stores/useAuthStore'

// ========== COMPOSABLES ==========
const router = useRouter()
const { init: notify } = useToast()
const authStore = useAuthStore()

// ========== DATA ==========
const userName = ref('Usuario')
const currentDate = ref('')

const stats = ref({
  jobsPublished: 0,
  jobsActive: 0,
  applications: 0,
  applicationsNew: 0,
  totalViews: 0,
  profileComplete: false,
  profilePercentage: 0
})

const activities = ref([
  {
    id: 1,
    type: 'job',
    title: 'Cargando actividades...',
    date: new Date()
  }
])

// ========== LIFECYCLE ==========
onMounted(() => {
  initializeDashboard()
  setCurrentDate()
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
      console.log('Nombre del usuario desde authStore:', userName.value)
    } else {
      // Fallback a localStorage
      const storedUser = localStorage.getItem('auth_user')
      if (storedUser) {
        const user = JSON.parse(storedUser)
        userName.value = user.name || 'Usuario'
        console.log('Nombre del usuario desde localStorage:', userName.value)
      }
    }

    // Cargar estadísticas y actividades
    await loadStats()
    await loadActivities()
  } catch (err) {
    console.error('Error inicializando dashboard:', err)
  }
}

const loadStats = async () => {
  try {
    const storedUser = localStorage.getItem('authUser')
    if (!storedUser) {
      console.log('Mostrando estadísticas por defecto (usuario no autenticado aún)')
      // Mostrar valores por defecto mientras se carga
      stats.value = {
        jobsPublished: 0,
        jobsActive: 0,
        applications: 0,
        applicationsNew: 0,
        totalViews: 0,
        profileComplete: false,
        profilePercentage: 0
      }
      return
    }

    const user = JSON.parse(storedUser)
    const email = user.email || ''

    console.log('Intentando cargar estadísticas para:', email)

    // Intentar cargar del endpoint si existe
    try {
      const response = await fetch(
        `http://localhost:8000/api/user/stats?email=${encodeURIComponent(email)}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
          }
        }
      )

      if (response.ok) {
        const data = await response.json()
        if (data.success && data.statistics) {
          stats.value = {
            jobsPublished: data.statistics.jobsPublished || 0,
            jobsActive: data.statistics.jobsActive || 0,
            applications: data.statistics.applications || 0,
            applicationsNew: data.statistics.applicationsNew || 0,
            totalViews: data.statistics.totalViews || 0,
            profileComplete: data.statistics.profileComplete || false,
            profilePercentage: data.statistics.profileComplete ? 100 : 0
          }
        }
      }
    } catch (err) {
      console.log('Endpoint de estadísticas no disponible, usando valores por defecto')
      // Mantener datos por defecto si hay error
    }
  } catch (err) {
    console.error('Error en loadStats:', err)
  }
}

const loadActivities = async () => {
  try {
    const storedUser = localStorage.getItem('authUser')
    if (!storedUser) {
      return
    }

    const user = JSON.parse(storedUser)
    const email = user.email || ''

    const response = await fetch(
      `/api/user/activities?email=${encodeURIComponent(email)}`
    )

    if (!response.ok) {
      throw new Error('Error cargando actividades')
    }

    const data = await response.json()
    if (data.success && data.activities) {
      activities.value = data.activities.map((activity, index) => ({
        id: index + 1,
        type: activity.type || 'job',
        title: activity.title,
        date: new Date(activity.date)
      }))
    }
  } catch (err) {
    console.error('Error cargando actividades:', err)
    // Mantener estado actual si hay error
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

const getActivityIcon = (type) => {
  const icons = {
    job: 'work',
    application: 'people',
    message: 'mail',
    profile: 'person'
  }
  return icons[type] || 'circle'
}

const formatTime = (date) => {
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (hours < 1) return 'Hace poco'
  if (hours < 24) return `Hace ${hours}h`
  if (days === 1) return 'Hace 1 día'
  return `Hace ${days} días`
}

const goToSection = (section) => {
  const routes = {
    jobs: '/dashboard/jobs-manager',
    candidates: '/dashboard/candidates',
    profile: '/dashboard/profile'
  }
  if (routes[section]) {
    router.push(routes[section])
  }
}

const goToPublish = () => {
  router.push('/publicar')
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
}
</style>
