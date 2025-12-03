/**
 * Composable para gestionar la configuración de planes de forma reactiva
 * Sincroniza automáticamente con Django Admin
 */

import { ref, computed } from 'vue'

// Estado global reactivo de planes (compartido entre todos los componentes)
const plansCache = ref({
  estandar: {
    name: 'Estándar',
    price: 35,
    currency: 'Bs.',
    duration: '15 días',
    qrCode: '/qr-codes/qr-estandar.png',
    description: 'Plan básico para publicaciones simples'
  },
  purpura: {
    name: 'Púrpura',
    price: 79,
    currency: 'Bs.',
    duration: '30 días',
    qrCode: '/qr-codes/qr-purpura.png',
    description: 'Plan destacado con mayor visibilidad',
    recommended: true
  },
  impulso: {
    name: 'Impulso Pro',
    price: 149,
    currency: 'Bs.',
    duration: '30 días',
    qrCode: '/qr-codes/qr-impulso.png',
    description: 'Plan premium con máxima visibilidad'
  }
})

const isLoading = ref(false)
const lastFetchTime = ref(0)
const CACHE_DURATION = 30000 // 30 segundos

/**
 * Hook principal para usar la configuración de planes
 */
export function usePlansConfig() {
  /**
   * Cargar planes desde Django (con cache inteligente)
   * @param {boolean} forceRefresh - Forzar recarga ignorando cache
   */
  const loadPlans = async (forceRefresh = false) => {
    const now = Date.now()

    // Si ya se cargó recientemente y no es forzado, usar cache
    if (!forceRefresh && lastFetchTime.value && (now - lastFetchTime.value) < CACHE_DURATION) {
      console.log('✓ Usando planes en cache')
      return plansCache.value
    }

    try {
      isLoading.value = true
      const response = await fetch('/api/plans/')
      const data = await response.json()

      if (data.success && data.data) {
        // Actualizar cache con datos del backend
        const qrCodeMap = {
          'estandar': '/qr-codes/qr-estandar.png',
          'púrpura': '/qr-codes/qr-purpura.png',
          'purpura': '/qr-codes/qr-purpura.png',
          'impulso pro': '/qr-codes/qr-impulso.png',
          'impulso': '/qr-codes/qr-impulso.png'
        }

        data.data.forEach(plan => {
          const planKey = plan.name.toLowerCase()
          plansCache.value[planKey] = {
            name: plan.label,
            price: plan.price,
            currency: plan.currency,
            duration: `${plan.durationDays} días`,
            qrCode: qrCodeMap[planKey] || '/qr-codes/qr-estandar.png',
            description: plan.description || `Plan ${plan.label}`,
            features: plan.features
          }
        })

        lastFetchTime.value = now
        console.log('✓ Planes actualizados desde Django:', Object.keys(plansCache.value))
        return plansCache.value
      }
    } catch (error) {
      console.warn('⚠ Error cargando planes desde backend:', error)
    } finally {
      isLoading.value = false
    }

    return plansCache.value
  }

  /**
   * Obtener información de un plan específico
   */
  const getPlanInfo = (planKey) => {
    const normalizedKey = planKey?.toLowerCase()
    return plansCache.value[normalizedKey] || null
  }

  /**
   * Obtener ruta del QR para un plan
   */
  const getQRPath = (planKey) => {
    const normalizedKey = planKey?.toLowerCase()
    const plan = plansCache.value[normalizedKey]
    return plan ? plan.qrCode : null
  }

  /**
   * Obtener precio del plan
   */
  const getPlanPrice = (planKey) => {
    const normalizedKey = planKey?.toLowerCase()
    const plan = plansCache.value[normalizedKey]
    return plan ? `${plan.price} ${plan.currency}` : null
  }

  /**
   * Generar referencia de pago única
   */
  const generatePaymentReference = (planKey) => {
    const planCode = planKey.substring(0, 3).toUpperCase()
    const timestamp = Date.now().toString().slice(-6)
    const random = Math.random().toString(36).substring(2, 6).toUpperCase()
    return `REF-${planCode}-${timestamp}-${random}`
  }

  // Computed para acceder a los planes reactivamente
  const plans = computed(() => plansCache.value)

  return {
    plans,
    isLoading,
    loadPlans,
    getPlanInfo,
    getQRPath,
    getPlanPrice,
    generatePaymentReference
  }
}
