<template>
  <div class="login-container">
    <!-- Lado izquierdo: Formulario -->
    <div class="login-left">
      <!-- Back Button -->
      <button @click="goHome" class="btn-back" type="button" title="Volver al inicio">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>

      <div class="form-wrapper">
        <!-- Logo y Header -->
        <div class="login-header">
          <div class="logo-circle">
            <img src="@/assets/guiaspurpuras.ico" alt="Guías Púrpuras" class="logo-img" />
          </div>
          <h1>¡Bienvenido de nuevo!</h1>
          <p class="subtitle">Continúa tu búsqueda laboral en:</p>
          <h2 class="brand-title">
            Guías Púrpuras Bolivia
            <img src="@/assets/bolivia.webp" alt="Bolivia" class="bolivia-flag" />
          </h2>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="handleLogin" class="login-form">
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
              <span v-if="validationErrors.email" class="input-error-text">{{ validationErrors.email }}</span>
            </div>
          </div>

          <!-- Password Input -->
          <div class="form-group">
            <div class="label-row">
              <label for="password" class="form-label">Contraseña</label>
              <router-link to="/forgot-password" class="forgot-link">Olvidaste la contraseña?</router-link>
            </div>
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

        <!-- Register Link -->
        <div class="signup-section">
          <p class="signup-text">¿No tienes una cuenta?</p>
          <router-link to="/register" class="btn-signup">
            Crear cuenta nueva
          </router-link>
        </div>
      </div>
    </div>

    <!-- Lado derecho: Panel de marca -->
    <div class="login-right">
      <div class="brand-overlay"></div>
      <div class="brand-content">
        <div class="brand-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
          </svg>
          <span>Plataforma #1 en Bolivia</span>
        </div>

        <h2>Tu próxima oportunidad laboral te espera</h2>
        <p class="brand-description">
          Conectamos talento con las mejores empresas de Bolivia. Más de 1,500 ofertas activas esperando por ti.
        </p>

        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 11l3 3L22 4"></path>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Ofertas Verificadas</h3>
              <p>Solo empresas reales y confiables</p>
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
              <h3>Actualizaciones Diarias</h3>
              <p>Nuevas oportunidades cada día</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Red de Contactos</h3>
              <p>Conecta con profesionales</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer en el panel derecho -->
      <div class="brand-footer">
        <p>{{ currentYear }} © Guías Púrpuras. Todos los derechos reservados.</p>
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

      // Verificar si hay una URL de redirección guardada
      const redirectUrl = sessionStorage.getItem('redirectAfterLogin')
      sessionStorage.removeItem('redirectAfterLogin')

      // Redirigir inteligentemente
      setTimeout(() => {
        if (redirectUrl) {
          router.push(redirectUrl)
        } else if (authStore.user?.role === 'company') {
          router.push('/dashboard/jobs-manager')
        } else {
          router.push('/dashboard/profile')
        }
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

const goHome = () => {
  router.push('/')
}

const currentYear = new Date().getFullYear()
</script>

<style scoped>
/* Contenedor principal con grid de 2 columnas */
.login-container {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

/* ========== LADO IZQUIERDO: FORMULARIO ========== */
.login-left {
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  position: relative;
}

.btn-back {
  position: absolute;
  top: 2rem;
  left: 2rem;
  width: 40px;
  height: 40px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-back:hover {
  background: #f9fafb;
  border-color: #7c3aed;
  color: #7c3aed;
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

.form-wrapper {
  width: 100%;
  max-width: 440px;
}

.login-header {
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

.login-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.75rem 0;
  letter-spacing: -0.03em;
}

.login-header .subtitle {
  color: #6b7280;
  font-size: 0.9375rem;
  line-height: 1.6;
  margin: 0 0 0.625rem 0;
  max-width: 360px;
  margin-left: auto;
  margin-right: auto;
}

.login-header .brand-title {
  font-size: 1.625rem;
  font-weight: 700;
  margin: 0 0 1.5rem 0;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.bolivia-flag {
  width: 28px;
  height: 28px;
  object-fit: contain;
  animation: gentle-float 3s ease-in-out infinite;
}

@keyframes gentle-float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-3px);
  }
}

/* Formulario */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.forgot-link {
  font-size: 0.875rem;
  color: #7c3aed;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: #6d28d9;
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
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-error-text {
  font-size: 0.8125rem;
  color: #ef4444;
  margin-top: 0.25rem;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  top: 0.75rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #7c3aed;
}

.password-toggle svg {
  width: 20px;
  height: 20px;
}

/* Error banner */
.error-banner {
  padding: 0.75rem 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  border-radius: 8px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.error-banner svg {
  width: 18px;
  height: 18px;
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
.btn-login {
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

.btn-login:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
}

.btn-login:disabled {
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

/* Sección de registro */
.signup-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.signup-text {
  font-size: 0.9375rem;
  color: #6b7280;
  margin: 0 0 1rem 0;
}

.btn-signup {
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

.btn-signup:hover {
  background: #f3e8ff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
}

.btn-signup:active {
  transform: translateY(0);
}

/* ========== LADO DERECHO: PANEL DE MARCA ========== */
.login-right {
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
  .login-container {
    grid-template-columns: 1fr;
  }

  .login-right {
    display: none;
  }

  .login-left {
    padding: 2rem 1.5rem;
  }

  .btn-back {
    top: 1.5rem;
    left: 1.5rem;
  }
}

/* Móviles grandes (hasta 640px) */
@media (max-width: 640px) {
  .login-left {
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

  .login-header {
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

  .login-header h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .login-header .subtitle {
    font-size: 0.875rem;
  }

  .login-header .brand-title {
    font-size: 1.25rem;
    margin-bottom: 1.25rem;
  }

  .bolivia-flag {
    width: 22px;
    height: 22px;
  }

  .login-form {
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

  .btn-toggle-password {
    width: 40px;
    height: 40px;
  }

  .btn-toggle-password svg {
    width: 18px;
    height: 18px;
  }

  .btn-primary {
    min-height: 48px;
    font-size: 1rem;
    padding: 0.875rem 1.5rem;
  }

  .forgot-password-link {
    font-size: 0.875rem;
    padding: 0.5rem;
  }

  .divider-text {
    font-size: 0.8125rem;
  }

  .btn-register {
    min-height: 48px;
    font-size: 0.9375rem;
  }
}

/* Móviles pequeños (hasta 375px) */
@media (max-width: 375px) {
  .login-left {
    padding: 1rem 0.875rem;
  }

  .login-header h1 {
    font-size: 1.375rem;
  }

  .login-header .brand-title {
    font-size: 1.125rem;
    gap: 0.375rem;
  }

  .bolivia-flag {
    width: 20px;
    height: 20px;
  }

  .login-form {
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
