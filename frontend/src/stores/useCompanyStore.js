import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './useAuthStore'

const API_BASE = 'http://localhost:8000/api'

export const useCompanyStore = defineStore('company', () => {
  // ========== STATE ==========
  const companies = ref([])
  const currentCompany = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const successMessage = ref(null)

  // ========== METHODS ==========

  /**
   * Obtener empresa del usuario autenticado
   */
  const getMyCompany = async () => {
    isLoading.value = true
    error.value = null

    try {
      const authStore = useAuthStore()
      const response = await fetch(`${API_BASE}/profiles/company/me/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al cargar empresa')
      }

      currentCompany.value = data.company
      return { success: true, company: data.company }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Obtener empresa por ID
   */
  const getCompanyById = async (companyId) => {
    isLoading.value = true
    error.value = null

    try {
      const authStore = useAuthStore()
      const response = await fetch(`${API_BASE}/profiles/company/${companyId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Empresa no encontrada')
      }

      currentCompany.value = data.profile
      return { success: true, company: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Crear nueva empresa
   */
  const createCompany = async (companyData, userProfileId, files = {}) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const authStore = useAuthStore()
      const formData = new FormData()

      // Agregar datos de texto
      Object.keys(companyData).forEach(key => {
        if (companyData[key] !== null && companyData[key] !== undefined) {
          formData.append(key, companyData[key])
        }
      })

      // Agregar userProfileId
      formData.append('userProfileId', userProfileId)

      // Agregar archivos
      if (files.logo) {
        formData.append('logo', files.logo)
      }
      if (files.banner) {
        formData.append('banner', files.banner)
      }

      const response = await fetch(`${API_BASE}/profiles/company/create`, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al crear empresa')
      }

      currentCompany.value = data.profile
      successMessage.value = data.message
      return { success: true, company: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Actualizar empresa - SOLO DATOS (JSON)
   * Para archivos, usar updateCompanyWithFiles
   */
  const updateCompany = async (companyId, companyData) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const authStore = useAuthStore()

      const response = await fetch(`${API_BASE}/profiles/company/${companyId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        },
        body: JSON.stringify(companyData)
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al actualizar empresa')
      }

      currentCompany.value = data.profile
      successMessage.value = data.message
      return { success: true, company: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Actualizar empresa con archivos (logo/banner)
   */
  const updateCompanyWithFiles = async (companyId, companyData, files = {}) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const authStore = useAuthStore()
      const formData = new FormData()

      // Agregar datos de texto
      Object.keys(companyData).forEach(key => {
        if (companyData[key] !== null && companyData[key] !== undefined) {
          formData.append(key, companyData[key])
        }
      })

      // Agregar archivos (solo si existen)
      if (files && files.logo) {
        console.log('[DEBUG] Adding logo to FormData:', files.logo.name)
        formData.append('logo', files.logo)
      }
      if (files && files.banner) {
        console.log('[DEBUG] Adding banner to FormData:', files.banner.name)
        formData.append('banner', files.banner)
      }

      console.log('[DEBUG] FormData entries:')
      for (let [key, value] of formData.entries()) {
        console.log(`  ${key}: ${value instanceof File ? value.name : value}`)
      }

      const response = await fetch(`${API_BASE}/profiles/company/${companyId}/`, {
        method: 'PATCH',
        body: formData,
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al actualizar empresa')
      }

      currentCompany.value = data.profile

      // 🆕 Si se actualizó el logo, actualizar también el authStore (para el navbar)
      if (authStore.user && files && files.logo && data.profile.logo) {
        authStore.user.profilePhoto = data.profile.logo
        // Actualizar localStorage también
        localStorage.setItem('auth_user', JSON.stringify(authStore.user))
      }

      successMessage.value = data.message
      return { success: true, company: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Subir logo de empresa
   */
  const uploadCompanyLogo = async (companyId, logoFile) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const formData = new FormData()
      formData.append('logo', logoFile)

      const authStore = useAuthStore()
      const jwtToken = authStore.accessToken

      if (!jwtToken) {
        throw new Error('No hay token de autenticación disponible')
      }

      const uploadUrl = `${API_BASE}/profiles/company/${companyId}/`

      const response = await fetch(uploadUrl, {
        method: 'PATCH',
        body: formData,
        headers: {
          'Authorization': `Bearer ${jwtToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al cargar el logo')
      }

      // Actualizar la empresa local
      currentCompany.value = {
        ...currentCompany.value,
        ...data.profile
      }

      // 🆕 Actualizar también el authStore con el nuevo logo (para el navbar)
      if (authStore.user && data.profile.logo) {
        authStore.user.profilePhoto = data.profile.logo
        // Actualizar localStorage también
        localStorage.setItem('auth_user', JSON.stringify(authStore.user))
      }

      successMessage.value = data.message || 'Logo actualizado exitosamente'
      return { success: true, company: data.profile }
    } catch (err) {
      console.error('Error during logo upload:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Subir banner de empresa
   */
  const uploadCompanyBanner = async (companyId, bannerFile) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const formData = new FormData()
      formData.append('banner', bannerFile)

      const authStore = useAuthStore()
      const jwtToken = authStore.accessToken

      if (!jwtToken) {
        throw new Error('No hay token de autenticación disponible')
      }

      const uploadUrl = `${API_BASE}/profiles/company/${companyId}/`

      const response = await fetch(uploadUrl, {
        method: 'PATCH',
        body: formData,
        headers: {
          'Authorization': `Bearer ${jwtToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al cargar el banner')
      }

      // Actualizar la empresa local
      currentCompany.value = {
        ...currentCompany.value,
        ...data.profile
      }

      successMessage.value = data.message || 'Banner actualizado exitosamente'
      return { success: true, company: data.profile }
    } catch (err) {
      console.error('Error during banner upload:', err)
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Listar empresas del usuario
   */
  const listUserCompanies = async (userId) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}/profiles/user/${userId}/companies`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al cargar empresas')
      }

      companies.value = data.companies || []
      return { success: true, companies: companies.value }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Eliminar logo de la empresa
   */
  const deleteCompanyLogo = async (companyId) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const authStore = useAuthStore()

      const response = await fetch(`${API_BASE}/profiles/company/${companyId}/logo/delete`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al eliminar logo')
      }

      currentCompany.value = data.profile
      successMessage.value = data.message || 'Logo eliminado exitosamente'
      return { success: true, company: data.profile }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Eliminar banner de la empresa
   */
  const deleteCompanyBanner = async (companyId) => {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    try {
      const authStore = useAuthStore()

      const response = await fetch(`${API_BASE}/profiles/company/${companyId}/banner/delete`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Error al eliminar banner')
      }

      currentCompany.value = data.profile
      successMessage.value = data.message || 'Banner eliminado exitosamente'
      return { success: true, company: data.profile }
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
  const clearCompany = () => {
    currentCompany.value = null
    error.value = null
    successMessage.value = null
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
    companies,
    currentCompany,
    isLoading,
    error,
    successMessage,

    // Methods
    getMyCompany,
    getCompanyById,
    createCompany,
    updateCompany,
    updateCompanyWithFiles,
    uploadCompanyLogo,
    uploadCompanyBanner,
    listUserCompanies,
    deleteCompanyLogo,
    deleteCompanyBanner,
    clearCompany,
    clearMessages
  }
})
