import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useOrdersStore = defineStore('orders', () => {
  // State
  const orders = ref([])
  const currentOrder = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const apiUrl = 'http://localhost:8000/api'

  // Getters
  const orderCount = computed(() => orders.value.length)

  const ordersByStatus = computed(() => {
    const grouped = {
      PENDING: [],
      PAID: [],
      INVOICE_SENT: [],
      COMPLETED: []
    }
    orders.value.forEach(order => {
      if (grouped[order.status]) {
        grouped[order.status].push(order)
      }
    })
    return grouped
  })

  const totalPaid = computed(() => {
    return orders.value.reduce((sum, order) => sum + (order.amountPaid || 0), 0)
  })

  // Actions
  const loadOrders = async (accessToken) => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${apiUrl}/orders/me`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          orders.value = data.orders || []
          console.log('✅ Órdenes cargadas:', orders.value.length)
        } else {
          error.value = data.message || 'Error al cargar órdenes'
        }
      } else {
        const errorData = await response.json()
        error.value = errorData.message || `Error ${response.status}`
        console.error('❌ Error al cargar órdenes:', response.status, errorData)
      }
    } catch (err) {
      error.value = err.message
      console.error('❌ Error en loadOrders:', err)
    } finally {
      loading.value = false
    }
  }

  const getOrderDetail = async (orderId, accessToken) => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${apiUrl}/orders/${orderId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          currentOrder.value = data.order
          console.log('✅ Detalle de orden cargado')
          return data.order
        } else {
          error.value = data.message || 'Error al cargar orden'
        }
      } else {
        const errorData = await response.json()
        error.value = errorData.message || `Error ${response.status}`
        console.error('❌ Error al cargar detalle:', response.status, errorData)
      }
    } catch (err) {
      error.value = err.message
      console.error('❌ Error en getOrderDetail:', err)
    } finally {
      loading.value = false
    }

    return null
  }

  const resendInvoice = async (orderId, method = 'both', accessToken) => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${apiUrl}/orders/${orderId}/resend-invoice`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({ method })
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          // Actualizar la orden en el estado local
          const index = orders.value.findIndex(o => o.id === orderId)
          if (index !== -1 && data.updatedOrder) {
            orders.value[index] = { ...orders.value[index], ...data.updatedOrder }
          }
          console.log('✅ Factura reenviada:', data.message)
          return true
        } else {
          error.value = data.message || 'Error al reenviar factura'
        }
      } else {
        const errorData = await response.json()
        error.value = errorData.message || `Error ${response.status}`
        console.error('❌ Error al reenviar:', response.status, errorData)
      }
    } catch (err) {
      error.value = err.message
      console.error('❌ Error en resendInvoice:', err)
    } finally {
      loading.value = false
    }

    return false
  }

  const downloadInvoice = async (orderId, accessToken) => {
    try {
      // Buscar la orden en el estado
      const order = orders.value.find(o => o.id === orderId)
      if (!order) {
        error.value = 'Orden no encontrada'
        return false
      }

      // Si existe paymentProof, descargar desde allí
      if (order.paymentProof) {
        window.open(order.paymentProof, '_blank')
        console.log('✅ Descargando comprobante de pago')
        return true
      }

      // Si existe, descargar la factura (esto se implementaría cuando haya un endpoint de descarga)
      error.value = 'La factura aún no está disponible para descargar'
      return false
    } catch (err) {
      error.value = err.message
      console.error('❌ Error en downloadInvoice:', err)
      return false
    }
  }

  const getOrderById = (orderId) => {
    return orders.value.find(o => o.id === orderId)
  }

  const clearOrders = () => {
    orders.value = []
    currentOrder.value = null
    error.value = null
  }

  return {
    // State
    orders,
    currentOrder,
    loading,
    error,

    // Getters
    orderCount,
    ordersByStatus,
    totalPaid,

    // Actions
    loadOrders,
    getOrderDetail,
    resendInvoice,
    downloadInvoice,
    getOrderById,
    clearOrders
  }
})
