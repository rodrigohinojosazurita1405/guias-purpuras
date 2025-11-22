import { ref } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'

/**
 * Composable para gestionar actividades del dashboard
 * Soporta múltiples tipos de eventos y actividades
 */
export function useDashboardActivities() {
  const authStore = useAuthStore()

  // ========== DATA ==========
  const activities = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  // ========== ACTIVITY TYPE ICONS ==========
  const activityIcons = {
    job: 'work',
    application: 'people',
    message: 'mail',
    profile: 'person',
    business: 'business',
    review: 'star',
    listing: 'list_alt',
    view: 'visibility',
    saved: 'bookmark'
  }

  // ========== ACTIVITY COLORS ==========
  const activityColors = {
    job: 'var(--color-purple)',
    application: '#3B82F6',
    message: '#F59E0B',
    profile: '#10B981',
    business: '#8B5CF6',
    review: '#EC4899',
    listing: '#06B6D4',
    view: '#F59E0B',
    saved: '#EC4899'
  }

  // ========== METHODS ==========
  /**
   * Cargar actividades desde la API
   */
  const loadActivities = async (limit = 5, guideType = null) => {
    isLoading.value = true
    error.value = null

    try {
      const userEmail = authStore.user?.email
      const accessToken = authStore.accessToken || localStorage.getItem('access_token')

      // Si no hay usuario autenticado, usar dummy activities inmediatamente
      if (!userEmail || !accessToken) {
        console.log('Sin autenticación, usando actividades dummy realistas (OPCIÓN A)')
        setDummyActivities(limit)
        return
      }

      const params = new URLSearchParams()
      params.append('email', userEmail)
      params.append('limit', limit)
      if (guideType) {
        params.append('guide_type', guideType)
      }

      // Intentar cargar del endpoint con timeout
      try {
        const response = await fetch(`http://localhost:8000/api/user/activities?${params.toString()}`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          },
          signal: AbortSignal.timeout(5000) // 5 segundo timeout
        })

        if (response.ok) {
          const data = await response.json()
          if (data.success && Array.isArray(data.activities)) {
            activities.value = data.activities.map((activity, index) => ({
              id: activity.id || index + 1,
              type: activity.type || 'listing',
              title: activity.title,
              description: activity.description || '',
              date: new Date(activity.date || new Date()),
              metadata: activity.metadata || {}
            }))
            return
          }
        }
      } catch (fetchErr) {
        console.log('Endpoint de actividades no disponible, usando datos dummy:', fetchErr.message)
      }

      // OPCIÓN A: Si falla la API, usar actividades dummy
      setDummyActivities(limit)
    } catch (err) {
      console.error('Error cargando actividades:', err)
      error.value = err.message
      setDummyActivities(limit)
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Establecer actividades dummy realistas (OPCIÓN A)
   */
  const setDummyActivities = (limit = 5) => {
    const dummyData = [
      {
        id: 1,
        type: 'job',
        title: 'Publicación creada: Desarrollador Frontend',
        description: 'Se publicó una nueva oferta de empleo',
        date: new Date(Date.now() - 2 * 60 * 60 * 1000), // Hace 2 horas
        metadata: {}
      },
      {
        id: 2,
        type: 'application',
        title: 'Nueva aplicación recibida',
        description: 'Juan Pérez aplicó a tu publicación',
        date: new Date(Date.now() - 5 * 60 * 60 * 1000), // Hace 5 horas
        metadata: {}
      },
      {
        id: 3,
        type: 'profile',
        title: 'Perfil actualizado',
        description: 'Se actualizó tu información de usuario',
        date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // Hace 1 día
        metadata: {}
      },
      {
        id: 4,
        type: 'view',
        title: 'Tu publicación fue vista',
        description: '5 usuarios vieron tu anuncio de desarrollador',
        date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // Hace 2 días
        metadata: {}
      },
      {
        id: 5,
        type: 'message',
        title: 'Nuevo mensaje recibido',
        description: 'María González te envió un mensaje',
        date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // Hace 3 días
        metadata: {}
      }
    ]

    activities.value = dummyData.slice(0, limit)
  }

  /**
   * Agregar una actividad nueva (uso interno)
   */
  const addActivity = (activity) => {
    const newActivity = {
      id: activities.value.length + 1,
      type: activity.type || 'listing',
      title: activity.title,
      description: activity.description || '',
      date: new Date(),
      metadata: activity.metadata || {}
    }
    activities.value.unshift(newActivity)
  }

  /**
   * Obtener el icono para un tipo de actividad
   */
  const getActivityIcon = (type) => {
    return activityIcons[type] || 'circle'
  }

  /**
   * Obtener el color para un tipo de actividad
   */
  const getActivityColor = (type) => {
    return activityColors[type] || '#6B7280'
  }

  /**
   * Formatear tiempo relativo
   */
  const formatTime = (date) => {
    const now = new Date()
    const diff = now - date

    const minutes = Math.floor(diff / (1000 * 60))
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))

    if (minutes < 1) return 'Hace poco'
    if (minutes < 60) return `Hace ${minutes}m`
    if (hours < 24) return `Hace ${hours}h`
    if (days === 1) return 'Hace 1 día'
    if (days < 30) return `Hace ${days}d`

    const months = Math.floor(days / 30)
    if (months < 12) return `Hace ${months}m`

    return 'Hace más de un año'
  }

  /**
   * Resetear actividades
   */
  const resetActivities = () => {
    activities.value = []
  }

  /**
   * Limpiar actividad por ID
   */
  const removeActivity = (id) => {
    activities.value = activities.value.filter(a => a.id !== id)
  }

  return {
    activities,
    isLoading,
    error,
    activityIcons,
    activityColors,
    loadActivities,
    addActivity,
    getActivityIcon,
    getActivityColor,
    formatTime,
    resetActivities,
    removeActivity,
    setDummyActivities
  }
}
