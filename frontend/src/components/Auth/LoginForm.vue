<template>
  <div class="login-container">
    <!-- Gradiente animado de fondo -->
    <div class="gradient-bg"></div>
    <div class="gradient-blob blob-1"></div>
    <div class="gradient-blob blob-2"></div>

    <div class="login-content">
      <!-- Card principal -->
      <div class="login-card">
        <!-- Header -->
        <div class="login-header">
          <div class="logo-circle">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
            </svg>
          </div>
          <h1>Bienvenido</h1>
          <p>Accede a tu cuenta de Guías Púrpuras</p>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="handleLogin" class="login-form">
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

          <!-- Password Input -->
          <div class="form-group">
            <label for="password" class="form-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
              Contraseña
            </label>
            <div class="input-wrapper">
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                :class="{ 'input-error': validationErrors.password }"
                placeholder="Tu contraseña"
                required
                :disabled="isLoading"
                @blur="validatePassword"
              />
              <button
                type="button"
                class="password-toggle"
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
              <span v-if="validationErrors.password" class="input-error-text">{{ validationErrors.password }}</span>
            </div>
          </div>

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

          <!-- Remember Me -->
          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.rememberMe" :disabled="isLoading" />
              <span>Mantener sesión iniciada</span>
            </label>
            <router-link to="/forgot-password" class="forgot-link">¿Olvidaste la contraseña?</router-link>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn-login"
            :disabled="isLoading || !isFormValid"
            :class="{ 'btn-loading': isLoading }"
          >
            <svg v-if="isLoading" class="spinner" viewBox="0 0 50 50">
              <circle cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
            </svg>
            <span>{{ isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}</span>
          </button>
        </form>

        <!-- Divider -->
        <div class="divider">
          <span>¿No tienes cuenta?</span>
        </div>

        <!-- Register Link -->
        <router-link to="/register" class="btn-register-link">
          Crear nueva cuenta
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
import { useAuthStore } from '@/stores/useAuthStore'

const router = useRouter()
const authStore = useAuthStore()

// Estado del formulario
const formData = ref({
  email: '',
  password: '',
  rememberMe: false
})

const showPassword = ref(false)
const errorMessage = ref('')
const isLoading = ref(false)
const validationErrors = ref({
  email: '',
  password: ''
})

// Validaciones
const isFormValid = computed(() => {
  return formData.value.email && formData.value.password && !validationErrors.value.email
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

const validatePassword = () => {
  if (!formData.value.password) {
    validationErrors.value.password = 'La contraseña es requerida'
  } else if (formData.value.password.length < 6) {
    validationErrors.value.password = 'Mínimo 6 caracteres'
  } else {
    validationErrors.value.password = ''
  }
}

const handleLogin = async () => {
  errorMessage.value = ''
  validateEmail()
  validatePassword()

  if (!isFormValid.value) {
    return
  }

  isLoading.value = true

  try {
    const result = await authStore.login(formData.value.email, formData.value.password)

    if (result.success) {
      // Si marcó "Recordarme", extender sesión (opcional)
      if (formData.value.rememberMe) {
        localStorage.setItem('rememberMe', 'true')
      }
      // Redirigir al home después de login
      setTimeout(() => {
        router.push('/')
      }, 500)
    } else {
      errorMessage.value = result.error || 'Error al iniciar sesión'
    }
  } catch (error) {
    errorMessage.value = 'Error de conexión. Intenta nuevamente.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Contenedor principal */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: #0f0c29;
}

/* Gradiente animado de fondo */
.gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  z-index: 0;
}

/* Blobs animados */
.gradient-blob {
  position: absolute;
  border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
  opacity: 0.3;
  mix-blend-mode: screen;
  z-index: 1;
}

.blob-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  top: -100px;
  left: -100px;
  animation: float 6s ease-in-out infinite;
}

.blob-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(45deg, #f093fb, #f5576c);
  bottom: -50px;
  right: -50px;
  animation: float 8s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0);
  }
  33% {
    transform: translate(30px, -50px);
  }
  66% {
    transform: translate(-20px, 20px);
  }
}

/* Contenido principal */
.login-content {
  position: relative;
  z-index: 20;
  width: 100%;
  max-width: 420px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* Card principal */
.login-card {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 20px;
  box-shadow:
    0 8px 32px 0 rgba(31, 38, 135, 0.37),
    0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 48px 40px;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  animation: slideUp 0.6s ease-out;
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

/* Header */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-circle {
  width: 60px;
  height: 60px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.logo-circle svg {
  width: 32px;
  height: 32px;
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

.login-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.login-header p {
  color: #666;
  font-size: 14px;
  margin: 0;
}

/* Formulario */
.login-form {
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
  padding-right: 40px;
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

.password-toggle {
  position: absolute;
  right: 12px;
  top: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
  padding: 4px;
  display: flex;
  align-items: center;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #667eea;
}

.password-toggle svg {
  width: 20px;
  height: 20px;
}

/* Mensajes de error */
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

/* Opciones de formulario */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  margin-bottom: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #555;
  cursor: pointer;
  user-select: none;
}

.checkbox-label input {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #667eea;
}

.forgot-link {
  font-size: 13px;
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: #764ba2;
}

/* Botón principal */
.btn-login {
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

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.4);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-login.btn-loading {
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

/* Botón de registro */
.btn-register-link {
  padding: 12px 24px;
  background: #f5f5f5;
  color: #667eea;
  font-size: 14px;
  font-weight: 600;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  text-align: center;
  display: block;
}

.btn-register-link:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
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
  .login-content {
    padding: 16px;
    max-width: 100%;
  }

  .login-card {
    padding: 32px 24px;
  }

  .login-header h1 {
    font-size: 24px;
  }

  .blob-1, .blob-2 {
    opacity: 0.15;
  }
}
</style>
