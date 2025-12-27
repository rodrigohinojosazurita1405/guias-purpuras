// frontend/src/stores/useApplicationStore.js
import { defineStore } from 'pinia'
import { ref, reactive, computed } from 'vue'

const API_BASE_URL = 'http://localhost:8000/api'

export const useApplicationStore = defineStore('application', () => {
  // ========== STATE ==========
  const currentApplicationData = reactive({
    jobId: null,
    // Pretensión salarial (condicional)
    salaryType: 'bruto',
    salaryCurrency: 'Bs.',
    salaryAmount: null,

    // Carta de presentación
    coverLetter: '',

    // Screening answers
    screeningAnswers: [],

    // CV
    useSavedCV: false,
    uploadedCV: null,
    cvFormData: null,

    // Terms
    acceptedTerms: false
  })

  const jobData = ref(null)
  const applications = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const submitting = ref(false)
  const applicationId = ref(null)

  // ========== GETTERS ==========
  const requiresSalaryExpectation = computed(() => {
    return jobData.value?.salaryType === 'negotiable' || jobData.value?.salaryType === 'pretension_salarial'
  })

  const hasScreeningQuestions = computed(() => {
    return jobData.value?.screeningQuestions && jobData.value.screeningQuestions.length > 0
  })

  const screeningQuestions = computed(() => {
    return jobData.value?.screeningQuestions || []
  })

  const salaryDisplayText = computed(() => {
    if (!jobData.value) return null
    const type = jobData.value.salaryType
    if (type === 'range' && jobData.value.salaryMin && jobData.value.salaryMax) {
      return `Bs. ${parseInt(jobData.value.salaryMin).toLocaleString()} - ${parseInt(jobData.value.salaryMax).toLocaleString()}`
    }
    if (type === 'fixed' && jobData.value.salaryFixed) {
      return `Bs. ${parseInt(jobData.value.salaryFixed).toLocaleString()}`
    }
    if (type === 'negotiable') {
      return 'A convenir'
    }
    if (type === 'pretension_salarial') {
      return 'Indique su pretensión salarial'
    }
    return null
  })

  const calculatedNetSalary = computed(() => {
    if (!currentApplicationData.salaryAmount || currentApplicationData.salaryType !== 'bruto') {
      return 0
    }
    // Cálculo aproximado (12.71% de aporte laboral)
    const netSalary = currentApplicationData.salaryAmount * 0.8729
    return Math.round(netSalary)
  })

  // ========== ACTIONS ==========

  /**
   * Cargar datos de una oferta de trabajo
   */
  const loadJobData = async (jobId) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`)
      }

      const data = await response.json()

      if (data.success) {
        jobData.value = data.job
        currentApplicationData.jobId = jobId

        // Inicializar screening answers array
        if (hasScreeningQuestions.value) {
          currentApplicationData.screeningAnswers = new Array(screeningQuestions.value.length).fill('')
        }

        console.log('[APPLICATION_STORE] Datos de trabajo cargados:', jobData.value)
        return true
      } else {
        throw new Error(data.message || 'Error desconocido')
      }
    } catch (err) {
      error.value = err.message
      console.error('[APPLICATION_STORE] Error al cargar trabajo:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Actualizar dato de la aplicación
   */
  const setApplicationData = (field, value) => {
    if (field in currentApplicationData) {
      currentApplicationData[field] = value
    }
  }

  /**
   * Actualizar respuesta de pregunta de screening
   */
  const setScreeningAnswer = (index, answer) => {
    if (index < currentApplicationData.screeningAnswers.length) {
      currentApplicationData.screeningAnswers[index] = answer
    }
  }

  /**
   * Validar si una aplicación está lista para enviar
   */
  const validateApplication = () => {
    const errors = {}

    // Validar pretensión salarial si es requerida
    if (requiresSalaryExpectation.value && !currentApplicationData.salaryAmount) {
      errors.salaryAmount = 'La pretensión salarial es requerida'
    }

    // Validar preguntas obligatorias de screening
    if (hasScreeningQuestions.value) {
      screeningQuestions.value.forEach((question, index) => {
        if (question.required) {
          const answer = currentApplicationData.screeningAnswers[index]
          if (!answer || !answer.toString().trim()) {
            errors[`screening_${index}`] = 'Esta pregunta es obligatoria'
          }
        }
      })
    }

    // Validar CV
    const hasCV = currentApplicationData.useSavedCV || currentApplicationData.uploadedCV || currentApplicationData.cvFormData
    if (!hasCV) {
      errors.cv = 'Debes proporcionar tu currículum'
    }

    // Validar términos
    if (!currentApplicationData.acceptedTerms) {
      errors.acceptedTerms = 'Debes aceptar los términos y condiciones'
    }

    return { valid: Object.keys(errors).length === 0, errors }
  }

  /**
   * Enviar aplicación al backend
   */
  const submitApplication = async () => {
    // Validar antes de enviar
    const validation = validateApplication()
    if (!validation.valid) {
      error.value = 'Por favor completa todos los campos requeridos'
      return { success: false, errors: validation.errors }
    }

    submitting.value = true
    error.value = null

    try {
      const payload = {
        applicantName: currentApplicationData.applicantName || 'Candidato',
        applicantEmail: currentApplicationData.applicantEmail || '',
        applicantPhone: currentApplicationData.applicantPhone || '',
        applicantWhatsapp: currentApplicationData.applicantWhatsapp || '',
        screeningAnswers: hasScreeningQuestions.value ? currentApplicationData.screeningAnswers : {},
        salaryExpectation: requiresSalaryExpectation.value ? {
          type: currentApplicationData.salaryType,
          currency: currentApplicationData.salaryCurrency,
          amount: currentApplicationData.salaryAmount
        } : null,
        coverLetter: currentApplicationData.coverLetter
      }

      console.log('[APPLICATION_STORE] Enviando aplicación:', payload)

      const response = await fetch(`${API_BASE_URL}/jobs/${currentApplicationData.jobId}/apply`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.message || 'Error al enviar la aplicación')
      }

      applicationId.value = data.applicationId
      console.log('[APPLICATION_STORE] Aplicación enviada exitosamente:', data)

      return { success: true, applicationId: data.applicationId }
    } catch (err) {
      error.value = err.message
      console.error('[APPLICATION_STORE] Error al enviar aplicación:', err)
      return { success: false, error: err.message }
    } finally {
      submitting.value = false
    }
  }

  /**
   * Cargar aplicaciones del usuario para un trabajo
   */
  const loadUserApplications = async (jobId) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/applications/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`)
      }

      const data = await response.json()

      if (data.success) {
        applications.value = data.applications || []
        return true
      } else {
        throw new Error(data.message || 'Error desconocido')
      }
    } catch (err) {
      error.value = err.message
      console.error('[APPLICATION_STORE] Error al cargar aplicaciones:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Resetear estado de la aplicación
   */
  const resetApplication = () => {
    Object.assign(currentApplicationData, {
      jobId: null,
      salaryType: 'bruto',
      salaryCurrency: 'Bs.',
      salaryAmount: null,
      coverLetter: '',
      screeningAnswers: [],
      useSavedCV: false,
      uploadedCV: null,
      cvFormData: null,
      acceptedTerms: false
    })

    jobData.value = null
    applicationId.value = null
    error.value = null
  }

  return {
    // State
    currentApplicationData,
    jobData,
    applications,
    isLoading,
    error,
    submitting,
    applicationId,

    // Getters
    requiresSalaryExpectation,
    hasScreeningQuestions,
    screeningQuestions,
    salaryDisplayText,
    calculatedNetSalary,

    // Actions
    loadJobData,
    setApplicationData,
    setScreeningAnswer,
    validateApplication,
    submitApplication,
    loadUserApplications,
    resetApplication
  }
})
