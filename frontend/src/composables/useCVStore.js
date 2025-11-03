// frontend/src/composables/useCVStore.js
import { ref, computed } from 'vue'
import { useToast } from 'vuestic-ui'

const STORAGE_KEY = 'guias_purpuras_cvs'
const MAX_CVS = 2 // Límite máximo de CVs

// Estado global (singleton)
const savedCVs = ref([])
const isInitialized = ref(false)

export function useCVStore() {
  const { init: notify } = useToast()

  // ========== COMPUTED ==========
  const cvCount = computed(() => savedCVs.value.length)
  const hasReachedLimit = computed(() => savedCVs.value.length >= MAX_CVS)
  const defaultCV = computed(() => savedCVs.value.find(cv => cv.isDefault))
  
  // ========== INITIALIZATION ==========
  const initialize = () => {
    if (isInitialized.value) return
    
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        savedCVs.value = JSON.parse(stored)
      }
      isInitialized.value = true
    } catch (error) {
      console.error('Error loading CVs:', error)
      savedCVs.value = []
    }
  }

  // ========== SAVE TO LOCALSTORAGE ==========
  const saveToStorage = () => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(savedCVs.value))
    } catch (error) {
      console.error('Error saving CVs:', error)
      notify({
        message: '❌ Error al guardar. Revisa el almacenamiento del navegador.',
        color: 'danger'
      })
    }
  }

  // ========== CREATE CV ==========
  const createCV = (cvData) => {
    // Verificar límite
    if (hasReachedLimit.value) {
      notify({
        message: `⚠️ Has alcanzado el límite de ${MAX_CVS} CVs. Elimina uno para crear otro.`,
        color: 'warning',
        duration: 4000
      })
      return null
    }

    const newCV = {
      id: Date.now().toString(),
      title: `${cvData.personalInfo.firstName} ${cvData.personalInfo.lastName}`,
      data: cvData,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      isDefault: savedCVs.value.length === 0 // Primero es default
    }

    savedCVs.value.push(newCV)
    saveToStorage()

    notify({
      message: '✅ CV guardado exitosamente',
      color: 'success',
      duration: 3000
    })

    return newCV
  }

  // ========== UPDATE CV ==========
  const updateCV = (id, cvData) => {
    const index = savedCVs.value.findIndex(cv => cv.id === id)
    
    if (index === -1) {
      notify({
        message: '❌ CV no encontrado',
        color: 'danger'
      })
      return false
    }

    savedCVs.value[index] = {
      ...savedCVs.value[index],
      title: `${cvData.personalInfo.firstName} ${cvData.personalInfo.lastName}`,
      data: cvData,
      updatedAt: new Date().toISOString()
    }

    saveToStorage()

    notify({
      message: '✅ CV actualizado exitosamente',
      color: 'success',
      duration: 3000
    })

    return true
  }

  // ========== DELETE CV ==========
  const deleteCV = (id) => {
    const index = savedCVs.value.findIndex(cv => cv.id === id)
    
    if (index === -1) {
      notify({
        message: '❌ CV no encontrado',
        color: 'danger'
      })
      return false
    }

    const wasDefault = savedCVs.value[index].isDefault
    savedCVs.value.splice(index, 1)

    // Si era default y quedan CVs, hacer default al primero
    if (wasDefault && savedCVs.value.length > 0) {
      savedCVs.value[0].isDefault = true
    }

    saveToStorage()

    notify({
      message: '🗑️ CV eliminado correctamente',
      color: 'info',
      duration: 3000
    })

    return true
  }

  // ========== SET DEFAULT CV ==========
  const setDefaultCV = (id) => {
    // Quitar default de todos
    savedCVs.value.forEach(cv => {
      cv.isDefault = false
    })

    // Poner default al seleccionado
    const cv = savedCVs.value.find(cv => cv.id === id)
    if (cv) {
      cv.isDefault = true
      saveToStorage()

      notify({
        message: '⭐ CV marcado como predeterminado',
        color: 'success',
        duration: 2000
      })

      return true
    }

    return false
  }

  // ========== GET CV BY ID ==========
  const getCVById = (id) => {
    return savedCVs.value.find(cv => cv.id === id)
  }

  // ========== GET ALL CVS ==========
  const getAllCVs = () => {
    return savedCVs.value
  }

  // ========== CLEAR ALL (para testing) ==========
  const clearAll = () => {
    savedCVs.value = []
    saveToStorage()
    notify({
      message: '🗑️ Todos los CVs eliminados',
      color: 'info'
    })
  }

  // ========== FORMAT DATE ==========
  const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }

  // Inicializar automáticamente
  initialize()

  return {
    // State
    savedCVs,
    cvCount,
    hasReachedLimit,
    defaultCV,
    MAX_CVS,

    // Methods
    createCV,
    updateCV,
    deleteCV,
    setDefaultCV,
    getCVById,
    getAllCVs,
    clearAll,
    formatDate
  }
}