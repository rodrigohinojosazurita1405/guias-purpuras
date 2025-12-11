import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './useAuthStore'

const API_BASE = 'http://localhost:8000/api'

export const useProfileStore = defineStore('profile', () => {
  // ========== STATE ==========
  const userProfile = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const successMessage = ref(null)

  // ========== COMPUTED ==========
  const isProfileComplete = computed(() => {
    return userProfile.value &&
           userProfile.value.fullName &&
           userProfile.value.email
  })

  const profileProgress = computed(() => {
    if (!userProfile.value) return 0

    const fields = [
      'fullName',
      'email',
      'phone',
      'location',
      'bio',
      'profilePhoto'
    ]

    const filledFields = fields.filter(field =>
      userProfile.value[field] && userProfile.value[field] !== ''
    ).length

    return Math.round((filledFields / fields.length) * 100)
  })

  // ========== METHODS ==========

  /**
   * Crear un nuevo perfil de usuario
   */
  const createProfile = async (profileData) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const response = await fetch(`${API_BASE}/profiles/user/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(profileData)
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al crear el perfil')
      }

      userProfile.value = data.profile
      successMessage.value = data.message

      return { success: true, profile: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Obtener perfil de usuario por email
   */
  const getProfileByEmail = async (email) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}/profiles/user/email/${email}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Perfil no encontrado')
      }

      userProfile.value = data.profile
      return { success: true, profile: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Obtener perfil de usuario por ID
   */
  const getProfileById = async (userId) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}/profiles/user/${userId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Perfil no encontrado')
      }

      userProfile.value = data.profile
      return { success: true, profile: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Actualizar perfil de usuario
   */
  const updateProfile = async (userId, updatedData) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const response = await fetch(`${API_BASE}/profiles/user/${userId}/edit`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al actualizar el perfil')
      }

      // Actualizar el perfil local
      userProfile.value = {
        ...userProfile.value,
        ...data.profile
      }

      successMessage.value = data.message
      return { success: true, profile: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Limpiar estado
   */
  const clearProfile = () => {
    userProfile.value = null
    error.value = null
    successMessage.value = null
  }

  /**
   * Cargar foto de perfil de usuario
   */
  const uploadProfilePhoto = async (userId, photoFile) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const formData = new FormData()
      formData.append('photo', photoFile)

      // Obtener token JWT del auth store
      const authStore = useAuthStore()
      const jwtToken = authStore.accessToken

      if (!jwtToken) {
        throw new Error('No hay token de autenticación disponible')
      }

      const uploadUrl = `${API_BASE}/profiles/user/${userId}/photo`

      const response = await fetch(uploadUrl, {
        method: 'PATCH',
        body: formData,
        headers: {
          'Authorization': `Bearer ${jwtToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al cargar la foto')
      }

      // Actualizar el perfil local
      userProfile.value = {
        ...userProfile.value,
        ...data.profile
      }

      // 🆕 Actualizar también el authStore con la nueva foto
      if (authStore.user && data.profile.profilePhoto) {
        authStore.user.profilePhoto = data.profile.profilePhoto
        // Actualizar localStorage también
        localStorage.setItem('auth_user', JSON.stringify(authStore.user))
      }

      successMessage.value = data.message
      return { success: true, profile: data.profile }
    } catch (err) {
      console.error('Error during photo upload:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Eliminar foto de perfil de usuario
   */
  const deleteProfilePhoto = async (userId) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      // Obtener token JWT del auth store
      const authStore = useAuthStore()
      const jwtToken = authStore.accessToken

      if (!jwtToken) {
        throw new Error('No hay token de autenticación disponible')
      }

      const deleteUrl = `${API_BASE}/profiles/user/${userId}/photo/delete`

      const response = await fetch(deleteUrl, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${jwtToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al eliminar la foto')
      }

      // Actualizar el perfil local
      userProfile.value = {
        ...userProfile.value,
        ...data.profile
      }

      // 🆕 Actualizar también el authStore eliminando la foto
      if (authStore.user) {
        authStore.user.profilePhoto = null
        // Actualizar localStorage también
        localStorage.setItem('auth_user', JSON.stringify(authStore.user))
      }

      successMessage.value = data.message
      return { success: true, profile: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Limpiar mensajes
   */
  const clearMessages = () => {
    error.value = null
    successMessage.value = null
  }

  return {
    // State
    userProfile,
    isLoading,
    error,
    successMessage,

    // Computed
    isProfileComplete,
    profileProgress,

    // Methods
    createProfile,
    getProfileByEmail,
    getProfileById,
    updateProfile,
    uploadProfilePhoto,
    deleteProfilePhoto,
    clearProfile,
    clearMessages
  }
})
