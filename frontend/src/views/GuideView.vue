<!-- 
  ═══════════════════════════════════════════════════════════
  GuideView.vue - Vista Principal de Guía (CORREGIDO)
  ═══════════════════════════════════════════════════════════
  
  Responsabilidad: Mostrar listado de anuncios según categoría
  Componentes: TopFiltersBar, FiltersSidebar, ProfessionalCard, RestaurantCard, JobCard, ListingCard
  Conexión Django: GET /api/listings/?category=profesionales
-->
<template>
  <MainLayout>
    
    <!-- ========== Breadcrumb ========== -->
    <section class="breadcrumb-section">
      <div class="breadcrumb-container">
        <div class="breadcrumb">
          <router-link to="/">Inicio</router-link>
          <VaIcon name="chevron_right" size="small" />
          <span class="current">{{ guideName }}</span>
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
          
          <!-- ========== FILTROS SUPERIORES ========== -->
          <TopFiltersBar
            :category="category"
            :subcategories="currentGuide.subcategories"
            :cities="cities"
            :results-count="filteredListings.length"
            v-model="topFilters"
            @filter-change="handleTopFilterChange"
          />

          <!-- Header con Sort -->
          <div class="listings-header">
            <div class="header-info">
              <h2>{{ guideName }}</h2>
             
            </div>
            <select v-model="sortBy" class="sort-select" @change="sortListings">
              <option value="recent">Más Recientes</option>
              <option value="rating">Mejor Calificados</option>
              <option value="featured">Destacados</option>
              <option value="name">Nombre (A-Z)</option>
            </select>
          </div>

          <!-- Grid con Cards -->
          <div class="listings-grid">
            <!-- Profesionales -->
            <ProfessionalCard 
              v-if="category === 'profesionales'"
              v-for="listing in paginatedListings" 
              :key="listing.id"
              :listing="listing"
            />

            <!-- Gastronomía -->
            <RestaurantCard 
              v-else-if="category === 'gastronomia'"
              v-for="listing in paginatedListings" 
              :key="listing.id"
              :listing="listing"
            />

            <!-- Trabajos -->
            <JobCard 
              v-else-if="category === 'trabajos'"
              v-for="listing in paginatedListings" 
              :key="listing.id"
              :listing="listing"
            />

            <!-- Servicios (Genérico) -->
            <ListingCard 
              v-else
              v-for="listing in paginatedListings" 
              :key="listing.id"
              :listing="listing"
              @click="viewListing"
            />
          </div>

          <!-- Estado vacío -->
          <div v-if="filteredListings.length === 0" class="empty-state">
            <va-icon name="search_off" size="4rem" color="#CCC" />
            <h3>No se encontraron resultados</h3>
            <p>Intenta ajustar los filtros de búsqueda</p>
            <va-button @click="clearAllFilters" color="purple">
              Limpiar filtros
            </va-button>
          </div>

          <!-- Paginación -->
          <div v-if="filteredListings.length > 0" class="pagination">
            <VaButton 
              preset="plain" 
              icon="chevron_left" 
              :disabled="currentPage === 1"
              @click="previousPage"
            />
            <VaButton 
              v-for="page in totalPages" 
              :key="page"
              :class="['page-btn', { active: page === currentPage }]"
              @click="goToPage(page)"
            >
              {{ page }}
            </VaButton>
            <VaButton 
              preset="plain" 
              icon="chevron_right" 
              :disabled="currentPage === totalPages"
              @click="nextPage"
            />
          </div>
        </div>

      </div>
    </section>

  </MainLayout>
</template>

<script>
/**
 * ═══════════════════════════════════════════════════════════
 * GuideView - Script (Con JobCard integrado)
 * ═══════════════════════════════════════════════════════════
 */

import MainLayout from '@/components/Layout/MainLayout.vue'
import TopFiltersBar from '@/components/Guide/TopFiltersBar.vue'
import FiltersSidebar from '@/components/Guide/FiltersSidebar.vue'
import ProfessionalCard from '@/components/Guide/ProfessionalCard.vue'
import RestaurantCard from '@/components/Guide/RestaurantCard.vue'
import JobCard from '@/components/Guide/JobCard.vue'
import ListingCard from '@/components/Guide/ListingCard.vue'

export default {
  name: 'GuideView',
  components: { 
    MainLayout, 
    TopFiltersBar,
    FiltersSidebar, 
    ProfessionalCard,
    RestaurantCard,
    JobCard,
    ListingCard 
  },
  
  props: {
    category: {
      type: String,
      required: true,
      validator: (value) => ['profesionales', 'gastronomia', 'trabajos', 'servicios'].includes(value)
    }
  },
  
  data() {
    return {
      showMobileFilters: false,
      sortBy: 'recent',
      
      // Filtros superiores
      topFilters: {
        subcategory: '',
        city: '',
        search: ''
      },
      
      // Paginación
      currentPage: 1,
      itemsPerPage: 9,
      
      cities: ['La Paz', 'Cochabamba', 'Santa Cruz', 'Oruro', 'Potosí', 'Tarija', 'Sucre', 'Beni', 'Pando'],
      
      // Configuración por categoría
      categoryConfig: {
        profesionales: {
          name: 'Profesionales en Bolivia',
          subcategories: ['Abogados', 'Contadores', 'Arquitectos', 'Doctores', 'Ingenieros', 'Psicólogos']
        },
        gastronomia: {
          name: 'Gastronomía en Bolivia',
          subcategories: ['Comida Tradicional', 'Comida Internacional', 'Pizzerías', 'Cafeterías', 'Heladerías', 'Fast Food']
        },
        trabajos: {
          name: 'Ofertas de Trabajo en Bolivia',
          subcategories: ['Tiempo Completo', 'Medio Tiempo', 'Freelance', 'Remoto', 'Pasantías']
        },
        servicios: {
          name: 'Servicios en Bolivia',
          subcategories: ['Plomería', 'Electricidad', 'Limpieza', 'Mudanzas', 'Reparaciones', 'Jardinería']
        }
      },
      
      // Mock data - TODO: Reemplazar con API
      allListings: []
    }
  },
  
  computed: {
    /**
     * Obtiene la configuración de la guía actual
     */
    currentGuide() {
      return {
        name: this.categoryConfig[this.category]?.name || 'Guías',
        subcategories: this.categoryConfig[this.category]?.subcategories || []
      }
    },

    /**
     * Nombre de la guía actual
     */
    guideName() {
      return this.currentGuide.name
    },

    /**
     * Listados filtrados
     */
    filteredListings() {
      let results = [...this.allListings]

      // Filtrar por subcategoría
      if (this.topFilters.subcategory) {
        results = results.filter(listing => 
          listing.subcategory === this.topFilters.subcategory ||
          listing.professionalTitle?.includes(this.topFilters.subcategory) ||
          listing.contractType === this.topFilters.subcategory
        )
      }

      // Filtrar por ciudad
      if (this.topFilters.city) {
        results = results.filter(listing => 
          listing.city === this.topFilters.city
        )
      }

      // Filtrar por búsqueda
      if (this.topFilters.search) {
        const searchLower = this.topFilters.search.toLowerCase()
        results = results.filter(listing => {
          const title = listing.title?.toLowerCase() || ''
          const professionalTitle = listing.professionalTitle?.toLowerCase() || ''
          const companyName = listing.companyName?.toLowerCase() || ''
          const subcategory = listing.subcategory?.toLowerCase() || ''
          const specialties = listing.specialties?.join(' ').toLowerCase() || ''
          const tags = listing.tags?.join(' ').toLowerCase() || ''
          
          return title.includes(searchLower) || 
                 professionalTitle.includes(searchLower) ||
                 companyName.includes(searchLower) ||
                 subcategory.includes(searchLower) ||
                 specialties.includes(searchLower) ||
                 tags.includes(searchLower)
        })
      }

      return results
    },

    /**
     * Listados ordenados
     */
    sortedListings() {
      const listings = [...this.filteredListings]

      switch (this.sortBy) {
        case 'rating':
          return listings.sort((a, b) => (b.rating || 0) - (a.rating || 0))
        case 'featured':
          return listings.sort((a, b) => {
            const priorityA = a.plan === 'destacado' ? 2 : a.plan === 'premium' ? 1 : 0
            const priorityB = b.plan === 'destacado' ? 2 : b.plan === 'premium' ? 1 : 0
            return priorityB - priorityA
          })
        case 'name':
          return listings.sort((a, b) => a.title.localeCompare(b.title))
        case 'recent':
        default:
          return listings
      }
    },

    /**
     * Listados paginados
     */
    paginatedListings() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.sortedListings.slice(start, end)
    },

    /**
     * Total de páginas
     */
    totalPages() {
      return Math.ceil(this.filteredListings.length / this.itemsPerPage)
    }
  },
  
  methods: {
    /**
     * Maneja cambio de filtros superiores
     */
    handleTopFilterChange(filters) {
      this.topFilters = { ...filters }
      this.currentPage = 1 // Reset a página 1
    },

    /**
     * Maneja cambio de filtros del sidebar
     */
    handleFilterChange(filters) {
      console.log('Filtros sidebar:', filters)
      // TODO: Integrar con filtros superiores si es necesario
    },

    /**
     * Limpia todos los filtros
     */
    clearAllFilters() {
      this.topFilters = {
        subcategory: '',
        city: '',
        search: ''
      }
      this.currentPage = 1
    },

    /**
     * Ordena los listados
     */
    sortListings() {
      this.currentPage = 1 // Reset a página 1
    },
    
    /**
     * Navega al detalle
     */
    viewListing(listing) {
      console.log('Ver:', listing.id)
      this.$router.push(`/guias/${this.category}/${listing.slug || listing.id}`)
    },

    /**
     * Paginación
     */
    goToPage(page) {
      this.currentPage = page
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },

    /**
     * Obtiene listados desde la API
     */
    async fetchListings() {
      try {
        // TODO: Llamar API real
        // const response = await fetch(`/api/listings/?category=${this.category}`)
        // this.allListings = await response.json()
        
        // Mock data por categoría
        this.loadMockData()
      } catch (error) {
        console.error('Error cargando listados:', error)
      }
    },

    /**
     * Carga datos mock según la categoría
     */
    loadMockData() {
      if (this.category === 'profesionales') {
        this.allListings = [
          {
            id: 1,
            slug: 'juan-perez-abogado',
            title: 'Dr. Juan Pérez',
            professionalTitle: 'Abogado especializado en derecho civil y familiar',
            subcategory: 'Abogados',
            yearsExperience: 15,
            specialties: ['Derecho Civil', 'Derecho Familiar', 'Mediación'],
            city: 'Cochabamba',
            plan: 'destacado',
            verified: true,
            rating: 4.8,
            images: [{ url: 'https://images.unsplash.com/photo-1556157382-97eda2d62296?w=400' }]
          },
          {
            id: 2,
            slug: 'maria-gomez-doctora',
            title: 'Dra. María Gómez',
            professionalTitle: 'Médico General con especialidad en Pediatría',
            subcategory: 'Doctores',
            yearsExperience: 10,
            specialties: ['Pediatría', 'Medicina General', 'Vacunación'],
            city: 'La Paz',
            plan: 'premium',
            verified: false,
            rating: 4.9,
            images: [{ url: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400' }]
          },
          {
            id: 3,
            slug: 'carlos-rodriguez-contador',
            title: 'Lic. Carlos Rodríguez',
            professionalTitle: 'Contador Público Autorizado',
            subcategory: 'Contadores',
            yearsExperience: 8,
            specialties: ['Contabilidad', 'Auditoría', 'Impuestos'],
            city: 'Santa Cruz',
            plan: 'free',
            verified: false,
            rating: 4.5,
            images: []
          },
          {
            id: 4,
            slug: 'ana-martinez-arquitecta',
            title: 'Arq. Ana Martínez',
            professionalTitle: 'Arquitecta especializada en diseño moderno',
            subcategory: 'Arquitectos',
            yearsExperience: 12,
            specialties: ['Diseño Arquitectónico', 'Remodelación', 'Construcción'],
            city: 'Cochabamba',
            plan: 'premium',
            verified: true,
            rating: 5.0,
            images: [{ url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400' }]
          }
        ]
      } else if (this.category === 'gastronomia') {
        this.allListings = [
          {
            id: 1,
            slug: 'el-sabor-boliviano',
            title: 'Restaurante El Sabor Boliviano',
            subcategory: 'Comida Tradicional',
            priceRange: 'moderado',
            schedule: 'Lun-Dom: 12:00 - 22:00',
            capacity: 80,
            parking: true,
            deliveryAvailable: true,
            city: 'Cochabamba',
            plan: 'destacado',
            verified: true,
            rating: 4.7,
            images: [{ url: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400' }],
            menuItems: [
              { name: 'Pique Macho', price: 45, image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=200' },
              { name: 'Silpancho', price: 35, image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=200' },
              { name: 'Sajta de Pollo', price: 40, image: 'https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=200' }
            ]
          },
          {
            id: 2,
            slug: 'pizzeria-italiana',
            title: 'Pizzería Italiana Don Giuseppe',
            subcategory: 'Pizzerías',
            priceRange: 'moderado',
            schedule: 'Mar-Dom: 18:00 - 23:00',
            capacity: 50,
            parking: false,
            deliveryAvailable: true,
            city: 'La Paz',
            plan: 'premium',
            verified: true,
            rating: 4.6,
            images: [{ url: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400' }],
            menuItems: [
              { name: 'Pizza Margarita', price: 55, image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=200' },
              { name: 'Pizza Pepperoni', price: 60, image: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=200' }
            ]
          },
          {
            id: 3,
            slug: 'cafe-del-centro',
            title: 'Café del Centro',
            subcategory: 'Cafeterías',
            priceRange: 'economico',
            schedule: 'Lun-Sáb: 8:00 - 20:00',
            capacity: 30,
            parking: false,
            deliveryAvailable: false,
            city: 'Santa Cruz',
            plan: 'free',
            verified: false,
            rating: 4.4,
            images: [{ url: 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400' }],
            menuItems: []
          }
        ]
      } else if (this.category === 'trabajos') {
        this.allListings = [
          {
            id: 1,
            title: 'Desarrollador Full Stack Senior',
            companyName: 'TechCorp Bolivia',
            companyLogo: 'https://via.placeholder.com/150x60/5C0099/FFFFFF?text=TechCorp',
            city: 'Cochabamba',
            contractType: 'Tiempo Completo',
            modality: 'Remoto',
            salary: 'Bs. 5000 - 8000',
            tags: ['Python', 'React', 'PostgreSQL', 'AWS'],
            publishedDaysAgo: 2,
            plan: 'destacado',
            verified: true,
            confidential: false,
            urgent: false,
            subcategory: 'Tiempo Completo'
          },
          {
            id: 2,
            title: 'Diseñador Gráfico',
            companyName: 'Importante Empresa',
            companyLogo: null,
            city: 'La Paz',
            contractType: 'Medio Tiempo',
            modality: 'Híbrido',
            salary: 'Bs. 3000 - 4500',
            tags: ['Adobe Suite', 'Illustrator', 'Photoshop', 'Branding'],
            publishedDaysAgo: 3,
            plan: 'premium',
            verified: false,
            confidential: false,
            importantCompany: true,
            urgent: false,
            subcategory: 'Medio Tiempo'
          },
          {
            id: 3,
            title: 'Analista de Marketing Digital',
            companyName: null,
            companyLogo: null,
            city: 'Santa Cruz',
            contractType: 'Tiempo Completo',
            modality: 'Presencial',
            salary: 'No Declarado',
            tags: ['SEO', 'Google Ads', 'Analytics', 'Social Media'],
            publishedDaysAgo: 5,
            plan: 'free',
            verified: false,
            confidential: true,
            urgent: true,
            subcategory: 'Tiempo Completo'
          },
          {
            id: 4,
            title: 'Contador Senior',
            companyName: 'Consultora Financiera ABC',
            companyLogo: 'https://via.placeholder.com/150x60/2E7D32/FFFFFF?text=ABC',
            city: 'Cochabamba',
            contractType: 'Tiempo Completo',
            modality: 'Presencial',
            salary: 'Bs. 6000 - 9000',
            tags: ['Contabilidad', 'Impuestos', 'Auditoría', 'NIC'],
            publishedDaysAgo: 1,
            plan: 'premium',
            verified: true,
            confidential: false,
            urgent: false,
            subcategory: 'Tiempo Completo'
          }
        ]
      } else if (this.category === 'servicios') {
        this.allListings = [
          {
            id: 1,
            category: 'Negocios',
            title: 'Plomería Profesional - Urgencias 24/7',
            subcategory: 'Plomería',
            image: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400',
            city: 'Cochabamba',
            timeAgo: 'Hace 2h',
            plan: 'destacado',
            verified: true,
            rating: 5,
            reviews: 32,
            views: 267
          },
          {
            id: 2,
            category: 'Servicios',
            title: 'Electricista Certificado',
            subcategory: 'Electricidad',
            image: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=400',
            city: 'Santa Cruz',
            timeAgo: 'Hace 1 día',
            plan: 'premium',
            verified: false,
            rating: 4,
            reviews: 18,
            views: 123
          }
        ]
      }
    }
  },

  /**
   * Al montar el componente, cargar los listados
   */
  mounted() {
    this.fetchListings()
  },

  /**
   * Cuando cambia la categoría (prop), recargar
   */
  watch: {
    category: {
      handler() {
        this.fetchListings()
        this.clearAllFilters() // Limpiar filtros al cambiar de categoría
      },
      immediate: false
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

.breadcrumb a {
  color: var(--color-purple);
  text-decoration: none;
  transition: color 0.3s ease;
}

.breadcrumb a:hover {
  color: var(--color-purple-dark);
  text-decoration: underline;
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
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
  min-height: calc(100vh - 250px);
}

.content-container {
  padding: 0 3rem;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
}

/* ========== Listings Area ========== */
.listings-area {
  width: 100%;
}

.listings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
}

.header-info h2 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0;
}

.sort-select {
  padding: 0.875rem 1rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--color-gray-900);
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sort-select:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

.listings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

/* ========== Empty State ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-dark);
  margin: 1rem 0 0.5rem 0;
}

.empty-state p {
  font-size: 1rem;
  color: #666;
  margin: 0 0 2rem 0;
}

/* ========== Pagination ========== */
.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 3rem;
}

.page-btn {
  min-width: 44px;
}

.page-btn.active {
  background: var(--color-purple) !important;
  color: #ffffff !important;
}

/* ========== Responsive ========== */
@media (max-width: 1024px) {
  .content-container {
    grid-template-columns: 1fr;
    padding: 0 2rem;
  }
  
  .mobile-btn {
    display: flex;
  }

  .listings-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .breadcrumb-container,
  .content-container {
    padding: 0 1.5rem;
  }

  .header-info h2 {
    font-size: 1.5rem;
  }

  .listings-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .sort-select {
    width: 100%;
  }

  .listings-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .pagination {
    margin-top: 2rem;
  }
}
</style>