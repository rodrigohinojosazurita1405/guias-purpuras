<!-- 
  ═══════════════════════════════════════════════════════════
  GuideView.vue - Vista Principal de Guía UNIFICADA
  ═══════════════════════════════════════════════════════════
  
  ✅ INTEGRADO CON STORE: Lee filtros automáticamente desde useSearchStore
  Responsabilidad: Mostrar listado de anuncios según categoría
  Categorías soportadas: profesionales, gastronomia, trabajos, negocios
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
       
        <!-- Sidebar de Filtros (Desktop y Mobile con overlay) -->
        <FiltersSidebar
          :show-mobile="showMobileFilters"
          :category="category"
          :categories="jobCategories"
          :contract-types="contractTypes"
          :subcategories="currentGuide.subcategories"
          :cities="cities"
          :subcategory-label="currentGuide.subcategoryLabel || 'Subcategoría'"
          :subcategory-placeholder="currentGuide.subcategoryPlaceholder || 'Todas'"
          @filter-change="handleFilterChange"
          @close="showMobileFilters = false"
        />
        
        <!-- Área de Listados -->
        <div class="listings-area">
          
          <!-- ========== FILTROS SUPERIORES ========== -->
          <TopFiltersBar
            :category="category"
            :subcategories="currentGuide.subcategories"
            :categories="jobCategories"
            :contract-types="contractTypes"
            :cities="cities"
            :results-count="filteredListings.length"
            v-model="topFilters"
            @filter-change="handleTopFilterChange"
          />

          <!-- Header con Sort y Toggle de Vista -->
          <div class="listings-header">
            <div class="header-info">
              <h2>{{ guideName }}</h2>
              <!-- Badge de ciudad detectada -->
              <div v-if="searchStore.userDetectedCity && searchStore.locationMethod !== 'manual'" class="location-detected-badge">
                <va-icon name="my_location" size="small" />
                <span>Mostrando resultados cerca de {{ searchStore.displayCity }}</span>
              </div>
            </div>

            <div class="header-controls">
              <!-- Toggle de vista Grid/Lista -->
              <div class="view-toggle">
                <button
                  class="toggle-btn"
                  :class="{ active: viewMode === 'grid' }"
                  @click="viewMode = 'grid'"
                  title="Vista en cuadrícula"
                >
                  <va-icon name="grid_view" size="small" />
                </button>
                <button
                  class="toggle-btn"
                  :class="{ active: viewMode === 'list' }"
                  @click="viewMode = 'list'"
                  title="Vista en lista"
                >
                  <va-icon name="view_list" size="small" />
                </button>
              </div>

              <!-- Sort select -->
              <select v-model="sortBy" class="sort-select" @change="sortListings">
                <option value="recent">Más Recientes</option>
                <option value="rating">Mejor Calificados</option>
                <option value="featured">Destacados</option>
                <option value="name">Nombre (A-Z)</option>
              </select>
            </div>
          </div>

          <!-- Vista Grid con Cards -->
          <div v-if="viewMode === 'grid'" class="listings-grid">
            <JobCard
              v-for="listing in paginatedListings"
              :key="listing.id"
              :listing="listing"
            />
          </div>

          <!-- Vista Lista -->
          <div v-else class="listings-list">
            <JobListItem
              v-for="listing in paginatedListings"
              :key="`list-${listing.id}`"
              :listing="listing"
            />
          </div>

          <!-- Estado vacío -->
          <div v-if="filteredListings.length === 0" class="empty-state">
            <va-icon name="search_off" size="4rem" color="#CCC" />
            <h3>No se encontraron resultados</h3>
            <p v-if="topFilters.city">
              No hay anuncios en <strong>{{ searchStore.displayCity }}</strong> que coincidan con tu búsqueda
            </p>
            <p v-else>Intenta ajustar los filtros de búsqueda</p>
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
 * GuideView - INTEGRADO CON STORE
 * ═══════════════════════════════════════════════════════════
 */

import { watch } from 'vue'
import MainLayout from '@/components/Layout/MainLayout.vue'
import TopFiltersBar from '@/components/Filters/TopFiltersBar.vue'
import FiltersSidebar from '@/components/Filters/FiltersSidebar.vue'
import JobCard from '@/components/Cards/JobCard.vue'
import JobListItem from '@/components/Cards/JobListItem.vue'
import ListingCard from '@/components/Cards/ListingCard.vue'
import { useSearchStore } from '@/stores/useSearchStore'
import { mockBusinesses } from '@/data/mockBusinesses.js'

export default {
  name: 'GuideView',
  components: {
    MainLayout,
    TopFiltersBar,
    FiltersSidebar,
    JobCard,
    JobListItem,
    ListingCard
  },

  props: {
    category: {
      type: String,
      required: true,
      validator: (value) => ['profesionales', 'gastronomia', 'trabajos', 'negocios', 'servicios'].includes(value)
    }
  },

  setup() {
    const searchStore = useSearchStore()
    return { searchStore }
  },

  data() {
    return {
      showMobileFilters: false,
      viewMode: localStorage.getItem('guideViewMode') || 'grid', // 'grid' o 'list' - persistido en localStorage
      sortBy: 'featured',  // Ordenar por plan por defecto (Impulso > Púrpura > Estándar)
      loading: false,

      // Filtros superiores (ahora sincronizados con el store)
      topFilters: {
        subcategory: '',
        category: '',
        contractType: '',
        city: '',
        search: ''
      },

      // Filtros del sidebar
      sidebarFilters: {
        publishDate: '',
        salaryMin: null,
        salaryMax: null,
        experienceYears: '',
        verifiedOnly: false
      },

      // Paginación
      currentPage: 1,
      itemsPerPage: 9,

      // Datos dinámicos desde BD
      cities: [],
      jobCategories: [],
      contractTypes: [],
      
      categoryConfig: {
        negocios: {
          name: 'Guías de Negocios en Bolivia',
          subcategories: ['Manufactura', 'Textil', 'Alimentos', 'Tecnología', 'Servicios', 'Construcción', 'Comercio', 'Transporte', 'Educación', 'Salud']
        },
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
          subcategories: [] // Se cargan dinámicamente desde BD
        },
        servicios: {
          name: 'Servicios en Bolivia',
          subcategories: ['Plomería', 'Electricidad', 'Limpieza', 'Mudanzas', 'Reparaciones', 'Jardinería']
        }
      },
      
      allListings: []
    }
  },
  
  computed: {
    currentGuide() {
      return {
        name: this.categoryConfig[this.category]?.name || 'Guías',
        subcategories: this.categoryConfig[this.category]?.subcategories || []
      }
    },

    guideName() {
      return this.currentGuide.name
    },

    filteredListings() {
      let results = [...this.allListings]

      // Filtrar por categoría (trabajos)
      if (this.category === 'trabajos' && this.topFilters.category) {
        results = results.filter(listing =>
          listing.jobCategory === this.topFilters.category
        )
      }

      // Filtrar por tipo de contrato (trabajos)
      if (this.category === 'trabajos' && this.topFilters.contractType) {
        results = results.filter(listing =>
          listing.contractType === this.topFilters.contractType
        )
      }

      // Filtrar por subcategoría (otros)
      if (this.category !== 'trabajos' && this.topFilters.subcategory) {
        results = results.filter(listing => {
          if (this.category === 'negocios') {
            return listing.category === this.topFilters.subcategory
          }
          return listing.subcategory === this.topFilters.subcategory ||
                 listing.professionalTitle?.includes(this.topFilters.subcategory)
        })
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
          const name = listing.name?.toLowerCase() || ''
          const description = listing.description?.toLowerCase() || ''
          const professionalTitle = listing.professionalTitle?.toLowerCase() || ''
          const companyName = listing.companyName?.toLowerCase() || ''
          const category = listing.category?.toLowerCase() || ''
          const subcategory = listing.subcategory?.toLowerCase() || ''
          const specialties = listing.specialties?.join(' ').toLowerCase() || ''
          const tags = listing.tags?.join(' ').toLowerCase() || ''

          return title.includes(searchLower) ||
                 name.includes(searchLower) ||
                 description.includes(searchLower) ||
                 professionalTitle.includes(searchLower) ||
                 companyName.includes(searchLower) ||
                 category.includes(searchLower) ||
                 subcategory.includes(searchLower) ||
                 specialties.includes(searchLower) ||
                 tags.includes(searchLower)
        })
      }

      // Filtrar por fecha de publicación
      if (this.sidebarFilters.publishDate) {
        results = results.filter(listing => {
          const daysAgo = listing.publishedDaysAgo || 0

          switch (this.sidebarFilters.publishDate) {
            case '24h':
              return daysAgo <= 1
            case '7d':
              return daysAgo <= 7
            case '30d':
              return daysAgo <= 30
            default:
              return true
          }
        })
      }

      // Filtrar por rango salarial
      if (this.sidebarFilters.salaryMin !== null || this.sidebarFilters.salaryMax !== null) {
        results = results.filter(listing => {
          // Extraer el salario numérico del string (ej: "Bs 5,000 - 8,000")
          if (!listing.salary || listing.salary === 'A convenir') return true

          const salaryMatch = listing.salary.match(/[\d,]+/g)
          if (!salaryMatch) return true

          // Obtener el salario mínimo y máximo del anuncio
          const listingSalaries = salaryMatch.map(s => parseFloat(s.replace(/,/g, '')))
          const listingMin = Math.min(...listingSalaries)
          const listingMax = Math.max(...listingSalaries)

          // Filtrar según los valores ingresados
          let matches = true
          if (this.sidebarFilters.salaryMin !== null) {
            matches = matches && listingMax >= this.sidebarFilters.salaryMin
          }
          if (this.sidebarFilters.salaryMax !== null) {
            matches = matches && listingMin <= this.sidebarFilters.salaryMax
          }

          return matches
        })
      }

      // Filtrar por años de experiencia
      if (this.sidebarFilters.experienceYears) {
        results = results.filter(listing => {
          // Este filtro se puede implementar cuando tengamos el campo en el backend
          // Por ahora lo dejamos como placeholder
          const experience = listing.yearsExperience || listing.experienceYears || 0

          switch (this.sidebarFilters.experienceYears) {
            case '0-1':
              return experience <= 1
            case '1-3':
              return experience > 1 && experience <= 3
            case '3-5':
              return experience > 3 && experience <= 5
            case '5+':
              return experience > 5
            default:
              return true
          }
        })
      }

      // Filtrar por verificados
      if (this.sidebarFilters.verifiedOnly) {
        results = results.filter(listing => listing.verified === true)
      }

      return results
    },

    sortedListings() {
      const listings = [...this.filteredListings]

      switch (this.sortBy) {
        case 'rating':
          return listings.sort((a, b) => (b.rating || 0) - (a.rating || 0))
        case 'featured':
          return listings.sort((a, b) => {
            // Configuración de días de anclaje según plan
            const featuredDaysConfig = {
              impulso: 10,  // Anclado 10 días
              purpura: 6,   // Anclado 6 días
              estandar: 0   // Sin anclaje
            }

            const getPriority = (item) => {
              const plan = item.plan?.toLowerCase()
              const daysAgo = item.publishedDaysAgo || 0
              const featuredDays = featuredDaysConfig[plan] || 0

              // Si el anuncio está dentro del período de anclaje, tiene prioridad alta
              const isAnchored = daysAgo < featuredDays

              if (plan === 'impulso' && isAnchored) return 6  // Impulso anclado - máxima prioridad
              if (plan === 'purpura' && isAnchored) return 5  // Púrpura anclado - segunda prioridad
              if (plan === 'impulso') return 4                // Impulso después de anclaje - con badges
              if (plan === 'purpura') return 3                // Púrpura después de anclaje - con badges
              if (plan === 'estandar') return 2               // Estándar - sin badges
              return 1
            }

            const priorityDiff = getPriority(b) - getPriority(a)

            // Si tienen la misma prioridad, ordenar por fecha (más reciente primero)
            if (priorityDiff === 0) {
              const dateA = new Date(a.createdAt || a.publishDate || '2024-01-01')
              const dateB = new Date(b.createdAt || b.publishDate || '2024-01-01')
              return dateB - dateA
            }

            return priorityDiff
          })
        case 'name':
          return listings.sort((a, b) => {
            const nameA = a.name || a.title || ''
            const nameB = b.name || b.title || ''
            return nameA.localeCompare(nameB)
          })
        case 'recent':
        default:
          return listings.sort((a, b) => {
            const dateA = new Date(a.createdAt || a.publishDate || '2024-01-01')
            const dateB = new Date(b.createdAt || b.publishDate || '2024-01-01')
            return dateB - dateA
          })
      }
    },

    paginatedListings() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.sortedListings.slice(start, end)
    },

    totalPages() {
      return Math.ceil(this.filteredListings.length / this.itemsPerPage)
    }
  },

  methods: {
    /**
     * 🆕 SINCRONIZAR CON STORE AL INICIAR
     */
    syncWithStore() {
      // Leer query params de la URL
      const { ciudad, q } = this.$route.query
      
      // Si hay query params, usarlos
      if (ciudad) {
        this.topFilters.city = this.normalizeCityName(ciudad)
      } 
      // Si no hay query params pero el store tiene ciudad, usarla
      else if (this.searchStore.selectedCity) {
        this.topFilters.city = this.normalizeCityName(this.searchStore.selectedCity)
      }
      
      if (q) {
        this.topFilters.search = q
      } else if (this.searchStore.searchQuery) {
        this.topFilters.search = this.searchStore.searchQuery
      }
    },

    /**
     * Normalizar nombre de ciudad (de slug a nombre completo)
     */
    normalizeCityName(citySlug) {
      const cityMap = {
        'oruro': 'Oruro',
        'la-paz': 'La Paz',
        'cochabamba': 'Cochabamba',
        'santa-cruz': 'Santa Cruz',
        'potosi': 'Potosí',
        'tarija': 'Tarija',
        'chuquisaca': 'Chuquisaca',
        'beni': 'Beni',
        'pando': 'Pando'
      }
      return cityMap[citySlug] || citySlug
    },

    handleFilterChange(filters) {
      // Filtros principales (desde sidebar en móvil)
      if (filters.category !== undefined) {
        this.topFilters.category = filters.category
      }
      if (filters.contractType !== undefined) {
        this.topFilters.contractType = filters.contractType
      }
      if (filters.subcategory !== undefined) {
        this.topFilters.subcategory = filters.subcategory
      }
      if (filters.city !== undefined) {
        this.topFilters.city = filters.city
      }

      // Filtros secundarios del sidebar
      if (filters.publishDate !== undefined) {
        this.sidebarFilters.publishDate = filters.publishDate
      }
      if (filters.salaryMin !== undefined) {
        this.sidebarFilters.salaryMin = filters.salaryMin
      }
      if (filters.salaryMax !== undefined) {
        this.sidebarFilters.salaryMax = filters.salaryMax
      }
      if (filters.experienceYears !== undefined) {
        this.sidebarFilters.experienceYears = filters.experienceYears
      }
      if (filters.verifiedOnly !== undefined) {
        this.sidebarFilters.verifiedOnly = filters.verifiedOnly
      }

      this.currentPage = 1
      // Cerrar sidebar móvil después de aplicar filtros
      this.showMobileFilters = false
    },

    handleTopFilterChange(filters) {
      this.topFilters = { ...this.topFilters, ...filters }
      this.currentPage = 1
    },

    clearAllFilters() {
      this.topFilters = {
        subcategory: '',
        city: '',
        search: ''
      }
      this.sidebarFilters = {
        publishDate: '',
        verifiedOnly: false
      }
      this.searchStore.clearAllFilters()
      this.currentPage = 1

      // ✅ LIMPIAR QUERY PARAMS DE LA URL
      this.$router.replace({
        path: this.$route.path,
        query: {}
      })
    },

    sortListings() {
      this.currentPage = 1
    },

    viewListing(listing) {
      this.$router.push(`/anuncio/${listing.id}`)
    },

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },

    goToPage(page) {
      this.currentPage = page
    },

    /**
     * Cargar trabajos desde la API
     */
    async loadJobsFromAPI() {
      try {
        this.loading = true
        const response = await fetch('/api/jobs/')
        if (!response.ok) throw new Error('Error al cargar trabajos')

        const data = await response.json()
        if (data.success && data.jobs) {
          this.allListings = data.jobs
        }
      } catch (error) {
        console.error('Error cargando trabajos desde API:', error)
        this.allListings = [] // Mostrar lista vacía si hay error
      } finally {
        this.loading = false
      }
    },

    /**
     * Cargar datos dinámicos desde la BD
     */
    async loadDynamicData() {
      try {
        const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

        // Cargar ciudades
        const citiesResponse = await fetch(`${baseURL}/api/jobs/cities`)
        const citiesData = await citiesResponse.json()
        if (citiesData.success && citiesData.cities) {
          this.cities = citiesData.cities.map(c => c.text)
        }

        // Cargar categorías de trabajo (jobCategory)
        const categoriesResponse = await fetch(`${baseURL}/api/jobs/categories-dynamic`)
        const categoriesData = await categoriesResponse.json()
        if (categoriesData.success && categoriesData.categories) {
          this.jobCategories = categoriesData.categories.map(c => c.text)
        }

        // Cargar tipos de contrato (contractType)
        const contractTypesResponse = await fetch(`${baseURL}/api/jobs/contract-types`)
        const contractTypesData = await contractTypesResponse.json()
        if (contractTypesData.success && contractTypesData.contractTypes) {
          this.contractTypes = contractTypesData.contractTypes.map(c => c.text)
        }
      } catch (error) {
        console.error('Error cargando datos dinámicos:', error)
        // Fallback a valores por defecto
        this.cities = ['La Paz', 'Cochabamba', 'Santa Cruz', 'Oruro', 'Potosí', 'Tarija', 'Chuquisaca', 'Beni', 'Pando']
        this.jobCategories = []
        this.contractTypes = []
      }
    },

    loadMockData() {
      if (this.category === 'negocios') {
        this.allListings = [...mockBusinesses]
      } 
      else if (this.category === 'profesionales') {
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
            reviews: 42,
            description: 'Abogado con amplia experiencia en casos civiles y familiares. Especialista en mediación y resolución de conflictos.',
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
            verified: true,
            rating: 4.9,
            reviews: 67,
            description: 'Doctora especializada en pediatría con enfoque en medicina preventiva y desarrollo infantil.',
            images: [{ url: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400' }]
          },
          {
            id: 3,
            slug: 'carlos-rodriguez-contador',
            title: 'Lic. Carlos Rodríguez',
            professionalTitle: 'Contador Público Autorizado',
            subcategory: 'Contadores',
            yearsExperience: 12,
            specialties: ['Contabilidad General', 'Auditoría', 'Tributación'],
            city: 'Santa Cruz',
            plan: 'premium',
            verified: false,
            rating: 4.7,
            reviews: 23,
            description: 'Contador con amplia experiencia en auditorías y asesoramiento tributario para empresas.',
            images: [{ url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400' }]
          }
        ]
      }
      else if (this.category === 'gastronomia') {
        this.allListings = [
          {
            id: 1,
            slug: 'restaurante-el-fogon',
            title: 'Restaurante El Fogón',
            subcategory: 'Comida Tradicional',
            cuisine: 'Boliviana',
            priceRange: 'moderado',
            city: 'Cochabamba',
            plan: 'destacado',
            verified: true,
            rating: 4.8,
            reviews: 67,
            description: 'Auténtica comida tradicional boliviana en ambiente familiar. Especialistas en platos típicos cochabambinos.',
            timeAgo: 'Actualizado hace 1h',
            deliveryAvailable: true,
            schedule: 'Lun-Dom 11:00 - 22:00',
            capacity: 80,
            parking: true,
            images: [{ url: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400' }],
            menuItems: [
              { name: 'Silpancho Tradicional', price: 35, image: 'https://images.unsplash.com/photo-1551782450-17144efb9c50?w=300&h=200&fit=crop' },
              { name: 'Pique Macho', price: 42, image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop' },
              { name: 'Chicharrón de Cerdo', price: 38, image: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=300&h=200&fit=crop' },
              { name: 'Anticucho de Corazón', price: 25, image: 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=300&h=200&fit=crop' }
            ]
          },
          {
            id: 2,
            slug: 'pizzeria-don-luigi',
            title: 'Pizzería Don Luigi',
            subcategory: 'Pizzerías',
            cuisine: 'Italiana',
            priceRange: 'moderado',
            city: 'La Paz',
            plan: 'premium',
            verified: true,
            rating: 4.6,
            reviews: 89,
            description: 'Auténtica pizza italiana con ingredientes importados. Masa artesanal y horno de leña tradicional.',
            timeAgo: 'Actualizado hace 2h',
            deliveryAvailable: true,
            schedule: 'Mar-Dom 18:00 - 23:00',
            capacity: 45,
            parking: false,
            images: [{ url: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400' }],
            menuItems: [
              { name: 'Pizza Margherita', price: 65, image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop' },
              { name: 'Pizza Quattro Stagioni', price: 78, image: 'https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?w=300&h=200&fit=crop' },
              { name: 'Calzone Especial', price: 72, image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300&h=200&fit=crop' }
            ]
          },
          {
            id: 3,
            slug: 'heladeria-sorbeto',
            title: 'Heladería Sorbeto',
            subcategory: 'Heladerías',
            cuisine: 'Postres',
            priceRange: 'economico',
            city: 'Santa Cruz',
            plan: 'premium',
            verified: true,
            rating: 4.9,
            reviews: 156,
            description: 'Helados artesanales con sabores únicos. Productos naturales y recetas familiares tradicionales.',
            timeAgo: 'Actualizado hace 3h',
            deliveryAvailable: false,
            schedule: 'Lun-Sab 14:00 - 22:00',
            capacity: 25,
            parking: true,
            images: [{ url: 'https://images.unsplash.com/photo-1488900128323-21503983a07e?w=400' }],
            menuItems: [
              { name: 'Helado de Coco Tropical', price: 15, image: 'https://images.unsplash.com/photo-1488900128323-21503983a07e?w=300&h=200&fit=crop' },
              { name: 'Sundae de Chocolate', price: 22, image: 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?w=300&h=200&fit=crop' },
              { name: 'Smoothie de Frutas', price: 18, image: 'https://images.unsplash.com/photo-1553530979-cb6735f24a89?w=300&h=200&fit=crop' },
              { name: 'Milkshake Especial', price: 25, image: 'https://images.unsplash.com/photo-1541518763669-27fef04b14ea?w=300&h=200&fit=crop' },
              { name: 'Copa Helada Premium', price: 35, image: 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300&h=200&fit=crop' }
            ]
          }
        ]
      }
      else if (this.category === 'trabajos') {
        // Cargar trabajos desde la API
        this.loadJobsFromAPI()
      } 
      else if (this.category === 'servicios') {
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
          }
        ]
      }
    }
  },

  async mounted() {
    // Cargar datos dinámicos desde BD
    await this.loadDynamicData()
    this.loadMockData()
    // 🆕 Sincronizar con store al montar
    this.syncWithStore()
  },

  watch: {
    category: {
      handler() {
        this.loadMockData()
        this.syncWithStore()
      },
      immediate: false
    },

    // 🆕 Observar cambios en la ruta
    '$route.query': {
      handler() {
        this.syncWithStore()
      },
      deep: true
    },

    // 💾 Guardar preferencia de vista en localStorage
    viewMode: {
      handler(newValue) {
        localStorage.setItem('guideViewMode', newValue)
      }
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
  position: relative;
  z-index: 5;
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

.header-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.header-info h2 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0;
}

/* 🆕 Badge de ubicación detectada */
.location-detected-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(92, 0, 153, 0.1);
  border: 1px solid rgba(92, 0, 153, 0.2);
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-purple);
}

/* Header controls (toggle + sort) */
.header-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Toggle de vista Grid/Lista */
.view-toggle {
  display: flex;
  background: white;
  border: 2px solid var(--color-gray-200);
  border-radius: 8px;
  overflow: hidden;
}

.toggle-btn {
  padding: 0.625rem 0.875rem;
  background: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #6B7280;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-btn:hover {
  background: #F9FAFB;
  color: var(--color-purple);
}

.toggle-btn.active {
  background: var(--color-purple);
  color: white;
}

.toggle-btn:not(:last-child) {
  border-right: 1px solid var(--color-gray-200);
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

/* ✅ GRID UNIFICADO */
.listings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

/* Vista Lista */
.listings-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

.empty-state strong {
  color: var(--color-purple);
  font-weight: 600;
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

  /* Ocultar el FiltersSidebar del flujo del grid en tablet/móvil pero permitir overlay */
  .content-container > .filters-wrapper .filters-sidebar:not(.mobile-open) {
    display: none;
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

  .header-controls {
    width: 100%;
    flex-direction: column;
    gap: 0.75rem;
  }

  .view-toggle {
    width: 100%;
  }

  .toggle-btn {
    flex: 1;
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

  .location-detected-badge {
    font-size: 0.8rem;
    padding: 0.4rem 0.8rem;
  }
}
</style>