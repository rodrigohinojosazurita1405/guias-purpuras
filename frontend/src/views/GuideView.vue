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

    <!-- ========== BARRA DE BÚSQUEDA Y FILTROS SUPERIOR (STICKY) ========== -->
    <TopSearchBar
      :category="category"
      :categories="jobCategories"
      :contract-types="contractTypes"
      :cities="cities"
      :results-count="filteredListings.length"
      :location-info="{
        detected: searchStore.userDetectedCity,
        method: searchStore.locationMethod,
        displayCity: searchStore.displayCity
      }"
      @filter-change="handleTopFilterChange"
      @search-click="scrollToResults"
    />

    <!-- ========== Contenido Principal ========== -->
    <section class="guide-content">
      <div class="content-container full-width">

        <!-- SPLIT VIEW: Lista Compacta + Panel de Detalles -->
        <div class="split-view" :class="{ 'has-selection': selectedJob }" v-if="category === 'trabajos'">
          <!-- Columna Izquierda: Lista Compacta -->
          <div class="jobs-list-column">
            <!-- Estado vacío -->
            <div v-if="filteredListings.length === 0" class="empty-state-compact">
              <va-icon name="search_off" size="3rem" color="#CCC" />
              <h3>No se encontraron resultados</h3>
              <p>Intenta ajustar los filtros de búsqueda</p>
            </div>

            <!-- Lista de trabajos compactos -->
            <JobListCompact
              v-for="listing in paginatedListings"
              :key="listing.id"
              :listing="listing"
              :is-selected="selectedJob && selectedJob.id === listing.id"
              @select="selectJob"
            />

            <!-- Indicador de carga para scroll infinito -->
            <div v-if="isLoadingMore" class="loading-more">
              <div class="spinner"></div>
              <span>Cargando más resultados...</span>
            </div>

            <!-- Mensaje de fin de resultados -->
            <div v-else-if="!hasMoreItems && filteredListings.length > 0" class="no-more-results">
              <va-icon name="check_circle" size="small" />
              <span>Has visto todos los resultados</span>
            </div>
          </div>

          <!-- Columna Derecha: Panel de Detalles -->
          <div class="detail-column" :class="{ 'has-selection': selectedJob || jobNotAvailable }">
            <!-- Overlay oscuro para móvil -->
            <div
              v-if="selectedJob || jobNotAvailable"
              class="modal-overlay"
              @click="closeJobDetail"
            ></div>

            <!-- Mensaje de oferta no disponible -->
            <div v-if="jobNotAvailable" class="job-not-available">
              <!-- Mensaje cuando la oferta está expirada (con información detallada) -->
              <template v-if="expiredJobInfo">
                <va-icon name="schedule" size="large" color="#f97316" />
                <h2 class="expired-title">Período de Postulación Finalizado</h2>

                <div class="expired-job-details">
                  <h3>{{ expiredJobInfo.title }}</h3>
                  <p v-if="expiredJobInfo.company" class="company-name">
                    <va-icon name="business" size="small" />
                    {{ expiredJobInfo.company }}
                  </p>
                </div>

                <div class="expired-message">
                  <va-icon name="info" size="small" color="#7c3aed" />
                  <p>{{ jobNotAvailableMessage }}</p>
                </div>

                <p class="help-text">
                  Esta oferta ya no acepta nuevas postulaciones.
                  Te invitamos a explorar otras oportunidades disponibles.
                </p>

                <va-button
                  @click="$router.push('/guias/trabajos')"
                  gradient
                  icon="arrow_forward"
                  icon-right
                >
                  Explorar Ofertas Activas
                </va-button>
              </template>

              <!-- Mensaje genérico para otros errores (404, 403, etc.) -->
              <template v-else>
                <va-icon name="error_outline" size="large" color="#ef4444" />
                <h2>Oferta No Encontrada</h2>
                <p>{{ jobNotAvailableMessage }}</p>
                <va-button @click="$router.push('/guias/trabajos')">
                  Ver Otras Ofertas
                </va-button>
              </template>
            </div>

            <!-- Panel solo visible si hay trabajo seleccionado -->
            <JobDetailPanel
              v-if="selectedJob && !jobNotAvailable"
              :listing="selectedJob"
              @close="closeJobDetail"
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

import MainLayout from '@/components/Layout/MainLayout.vue'
import TopSearchBar from '@/components/Filters/TopSearchBar.vue'
import JobListCompact from '@/views/Detail/JobListCompact.vue'
import JobDetailPanel from '@/views/Detail/JobDetailPanel.vue'
import ListingCard from '@/components/Cards/ListingCard.vue'
import { useSearchStore } from '@/stores/useSearchStore'
import { mockBusinesses } from '@/data/mockBusinesses.js'
import axios from 'axios'

export default {
  name: 'GuideView',
  components: {
    MainLayout,
    TopSearchBar,
    JobListCompact,
    JobDetailPanel,
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

      // Scroll infinito
      displayedItems: 20, // Número inicial de items a mostrar
      itemsPerLoad: 15, // Items a cargar cada vez
      isLoadingMore: false,

      // Split View - Trabajo seleccionado
      selectedJob: null,
      jobNotAvailable: false, // Flag para mostrar mensaje de oferta no disponible
      jobNotAvailableMessage: '', // Mensaje personalizado
      expiredJobInfo: null, // Información de oferta expirada

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

      // 🎯 Si hay parámetro 'selected', mostrar SOLO ese trabajo
      const selectedId = this.$route.query.selected
      if (selectedId) {
        // Comparar como string porque los IDs pueden ser UUIDs alfanuméricos
        const selectedJob = results.find(job => String(job.id) === String(selectedId))
        if (selectedJob) {
          return [selectedJob]
        } else {
          console.warn('⚠️ [filteredListings] Trabajo NO encontrado con ID:', selectedId, '- Mostrando todos')
          return results
        }
      }

      // Filtrar por categoría (trabajos)
      if (this.category === 'trabajos' && this.topFilters.category) {
        results = results.filter(listing => {
          // Normalizar para comparación (remover acentos y comparar en minúsculas)
          const normalizeText = (text) => {
            if (!text) return ''
            return text
              .toLowerCase()
              .normalize('NFD')
              .replace(/[\u0300-\u036f]/g, '')
              .trim()
          }

          const listingCategory = normalizeText(listing.jobCategory)
          const filterCategory = normalizeText(this.topFilters.category)
          const match = listingCategory === filterCategory

          return match
        })
      }

      // Filtrar por tipo de contrato (trabajos)
      if (this.category === 'trabajos' && this.topFilters.contractType) {

        results = results.filter(listing => {
          // Normalizar para comparación (remover acentos, plurales y comparar en minúsculas)
          const normalizeContractType = (text) => {
            if (!text) return ''
            let normalized = text
              .toLowerCase()
              .normalize('NFD')
              .replace(/[\u0300-\u036f]/g, '') // Remover acentos
              .trim()

            // Normalizar variaciones comunes
            // "Pasantías" -> "pasantia"
            if (normalized.endsWith('ias')) {
              normalized = normalized.replace(/ias$/, 'ia')
            }
            // "Pasantes" -> "pasante"
            if (normalized.endsWith('es') && !normalized.endsWith('tes')) {
              normalized = normalized.slice(0, -1)
            }

            return normalized
          }

          const listingContractType = normalizeContractType(listing.contractType)
          const filterContractType = normalizeContractType(this.topFilters.contractType)
          const match = listingContractType === filterContractType

          return match
        })
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

      // Filtrar por ciudad (normalizar comparación)
      if (this.topFilters.city) {
        const filterCity = this.normalizeCityName(this.topFilters.city)
        results = results.filter(listing => {
          const listingCity = this.normalizeCityName(listing.city)
          return listingCity === filterCity
        })
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
          // Si el salario es "A convenir", incluirlo siempre
          if (!listing.salary || listing.salary === 'A convenir') return true

          // Intentar obtener el salario desde los campos directos del backend
          let listingMin = listing.salaryMin
          let listingMax = listing.salaryMax

          // Si no existen, extraer del string formateado
          if (!listingMin || !listingMax) {
            const salaryMatch = listing.salary.match(/[\d,]+/g)
            if (!salaryMatch) return true

            const listingSalaries = salaryMatch.map(s => parseFloat(s.replace(/,/g, '')))
            listingMin = Math.min(...listingSalaries)
            listingMax = Math.max(...listingSalaries)
          }

          // Lógica de filtrado mejorada:
          // Mostrar el anuncio si hay CUALQUIER superposición entre los rangos
          let matches = true

          // Si el usuario especifica salario mínimo:
          // Mostrar anuncios cuyo salario máximo sea >= al mínimo buscado
          if (this.sidebarFilters.salaryMin !== null) {
            matches = matches && listingMax >= this.sidebarFilters.salaryMin
          }

          // Si el usuario especifica salario máximo:
          // Mostrar anuncios cuyo salario mínimo sea <= al máximo buscado
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

      // Filtrar por modalidad (remoto, híbrido, presencial)
      if (this.topFilters.modality) {
        results = results.filter(listing =>
          listing.modality === this.topFilters.modality
        )
      }

      // Filtrar por educación
      if (this.sidebarFilters.education) {
        results = results.filter(listing => {
          const educationLevel = listing.education || listing.educationRequired || ''
          return educationLevel.toLowerCase().includes(this.sidebarFilters.education.toLowerCase())
        })
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
      // Usar scroll infinito: mostrar solo los primeros displayedItems
      return this.sortedListings.slice(0, this.displayedItems)
    },

    hasMoreItems() {
      // Verificar si hay más items para cargar
      return this.displayedItems < this.sortedListings.length
    }
  },

  methods: {
    /**
     * 🆕 SINCRONIZAR CON STORE AL INICIAR
     */
    async syncWithStore() {
      // Leer query params de la URL
      const { ciudad, q, category, contractType } = this.$route.query

      // 🔥 Si hay parámetro 'selected', NO aplicar filtros del store
      // Esto permite mostrar todos los trabajos cuando se viene desde "Empleos destacados"
      const hasSelectedParam = this.$route.query.selected

      // Si hay query params, usarlos
      if (ciudad) {
        this.topFilters.city = this.normalizeCityName(ciudad)
      }
      // Si no hay query params y NO hay selected param, usar el store
      else if (this.searchStore.selectedCity && !hasSelectedParam) {
        this.topFilters.city = this.normalizeCityName(this.searchStore.selectedCity)
      }

      if (q) {
        this.topFilters.search = q
      } else if (this.searchStore.searchQuery && !hasSelectedParam) {
        this.topFilters.search = this.searchStore.searchQuery
      }

      // 🆕 Si hay categoría en query params, usarla
      if (category) {
        const denormalizedCategory = await this.denormalizeCategory(category)
        this.topFilters.category = denormalizedCategory
      }

      // 🆕 Si hay tipo de contrato en query params, usarlo
      if (contractType) {
        this.topFilters.contractType = contractType
      } else if (this.searchStore.selectedContractType && !hasSelectedParam) {
        this.topFilters.contractType = this.searchStore.selectedContractType
      }
    },

    /**
     * Convertir slug de categoría a nombre completo
     */
    async denormalizeCategory(categorySlug) {
      // El slug viene en formato como "tecnologia-e-informatica"
      // Necesitamos convertirlo al nombre real que usa el backend
      try {
        const response = await axios.get('http://localhost:8000/api/jobs/categories-dynamic/')
        if (response.data && response.data.categories) {
          const category = response.data.categories.find(cat => cat.slug === categorySlug)
          if (category) {
            return category.text // Retornar el nombre completo: "Tecnología e Informática"
          }
        }
      } catch (error) {
        console.error('Error al obtener categorías:', error)
      }
      // Si no encuentra, devolver el slug convertido a título (respetando palabras cortas como "y", "e", "de")
      const smallWords = ['y', 'e', 'de', 'del', 'la', 'el', 'los', 'las', 'a', 'al']
      const result = categorySlug.split('-').map((word, index) => {
        // Primera palabra siempre con mayúscula
        if (index === 0) {
          return word.charAt(0).toUpperCase() + word.slice(1)
        }
        // Palabras cortas en minúscula (excepto la primera)
        if (smallWords.includes(word.toLowerCase())) {
          return word.toLowerCase()
        }
        // Resto con mayúscula inicial
        return word.charAt(0).toUpperCase() + word.slice(1)
      }).join(' ')

      return result
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
      // Actualizar filtros principales
      this.topFilters = {
        search: filters.search || '',
        city: filters.city || '',
        category: filters.category || '',
        contractType: filters.contractType || '',
        subcategory: filters.subcategory || '',
        modality: filters.modality || ''
      }

      // Actualizar filtros del sidebar (salario, fecha, educación)
      this.sidebarFilters = {
        publishDate: filters.publishDate || '',
        salaryMin: filters.salaryMin || null,
        salaryMax: filters.salaryMax || null,
        experienceYears: filters.experienceYears || '',
        verifiedOnly: filters.verifiedOnly || false,
        education: filters.education || ''
      }

      // Resetear scroll infinito
      this.resetDisplayedItems()
    },

    scrollToResults() {
      // Scroll suave hasta la sección de resultados
      const resultsSection = document.querySelector('.results-header')
      if (resultsSection) {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    },

    selectJob(job) {
      // Seleccionar trabajo para mostrar en el panel de detalles
      this.selectedJob = job
      this.jobNotAvailable = false // Reset flag
      this.jobNotAvailableMessage = '' // Reset mensaje
      this.expiredJobInfo = null // Reset info de expirado

      // En móvil, prevenir scroll del body
      if (window.innerWidth < 1024) {
        document.body.style.overflow = 'hidden'
      }
    },

    async checkJobAvailability(jobId) {
      // Verificar si un trabajo existe pero no está disponible (expirado/cerrado)
      try {
        const response = await fetch(`${this.baseURL}/api/jobs/${jobId}/`)
        const data = await response.json()

        if (response.status === 410) {
          // 410 Gone - Oferta expirada/cerrada
          this.jobNotAvailable = true
          this.expiredJobInfo = {
            title: data.jobTitle || 'Oferta laboral',
            company: data.companyName || '',
            expiryDate: data.expiryDate,
            reason: data.reason
          }
          this.jobNotAvailableMessage = data.message || 'Esta oferta ya no está disponible.'
        } else if (!response.ok) {
          // Otro error (404, 403, etc.)
          this.jobNotAvailable = true
          this.expiredJobInfo = null
          this.jobNotAvailableMessage = data.message || 'Esta oferta no fue encontrada.'
        }
      } catch (error) {
        console.error('Error verificando disponibilidad del trabajo:', error)
        this.jobNotAvailable = true
        this.expiredJobInfo = null
        this.jobNotAvailableMessage = 'No se pudo verificar la disponibilidad de esta oferta.'
      }
    },

    closeJobDetail() {
      // Cerrar el panel de detalles en móvil
      if (window.innerWidth < 1024) {
        this.selectedJob = null
        this.jobNotAvailable = false
        this.jobNotAvailableMessage = ''
        document.body.style.overflow = ''
      }
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

    loadMoreItems() {
      if (this.isLoadingMore || !this.hasMoreItems) return

      this.isLoadingMore = true

      // Simular delay de carga (puedes quitar esto si quieres)
      setTimeout(() => {
        this.displayedItems += this.itemsPerLoad
        this.isLoadingMore = false
      }, 300)
    },

    handleScroll() {
      // Detectar cuando el usuario está cerca del final de la página
      const scrollPosition = window.innerHeight + window.scrollY
      const bottomPosition = document.documentElement.scrollHeight - 500 // 500px antes del final

      if (scrollPosition >= bottomPosition && this.hasMoreItems && !this.isLoadingMore) {
        this.loadMoreItems()
      }
    },

    resetDisplayedItems() {
      // Resetear al cambiar filtros
      this.displayedItems = this.itemsPerLoad
    },

    /**
     * Normalizar nombre de ciudad para comparación
     */
    normalizeCityName(cityName) {
      if (!cityName) return ''

      const citySlugMap = {
        'cochabamba': 'cochabamba',
        'la paz': 'la-paz',
        'la-paz': 'la-paz',
        'santa cruz': 'santa-cruz',
        'santa-cruz': 'santa-cruz',
        'oruro': 'oruro',
        'potosí': 'potosi',
        'potosi': 'potosi',
        'tarija': 'tarija',
        'chuquisaca': 'chuquisaca',
        'chuquisaca (sucre)': 'chuquisaca',
        'sucre': 'chuquisaca',
        'beni': 'beni',
        'pando': 'pando'
      }

      const normalized = cityName
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '') // Quitar acentos
        .trim()

      return citySlugMap[normalized] || normalized
    },

    /**
     * Cargar trabajos desde la API
     */
    async loadJobsFromAPI() {
      try {
        this.loading = true
        const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
        const response = await fetch(`${baseURL}/api/jobs/`)

        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${response.statusText}`)
        }

        const data = await response.json()

        if (data.success && data.jobs) {
          this.allListings = data.jobs
        } else {
          console.warn('[GuideView] No se encontraron trabajos en la respuesta')
          this.allListings = []
        }
      } catch (error) {
        console.error('[GuideView] Error cargando trabajos desde API:', error)
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

    async loadMockData() {
      if (this.category === 'trabajos') {
        // Cargar trabajos desde la API
        await this.loadJobsFromAPI()
      }
      else if (this.category === 'negocios') {
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
    // 🔥 IMPORTANTE: Esperar a que los trabajos se carguen
    await this.loadMockData()
    // 🆕 Sincronizar con store al montar
    this.syncWithStore()

    // Verificar si hay un trabajo preseleccionado en la URL (query param 'selected')
    const selectedId = this.$route.query.selected
    if (selectedId) {
      // Buscar el trabajo en la lista y seleccionarlo (comparar como string porque IDs pueden ser UUIDs)
      const job = this.allListings.find(listing => String(listing.id) === String(selectedId))
      if (job) {
        this.selectJob(job)
      } else {
        console.warn('[GuideView] No se encontró el trabajo con ID:', selectedId)
        // Si no está en el listado, verificar si existe pero está expirado
        await this.checkJobAvailability(selectedId)
      }
    }

    // Agregar listener de scroll para scroll infinito
    window.addEventListener('scroll', this.handleScroll)
  },

  beforeUnmount() {
    // Limpiar listener de scroll
    window.removeEventListener('scroll', this.handleScroll)
  },

  watch: {
    category: {
      handler() {
        this.loadMockData()
        this.syncWithStore()
        // Limpiar selección al cambiar de categoría
        this.selectedJob = null
      },
      immediate: false
    },

    // Actualizar selección cuando cambien los filtros
    filteredListings: {
      handler(newListings) {
        if (this.category === 'trabajos' && newListings.length > 0) {
          // Si el trabajo seleccionado ya no está en la lista, limpiar selección
          const stillExists = newListings.some(job => job.id === this.selectedJob?.id)
          if (!stillExists) {
            this.selectedJob = null
          }
        } else if (newListings.length === 0) {
          this.selectedJob = null
        }
      }
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
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.content-container.full-width {
  display: block; /* Sin grid, full width */
}

/* ========== SPLIT VIEW ========== */
.split-view {
  display: grid;
  gap: 1.5rem;
  min-height: 600px;
  transition: grid-template-columns 0.3s ease;
}

/* Sin selección: Lista ocupa casi todo el ancho */
.split-view:not(.has-selection) {
  grid-template-columns: 1fr 0;
}

/* Con selección: Vista dividida normal */
.split-view.has-selection {
  grid-template-columns: 40% 60%;
}

/* Columna Izquierda - Lista Compacta */
.jobs-list-column {
  display: flex;
  flex-direction: column;
  padding-right: 0.5rem;
  max-width: 100%;
}

/* Columna Derecha - Panel de Detalles */
.detail-column {
  position: sticky;
  top: 1rem;
  align-self: flex-start;
  overflow: hidden;
  transition: opacity 0.3s ease;
  max-height: calc(100vh - 2rem);
}

/* Ocultar panel cuando no hay selección */
.split-view:not(.has-selection) .detail-column {
  opacity: 0;
  pointer-events: none;
  width: 0;
}

/* Mostrar panel cuando hay selección */
.split-view.has-selection .detail-column {
  opacity: 1;
  pointer-events: auto;
}

/* Overlay oscuro para modal móvil */
.modal-overlay {
  display: none;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (max-width: 1024px) {
  .modal-overlay {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    z-index: 999;
    animation: fadeIn 0.3s ease-out;
  }
}

/* Estado Vacío Compacto */
.empty-state-compact {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
  text-align: center;
  background: white;
  border-radius: 12px;
  border: 2px dashed #E5E7EB;
}

.empty-state-compact h3 {
  font-size: 1.125rem;
  color: #6B7280;
  margin: 1rem 0 0.5rem 0;
}

.empty-state-compact p {
  color: #9CA3AF;
  font-size: 0.9rem;
}

/* Indicador de Carga - Scroll Infinito */
.loading-more {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1rem;
}

.loading-more span {
  font-size: 0.9rem;
  color: #6B7280;
  font-weight: 500;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #E5E7EB;
  border-top-color: #7C3AED;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Mensaje de fin de resultados */
.no-more-results {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1.5rem;
  margin-top: 1rem;
  background: #F9FAFB;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #059669;
  font-weight: 500;
}

/* Placeholder - Selecciona un trabajo */
.select-job-placeholder {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 4rem 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  position: sticky;
  top: 180px;
}

.select-job-placeholder h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #374151;
  margin: 1rem 0 0.5rem 0;
}

.select-job-placeholder p {
  color: #6B7280;
  font-size: 0.95rem;
  max-width: 300px;
  line-height: 1.5;
}

/* Ocultar placeholder en móvil */
@media (max-width: 1024px) {
  .select-job-placeholder {
    display: none;
  }

  /* Split view se convierte en lista completa en móvil */
  .split-view {
    display: block;
  }

  .jobs-list-column {
    width: 100%;
    padding-right: 0;
  }

  .detail-column {
    display: none; /* Ocultar por defecto en móvil */
  }

  /* Cuando hay trabajo seleccionado, mostrar como modal */
  .detail-column.has-selection {
    display: flex !important;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    align-items: center;
    justify-content: center;
  }
}

/* ========== Vista Grid (Fallback) ========== */
.listings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
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

/* ========== MENSAJE DE OFERTA NO DISPONIBLE ========== */
.job-not-available {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin: 2rem;
  min-height: 450px;
  border: 1px solid #f0f0f0;
}

.job-not-available .va-icon {
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

/* Título específico para ofertas expiradas */
.job-not-available .expired-title {
  font-size: 1.85rem;
  font-weight: 700;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 1.5rem 0;
}

/* Detalles de la oferta expirada */
.expired-job-details {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid #f97316;
  margin-bottom: 1.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.1);
}

.expired-job-details h3 {
  font-size: 1.35rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.75rem 0;
  line-height: 1.4;
}

.expired-job-details .company-name {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #666;
  font-size: 1rem;
  font-weight: 500;
  margin: 0;
}

/* Mensaje de expiración */
.expired-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  background: #f3f4f6;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  margin-bottom: 1.25rem;
  max-width: 500px;
  width: 100%;
}

.expired-message p {
  margin: 0;
  color: #374151;
  font-size: 1rem;
  font-weight: 500;
}

/* Texto de ayuda */
.help-text {
  color: #6b7280;
  font-size: 0.95rem;
  margin: 0 0 2rem 0;
  max-width: 450px;
  line-height: 1.6;
}

/* Título genérico para otros errores */
.job-not-available h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 1rem 0;
}

.job-not-available p {
  font-size: 1.125rem;
  color: #666;
  margin: 0 0 2rem 0;
  max-width: 500px;
}

.job-not-available .va-button {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  transition: transform 0.2s;
}

.job-not-available .va-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}
</style>