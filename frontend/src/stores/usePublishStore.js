// frontend/src/stores/usePublishStore.js
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const STORAGE_KEY = 'publish_job_draft'
const STORAGE_STEP_KEY = 'publish_current_step'

// Estructura por defecto del jobData
const DEFAULT_JOB_DATA = {
  // Paso 0: Selección inicial
  subcategory: '',
  city: '',

  // Paso 1: Información del trabajo
  title: '',
  companyName: '',
  companyId: '', // ID de la empresa del usuario
  logo: null, // Logo URL de la empresa
  companyAnonymous: false,
  description: '',
  jobCategory: '',
  contractType: 'Tiempo Completo',
  expiryDate: null,
  requirements: '',
  responsibilities: '',
  education: '',
  experience: '',
  languages: '',
  technicalSkills: '',
  salaryType: 'range',
  salaryMin: null,
  salaryMax: null,
  salaryFixed: null,
  benefits: '',
  vacancies: 1,
  email: '',
  whatsapp: '',
  website: '',
  applicationInstructions: '',
  screeningQuestions: [],

  // Paso 2: Plan de pago
  selectedPlan: null,
  price: 0,
  paymentReference: null, // Referencia única de pago (REF-XXX-XXX-XXX)
  proofOfPayment: null, // Archivo de comprobante de pago
  proofOfPaymentPreview: null, // Preview de la imagen

  // Paso 3: Configuración de Aplicación
  applicationType: 'internal', // 'internal', 'external', 'both'
  externalApplicationUrl: '',

  // Paso 4: Resumen/Confirmación
  agreedToTerms: false,
  publishedDate: null, // Fecha de publicación
  paymentVerified: false // Verificación de pago completada
}

export const usePublishStore = defineStore('publish', () => {
  // ========== STATE ==========
  const currentStep = ref(0)
  const jobData = ref({ ...DEFAULT_JOB_DATA })

  // ========== CARGAR DATOS GUARDADOS ==========
  const loadDraftFromStorage = () => {
    try {
      const savedDraft = localStorage.getItem(STORAGE_KEY)
      const savedStep = localStorage.getItem(STORAGE_STEP_KEY)

      if (savedDraft) {
        const parsedDraft = JSON.parse(savedDraft)
        jobData.value = { ...DEFAULT_JOB_DATA, ...parsedDraft }
      }

      if (savedStep) {
        currentStep.value = parseInt(savedStep, 10)
      }
    } catch (error) {
      console.error('Error al cargar borrador:', error)
    }
  }

  // ========== GUARDAR EN STORAGE ==========
  const saveDraftToStorage = () => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(jobData.value))
      localStorage.setItem(STORAGE_STEP_KEY, String(currentStep.value))
    } catch (error) {
      console.error('Error al guardar borrador:', error)
    }
  }

  // ========== AUTO-GUARDADO CON WATCH ==========
  watch(
    jobData,
    () => {
      saveDraftToStorage()
    },
    { deep: true }
  )

  watch(currentStep, () => {
    saveDraftToStorage()
  })

  // ========== ACTIONS ==========
  const setJobData = (data) => {
    jobData.value = { ...jobData.value, ...data }
    saveDraftToStorage()
  }

  const setCurrentStep = (step) => {
    currentStep.value = step
    saveDraftToStorage()
  }

  const nextStep = () => {
    currentStep.value++
    saveDraftToStorage()
  }

  const previousStep = () => {
    if (currentStep.value > 0) {
      currentStep.value--
      saveDraftToStorage()
    }
  }

  const resetForm = () => {
    currentStep.value = 0
    jobData.value = { ...DEFAULT_JOB_DATA }
    localStorage.removeItem(STORAGE_KEY)
    localStorage.removeItem(STORAGE_STEP_KEY)
  }

  const clearDraft = () => {
    localStorage.removeItem(STORAGE_KEY)
    localStorage.removeItem(STORAGE_STEP_KEY)
  }

  return {
    // State
    currentStep,
    jobData,

    // Actions
    setJobData,
    setCurrentStep,
    nextStep,
    previousStep,
    resetForm,
    clearDraft,
    loadDraftFromStorage
  }
})
