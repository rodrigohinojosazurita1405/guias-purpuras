<!-- frontend/src/components/Dashboard/MessagesView.vue -->
<template>
  <div class="messages-wrapper">
    <div class="messages-container">
      <!-- Header -->
      <div class="messages-header">
        <h1>Mensajes y Notificaciones</h1>
        <p class="subtitle">Gestiona tus comunicaciones y alertas</p>
      </div>

      <!-- Tabs -->
      <div class="messages-tabs">
        <button
          class="tab-button"
          :class="{ active: activeTab === 'notifications' }"
          @click="activeTab = 'notifications'"
        >
          <va-icon name="notifications" size="small" />
          <span>Notificaciones</span>
          <span v-if="unreadNotifications > 0" class="badge">{{ unreadNotifications }}</span>
        </button>
        <button
          class="tab-button"
          :class="{ active: activeTab === 'contacts' }"
          @click="activeTab = 'contacts'"
        >
          <va-icon name="people" size="small" />
          <span>Contactos</span>
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <va-progress-bar indeterminate color="purple" size="large" />
        <p>Cargando mensajes...</p>
      </div>

      <!-- Notificaciones Tab -->
      <div v-else-if="activeTab === 'notifications'" class="tab-content">
        <!-- Empty State -->
        <div v-if="notifications.length === 0" class="empty-state">
          <va-icon name="notifications_none" size="4rem" color="#9CA3AF" />
          <h3>No tienes notificaciones</h3>
          <p>Las alertas sobre postulaciones y actividad aparecerán aquí</p>
        </div>

        <!-- Notifications List -->
        <div v-else class="notifications-list">
          <div
            v-for="notification in notifications"
            :key="notification.id"
            class="notification-card"
            :class="{ unread: !notification.read }"
          >
            <div class="notification-icon" :class="notification.type">
              <va-icon :name="getNotificationIcon(notification.type)" />
            </div>
            <div class="notification-content">
              <h4>{{ notification.title }}</h4>
              <p>{{ notification.message }}</p>
              <span class="notification-time">{{ formatTime(notification.createdAt) }}</span>
            </div>
            <button
              v-if="!notification.read"
              class="mark-read-btn"
              @click="markAsRead(notification.id)"
              title="Marcar como leída"
            >
              <va-icon name="done" size="small" />
            </button>
          </div>
        </div>
      </div>

      <!-- Contactos Tab -->
      <div v-else-if="activeTab === 'contacts'" class="tab-content">
        <!-- Search -->
        <div class="search-box">
          <va-icon name="search" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar contactos..."
            class="search-input"
          />
        </div>

        <!-- Empty State -->
        <div v-if="filteredContacts.length === 0" class="empty-state">
          <va-icon name="people_outline" size="4rem" color="#9CA3AF" />
          <h3>No tienes contactos aún</h3>
          <p v-if="authStore.user?.role === 'company'">
            Los candidatos que postulen a tus anuncios aparecerán aquí
          </p>
          <p v-else>
            Las empresas a las que postules aparecerán aquí
          </p>
        </div>

        <!-- Contacts List -->
        <div v-else class="contacts-list">
          <div
            v-for="contact in filteredContacts"
            :key="contact.id"
            class="contact-card"
          >
            <div class="contact-avatar">
              <va-icon name="person" size="large" />
            </div>
            <div class="contact-info">
              <h4>{{ contact.name }}</h4>
              <p class="contact-meta">{{ contact.email }}</p>
              <p class="contact-context">{{ contact.context }}</p>
            </div>
            <div class="contact-actions">
              <a
                :href="`mailto:${contact.email}`"
                class="contact-btn email"
                title="Enviar email"
              >
                <va-icon name="mail" size="small" />
                <span>Email</span>
              </a>
              <a
                v-if="contact.whatsapp"
                :href="`https://wa.me/${cleanPhone(contact.whatsapp)}`"
                target="_blank"
                class="contact-btn whatsapp"
                title="Contactar por WhatsApp"
              >
                <va-icon name="chat" size="small" />
                <span>WhatsApp</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Info Box -->
      <div class="info-box">
        <va-icon name="info" size="small" color="#7C3AED" />
        <div class="info-text">
          <strong>💬 Chat interno próximamente</strong>
          <p>
            Estamos trabajando en un sistema de mensajería interna completo.
            Por ahora, puedes contactar directamente por email o WhatsApp.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'

// ========== COMPOSABLES ==========
const authStore = useAuthStore()
const { init: notify } = useToast()

// ========== DATA ==========
const loading = ref(false)
const activeTab = ref('notifications')
const searchQuery = ref('')

// Mock data - En el futuro vendrá del backend
const notifications = ref([
  {
    id: 1,
    type: 'application',
    title: 'Nueva postulación recibida',
    message: 'Juan Pérez se postuló a tu anuncio "Desarrollador Full Stack"',
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 horas atrás
    read: false
  },
  {
    id: 2,
    type: 'payment',
    title: 'Pago verificado',
    message: 'Tu pago para el plan Púrpura ha sido verificado exitosamente',
    createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 día atrás
    read: true
  },
  {
    id: 3,
    type: 'expiry',
    title: 'Anuncio próximo a vencer',
    message: 'Tu anuncio "Diseñador UI/UX" vence en 3 días',
    createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 días atrás
    read: false
  }
])

const contacts = ref([
  {
    id: 1,
    name: 'Juan Pérez',
    email: 'juan.perez@example.com',
    whatsapp: '+59177123456',
    context: 'Postulado a: Desarrollador Full Stack',
    lastInteraction: new Date()
  },
  {
    id: 2,
    name: 'María García',
    email: 'maria.garcia@example.com',
    whatsapp: '+59176654321',
    context: 'Postulado a: Diseñador UI/UX',
    lastInteraction: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
  }
])

// ========== COMPUTED ==========
const unreadNotifications = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

const filteredContacts = computed(() => {
  if (!searchQuery.value) return contacts.value

  const query = searchQuery.value.toLowerCase()
  return contacts.value.filter(contact =>
    contact.name.toLowerCase().includes(query) ||
    contact.email.toLowerCase().includes(query) ||
    contact.context.toLowerCase().includes(query)
  )
})

// ========== LIFECYCLE ==========
onMounted(() => {
  loadData()
})

// ========== METHODS ==========
const loadData = async () => {
  try {
    loading.value = true
    // TODO: Cargar notificaciones y contactos desde el backend
    await new Promise(resolve => setTimeout(resolve, 500)) // Simular carga
  } catch (err) {
    console.error('Error cargando datos:', err)
    notify({
      message: 'Error al cargar mensajes',
      color: 'danger'
    })
  } finally {
    loading.value = false
  }
}

const getNotificationIcon = (type) => {
  const icons = {
    'application': 'person_add',
    'payment': 'check_circle',
    'expiry': 'event',
    'message': 'mail',
    'system': 'info'
  }
  return icons[type] || 'notifications'
}

const formatTime = (date) => {
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (hours < 1) return 'Hace unos momentos'
  if (hours < 24) return `Hace ${hours} hora${hours !== 1 ? 's' : ''}`
  if (days < 7) return `Hace ${days} día${days !== 1 ? 's' : ''}`

  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const markAsRead = (notificationId) => {
  const notification = notifications.value.find(n => n.id === notificationId)
  if (notification) {
    notification.read = true
    notify({
      message: 'Notificación marcada como leída',
      color: 'success',
      duration: 2000
    })
  }
}

const cleanPhone = (phone) => {
  // Remover caracteres no numéricos excepto el +
  return phone.replace(/[^\d+]/g, '')
}
</script>

<style scoped>
.messages-wrapper {
  min-height: calc(100vh - 70px);
  background: #f5f5f5;
  padding: 2rem;
}

.messages-container {
  max-width: 1000px;
  margin: 0 auto;
}

/* ========== HEADER ========== */
.messages-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #E5E7EB;
}

.messages-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
}

.subtitle {
  margin: 0.5rem 0 0;
  color: #6B7280;
  font-size: 0.95rem;
}

/* ========== TABS ========== */
.messages-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  background: white;
  padding: 0.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tab-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  color: #6B7280;
  transition: all 0.2s;
  position: relative;
}

.tab-button:hover {
  background: #F3F4F6;
  color: #1F2937;
}

.tab-button.active {
  background: linear-gradient(135deg, #7C3AED, #6D28D9);
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #EF4444;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.4rem;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

/* ========== LOADING ========== */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
}

.loading-state p {
  margin-top: 1rem;
  color: #666;
}

/* ========== TAB CONTENT ========== */
.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== SEARCH ========== */
.search-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  transition: all 0.2s;
}

.search-box:focus-within {
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 0.95rem;
  background: transparent;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.empty-state h3 {
  margin: 1rem 0 0.5rem;
  font-size: 1.25rem;
  color: #1a1a1a;
}

.empty-state p {
  color: #6B7280;
  margin: 0;
}

/* ========== NOTIFICATIONS LIST ========== */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.notification-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  border-left: 4px solid transparent;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.notification-card.unread {
  background: #F9FAFB;
  border-left-color: #7C3AED;
}

.notification-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.notification-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  flex-shrink: 0;
}

.notification-icon.application {
  background: #DBEAFE;
  color: #1E40AF;
}

.notification-icon.payment {
  background: #D1FAE5;
  color: #065F46;
}

.notification-icon.expiry {
  background: #FEF3C7;
  color: #92400E;
}

.notification-icon.message {
  background: #EDE9FE;
  color: #5B21B6;
}

.notification-content {
  flex: 1;
}

.notification-content h4 {
  margin: 0 0 0.25rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1F2937;
}

.notification-content p {
  margin: 0 0 0.5rem;
  font-size: 0.875rem;
  color: #6B7280;
  line-height: 1.5;
}

.notification-time {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.mark-read-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: #F3F4F6;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.mark-read-btn:hover {
  background: #7C3AED;
  color: white;
}

/* ========== CONTACTS LIST ========== */
.contacts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contact-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.contact-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.contact-avatar {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #7C3AED, #6D28D9);
  color: white;
  border-radius: 50%;
  flex-shrink: 0;
}

.contact-info {
  flex: 1;
}

.contact-info h4 {
  margin: 0 0 0.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: #1F2937;
}

.contact-meta {
  margin: 0 0 0.25rem;
  font-size: 0.875rem;
  color: #6B7280;
}

.contact-context {
  margin: 0;
  font-size: 0.8rem;
  color: #9CA3AF;
  font-style: italic;
}

.contact-actions {
  display: flex;
  gap: 0.5rem;
}

.contact-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.contact-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.contact-btn.email {
  background: #7C3AED;
  color: white;
}

.contact-btn.email:hover {
  background: #6D28D9;
}

.contact-btn.whatsapp {
  background: #10B981;
  color: white;
}

.contact-btn.whatsapp:hover {
  background: #059669;
}

/* ========== INFO BOX ========== */
.info-box {
  display: flex;
  gap: 0.75rem;
  padding: 1.25rem;
  background: #F5F3FF;
  border: 1px solid #DDD6FE;
  border-radius: 12px;
  margin-top: 2rem;
}

.info-text {
  flex: 1;
}

.info-text strong {
  display: block;
  color: #5B21B6;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}

.info-text p {
  margin: 0;
  font-size: 0.875rem;
  color: #6D28D9;
  line-height: 1.6;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .messages-wrapper {
    padding: 1rem;
  }

  .messages-header h1 {
    font-size: 1.5rem;
  }

  .tab-button span:not(.badge) {
    display: none;
  }

  .contact-card {
    flex-direction: column;
    text-align: center;
  }

  .contact-actions {
    width: 100%;
    flex-direction: column;
  }

  .contact-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
