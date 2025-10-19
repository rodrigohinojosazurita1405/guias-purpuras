<template>
  <!-- 
    HeroSection.vue - Sección principal con búsqueda
    
    Propósito: Hero con título, búsqueda avanzada y estadísticas
    Conecta con: HomeView.vue (componente padre)
    Emite: search (cuando el usuario busca)
    Datos: Guías principales, ciudades, estadísticas
  -->
  <section class="hero-section">
    <div class="hero-background"></div>
    <div class="hero-overlay">
      <div class="hero-content">
        <!-- Título Principal -->
        <h1 class="hero-title animate-fade-in">
          Encuentra Todo lo que Buscas en Bolivia
        </h1>
        <p class="hero-subtitle animate-fade-in-delay">
          Profesionales, Restaurantes, Trabajos y Servicios en tu ciudad
        </p>

        <!-- Búsqueda Avanzada -->
        <div class="search-container animate-slide-up">
          <!-- Tabs de Guías -->
          <div class="search-tabs">
            <button 
              v-for="guide in guides" 
              :key="guide.id"
              :class="['search-tab', { active: activeGuide === guide.slug }]"
              @click="activeGuide = guide.slug"
            >
              <VaIcon :name="guide.icon" size="small" />
              <span>{{ guide.name }}</span>
            </button>
          </div>

          <!-- Formulario de Búsqueda -->
          <div class="search-form">
            <div class="search-field search-main">
              <VaIcon name="search" size="large" color="var(--color-purple-dark)" />
              <input 
                type="text" 
                :placeholder="getSearchPlaceholder()"
                v-model="searchQuery"
                @keyup.enter="handleSearch"
              />
            </div>

            <div class="search-field search-location">
              <VaIcon name="location_on" size="large" color="var(--color-orange-primary)" />
              <select v-model="selectedCity">
                <option value="">Todas las Ciudades</option>
                <option v-for="city in cities" :key="city" :value="city">
                  {{ city }}
                </option>
              </select>
            </div>

            <VaButton class="search-button" size="large" @click="handleSearch">
              <VaIcon name="search" />
              Buscar
            </VaButton>
          </div>

          <!-- Filtros Rápidos -->
          <div class="quick-filters">
            <span class="filter-label">Búsquedas populares:</span>
            <button 
              v-for="filter in quickFilters" 
              :key="filter"
              class="quick-filter-btn"
              @click="quickSearch(filter)"
            >
              {{ filter }}
            </button>
          </div>
        </div>

        <!-- Estadísticas -->
        <div class="stats-row">
          <div class="stat-item">
            <VaIcon name="article" size="large" />
            <div class="stat-content">
              <h3>{{ stats.listings.toLocaleString() }}+</h3>
              <p>Anuncios Activos</p>
            </div>
          </div>
          <div class="stat-item">
            <VaIcon name="people" size="large" />
            <div class="stat-content">
              <h3>{{ stats.users.toLocaleString() }}+</h3>
              <p>Usuarios</p>
            </div>
          </div>
          <div class="stat-item">
            <VaIcon name="verified" size="large" />
            <div class="stat-content">
              <h3>{{ stats.verified.toLocaleString() }}+</h3>
              <p>Verificados</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
/**
 * HeroSection Component
 * 
 * Props: Ninguno (datos locales por ahora)
 * 
 * Emits:
 * - search: { query, city, guide } cuando el usuario busca
 * 
 * State:
 * - activeGuide: guía seleccionada en los tabs
 * - searchQuery: texto de búsqueda
 * - selectedCity: ciudad seleccionada
 * 
 * TODO: 
 * - Conectar con API Django /api/search/
 * - Obtener estadísticas desde /api/stats/
 */

export default {
  name: 'HeroSection',
  emits: ['search'],
  data() {
    return {
      activeGuide: 'profesionales',
      searchQuery: '',
      selectedCity: '',
      
      // Guías principales (mock)
      // TODO: Obtener desde Django API /api/guides/
      guides: [
        { id: 1, slug: 'profesionales', name: 'Profesionales', icon: 'business_center' },
        { id: 2, slug: 'gastronomicas', name: 'Gastronomía', icon: 'restaurant' },
        { id: 3, slug: 'trabajos', name: 'Trabajos', icon: 'work' },
        { id: 4, slug: 'servicios', name: 'Servicios', icon: 'build' }
      ],
      
      // Ciudades de Bolivia
      cities: [
        'La Paz', 'Cochabamba', 'Santa Cruz', 'Sucre',
        'Oruro', 'Potosí', 'Tarija', 'Beni', 'Pando'
      ],
      
      // Filtros rápidos
      quickFilters: ['Abogados', 'Restaurantes', 'Desarrollador', 'Plomero'],
      
      // Estadísticas (mock)
      // TODO: Obtener desde Django API /api/stats/
      stats: {
        listings: 12456,
        users: 45678,
        verified: 3421
      }
    }
  },
  methods: {
    getSearchPlaceholder() {
      const placeholders = {
        profesionales: '¿Qué profesional buscas? (ej: Abogado, Contador...)',
        gastronomicas: '¿Qué tipo de comida buscas? (ej: Pizzería, Sushi...)',
        trabajos: '¿Qué trabajo buscas? (ej: Desarrollador, Vendedor...)',
        servicios: '¿Qué servicio necesitas? (ej: Plomero, Electricista...)'
      }
      return placeholders[this.activeGuide] || '¿Qué estás buscando?'
    },
    
    handleSearch() {
      // Emitir evento de búsqueda al componente padre
      this.$emit('search', {
        query: this.searchQuery,
        city: this.selectedCity,
        guide: this.activeGuide
      })
      
      console.log('Búsqueda:', {
        query: this.searchQuery,
        city: this.selectedCity,
        guide: this.activeGuide
      })
      
      // TODO: Redirigir a /guia/:slug con parámetros de búsqueda
    },
    
    quickSearch(filter) {
      this.searchQuery = filter
      this.handleSearch()
    }
  }
}
</script>

<style scoped>
/**
 * Estilos del Hero Section
 * Full width, imagen de fondo, overlay púrpura
 */

.hero-section {
  background: url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920') center/cover;
  min-height: 700px;
  display: flex;
  align-items: center;
  overflow: hidden;
  position: relative;
  width: 100%;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.hero-overlay {
  position: relative;
  z-index: 1;
  width: 100%;
  background: linear-gradient(135deg, rgba(26, 11, 61, 0.95) 0%, rgba(107, 70, 193, 0.90) 100%);
  padding: 5rem 0;
}

.hero-content {
  max-width: 100%;
  padding: 0 3rem;
  margin: 0 auto;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  color: #ffffff;
  text-align: center;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.95);
  text-align: center;
  margin-bottom: 3rem;
  font-weight: 300;
}

/* Search Container */
.search-container {
  max-width: 1200px;
  margin: 0 auto 3rem;
}

.search-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.search-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.search-tab:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
}

.search-tab.active {
  background: #ffffff;
  color: var(--color-purple-dark);
  border-color: #ffffff;
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.3);
}

.search-form {
  display: grid;
  grid-template-columns: 2fr 1.2fr auto;
  gap: 1rem;
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.search-field {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: var(--color-gray-50);
  border-radius: 12px;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.search-field:focus-within {
  background: #ffffff;
  border-color: var(--color-purple-dark);
  box-shadow: 0 0 0 4px rgba(107, 70, 193, 0.1);
}

.search-field input,
.search-field select {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 1rem;
  outline: none;
  color: var(--color-gray-900);
  font-weight: 500;
}

.search-field input::placeholder {
  color: var(--color-gray-400);
}

.search-field select {
  cursor: pointer;
}

.search-button {
  background: linear-gradient(135deg, var(--color-orange-primary) 0%, var(--color-orange-light) 100%) !important;
  padding: 1rem 2.5rem !important;
  font-size: 1.1rem !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 20px rgba(255, 140, 0, 0.4);
  white-space: nowrap;
}

.search-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(255, 140, 0, 0.5);
}

/* Quick Filters */
.quick-filters {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.filter-label {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.quick-filter-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.quick-filter-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}

/* Stats Row */
.stats-row {
  display: flex;
  justify-content: center;
  gap: 4rem;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #ffffff;
}

.stat-item .va-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
  line-height: 1;
}

.stat-content p {
  font-size: 0.9rem;
  opacity: 0.9;
  margin: 0.25rem 0 0 0;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .search-tabs {
    flex-direction: column;
  }

  .search-tab {
    width: 100%;
    justify-content: center;
  }

  .search-form {
    grid-template-columns: 1fr;
  }

  .stats-row {
    gap: 2rem;
  }

  .stat-item {
    flex-direction: column;
    text-align: center;
  }

  .hero-content {
    padding: 0 1.5rem;
  }
}
</style>