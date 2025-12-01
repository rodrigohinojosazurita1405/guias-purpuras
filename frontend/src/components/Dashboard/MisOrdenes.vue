<!-- frontend/src/components/Dashboard/MisOrdenes.vue -->
<template>
  <div class="mis-ordenes-container">
    <!-- Header -->
    <div class="section-header">
      <h2>Mis Órdenes</h2>
      <p class="section-subtitle">Historial de compras de planes y gestión de facturas</p>
    </div>

    <!-- Stats Bar -->
    <div class="stats-bar">
      <div class="stat-item">
        <div class="stat-value">{{ ordersStore.orderCount }}</div>
        <div class="stat-label">Órdenes Totales</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ ordersStore.totalPaid.toFixed(2) }}</div>
        <div class="stat-label">Total Pagado (Bs)</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ ordersStore.ordersByStatus.PAID.length }}</div>
        <div class="stat-label">Órdenes Pagadas</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ ordersStore.ordersByStatus.INVOICE_SENT.length }}</div>
        <div class="stat-label">Facturas Enviadas</div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="search-box">
        <va-icon name="search" />
        <va-input
          v-model="searchQuery"
          placeholder="Buscar por razón social, NIT o número de factura..."
          type="text"
          clearable
          class="search-input"
        />
      </div>

      <div class="filter-controls">
        <va-select
          v-model="filterStatus"
          :options="statusOptions"
          placeholder="Filtrar por estado"
          clearable
          class="filter-select"
        />

        <va-select
          v-model="sortBy"
          :options="sortOptions"
          placeholder="Ordenar por"
          class="filter-select"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="ordersStore.loading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
      <p>Cargando tus órdenes...</p>
    </div>

    <!-- Orders List -->
    <div v-else-if="filteredOrders.length > 0" class="orders-list">
      <div
        v-for="order in filteredOrders"
        :key="order.id"
        class="order-card"
        :class="[`status-${order.status}`]"
      >
        <!-- Card Header with Status Badge -->
        <div class="card-header">
          <div class="order-info">
            <h3 class="order-title">{{ order.razonSocial }}</h3>
            <p class="order-number">Factura: #{{ order.invoiceNumber }}</p>
          </div>
          <div class="status-badge" :class="'status-' + order.status">
            <va-icon :name="getStatusIcon(order.status)" size="small" />
            <span>{{ order.statusDisplay }}</span>
          </div>
        </div>

        <!-- Order Details Grid -->
        <div class="order-details">
          <div class="detail-item">
            <span class="detail-label">Plan</span>
            <span class="detail-value">{{ order.planLabel }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">NIT</span>
            <span class="detail-value">{{ order.nit }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">CI</span>
            <span class="detail-value">{{ order.ci }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Monto Pagado</span>
            <span class="detail-value amount">{{ order.amountPaid }} Bs</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Fecha de Orden</span>
            <span class="detail-value">{{ formatDate(order.orderDate) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Correo Electrónico</span>
            <span class="detail-value">{{ order.electronicInvoiceEmail || 'No especificado' }}</span>
          </div>
        </div>

        <!-- Invoice Status Info -->
        <div v-if="order.electronicInvoiceSentDate" class="invoice-info">
          <va-icon name="check_circle" size="small" color="success" />
          <span class="invoice-text">
            Factura enviada: {{ formatDate(order.electronicInvoiceSentDate) }}
          </span>
        </div>

        <!-- Card Actions -->
        <div class="card-actions">
          <button class="action-btn-gradient" @click="handleViewOrder(order.id)">
            <va-icon name="visibility" size="small" />
            Ver Detalle
          </button>

          <button
            v-if="order.paymentProof"
            class="action-btn-gradient"
            @click="handleDownloadProof(order.id)"
          >
            <va-icon name="download" size="small" />
            Descargar Comprobante
          </button>

          <button
            v-if="order.status !== 'COMPLETED'"
            class="action-btn-secondary"
            @click="handleResendInvoice(order.id, 'email')"
          >
            <va-icon name="email" size="small" />
            Reenviar Email
          </button>

          <button
            v-if="order.electronicInvoiceWhatsapp && order.status !== 'COMPLETED'"
            class="action-btn-secondary"
            @click="handleResendInvoice(order.id, 'whatsapp')"
          >
            <va-icon name="chat" size="small" />
            Reenviar WhatsApp
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <va-icon name="shopping_cart" size="4rem" color="purple" />
      <h3>No tienes órdenes de planes</h3>
      <p>Adquiere un plan para comenzar a publicar ofertas de trabajo</p>
      <button class="explore-btn" @click="$router.push('/planes')">
        <va-icon name="storefront" />
        Ver Planes Disponibles
      </button>
    </div>

    <!-- Pagination (if needed in future) -->
    <div v-if="filteredOrders.length > 0 && totalOrders > itemsPerPage" class="pagination">
      <va-pagination
        v-model="currentPage"
        :pages="totalPages"
      />
    </div>

    <!-- Order Detail Modal -->
    <va-modal
      v-model="showDetailModal"
      size="large"
      title="Detalle de Orden"
      @close="showDetailModal = false"
    >
      <div v-if="selectedOrder" class="order-detail-modal">
        <div class="detail-section">
          <h4>Información de la Orden</h4>
          <div class="detail-grid">
            <div>
              <strong>Número de Factura:</strong><br>{{ selectedOrder.invoiceNumber }}
            </div>
            <div>
              <strong>Estado:</strong><br>
              <va-chip :color="getStatusColor(selectedOrder.status)">
                {{ selectedOrder.statusDisplay }}
              </va-chip>
            </div>
            <div>
              <strong>Razón Social:</strong><br>{{ selectedOrder.razonSocial }}
            </div>
            <div>
              <strong>NIT:</strong><br>{{ selectedOrder.nit }}
            </div>
            <div>
              <strong>CI:</strong><br>{{ selectedOrder.ci }}
            </div>
            <div>
              <strong>Plan:</strong><br>{{ selectedOrder.planLabel }}
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>Información de Pago</h4>
          <div class="detail-grid">
            <div>
              <strong>Monto Pagado:</strong><br>{{ selectedOrder.amountPaid }} Bs
            </div>
            <div>
              <strong>Fecha de Orden:</strong><br>{{ formatDate(selectedOrder.orderDate) }}
            </div>
            <div>
              <strong>Email para Factura:</strong><br>{{ selectedOrder.electronicInvoiceEmail || 'No especificado' }}
            </div>
            <div>
              <strong>WhatsApp:</strong><br>{{ selectedOrder.electronicInvoiceWhatsapp || 'No especificado' }}
            </div>
          </div>
        </div>

        <div v-if="selectedOrder.electronicInvoiceSentDate" class="detail-section">
          <h4>Estado de Factura Electrónica</h4>
          <p>
            <va-icon name="check_circle" size="small" color="success" />
            Enviada el: {{ formatDate(selectedOrder.electronicInvoiceSentDate) }}
          </p>
        </div>
      </div>

      <template #footer>
        <va-button preset="plain" @click="showDetailModal = false">Cerrar</va-button>
        <va-button
          v-if="selectedOrder && selectedOrder.status !== 'COMPLETED'"
          @click="handleResendInvoice(selectedOrder.id, 'email')"
        >
          <va-icon name="email" size="small" />
          Reenviar Factura
        </va-button>
      </template>
    </va-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vuestic-ui'
import { useAuthStore } from '@/stores/useAuthStore'
import { useOrdersStore } from '@/stores/useOrdersStore'

// ========== COMPOSABLES ==========
const { init: notify } = useToast()
const authStore = useAuthStore()
const ordersStore = useOrdersStore()

// ========== PROPS ==========
const props = defineProps({
  userProfileId: {
    type: String,
    required: true
  }
})

// ========== DATA ==========
const searchQuery = ref('')
const filterStatus = ref('')
const sortBy = ref('recent')
const currentPage = ref(1)
const itemsPerPage = 10
const showDetailModal = ref(false)
const selectedOrder = ref(null)

const statusOptions = [
  { text: 'Pendiente de Pago', value: 'PENDING' },
  { text: 'Pagado', value: 'PAID' },
  { text: 'Factura Enviada', value: 'INVOICE_SENT' },
  { text: 'Completado', value: 'COMPLETED' }
]

const sortOptions = [
  { text: 'Más reciente', value: 'recent' },
  { text: 'Más antigua', value: 'oldest' },
  { text: 'Mayor monto', value: 'amount_desc' },
  { text: 'Menor monto', value: 'amount_asc' }
]

// ========== LIFECYCLE ==========
onMounted(() => {
  loadOrders()
})

// ========== COMPUTED PROPERTIES ==========
const filteredOrders = computed(() => {
  let filtered = ordersStore.orders

  // Filter by status
  if (filterStatus.value) {
    filtered = filtered.filter(order => order.status === filterStatus.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(order =>
      order.razonSocial.toLowerCase().includes(query) ||
      order.nit.toLowerCase().includes(query) ||
      order.invoiceNumber.toLowerCase().includes(query)
    )
  }

  // Sort
  const sorted = [...filtered]
  if (sortBy.value === 'recent') {
    sorted.sort((a, b) => new Date(b.orderDate) - new Date(a.orderDate))
  } else if (sortBy.value === 'oldest') {
    sorted.sort((a, b) => new Date(a.orderDate) - new Date(b.orderDate))
  } else if (sortBy.value === 'amount_desc') {
    sorted.sort((a, b) => b.amountPaid - a.amountPaid)
  } else if (sortBy.value === 'amount_asc') {
    sorted.sort((a, b) => a.amountPaid - b.amountPaid)
  }

  return sorted.slice(
    (currentPage.value - 1) * itemsPerPage,
    currentPage.value * itemsPerPage
  )
})

const totalOrders = computed(() => ordersStore.orders.length)

const totalPages = computed(() =>
  Math.ceil(totalOrders.value / itemsPerPage)
)

// ========== METHODS ==========
const loadOrders = async () => {
  try {
    if (!authStore.accessToken) {
      notify({
        message: 'No hay sesión activa',
        color: 'danger'
      })
      return
    }

    await ordersStore.loadOrders(authStore.accessToken)

    if (ordersStore.error) {
      notify({
        message: `Error: ${ordersStore.error}`,
        color: 'danger',
        duration: 5000
      })
    } else if (ordersStore.orders.length > 0) {
      notify({
        message: `✅ ${ordersStore.orders.length} órdenes cargadas`,
        color: 'success',
        duration: 2000
      })
    }
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  }
}

const getStatusLabel = (status) => {
  const labels = {
    'PENDING': 'Pendiente de Pago',
    'PAID': 'Pagado',
    'INVOICE_SENT': 'Factura Enviada',
    'COMPLETED': 'Completado'
  }
  return labels[status] || status
}

const getStatusIcon = (status) => {
  const icons = {
    'PENDING': 'schedule',
    'PAID': 'check_circle',
    'INVOICE_SENT': 'done_all',
    'COMPLETED': 'check_circle'
  }
  return icons[status] || 'info'
}

const getStatusColor = (status) => {
  const colors = {
    'PENDING': 'warning',
    'PAID': 'info',
    'INVOICE_SENT': 'success',
    'COMPLETED': 'success'
  }
  return colors[status] || 'default'
}

const formatDate = (dateString) => {
  try {
    const date = new Date(dateString)
    const now = new Date()
    const diff = now - date
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))

    if (days === 0) return 'Hoy'
    if (days === 1) return 'Ayer'
    if (days < 7) return `Hace ${days} días`
    if (days < 30) return `Hace ${Math.floor(days / 7)} semanas`
    if (days < 365) return `Hace ${Math.floor(days / 30)} meses`

    return date.toLocaleDateString('es-ES')
  } catch (err) {
    return 'Fecha inválida'
  }
}

const handleViewOrder = (orderId) => {
  const order = ordersStore.getOrderById(orderId)
  if (order) {
    selectedOrder.value = order
    showDetailModal.value = true
  }
}

const handleDownloadProof = (orderId) => {
  ordersStore.downloadInvoice(orderId, authStore.accessToken)
  notify({
    message: '✅ Descargando comprobante...',
    color: 'success',
    duration: 2000
  })
}

const handleResendInvoice = async (orderId, method = 'email') => {
  try {
    const success = await ordersStore.resendInvoice(orderId, method, authStore.accessToken)
    if (success) {
      notify({
        message: `✅ Factura reenviada por ${method}`,
        color: 'success',
        duration: 3000
      })
    } else {
      notify({
        message: `Error: ${ordersStore.error || 'No se pudo reenviar'}`,
        color: 'danger',
        duration: 3000
      })
    }
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  }
}
</script>

<style scoped>
.mis-ordenes-container {
  padding: 0;
}

/* ========== HEADER ========== */
.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.5rem;
}

.section-subtitle {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
}

/* ========== STATS BAR ========== */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-item {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #7c3aed;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.85rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ========== FILTER BAR ========== */
.filter-bar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.search-box :deep(.va-input) {
  width: 100%;
}

.filter-controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.filter-select {
  min-width: 200px;
}

/* ========== LOADING STATE ========== */
.loading-state {
  text-align: center;
  padding: 3rem 1rem;
}

.loading-state p {
  margin-top: 1rem;
  color: #666;
}

/* ========== ORDERS LIST ========== */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.order-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  overflow: hidden;
  transition: all 0.3s ease;
}

.order-card:hover {
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.1);
  border-color: #7c3aed;
}

.order-card.status-COMPLETED {
  border-left: 4px solid #10b981;
}

.order-card.status-PAID {
  border-left: 4px solid #3b82f6;
}

.order-card.status-INVOICE_SENT {
  border-left: 4px solid #8b5cf6;
}

.order-card.status-PENDING {
  border-left: 4px solid #f59e0b;
}

/* ========== CARD HEADER ========== */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.order-info {
  flex: 1;
}

.order-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 0.25rem;
}

.order-number {
  font-size: 0.85rem;
  color: #999;
  margin: 0;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  min-width: 150px;
  justify-content: center;
}

.status-badge.status-PENDING {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.status-PAID {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.status-INVOICE_SENT {
  background: #d8b4fe;
  color: #6d28d9;
}

.status-badge.status-COMPLETED {
  background: #d1fae5;
  color: #065f46;
}

/* ========== ORDER DETAILS ========== */
.order-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-label {
  font-size: 0.75rem;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.detail-value {
  font-size: 1rem;
  color: #1a1a1a;
  font-weight: 500;
}

.detail-value.amount {
  color: #7c3aed;
  font-weight: 700;
}

/* ========== INVOICE INFO ========== */
.invoice-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: #f0fdf4;
  border-left: 3px solid #10b981;
}

.invoice-text {
  font-size: 0.9rem;
  color: #065f46;
}

/* ========== CARD ACTIONS ========== */
.card-actions {
  display: flex;
  gap: 0.75rem;
  padding: 1.5rem;
  flex-wrap: wrap;
}

.action-btn-gradient,
.action-btn-secondary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn-gradient {
  background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
  color: white;
}

.action-btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
}

.action-btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
}

.action-btn-secondary:hover {
  background: #e5e7eb;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  border: 1px dashed #d1d5db;
}

.empty-state h3 {
  font-size: 1.25rem;
  color: #1a1a1a;
  margin: 1rem 0 0.5rem;
}

.empty-state p {
  color: #666;
  margin-bottom: 1.5rem;
}

.explore-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.explore-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
}

/* ========== PAGINATION ========== */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

/* ========== ORDER DETAIL MODAL ========== */
.order-detail-modal {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-section {
  padding: 1rem;
  background: #fafafa;
  border-radius: 8px;
}

.detail-section h4 {
  margin: 0 0 1rem;
  color: #1a1a1a;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.detail-grid > div {
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.detail-grid strong {
  color: #7c3aed;
  display: block;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .stats-bar {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-bar {
    flex-direction: column;
  }

  .filter-controls {
    grid-template-columns: 1fr;
  }

  .order-details {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .card-actions {
    flex-direction: column;
  }

  .action-btn-gradient,
  .action-btn-secondary {
    width: 100%;
    justify-content: center;
  }

  .status-badge {
    width: 100%;
  }
}
</style>
