<template>
  <!-- 
    HomeView.vue - Vista principal del sitio
    
    Propósito: Ensamblar todas las secciones del Home
    Conecta con: MainLayout.vue (layout) y todos los componentes de Home/
    Emite: change-location (hacia MainLayout)
    Responsabilidad: Solo organizar componentes, sin lógica compleja
  -->
  <MainLayout @change-location="showLocationModal = true">
    <!-- Hero con Búsqueda -->
    <HeroSection @search="handleSearch" />

    <!-- 4 Guías Principales -->
    <GuidesSection @guide-click="handleGuideClick" />

    <!-- Anuncios Destacados -->
    <FeaturedSection @listing-click="handleListingClick" />

    <!-- Cómo Funciona -->
    <HowItWorksSection @publish-click="handlePublish" />

    <!-- Planes y Precios -->
    <PricingSection @plan-select="handlePlanSelect" />

    <!-- Testimonios -->
    <TestimonialsSection />

    <!-- CTA Final -->
    <CTABanner 
      @publish-click="handlePublish" 
      @explore-click="handleExplore"
    />

    <!-- Modal de Selección de Ubicación -->
    <VaModal v-model="showLocationModal" size="large":hide-default-actions="true">
      <template #header>
        <h3>Selecciona tu Ubicación</h3>
      </template>

      <div class="location-modal-content">
        <!-- Botón de Geolocalización -->
        <VaButton block class="detect-location-btn" @click="detectLocation">
          <VaIcon name="my_location" />
          Detectar mi Ubicación Automáticamente
        </VaButton>

        <div class="divider">
          <span>O elige manualmente</span>
        </div>

        <!-- Grid de Ciudades -->
        <div class="cities-grid">
          <button 
            v-for="city in cities" 
            :key="city"
            :class="['city-btn', { active: selectedCity === city }]"
            @click="selectCity(city)"
          >
            <VaIcon name="location_city" />
            {{ city }}
          </button>
        </div>

        <!-- Botones de Acción -->
        <div class="modal-actions">
          <VaButton preset="secondary" @click="showLocationModal = false">
            Cancelar
          </VaButton>
          <VaButton color="var(--color-purple-dark)" @click="confirmLocation">
            Confirmar
          </VaButton>
        </div>
      </div>
    </VaModal>
  </MainLayout>
</template>

<script>
/**
 * HomeView Component
 * 
 * Componentes hijos:
 * - MainLayout: Layout principal (Navbar + Footer)
 * - HeroSection: Hero con búsqueda
 * - GuidesSection: 4 guías principales
 * - FeaturedSection: Anuncios destacados
 * - HowItWorksSection: Cómo funciona
 * - PricingSection: Planes y precios
 * - TestimonialsSection: Testimonios
 * - CTABanner: Llamado a la acción
 * 
 * State:
 * - showLocationModal: controla visibilidad del modal
 * - selectedCity: ciudad seleccionada por el usuario
 * - cities: lista de ciudades de Bolivia
 * 
 * Methods:
 * - handleSearch: procesa búsquedas del Hero
 * - handleGuideClick: navega a una guía específica
 * - handleListingClick: navega al detalle de un anuncio
 * - handlePublish: redirige a publicar anuncio
 * - handlePlanSelect: procesa selección de plan
 * - detectLocation: obtiene ubicación del navegador
 * - confirmLocation: guarda ubicación seleccionada
 * 
 * TODO:
 * - Implementar Vue Router para navegación
 * - Conectar con Django API para datos reales
 * - Guardar ubicación en localStorage
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
  },
  data() {
    return {
      showLocationModal: false,
      selectedCity: '',
      
      // Ciudades de Bolivia
      cities: [
        'La Paz', 'Cochabamba', 'Santa Cruz', 'Sucre',
        'Oruro', 'Potosí', 'Tarija', 'Beni', 'Pando'
      ]
    }
  },
  methods: {
    /**
     * Maneja búsqueda desde HeroSection
     * @param {Object} searchData - { query, city, guide }
     */
    handleSearch(searchData) {
      console.log('Búsqueda recibida en HomeView:', searchData)
      
      // TODO: Implementar navegación con Vue Router
      // this.$router.push({
      //   name: 'GuideView',
      //   params: { guide: searchData.guide },
      //   query: { q: searchData.query, city: searchData.city }
      // })
    },

    /**
     * Navega a una guía específica
     * @param {Object} guide - Objeto guía
     */
    handleGuideClick(guide) {
      console.log('Navegando a guía:', guide.slug)
      
      // TODO: Implementar navegación
      // this.$router.push(`/guia/${guide.slug}`)
    },

    /**
     * Navega al detalle de un anuncio
     * @param {Object} listing - Objeto anuncio
     */
    handleListingClick(listing) {
      console.log('Navegando a anuncio:', listing.id)
      
      // TODO: Implementar navegación
      // this.$router.push(`/anuncio/${listing.id}`)
    },

    /**
     * Redirige a página de publicar
     */
    handlePublish() {
      console.log('Redirigiendo a publicar')
      
      // TODO: Implementar navegación
      // this.$router.push('/publicar')
    },

    /**
     * Procesa selección de plan
     * @param {Object} plan - Plan seleccionado
     */
    handlePlanSelect(plan) {
      console.log('Plan seleccionado:', plan.name)
      
      // TODO: Si es plan gratis, ir a publicar
      // TODO: Si es plan de pago, ir a checkout
      // if (plan.price === 0) {
      //   this.$router.push('/publicar')
      // } else {
      //   this.$router.push(`/checkout/${plan.id}`)
      // }
    },

    /**
     * Explora anuncios
     */
    handleExplore() {
      console.log('Explorando anuncios')
      
      // TODO: Implementar navegación
      // this.$router.push('/explorar')
    },

    /**
     * Detecta ubicación del navegador
     */
    detectLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            console.log('Ubicación detectada:', position.coords)
            
            // TODO: Hacer reverse geocoding con API
            // Por ahora, mock
            this.selectedCity = 'Cochabamba'
            this.showLocationModal = false
            
            // TODO: Guardar en localStorage
            // localStorage.setItem('userCity', this.selectedCity)
          },
          (error) => {
            console.error('Error de geolocalización:', error)
            alert('No se pudo detectar tu ubicación. Por favor selecciona manualmente.')
          }
        )
      } else {
        alert('Tu navegador no soporta geolocalización')
      }
    },

    /**
     * Selecciona una ciudad manualmente
     * @param {String} city - Nombre de la ciudad
     */
    selectCity(city) {
      this.selectedCity = city
    },

    /**
     * Confirma la ubicación seleccionada
     */
    confirmLocation() {
      if (!this.selectedCity) {
        alert('Por favor selecciona una ciudad')
        return
      }
      
      console.log('Ubicación confirmada:', this.selectedCity)
      
      // TODO: Guardar en localStorage
      // localStorage.setItem('userCity', this.selectedCity)
      
      // TODO: Emitir evento o actualizar store de Pinia
      
      this.showLocationModal = false
    }
  }
}
</script>

<style scoped>
/**
 * Estilos del HomeView
 * Solo estilos del modal, el resto está en los componentes
 */

/* Modal de Ubicación */
.location-modal-content {
  padding: 1rem 0;
}

.detect-location-btn {
  background: linear-gradient(135deg, var(--color-orange-primary) 0%, var(--color-orange-light) 100%) !important;
  color: #ffffff !important;
  font-weight: 600 !important;
  padding: 1rem !important;
  margin-bottom: 2rem;
}

.divider {
  text-align: center;
  margin: 2rem 0;
  position: relative;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--color-gray-200);
}

.divider span {
  background: #ffffff;
  padding: 0 1rem;
  position: relative;
  z-index: 1;
  color: var(--color-gray-500);
}

.cities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.city-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem 1rem;
  background: var(--color-gray-50);
  border: 2px solid var(--color-gray-200);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  color: var(--color-gray-600);
}

.city-btn:hover {
  background: var(--color-gray-100);
  border-color: var(--color-gray-300);
}

.city-btn.active {
  background: var(--color-purple-dark);
  color: #ffffff;
  border-color: var(--color-purple-dark);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-gray-200);
}

/* Responsive */
@media (max-width: 768px) {
  .cities-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>