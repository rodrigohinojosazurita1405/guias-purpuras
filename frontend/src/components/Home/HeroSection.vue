<!-- frontend/src/components/Home/HeroSection.vue -->
<template>
  <section class="hero-section">
    <div class="hero-content">
      <!-- Título Principal -->
      <h1 class="hero-title">
        Encuentra Todo lo que Buscas en
        <span class="highlight">Bolivia</span>
      </h1>
      
      <p class="hero-subtitle">
        Profesionales, Restaurantes, Trabajos y Servicios en tu ciudad
      </p>

      <!-- Tabs de Categorías -->
      <div class="category-tabs">
        <button
          v-for="cat in categories"
          :key="cat.id"
          @click="selectedCategory = cat.id"
          :class="['category-tab', { active: selectedCategory === cat.id }]"
        >
          <va-icon :name="cat.icon" size="small" />
          {{ cat.label }}
        </button>
      </div>

      <!-- Barra de Búsqueda -->
      <div class="search-bar">
        <div class="search-input-wrapper">
          <va-icon name="search" class="search-icon" />
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="getPlaceholder()"
            class="search-input"
            @keyup.enter="handleSearch"
          />
        </div>

        <div class="location-wrapper">
          <va-icon name="location_on" class="location-icon" />
          <select v-model="selectedCity" class="location-select">
            <option value="">Toda Bolivia</option>
            <option value="oruro">Oruro</option>
            <option value="la-paz">La Paz</option>
            <option value="cochabamba">Cochabamba</option>
            <option value="santa-cruz">Santa Cruz</option>
            <option value="potosi">Potosí</option>
            <option value="tarija">Tarija</option>
            <option value="chuquisaca">Chuquisaca</option>
            <option value="beni">Beni</option>
            <option value="pando">Pando</option>
          </select>
        </div>

        <va-button
          @click="handleSearch"
          color="yellow-primary"
          size="large"
          class="search-button"
        >
          <va-icon name="search" />
          Buscar
        </va-button>
      </div>

      <!-- Búsquedas Populares -->
      <div class="popular-searches">
        <span class="popular-label">Búsquedas populares:</span>
        <button
          v-for="search in popularSearches"
          :key="search"
          @click="quickSearch(search)"
          class="popular-tag"
        >
          {{ search }}
        </button>
      </div>

      <!-- Estadísticas -->
      <div class="hero-stats">
        <div class="stat-item">
          <va-icon name="description" size="large" color="yellow-primary" />
          <div class="stat-content">
            <span class="stat-number">12.456+</span>
            <span class="stat-label">Anuncios Activos</span>
          </div>
        </div>
        
        <div class="stat-item">
          <va-icon name="people" size="large" color="yellow-primary" />
          <div class="stat-content">
            <span class="stat-number">45.678+</span>
            <span class="stat-label">Usuarios</span>
          </div>
        </div>
        
        <div class="stat-item">
          <va-icon name="verified" size="large" color="yellow-primary" />
          <div class="stat-content">
            <span class="stat-number">3.421+</span>
            <span class="stat-label">Verificados</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// ==========================================
// COMPOSABLES
// ==========================================
const router = useRouter()

// ==========================================
// STATE
// ==========================================
const selectedCategory = ref('profesionales')
const searchQuery = ref('')
const selectedCity = ref('')

const categories = [
  { id: 'profesionales', label: 'Profesionales', icon: 'work' },
  { id: 'gastronomia', label: 'Gastronomía', icon: 'restaurant' },
  { id: 'trabajos', label: 'Trabajos', icon: 'business_center' },
  { id: 'servicios', label: 'Servicios', icon: 'build' }
]

const popularSearches = ['Abogados', 'Restaurantes', 'Plomero', 'Desarrollador']

// ==========================================
// MÉTODOS
// ==========================================
const getPlaceholder = () => {
  const placeholders = {
    profesionales: 'Busca abogados, doctores, contadores...',
    gastronomia: 'Busca restaurantes, cafeterías, comida rápida...',
    trabajos: 'Busca empleos, ofertas laborales...',
    servicios: 'Busca plomeros, electricistas, carpinteros...'
  }
  return placeholders[selectedCategory.value]
}

const handleSearch = () => {
  // Construir query params
  const params = {
    q: searchQuery.value,
    ciudad: selectedCity.value
  }
  
  // Navegar a la vista de guías con filtros
  router.push({
    name: `guias-${selectedCategory.value}`,
    query: params
  })
}

const quickSearch = (term) => {
  searchQuery.value = term
  handleSearch()
}
</script>

<style scoped>
   ESTADÍSTICAS
   ========================================== */
.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 3rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-yellow-primary);
}

.stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
  .hero-section {
    padding: 3rem 1rem;
    min-height: auto;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
  }

  .category-tabs {
    gap: 0.5rem;
  }

  .category-tab {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }

  .search-bar {
    flex-direction: column;
    gap: 0.75rem;
  }

  .location-wrapper {
    border-left: none;
    border-top: 2px solid #E0E0E0;
    padding-top: 0.75rem;
  }

  .hero-stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .popular-searches {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.5rem;
  }

  .search-button {
    width: 100%;
  }
}
</style>
   HERO SECTION
   ========================================== */
.hero-section {
  background: linear-gradient(135deg, var(--color-purple-darkest) 0%, var(--color-purple) 100%);
  padding: 4rem 1rem;
  min-height: 600px;
  display: flex;
  align-items: center;
}

.hero-content {
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

/* ==========================================
   TÍTULOS
   ========================================== */
.hero-title {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  text-align: center;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.hero-title .highlight {
  color: var(--color-yellow-primary);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
  margin-bottom: 3rem;
}

/* ==========================================
   TABS DE CATEGORÍAS
   ========================================== */
.category-tabs {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.category-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border: 2px solid transparent;
  border-radius: 50px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.category-tab:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.category-tab.active {
  background-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  border-color: var(--color-yellow-primary);
}

/* ==========================================
   BARRA DE BÚSQUEDA
   ========================================== */
.search-bar {
  display: flex;
  gap: 1rem;
  background-color: white;
  padding: 0.75rem;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  margin-bottom: 2rem;
}

.search-input-wrapper {
  flex: 2;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0 1rem;
}

.search-icon {
  color: var(--color-purple);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1rem;
  color: #333;
}

.search-input::placeholder {
  color: #999;
}

.location-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1rem;
  border-left: 2px solid #E0E0E0;
}

.location-icon {
  color: var(--color-yellow-primary);
}

.location-select {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1rem;
  color: #333;
  cursor: pointer;
  background-color: transparent;
}

.search-button {
  border-radius: 12px;
  font-weight: 600;
  padding: 0 2rem;
}

/* ==========================================
   BÚSQUEDAS POPULARES
   ========================================== */
.popular-searches {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

.popular-label {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.popular-tag {
  padding: 0.5rem 1rem;
  background-color: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.popular-tag:hover {
  background-color: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  border-color: var(--color-yellow-primary);
  transform: translateY(-2px);
}

/* ==========================================