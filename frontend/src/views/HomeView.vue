<template>
  <!-- 
    HomeView.vue - Vista principal del sitio
    
    Propósito: Ensamblar todas las secciones del Home
    Conecta con: MainLayout.vue (layout) y todos los componentes de Home/
  -->
  <MainLayout>
    <!-- Hero con Búsqueda -->
    <HeroSection />

    <!-- 4 Guías Principales -->
    <GuidesSection />

    <!-- Anuncios Destacados -->
    <FeaturedSection />

    <!-- Cómo Funciona -->
    <HowItWorksSection />

    <!-- Planes y Precios -->
    <PricingSection />

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
 * - MainLayout: Layout principal (Navbar + Footer)
 * - HeroSection: Hero con búsqueda y navegación a categorías
 * - GuidesSection: 4 guías principales
 * - FeaturedSection: Anuncios destacados
 * - HowItWorksSection: Cómo funciona
 * - PricingSection: Planes y precios
 * - TestimonialsSection: Testimonios
 * - CTABanner: Llamado a la acción
 * 
 * Nota: La navegación ahora es manejada directamente por cada componente
 */

import MainLayout from '@/components/Layout/MainLayout.vue'
import HeroSection from '@/components/Home/HeroSection.vue'
import GuidesSection from '@/components/Home/GuidesSection.vue'
import FeaturedSection from '@/components/Home/FeaturedSection.vue'
import HowItWorksSection from '@/components/Home/HowItWorksSection.vue'
import PricingSection from '@/components/Home/PricingSection.vue'
import TestimonialsSection from '@/components/Home/TestimonialsSection.vue'
import CTABanner from '@/components/Home/CTABanner.vue'

export default {
  name: 'HomeView',
  components: {
    MainLayout,
    HeroSection,
    GuidesSection,
    FeaturedSection,
    HowItWorksSection,
    PricingSection,
    TestimonialsSection,
    CTABanner
  }
}
</script>

<style scoped>
/* No se necesitan estilos en HomeView, cada componente maneja sus propios estilos */
</style>