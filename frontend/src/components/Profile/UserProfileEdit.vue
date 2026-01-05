<!-- frontend/src/components/Profile/UserProfileEdit.vue -->
<template>
  <div class="profile-edit-container">
    <div class="edit-header">
      <h2>Mi Perfil</h2>
      <button class="close-btn" @click="$emit('close')" type="button">
        <va-icon name="close" />
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="profileStore.isLoading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
    </div>

    <!-- Form -->
    <form v-else @submit.prevent="handleSaveProfile" class="profile-form">
      <!-- Avatar Upload Section -->
      <div class="avatar-section">
        <h3 class="section-title">Foto de Perfil</h3>
        <avatar-upload :user-profile-id="userProfileId" />
      </div>

      <!-- Tip Section -->
      <div class="tip-box">
        <va-icon name="info" size="small" />
        <p>
          <strong>Consejo Profesional:</strong> Una foto de perfil con vestimenta formal y fondo neutro aumenta significativamente
          tus posibilidades de ser contactado. Los reclutadores valoran la presentación profesional desde el primer vistazo.
        </p>
      </div>

      <!-- Nombre Completo -->
      <div class="form-group">
        <label class="form-label">Nombre Completo *</label>
        <va-input
          v-model="formData.fullName"
          placeholder="Juan Pérez"
          class="form-input"
          required
        />
      </div>

      <!-- Email (readonly) -->
      <div class="form-group">
        <label class="form-label">Email (No editable)</label>
        <va-input
          :model-value="formData.email"
          disabled
          class="form-input"
        />
      </div>

      <!-- WhatsApp -->
      <div class="form-group">
        <label class="form-label">WhatsApp</label>
        <va-input
          v-model="formData.phone"
          placeholder="591XXXXXXXXX (sin espacios ni guiones)"
          type="tel"
          class="form-input"
        />
        <p class="field-hint">Número de WhatsApp para que los reclutadores te contacten directamente</p>
      </div>

      <!-- Ubicación -->
      <div class="form-group">
        <label class="form-label">Ubicación</label>
        <va-input
          v-model="formData.location"
          placeholder="La Paz, Bolivia"
          class="form-input"
        />
      </div>

      <!-- Biografía -->
      <div class="form-group">
        <label class="form-label">Biografía</label>
        <va-textarea
          v-model="formData.bio"
          placeholder="Cuéntanos sobre ti..."
          rows="4"
          class="form-textarea"
        />
      </div>

      <!-- Form Actions -->
      <div class="form-actions">
        <button
          type="submit"
          class="btn-save"
          :disabled="profileStore.isLoading"
        >
          <va-icon name="save" />
          {{ profileStore.isLoading ? 'Guardando...' : 'Guardar' }}
        </button>

        <button
          type="button"
          class="btn-cancel"
          @click="$emit('close')"
          :disabled="profileStore.isLoading"
        >
          <va-icon name="close" />
          Cancelar
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useToast } from 'vuestic-ui'
import { useProfileStore } from '@/stores/useProfileStore'
import AvatarUpload from './AvatarUpload.vue'

// ========== COMPOSABLES ==========
const { init: notify } = useToast()
const profileStore = useProfileStore()

// ========== PROPS ==========
const props = defineProps({
  userProfileId: {
    type: String,
    required: true
  }
})

// ========== EMITS ==========
const emit = defineEmits(['close', 'updated'])

// ========== DATA ==========
const formData = ref({
  fullName: '',
  email: '',
  phone: '',
  location: '',
  bio: ''
})

// ========== LIFECYCLE ==========
onMounted(() => {
  if (props.userProfileId) {
    loadUserProfile()
  }
})

// Observar cambios en userProfileId
watch(() => props.userProfileId, (newId) => {
  if (newId) {
    loadUserProfile()
  }
})

// ========== METHODS ==========
const loadUserProfile = async () => {
  const result = await profileStore.getProfileById(props.userProfileId)

  if (result.success) {
    formData.value = {
      fullName: result.profile.fullName,
      email: result.profile.email,
      phone: result.profile.phone || '',
      location: result.profile.location || '',
      bio: result.profile.bio || ''
    }
  } else {
    notify({
      message: `Error: ${result.error}`,
      color: 'danger',
      duration: 5000
    })
  }
}

const handleSaveProfile = async () => {
  try {
    // Validación
    if (!formData.value.fullName.trim()) {
      notify({
        message: 'El nombre es requerido',
        color: 'warning',
        duration: 3000
      })
      return
    }

    const result = await profileStore.updateProfile(props.userProfileId, {
      fullName: formData.value.fullName,
      phone: formData.value.phone,
      location: formData.value.location,
      bio: formData.value.bio
    })

    if (result.success) {
      notify({
        message: 'Perfil actualizado exitosamente',
        color: 'success',
        duration: 5000
      })
      emit('updated', result.profile)
      setTimeout(() => emit('close'), 1000)
    } else {
      notify({
        message: `Error: ${result.error}`,
        color: 'danger',
        duration: 5000
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
.profile-edit-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.edit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.edit-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6B7280;
}

.close-btn:hover {
  background: #FEE2E2;
  border-color: #FCA5A5;
  color: #DC2626;
}

.close-btn:active {
  background: #FECACA;
}

.loading-state {
  text-align: center;
  padding: 2rem;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.avatar-section {
  padding: 1.5rem;
  background: #F9FAFB;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tip-box {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #F3E8FF, #EDE9FE);
  border-left: 4px solid #7c3aed;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.tip-box .va-icon {
  color: #7c3aed;
  margin-top: 0.125rem;
  flex-shrink: 0;
}

.tip-box p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #4C1D95;
}

.tip-box strong {
  color: #6d28d9;
  font-weight: 700;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.field-hint {
  font-size: 0.85rem;
  color: #6B7280;
  margin: 0.25rem 0 0 0;
  font-style: italic;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #5C0099;
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f0f0f0;
  justify-content: flex-start;
}

/* Save Button */
.btn-save {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.75rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
}

.btn-save:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35);
  transform: translateY(-2px);
}

.btn-save:active {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(124, 58, 237, 0.25);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Cancel Button */
.btn-cancel {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.75rem;
  background: #DC2626;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.25);
}

.btn-cancel:hover {
  background: #B91C1C;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.35);
  transform: translateY(-2px);
}

.btn-cancel:active {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(220, 38, 38, 0.25);
}

.btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Responsive */
@media (max-width: 768px) {
  .profile-edit-container {
    padding: 1.5rem;
  }

  .edit-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .edit-header h2 {
    font-size: 1.25rem;
  }
}
</style>
