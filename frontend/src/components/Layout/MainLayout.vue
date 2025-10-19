<template>
  <!-- 
    MainLayout.vue - Layout principal de la aplicación
    
    Propósito: Estructura base que envuelve todas las páginas
    Componentes hijos: TopBar, Navbar, Footer
    Emite: change-location (desde Navbar hacia las vistas)
    Ubicación: Envuelve todo el contenido de las vistas
  -->
  <div class="main-layout">
    <!-- Barra Superior -->
    <TopBar />

    <!-- Navegación Principal -->
    <Navbar 
      :current-location="currentLocation"
      @change-location="$emit('change-location')"
    />

    <!-- Contenido Principal (slot para las vistas) -->
    <main class="main-content">
      <slot></slot>
    </main>

    <!-- Pie de Página -->
    <Footer />
  </div>
</template>

<script>
/**
 * MainLayout Component
 * 
 * Componentes:
 * - TopBar: Barra superior con contacto
 * - Navbar: Navegación principal
 * - Footer: Pie de página
 * 
 * Props: Ninguno (recibe datos de las vistas padre)
 * 
 * Emits:
 * - change-location: cuando el usuario quiere cambiar su ubicación
 * 
 * Slot:
 * - default: contenido de las vistas (HomeView, GuideView, etc.)
 */

import TopBar from './TopBar.vue'
import Navbar from './Navbar.vue'
import Footer from './Footer.vue'

export default {
  name: 'MainLayout',
  components: {
    TopBar,
    Navbar,
    Footer
  },
  emits: ['change-location'],
  data() {
    return {
      // Ubicación actual del usuario (mock)
      // TODO: Obtener desde localStorage o API de geolocalización
      currentLocation: 'Cochabamba, Bolivia'
    }
  }
}
</script>

<style scoped>
/**
 * Estilos del Layout Principal
 * Mínimos, solo estructura base
 */

.main-layout {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  width: 100%;
  padding: 0;
  margin: 0;
}
</style>