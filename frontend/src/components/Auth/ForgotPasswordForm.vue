<template>
  <div class="forgot-password-container">
    <!-- Gradiente animado de fondo -->
    <div class="gradient-bg"></div>
    <div class="gradient-blob blob-1"></div>
    <div class="gradient-blob blob-2"></div>

    <div class="forgot-password-content">
      <!-- Card principal -->
      <div class="forgot-password-card">
        <!-- Header -->
        <div class="card-header">
          <div class="logo-circle">
            <img src="@/assets/guiaspurpuras.ico" alt="Guías Púrpuras" class="logo-img" />
          </div>
          <h1>¿Olvidaste tu contraseña?</h1>
          <p>Te ayudaremos a recuperar tu cuenta</p>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="handleForgotPassword" class="forgot-form">
          <!-- Email Input -->
          <div class="form-group">
            <label for="email" class="form-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
              </svg>
              Correo Electrónico
            </label>
            <div class="input-wrapper">
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
              <span v-if="validationErrors.email" class="input-error-text">{{ validationErrors.email }}</span>
            </div>
          </div>

          <!-- Info Message -->
          <div v-if="!successMessage" class="info-banner">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            Te enviaremos un enlace para restablecer tu contraseña
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
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
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

        <!-- Divider -->
        <div class="divider">
          <span>Recuerda tu contraseña?</span>
        </div>

        <!-- Login Link -->
        <router-link to="/login" class="btn-login-link">
          Volver a Iniciar Sesión
        </router-link>
      </div>

      <!-- Footer -->
      <div class="auth-footer">
        <p>2024 © Guías Púrpuras. Todos los derechos reservados.</p>
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
</script>

<style scoped>
/* Contenedor principal */
.forgot-password-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: #0f0c29;
}

/* Gradiente animado de fondo - Efecto dinámico */
.gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    -45deg,
    #0f0c29 0%,
    #1a1847 25%,
    #302b63 50%,
    #2a1f5e 75%,
    #24243e 100%
  );
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  z-index: 0;
}

/* Blobs animados con efecto de pulsación */
.gradient-blob {
  position: absolute;
  border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
  opacity: 0.25;
  mix-blend-mode: screen;
  filter: blur(40px);
  z-index: 1;
}

.blob-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 50%, #c084fc 100%);
  top: -150px;
  left: -150px;
  animation: blobFloat1 20s ease-in-out infinite;
  box-shadow: 0 0 100px rgba(124, 58, 237, 0.4);
}

.blob-2 {
  width: 450px;
  height: 450px;
  background: linear-gradient(135deg, #6d28d9 0%, #a78bfa 100%);
  bottom: -200px;
  right: -150px;
  animation: blobFloat2 25s ease-in-out infinite;
  box-shadow: 0 0 80px rgba(109, 40, 217, 0.3);
}

/* Blob adicional para más dimensionalidad */
.gradient-blob::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 50%, rgba(124, 58, 237, 0.2), transparent 70%);
  border-radius: inherit;
  animation: pulse 4s ease-in-out infinite;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes blobFloat1 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(50px, -80px) scale(1.05);
  }
  50% {
    transform: translate(-30px, 40px) scale(0.95);
  }
  75% {
    transform: translate(100px, -50px) scale(1.08);
  }
}

@keyframes blobFloat2 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(-60px, 80px) scale(0.95);
  }
  50% {
    transform: translate(40px, -60px) scale(1.08);
  }
  75% {
    transform: translate(-80px, 30px) scale(1.02);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.2;
    transform: scale(1);
  }
  50% {
    opacity: 0.4;
    transform: scale(1.1);
  }
}

/* Contenido principal */
.forgot-password-content {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* Card principal */
.forgot-password-card {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 20px;
  box-shadow:
    0 8px 32px 0 rgba(124, 58, 237, 0.25),
    0 20px 60px rgba(109, 40, 217, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.6);
  padding: 48px 40px;
  backdrop-filter: blur(10px);
  border: 1.5px solid rgba(124, 58, 237, 0.2);
  animation: slideUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  overflow: hidden;
}

.forgot-password-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  animation: shimmer 3s infinite;
  z-index: -1;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* Header */
.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-circle {
  width: 70px;
  height: 70px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.3);
}

.logo-img {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

@keyframes popIn {
  0% {
    transform: scale(0);
  }
  70% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.card-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.card-header p {
  color: #666;
  font-size: 14px;
  margin: 0;
}

/* Formulario */
.forgot-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.label-icon {
  width: 16px;
  height: 16px;
  color: #667eea;
}

.input-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
  background: #f9f9f9;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
  background-color: #f0f0f0;
  color: #999;
  cursor: not-allowed;
}

.form-input.input-error {
  border-color: #ff6b6b;
}

.form-input.input-error:focus {
  box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.1);
}

.input-error-text {
  font-size: 12px;
  color: #ff6b6b;
  margin-top: 4px;
  animation: shake 0.3s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* Info banner */
.info-banner {
  padding: 12px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.info-banner svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

/* Success banner */
.success-banner {
  padding: 12px 16px;
  background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
  color: white;
  border-radius: 8px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: slideDown 0.3s ease-out;
}

.success-banner svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

/* Error banner */
.error-banner {
  padding: 12px 16px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%);
  color: white;
  border-radius: 8px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: slideDown 0.3s ease-out;
}

.error-banner svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
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

.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Botón principal */
.btn-submit {
  padding: 12px 24px;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.4);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-submit.btn-loading {
  pointer-events: none;
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

/* Divisor */
.divider {
  position: relative;
  margin: 24px 0;
  text-align: center;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 1px;
  background: #e8e8e8;
}

.divider span {
  position: relative;
  background: white;
  padding: 0 16px;
  color: #999;
  font-size: 13px;
}

/* Botón de login */
.btn-login-link {
  padding: 12px 24px;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  text-align: center;
  display: block;
}

.btn-login-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.4);
}

/* Footer */
.auth-footer {
  text-align: center;
  padding: 24px 0;
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
}

.auth-footer p {
  margin: 0;
}

/* Responsive */
@media (max-width: 500px) {
  .forgot-password-content {
    padding: 16px;
    max-width: 100%;
  }

  .forgot-password-card {
    padding: 32px 24px;
  }

  .card-header h1 {
    font-size: 24px;
  }

  .blob-1, .blob-2 {
    opacity: 0.15;
  }
}
</style>
