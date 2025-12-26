// frontend/src/stores/useAuthStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE_URL = 'http://localhost:8000/api'

export const useAuthStore = defineStore('auth', () => {
  // ========== STATE ==========
  const user = ref(null)
  const accessToken = ref(null)
  const refreshToken = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const isInitialized = ref(false)  // ¡NUEVO! Flag para rastrear si initAuth() ya se ejecutó

  // ========== GETTERS ==========
  const isAuthenticated = computed(() => {
    const authState = !!user.value && !!accessToken.value
    return authState
  })
  
  const userInitials = computed(() => {
    if (!user.value?.name) return '?'
    const names = user.value.name.split(' ')
    return names.length > 1 
      ? `${names[0][0]}${names[1][0]}`.toUpperCase()
      : names[0][0].toUpperCase()
  })

  // ========== ACTIONS ==========
  
  /**
   * Inicializar auth desde localStorage al cargar la app
   */
  const initAuth = () => {
    // IMPORTANTE: Limpiar las claves de Vue DevTools que pueden interferir
    const devToolsKeys = [
      '__VUE_DEVTOOLS_NEXT_PLUGIN_SETTINGS__dev.esm.pinia__',
      '__vue-devtools-frame-state__',
      '__vue-devtools-theme__'
    ]
    devToolsKeys.forEach(key => {
      localStorage.removeItem(key)
    })

    const storedAccessToken = localStorage.getItem('access_token')
    const storedRefreshToken = localStorage.getItem('refresh_token')
    const storedUser = localStorage.getItem('auth_user')

    // IMPORTANTE: Solo restaurar sesión si AMBOS tokens existen
    // Si solo existe uno, significa logout parcial - limpiar todo
    if (storedAccessToken && storedRefreshToken && storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser)
        // Solo asignar si el parse fue exitoso
        accessToken.value = storedAccessToken
        refreshToken.value = storedRefreshToken
        user.value = parsedUser
      } catch (error) {
        console.error('❌ Error parsing stored user, clearing auth:', error)
        // Si hay error al parsear, limpiar todo
        logout()
      }
    } else {
      // Si faltan datos, asegurar que todo está vacío
      user.value = null
      accessToken.value = null
      refreshToken.value = null
    }

    // ¡IMPORTANTE! Marcar como inicializado
    isInitialized.value = true
  }

  /**
   * Login con email y password
   */
  const login = async (email, password) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.message || 'Error al iniciar sesión')
      }

      // Guardar tokens y usuario en state (incluir role)
      accessToken.value = data.tokens.access
      refreshToken.value = data.tokens.refresh
      user.value = {
        ...data.user,
        role: data.user.role || 'applicant'  // Asegurar que siempre haya un role
      }

      // Guardar en localStorage
      localStorage.setItem('access_token', data.tokens.access)
      localStorage.setItem('refresh_token', data.tokens.refresh)
      localStorage.setItem('auth_user', JSON.stringify(user.value))

      return { success: true }

    } catch (err) {
      error.value = err.message
      console.error('Login error:', err)
      return {
        success: false,
        error: err.message
      }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Registro de nuevo usuario con rol
   */
  const register = async (name, email, password, role = 'applicant') => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, role })
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.message || 'Error al registrarse')
      }

      // Guardar tokens y usuario en state (incluir role)
      accessToken.value = data.tokens.access
      refreshToken.value = data.tokens.refresh
      user.value = {
        ...data.user,
        role: data.user.role || 'applicant'  // Asegurar que siempre haya un role
      }

      // Guardar en localStorage
      localStorage.setItem('access_token', data.tokens.access)
      localStorage.setItem('refresh_token', data.tokens.refresh)
      localStorage.setItem('auth_user', JSON.stringify(user.value))

      return { success: true }

    } catch (err) {
      error.value = err.message
      console.error('Register error:', err)
      return {
        success: false,
        error: err.message
      }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Logout - Limpia estado local INMEDIATAMENTE (SINCRÓNICO)
   */
  const logout = () => {
    // Guardar el refresh token antes de limpiar (para notificar al backend después)
    const oldRefreshToken = refreshToken.value

    // PASO 1: Limpiar PRIMERO el estado reactivo (ANTES de localStorage)
    // Esto previene que Pinia DevTools sincronice el estado de vuelta a localStorage
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    error.value = null
    isLoading.value = false
    isInitialized.value = false  // ¡CRUCIAL! Resetear el flag de inicialización

    // PASO 2: Ahora limpiar localStorage (cuando el estado reactivo ya está vacío)
    const keysToRemove = [
      'access_token',
      'refresh_token',
      'auth_user',
      'authUser',
      'user',
      'rememberMe',
      'userProfileId',
      'token',
      'jwt_token',
      'user_data'
    ]

    keysToRemove.forEach(key => {
      localStorage.removeItem(key)
    })

    // PASO 2a: Limpiar borrador de publicación de trabajo
    localStorage.removeItem('publish_job_draft')
    localStorage.removeItem('publish_current_step')

    // IMPORTANTE: Limpiar las claves de Vue DevTools también
    const devToolsKeys = [
      '__VUE_DEVTOOLS_NEXT_PLUGIN_SETTINGS__dev.esm.pinia__',
      '__vue-devtools-frame-state__',
      '__vue-devtools-theme__'
    ]
    devToolsKeys.forEach(key => {
      if (localStorage.getItem(key)) {
        localStorage.removeItem(key)
      }
    })

    // También limpiar sessionStorage
    sessionStorage.clear()

    // PASO 3: Hacer una limpieza adicional esperando un microtask
    // Esto asegura que Pinia haya procesado todos los cambios de estado
    Promise.resolve().then(() => {
      // Verificar una vez más que localStorage sigue vacío
      const keysToRemove = ['access_token', 'refresh_token', 'auth_user']
      keysToRemove.forEach(key => {
        if (localStorage.getItem(key)) {
          console.warn(`⚠️ [SEGURIDAD] Se detectó ${key} en localStorage, removiendo nuevamente!`)
          localStorage.removeItem(key)
        }
      })
    })

    // PASO 4: Notificar al backend de forma asincrónica (fire-and-forget)
    // Esto NO bloquea el logout local
    if (oldRefreshToken) {
      // Usar setTimeout para que sea verdaderamente asincrónico
      setTimeout(() => {
        fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh: oldRefreshToken })
        })
        .catch(err => {
          console.error('⚠️ Backend logout falló:', err.message)
        })
      }, 0)
    }
  }

  /**
   * Refrescar access token usando el refresh token
   */
  const refreshAccessToken = async () => {
    if (!refreshToken.value) {
      return { success: false, error: 'No refresh token available', shouldLogout: true }
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken.value })
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.message || 'Token expirado')
      }

      // Actualizar tokens (con rotación de refresh token del backend)
      accessToken.value = data.tokens.access
      if (data.tokens.refresh) {
        refreshToken.value = data.tokens.refresh
      }

      // Guardar en localStorage
      localStorage.setItem('access_token', data.tokens.access)
      if (data.tokens.refresh) {
        localStorage.setItem('refresh_token', data.tokens.refresh)
      }

      return { success: true }

    } catch (err) {
      // Si el refresh falla, hacer logout
      logout()
      return {
        success: false,
        error: err.message,
        shouldLogout: true,
        message: 'Por seguridad, su sesión ha sido cerrada. Por favor, inicie sesión nuevamente.'
      }
    }
  }

  /**
   * Actualizar perfil del usuario
   * TODO: Conectar con Django API
   */
  const updateProfile = async (updates) => {
    isLoading.value = true

    try {
      // TODO: API call

      // MOCK
      await new Promise(resolve => setTimeout(resolve, 800))

      user.value = { ...user.value, ...updates }
      localStorage.setItem('auth_user', JSON.stringify(user.value))

      return { success: true }

    } catch (error) {
      console.error('Update profile error:', error)
      return {
        success: false,
        error: 'Error al actualizar perfil.'
      }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Sincronizar foto de perfil desde el backend
   * Útil para actualizar la foto sin cerrar sesión
   */
  const syncProfilePhoto = async () => {
    if (!user.value) return

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: user.value.email,
          // Nota: No podemos hacer login sin password, así que usaremos un endpoint diferente
        })
      })

      // En su lugar, vamos a obtener la foto directamente de los perfiles
      const profilesModule = await import('./useProfileStore')
      const profileStore = profilesModule.useProfileStore()

      if (user.value.role === 'company') {
        const companyModule = await import('./useCompanyStore')
        const companyStore = companyModule.useCompanyStore()
        const result = await companyStore.getMyCompany()

        if (result.success && result.company?.logo) {
          user.value.profilePhoto = result.company.logo
          localStorage.setItem('auth_user', JSON.stringify(user.value))
        }
      } else {
        const result = await profileStore.getProfileByEmail(user.value.email)

        if (result.success && result.profile?.profilePhoto) {
          user.value.profilePhoto = result.profile.profilePhoto
          localStorage.setItem('auth_user', JSON.stringify(user.value))
        }
      }
    } catch (err) {
      console.error('Error sincronizando foto de perfil:', err)
    }
  }

  // NO inicializar aquí - se llamará manualmente desde main.js
  // initAuth()

  return {
    // State
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    isInitialized,  // ¡NUEVO! Exportar el flag

    // Getters
    isAuthenticated,
    userInitials,

    // Actions
    login,
    register,
    logout,
    refreshAccessToken,
    updateProfile,
    syncProfilePhoto,
    initAuth
  }
})