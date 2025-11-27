/**
 * Configuración de Pagos y QR
 * Este archivo centraliza la información de planes, precios y rutas de QR
 */

export const PAYMENT_CONFIG = {
  plans: {
    estandar: {
      name: 'Estandar',
      price: 35,
      currency: 'Bs.',
      duration: '15 días',
      qrCode: '/qr-codes/qr-escencial.png', // Ruta segura en public/ (mantener nombre del archivo)
      description: 'Plan básico para publicaciones simples'
    },
    purpura: {
      name: 'Púrpura',
      price: 79,
      currency: 'Bs.',
      duration: '30 días',
      qrCode: '/qr-codes/qr-purpura.png', // Ruta segura en public/
      description: 'Plan destacado con mayor visibilidad',
      recommended: true
    },
    impulso: {
      name: 'Impulso Pro',
      price: 169,
      currency: 'Bs.',
      duration: '30 días',
      qrCode: '/qr-codes/qr-impulso.png', // Ruta segura en public/
      description: 'Plan premium con máxima visibilidad'
    }
  },

  /**
   * Obtener información del plan
   */
  getPlanInfo(planKey) {
    return this.plans[planKey] || null
  },

  /**
   * Obtener ruta del QR para un plan
   */
  getQRPath(planKey) {
    const plan = this.plans[planKey]
    return plan ? plan.qrCode : null
  },

  /**
   * Obtener precio del plan
   */
  getPlanPrice(planKey) {
    const plan = this.plans[planKey]
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
