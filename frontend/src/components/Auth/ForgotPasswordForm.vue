<template>
  <div class="forgot-password-container">
    <!-- Lado izquierdo: Formulario -->
    <div class="forgot-password-left">
      <!-- Back Button -->
      <button @click="goHome" class="btn-back" type="button" title="Volver al inicio">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>

      <div class="form-wrapper">
        <!-- Logo y Header -->
        <div class="forgot-password-header">
          <div class="logo-circle">
            <img src="@/assets/guiaspurpuras.ico" alt="Guías Púrpuras" class="logo-img" />
          </div>
          <h1>¿Olvidaste tu contraseña?</h1>
          <p>Te enviaremos un enlace para restablecer tu contraseña</p>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="handleForgotPassword" class="forgot-form">
          <!-- Email Input -->
          <div class="form-group">
            <label for="email" class="form-label">Correo Electrónico</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
              </svg>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                class="form-input"
                :class="{ 'input-error': validationErrors.email }"
                placeholder="tu@email.com"
                required
                :disabled="isLoading"
                @blur="validateEmail"
              />
            </div>
            <span v-if="validationErrors.email" class="input-error-text">{{ validationErrors.email }}</span>
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
            <span>{{ isLoading ? 'Enviando...' : 'Enviar enlace de recuperación' }}</span>
          </button>
        </form>

        <!-- Login Link -->
        <div class="login-section">
          <p class="login-text">¿Recordaste tu contraseña?</p>
          <router-link to="/login" class="btn-login-link">
            Volver a Iniciar Sesión
          </router-link>
        </div>
      </div>
    </div>

    <!-- Lado derecho: Panel de marca -->
    <div class="forgot-password-right">
      <div class="brand-overlay"></div>
      <div class="brand-content">
        <div class="brand-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          <span>Recuperación Segura</span>
        </div>

        <h2>Recupera tu acceso de forma segura</h2>
        <p class="brand-description">
          Te enviaremos un enlace seguro a tu correo electrónico para que puedas restablecer tu contraseña.
        </p>

        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Proceso Seguro</h3>
              <p>Enlace de recuperación encriptado</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Enlace Temporal</h3>
              <p>Válido por 1 hora solamente</p>
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
              <h3>Verificación</h3>
              <p>Revisa tu bandeja de entrada</p>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estado del formulario
const formData = ref({
  email: ''
})

const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const validationErrors = ref({
  email: ''
})

// Validaciones
const isFormValid = computed(() => {
  return formData.value.email && !validationErrors.value.email
})

const validateEmail = () => {
  if (!formData.value.email) {
    validationErrors.value.email = 'El correo es requerido'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) {
    validationErrors.value.email = 'Correo inválido'
  } else {
    validationErrors.value.email = ''
  }
}

const handleForgotPassword = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  validateEmail()

  if (!isFormValid.value) {
    return
  }

  isLoading.value = true

  try {
    const response = await fetch('http://localhost:8000/api/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: formData.value.email })
    })

    const data = await response.json()

    if (!response.ok || !data.success) {
      throw new Error(data.message || 'Error al solicitar recuperación')
    }

    successMessage.value = data.message || 'Revisa tu correo para continuar'

    // Redirigir después de un delay
    setTimeout(() => {
      router.push('/login')
    }, 3000)

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
.forgot-password-container {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: white;
}

/* ========== LADO IZQUIERDO: FORMULARIO ========== */
.forgot-password-left {
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

.forgot-password-header {
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

.forgot-password-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.75rem 0;
  letter-spacing: -0.03em;
}

.forgot-password-header p {
  color: #6b7280;
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
  max-width: 360px;
  margin-left: auto;
  margin-right: auto;
}

/* Formulario */
.forgot-form {
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
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #9ca3af;
  pointer-events: none;
  z-index: 1;
}

.form-input {
  padding: 0.875rem 1rem 0.875rem 2.875rem;
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
.forgot-password-right {
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
/* Tablets y pantallas medianas */
@media (max-width: 1024px) {
  .forgot-password-container {
    grid-template-columns: 1fr;
  }

  .forgot-password-right {
    display: none;
  }

  .forgot-password-left {
    padding: 2rem 1.5rem;
  }

  .btn-back {
    top: 1.5rem;
    left: 1.5rem;
  }
}

/* Móviles grandes (hasta 640px) */
@media (max-width: 640px) {
  .forgot-password-left {
    padding: 1.5rem 1rem;
  }

  .btn-back {
    top: 1rem;
    left: 1rem;
    width: 40px;
    height: 40px;
  }

  .form-wrapper {
    max-width: 100%;
  }

  .forgot-password-header {
    margin-bottom: 2rem;
  }

  .logo-circle {
    width: 60px;
    height: 60px;
  }

  .logo-img {
    width: 36px;
    height: 36px;
  }

  .forgot-password-header h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .forgot-password-header p {
    font-size: 0.875rem;
  }

  .forgot-password-form {
    gap: 1.25rem;
  }

  .form-label {
    font-size: 0.875rem;
  }

  .form-input {
    font-size: 16px !important; /* Previene zoom en iOS */
    min-height: 48px; /* Mejor área táctil */
    padding: 0.75rem 1rem 0.75rem 2.75rem;
  }

  .input-icon {
    width: 18px;
    height: 18px;
  }

  .btn-primary {
    min-height: 48px;
    font-size: 1rem;
    padding: 0.875rem 1.5rem;
  }

  .btn-login-link {
    min-height: 48px;
    font-size: 0.9375rem;
  }
}

/* Móviles pequeños (hasta 375px) */
@media (max-width: 375px) {
  .forgot-password-left {
    padding: 1rem 0.875rem;
  }

  .forgot-password-header h1 {
    font-size: 1.375rem;
  }

  .forgot-password-header p {
    font-size: 0.8125rem;
  }

  .forgot-password-form {
    gap: 1rem;
  }

  .form-input {
    padding: 0.625rem 0.875rem 0.625rem 2.5rem;
  }

  .input-icon {
    left: 0.875rem;
  }
}
</style>
