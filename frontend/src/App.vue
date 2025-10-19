<template>
  <HomeView />
</template>

<script>
/**
 * App.vue - Componente raíz de la aplicación
 * 
 * Propósito: Punto de entrada principal de Vue
 * Conecta con: HomeView.vue
 * Responsabilidad: Solo renderizar la vista principal
 */

import HomeView from './views/HomeView.vue'

export default {
  name: 'App',
  components: {
    HomeView
  }
}
</script>

<style>
/**
 * Estilos Globales
 * Se aplican a toda la aplicación
 */

/* Reset Global */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100%;
  overflow-x: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
}

/* Variables CSS para la nueva paleta de colores */
:root {
  /* Púrpuras - Paleta Principal */
  --color-purple-darkest: #3D0066;
  --color-purple-dark: #510087;
  --color-purple: #5C0099;
  
  /* Amarillos - Acentos */
  --color-yellow-primary: #FDC500;
  --color-yellow-light: #FFD500;
  
  /* Para mantener compatibilidad con código existente */
  --color-orange-primary: #FDC500;  /* Mapea al amarillo */
  --color-orange-light: #FFD500;     /* Mapea al amarillo claro */
  
  /* Grises */
  --color-gray-50: #F9FAFB;
  --color-gray-100: #F3F4F6;
  --color-gray-200: #E5E7EB;
  --color-gray-300: #D1D5DB;
  --color-gray-400: #9CA3AF;
  --color-gray-500: #6B7280;
  --color-gray-600: #4B5563;
  --color-gray-700: #374151;
  --color-gray-800: #1F2937;
  --color-gray-900: #111827;
  
  /* Estados */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
  --color-info: #3B82F6;
}
/* Scrollbar personalizada */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: var(--color-gray-100);
}

::-webkit-scrollbar-thumb {
  background: var(--color-purple);
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color-purple-light);
}

/* Animaciones globales */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Clases de utilidad globales */
.animate-fade-in {
  animation: fadeIn 0.8s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.8s ease-out;
}
</style>