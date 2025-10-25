<template>
  <!-- 
    TopBar.vue - Barra superior con información de contacto
    
    Propósito: Mostrar teléfono, email y enlaces de ayuda
    Conecta con: MainLayout.vue (componente padre)
    Ubicación: Parte superior fija de todas las páginas
  -->
  <div class="top-bar">
    <div class="top-bar-content">
      <!-- Información de contacto -->
      <div class="top-left">
        <a href="tel:+59144123456" class="top-link">
          <VaIcon name="phone" size="small" />
          <span>+59165324767</span>
        </a>
        <a href="mailto:info@guiaspurpuras.com" class="top-link">
          <VaIcon name="email" size="small" />
          <span>info@guiaspurpuras.com.bo</span>
        </a>
      </div>

      <!-- Enlaces secundarios -->
      <div class="top-right">
        <a href="#" class="top-link">
          <VaIcon name="help_outline" size="small" />
          <span>Ayuda</span>
        </a>
        <div class="language-selector">
          <VaIcon name="language" size="small" />
          <span>ES</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TopBar'
}
</script>

<style scoped>
/**
 * Estilos del TopBar
 * Usa variables CSS definidas en App.vue
 */

.top-bar {
  background: var(--color-purple-dark);
  color: #ffffff;
  padding: 0.75rem 0;
  font-size: 0.85rem;
  width: 100%;
}

.top-bar-content {
  max-width: 100%;
  padding: 0 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top-left,
.top-right {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.top-link {
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s;
}

.top-link:hover {
  color: var(--color-orange-primary);
}

.language-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  transition: background 0.3s;
}

.language-selector:hover {
  background: rgba(255, 255, 255, 0.15);
}

/* Responsive */
@media (max-width: 768px) {
  .top-bar {
    display: none;
  }
}
</style>