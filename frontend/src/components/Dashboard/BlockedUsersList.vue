<!-- frontend/src/components/Dashboard/BlockedUsersList.vue -->
<template>
  <div class="blocked-users-container">
    <!-- Header -->
    <div class="section-header">
      <div class="header-content">
        <h2>Usuarios Bloqueados</h2>
        <p class="section-subtitle">Lista de postulantes bloqueados automáticamente por el sistema</p>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar" v-if="blockedUsers.length > 0">
      <div class="search-box">
        <va-icon name="search" />
        <va-input
          v-model="searchQuery"
          placeholder="Buscar por nombre o email..."
          type="text"
          clearable
          class="search-input"
        />
      </div>

      <div class="filter-controls">
        <va-select
          v-model="filterReason"
          :options="reasonOptions"
          placeholder="Filtrar por motivo"
          clearable
          class="filter-select"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
      <p>Cargando usuarios bloqueados...</p>
    </div>

    <!-- Blocked Users List -->
    <div v-else-if="filteredBlockedUsers.length > 0" class="blocked-users-list">
      <div
        v-for="blockedUser in filteredBlockedUsers"
        :key="blockedUser.id"
        class="blocked-user-card"
      >
        <!-- Card Header -->
        <div class="card-header">
          <div class="user-info">
            <div class="user-avatar">
              <va-icon name="person" size="1.5rem" />
            </div>
            <div class="user-details">
              <h3 class="user-name">{{ blockedUser.firstName }} {{ blockedUser.lastName }}</h3>
              <p class="user-email">{{ blockedUser.email }}</p>
            </div>
          </div>
          <div class="block-badge">
            <va-icon name="block" size="small" />
            <span>BLOQUEADO</span>
          </div>
        </div>

        <!-- Reason Section -->
        <div class="reason-section">
          <div class="reason-item">
            <span class="label">Motivo:</span>
            <span class="value" :class="`reason-${blockedUser.reason}`">
              {{ blockedUser.reasonDisplay || getReasonLabel(blockedUser.reason) }}
            </span>
          </div>
          <div class="date-item">
            <span class="label">Bloqueado:</span>
            <span class="value">{{ formatDate(blockedUser.blockedAt) }}</span>
          </div>
        </div>

        <!-- Notes Section -->
        <div v-if="blockedUser.notes" class="notes-section">
          <span class="label">Notas:</span>
          <p class="notes-content">{{ blockedUser.notes }}</p>
        </div>

        <!-- Card Actions -->
        <div class="card-actions">
          <button class="action-btn-secondary" @click="handleViewCV(blockedUser.blockedUserId)">
            <va-icon name="description" size="small" />
            Ver CV
          </button>

          <button class="action-btn-danger" @click="handleUnblock(blockedUser.id)">
            <va-icon name="close" size="small" />
            Desbloquear
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <va-icon name="done_all" size="4rem" color="green" />
      <h3>No hay usuarios bloqueados</h3>
      <p>No tienes ningún postulante bloqueado en este momento</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vuestic-ui'
import { useBlockedUsersStore } from '@/stores/useBlockedUsersStore'
import { useAuthStore } from '@/stores/useAuthStore'

// ========== STORES ==========
const blockedUsersStore = useBlockedUsersStore()
const authStore = useAuthStore()
const { init: notify } = useToast()

// ========== DATA ==========
const searchQuery = ref('')
const filterReason = ref('')

const reasonOptions = [
  { text: 'Spam', value: 'spam' },
  { text: 'Comportamiento inapropiado', value: 'inappropriate' },
  { text: 'No calificado repetidamente', value: 'unqualified' },
  { text: 'Otra razón', value: 'other' }
]

// ========== LIFECYCLE ==========
onMounted(() => {
  loadBlockedUsers()
})

// ========== COMPUTED PROPERTIES ==========
const loading = computed(() => blockedUsersStore.loading)
const blockedUsers = computed(() => blockedUsersStore.blockedUsers)

const filteredBlockedUsers = computed(() => {
  let filtered = blockedUsers.value

  // Filter by reason
  if (filterReason.value) {
    filtered = filtered.filter(bu => bu.reason === filterReason.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(bu => {
      const fullName = `${bu.firstName || ''} ${bu.lastName || ''}`.toLowerCase()
      return fullName.includes(query) || bu.email.toLowerCase().includes(query)
    })
  }

  return filtered
})

// ========== METHODS ==========
const loadBlockedUsers = async () => {
  try {
    await blockedUsersStore.loadBlockedUsers(authStore.accessToken)

    if (blockedUsersStore.error) {
      notify({
        message: `Error: ${blockedUsersStore.error}`,
        color: 'danger',
        duration: 5000
      })
    }
  } catch (err) {
    notify({
      message: `Error al cargar usuarios bloqueados: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  }
}

const getReasonLabel = (reason) => {
  const labels = {
    'spam': 'Spam',
    'inappropriate': 'Comportamiento inapropiado',
    'unqualified': 'No calificado repetidamente',
    'other': 'Otra razón'
  }
  return labels[reason] || reason
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const handleViewCV = (userId) => {
  notify({
    message: 'Funcionalidad de CV próximamente...',
    color: 'info'
  })
  // TODO: Navegar a CV detail cuando esté implementado
}

const handleUnblock = async (blockId) => {
  if (confirm('¿Estás seguro de que deseas desbloquear a este postulante?')) {
    try {
      const success = await blockedUsersStore.unblockUser(blockId, authStore.accessToken)

      if (success) {
        notify({
          message: '✅ Postulante desbloqueado exitosamente',
          color: 'success',
          duration: 3000
        })
      } else {
        notify({
          message: `Error: ${blockedUsersStore.error}`,
          color: 'danger',
          duration: 5000
        })
      }
    } catch (err) {
      notify({
        message: `Error al desbloquear: ${err.message}`,
        color: 'danger',
        duration: 5000
      })
    }
  }
}
</script>

<style scoped>
.blocked-users-container {
  padding: 0;
}

/* ========== HEADER ========== */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 2rem;
}

.header-content h2 {
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

.btn-block-user {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-block-user:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
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
  padding: 0.75rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  transition: all 0.2s;
}

.search-box:focus-within {
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.search-box .va-icon {
  color: #999;
  flex-shrink: 0;
}

.search-input {
  width: 100%;
  border: none !important;
  padding: 0 !important;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select {
  flex: 1;
  min-width: 200px;
}

/* ========== LOADING STATE ========== */
.loading-state {
  text-align: center;
  padding: 3rem 2rem;
  background: white;
  border-radius: 12px;
}

.loading-state p {
  margin-top: 1rem;
  color: #666;
}

/* ========== BLOCKED USERS LIST ========== */
.blocked-users-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.blocked-user-card {
  background: white;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.blocked-user-card:hover {
  border-color: #e0e0e0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.blocked-user-card {
  border-left: 4px solid #dc2626;
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f5f5f5;
}

.user-info {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 0.25rem;
}

.user-email {
  color: #666;
  margin: 0;
  font-size: 0.9rem;
}

.block-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #fee2e2;
  color: #991b1b;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
}

/* Reason Section */
.reason-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.reason-item,
.date-item,
.duration-item,
.permanent-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label {
  font-weight: 600;
  color: #666;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.value {
  color: #1a1a1a;
  font-weight: 500;
}

.reason-spam {
  background: #fee2e2;
  color: #991b1b;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

.reason-unqualified {
  background: #fef3c7;
  color: #92400e;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

.reason-other {
  background: #e5e7eb;
  color: #374151;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

.permanent {
  background: #dc2626;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

/* Notes Section */
.notes-section {
  padding: 1rem;
  background: #f5f5f5;
  border-left: 3px solid #7c3aed;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.notes-section .label {
  margin-bottom: 0.5rem;
}

.notes-content {
  color: #666;
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Card Actions */
.card-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  padding-top: 1rem;
  border-top: 1px solid #f5f5f5;
}

.action-btn-secondary,
.action-btn-danger {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.85rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s;
  flex: 1;
  min-width: 120px;
}

.action-btn-secondary {
  background: #f3f4f6;
  color: #1f2937;
  border: 1px solid #e5e7eb;
}

.action-btn-secondary:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
}

.action-btn-danger {
  background: #fee2e2;
  color: #991b1b;
}

.action-btn-danger:hover {
  background: #fecaca;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  background: white;
  border-radius: 12px;
  border: 1px dashed #e0e0e0;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
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
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.explore-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
}

/* ========== MODAL ========== */
.modal-content {
  padding: 1.5rem 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.form-group label {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.radio-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.radio-item input[type="radio"] {
  cursor: pointer;
}

.radio-item span {
  color: #1a1a1a;
  font-weight: 500;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
  }

  .btn-block-user {
    width: 100%;
    justify-content: center;
  }

  .filter-bar {
    flex-direction: column;
  }

  .filter-controls {
    flex-direction: column;
  }

  .filter-select {
    min-width: auto;
  }

  .card-header {
    flex-direction: column;
  }

  .block-badge {
    align-self: flex-start;
  }

  .reason-section {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
  }

  .action-btn-secondary,
  .action-btn-danger {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .section-header h2 {
    font-size: 1.5rem;
  }

  .blocked-user-card {
    padding: 1rem;
  }

  .user-info {
    flex-direction: column;
  }

  .user-avatar {
    width: 40px;
    height: 40px;
  }
}
</style>
