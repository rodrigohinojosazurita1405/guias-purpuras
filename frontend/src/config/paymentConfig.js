/**
 * Configuración de Pagos y QR
 * Este archivo centraliza la información de planes, precios y rutas de QR
 * Los datos se cargan dinámicamente desde Django pero incluye fallback estático
 */

export const PAYMENT_CONFIG = {
  // Planes estáticos como fallback (se sobrescriben al cargar desde backend)
  plans: {
    escencial: {
      name: 'Escencial',
      price: 35,
      currency: 'Bs.',
      duration: '15 días',
      qrCode: '/qr-codes/qr-estandar.png',
      description: 'Plan básico para publicaciones simples'
    },
    estandar: {
      name: 'Estandar',
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
      price: 169,
      currency: 'Bs.',
      duration: '30 días',
      qrCode: '/qr-codes/qr-impulso.png',
      description: 'Plan premium con máxima visibilidad'
    }
  },

  /**
   * Cargar planes dinámicamente desde Django
   * Actualiza el objeto plans con los datos del backend
   */
  async loadPlansFromBackend() {
    try {
      const response = await fetch('/api/plans/')
      const data = await response.json()

      if (data.success && data.data) {
        // Actualizar planes con datos del backend
        data.data.forEach(plan => {
          const planKey = plan.name.toLowerCase()
          const qrCodeMap = {
            'estandar': '/qr-codes/qr-estandar.png',
            'escencial': '/qr-codes/qr-estandar.png',
            'púrpura': '/qr-codes/qr-purpura.png',
            'purpura': '/qr-codes/qr-purpura.png',
            'impulso pro': '/qr-codes/qr-impulso.png',
            'impulso': '/qr-codes/qr-impulso.png'
          }

          this.plans[planKey] = {
            name: plan.label,
            price: plan.price,
            currency: plan.currency,
            duration: `${plan.durationDays} días`,
            qrCode: qrCodeMap[planKey] || '/qr-codes/qr-estandar.png',
            description: plan.description || `Plan ${plan.label}`
          }
        })
        console.log('✓ Planes cargados desde backend:', Object.keys(this.plans))
        return true
      }
    } catch (error) {
      console.warn('⚠ No se pudieron cargar planes desde backend, usando fallback:', error)
      return false
    }
  },

  /**
   * Obtener información del plan
   */
  getPlanInfo(planKey) {
    // Normalizar clave a minúsculas para compatibilidad
    const normalizedKey = planKey?.toLowerCase()
    return this.plans[normalizedKey] || null
  },

  /**
   * Obtener ruta del QR para un plan
   */
  getQRPath(planKey) {
    // Normalizar clave a minúsculas para compatibilidad
    const normalizedKey = planKey?.toLowerCase()
    const plan = this.plans[normalizedKey]
    return plan ? plan.qrCode : null
  },

  /**
   * Obtener precio del plan
   */
  getPlanPrice(planKey) {
    // Normalizar clave a minúsculas para compatibilidad
    const normalizedKey = planKey?.toLowerCase()
    const plan = this.plans[normalizedKey]
    return plan ? `${plan.price} ${plan.currency}` : null
  },

  /**
   * Generar referencia de pago única
   * Formato: REF-PLAN-TIMESTAMP-RANDOM
   */
  generatePaymentReference(planKey) {
    const planCode = planKey.substring(0, 3).toUpperCase()
    const timestamp = Date.now().toString().slice(-6)
    const random = Math.random().toString(36).substring(2, 6).toUpperCase()
    return `REF-${planCode}-${timestamp}-${random}`
  }
}

export default PAYMENT_CONFIG
