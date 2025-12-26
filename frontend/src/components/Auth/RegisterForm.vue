<template>
  <div class="register-container">
    <!-- Lado izquierdo: Formulario -->
    <div class="register-left">
      <!-- Back Button -->
      <button @click="goHome" class="btn-back" type="button" title="Volver al inicio">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>

      <div class="form-wrapper">
        <!-- Logo y Header -->
        <div class="register-header">
          <div class="logo-circle">
            <img src="@/assets/guiaspurpuras.ico" alt="Guías Púrpuras" class="logo-img" />
          </div>
          <h1>¡Crea tu cuenta gratis!</h1>
          <p>Comienza tu viaje hacia nuevas oportunidades laborales en:</p>
          <h2 class="brand-title">
            Guías Púrpuras Bolivia
            <img src="@/assets/bolivia.webp" alt="Bolivia" class="bolivia-flag" />
          </h2>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="handleRegister" class="register-form">
          <!-- Role Selection (Movido arriba) -->
          <div class="form-group">
            <label for="role" class="form-label">¿Quién eres?</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <select
                id="role"
                v-model="formData.role"
                class="form-input"
                required
                :disabled="isLoading"
              >
                <option value="">Selecciona tu rol...</option>
                <option value="applicant">Postulante - Busco empleo</option>
                <option value="company">Empresa - Busco talento</option>
              </select>
            </div>
          </div>

          <!-- Name Input -->
          <div class="form-group">
            <label for="name" class="form-label">{{ nameLabel }}</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                class="form-input"
                :class="{ 'input-error': validationErrors.name }"
                :placeholder="namePlaceholder"
                required
                :disabled="isLoading"
                @blur="validateName"
              />
              <span v-if="validationErrors.name" class="input-error-text">{{ validationErrors.name }}</span>
            </div>
          </div>

          <!-- Email Input -->
          <div class="form-group">
            <label for="email" class="form-label">{{ emailLabel }}</label>
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
                :placeholder="emailPlaceholder"
                required
                :disabled="isLoading"
                @blur="validateEmail"
              />
              <span v-if="validationErrors.email" class="input-error-text">{{ validationErrors.email }}</span>
            </div>
          </div>

          <!-- Password Input -->
          <div class="form-group">
            <label for="password" class="form-label">Contraseña</label>
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
                placeholder="Mínimo 6 caracteres"
                required
                :disabled="isLoading"
                @input="validatePassword"
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

            <!-- Password strength indicator -->
            <div v-if="formData.password" class="password-strength">
              <div class="strength-bar">
                <div
                  class="strength-fill"
                  :class="passwordStrength.level"
                  :style="{ width: passwordStrength.percentage + '%' }"
                ></div>
              </div>
              <span class="strength-text" :class="passwordStrength.level">
                {{ passwordStrength.text }}
              </span>
            </div>
          </div>

          <!-- Confirm Password Input -->
          <div class="form-group">
            <label for="confirmPassword" class="form-label">Confirmar Contraseña</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <input
                id="confirmPassword"
                v-model="formData.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-input"
                :class="{ 'input-error': validationErrors.confirmPassword }"
                placeholder="Confirma tu contraseña"
                required
                :disabled="isLoading"
                @blur="validateConfirmPassword"
              />
              <button
                type="button"
                class="password-toggle"
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
              <span v-if="validationErrors.confirmPassword" class="input-error-text">{{ validationErrors.confirmPassword }}</span>
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

          <!-- Terms & Conditions -->
          <label class="checkbox-label">
            <input type="checkbox" v-model="acceptTerms" :disabled="isLoading" required />
            <span>Acepto los <router-link to="/terminos">términos y condiciones</router-link></span>
          </label>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn-register"
            :disabled="isLoading || !isFormValid"
            :class="{ 'btn-loading': isLoading }"
          >
            <svg v-if="isLoading" class="spinner" viewBox="0 0 50 50">
              <circle cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
            </svg>
            <span>{{ isLoading ? 'Creando cuenta...' : 'Crear Cuenta' }}</span>
          </button>
        </form>

        <!-- Login Link -->
        <div class="login-section">
          <p class="login-text">¿Ya tienes una cuenta?</p>
          <router-link to="/login" class="btn-login-link">
            Iniciar sesión
          </router-link>
        </div>
      </div>
    </div>

    <!-- Lado derecho: Panel de marca -->
    <div class="register-right">
      <div class="brand-overlay"></div>
      <div class="brand-content">
        <div class="brand-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <span>100% Gratis para Postulantes</span>
        </div>

        <h2>Únete a la comunidad laboral más grande de Bolivia</h2>
        <p class="brand-description">
          Miles de profesionales y empresas ya confían en Guías Púrpuras para encontrar las mejores oportunidades.
        </p>

        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="8.5" cy="7" r="4"></circle>
                <polyline points="17 11 19 13 23 9"></polyline>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Perfil Profesional</h3>
              <p>Crea tu perfil y destaca tus habilidades</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Postula Fácilmente</h3>
              <p>Aplica a empleos con un solo clic</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
              </svg>
            </div>
            <div class="feature-text">
              <h3>Notificaciones</h3>
              <p>Recibe alertas de nuevas ofertas</p>
            </div>
          </div>
        </div>

        <div class="stats-banner">
          <div class="stat-item">
            <span class="stat-number">1,500+</span>
            <span class="stat-label">Empleos</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">500+</span>
            <span class="stat-label">Empresas</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">3,000+</span>
            <span class="stat-label">Usuarios</span>
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
import { useAuthStore } from '@/stores/useAuthStore'

const router = useRouter()
const authStore = useAuthStore()

// Estado del formulario
const formData = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: ''
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const acceptTerms = ref(false)
const errorMessage = ref('')
const isLoading = ref(false)
const validationErrors = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// Validaciones
const isFormValid = computed(() => {
  return (
    formData.value.name &&
    formData.value.email &&
    formData.value.password &&
    formData.value.confirmPassword &&
    formData.value.role &&
    acceptTerms.value &&
    !validationErrors.value.name &&
    !validationErrors.value.email &&
    !validationErrors.value.password &&
    !validationErrors.value.confirmPassword
  )
})

// Labels dinámicos según el rol
const nameLabel = computed(() => {
  return formData.value.role === 'company' ? 'Nombre de la Empresa' : 'Nombre Completo'
})

const namePlaceholder = computed(() => {
  return formData.value.role === 'company' ? 'Ej: Empresa S.A.' : 'Juan Pérez'
})

const emailLabel = computed(() => {
  return formData.value.role === 'company' ? 'Correo Electrónico de la Empresa' : 'Correo Electrónico'
})

const emailPlaceholder = computed(() => {
  return formData.value.role === 'company' ? 'contacto@empresa.com' : 'tu@email.com'
})

// Indicador de fortaleza de contraseña
const passwordStrength = computed(() => {
  const pwd = formData.value.password
  if (!pwd) return { level: 'none', percentage: 0, text: '' }

  let strength = 0
  const checks = [
    pwd.length >= 8,
    pwd.length >= 12,
    /[a-z]/.test(pwd),
    /[A-Z]/.test(pwd),
    /[0-9]/.test(pwd),
    /[^a-zA-Z0-9]/.test(pwd)
  ]

  strength = checks.filter(Boolean).length

  if (strength <= 2) {
    return { level: 'weak', percentage: 33, text: 'Contraseña débil' }
  } else if (strength <= 4) {
    return { level: 'medium', percentage: 66, text: 'Contraseña regular' }
  } else {
    return { level: 'strong', percentage: 100, text: 'Contraseña fuerte' }
  }
})

// Métodos de validación
const validateName = () => {
  if (!formData.value.name) {
    validationErrors.value.name = 'El nombre es requerido'
  } else if (formData.value.name.length < 3) {
    validationErrors.value.name = 'Mínimo 3 caracteres'
  } else {
    validationErrors.value.name = ''
  }
}

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
  validateConfirmPassword()
}

const validateConfirmPassword = () => {
  if (!formData.value.confirmPassword) {
    validationErrors.value.confirmPassword = 'Debes confirmar la contraseña'
  } else if (formData.value.password.trim() !== formData.value.confirmPassword.trim()) {
    validationErrors.value.confirmPassword = 'Las contraseñas no coinciden'
  } else {
    validationErrors.value.confirmPassword = ''
  }
}

const handleRegister = async () => {
  errorMessage.value = ''

  // Validar todos los campos
  validateName()
  validateEmail()
  validatePassword()
  validateConfirmPassword()

  if (!isFormValid.value) {
    return
  }

  isLoading.value = true

  try {
    const result = await authStore.register(
      formData.value.name,
      formData.value.email,
      formData.value.password,
      formData.value.role
    )

    if (result.success) {
      setTimeout(() => {
        // Redirigir inteligentemente según el rol
        if (authStore.user?.role === 'company') {
          router.push('/dashboard/company')
        } else {
          router.push('/dashboard/profile')
        }
      }, 500)
    } else {
      errorMessage.value = result.error || 'Error al registrarse'
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
.register-container {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

/* ========== LADO IZQUIERDO: FORMULARIO ========== */
.register-left {
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  position: relative;
  overflow-y: auto;
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

.register-header {
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

.register-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.75rem 0;
  letter-spacing: -0.03em;
}

.register-header h2.brand-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
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
  width: 26px;
  height: 26px;
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

.register-header p {
  color: #6b7280;
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
  max-width: 360px;
  margin-left: auto;
  margin-right: auto;
}

/* Formulario */
.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
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
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-error-text {
  font-size: 0.8125rem;
  color: #ef4444;
  margin-top: 0.25rem;
}

select.form-input {
  cursor: pointer;
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

/* Password strength */
.password-strength {
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: #f0f0f0;
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
}

.strength-fill.weak {
  background: #ef4444;
}

.strength-fill.medium {
  background: #f59e0b;
}

.strength-fill.strong {
  background: #10b981;
}

.strength-text {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.strength-text.weak {
  color: #ef4444;
}

.strength-text.medium {
  color: #f59e0b;
}

.strength-text.strong {
  color: #10b981;
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

/* Checkbox */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  font-size: 0.875rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem 0;
}

.checkbox-label input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #7c3aed;
  flex-shrink: 0;
}

.checkbox-label a {
  color: #7c3aed;
  text-decoration: none;
  font-weight: 600;
}

.checkbox-label a:hover {
  text-decoration: underline;
}

/* Botón principal */
.btn-register {
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
  margin-top: 0.5rem;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
}

.btn-register:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
}

.btn-register:active:not(:disabled) {
  transform: translateY(0);
}

.btn-register:disabled {
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
.register-right {
  background-image: url('@/assets/images/bg1.jpg');
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
  margin-bottom: 2.5rem;
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

.stats-banner {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fbbf24;
  margin: 0;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
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
  .register-container {
    grid-template-columns: 1fr;
  }

  .register-right {
    display: none;
  }

  .register-left {
    padding: 2rem 1.5rem;
  }

  .btn-back {
    top: 1.5rem;
    left: 1.5rem;
  }
}

/* Móviles grandes (hasta 640px) */
@media (max-width: 640px) {
  .register-left {
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

  .register-header {
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

  .register-header h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .register-header p {
    font-size: 0.875rem;
  }

  .register-header .brand-title {
    font-size: 1.25rem;
    margin-bottom: 1rem;
  }

  .bolivia-flag {
    width: 22px;
    height: 22px;
  }

  .register-form {
    gap: 1.25rem;
  }

  .form-label {
    font-size: 0.875rem;
  }

  .form-input, select.form-input {
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

  .password-strength-bar {
    height: 3px;
  }

  .password-strength-text {
    font-size: 0.75rem;
  }

  .btn-primary {
    min-height: 48px;
    font-size: 1rem;
    padding: 0.875rem 1.5rem;
  }

  .checkbox-label {
    font-size: 0.8125rem;
    padding: 0.625rem 0;
  }

  .checkbox-label input {
    width: 20px;
    height: 20px;
  }

  .divider-text {
    font-size: 0.8125rem;
  }

  .btn-login {
    min-height: 48px;
    font-size: 0.9375rem;
  }
}

/* Móviles pequeños (hasta 375px) */
@media (max-width: 375px) {
  .register-left {
    padding: 1rem 0.875rem;
  }

  .register-header h1 {
    font-size: 1.375rem;
  }

  .register-header .brand-title {
    font-size: 1.125rem;
    gap: 0.375rem;
  }

  .bolivia-flag {
    width: 20px;
    height: 20px;
  }

  .register-form {
    gap: 1rem;
  }

  .form-input, select.form-input {
    padding: 0.625rem 0.875rem 0.625rem 2.5rem;
  }

  .input-icon {
    left: 0.875rem;
  }

  .checkbox-label {
    font-size: 0.75rem;
  }
}
</style>
