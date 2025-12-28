// frontend/src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuestic } from 'vuestic-ui'
import 'vuestic-ui/css'
import './assets/main.css'

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

  // CONFIGURACIÓN DE TRADUCCIONES AL ESPAÑOL
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
// REGISTRAR DIRECTIVAS GLOBALES
// ==========================================

// Directiva global para tooltips (v-tooltip)
app.directive('tooltip', {
  mounted(el, binding) {
    // Crear el elemento tooltip
    const tooltip = document.createElement('div')
    tooltip.className = 'gp-tooltip'
    tooltip.textContent = binding.value
    tooltip.style.cssText = `
      position: absolute;
      background: linear-gradient(135deg, #10B981 0%, #059669 100%);
      color: white;
      padding: 0.5rem 0.75rem;
      border-radius: 6px;
      font-size: 0.875rem;
      font-weight: 500;
      white-space: nowrap;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.2s ease;
      z-index: 9999;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    `

    // Añadir flecha
    const arrow = document.createElement('div')
    arrow.className = 'gp-tooltip-arrow'
    arrow.style.cssText = `
      position: absolute;
      width: 0;
      height: 0;
      border-left: 6px solid transparent;
      border-right: 6px solid transparent;
      border-top: 6px solid #059669;
      bottom: -6px;
      left: 50%;
      transform: translateX(-50%);
    `
    tooltip.appendChild(arrow)

    document.body.appendChild(tooltip)

    // Guardar referencia al tooltip en el elemento
    el._tooltip = tooltip

    // Función para mostrar tooltip
    const showTooltip = (e) => {
      const rect = el.getBoundingClientRect()
      const tooltipRect = tooltip.getBoundingClientRect()

      tooltip.style.left = `${rect.left + rect.width / 2 - tooltipRect.width / 2}px`
      tooltip.style.top = `${rect.top - tooltipRect.height - 8}px`
      tooltip.style.opacity = '1'
    }

    // Función para ocultar tooltip
    const hideTooltip = () => {
      tooltip.style.opacity = '0'
    }

    // Añadir event listeners
    el.addEventListener('mouseenter', showTooltip)
    el.addEventListener('mouseleave', hideTooltip)

    // Guardar los listeners para cleanup
    el._showTooltip = showTooltip
    el._hideTooltip = hideTooltip
  },

  unmounted(el) {
    // Cleanup
    if (el._tooltip) {
      document.body.removeChild(el._tooltip)
    }
    if (el._showTooltip) {
      el.removeEventListener('mouseenter', el._showTooltip)
    }
    if (el._hideTooltip) {
      el.removeEventListener('mouseleave', el._hideTooltip)
    }
  }
})

// ==========================================
// INTERCEPTOR GLOBAL PARA ATRIBUTOS TITLE
// ==========================================
// Esta función convierte TODOS los title="" nativos en tooltips bonitos

const initGlobalTooltips = () => {
  // Función para crear tooltip personalizado
  const createCustomTooltip = (element, text) => {
    if (!text || element._hasCustomTooltip) return

    // Crear el elemento tooltip
    const tooltip = document.createElement('div')
    tooltip.className = 'gp-tooltip'
    tooltip.textContent = text
    tooltip.style.cssText = `
      position: fixed;
      background: linear-gradient(135deg, #10B981 0%, #059669 100%);
      color: white;
      padding: 0.5rem 0.75rem;
      border-radius: 6px;
      font-size: 0.875rem;
      font-weight: 500;
      white-space: nowrap;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.2s ease;
      z-index: 9999;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    `

    // Añadir flecha
    const arrow = document.createElement('div')
    arrow.style.cssText = `
      position: absolute;
      width: 0;
      height: 0;
      border-left: 6px solid transparent;
      border-right: 6px solid transparent;
      border-top: 6px solid #059669;
      bottom: -6px;
      left: 50%;
      transform: translateX(-50%);
    `
    tooltip.appendChild(arrow)
    document.body.appendChild(tooltip)

    // Guardar referencia
    element._customTooltip = tooltip
    element._hasCustomTooltip = true

    // Event handlers
    const showTooltip = () => {
      const rect = element.getBoundingClientRect()
      const tooltipRect = tooltip.getBoundingClientRect()

      tooltip.style.left = `${rect.left + rect.width / 2 - tooltipRect.width / 2}px`
      tooltip.style.top = `${rect.top - tooltipRect.height - 8}px`
      tooltip.style.opacity = '1'
    }

    const hideTooltip = () => {
      tooltip.style.opacity = '0'
    }

    element.addEventListener('mouseenter', showTooltip)
    element.addEventListener('mouseleave', hideTooltip)

    // Guardar para cleanup
    element._showTooltip = showTooltip
    element._hideTooltip = hideTooltip
  }

  // Observador de mutaciones para detectar nuevos elementos con title
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === 1) { // Element node
          // Procesar el nodo y sus hijos
          const elementsWithTitle = node.querySelectorAll ?
            [node, ...node.querySelectorAll('[title]')] :
            [node]

          elementsWithTitle.forEach((el) => {
            if (el.hasAttribute && el.hasAttribute('title')) {
              const titleText = el.getAttribute('title')
              if (titleText) {
                el.removeAttribute('title') // Remover title nativo
                el.setAttribute('data-tooltip', titleText) // Guardar en data attribute
                createCustomTooltip(el, titleText)
              }
            }
          })
        }
      })
    })
  })

  // Iniciar observador
  observer.observe(document.body, {
    childList: true,
    subtree: true
  })

  // Procesar elementos existentes al inicio
  setTimeout(() => {
    document.querySelectorAll('[title]').forEach((el) => {
      const titleText = el.getAttribute('title')
      if (titleText) {
        el.removeAttribute('title')
        el.setAttribute('data-tooltip', titleText)
        createCustomTooltip(el, titleText)
      }
    })
  }, 1000) // Esperar a que Vue termine de renderizar
}

// ==========================================
// REGISTRAR COMPONENTES GLOBALES
// ==========================================

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

// ==========================================
// INICIALIZAR TOOLTIPS GLOBALES
// ==========================================
// Iniciar después de montar la app
setTimeout(() => {
  initGlobalTooltips()
  console.log('✅ Sistema de tooltips globales activado')
}, 500)