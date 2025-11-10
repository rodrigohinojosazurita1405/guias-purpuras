<!-- frontend/src/components/Home/GuidesSection.vue -->
<template>
  <section class="guides-section">
<!-- ========== HERO SECTION ========== -->
    
<div class="compact-hero">
  <div class="container-fluid">
    <div class="compact-hero-content">
      <div class="compact-hero-text">
        <h1 class="compact-hero-title">
          Descubre las <span class="highlight">Mejores Oportunidades</span>
        </h1>
        <p class="compact-hero-subtitle">
          Anuncios <strong>destacados y verificados</strong> en empleos, profesionales, 
          gastronomía y negocios. Tu próximo éxito comienza aquí.
        </p>
      </div>
      <div class="compact-hero-actions">
        <button class="btn-compact-primary" @click="goToPublish">
          <va-icon name="add_circle" size="1.1rem" />
          ¡Anuncia ahora!
        </button>
        <button class="btn-compact-secondary" @click="scrollToContent">
          <va-icon name="explore" size="1.1rem" />
          Explorar
        </button>
      </div>
      <div class="compact-hero-visual">
        <div class="mini-floating-icons">
          <div class="mini-icon" style="animation-delay: 0s;">
            <va-icon name="work" size="1.5rem" color="#5C0099" />
          </div>
          <div class="mini-icon" style="animation-delay: 1s;">
            <va-icon name="business_center" size="1.5rem" color="#5C0099" />
          </div>
          <div class="mini-icon" style="animation-delay: 2s;">
            <va-icon name="restaurant" size="1.5rem" color="#5C0099" />
          </div>
          <div class="mini-icon" style="animation-delay: 3s;">
            <va-icon name="store" size="1.5rem" color="#5C0099" />
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

    <div class="container-fluid">
      <div class="layout-wrapper">
        
        <!-- ========== SIDEBAR IZQUIERDO ========== -->
        <aside class="sidebar-categories">
          <div class="sidebar-header">
            <h3>Categorías</h3>
          </div>

          <!-- Lista de Guías con Categorías -->
          <div class="guides-list">
            <div
              v-for="guide in guides"
              :key="guide.id"
              class="guide-item"
              :class="{ 'active-guide': activeTab === guide.id }"
            >
              <!-- Header de Guía (Click para cambiar tab) -->
              <div 
                class="guide-header"
                @click="changeTab(guide.id)"
              >
                <div class="guide-icon-small">
                  <va-icon :name="guide.icon" size="1.2rem" :color="activeTab === guide.id ? '#FFFFFF' : guide.color" />
                </div>
                <span class="guide-name">{{ guide.shortTitle }}</span>
                <span class="guide-count">({{ guide.stats.total }})</span>
                <va-icon 
                  :name="expandedGuides.includes(guide.id) ? 'expand_less' : 'expand_more'" 
                  size="small"
                  class="expand-icon"
                  @click.stop="toggleGuide(guide.id)"
                />
              </div>

              <!-- Categorías Desplegables (FILTROS) -->
              <transition name="accordion">
                <div v-show="expandedGuides.includes(guide.id)" class="categories-dropdown">
                  <a
                    v-for="category in guide.categories"
                    :key="category.id"
                    href="#"
                    :class="['category-link', { 'active-category': activeCategory === category.id }]"
                    @click.prevent="filterByCategory(guide.id, category.id)"
                  >
                    <va-icon :name="category.icon" size="14px" />
                    <span>{{ category.name }}</span>
                    <span class="cat-count">({{ category.count }})</span>
                  </a>
                </div>
              </transition>
            </div>
          </div>

          <!-- CTA Publicar -->
          <div class="sidebar-cta">
            <button class="btn-publish" @click="goToPublish">
              <va-icon name="add_circle" size="small" />
              Publicar Anuncio
            </button>
          </div>
        </aside>

        <!-- ========== ÁREA PRINCIPAL CON TABS ========== -->
        <main class="main-content">
          
          <!-- ========== TABS NAVEGACIÓN ========== -->
          <div class="tabs-navigation">
            <button
              v-for="guide in guides"
              :key="guide.id"
              :class="['tab-btn', { active: activeTab === guide.id }]"
              @click="changeTab(guide.id)"
            >
              <va-icon :name="guide.icon" size="1.2rem" />
              <span>{{ guide.shortTitle }}</span>
              <span class="tab-count">{{ getFilteredCount(guide.id) }}</span>
            </button>
          </div>

          <!-- Header con título y filtros rápidos -->
          <div class="content-header">
            <div class="header-left">
              <h2 class="content-title">{{ currentGuideTitle }}</h2>
              <p class="content-subtitle">
                Se han encontrado <strong>{{ filteredListings.length }}</strong> ofertas en Bolivia
              </p>
            </div>
            
            <!-- Ordenamiento -->
            <select v-model="sortBy" class="sort-select">
              <option value="featured">Destacados primero</option>
              <option value="recent">Más recientes</option>
              <option value="rating">Mejor valorados</option>
            </select>
          </div>

          <!-- Filtro activo (chips) -->
          <div class="active-filters" v-if="activeCategory">
            <div class="filter-chip">
              <span>{{ activeCategoryName }}</span>
              <va-icon name="close" size="small" @click="clearCategoryFilter" />
            </div>
          </div>

          <!-- ========== MINI CARDS (Lista de Anuncios) ========== -->
          <div class="listings-container">
            <div
              v-for="listing in paginatedListings"
              :key="listing.id"
              class="listing-mini-card"
              @click="goToListing(listing)"
            >
              <!-- Imagen/Logo -->
              <div class="listing-image">
                <img :src="getListingImage(listing)" :alt="getListingTitle(listing)" />
              </div>

              <!-- Contenido -->
              <div class="listing-content">
                <h4 class="listing-title">{{ getListingTitle(listing) }}</h4>
                
                <div class="listing-info">
                  <span class="info-item">
                    <va-icon name="business" size="14px" />
                    {{ getListingCompany(listing) }}
                  </span>
                  <span class="info-item">
                    <va-icon name="location_on" size="14px" />
                    {{ listing.city }}
                  </span>
                </div>

                <div class="listing-meta">
                  <span class="listing-date">
                    <va-icon name="schedule" size="12px" />
                    {{ getListingDate(listing) }}
                  </span>
                  
                  <!-- Rating (si existe) -->
                  <span class="listing-rating" v-if="listing.rating">
                    <va-icon name="star" size="12px" color="var(--color-yellow-primary)" />
                    {{ listing.rating }} ({{ listing.reviews }})
                  </span>
                </div>
              </div>

              <!-- Badge Destacado -->
              <div class="listing-badge" v-if="isHighlighted(listing)">
                <span :class="['badge-highlight', getBadgeClass(listing)]">
                  {{ getBadgeText(listing) }}
                </span>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredListings.length === 0" class="empty-state">
              <va-icon name="inbox" size="4rem" color="#ccc" />
              <p>No se encontraron anuncios en esta categoría</p>
              <button class="btn-clear" @click="clearCategoryFilter">
                Limpiar filtros
              </button>
            </div>
          </div>

          <!-- ✅ PAGINACIÓN MODERNA Y CENTRADA -->
          <div class="pagination-wrapper" v-if="filteredListings.length > 0">
            <div class="pagination">
              <button 
                class="btn-page btn-prev" 
                :disabled="currentPage === 1" 
                @click="previousPage"
              >
                <va-icon name="chevron_left" size="1.2rem" />
              </button>
              
              <!-- Números de página -->
              <div class="page-numbers">
                <!-- Primera página -->
                <button
                  v-if="currentPage > 3"
                  class="page-number"
                  @click="goToPage(1)"
                >
                  1
                </button>
                
                <!-- Dots izquierda -->
                <span v-if="currentPage > 4" class="page-dots">•••</span>
                
                <!-- Páginas visibles -->
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  :class="['page-number', { active: page === currentPage }]"
                  @click="goToPage(page)"
                >
                  {{ page }}
                </button>
                
                <!-- Dots derecha -->
                <span v-if="currentPage < totalPages - 3" class="page-dots">•••</span>
                
                <!-- Última página -->
                <button
                  v-if="currentPage < totalPages - 2"
                  class="page-number"
                  @click="goToPage(totalPages)"
                >
                  {{ totalPages }}
                </button>
              </div>
              
              <button 
                class="btn-page btn-next" 
                :disabled="currentPage === totalPages" 
                @click="nextPage"
              >
                <va-icon name="chevron_right" size="1.2rem" />
              </button>
            </div>

            <!-- Info de resultados -->
            <div class="results-info">
              Mostrando {{ startIndex + 1 }} - {{ endIndex }} de {{ filteredListings.length }} anuncios
            </div>
          </div>
        </main>

      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'

// ==========================================
// COMPOSABLES
// ==========================================
const router = useRouter()

// ==========================================
// STATE
// ==========================================
const activeTab = ref('trabajos') // Tab activo por defecto
const expandedGuides = ref([]) // 
const activeCategory = ref(null) // Categoría seleccionada para filtrar
const sortBy = ref('featured') // Ordenamiento
const currentPage = ref(1)
const itemsPerPage = 20 // ✅ 20 anuncios por página

// ==========================================
// MÉTODOS HERO
// ==========================================
const scrollToContent = () => {
  const content = document.querySelector('.layout-wrapper')
  if (content) {
    content.scrollIntoView({ behavior: 'smooth' })
  }
}

// ==========================================
// DATA - GUÍAS CON CATEGORÍAS
// ==========================================
const guides = [
  {
    id: 'trabajos',
    shortTitle: 'Trabajos',
    fullTitle: 'Trabajo en Bolivia',
    icon: 'work',
    color: '#5C0099',
    stats: { total: 268 },
    categories: [
      { id: 'comercial', name: 'Comercial y Ventas', icon: 'storefront', count: 58, slug: 'comercial-ventas' },
      { id: 'finanzas', name: 'Contabilidad y Finanzas', icon: 'account_balance', count: 57, slug: 'contabilidad-finanzas' },
      { id: 'ingenieria', name: 'Ingenierías', icon: 'engineering', count: 29, slug: 'ingenierias' },
      { id: 'atencion', name: 'Atención al Cliente', icon: 'support_agent', count: 24, slug: 'atencion-cliente' },
      { id: 'marketing', name: 'Marketing y Publicidad', icon: 'campaign', count: 16, slug: 'marketing' },
      { id: 'logistica', name: 'Logística y Almacén', icon: 'local_shipping', count: 15, slug: 'logistica' },
      { id: 'salud', name: 'Salud y Farmacia', icon: 'local_hospital', count: 14, slug: 'salud' },
      { id: 'rrhh', name: 'Recursos Humanos', icon: 'groups', count: 11, slug: 'recursos-humanos' }
    ]
  },
  {
    id: 'gastronomia',
    shortTitle: 'Gastronomía',
    fullTitle: 'Gastronomía en Bolivia',
    icon: 'restaurant',
    color: '#5C0099',
    stats: { total: 2189 },
    categories: [
      { id: 'tradicional', name: 'Comida Tradicional', icon: 'restaurant_menu', count: 456, slug: 'tradicional' },
      { id: 'pizzerias', name: 'Pizzerías', icon: 'local_pizza', count: 234, slug: 'pizzerias' },
      { id: 'cafeterias', name: 'Cafeterías', icon: 'local_cafe', count: 189, slug: 'cafeterias' },
      { id: 'heladerias', name: 'Heladerías', icon: 'icecream', count: 123, slug: 'heladerias' }
    ]
  },
  {
    id: 'profesionales',
    shortTitle: 'Profesionales',
    fullTitle: 'Profesionales en Bolivia',
    icon: 'business_center',
    color: '#5C0099',
    stats: { total: 3245 },
    categories: [
      { id: 'abogados', name: 'Abogados', icon: 'gavel', count: 245, slug: 'abogados' },
      { id: 'doctores', name: 'Doctores', icon: 'medical_services', count: 189, slug: 'doctores' },
      { id: 'contadores', name: 'Contadores', icon: 'calculate', count: 156, slug: 'contadores' },
      { id: 'arquitectos', name: 'Arquitectos', icon: 'architecture', count: 98, slug: 'arquitectos' },
      { id: 'ingenieros', name: 'Ingenieros', icon: 'engineering', count: 234, slug: 'ingenieros' }
    ]
  },
  
  {
    id: 'negocios',
    shortTitle: 'Negocios',
    fullTitle: 'Guías de Negocios en Bolivia',
    icon: 'store',
    color: '#5C0099',
    stats: { total: 2510 },
    categories: [
      { id: 'manufactura', name: 'Manufactura', icon: 'factory', count: 245, slug: 'manufactura' },
      { id: 'textil', name: 'Textil', icon: 'checkroom', count: 189, slug: 'textil' },
      { id: 'alimentos', name: 'Alimentos', icon: 'lunch_dining', count: 234, slug: 'alimentos' },
      { id: 'tecnologia', name: 'Tecnología', icon: 'computer', count: 156, slug: 'tecnologia' },
      { id: 'servicios', name: 'Servicios', icon: 'build', count: 334, slug: 'servicios' },
      { id: 'construccion', name: 'Construcción', icon: 'construction', count: 198, slug: 'construccion' },
      { id: 'comercio', name: 'Comercio', icon: 'shopping_cart', count: 267, slug: 'comercio' },
      { id: 'transporte', name: 'Transporte', icon: 'local_shipping', count: 145, slug: 'transporte' }
    ]
  }
]

// ==========================================
// MOCK DATA - ANUNCIOS POR GUÍA
// ==========================================
const allListingsData = {
  trabajos: [
    {
      id: 1, guideId: 'trabajos', categoryId: 'ingenieria',
      title: 'ASESORÍA EN DISEÑO GRÁFICO', company: 'Escuela de negocios ESAM',
      city: 'Santa Cruz', date: '07/Noviembre/2025',
      image: 'https://placehold.co/100x100/5C0099/white?text=ESAM',
      plan: 'destacado', featured: true
    },
    {
      id: 2, guideId: 'trabajos', categoryId: 'ingenieria',
      title: 'TÉCNICO ELÉCTRICO AUTOMOTRIZ JUNIOR', company: 'IMSE LTDA',
      city: 'Santa Cruz', date: '07/Noviembre/2025',
      image: 'https://placehold.co/100x100/3D0066/white?text=IMSE',
      plan: 'top', featured: true
    },
    {
      id: 3, guideId: 'trabajos', categoryId: 'finanzas',
      title: 'LIQUIDADOR', company: 'NACIONAL SEGUROS',
      city: 'Cochabamba', date: '07/Noviembre/2025',
      image: 'https://placehold.co/100x100/510087/white?text=NS',
      plan: 'destacado', featured: true
    },
    {
      id: 4, guideId: 'trabajos', categoryId: 'comercial',
      title: 'ANALISTA DE MARCA', company: 'Nova Moda S.R.L',
      city: 'Cochabamba', date: '07/Noviembre/2025',
      image: 'https://placehold.co/100x100/3D0066/white?text=NM',
      plan: 'premium', featured: false
    },
    {
      id: 5, guideId: 'trabajos', categoryId: 'salud',
      title: 'ODONTÓLOGO', company: 'ODONTO CERPAX S.R.L.',
      city: 'Cochabamba', date: '06/Noviembre/2025',
      image: 'https://placehold.co/100x100/5C0099/white?text=OC',
      plan: 'basico', featured: false
    }
  ],
  profesionales: [
    {
      id: 10, 
      guideId: 'profesionales', 
      categoryId: 'abogados',
      slug: 'juan-perez-abogado',
      title: 'Dr. Juan Pérez - Abogado Especialista', 
      company: 'Estudio Jurídico Mendoza',
      city: 'Cochabamba', 
      date: 'Hace 2 horas',
      plan: 'top', 
      featured: true, 
      rating: 4.8, 
      reviews: 42,
      // ✅ Array de imágenes (como en ProfessionalDetailView)
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1556157382-97eda2d62296?w=300&h=300&fit=crop', order: 1 },
        { id: 2, url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop', order: 2 }
      ]
    },
    {
      id: 11, 
      guideId: 'profesionales', 
      categoryId: 'doctores',
      slug: 'maria-gomez-doctora',
      title: 'Dra. María Gómez - Pediatra', 
      company: 'Clínica San Rafael',
      city: 'La Paz', 
      date: 'Hace 5 horas',
      plan: 'destacado', 
      featured: true, 
      rating: 4.9, 
      reviews: 67,
      // ✅ Array de imágenes
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop', order: 1 },
        { id: 2, url: 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=300&h=300&fit=crop', order: 2 }
      ]
    },
    {
      id: 12, 
      guideId: 'profesionales', 
      categoryId: 'contadores',
      slug: 'carlos-rodriguez-contador',
      title: 'Lic. Carlos Rodríguez - Contador', 
      company: 'Contadores Asociados',
      city: 'Santa Cruz', 
      date: 'Hace 1 día',
      plan: 'premium', 
      featured: false, 
      rating: 4.7, 
      reviews: 23,
      // ✅ Array de imágenes
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop', order: 1 }
      ]
    }
  ],
  gastronomia: [
    {
      id: 20, 
      guideId: 'gastronomia', 
      categoryId: 'tradicional',
      slug: 'restaurante-el-fogon',
      title: 'Restaurante El Fogón', 
      company: 'Grupo Gastronómico',
      city: 'La Paz', 
      date: 'Hace 1 hora',
      plan: 'top', 
      featured: true, 
      rating: 4.8, 
      reviews: 67,
      // ✅ Imagen del restaurante
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=300&h=300&fit=crop', order: 1 },
        { id: 2, url: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=300&h=300&fit=crop', order: 2 }
      ]
    },
    {
      id: 21, 
      guideId: 'gastronomia', 
      categoryId: 'pizzerias',
      slug: 'pizzeria-don-luigi',
      title: 'Pizzería Don Luigi', 
      company: 'Don Luigi SRL',
      city: 'Cochabamba', 
      date: 'Hace 3 horas',
      plan: 'destacado', 
      featured: true, 
      rating: 4.6, 
      reviews: 89,
      // ✅ Imagen de pizza
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=300&fit=crop', order: 1 }
      ]
    },
    {
      id: 22, 
      guideId: 'gastronomia', 
      categoryId: 'heladerias',
      slug: 'heladeria-sorbeto',
      title: 'Heladería Sorbeto', 
      company: 'Sorbeto Natural',
      city: 'Santa Cruz', 
      date: 'Hace 6 horas',
      plan: 'premium', 
      featured: false, 
      rating: 4.9, 
      reviews: 156,
      // ✅ Imagen de helado
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1488900128323-21503983a07e?w=300&h=300&fit=crop', order: 1 }
      ]
    }
  ],
  negocios: [
    {
      id: 30, 
      guideId: 'negocios', 
      categoryId: 'manufactura',
      slug: 'fabrica-textil-la-paz',
      title: 'Fábrica Textil La Paz', 
      company: 'Textiles Andinos SRL',
      city: 'La Paz', 
      date: 'Hace 2 horas',
      plan: 'top', 
      featured: true, 
      rating: 4.9, 
      reviews: 67,
      // ✅ Logo/Imagen de la fábrica
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=300&h=300&fit=crop', order: 1 }
      ]
    },
    {
      id: 31, 
      guideId: 'negocios', 
      categoryId: 'alimentos',
      slug: 'distribuidora-alimentos-santa-cruz',
      title: 'Distribuidora de Alimentos Santa Cruz', 
      company: 'Alimentos del Valle',
      city: 'Santa Cruz', 
      date: 'Hace 4 horas',
      plan: 'destacado', 
      featured: true, 
      rating: 4.7, 
      reviews: 45,
      // ✅ Imagen de productos
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=300&h=300&fit=crop', order: 1 }
      ]
    },
    {
      id: 32, 
      guideId: 'negocios', 
      categoryId: 'tecnologia',
      slug: 'techbolivia-soluciones-it',
      title: 'TechBolivia - Soluciones IT', 
      company: 'Tech Bolivia SRL',
      city: 'Cochabamba', 
      date: 'Hace 1 día',
      plan: 'premium', 
      featured: false, 
      rating: 4.8, 
      reviews: 89,
      // ✅ Logo tech
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=300&h=300&fit=crop', order: 1 }
      ]
    },
    {
      id: 33, 
      guideId: 'negocios', 
      categoryId: 'servicios',
      slug: 'plomeria-emergencias-24-7',
      title: 'Plomería 24/7 Emergencias', 
      company: 'Servicios Rápidos',
      city: 'La Paz', 
      date: 'Hace 3 horas',
      plan: 'destacado', 
      featured: true, 
      rating: 5.0, 
      reviews: 34,
      // ✅ Imagen de herramientas/servicio
      images: [
        { id: 1, url: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=300&h=300&fit=crop', order: 1 }
      ]
    }
  ]
}

// ==========================================
// COMPUTED
// ==========================================
const currentGuideTitle = computed(() => {
  const guide = guides.find(g => g.id === activeTab.value)
  return guide ? guide.fullTitle : 'Guías en Bolivia'
})

const activeCategoryName = computed(() => {
  if (!activeCategory.value) return ''
  const guide = guides.find(g => g.id === activeTab.value)
  const cat = guide?.categories.find(c => c.id === activeCategory.value)
  return cat ? cat.name : ''
})

const filteredListings = computed(() => {
  let listings = allListingsData[activeTab.value] || []
  
  // Filtrar por categoría si está activa
  if (activeCategory.value) {
    listings = listings.filter(l => l.categoryId === activeCategory.value)
  }
  
  return listings
})

const sortedListings = computed(() => {
  const listings = [...filteredListings.value]
  
  switch (sortBy.value) {
    case 'featured':
      return listings.sort((a, b) => {
        const getPriority = (item) => {
          if (item.plan === 'top') return 3
          if (item.plan === 'destacado') return 2
          if (item.plan === 'premium') return 1
          return 0
        }
        return getPriority(b) - getPriority(a)
      })
    case 'recent':
      return listings.sort((a, b) => {
        const dateA = new Date(a.date)
        const dateB = new Date(b.date)
        return dateB - dateA
      })
    case 'rating':
      return listings.sort((a, b) => (b.rating || 0) - (a.rating || 0))
    default:
      return listings
  }
})

const paginatedListings = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return sortedListings.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredListings.value.length / itemsPerPage)
})

// ✅ NUEVO: Páginas visibles en paginación (mostrar max 5)
const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// ✅ NUEVO: Índices para mostrar info
const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage
})

const endIndex = computed(() => {
  return Math.min(startIndex.value + itemsPerPage, filteredListings.value.length)
})

// ==========================================
// MÉTODOS
// ==========================================
// Estado inicial - vacío o solo la primera
const toggleGuide = (guideId) => {
  const index = expandedGuides.value.indexOf(guideId)
  if (index > -1) {
    // Si ya está expandida, la contraemos
    expandedGuides.value.splice(index, 1)
  } else {
    // ✅ COMPORTAMIENTO ACORDEÓN: Expandir solo esta, contraer demás
    expandedGuides.value = [guideId] // Reemplazar array completo
  }
}

const changeTab = (guideId) => {
  activeTab.value = guideId
  activeCategory.value = null
  currentPage.value = 1
  // ✅ NO modificar expandedGuides - sidebar independiente
}

const filterByCategory = (guideId, categoryId) => {
  // Cambiar a la guía correspondiente si no está activa
  if (activeTab.value !== guideId) {
    activeTab.value = guideId
  }
  
  // Toggle categoría
  if (activeCategory.value === categoryId) {
    activeCategory.value = null
  } else {
    activeCategory.value = categoryId
  }
  
  currentPage.value = 1
}

const clearCategoryFilter = () => {
  activeCategory.value = null
  currentPage.value = 1
}

const getFilteredCount = (guideId) => {
  const listings = allListingsData[guideId] || []
  return listings.length
}

const goToListing = (listing) => {
  // Navegar según el tipo de guía
  const routeMap = {
    trabajos: { name: 'JobDetail', params: { id: listing.id } },
    profesionales: { name: 'ProfessionalDetail', params: { slug: listing.slug || listing.id } },
    gastronomia: { name: 'RestaurantDetail', params: { slug: listing.slug || listing.id } },
    negocios: { name: 'BusinessDetail', params: { slug: listing.slug || listing.id } }
  }
  
  const route = routeMap[activeTab.value]
  if (route) {
    router.push(route)
  } else {
    console.warn('Ruta no definida para:', activeTab.value)
  }
}

const goToPublish = () => {
  router.push({ name: 'Publish' })
}

const previousPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

// ✅ MÉTODO NUEVO: Ir a página específica
const goToPage = (page) => {
  currentPage.value = page
}

// Helpers para renderizado
const getListingImage = (listing) => {
  // Si tiene array de imágenes (como en ProfessionalDetailView), usar la primera
  if (listing.images && listing.images.length > 0) {
    return listing.images[0].url
  }
  // Si tiene imagen directa
  if (listing.image) {
    return listing.image
  }
  // Fallback con iniciales según tipo
  const initials = getInitials(listing)
  return `https://placehold.co/300x300/5C0099/white?text=${encodeURIComponent(initials)}`
}

const getInitials = (listing) => {
  if (listing.title) {
    const words = listing.title.split(' ')
    if (words.length >= 2) {
      return words[0][0] + words[1][0]
    }
    return words[0].substring(0, 2).toUpperCase()
  }
  return 'GP' // Guías Púrpuras
}
const getListingTitle = (listing) => listing.title
const getListingCompany = (listing) => listing.company || 'Empresa Confidencial'
const getListingDate = (listing) => listing.date

const isHighlighted = (listing) => {
  return listing.featured || listing.plan === 'top' || listing.plan === 'destacado'
}

const getBadgeClass = (listing) => {
  if (listing.plan === 'top') return 'badge-top'
  if (listing.plan === 'destacado') return 'badge-destacado'
  return ''
}

const getBadgeText = (listing) => {
  if (listing.plan === 'top') return 'TOP'
  if (listing.plan === 'destacado') return 'Oferta destacada'
  return 'Destacado'
}

// ==========================================
// WATCHERS
// ==========================================
watch(activeTab, () => {
  currentPage.value = 1
})
</script>

<style scoped>
/* ==========================================
   COMPACT HERO - SEMI HERO HEADER
   ========================================== */
.compact-hero {
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  padding: 2rem 0;
  color: white;
  position: relative;
  overflow: hidden;
}

.compact-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" opacity="0.05"><polygon fill="white" points="0,1000 1000,0 1000,1000"/></svg>');
  background-size: cover;
}

.compact-hero-content {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 2rem;
  align-items: center;
  position: relative;
  z-index: 2;
}

.compact-hero-text {
  max-width: 500px;
}

.compact-hero-title {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 0.5rem 0;
  color: white;
}

.compact-hero-title .highlight {
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, var(--color-yellow-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.compact-hero-subtitle {
  font-size: 1rem;
  line-height: 1.4;
  margin: 0;
  opacity: 0.9;
  font-weight: 400;
}

.compact-hero-subtitle strong {
  color: var(--color-yellow-primary);
  font-weight: 600;
}

.compact-hero-actions {
  display: flex;
  gap: 0.75rem;
  flex-shrink: 0;
}

/* ==========================================
   BOTONES MEJORADOS - TEXTO MÁS GRANDE
   ========================================== */
.btn-compact-primary {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, var(--color-yellow-light) 100%);
  color: var(--color-purple-darkest);
  border: none;
  border-radius: 8px;
  font-weight: 800;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3);
  white-space: nowrap;
  letter-spacing: 0.5px;
}

.btn-compact-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(253, 197, 0, 0.4);
}

.btn-compact-secondary {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  white-space: nowrap;
  letter-spacing: 0.5px;
}

.btn-compact-secondary:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.compact-hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.mini-floating-icons {
  display: flex;
  gap: 0.75rem;
}

.mini-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  animation: mini-float 4s ease-in-out infinite;
}

.mini-icon:hover {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

@keyframes mini-float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-5px) rotate(2deg); }
}

/* ==========================================
   LAYOUT PRINCIPAL
   ========================================== */
.guides-section {
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
  min-height: 100vh;
}

.container-fluid {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.layout-wrapper {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
  align-items: start;
  padding: 2rem 0;
}

/* ==========================================
   SIDEBAR - SIMPLIFICADO
   ========================================== */
.sidebar-categories {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(92, 0, 153, 0.12);
  position: sticky;
  top: 20px;
}

.sidebar-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 3px solid var(--color-purple);
  background: #FAFAFA;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
}

/* ==========================================
   GUÍAS LIST - SIMPLIFICADO
   ========================================== */
.guides-list {
  padding: 0.5rem 0;
}

.guide-item {
  border-bottom: 1px solid #F0F0F0;
  position: relative;
  transition: background-color 0.3s ease;
}

.guide-item.active-guide {
  background: rgba(92, 0, 153, 0.05);
}

.guide-item.active-guide .guide-header {
  background: var(--color-purple);
  color: white;
}

.guide-item.active-guide .guide-name,
.guide-item.active-guide .guide-count,
.guide-item.active-guide .expand-icon {
  color: white !important;
}

.guide-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1.25rem;
  cursor: pointer;
  transition: all 0.25s ease;
}

.guide-header:hover {
  background: #F8F9FA;
}

.guide-item.active-guide .guide-header:hover {
  background: var(--color-purple-dark);
}

.guide-icon-small {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F0E6F6;
  border-radius: 8px;
  flex-shrink: 0;
  transition: background-color 0.3s ease;
}

.guide-item.active-guide .guide-icon-small {
  background: rgba(255, 255, 255, 0.2);
}

.guide-name {
  flex: 1;
  font-weight: 600;
  font-size: 0.95rem;
  color: #333;
}

.guide-count {
  font-size: 0.85rem;
  color: #666;
}

.expand-icon {
  color: #999;
  transition: transform 0.3s ease;
}

.guide-item.active-guide .expand-icon {
  transform: rotate(180deg);
}

/* ==========================================
   CATEGORÍAS DROPDOWN - CON EFECTOS ACORDEÓN
   ========================================== */
.categories-dropdown {
  background: #FAFAFA;
  padding: 0.5rem 0;
  overflow: hidden;
}

/* ==========================================
   TRANSICIONES ACORDEÓN - PARA <transition name="accordion">
   ========================================== */
.accordion-enter-active {
  transition: all 0.4s ease-out;
  max-height: 500px;
}

.accordion-leave-active {
  transition: all 0.3s ease-in;
  max-height: 500px;
}

.accordion-enter-from {
  opacity: 0;
  max-height: 0;
  transform: translateY(-10px);
}

.accordion-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-10px);
}

.accordion-enter-to {
  opacity: 1;
  max-height: 500px;
  transform: translateY(0);
}

.accordion-leave-from {
  opacity: 1;
  max-height: 500px;
  transform: translateY(0);
}

.category-link {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.65rem 1.25rem 0.65rem 3.5rem;
  text-decoration: none;
  color: #555;
  font-size: 0.9rem;
  transition: all 0.25s ease;
  transform-origin: left;
}

.category-link:hover {
  background: #F0E6F6;
  color: var(--color-purple);
  transform: translateX(4px);
}

.category-link.active-category {
  background: #F0E6F6;
  color: var(--color-purple-darkest);
  font-weight: 600;
  border-left: 4px solid var(--color-purple);
  transform: translateX(4px);
}

.cat-count {
  margin-left: auto;
  font-size: 0.8rem;
  color: #999;
}

/* ==========================================
   SIDEBAR CTA - 30% AMARILLO
   ========================================== */
.sidebar-cta {
  padding: 1rem 1.25rem 1.25rem;
  border-top: 1px solid #F0F0F0;
}

.btn-publish {
  width: 100%;
  padding: 0.95rem;
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, var(--color-yellow-light) 100%);
  color: var(--color-purple-darkest);
  border: none;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3);
}

.btn-publish:hover {
  background: linear-gradient(135deg, var(--color-yellow-light) 0%, var(--color-yellow-primary) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(253, 197, 0, 0.4);
}

/* ==========================================
   ÁREA PRINCIPAL
   ========================================== */
.main-content {
  background: white;
  border-radius: 8px;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  min-height: 600px;
}

/* ==========================================
   TABS NAVEGACIÓN
   ========================================== */
.tabs-navigation {
  display: flex;
  background: white;
  border-bottom: 3px solid #E0E0E0;
  border-radius: 8px 8px 0 0;
  overflow-x: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--color-purple) #F0F0F0;
}

.tabs-navigation::-webkit-scrollbar {
  height: 4px;
}

.tabs-navigation::-webkit-scrollbar-track {
  background: #F0F0F0;
}

.tabs-navigation::-webkit-scrollbar-thumb {
  background: var(--color-purple);
  border-radius: 4px;
}

.tab-btn {
  flex: 1;
  min-width: 150px;
  padding: 1.25rem 1rem;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  margin-bottom: -3px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  color: #666;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  background: rgba(92, 0, 153, 0.05);
  color: var(--color-purple);
}

.tab-btn.active {
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  color: white;
  border-bottom-color: var(--color-yellow-primary);
}

.tab-count {
  background: rgba(0, 0, 0, 0.1);
  padding: 0.25rem 0.65rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 700;
  transition: all 0.2s ease;
}

.tab-btn.active .tab-count {
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

/* ==========================================
   CONTENT HEADER
   ========================================== */
.content-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 2rem;
  gap: 2rem;
  border-bottom: 1px solid #F0F0F0;
}

.header-left {
  flex: 1;
}

.content-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.content-subtitle {
  font-size: 0.95rem;
  color: #666;
  margin: 0;
}

.content-subtitle strong {
  color: var(--color-purple);
  font-weight: 700;
}

.sort-select {
  padding: 0.75rem 1rem;
  background: white;
  border: 2px solid var(--color-gray-medium);
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sort-select:hover {
  border-color: var(--color-purple);
}

.sort-select:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

/* ==========================================
   FILTROS ACTIVOS (CHIPS)
   ========================================== */
.active-filters {
  padding: 1rem 2rem;
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  border-bottom: 1px solid #F0F0F0;
}

.filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  color: white;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-chip:hover {
  background: linear-gradient(135deg, var(--color-purple-dark) 0%, var(--color-purple-darkest) 100%);
  transform: scale(1.05);
}

.filter-chip va-icon {
  cursor: pointer;
}

/* ==========================================
   MINI CARDS (Anuncios)
   ========================================== */
.listings-container {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.listing-mini-card {
  display: grid;
  grid-template-columns: 100px 1fr auto;
  gap: 1.25rem;
  padding: 1.25rem;
  border: 2px solid #F0F0F0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
  background: white;
}

.listing-mini-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, var(--color-purple) 70%, var(--color-yellow-primary) 30%);
  opacity: 0;
  transition: opacity 0.25s ease;
  border-radius: 12px 0 0 12px;
}

.listing-mini-card:hover {
  border-color: var(--color-purple);
  box-shadow: 0 6px 20px rgba(92, 0, 153, 0.15);
  transform: translateX(4px);
}

.listing-mini-card:hover::before {
  opacity: 1;
}

.listing-mini-card:hover .listing-title {
  color: var(--color-purple-dark);
}

.listing-mini-card:hover .listing-image {
  transform: scale(1.05);
}

.listing-image {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.25s ease;
  position: relative;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.15);
}

.listing-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.25s ease;
}

.listing-mini-card:hover .listing-image img {
  transform: scale(1.08);
}

.listing-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  justify-content: center;
}

.listing-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-purple);
  margin: 0;
  line-height: 1.4;
  transition: color 0.2s ease;
  position: relative;
}

.listing-mini-card:hover .listing-title {
  color: var(--color-purple-dark);
}

.listing-info {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.listing-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.25rem;
}

.listing-date {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  color: #999;
}

.listing-rating {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  color: #666;
  font-weight: 600;
}

.listing-badge {
  display: flex;
  align-items: flex-start;
  padding-top: 0.25rem;
}

.badge-highlight {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.badge-top {
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, var(--color-yellow-light) 100%);
  color: var(--color-purple-darkest);
}

.badge-destacado {
  background: linear-gradient(135deg, #6C757D 0%, #495057 100%);
  color: white;
}

/* ==========================================
   EMPTY STATE
   ========================================== */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #999;
}

.empty-state p {
  margin: 1rem 0 2rem 0;
  font-size: 1.1rem;
  color: #666;
}

.btn-clear {
  padding: 0.75rem 2rem;
  background: var(--color-purple);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-clear:hover {
  background: var(--color-purple-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

/* ==========================================
   PAGINACIÓN MODERNA
   ========================================== */
.pagination-wrapper {
  padding: 2rem;
  border-top: 1px solid #F0F0F0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-page {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 2px solid var(--color-gray-medium);
  border-radius: 8px;
  font-weight: 600;
  color: var(--color-purple);
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-page:hover:not(:disabled) {
  background: var(--color-purple);
  color: white;
  border-color: var(--color-purple);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.2);
}

.btn-page:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

.page-numbers {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-number {
  min-width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 2px solid var(--color-gray-medium);
  border-radius: 8px;
  font-weight: 600;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.page-number:hover {
  border-color: var(--color-purple);
  color: var(--color-purple);
  transform: translateY(-2px);
}

.page-number.active {
  background: var(--color-purple);
  border-color: var(--color-purple);
  color: white;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

.page-dots {
  padding: 0 0.5rem;
  color: #999;
  font-weight: 600;
  font-size: 0.9rem;
}

.results-info {
  padding: 0.75rem 1.5rem;
  background: #F8F9FA;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1024px) {
  .compact-hero-content {
    grid-template-columns: 1fr auto;
    gap: 1.5rem;
  }
  
  .compact-hero-visual {
    display: none;
  }

  .layout-wrapper {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .sidebar-categories {
    position: static;
    max-width: 100%;
  }

  .tabs-navigation {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .tab-btn {
    min-width: 130px;
    padding: 1.25rem 0.85rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 768px) {
  .compact-hero {
    padding: 1.5rem 0;
  }
  
  .compact-hero-content {
    grid-template-columns: 1fr;
    gap: 1rem;
    text-align: center;
  }
  
  .compact-hero-title {
    font-size: 1.75rem;
  }
  
  .compact-hero-subtitle {
    font-size: 0.95rem;
  }
  
  .compact-hero-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .btn-compact-primary,
  .btn-compact-secondary {
    padding: 0.9rem 1.75rem;
    font-size: 1.1rem;
    font-weight: 700;
  }

  .guides-section {
    padding: 1.5rem 0;
  }

  .main-content {
    border-radius: 8px;
  }

  .content-header {
    flex-direction: column;
    padding: 1.5rem;
    gap: 1rem;
  }

  .header-left {
    width: 100%;
  }

  .sort-select {
    width: 100%;
  }

  .listings-container {
    padding: 1.5rem;
  }

  .listing-mini-card {
    grid-template-columns: 90px 1fr;
    gap: 1rem;
    padding: 1rem;
  }

  .listing-image {
    width: 90px;
    height: 90px;
  }

  .listing-badge {
    grid-column: 1 / -1;
    padding-top: 0;
    margin-top: 0.75rem;
    justify-content: flex-start;
  }

  .tab-btn {
    padding: 1rem 0.75rem;
    min-width: 110px;
    font-size: 0.85rem;
    gap: 0.5rem;
  }

  .tab-count {
    font-size: 0.75rem;
    padding: 0.25rem 0.6rem;
  }

  .listing-title {
    font-size: 0.95rem;
  }

  .info-item {
    font-size: 0.85rem;
  }

  .listing-meta {
    flex-direction: column;
    gap: 0.35rem;
  }

  .pagination-wrapper {
    padding: 2rem 1rem;
  }

  .pagination {
    padding: 0.75rem 1rem;
    gap: 0.5rem;
  }

  .btn-page {
    width: 40px;
    height: 40px;
  }

  .page-number {
    min-width: 40px;
    height: 40px;
    font-size: 0.9rem;
  }

  .page-dots {
    font-size: 0.85rem;
  }

  .results-info {
    font-size: 0.85rem;
    padding: 0.65rem 1.25rem;
  }
}

@media (max-width: 480px) {
  .compact-hero-title {
    font-size: 1.5rem;
  }
  
  .compact-hero-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn-compact-primary,
  .btn-compact-secondary {
    width: 100%;
    max-width: 250px;
    justify-content: center;
    padding: 0.85rem 1.5rem;
    font-size: 1.1rem;
    font-weight: 700;
  }

  .content-title {
    font-size: 1.35rem;
  }

  .content-subtitle {
    font-size: 0.9rem;
  }

  .listing-mini-card {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .listing-image {
    width: 100%;
    height: 150px;
    margin: 0 auto;
  }

  .listing-content {
    align-items: center;
  }

  .listing-info {
    align-items: center;
  }

  .tabs-navigation {
    flex-wrap: nowrap;
    justify-content: flex-start;
  }

  .tab-btn {
    flex: 0 0 auto;
    min-width: 100px;
  }

  .pagination {
    flex-wrap: wrap;
    padding: 0.65rem;
    border-radius: 30px;
  }

  .btn-page {
    width: 36px;
    height: 36px;
  }

  .page-number {
    min-width: 36px;
    height: 36px;
    font-size: 0.85rem;
  }

  .page-numbers {
    padding: 0 0.25rem;
    gap: 0.35rem;
  }

  .results-info {
    font-size: 0.8rem;
    padding: 0.5rem 1rem;
  }
}

@media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
  .layout-wrapper {
    grid-template-columns: 240px 1fr;
  }

  .sidebar-categories {
    position: sticky;
  }
}
</style>