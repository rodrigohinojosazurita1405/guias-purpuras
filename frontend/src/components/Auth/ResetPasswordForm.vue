<template>
  <div class="reset-password-container">
    <!-- Lado izquierdo: Formulario -->
    <div class="reset-password-left">
      <!-- Back Button -->
      <button @click="goHome" class="btn-back" type="button" title="Volver al inicio">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>

      <div class="form-wrapper">
        <!-- Logo y Header -->
        <div class="reset-password-header">
          <div class="logo-circle">
            <img src="@/assets/guiaspurpuras.ico" alt="Guías Púrpuras" class="logo-img" />
          </div>
          <h1>Restablecer Contraseña</h1>
          <p>Ingresa tu nueva contraseña</p>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="handleResetPassword" class="reset-form">
          <!-- Password Input -->
          <div class="form-group">
            <label for="password" class="form-label">Nueva Contraseña</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                :class="{ 'input-error': validationErrors.password }"
                placeholder="Tu nueva contraseña"
                required
                :disabled="isLoading"
                @blur="validatePassword"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showPassword = !showPassword"
                :disabled="isLoading"
              >
                <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              </button>
            </div>
            <span v-if="validationErrors.password" class="input-error-text">{{ validationErrors.password }}</span>
          </div>

          <!-- Confirm Password Input -->
          <div class="form-group">
            <label for="confirmPassword" class="form-label">Confirmar Contraseña</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
              <input
                id="confirmPassword"
                v-model="formData.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-input"
                :class="{ 'input-error': validationErrors.confirmPassword }"
                placeholder="Confirma tu nueva contraseña"
                required
                :disabled="isLoading"
                @blur="validateConfirmPassword"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showConfirmPassword = !showConfirmPassword"
                :disabled="isLoading"
              >
                <svg v-if="!showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              </button>
            </div>
            <span v-if="validationErrors.confirmPassword" class="input-error-text">{{ validationErrors.confirmPassword }}</span>
          </div>

          <!-- Success Message -->
          <transition name="slide-down">
            <div v-if="successMessage" class="success-banner">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              {{ successMessage }}
            </div>
          </transition>

          <!-- Error Message -->
          <transition name="slide-down">
            <div v-if="errorMessage" class="error-banner">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
              </svg>
              {{ errorMessage }}
            </div>
          </transition>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn-submit"
            :disabled="isLoading || !isFormValid"
            :class="{ 'btn-loading': isLoading }"
          >
            <svg v-if="isLoading" class="spinner" viewBox="0 0 50 50">
              <circle cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
            </svg>
            <span>{{ isLoading ? 'Restableciendo...' : 'Restablecer Contraseña' }}</span>
          </button>
        </form>

        <!-- Login Link -->
        <div class="login-section">
          <p class="login-text">¿Ya restableciste tu contraseña?</p>
          <router-link to="/login" class="btn-login-link">
            Iniciar Sesión
          </router-link>
        </div>
      </div>
    </div>

    <!-- Lado derecho: Panel de marca -->
    <div class="reset-password-right">
      <div class="brand-overlay"></div>
      <div class="brand-content">
        <div class="brand-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          <span>Seguridad Garantizada</span>
        </div>

        <h2>Crea una contraseña segura</h2>
        <p class="brand-description">
          Asegúrate de usar una contraseña única y fuerte para proteger tu cuenta.
        </p>

        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Mínimo 6 caracteres</h3>
              <p>Asegúrate de usar al menos 6 caracteres</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Combina caracteres</h3>
              <p>Usa letras, números y símbolos</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Contraseña única</h3>
              <p>No uses la misma contraseña de otros sitios</p>
            </div>
          </div>
        </div>
      </div>

      <div class="brand-footer">
        <p>{{ currentYear }} © Guías Púrpuras. Todos los derechos reservados.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// Estado del formulario
const formData = ref({
  password: '',
  confirmPassword: ''
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const validationErrors = ref({
  password: '',
  confirmPassword: ''
})

const token = ref('')

// Obtener token de la URL
onMounted(() => {
  token.value = route.params.token || ''
  if (!token.value) {
    errorMessage.value = 'Token inválido. Por favor solicita un nuevo enlace de recuperación.'
  }
})

// Validaciones
const isFormValid = computed(() => {
  return (
    formData.value.password &&
    formData.value.confirmPassword &&
    !validationErrors.value.password &&
    !validationErrors.value.confirmPassword &&
    token.value
  )
})

const validatePassword = () => {
  if (!formData.value.password) {
    validationErrors.value.password = 'La contraseña es requerida'
  } else if (formData.value.password.length < 6) {
    validationErrors.value.password = 'Mínimo 6 caracteres'
  } else {
    validationErrors.value.password = ''
  }
  // Re-validar confirmación si ya tiene valor
  if (formData.value.confirmPassword) {
    validateConfirmPassword()
  }
}

const validateConfirmPassword = () => {
  if (!formData.value.confirmPassword) {
    validationErrors.value.confirmPassword = 'Confirma tu contraseña'
  } else if (formData.value.password !== formData.value.confirmPassword) {
    validationErrors.value.confirmPassword = 'Las contraseñas no coinciden'
  } else {
    validationErrors.value.confirmPassword = ''
  }
}

const handleResetPassword = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  validatePassword()
  validateConfirmPassword()

  if (!isFormValid.value) {
    return
  }

  isLoading.value = true

  try {
    const response = await fetch('http://localhost:8000/api/auth/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        token: token.value,
        password: formData.value.password
      })
    })

    const data = await response.json()

    if (!response.ok || !data.success) {
      throw new Error(data.message || 'Error al restablecer contraseña')
    }

    successMessage.value = data.message || 'Contraseña restablecida exitosamente'

    // Redirigir al login después de un delay
    setTimeout(() => {
      router.push('/login')
    }, 2000)

  } catch (error) {
    errorMessage.value = error.message || 'Error de conexión. Intenta nuevamente.'
  } finally {
    isLoading.value = false
  }
}

const goHome = () => {
  router.push('/')
}

const currentYear = new Date().getFullYear()
</script>

<style scoped>
/* ========== LAYOUT PRINCIPAL ========== */
.reset-password-container {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: white;
}

/* ========== LADO IZQUIERDO: FORMULARIO ========== */
.reset-password-left {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  position: relative;
  background: white;
}

/* Back Button */
.btn-back {
  position: absolute;
  top: 2rem;
  left: 2rem;
  width: 40px;
  height: 40px;
  background: white;
  border: 1px solid #e5e7eb;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  border-radius: 10px;
  padding: 0;
  z-index: 10;
}

.btn-back:hover {
  color: #7c3aed;
  border-color: #7c3aed;
  background: #f9fafb;
}

.btn-back:active {
  transform: scale(0.95);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

.form-wrapper {
  width: 100%;
  max-width: 440px;
}

.reset-password-header {
  margin-bottom: 2.5rem;
  text-align: center;
}

.logo-circle {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, #f3e8ff 0%, #ede9fe 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.75rem auto;
  box-shadow: 0 4px 16px rgba(124, 58, 237, 0.1);
  border: 1px solid rgba(124, 58, 237, 0.1);
}

.logo-img {
  width: 44px;
  height: 44px;
  object-fit: contain;
}

.reset-password-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.75rem 0;
  letter-spacing: -0.03em;
}

.reset-password-header p {
  color: #6b7280;
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
  max-width: 360px;
  margin-left: auto;
  margin-right: auto;
}

/* Formulario */
.reset-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.input-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 0.875rem;
  width: 18px;
  height: 18px;
  color: #9ca3af;
  pointer-events: none;
}

.toggle-password {
  position: absolute;
  right: 1rem;
  top: 0.875rem;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  color: #9ca3af;
  transition: color 0.2s ease;
}

.toggle-password:hover {
  color: #7c3aed;
}

.toggle-password svg {
  width: 18px;
  height: 18px;
}

.form-input {
  padding: 0.875rem 2.875rem 0.875rem 2.875rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  font-size: 0.9375rem;
  font-family: inherit;
  transition: all 0.2s ease;
  background: #fafafa;
  color: #111827;
  min-height: 48px;
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-input:focus {
  outline: none;
  border-color: #7c3aed;
  background: white;
  box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.08);
}

.form-input:disabled {
  background-color: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.form-input.input-error {
  border-color: #ef4444;
}

.form-input.input-error:focus {
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.08);
}

.input-error-text {
  font-size: 0.8125rem;
  color: #ef4444;
  margin-top: 0.25rem;
}

/* Success banner */
.success-banner {
  padding: 0.875rem 1rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-radius: 10px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.success-banner svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* Error banner */
.error-banner {
  padding: 0.875rem 1rem;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-radius: 10px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.error-banner svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from, .slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Botón principal */
.btn-submit {
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-height: 52px;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
}

.btn-submit:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 18px;
  height: 18px;
  stroke: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Sección de login */
.login-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.login-text {
  font-size: 0.9375rem;
  color: #6b7280;
  margin: 0 0 1rem 0;
}

.btn-login-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: white;
  color: #7c3aed;
  font-size: 0.9375rem;
  font-weight: 600;
  border: 2px solid #7c3aed;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.25s ease;
  min-height: 48px;
}

.btn-login-link:hover {
  background: #f3e8ff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
}

.btn-login-link:active {
  transform: translateY(0);
}

/* ========== LADO DERECHO: PANEL DE MARCA ========== */
.reset-password-right {
  background-image: url('@/assets/images/bg2.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 3rem 3rem 2rem 3rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.brand-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(81, 0, 135, 0.92) 0%, rgba(61, 0, 102, 0.95) 100%);
  z-index: 1;
}

.brand-content {
  position: relative;
  z-index: 2;
}

.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  font-size: 0.8125rem;
  font-weight: 600;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.brand-badge svg {
  width: 16px;
  height: 16px;
}

.brand-content h2 {
  font-size: 2.25rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 1.25rem 0;
  letter-spacing: -0.03em;
}

.brand-description {
  font-size: 1.0625rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 2.5rem 0;
}

.features-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.feature-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-icon svg {
  width: 24px;
  height: 24px;
  color: #fbbf24;
}

.feature-text h3 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: white;
}

.feature-text p {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.75);
  margin: 0;
  line-height: 1.5;
}

.brand-footer {
  position: relative;
  z-index: 2;
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
}

.brand-footer p {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .reset-password-container {
    grid-template-columns: 1fr;
  }

  .reset-password-right {
    display: none;
  }

  .reset-password-left {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 500px) {
  .btn-back {
    top: 1rem;
    left: 1rem;
    width: 36px;
    height: 36px;
  }

  .reset-password-left {
    padding: 1.5rem 1rem;
  }

  .reset-password-header h1 {
    font-size: 1.5rem;
  }

  .reset-password-header p {
    font-size: 0.875rem;
  }
}
</style>
