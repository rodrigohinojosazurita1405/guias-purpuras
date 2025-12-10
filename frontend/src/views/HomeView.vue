<template>
  <!-- 
    HomeView.vue - Vista principal del sitio
    
    Propósito: Ensamblar todas las secciones del Home
    Conecta con: MainLayout.vue (layout) y componentes de Home/
  -->
  <MainLayout>
    <!-- Hero con Búsqueda y Geolocalización -->
    <HeroSection />

    <!-- Categorías Populares -->
    <PopularCategories />

    <!-- Anuncios Destacados -->
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
 * - HeroSection: Hero rediseñado funcional con búsqueda protagonista
 * - PopularCategories: Categorías principales con íconos
 * - GuidesSection: Anuncios destacados (estilo OLX)
 * - TestimonialsSection: Testimonios simplificados
 * - CTABanner: CTA minimalista
 *
 * ✅ Geolocalización: Implementada en HeroSection via useSearchStore
 */

import MainLayout from '@/components/Layout/MainLayout.vue'
import HeroSection from '@/components/Home/HeroSection.vue'
import PopularCategories from '@/components/Home/PopularCategories.vue'
import GuidesSection from '@/components/Home/GuidesSection.vue'
import TestimonialsSection from '@/components/Home/TestimonialsSection.vue'
import CTABanner from '@/components/Home/CTABanner.vue'

export default {
  name: 'HomeView',
  components: {
    MainLayout,
    HeroSection,
    PopularCategories,
    GuidesSection,
    TestimonialsSection,
    CTABanner
  }
}
</script>

<style scoped>
/* No se necesitan estilos en HomeView, cada componente maneja sus propios estilos */
</style>