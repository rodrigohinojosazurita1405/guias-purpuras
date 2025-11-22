// frontend/src/stores/usePublishStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePublishStore = defineStore('publish', () => {
  // ========== STATE ==========
  const currentStep = ref(0)
  const jobData = ref({
    // Paso 0: Selección inicial
    subcategory: '',
    city: '',

    // Paso 1: Información del trabajo
    title: '',
    companyName: '',
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

    // Paso 3: Configuración de Aplicación
    applicationType: 'internal', // 'internal', 'external', 'both'
    externalApplicationUrl: '',

    // Paso 4: Resumen/Confirmación
    agreedToTerms: false
  })

  // ========== ACTIONS ==========
  const setJobData = (data) => {
    jobData.value = { ...jobData.value, ...data }
  }

  const setCurrentStep = (step) => {
    currentStep.value = step
  }

  const nextStep = () => {
    currentStep.value++
  }

  const previousStep = () => {
    if (currentStep.value > 0) {
      currentStep.value--
    }
  }

  const resetForm = () => {
    currentStep.value = 0
    jobData.value = {
      subcategory: '',
      city: '',
      title: '',
      companyName: '',
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
      selectedPlan: null,
      price: 0,
      applicationType: 'internal',
      externalApplicationUrl: '',
      agreedToTerms: false
    }
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
    resetForm
  }
})
