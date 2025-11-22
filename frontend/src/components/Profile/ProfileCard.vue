<template>
  <div v-if="profile" class="profile-card">
    <!-- Header with avatar -->
    <div class="card-header">
      <img
        v-if="profile.profilePhoto"
        :src="profile.profilePhoto"
        alt="Avatar"
        class="avatar-image"
      />
      <div v-else class="avatar-placeholder">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      </div>

      <div class="header-info">
        <h3>{{ profile.fullName }}</h3>
        <p class="email">{{ profile.email }}</p>
      </div>

      <button v-if="showEditBtn" class="edit-btn" @click="emit('edit')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
        </svg>
      </button>
    </div>

    <!-- Profile Info -->
    <div class="card-content">
      <!-- Phone -->
      <div v-if="profile.phone" class="info-row">
        <span class="label">Teléfono</span>
        <span class="value">{{ profile.phone }}</span>
      </div>

      <!-- Location -->
      <div v-if="profile.location" class="info-row">
        <span class="label">Ubicación</span>
        <span class="value">{{ profile.location }}</span>
      </div>

      <!-- Bio -->
      <div v-if="profile.bio" class="info-row bio">
        <span class="label">Biografía</span>
        <p class="value">{{ profile.bio }}</p>
      </div>

      <!-- Dates -->
      <div class="info-row timestamps">
        <span class="label">Miembro desde</span>
        <span class="value">{{ formatDate(profile.createdAt) }}</span>
      </div>
    </div>

    <!-- Completion Badge -->
    <div class="card-footer">
      <div class="completion-badge">
        <span>Perfil {{ completionPercentage }}% completado</span>
      </div>
    </div>
  </div>

  <!-- Empty State -->
  <div v-else class="empty-state">
    <div class="empty-icon">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
      </svg>
    </div>
    <h3>Sin Perfil</h3>
    <p>Crea tu perfil para que otros puedan conocerte</p>
    <button class="create-btn" @click="emit('create')">Crear Perfil</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  profile: {
    type: Object,
    default: null
  },
  showEditBtn: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['edit', 'create'])

const completionPercentage = computed(() => {
  if (!props.profile) return 0

  const fields = ['fullName', 'email', 'phone', 'location', 'bio', 'profilePhoto']
  const filledFields = fields.filter(field =>
    props.profile[field] && props.profile[field] !== ''
  ).length

  return Math.round((filledFields / fields.length) * 100)
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}
</script>

<style scoped>
.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.profile-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-header {
  padding: 2rem;
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  color: white;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  position: relative;
}

.avatar-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid white;
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  border: 4px solid white;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.header-info {
  flex: 1;
}

.header-info h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.email {
  margin: 0.25rem 0 0 0;
  opacity: 0.95;
  font-size: 0.95rem;
}

.edit-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid white;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.edit-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.card-content {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-row.bio {
  flex-direction: column;
}

.info-row.timestamps {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.label {
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
  min-width: 120px;
}

.value {
  color: #1a1a2e;
  font-weight: 500;
}

.info-row.bio .label {
  margin-bottom: 0.5rem;
}

.info-row.bio .value {
  display: block;
  margin-top: 0.5rem;
  line-height: 1.5;
  color: #333;
}

.card-footer {
  padding: 1rem 2rem;
  background: #f9f9f9;
  display: flex;
  justify-content: center;
}

.completion-badge {
  background: linear-gradient(135deg, #7c3aed, #10b981);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

/* Empty State */
.empty-state {
  background: white;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  color: #ccc;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.empty-state h3 {
  color: #1a1a2e;
  margin: 1rem 0 0.5rem 0;
  font-size: 1.3rem;
}

.empty-state p {
  color: #666;
  margin: 0 0 1.5rem 0;
}

.create-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

@media (max-width: 600px) {
  .card-header {
    padding: 1.5rem;
    flex-direction: column;
    text-align: center;
  }

  .header-info {
    width: 100%;
  }

  .edit-btn {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
  }

  .card-content {
    padding: 1.5rem;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .label {
    min-width: auto;
    margin-bottom: 0.25rem;
  }
}
</style>
