<template>
  <div class="profile-form-container">
    <!-- Header -->
    <div class="form-header">
      <h2>Mi Perfil</h2>
      <p v-if="profileStore.userProfile" class="progress-text">
        Perfil completado al {{ profileStore.profileProgress }}%
      </p>
      <div v-if="profileStore.userProfile" class="progress-bar">
        <div class="progress-fill" :style="{ width: profileStore.profileProgress + '%' }"></div>
      </div>
    </div>

    <!-- Success Message -->
    <div v-if="profileStore.successMessage" class="message-banner success-banner">
      <span>{{ profileStore.successMessage }}</span>
      <button @click="profileStore.clearMessages" class="close-btn">✕</button>
    </div>

    <!-- Error Message -->
    <div v-if="profileStore.error" class="message-banner error-banner">
      <span>{{ profileStore.error }}</span>
      <button @click="profileStore.clearMessages" class="close-btn">✕</button>
    </div>

    <!-- Form -->
    <form @submit.prevent="handleSubmit" class="profile-form">
      <!-- Full Name -->
      <div class="form-group">
        <label for="fullName">Nombre Completo *</label>
        <input
          v-model="formData.fullName"
          type="text"
          id="fullName"
          placeholder="Juan Pérez García"
          required
          @blur="validateField('fullName')"
        />
        <span v-if="validationErrors.fullName" class="error-text">
          {{ validationErrors.fullName }}
        </span>
      </div>

      <!-- Email -->
      <div class="form-group">
        <label for="email">Email *</label>
        <input
          v-model="formData.email"
          type="email"
          id="email"
          placeholder="tu@email.com"
          required
          @blur="validateField('email')"
          disabled
        />
        <span class="help-text">El email no puede ser modificado</span>
      </div>

      <!-- Phone -->
      <div class="form-group">
        <label for="phone">Teléfono</label>
        <input
          v-model="formData.phone"
          type="tel"
          id="phone"
          placeholder="+591 12345678"
          @blur="validateField('phone')"
        />
      </div>

      <!-- Location -->
      <div class="form-group">
        <label for="location">Ubicación</label>
        <input
          v-model="formData.location"
          type="text"
          id="location"
          placeholder="La Paz, Bolivia"
          @blur="validateField('location')"
        />
      </div>

      <!-- Bio -->
      <div class="form-group">
        <label for="bio">Biografía</label>
        <textarea
          v-model="formData.bio"
          id="bio"
          placeholder="Cuéntanos sobre ti..."
          rows="5"
          @blur="validateField('bio')"
        ></textarea>
        <span class="char-count">{{ formData.bio.length }}/500</span>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        class="submit-btn"
        :disabled="profileStore.isLoading || !isFormValid"
        :class="{ loading: profileStore.isLoading }"
      >
        <span v-if="!profileStore.isLoading">
          {{ profileStore.userProfile ? 'Actualizar Perfil' : 'Crear Perfil' }}
        </span>
        <span v-else class="spinner"></span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProfileStore } from '@/stores/useProfileStore'
import { useAuthStore } from '@/stores/useAuthStore'

const profileStore = useProfileStore()
const authStore = useAuthStore()

const formData = ref({
  fullName: '',
  email: '',
  phone: '',
  location: '',
  bio: ''
})

const validationErrors = ref({
  fullName: '',
  email: '',
  phone: '',
  location: '',
  bio: ''
})

const isFormValid = computed(() => {
  return formData.value.fullName.trim() !== '' &&
         formData.value.email.trim() !== '' &&
         Object.values(validationErrors.value).every(error => !error)
})

const validateField = (fieldName) => {
  const value = formData.value[fieldName]

  switch (fieldName) {
    case 'fullName':
      if (!value.trim()) {
        validationErrors.value.fullName = 'El nombre es requerido'
      } else if (value.trim().length < 2) {
        validationErrors.value.fullName = 'El nombre debe tener al menos 2 caracteres'
      } else {
        validationErrors.value.fullName = ''
      }
      break

    case 'phone':
      if (value && value.length < 5) {
        validationErrors.value.phone = 'El teléfono debe ser válido'
      } else {
        validationErrors.value.phone = ''
      }
      break

    case 'bio':
      if (value.length > 500) {
        validationErrors.value.bio = 'La biografía no debe exceder 500 caracteres'
      } else {
        validationErrors.value.bio = ''
      }
      break

    default:
      validationErrors.value[fieldName] = ''
  }
}

const handleSubmit = async () => {
  // Validar todos los campos
  Object.keys(formData.value).forEach(field => {
    validateField(field)
  })

  if (!isFormValid.value) return

  if (profileStore.userProfile) {
    // Update existing profile
    const result = await profileStore.updateProfile(
      profileStore.userProfile.id,
      {
        fullName: formData.value.fullName,
        phone: formData.value.phone,
        location: formData.value.location,
        bio: formData.value.bio
      }
    )

    if (result.success) {
      // Success - message will be shown from store
      setTimeout(() => {
        profileStore.clearMessages()
      }, 3000)
    }
  } else {
    // Create new profile
    const result = await profileStore.createProfile(formData.value)

    if (result.success) {
      // Success - message will be shown from store
      setTimeout(() => {
        profileStore.clearMessages()
      }, 3000)
    }
  }
}

onMounted(async () => {
  // Load user profile if logged in
  if (authStore.isAuthenticated) {
    const result = await profileStore.getProfileByEmail(authStore.user.email)

    if (result.success) {
      formData.value = {
        fullName: result.profile.fullName || '',
        email: result.profile.email || '',
        phone: result.profile.phone || '',
        location: result.profile.location || '',
        bio: result.profile.bio || ''
      }
    }
  }
})
</script>

<style scoped>
.profile-form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-header {
  margin-bottom: 2rem;
}

.form-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 0.5rem;
}

.progress-text {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #7c3aed, #10b981);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.message-banner {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.success-banner {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error-banner {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.close-btn {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.form-group input:disabled {
  background: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  font-size: 0.95rem;
}

.error-text {
  color: #ef4444;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.help-text {
  color: #999;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.char-count {
  color: #999;
  font-size: 0.85rem;
  margin-top: 0.25rem;
  text-align: right;
}

.submit-btn {
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 44px;
}

.submit-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit-btn.loading {
  pointer-events: none;
}

.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 600px) {
  .profile-form-container {
    padding: 1.5rem;
  }

  .form-header h2 {
    font-size: 1.5rem;
  }
}
</style>
