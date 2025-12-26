/**
 * Utilidad de logging que solo muestra mensajes en desarrollo
 * En producción, los logs se silencian automáticamente
 */

const isDevelopment = import.meta.env.MODE === 'development'

export const logger = {
  log: (...args) => {
    if (isDevelopment) {
      console.log(...args)
    }
  },

  warn: (...args) => {
    if (isDevelopment) {
      console.warn(...args)
    }
  },

  error: (...args) => {
    // Los errores siempre se muestran, incluso en producción
    console.error(...args)
  },

  debug: (...args) => {
    if (isDevelopment) {
      console.debug(...args)
    }
  },

  info: (...args) => {
    if (isDevelopment) {
      console.info(...args)
    }
  }
}

// Exportar como default también
export default logger
