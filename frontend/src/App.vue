<!-- frontend/src/App.vue -->
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
// No hay lógica aquí, solo renderizamos las rutas
</script>

<style>
/* ==========================================
   VARIABLES GLOBALES CSS
   ========================================== */
:root {
  /* Púrpuras */
  --color-purple-darkest: #3D0066;
  --color-purple-dark: #510087;
  --color-purple: #5C0099;
  
  /* Amarillos */
  --color-yellow-primary: rgb(253, 197, 0);
  --color-yellow-light: #FFD500;
  
  /* Grises */
  --color-gray-light: #F5F5F5;
  --color-gray-medium: #E0E0E0;
  --color-gray-dark: #666666;
  
  /* Fuentes */
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ==========================================
   RESET Y ESTILOS BASE
   ========================================== */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-family);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #FFFFFF;
  color: #333333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ==========================================
   UTILIDADES GLOBALES
   ========================================== */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.container-wide {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.text-purple {
  color: var(--color-purple);
}

.text-yellow {
  color: var(--color-yellow-primary);
}

.bg-purple {
  background-color: var(--color-purple);
}

.bg-yellow {
  background-color: var(--color-yellow-primary);
}

/* ==========================================
   TRANSICIONES DE RUTA
   ========================================== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>