<template>
  <!-- 
    HomeView.vue - Vista principal del sitio
    
    Propósito: Ensamblar todas las secciones del Home
    Conecta con: MainLayout.vue (layout) y componentes de Home/
  -->
  <MainLayout>
    <!-- Hero con Búsqueda y Geolocalización -->
    <HeroSection />

    <!-- 4 Guías Principales (Cards Flotantes) -->
    <GuidesSection />

    <!-- Testimonios -->
    <TestimonialsSection />

    <!-- CTA Final -->
    <CTABanner />
  </MainLayout>
</template>

<script>
/**
 * HomeView Component
 * 
 * Componentes hijos:
 * - MainLayout: Layout principal (TopBar + Navbar + Footer)
 * - HeroSection: Hero con búsqueda y geolocalización automática
 * - GuidesSection: 4 cards flotantes de categorías principales
 * - TestimonialsSection: Testimonios de usuarios
 * - CTABanner: Llamado a la acción final
 * 
 * ✅ Geolocalización: Implementada en HeroSection via useSearchStore
 */

import MainLayout from '@/components/Layout/MainLayout.vue'
import HeroSection from '@/components/Home/HeroSection.vue'
import GuidesSection from '@/components/Home/GuidesSection.vue'
import TestimonialsSection from '@/components/Home/TestimonialsSection.vue'
import CTABanner from '@/components/Home/CTABanner.vue'

export default {
  name: 'HomeView',
  components: {
    MainLayout,
    HeroSection,
    GuidesSection,
    TestimonialsSection,
    CTABanner
  }
}
</script>

<style scoped>
/* No se necesitan estilos en HomeView, cada componente maneja sus propios estilos */
</style>