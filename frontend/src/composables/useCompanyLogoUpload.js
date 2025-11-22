import { ref } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'

/**
 * Composable para manejar la carga de logo de empresa
 */
export function useCompanyLogoUpload() {
  const authStore = useAuthStore()

  // ========== DATA ==========
  const isUploading = ref(false)
  const isDeleting = ref(false)
  const uploadError = ref(null)
  const uploadSuccess = ref(null)

  const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB

  // ========== METHODS ==========
  /**
   * Subir logo de empresa
   * @param {string} companyId - ID de la empresa
   * @param {File} file - Archivo de imagen a subir
   * @returns {Promise<Object>} Resultado de la operación
   */
  const uploadCompanyLogo = async (companyId, file) => {
    uploadError.value = null
    uploadSuccess.value = null

    if (!companyId) {
      uploadError.value = 'ID de empresa no disponible'
      return { success: false, error: uploadError.value }
    }

    if (!file) {
      uploadError.value = 'No se seleccionó archivo'
      return { success: false, error: uploadError.value }
    }

    // Validar tipo de archivo
    if (!file.type.startsWith('image/')) {
      uploadError.value = 'Por favor selecciona un archivo de imagen válido'
      return { success: false, error: uploadError.value }
    }

    // Validar tamaño
    if (file.size > MAX_FILE_SIZE) {
      uploadError.value = `El archivo es demasiado grande. Máximo ${MAX_FILE_SIZE / 1024 / 1024}MB`
      return { success: false, error: uploadError.value }
    }

    isUploading.value = true

    try {
      const accessToken = authStore.accessToken || localStorage.getItem('access_token')

      if (!accessToken) {
        throw new Error('No hay autenticación disponible')
      }

      // Crear FormData para enviar archivo
      const formData = new FormData()
      formData.append('logo', file)

      const response = await fetch(
        `http://localhost:8000/api/profiles/company/${companyId}/logo`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken}`
          },
          body: formData
        }
      )

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Error al subir logo')
      }

      const data = await response.json()
      uploadSuccess.value = 'Logo de empresa actualizado exitosamente'

      return {
        success: true,
        message: uploadSuccess.value,
        logoUrl: data.logoUrl
      }
    } catch (err) {
      uploadError.value = err.message || 'Error al subir logo'
      console.error('Error uploading company logo:', err)
      return {
        success: false,
        error: uploadError.value
      }
    } finally {
      isUploading.value = false
    }
  }

  /**
   * Eliminar logo de empresa
   * @param {string} companyId - ID de la empresa
   * @returns {Promise<Object>} Resultado de la operación
   */
  const deleteCompanyLogo = async (companyId) => {
    uploadError.value = null
    uploadSuccess.value = null

    if (!companyId) {
      uploadError.value = 'ID de empresa no disponible'
      return { success: false, error: uploadError.value }
    }

    isDeleting.value = true

    try {
      const accessToken = authStore.accessToken || localStorage.getItem('access_token')

      if (!accessToken) {
        throw new Error('No hay autenticación disponible')
      }

      const response = await fetch(
        `http://localhost:8000/api/profiles/company/${companyId}/logo`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      )

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Error al eliminar logo')
      }

      uploadSuccess.value = 'Logo eliminado exitosamente'

      return {
        success: true,
        message: uploadSuccess.value
      }
    } catch (err) {
      uploadError.value = err.message || 'Error al eliminar logo'
      console.error('Error deleting company logo:', err)
      return {
        success: false,
        error: uploadError.value
      }
    } finally {
      isDeleting.value = false
    }
  }

  /**
   * Limpiar mensajes de error y éxito
   */
  const clearMessages = () => {
    uploadError.value = null
    uploadSuccess.value = null
  }

  return {
    isUploading,
    isDeleting,
    uploadError,
    uploadSuccess,
    uploadCompanyLogo,
    deleteCompanyLogo,
    clearMessages
  }
}
