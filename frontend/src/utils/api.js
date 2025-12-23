/**
 * API utility for making authenticated requests
 * Automatically adds JWT token to request headers
 * Maneja refresh automático de tokens y sesiones expiradas
 */

import { useAuthStore } from '@/stores/useAuthStore'
import { useRouter } from 'vue-router'

const API_BASE_URL = 'http://localhost:8000/api'

// Flag para evitar múltiples refreshes simultáneos
let isRefreshing = false
let refreshPromise = null

/**
 * Get the current access token from the auth store
 */
const getAccessToken = () => {
  const authStore = useAuthStore()
  return authStore.accessToken
}

/**
 * Mostrar notificación de sesión expirada
 */
const showSessionExpiredNotification = () => {
  // Usar Vuestic Notification si está disponible
  if (window.vaToast) {
    window.vaToast.init({
      message: 'Por seguridad, su sesión ha sido cerrada. Por favor, inicie sesión nuevamente.',
      color: 'warning',
      duration: 5000,
      position: 'top-right',
      icon: 'warning'
    })
  } else {
    // Fallback a alert si no está disponible
    alert('Por seguridad, su sesión ha sido cerrada. Por favor, inicie sesión nuevamente.')
  }
}

/**
 * Fetch wrapper que automáticamente agrega authorization header
 * y maneja el refresh de tokens expirados
 */
export const apiCall = async (endpoint, options = {}) => {
  const token = getAccessToken()

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }

  // Agregar authorization header si existe token
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      ...options,
      headers
    })

    // Si el token expiró (401), intentar refrescarlo
    if (response.status === 401 && token) {
      // Si ya hay un refresh en curso, esperar a que termine
      if (isRefreshing && refreshPromise) {
        await refreshPromise
      } else {
        // Iniciar nuevo refresh
        isRefreshing = true
        const authStore = useAuthStore()

        refreshPromise = authStore.refreshAccessToken()
        const refreshResult = await refreshPromise

        isRefreshing = false
        refreshPromise = null

        if (refreshResult.success) {
          // Reintentar el request original con el nuevo token
          const newToken = authStore.accessToken
          headers.Authorization = `Bearer ${newToken}`

          return fetch(url, {
            ...options,
            headers
          })
        } else {
          // Refresh falló, mostrar mensaje y redirigir a login
          showSessionExpiredNotification()

          // Redirigir a login después de un breve delay
          setTimeout(() => {
            const router = useRouter()
            router.push('/login')
          }, 1000)

          throw new Error(refreshResult.message || 'Por seguridad, su sesión ha sido cerrada.')
        }
      }
    }

    return response
  } catch (error) {
    console.error('API call error:', error)
    throw error
  }
}

/**
 * Helper functions for common HTTP methods
 */

export const get = (endpoint, options = {}) => {
  return apiCall(endpoint, { ...options, method: 'GET' })
}

export const post = (endpoint, data, options = {}) => {
  return apiCall(endpoint, {
    ...options,
    method: 'POST',
    body: JSON.stringify(data)
  })
}

export const patch = (endpoint, data, options = {}) => {
  return apiCall(endpoint, {
    ...options,
    method: 'PATCH',
    body: JSON.stringify(data)
  })
}

export const put = (endpoint, data, options = {}) => {
  return apiCall(endpoint, {
    ...options,
    method: 'PUT',
    body: JSON.stringify(data)
  })
}

export const del = (endpoint, options = {}) => {
  return apiCall(endpoint, { ...options, method: 'DELETE' })
}

export default {
  apiCall,
  get,
  post,
  patch,
  put,
  del
}
