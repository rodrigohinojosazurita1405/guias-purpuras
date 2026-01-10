<!-- Componente de Progreso del Perfil -->
<template>
  <div class="profile-progress-card">
    <div class="progress-header">
      <div class="header-left">
        <va-icon name="person" size="large" class="profile-icon" />
        <div>
          <h3 class="progress-title">Completitud del Perfil</h3>
          <p class="progress-subtitle">{{ percentage }}% completado</p>
        </div>
      </div>
      <div class="percentage-badge" :class="getBadgeClass()">
        {{ percentage }}%
      </div>
    </div>

    <!-- Barra de progreso animada -->
    <div class="progress-bar-container">
      <div
        class="progress-bar-fill"
        :class="getBarClass()"
        :style="{ width: percentage + '%' }"
      >
        <div class="progress-shine"></div>
      </div>
    </div>

    <!-- Campos obligatorios -->
    <div class="fields-list">
      <div class="field-item" v-for="field in requiredFields" :key="field.key">
        <div class="field-icon">
          <va-icon
            :name="field.completed ? 'check_circle' : 'radio_button_unchecked'"
            :class="{ completed: field.completed }"
            size="small"
          />
        </div>
        <span class="field-label" :class="{ completed: field.completed }">
          {{ field.label }}
        </span>
      </div>
    </div>

    <!-- Botón de acción -->
    <button
      v-if="percentage < 100"
      class="complete-profile-btn"
      @click="$emit('goToProfile')"
    >
      <va-icon name="edit" size="small" />
      <span>Completar Perfil</span>
    </button>
    <div v-else class="success-message">
      <va-icon name="celebration" size="small" />
      <span>¡Perfil completo! Estás listo para postular</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// ========== PROPS ==========
const props = defineProps({
  percentage: {
    type: Number,
    default: 0
  },
  requiredFields: {
    type: Array,
    default: () => []
    // Formato: [{ key: 'photo', label: 'Foto de perfil', completed: true }]
  }
})

// ========== EMITS ==========
defineEmits(['goToProfile'])

// ========== COMPUTED ==========
const getBadgeClass = () => {
  if (props.percentage >= 80) return 'badge-success'
  if (props.percentage >= 50) return 'badge-warning'
  return 'badge-danger'
}

const getBarClass = () => {
  if (props.percentage >= 80) return 'bar-success'
  if (props.percentage >= 50) return 'bar-warning'
  return 'bar-danger'
}
</script>

<style scoped>
.profile-progress-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #E5E7EB;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* ========== HEADER ========== */
.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
}

.progress-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1F2937;
}

.progress-subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.percentage-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.badge-success {
  background: linear-gradient(135deg, #10B981, #059669);
  color: white;
}

.badge-warning {
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
}

.badge-danger {
  background: linear-gradient(135deg, #EF4444, #DC2626);
  color: white;
}

/* ========== PROGRESS BAR ========== */
.progress-bar-container {
  position: relative;
  width: 100%;
  height: 12px;
  background: #F3F4F6;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.progress-bar-fill {
  position: relative;
  height: 100%;
  border-radius: 20px;
  transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.bar-success {
  background: linear-gradient(90deg, #10B981, #059669);
}

.bar-warning {
  background: linear-gradient(90deg, #F59E0B, #D97706);
}

.bar-danger {
  background: linear-gradient(90deg, #EF4444, #DC2626);
}

/* Efecto de brillo en la barra */
.progress-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: shine 2s infinite;
}

@keyframes shine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* ========== FIELDS LIST ========== */
.fields-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.field-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.field-item:hover {
  background-color: #F9FAFB;
}

.field-icon .va-icon {
  color: #D1D5DB;
  transition: color 0.3s ease;
}

.field-icon .va-icon.completed {
  color: #10B981;
}

.field-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
  transition: color 0.3s ease;
}

.field-label.completed {
  color: #1F2937;
  font-weight: 600;
}

/* ========== BUTTON ========== */
.complete-profile-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.875rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.complete-profile-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
}

.complete-profile-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(124, 58, 237, 0.3);
}

.success-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
  border-radius: 8px;
  color: #065F46;
  font-weight: 600;
  font-size: 0.95rem;
}

.success-message .va-icon {
  color: #10B981;
}
</style>
