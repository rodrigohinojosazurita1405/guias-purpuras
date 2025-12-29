<template>
  <div class="notifications-container">
    <!-- Header -->
    <div class="section-header">
      <div class="header-content">
        <h2>Notificaciones</h2>
        <p class="section-subtitle">Mantente al día con las actualizaciones importantes</p>
      </div>

      <!-- Stats Summary -->
      <div class="stats-summary">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #ef4444, #dc2626)">
            <va-icon name="notifications_active" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-label">No leídas</span>
            <span class="stat-value">{{ unreadCount }}</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6, #2563eb)">
            <va-icon name="inbox" size="1.25rem" />
          </div>
          <div class="stat-info">
            <span class="stat-label">Total</span>
            <span class="stat-value">{{ total }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Action Bar -->
    <div class="action-bar">
      <div class="filter-controls">
        <!-- Filtro de no leídas mejorado -->
        <div class="filter-chips">
          <button
            class="filter-chip"
            :class="{ active: viewMode === 'all' }"
            @click="viewMode = 'all'"
          >
            <va-icon name="inbox" size="1rem" />
            <span>Todas</span>
            <span class="chip-badge">{{ total }}</span>
          </button>

          <button
            class="filter-chip"
            :class="{ active: viewMode === 'unread' }"
            @click="viewMode = 'unread'"
          >
            <va-icon name="notifications_active" size="1rem" />
            <span>No leídas</span>
            <span v-if="unreadCount > 0" class="chip-badge unread">{{ unreadCount }}</span>
          </button>

          <button
            class="filter-chip"
            :class="{ active: viewMode === 'history' }"
            @click="viewMode = 'history'"
          >
            <va-icon name="history" size="1rem" />
            <span>Historial</span>
            <span v-if="dismissedCount > 0" class="chip-badge">{{ dismissedCount }}</span>
          </button>
        </div>

        <!-- Filtro por tipo -->
        <va-select
          v-model="filterType"
          :options="notificationTypes"
          placeholder="Filtrar por tipo"
          class="type-filter"
          style="width: 200px"
          clearable
        >
          <template #prepend>
            <va-icon name="category" size="small" />
          </template>
        </va-select>
      </div>

      <va-button
        v-if="unreadCount > 0"
        color="success"
        @click="markAllAsRead"
        size="small"
        icon="done_all"
      >
        Marcar todas como leídas
      </va-button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
      <p>Cargando notificaciones...</p>
    </div>

    <!-- Notifications List with Grouping -->
    <div v-else-if="notifications.length > 0" class="notifications-list">
      <div v-for="(group, dateLabel) in groupedNotifications" :key="dateLabel" class="date-group-wrapper">
        <div class="date-group-header">
          <va-icon :name="getDateIcon(dateLabel)" size="1rem" />
          <span>{{ dateLabel }}</span>
          <div class="date-divider"></div>
        </div>

        <transition-group name="notification-list" tag="div" class="notification-group">
          <div
            v-for="notification in group"
            :key="notification.id"
            class="notification-item"
            :class="{ 'unread': !notification.isRead }"
            @click="handleNotificationClick(notification)"
          >
            <div class="notification-icon" :class="`type-${notification.type}`">
              <va-icon :name="getNotificationIcon(notification.type)" size="1.5rem" />
            </div>

            <div class="notification-content">
              <div class="notification-header">
                <h3 class="notification-title">{{ notification.title }}</h3>
                <span class="notification-time">{{ formatTime(notification.createdAt) }}</span>
              </div>

              <p class="notification-message">{{ notification.message }}</p>

              <div v-if="!notification.isRead" class="unread-indicator">
                <span class="unread-badge">
                  <va-icon name="fiber_manual_record" size="0.5rem" />
                  Nueva
                </span>
              </div>
            </div>

            <div class="notification-actions">
              <va-button
                v-if="!notification.isRead"
                preset="plain"
                size="small"
                icon="done"
                color="success"
                @click.stop="markAsRead(notification.id)"
                title="Marcar como leída"
              />
              <va-button
                preset="plain"
                size="small"
                icon="close"
                color="danger"
                @click.stop="deleteNotification(notification.id)"
                title="Eliminar"
              />
            </div>
          </div>
        </transition-group>
      </div>

      <!-- Load More Button -->
      <div v-if="hasMore" class="load-more-section">
        <button class="load-more-btn" @click="loadMore" :disabled="loading">
          <va-icon name="expand_more" />
          Cargar más notificaciones
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <va-icon name="notifications_none" size="4rem" color="#ccc" />
      <h3>No tienes notificaciones</h3>
      <p v-if="viewMode === 'unread'">No hay notificaciones sin leer</p>
      <p v-else-if="viewMode === 'history'">No hay notificaciones en el historial</p>
      <p v-else>Aún no has recibido ninguna notificación</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'

const authStore = useAuthStore()
const { init: initToast } = useToast()

// Estado
const notifications = ref([])
const loading = ref(false)
const unreadCount = ref(0)
const dismissedCount = ref(0) // Contador de notificaciones descartadas
const total = ref(0)
const offset = ref(0)
const limit = 20
const hasMore = ref(false)
const viewMode = ref('all') // 'all', 'unread', 'history'
const filterType = ref(null)

// Opciones de tipos de notificaciones
const notificationTypes = [
  { value: 'new_application', text: 'Nueva aplicación' },
  { value: 'payment_verified', text: 'Pago verificado' },
  { value: 'payment_rejected', text: 'Pago rechazado' },
  { value: 'job_expiring_soon', text: 'Anuncio por vencer' },
  { value: 'application_sent', text: 'Aplicación enviada' },
  { value: 'saved_job_closed', text: 'Trabajo cerrado' },
  { value: 'password_changed', text: 'Contraseña cambiada' }
]

// Cargar notificaciones
const fetchNotifications = async (append = false) => {
  try {
    loading.value = true

    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: append ? offset.value.toString() : '0',
    })

    // Modo de vista
    if (viewMode.value === 'unread') {
      params.append('unread_only', 'true')
    } else if (viewMode.value === 'history') {
      params.append('include_dismissed', 'true')
    }

    if (filterType.value) {
      params.append('type', filterType.value)
    }

    const response = await fetch(`/api/notifications/?${params}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()

      if (append) {
        notifications.value = [...notifications.value, ...data.notifications]
      } else {
        notifications.value = data.notifications
        offset.value = 0
      }

      unreadCount.value = data.unread_count
      dismissedCount.value = data.dismissed_count || 0
      total.value = data.total
      hasMore.value = (offset.value + limit) < data.total

      if (append) {
        offset.value += limit
      }
    }
  } catch (error) {
    console.error('Error al cargar notificaciones:', error)
    initToast({
      message: 'Error al cargar notificaciones',
      color: 'danger',
      duration: 3000,
      position: 'top-right'
    })
  } finally {
    loading.value = false
  }
}

// Marcar como leída
const markAsRead = async (notificationId) => {
  try {
    const response = await fetch(`/api/notifications/${notificationId}/mark-read/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })

    if (response.ok) {
      // Actualizar en el frontend
      const notif = notifications.value.find(n => n.id === notificationId)
      if (notif) {
        notif.isRead = true
        unreadCount.value = Math.max(0, unreadCount.value - 1)
      }
    }
  } catch (error) {
    console.error('Error al marcar como leída:', error)
  }
}

// Marcar todas como leídas
const markAllAsRead = async () => {
  try {
    const response = await fetch('/api/notifications/mark-all-read/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })

    if (response.ok) {
      // Actualizar frontend
      notifications.value.forEach(n => n.isRead = true)
      unreadCount.value = 0

      initToast({
        message: 'Todas las notificaciones marcadas como leídas',
        color: 'success',
        duration: 3000,
        position: 'top-right'
      })
    }
  } catch (error) {
    console.error('Error al marcar todas como leídas:', error)
  }
}

// Descartar/ocultar o eliminar permanentemente notificación
const dismissNotification = async (notificationId) => {
  try {
    // Si estamos en modo historial, eliminar permanentemente
    const isPermanent = viewMode.value === 'history'
    const url = isPermanent
      ? `/api/notifications/${notificationId}/?permanent=true`
      : `/api/notifications/${notificationId}/`

    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      const notif = notifications.value.find(n => n.id === notificationId)

      // Remover del frontend
      notifications.value = notifications.value.filter(n => n.id !== notificationId)

      // Actualizar contadores según la acción
      if (data.action === 'deleted') {
        // Eliminación permanente - reducir contador de descartadas
        dismissedCount.value = Math.max(0, dismissedCount.value - 1)
      } else {
        // Descartada - reducir contador de no leídas si aplica
        if (notif && !notif.isRead) {
          unreadCount.value = Math.max(0, unreadCount.value - 1)
        }
        // Aumentar contador de descartadas
        dismissedCount.value += 1
      }

      total.value = Math.max(0, total.value - 1)

      // Mensaje apropiado según la acción
      const message = data.action === 'deleted'
        ? 'Notificación eliminada permanentemente'
        : 'Notificación descartada'

      initToast({
        message,
        color: data.action === 'deleted' ? 'danger' : 'success',
        duration: 2000,
        position: 'top-right'
      })
    }
  } catch (error) {
    console.error('Error al procesar notificación:', error)
  }
}

// Mantener compatibilidad con el nombre anterior
const deleteNotification = dismissNotification

// Observar cambios en el modo de vista
watch(viewMode, () => {
  fetchNotifications(false)
})

// Cargar más
const loadMore = () => {
  fetchNotifications(true)
}

// Manejar click en notificación
const handleNotificationClick = (notification) => {
  if (!notification.isRead) {
    markAsRead(notification.id)
  }

  // TODO: Navegar a la sección relevante según el tipo de notificación
  // Por ejemplo, si es new_application, ir a la lista de postulantes
}

// Obtener icono según tipo
const getNotificationIcon = (type) => {
  const icons = {
    'new_application': 'person_add',
    'payment_verified': 'verified',
    'payment_rejected': 'cancel',
    'job_expiring_soon': 'schedule',
    'job_expired': 'event_busy',
    'application_sent': 'send',
    'saved_job_closed': 'work_off',
    'blocked_attempt': 'block',
    'password_changed': 'lock',
    'profile_updated': 'edit',
    'system': 'info'
  }
  return icons[type] || 'notifications'
}

// Formatear tiempo relativo
const formatTime = (timestamp) => {
  const now = new Date()
  const date = new Date(timestamp)
  const diff = Math.floor((now - date) / 1000) // segundos

  if (diff < 60) return 'Hace unos segundos'
  if (diff < 3600) return `Hace ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `Hace ${Math.floor(diff / 3600)} h`
  if (diff < 604800) return `Hace ${Math.floor(diff / 86400)} días`

  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
  })
}

// Obtener etiqueta de fecha para agrupar
const getDateLabel = (timestamp) => {
  const now = new Date()
  const date = new Date(timestamp)
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const notifDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
  const diffDays = Math.floor((today - notifDate) / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Hoy'
  if (diffDays === 1) return 'Ayer'
  if (diffDays <= 7) return 'Esta semana'
  if (diffDays <= 30) return 'Este mes'
  return 'Anterior'
}

// Agrupar notificaciones por fecha
const groupedNotifications = computed(() => {
  const groups = {}
  const order = ['Hoy', 'Ayer', 'Esta semana', 'Este mes', 'Anterior']

  notifications.value.forEach(notification => {
    const label = getDateLabel(notification.createdAt)
    if (!groups[label]) {
      groups[label] = []
    }
    groups[label].push(notification)
  })

  // Ordenar según el orden definido
  const sorted = {}
  order.forEach(key => {
    if (groups[key]) {
      sorted[key] = groups[key]
    }
  })

  return sorted
})

// Obtener icono según etiqueta de fecha
const getDateIcon = (dateLabel) => {
  const icons = {
    'Hoy': 'today',
    'Ayer': 'history',
    'Esta semana': 'date_range',
    'Este mes': 'calendar_month',
    'Anterior': 'archive'
  }
  return icons[dateLabel] || 'calendar_today'
}

// Watchers
watch(filterType, () => {
  offset.value = 0
  fetchNotifications(false)
})

// Lifecycle
onMounted(() => {
  fetchNotifications()
})
</script>

<style scoped>
.notifications-container {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.section-header {
  margin-bottom: 2rem;
}

.header-content h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.section-subtitle {
  color: #6b7280;
  font-size: 0.95rem;
  margin: 0;
}

/* Stats Summary */
.stats-summary {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex: 1;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

/* Action Bar */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Filter Chips */
.filter-chips {
  display: flex;
  gap: 0.5rem;
  background: #f3f4f6;
  padding: 0.25rem;
  border-radius: 10px;
}

.filter-chip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: #6b7280;
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.filter-chip:hover {
  background: #e5e7eb;
  color: #374151;
}

.filter-chip.active {
  background: white;
  color: #7c3aed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chip-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  padding: 0 0.4rem;
  background: #e5e7eb;
  color: #4b5563;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.filter-chip.active .chip-badge {
  background: #ede9fe;
  color: #7c3aed;
}

.chip-badge.unread {
  background: #fee2e2;
  color: #dc2626;
  animation: pulse-badge 2s ease-in-out infinite;
}

@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.loading-state p {
  margin-top: 1rem;
  color: #6b7280;
}

/* Notifications List */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Date Group Header */
.date-group-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: #6b7280;
  font-weight: 600;
  font-size: 0.9rem;
}

.date-group-header .va-icon {
  color: #9333ea;
}

.date-divider {
  flex: 1;
  height: 2px;
  background: linear-gradient(to right, #e5e7eb, transparent);
}

.notification-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Notification Item */
.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border-left: 3px solid transparent;
  position: relative;
  overflow: hidden;
}

.notification-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(147, 51, 234, 0.02), transparent);
  opacity: 0;
  transition: opacity 0.25s ease;
}

.notification-item:hover::before {
  opacity: 1;
}

.notification-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.notification-item.unread {
  border-left-color: #7c3aed;
  background: linear-gradient(to right, #faf5ff 0%, white 15%);
}

.notification-item.unread::before {
  background: linear-gradient(135deg, rgba(147, 51, 234, 0.04), transparent);
  opacity: 1;
}

.notification-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
}

.notification-icon.type-new_application {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.notification-icon.type-payment_verified {
  background: linear-gradient(135deg, #10b981, #059669);
}

.notification-icon.type-payment_rejected {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.notification-icon.type-application_sent {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.notification-icon.type-job_expiring_soon,
.notification-icon.type-job_expired {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.notification-icon.type-saved_job_closed {
  background: linear-gradient(135deg, #64748b, #475569);
}

.notification-icon.type-password_changed {
  background: linear-gradient(135deg, #0891b2, #0e7490);
}

.notification-content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.notification-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.notification-time {
  font-size: 0.8rem;
  color: #9ca3af;
  white-space: nowrap;
}

.notification-message {
  color: #4b5563;
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.5;
}

.unread-indicator {
  margin-top: 0.5rem;
}

.unread-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.85rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  box-shadow: 0 2px 4px rgba(124, 58, 237, 0.3);
  animation: badge-glow 2s ease-in-out infinite;
}

@keyframes badge-glow {
  0%, 100% {
    box-shadow: 0 2px 4px rgba(124, 58, 237, 0.3);
  }
  50% {
    box-shadow: 0 2px 8px rgba(124, 58, 237, 0.5);
  }
}

.notification-actions {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  position: relative;
  z-index: 1;
}

/* Transition Animations */
.notification-list-enter-active,
.notification-list-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.notification-list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.notification-list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.notification-list-move {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.empty-state h3 {
  margin: 1rem 0 0.5rem;
  color: #1f2937;
  font-size: 1.25rem;
}

.empty-state p {
  color: #9ca3af;
  font-size: 0.95rem;
  margin: 0;
}

/* Load More */
.load-more-section {
  text-align: center;
  margin-top: 1.5rem;
}

.load-more-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  color: #4b5563;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.load-more-btn:hover:not(:disabled) {
  border-color: #9333ea;
  color: #9333ea;
  transform: translateY(-2px);
}

.load-more-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .notifications-container {
    padding: 1rem;
  }

  .header-content h2 {
    font-size: 1.5rem;
  }

  .stats-summary {
    flex-direction: column;
  }

  .action-bar {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .filter-controls {
    flex-direction: column;
    width: 100%;
  }

  .filter-chips {
    width: 100%;
    justify-content: center;
  }

  .filter-chip {
    flex: 1;
    justify-content: center;
  }

  .type-filter {
    width: 100% !important;
  }

  .notification-item {
    padding: 1rem;
  }

  .notification-icon {
    width: 40px;
    height: 40px;
  }

  .notification-header {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  .notification-title {
    font-size: 0.95rem;
  }

  .notification-message {
    font-size: 0.85rem;
  }

  .date-group-header {
    font-size: 0.85rem;
  }

  .notification-actions {
    flex-direction: row;
    margin-top: 0.5rem;
  }
}

@media (max-width: 480px) {
  .stat-card {
    padding: 0.75rem 1rem;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
  }

  .stat-value {
    font-size: 1.25rem;
  }

  .filter-chip {
    font-size: 0.85rem;
    padding: 0.4rem 0.75rem;
  }

  .chip-badge {
    min-width: 20px;
    height: 20px;
    font-size: 0.7rem;
  }
}
</style>
