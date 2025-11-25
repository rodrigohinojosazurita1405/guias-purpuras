<template>
  <div class="login-container">
    <!-- Gradiente animado de fondo -->
    <div class="gradient-bg"></div>
    <div class="gradient-blob blob-1"></div>
    <div class="gradient-blob blob-2"></div>

    <!-- Partículas flotantes -->
    <div class="particles-container">
      <div class="particle particle-1"></div>
      <div class="particle particle-2"></div>
      <div class="particle particle-3"></div>
      <div class="particle particle-4"></div>
      <div class="particle particle-5"></div>
      <div class="particle particle-6"></div>
      <div class="particle particle-7"></div>
      <div class="particle particle-8"></div>
      <div class="particle particle-9"></div>
      <div class="particle particle-10"></div>
      <div class="particle particle-11"></div>
      <div class="particle particle-12"></div>
    </div>

    <!-- Esferas rebotando -->
    <div class="bounce-spheres-container">
      <div class="bounce-sphere bounce-sphere-1"></div>
      <div class="bounce-sphere bounce-sphere-2"></div>
      <div class="bounce-sphere bounce-sphere-3"></div>
      <div class="bounce-sphere bounce-sphere-4"></div>
    </div>

    <!-- Estrellas fugaces -->
    <div class="meteors-container">
      <div class="meteor meteor-1"></div>
      <div class="meteor meteor-2"></div>
      <div class="meteor meteor-3"></div>
      <div class="meteor meteor-4"></div>
    </div>

    <div class="login-content">
      <!-- Card principal -->
      <div class="login-card">
        <!-- Back Button -->
        <button @click="goHome" class="btn-back" type="button" title="Volver al inicio">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>

        <!-- Header -->
        <div class="login-header">
          <div class="logo-circle">
            <img src="@/assets/guiaspurpuras.ico" alt="Guías Púrpuras" class="logo-img" />
          </div>
          <h1>Bienvenido</h1>
          <p>Accede a tu cuenta de Guías Púrpuras Bolivia</p>
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

const goHome = () => {
  router.push('/')
}

const currentYear = new Date().getFullYear()
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

/* Partículas flotantes - Destellos fluidos */
.particles-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 2;
  overflow: hidden;
  pointer-events: none;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.9), rgba(124, 58, 237, 0.5));
  box-shadow: 0 0 30px rgba(124, 58, 237, 0.8), 0 0 60px rgba(167, 139, 250, 0.4);
  filter: blur(0.5px);
}

.particle-1 {
  width: 12px;
  height: 12px;
  top: 15%;
  left: 10%;
  animation: floatParticle 20s ease-in-out infinite;
}

.particle-2 {
  width: 16px;
  height: 16px;
  top: 25%;
  left: 85%;
  animation: floatParticle 25s ease-in-out infinite reverse;
  animation-delay: 2s;
}

.particle-3 {
  width: 10px;
  height: 10px;
  top: 45%;
  left: 20%;
  animation: floatParticle 22s ease-in-out infinite;
  animation-delay: 4s;
}

.particle-4 {
  width: 14px;
  height: 14px;
  top: 60%;
  left: 90%;
  animation: floatParticle 28s ease-in-out infinite reverse;
  animation-delay: 1s;
}

.particle-5 {
  width: 12px;
  height: 12px;
  top: 75%;
  left: 15%;
  animation: floatParticle 24s ease-in-out infinite;
  animation-delay: 3s;
}

.particle-6 {
  width: 16px;
  height: 16px;
  top: 35%;
  left: 75%;
  animation: floatParticle 26s ease-in-out infinite reverse;
  animation-delay: 5s;
}

.particle-7 {
  width: 10px;
  height: 10px;
  top: 55%;
  left: 25%;
  animation: floatParticle 21s ease-in-out infinite;
  animation-delay: 2.5s;
}

.particle-8 {
  width: 14px;
  height: 14px;
  top: 20%;
  left: 70%;
  animation: floatParticle 27s ease-in-out infinite reverse;
  animation-delay: 4.5s;
}

.particle-9 {
  width: 12px;
  height: 12px;
  top: 70%;
  left: 50%;
  animation: floatParticle 23s ease-in-out infinite;
  animation-delay: 1.5s;
}

.particle-10 {
  width: 14px;
  height: 14px;
  top: 40%;
  left: 40%;
  animation: floatParticle 29s ease-in-out infinite reverse;
  animation-delay: 3.5s;
}

.particle-11 {
  width: 10px;
  height: 10px;
  top: 80%;
  left: 80%;
  animation: floatParticle 25s ease-in-out infinite;
  animation-delay: 0s;
}

.particle-12 {
  width: 16px;
  height: 16px;
  top: 50%;
  left: 5%;
  animation: floatParticle 26s ease-in-out infinite reverse;
  animation-delay: 2s;
}

@keyframes floatParticle {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  50% {
    transform: translate(100px, -150px) scale(1.5);
    opacity: 0.8;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translate(50px, -300px) scale(0.5);
    opacity: 0;
  }
}

/* Esferas rebotando */
.bounce-spheres-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 1.5;
  overflow: hidden;
  pointer-events: none;
}

.bounce-sphere {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, rgba(167, 139, 250, 0.6), rgba(124, 58, 237, 0.2));
  box-shadow:
    0 0 40px rgba(167, 139, 250, 0.5),
    inset -2px -2px 5px rgba(0, 0, 0, 0.2),
    inset 2px 2px 5px rgba(255, 255, 255, 0.1);
  filter: blur(0.3px);
  border: 1px solid rgba(167, 139, 250, 0.3);
}

.bounce-sphere-1 {
  width: 40px;
  height: 40px;
  bottom: -50px;
  left: 15%;
  animation: bounce1 4s ease-in-out infinite;
}

.bounce-sphere-2 {
  width: 50px;
  height: 50px;
  bottom: -60px;
  right: 20%;
  animation: bounce2 5s ease-in-out infinite;
  animation-delay: 0.5s;
}

.bounce-sphere-3 {
  width: 35px;
  height: 35px;
  bottom: -40px;
  left: 50%;
  animation: bounce3 4.5s ease-in-out infinite;
  animation-delay: 1s;
}

.bounce-sphere-4 {
  width: 45px;
  height: 45px;
  bottom: -55px;
  left: 75%;
  animation: bounce1 5.5s ease-in-out infinite;
  animation-delay: 0.3s;
}

@keyframes bounce1 {
  0% {
    transform: translateY(0) scaleY(1);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  25% {
    transform: translateY(-300px) scaleY(1);
  }
  50% {
    transform: translateY(-80px) scaleY(0.8);
  }
  75% {
    transform: translateY(-200px) scaleY(1);
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(0) scaleY(1);
    opacity: 0;
  }
}

@keyframes bounce2 {
  0% {
    transform: translateY(0) scaleY(1);
    opacity: 0;
  }
  8% {
    opacity: 1;
  }
  20% {
    transform: translateY(-350px) scaleY(1);
  }
  45% {
    transform: translateY(-100px) scaleY(0.75);
  }
  70% {
    transform: translateY(-220px) scaleY(1);
  }
  92% {
    opacity: 1;
  }
  100% {
    transform: translateY(0) scaleY(1);
    opacity: 0;
  }
}

@keyframes bounce3 {
  0% {
    transform: translateY(0) scaleY(1);
    opacity: 0;
  }
  12% {
    opacity: 1;
  }
  28% {
    transform: translateY(-320px) scaleY(1);
  }
  52% {
    transform: translateY(-90px) scaleY(0.8);
  }
  78% {
    transform: translateY(-210px) scaleY(1);
  }
  88% {
    opacity: 1;
  }
  100% {
    transform: translateY(0) scaleY(1);
    opacity: 0;
  }
}

/* Estrellas fugaces (Shooting Stars) */
.meteors-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 3;
  overflow: hidden;
  pointer-events: none;
}

.meteor {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(ellipse at 20% 20%, rgba(255, 255, 255, 0.9), rgba(167, 139, 250, 0.6), transparent);
  box-shadow:
    0 0 30px rgba(167, 139, 250, 0.6),
    0 0 60px rgba(124, 58, 237, 0.3),
    inset 0 0 15px rgba(255, 255, 255, 0.4);
  filter: blur(0.5px);
}

.meteor::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(167, 139, 250, 0.4), transparent 70%);
  border-radius: 50%;
  animation: shootingGlow 2s ease-out infinite;
}

.meteor-1 {
  width: 8px;
  height: 8px;
  top: 15%;
  left: 15%;
  animation: shootingStar 4s ease-in infinite;
  animation-delay: 0s;
}

.meteor-2 {
  width: 6px;
  height: 6px;
  top: 30%;
  left: 85%;
  animation: shootingStar 4.5s ease-in infinite;
  animation-delay: 1.2s;
}

.meteor-3 {
  width: 7px;
  height: 7px;
  top: 55%;
  left: 10%;
  animation: shootingStar 4.2s ease-in infinite;
  animation-delay: 2.4s;
}

.meteor-4 {
  width: 6px;
  height: 6px;
  top: 70%;
  left: 80%;
  animation: shootingStar 4.8s ease-in infinite;
  animation-delay: 0.6s;
}

@keyframes shootingStar {
  0% {
    opacity: 0;
    transform: translate(0, 0) scale(0.5);
  }
  5% {
    opacity: 1;
    transform: translate(0, 0) scale(1);
  }
  85% {
    opacity: 0.8;
  }
  100% {
    opacity: 0;
    transform: translate(150px, -200px) scale(0.2);
  }
}

@keyframes shootingGlow {
  0% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(2);
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
    0 8px 32px 0 rgba(124, 58, 237, 0.25),
    0 20px 60px rgba(109, 40, 217, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.6);
  padding: 48px 40px;
  backdrop-filter: blur(10px);
  border: 1.5px solid rgba(124, 58, 237, 0.2);
  animation: slideUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  overflow: visible;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: transparent;
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

/* Back Button */
.btn-back {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 36px;
  height: 36px;
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border-radius: 6px;
  padding: 0;
  z-index: 10;
}

.btn-back:hover {
  color: #7c3aed;
  background: rgba(124, 58, 237, 0.1);
}

.btn-back:active {
  transform: scale(0.95);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

/* Header */
.login-header {
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

.btn-register-link:hover {
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
