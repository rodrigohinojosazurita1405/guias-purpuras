import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'

/**
 * Composable para gestionar estadísticas del dashboard de forma agnóstica
 * Soporta múltiples tipos de guías (trabajos, negocios, restaurantes, profesionales)
 */
export function useDashboardStats() {
  const authStore = useAuthStore()

  // ========== DATA ==========
  const stats = ref({
    totalPublished: 0,
    activeListings: 0,
    totalApplications: 0,
    newApplications: 0,
    totalViews: 0,
    profileComplete: false,
    profilePercentage: 0
  })

  const isLoading = ref(false)
  const error = ref(null)

  // ========== COMPUTED ==========
  const statsLabels = computed(() => {
    // Los labels se adaptan según el contexto
    // Por ahora, labels genéricos que funcionan para cualquier guía
    return {
      totalPublished: 'Publicaciones',
      activeListings: 'Activas',
      totalApplications: 'Interacciones',
      newApplications: 'Nuevas',
      totalViews: 'Vistas',
      profileComplete: 'Perfil'
    }
  })

  // ========== METHODS ==========
  /**
   * Cargar estadísticas desde la API
   * Soporta parámetro opcional de tipo de guía para futuras extensiones
   */
  const loadStats = async (guideType = null) => {
    isLoading.value = true
    error.value = null

    try {
      const email = authStore.user?.email
      const accessToken = authStore.accessToken || localStorage.getItem('access_token')

      // Si no hay autenticación real, usar dummy stats inmediatamente
      if (!email || !accessToken) {
        console.log('Sin autenticación, usando estadísticas dummy realistas (OPCIÓN A)')
        setDummyStats()
        return
      }

      // Intentar cargar del endpoint de estadísticas (OPCIÓN A: Si falla, usar dummy)
      try {
        const params = new URLSearchParams()
        params.append('email', email)
        if (guideType) {
          params.append('guide_type', guideType)
        }

        console.log('📊 [DashboardStats] Cargando estadísticas para:', email)
        console.log('📊 [DashboardStats] URL:', `/api/user/stats?${params.toString()}`)

        const response = await fetch(
          `/api/user/stats?${params.toString()}`,
          {
            headers: {
              'Authorization': `Bearer ${accessToken}`,
              'Content-Type': 'application/json'
            },
            signal: AbortSignal.timeout(10000) // 10 segundos timeout
          }
        )

        console.log('📊 [DashboardStats] Response status:', response.status)

        if (response.ok) {
          const data = await response.json()
          console.log('📊 [DashboardStats] Data recibida:', data)

          if (data.success && data.statistics) {
            // Mapear datos del backend a nuestro formato genérico
            stats.value = {
              totalPublished: data.statistics.totalPublished || data.statistics.jobsPublished || 0,
              activeListings: data.statistics.activeListings || data.statistics.jobsActive || 0,
              totalApplications: data.statistics.totalApplications || data.statistics.applications || 0,
              newApplications: data.statistics.newApplications || data.statistics.applicationsNew || 0,
              totalViews: data.statistics.totalViews || 0,
              profileComplete: data.statistics.profileComplete || false,
              profilePercentage: data.statistics.profilePercentage || (data.statistics.profileComplete ? 100 : 0)
            }
            console.log('✅ [DashboardStats] Estadísticas actualizadas:', JSON.parse(JSON.stringify(stats.value)))
            return
          }
        } else {
          const errorData = await response.json()
          console.error('❌ [DashboardStats] Error del servidor:', errorData)
        }
      } catch (fetchErr) {
        console.error('❌ [DashboardStats] Error en fetch:', fetchErr.message, fetchErr)
      }

      // OPCIÓN A: Si falla la API, usar estadísticas dummy realistas
      setDummyStats()
    } catch (err) {
      console.error('Error cargando estadísticas:', err)
      error.value = err.message
      setDummyStats()
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Establecer estadísticas dummy realistas (OPCIÓN A)
   */
  const setDummyStats = () => {
    stats.value = {
      totalPublished: 3,
      activeListings: 2,
      totalApplications: 12,
      newApplications: 3,
      totalViews: 124,
      profileComplete: true,
      profilePercentage: 85
    }
  }

  /**
   * Resetear estadísticas a valores por defecto
   */
  const resetStats = () => {
    stats.value = {
      totalPublished: 0,
      activeListings: 0,
      totalApplications: 0,
      newApplications: 0,
      totalViews: 0,
      profileComplete: false,
      profilePercentage: 0
    }
  }

  /**
   * Actualizar una estadística específica
   */
  const updateStat = (key, value) => {
    if (key in stats.value) {
      stats.value[key] = value
    }
  }

  /**
   * Incrementar una estadística
   */
  const incrementStat = (key, amount = 1) => {
    if (typeof stats.value[key] === 'number') {
      stats.value[key] += amount
    }
  }

  return {
    stats,
    statsLabels,
    isLoading,
    error,
    loadStats,
    resetStats,
    updateStat,
    incrementStat,
    setDummyStats
  }
}
