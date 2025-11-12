<!-- frontend/src/components/Auth/AuthModal.vue -->
<template>
  <VaModal
    v-model="isOpen"
    size="medium"
    :hide-default-actions="true"
    @update:model-value="handleClose"
    no-padding
    fullscreen
    overlay-opacity="0.8"
    :z-index="99999"
  >
    <div class="modal-wrapper">
      <div class="auth-modal">
        <!-- Header con Logo -->
        <div class="modal-header">
          <img src="/src/assets/guiaspurpuras.ico" alt="Logo" class="modal-logo" />
          <h2 class="modal-title">
            {{ currentTab === 'login' ? 'Inicia sesión' : 'Regístrate' }} en <span class="brand-name">Guías Púrpuras</span>
          </h2>
          <button class="close-btn" @click="handleClose(false)">
            <va-icon name="close" />
          </button>
        </div>

        <!-- Tabs -->
        <div class="auth-tabs">
          <button
            :class="['tab-btn', { active: currentTab === 'login' }]"
            @click="currentTab = 'login'"
          >
            Ingresar
          </button>
          <button
            :class="['tab-btn', { active: currentTab === 'register' }]"
            @click="currentTab = 'register'"
          >
            Registrarse
          </button>
        </div>

        <div class="modal-body">
          <!-- LOGIN FORM -->
          <form v-if="currentTab === 'login'" @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label class="form-label">Correo electrónico o Número de WhatsApp</label>
              <VaInput
                v-model="loginForm.identifier"
                placeholder="correo@ejemplo.com o +591 12345678"
                class="form-input"
              >
                <template #prepend>
                  <va-icon name="person" color="#666" />
                </template>
              </VaInput>
            </div>

            <div class="form-group">
              <label class="form-label">Contraseña</label>
              <VaInput
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Tu contraseña"
                class="form-input"
              >
                <template #prepend>
                  <va-icon name="lock" color="#666" />
                </template>
                <template #append>
                  <va-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    @click="showPassword = !showPassword"
                    style="cursor: pointer; color: #666;"
                  />
                </template>
              </VaInput>
            </div>

            <div class="form-options">
              <VaCheckbox
                v-model="loginForm.remember"
                label="Recordarme"
              />
              <a href="#" class="forgot-link" @click.prevent="handleForgotPassword">
                ¿Se te olvidó tu contraseña?
              </a>
            </div>

            <VaButton
              type="submit"
              color="primary"
              class="submit-btn"
              :loading="isLoading"
              block
            >
              Iniciar sesión
            </VaButton>

            <div class="help-link">
              <a href="#" @click.prevent="handleHelp">
                <va-icon name="help_outline" size="small" />
                ¿Tienes problemas para iniciar sesión?
              </a>
            </div>
          </form>

          <!-- REGISTER FORM -->
          <form v-if="currentTab === 'register'" @submit.prevent="handleRegister" class="auth-form">
            <div class="form-group">
              <label class="form-label">Nombre completo</label>
              <VaInput
                v-model="registerForm.name"
                placeholder="Juan Pérez"
                class="form-input"
              >
                <template #prepend>
                  <va-icon name="person" color="#666" />
                </template>
              </VaInput>
            </div>

            <div class="form-group">
              <label class="form-label">Correo electrónico</label>
              <VaInput
                v-model="registerForm.email"
                type="email"
                placeholder="correo@ejemplo.com"
                class="form-input"
              >
                <template #prepend>
                  <va-icon name="email" color="#666" />
                </template>
              </VaInput>
            </div>

            <div class="form-group">
              <label class="form-label">Teléfono / WhatsApp</label>
              <VaInput
                v-model="registerForm.phone"
                placeholder="+591 70123456"
                class="form-input"
              >
                <template #prepend>
                  <va-icon name="phone" color="#666" />
                </template>
              </VaInput>
            </div>

            <div class="form-group">
              <label class="form-label">Contraseña</label>
              <VaInput
                v-model="registerForm.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Mínimo 6 caracteres"
                class="form-input"
              >
                <template #prepend>
                  <va-icon name="lock" color="#666" />
                </template>
                <template #append>
                  <va-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    @click="showPassword = !showPassword"
                    style="cursor: pointer; color: #666;"
                  />
                </template>
              </VaInput>
            </div>

            <div class="form-options">
              <VaCheckbox
                v-model="registerForm.acceptTerms"
                class="terms-checkbox"
              >
                <template #label>
                  <span class="terms-text">
                    Acepto los <a href="#" @click.prevent="showTerms">términos y condiciones</a>
                  </span>
                </template>
              </VaCheckbox>
            </div>

            <VaButton
              type="submit"
              color="primary"
              class="submit-btn"
              :loading="isLoading"
              block
            >
              Crear cuenta
            </VaButton>
          </form>

          <!-- DIVIDER -->
          <div class="divider">
            <span class="divider-text">o</span>
          </div>

          <!-- OAUTH BUTTONS -->
          <div class="oauth-buttons">
            <button
              type="button"
              class="oauth-btn google-btn"
              @click="handleGoogleAuth"
              disabled
            >
              <svg class="oauth-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Continuar con Google
            </button>

            <button
              type="button"
              class="oauth-btn facebook-btn"
              @click="handleFacebookAuth"
              disabled
            >
              <svg class="oauth-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="#1877F2" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
              Continuar con Facebook
            </button>
          </div>

          <!-- FOOTER -->
          <div class="modal-footer">
            <p v-if="currentTab === 'login'">
              ¿No tienes una cuenta? 
              <a href="#" @click.prevent="currentTab = 'register'" class="switch-link">Regístrate</a>
            </p>
            <p v-else>
              ¿Ya tienes cuenta? 
              <a href="#" @click.prevent="currentTab = 'login'" class="switch-link">Inicia sesión</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </VaModal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'

const authStore = useAuthStore()
const { init: notify } = useToast()

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  // 🆕 PROP PARA TAB INICIAL
  initialTab: {
    type: String,
    default: 'register', // Por defecto registro
    validator: (value) => ['login', 'register'].includes(value)
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const isOpen = ref(props.modelValue)
// 🆕 USAR INITIAL TAB DEL PROP
const currentTab = ref(props.initialTab)
const showPassword = ref(false)
const isLoading = ref(false)

const loginForm = ref({
  identifier: '',
  password: '',
  remember: false
})

const registerForm = ref({
  name: '',
  email: '',
  phone: '',
  password: '',
  acceptTerms: false
})

const handleClose = (value) => {
  isOpen.value = value
  emit('update:modelValue', value)
  if (!value) resetForms()
}

const resetForms = () => {
  loginForm.value = { identifier: '', password: '', remember: false }
  registerForm.value = { name: '', email: '', phone: '', password: '', acceptTerms: false }
  showPassword.value = false
  // 🆕 RESETEAR AL TAB INICIAL AL CERRAR
  currentTab.value = props.initialTab
}

const handleLogin = async () => {
  if (!loginForm.value.identifier || !loginForm.value.password) {
    notify({ message: 'Por favor completa todos los campos', color: 'warning' })
    return
  }
  isLoading.value = true
  try {
    const result = await authStore.login(loginForm.value.identifier, loginForm.value.password)
    if (result.success) {
      notify({ message: '¡Bienvenido de nuevo! 🎉', color: 'success' })
      handleClose(false)
      emit('success')
    } else {
      notify({ message: result.error || 'Error al iniciar sesión', color: 'danger' })
    }
  } catch (error) {
    notify({ message: 'Error de conexión. Intenta nuevamente.', color: 'danger' })
  } finally {
    isLoading.value = false
  }
}

const handleRegister = async () => {
  if (!registerForm.value.name || !registerForm.value.email || !registerForm.value.password) {
    notify({ message: 'Por favor completa los campos obligatorios', color: 'warning' })
    return
  }
  if (!registerForm.value.acceptTerms) {
    notify({ message: 'Debes aceptar los términos y condiciones', color: 'warning' })
    return
  }
  isLoading.value = true
  try {
    const result = await authStore.register(
      registerForm.value.name,
      registerForm.value.email,
      registerForm.value.password,
      registerForm.value.phone
    )
    if (result.success) {
      notify({ message: '¡Cuenta creada exitosamente! 🎉', color: 'success' })
      handleClose(false)
      emit('success')
    } else {
      notify({ message: result.error || 'Error al registrarse', color: 'danger' })
    }
  } catch (error) {
    notify({ message: 'Error de conexión. Intenta nuevamente.', color: 'danger' })
  } finally {
    isLoading.value = false
  }
}

const handleGoogleAuth = () => {
  notify({ message: '🚧 Google Login próximamente', color: 'info', duration: 3000 })
}

const handleFacebookAuth = () => {
  notify({ message: '🚧 Facebook Login próximamente', color: 'info', duration: 3000 })
}

const handleForgotPassword = () => {
  notify({ message: '🚧 Recuperación de contraseña próximamente', color: 'info' })
}

const handleHelp = () => {
  notify({ message: '📧 Contacta a soporte@guiaspurpuras.com', color: 'info' })
}

const showTerms = () => {
  notify({ message: '📄 Términos y condiciones próximamente', color: 'info' })
}

// 🆕 WATCH PARA CAMBIAR TAB CUANDO CAMBIA EL PROP
watch(() => props.initialTab, (newTab) => {
  currentTab.value = newTab
})

watch(() => props.modelValue, (newValue) => {
  isOpen.value = newValue
  // 🆕 RESETEAR AL TAB INICIAL AL ABRIR
  if (newValue) {
    currentTab.value = props.initialTab
  }
})
</script>

<style scoped>
/* Los estilos siguen igual... */
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5rem 1rem;
  overflow-y: auto;
  z-index: 9999;
}

.auth-modal {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 540px;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.4);
  position: relative;
  z-index: 10000;
}

.modal-header {
  position: relative;
  padding: 2.5rem 2rem 1.5rem;
  text-align: center;
  border-bottom: 1px solid #E0E0E0;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
  border-radius: 20px 20px 0 0;
}

.modal-logo {
  width: 60px;
  height: 60px;
  margin-bottom: 1rem;
}

.modal-title {
  font-size: 1.6rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  line-height: 1.4;
}

.brand-name {
  color: var(--color-purple);
  font-weight: 700;
}

.close-btn {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #666;
  transition: all 0.2s;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
  background: #F5F5F5;
  transform: rotate(90deg);
}

.auth-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-bottom: 2px solid #E0E0E0;
  background: white;
}

.tab-btn {
  padding: 1.1rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  font-weight: 600;
  font-size: 1.05rem;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: var(--color-purple);
  background: rgba(92, 0, 153, 0.05);
}

.tab-btn.active {
  color: var(--color-purple);
  border-bottom-color: var(--color-purple);
  background: rgba(92, 0, 153, 0.03);
}

.modal-body {
  padding: 2.5rem 2rem;
  background: white;
  border-radius: 0 0 20px 20px;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: #333;
  font-size: 0.95rem;
}

.form-input {
  width: 100%;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-top: -0.5rem;
}

.forgot-link {
  color: var(--color-purple);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  white-space: nowrap;
}

.forgot-link:hover {
  text-decoration: underline;
}

.terms-text {
  font-size: 0.9rem;
  color: #666;
}

.terms-text a {
  color: var(--color-purple);
  text-decoration: none;
}

.terms-text a:hover {
  text-decoration: underline;
}

.submit-btn {
  margin-top: 0.5rem;
  padding: 1rem;
  font-weight: 600;
  font-size: 1.05rem;
  background: var(--color-purple) !important;
  border-radius: 10px;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(92, 0, 153, 0.4);
}

.help-link {
  text-align: center;
  margin-top: -0.5rem;
}

.help-link a {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #00A3BF;
  text-decoration: none;
  font-size: 0.9rem;
}

.help-link a:hover {
  text-decoration: underline;
}

.divider {
  position: relative;
  text-align: center;
  margin: 2rem 0;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 45%;
  height: 1px;
  background: #E0E0E0;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.divider-text {
  background: white;
  padding: 0 1rem;
  color: #999;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.oauth-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.oauth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 10px;
  background: white;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.oauth-btn:not(:disabled):hover {
  border-color: #C0C0C0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.oauth-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.google-btn {
  color: #333;
}

.facebook-btn {
  color: #1877F2;
}

.oauth-icon {
  flex-shrink: 0;
}

.modal-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E0E0E0;
}

.modal-footer p {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

.switch-link {
  color: var(--color-purple);
  text-decoration: none;
  font-weight: 600;
}

.switch-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .modal-wrapper {
    padding: 2rem 0.5rem;
  }

  .auth-modal {
    border-radius: 16px;
    max-width: 95%;
  }

  .modal-header {
    padding: 2rem 1.5rem 1rem;
    border-radius: 16px 16px 0 0;
  }

  .modal-logo {
    width: 50px;
    height: 50px;
  }

  .modal-body {
    padding: 2rem 1.5rem;
    border-radius: 0 0 16px 16px;
    max-height: calc(100vh - 150px);
  }

  .modal-title {
    font-size: 1.35rem;
  }

  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .oauth-btn {
    font-size: 0.9rem;
    padding: 0.875rem;
  }

  .tab-btn {
    font-size: 1rem;
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .modal-wrapper {
    padding: 1rem 0.25rem;
  }

  .modal-header {
    padding: 1.5rem 1rem 1rem;
  }

  .modal-body {
    padding: 1.5rem 1rem;
  }
}
</style>