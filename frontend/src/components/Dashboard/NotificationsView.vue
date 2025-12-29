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
        <va-button
          :color="showUnreadOnly ? 'primary' : 'secondary'"
          @click="toggleUnreadFilter"
          size="small"
          icon="filter_list"
        >
          {{ showUnreadOnly ? 'Mostrar todas' : 'Solo no leídas' }}
        </va-button>
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

    <!-- Notifications List -->
    <div v-else-if="notifications.length > 0" class="notifications-list">
      <div
        v-for="notification in notifications"
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
            <span class="unread-badge">Nueva</span>
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
          />
        </div>
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
      <p>{{ showUnreadOnly ? 'No hay notificaciones sin leer' : 'Aún no has recibido ninguna notificación' }}</p>
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
const total = ref(0)
const offset = ref(0)
const limit = 20
const hasMore = ref(false)
const showUnreadOnly = ref(false)

// Cargar notificaciones
const fetchNotifications = async (append = false) => {
  try {
    loading.value = true

    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: append ? offset.value.toString() : '0',
    })

    if (showUnreadOnly.value) {
      params.append('unread_only', 'true')
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

// Toggle filtro no leídas
const toggleUnreadFilter = () => {
  showUnreadOnly.value = !showUnreadOnly.value
  fetchNotifications(false)
}

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

// Watchers
watch(showUnreadOnly, () => {
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
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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
  gap: 0.75rem;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s ease;
  border-left: 4px solid transparent;
}

.notification-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.notification-item.unread {
  border-left-color: #ef4444;
  background: linear-gradient(to right, #fef2f2 0%, white 10%);
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

.notification-content {
  flex: 1;
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
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.notification-actions {
  display: flex;
  align-items: center;
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

  .stats-summary {
    flex-direction: column;
  }

  .action-bar {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .notification-item {
    flex-direction: column;
  }

  .notification-header {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
