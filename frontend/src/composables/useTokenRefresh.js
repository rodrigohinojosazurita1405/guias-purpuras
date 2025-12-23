/**
 * Composable para manejar el refresh automático de tokens JWT
 * Basado en mejores prácticas de la industria:
 * - Refresh proactivo antes de expiración
 * - Manejo de sesión al cerrar navegador
 * - Detección de inactividad del usuario
 */

import { onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'

// Configuración de tiempos (en milisegundos)
const CONFIG = {
  // Access token expira en 15min, refrescar a los 12min (3min antes)
  TOKEN_REFRESH_INTERVAL: 12 * 60 * 1000, // 12 minutos

  // Tiempo de inactividad antes de cerrar sesión (30 minutos)
  INACTIVITY_TIMEOUT: 30 * 60 * 1000, // 30 minutos

  // Tiempo antes de expiración para mostrar advertencia (2 minutos)
  WARNING_TIME: 2 * 60 * 1000 // 2 minutos
}

export function useTokenRefresh() {
  const authStore = useAuthStore()

  let refreshIntervalId = null
  let inactivityTimeoutId = null
  let lastActivityTime = Date.now()

  /**
   * Refrescar token automáticamente
   */
  const autoRefreshToken = async () => {
    if (!authStore.isAuthenticated) {
      return
    }

    const result = await authStore.refreshAccessToken()

    if (!result.success) {
      stopTokenRefresh()
    }
  }

  /**
   * Iniciar el timer de refresh automático
   */
  const startTokenRefresh = () => {
    if (!authStore.isAuthenticated) {
      return
    }

    // Limpiar cualquier intervalo previo
    if (refreshIntervalId) {
      clearInterval(refreshIntervalId)
    }

    // Configurar nuevo intervalo
    refreshIntervalId = setInterval(autoRefreshToken, CONFIG.TOKEN_REFRESH_INTERVAL)
  }

  /**
   * Detener el timer de refresh automático
   */
  const stopTokenRefresh = () => {
    if (refreshIntervalId) {
      clearInterval(refreshIntervalId)
      refreshIntervalId = null
    }
  }

  /**
   * Reiniciar el timer de inactividad
   */
  const resetInactivityTimeout = () => {
    lastActivityTime = Date.now()

    // Limpiar timeout previo
    if (inactivityTimeoutId) {
      clearTimeout(inactivityTimeoutId)
    }

    // Configurar nuevo timeout
    inactivityTimeoutId = setTimeout(() => {
      authStore.logout()

      // Mostrar notificación
      if (window.vaToast) {
        window.vaToast.init({
          message: 'Por seguridad, su sesión ha sido cerrada debido a inactividad.',
          color: 'warning',
          duration: 5000,
          position: 'top-right',
          icon: 'info'
        })
      }
    }, CONFIG.INACTIVITY_TIMEOUT)
  }

  /**
   * Manejar eventos de actividad del usuario
   */
  const handleUserActivity = () => {
    if (!authStore.isAuthenticated) return
    resetInactivityTimeout()
  }

  /**
   * Detectar cuando el navegador se cierra/recarga
   */
  const handleBeforeUnload = (event) => {
    // No hacer nada aquí - permitir que el sessionStorage se limpie naturalmente
    // Los tokens en localStorage persistirán para sesiones futuras
  }

  /**
   * Detectar cuando la pestaña se oculta (cambio de pestaña o minimizar)
   */
  const handleVisibilityChange = () => {
    if (!document.hidden) {
      // Cuando el usuario vuelve, verificar si el token necesita refresh
      if (authStore.isAuthenticated) {
        const timeSinceActivity = Date.now() - lastActivityTime
        // Si ha pasado más de la mitad del tiempo de refresh, hacer refresh inmediato
        if (timeSinceActivity > CONFIG.TOKEN_REFRESH_INTERVAL / 2) {
          autoRefreshToken()
        }
      }
    }
  }

  /**
   * Inicializar el sistema de refresh automático
   */
  const init = () => {
    if (!authStore.isAuthenticated) {
      return
    }

    // Iniciar auto-refresh periódico
    startTokenRefresh()

    // Iniciar detección de inactividad
    resetInactivityTimeout()

    // Escuchar eventos de actividad del usuario
    const activityEvents = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click']
    activityEvents.forEach(event => {
      window.addEventListener(event, handleUserActivity, { passive: true })
    })

    // Escuchar cambios de visibilidad de pestaña
    document.addEventListener('visibilitychange', handleVisibilityChange)

    // Escuchar cierre de navegador (cleanup)
    window.addEventListener('beforeunload', handleBeforeUnload)
  }

  /**
   * Limpiar todos los listeners y timers
   */
  const cleanup = () => {
    // Detener timers
    stopTokenRefresh()
    if (inactivityTimeoutId) {
      clearTimeout(inactivityTimeoutId)
    }

    // Remover event listeners
    const activityEvents = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click']
    activityEvents.forEach(event => {
      window.removeEventListener(event, handleUserActivity)
    })

    document.removeEventListener('visibilitychange', handleVisibilityChange)
    window.removeEventListener('beforeunload', handleBeforeUnload)
  }

  // Lifecycle hooks
  onMounted(() => {
    init()
  })

  onUnmounted(() => {
    cleanup()
  })

  return {
    init,
    cleanup,
    startTokenRefresh,
    stopTokenRefresh,
    resetInactivityTimeout
  }
}
