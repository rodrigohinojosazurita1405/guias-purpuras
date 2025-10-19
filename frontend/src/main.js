// frontend/src/main.js
import { createApp } from 'vue'
import { createVuestic } from 'vuestic-ui'
import 'vuestic-ui/css'

import App from './App.vue'
import router from './router'

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
  }
}

const app = createApp(App)

app.use(router)
app.use(createVuestic({ config: vuesticConfig }))

app.mount('#app')