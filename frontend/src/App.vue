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

  /* Estados */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
  --color-info: #3B82F6;

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

/* ==========================================
   VUESTIC UI LABEL COLOR OVERRIDE - FORCE
   ========================================== */
/* Usar !important para forzar override de estilos Vuestic */
:root {
  --va-text-element-color: #2D3748 !important;
}

/* Override directo para todos los labels de Vuestic */
.va-input__label {
  color: #2D3748 !important;
}

.va-select__label {
  color: #2D3748 !important;
}

.va-textarea__label {
  color: #2D3748 !important;
}

.va-date-input__label {
  color: #2D3748 !important;
}

.va-radio__label {
  color: #2D3748 !important;
}

.va-switch__label {
  color: #2D3748 !important;
}

.va-checkbox__label {
  color: #2D3748 !important;
}

/* Required marks */
.va-input__required-mark,
.va-select__required-mark,
.va-textarea__required-mark,
.va-date-input__required-mark {
  color: #EF4444 !important;
}

/* Label genérico */
label {
  color: #2D3748 !important;
}

/* Selector por atributo como último recurso */
[class*="label"] {
  color: #2D3748 !important;
}

/* ========== VUESTIC UI SPACING OPTIMIZATION ========== */
/* Forzar display flex y gap para espacios visibles */
.va-input,
.va-select,
.va-textarea,
.va-date-input,
.va-radio,
.va-switch,
.va-checkbox {
  display: flex !important;
  flex-direction: column !important;
  gap: 0.6rem !important;
  margin-bottom: 0 !important;
}

/* Labels de Vuestic */
.va-input__label,
.va-select__label,
.va-textarea__label,
.va-date-input__label,
.va-radio__label,
.va-switch__label,
.va-checkbox__label {
  margin: 0 !important;
  padding: 0 !important;
  font-size: 0.95rem !important;
  line-height: 1.1 !important;
  font-weight: 500 !important;
  display: block !important;
}

/* Contenedores internos */
.va-input__container,
.va-select__container,
.va-textarea__container,
.va-date-input__container,
.va-radio__container,
.va-switch__container,
.va-checkbox__container {
  gap: 0.6rem !important;
  margin: 0 !important;
}

/* ==========================================
   ESTILOS GLOBALES DE BOTONES
   ========================================== */
/* Botones primarios con gradiente púrpura */
.va-button:not([class*="secondary"]):not([class*="danger"]):not(.btn-delete):not(.delete-confirm-btn),
button.btn-primary,
.btn-purple {
  background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
  color: white !important;
  border: none !important;
  transition: all 0.3s ease !important;
}

.va-button:not([class*="secondary"]):not([class*="danger"]):not(.btn-delete):not(.delete-confirm-btn):hover,
button.btn-primary:hover,
.btn-purple:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
}
</style>