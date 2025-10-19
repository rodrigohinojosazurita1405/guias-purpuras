<template>
  <!-- 
    ═══════════════════════════════════════════════════════════
    GuideView.vue - Vista Principal de Guía (REFACTORIZADA)
    ═══════════════════════════════════════════════════════════
    
    Responsabilidad: Solo orquestar componentes
    Componentes hijos: FiltersSidebar, ListingCard
    Conexión Django: GET /api/listings/?guide=profesionales
  -->
  <MainLayout>
    
    <!-- ========== Breadcrumb ========== -->
    <section class="breadcrumb-section">
      <div class="breadcrumb-container">
        <div class="breadcrumb">
          <a href="#">Inicio</a>
          <VaIcon name="chevron_right" size="small" />
          <span class="current">{{ currentGuide.name }}</span>
        </div>
        <VaButton preset="plain" icon="tune" class="mobile-btn" @click="showMobileFilters = true">
          Filtros
        </VaButton>
      </div>
    </section>

    <!-- ========== Contenido Principal ========== -->
    <section class="guide-content">
      <div class="content-container">
        
        <!-- Sidebar de Filtros (Desktop) -->
        <FiltersSidebar 
          :subcategories="currentGuide.subcategories"
          :cities="cities"
          @filter-change="handleFilterChange"
        />

        <!-- Área de Listados -->
        <div class="listings-area">
          <!-- Header -->
          <div class="listings-header">
            <h2>{{ mockListings.length }} Resultados</h2>
            <select v-model="sortBy" class="sort-select">
              <option value="recent">Más Recientes</option>
              <option value="rating">Mejor Calificados</option>
            </select>
          </div>

          <!-- Grid con Cards (SOLO 2 ejemplos) -->
          <div class="listings-grid">
            <ListingCard 
              v-for="listing in mockListings" 
              :key="listing.id"
              :listing="listing"
              @click="viewListing"
            />
          </div>

          <!-- Paginación -->
          <div class="pagination">
            <VaButton preset="plain" icon="chevron_left" disabled />
            <VaButton class="page-btn active">1</VaButton>
            <VaButton preset="plain" icon="chevron_right" disabled />
          </div>
        </div>

      </div>
    </section>

  </MainLayout>
</template>

<script>
/**
 * ═══════════════════════════════════════════════════════════
 * GuideView - Script (Refactorizado)
 * ═══════════════════════════════════════════════════════════
 */

import MainLayout from '@/components/Layout/MainLayout.vue'
import FiltersSidebar from '@/components/Guide/FiltersSidebar.vue'
import ListingCard from '@/components/Guide/ListingCard.vue'

export default {
  name: 'GuideView',
  components: { MainLayout, FiltersSidebar, ListingCard },
  
  data() {
    return {
      showMobileFilters: false,
      sortBy: 'recent',
      
      // TODO: Obtener desde Django /api/guides/:slug/
      currentGuide: {
        name: 'Guías Profesionales',
        subcategories: ['Abogados', 'Contadores', 'Arquitectos']
      },
      
      cities: ['La Paz', 'Cochabamba', 'Santa Cruz'],
      
      // TODO: Obtener desde Django /api/listings/
      mockListings: [
        {
          id: 1,
          category: 'Abogados',
          title: 'Dr. Carlos Mendoza - Abogado',
          image: 'https://images.unsplash.com/photo-1556157382-97eda2d62296?w=400',
          location: 'Cochabamba',
          timeAgo: 'Hace 2h',
          plan: 'top',
          verified: true,
          rating: 5,
          reviews: 48,
          views: 234
        },
        {
          id: 2,
          category: 'Contadores',
          title: 'Lic. María Torres - Contadora',
          image: 'https://images.unsplash.com/photo-1554224311-beee2c0c2d98?w=400',
          location: 'Cochabamba',
          timeAgo: 'Hace 5h',
          plan: 'featured',
          verified: false,
          rating: 4,
          reviews: 23,
          views: 156
        }
      ]
    }
  },
  
  methods: {
    /**
     * Maneja cambio de filtros
     * TODO: Llamar API Django con nuevos filtros
     */
    handleFilterChange(filters) {
      console.log('Filtros aplicados:', filters)
      // TODO: axios.get('/api/listings/', { params: filters })
    },
    
    /**
     * Navega al detalle
     * TODO: this.$router.push(`/anuncio/${listing.id}`)
     */
    viewListing(listing) {
      console.log('Ver:', listing.id)
    }
  }
}
</script>

<style scoped>
/* ========== Breadcrumb ========== */
.breadcrumb-section {
  background: var(--color-gray-50);
  border-bottom: 1px solid var(--color-gray-200);
  padding: 1rem 0;
}

.breadcrumb-container {
  padding: 0 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumb .current {
  color: var(--color-purple-dark);
  font-weight: 600;
}

.mobile-btn {
  display: none;
}

/* ========== Layout ========== */
.guide-content {
  padding: 2rem 0;
}

.content-container {
  padding: 0 3rem;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
}

/* ========== Listings Area ========== */
.listings-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.listings-header h2 {
  font-size: 1.8rem;
  color: var(--color-gray-900);
}

.sort-select {
  padding: 0.75rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 8px;
}

.listings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.page-btn.active {
  background: var(--color-purple-dark) !important;
  color: #ffffff !important;
}

/* ========== Responsive ========== */
@media (max-width: 1024px) {
  .content-container {
    grid-template-columns: 1fr;
  }
  
  .mobile-btn {
    display: flex;
  }
}
</style>