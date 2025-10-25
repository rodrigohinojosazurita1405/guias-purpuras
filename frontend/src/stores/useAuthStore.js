// frontend/src/stores/useAuthStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // ========== STATE ==========
  const user = ref(null)
  const token = ref(null)
  const isLoading = ref(false)

  // ========== GETTERS ==========
  const isAuthenticated = computed(() => !!user.value && !!token.value)
  
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
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('auth_user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      try {
        user.value = JSON.parse(storedUser)
      } catch (error) {
        console.error('Error parsing stored user:', error)
        logout()
      }
    }
  }

  /**
   * Login con email y password
   * TODO: Conectar con Django API
   */
  const login = async (email, password) => {
    isLoading.value = true
    
    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/auth/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ email, password })
      // })
      // const data = await response.json()
      
      // MOCK - Simular respuesta del backend
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const mockUser = {
        id: 1,
        name: 'Juan Pérez',
        email: email,
        phone: '+591 70123456',
        defaultCity: 'cochabamba',
        defaultAddress: 'Av. Heroínas #123, Zona Central',
        avatar: null
      }
      
      const mockToken = 'mock_jwt_token_12345'
      
      // Guardar en state
      user.value = mockUser
      token.value = mockToken
      
      // Guardar en localStorage
      localStorage.setItem('auth_token', mockToken)
      localStorage.setItem('auth_user', JSON.stringify(mockUser))
      
      return { success: true }
      
    } catch (error) {
      console.error('Login error:', error)
      return { 
        success: false, 
        error: 'Error al iniciar sesión. Verifica tus credenciales.' 
      }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Registro de nuevo usuario
   * TODO: Conectar con Django API
   */
  const register = async (name, email, password, phone = null) => {
    isLoading.value = true
    
    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/auth/register', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ name, email, password, phone })
      // })
      // const data = await response.json()
      
      // MOCK - Simular respuesta del backend
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      const mockUser = {
        id: Date.now(),
        name: name,
        email: email,
        phone: phone || null,
        defaultCity: null,
        defaultAddress: null,
        avatar: null
      }
      
      const mockToken = `mock_jwt_token_${Date.now()}`
      
      // Guardar en state
      user.value = mockUser
      token.value = mockToken
      
      // Guardar en localStorage
      localStorage.setItem('auth_token', mockToken)
      localStorage.setItem('auth_user', JSON.stringify(mockUser))
      
      return { success: true }
      
    } catch (error) {
      console.error('Register error:', error)
      return { 
        success: false, 
        error: 'Error al registrarse. Intenta nuevamente.' 
      }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Logout
   */
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
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

  // Inicializar al cargar el store
  initAuth()

  return {
    // State
    user,
    token,
    isLoading,
    
    // Getters
    isAuthenticated,
    userInitials,
    
    // Actions
    login,
    register,
    logout,
    updateProfile
  }
})