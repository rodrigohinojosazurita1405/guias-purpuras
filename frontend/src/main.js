// frontend/src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuestic } from 'vuestic-ui'
import 'vuestic-ui/css'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/useAuthStore'
import { vuesticSpanishConfig } from './config/vuestic-i18n-config'

// ==========================================
// CONFIGURACIÓN DE VUESTIC UI
// ==========================================
const vuesticConfig = {
  colors: {
    variables: {
      // Púrpuras
      'purple-darkest': '#3D0066',
      'purple-dark': '#510087',
      'purple': '#5C0099',
      
      // Amarillos
      'yellow-primary': '#FDC500',
      'yellow-light': '#FFD500',
      
      // Override de colores de Vuestic
      primary: '#5C0099',
      secondary: '#FDC500',
      success: '#40e583',
      info: '#2c82e0',
      danger: '#e34b4a',
      warning: '#ffc200',
    }
  },
  
  // ✨ CONFIGURACIÓN DE TRADUCCIONES AL ESPAÑOL
  i18n: vuesticSpanishConfig
}

// ==========================================
// CREAR APP E INSTANCIAS
// ==========================================
const app = createApp(App)
const pinia = createPinia()

// ==========================================
// USAR PLUGINS
// ==========================================
app.use(pinia)
app.use(router)
app.use(createVuestic({ config: vuesticConfig }))

// ==========================================
// INICIALIZAR AUTH STORE (SOLO UNA VEZ AL INICIO)
// ==========================================
const authStore = useAuthStore(pinia)
authStore.initAuth()
console.log('✅ Auth store inicializado en main.js')

// ==========================================
// MONTAR APP
// ==========================================
app.mount('#app')