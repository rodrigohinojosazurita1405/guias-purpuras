<!-- frontend/src/components/Home/HeroSection.vue -->
<template>
  <section class="hero-section">
    <!-- Slider de Imágenes de Fondo -->
    <div class="hero-background-slider">
      <transition name="fade-slide" mode="out-in">
        <div 
          :key="currentSlide" 
          class="hero-slide"
          :style="{ backgroundImage: `url(${backgroundImages[currentSlide]})` }"
        ></div>
      </transition>
      <div class="hero-overlay"></div>
    </div>

    <div class="hero-content">
      <!-- Título Principal -->
      <h1 class="hero-title">
        Una guía moderna para una 
        <span class="highlight">Bolivia</span>
        conectada 
      </h1>
      
      <p class="hero-subtitle">
        Somos el ecosistema digital que conecta el talento, gastronomía, las empresas PyMe y las oportunidades de Bolivia.
      </p>

      <!-- Tabs de Categorías -->
      <div class="category-tabs">
        <button
          v-for="cat in categories"
          :key="cat.id"
          @click="selectCategory(cat.id)"
          :class="['category-tab', { active: searchStore.selectedCategory === cat.id }]"
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
            v-model="searchStore.searchQuery"
            type="text"
            :placeholder="getPlaceholder()"
            class="search-input"
            @keyup.enter="handleSearch"
          />
        </div>

        <div class="location-wrapper">
          <va-icon 
            :name="searchStore.isLoadingLocation ? 'refresh' : 'location_on'" 
            :class="['location-icon', { spinning: searchStore.isLoadingLocation }]" 
          />
          <select 
            v-model="searchStore.selectedCity" 
            class="location-select"
            @change="onCityChange"
            :disabled="searchStore.isLoadingLocation"
          >
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
          
          <!-- Badge de ubicación detectada -->
          <button 
            v-if="searchStore.userDetectedCity && searchStore.locationMethod !== 'manual'"
            @click="searchStore.resetLocation()"
            class="location-badge"
            title="Ciudad detectada automáticamente. Click para re-detectar"
          >
            <va-icon name="my_location" size="14px" />
            <span>Auto</span>
          </button>
        </div>

        <va-button
          @click="handleSearch"
          color="yellow-primary"
          size="large"
          class="search-button"
          :loading="searchStore.isLoadingLocation"
        >
          <va-icon name="search" />
          Buscar
        </va-button>
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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useSearchStore } from '@/stores/useSearchStore'

const router = useRouter()
const searchStore = useSearchStore()

// ==========================================
// STATE
// ==========================================
const currentSlide = ref(0)

// ==========================================
// IMÁGENES DEL SLIDER
// ==========================================
const backgroundImages = [
  new URL('@/assets/hero/bg1.jpg', import.meta.url).href,
  // Agrega más imágenes aquí
]

// ==========================================
// CONFIGURACIÓN DEL SLIDER
// ==========================================
let sliderInterval = null
const SLIDE_DURATION = 5000

// ==========================================
// DATOS
// ==========================================
const categories = [
  { id: 'profesionales', label: 'Profesionales', icon: 'work' },
  { id: 'gastronomia', label: 'Gastronomía', icon: 'restaurant' },
  { id: 'trabajos', label: 'Trabajos', icon: 'business_center' },
  { id: 'negocios', label: 'Negocios', icon: 'store' }
]

// ✅ BÚSQUEDAS POPULARES DINÁMICAS SEGÚN CATEGORÍA
const popularSearches = computed(() => {
  const searches = {
    profesionales: ['Abogados', 'Doctores', 'Contadores', 'Arquitectos'],
    gastronomia: ['Restaurantes', 'Pizzerías', 'Cafeterías', 'Heladerías'],
    trabajos: ['Desarrollador', 'Diseñador', 'Contador', 'Ingeniero'],
    negocios: ['Manufactura', 'Tecnología', 'Comercio', 'Servicios']
  }
  return searches[searchStore.selectedCategory] || searches.profesionales
})

// ==========================================
// MÉTODOS
// ==========================================
const getPlaceholder = () => {
  const placeholders = {
    profesionales: 'Busca abogados, doctores, contadores...',
    gastronomia: 'Busca restaurantes, cafeterías, comida rápida...',
    trabajos: 'Busca empleos, ofertas laborales...',
    negocios: 'Busca Empresas, PyMes, Industrias...'
  }
  return placeholders[searchStore.selectedCategory]
}

const selectCategory = (categoryId) => {
  searchStore.setSelectedCategory(categoryId)
}

const onCityChange = () => {
  // Cuando el usuario cambia manualmente, actualizar el store
  searchStore.setSelectedCity(searchStore.selectedCity)
}

const handleSearch = () => {
  router.push({
    path: `/guias/${searchStore.selectedCategory}`,
    query: searchStore.searchParams
  })
}

const quickSearch = (term) => {
  searchStore.setSearchQuery(term)
  handleSearch()
}

// ==========================================
// SLIDER AUTOMÁTICO
// ==========================================
const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % backgroundImages.length
}

const startSlider = () => {
  if (backgroundImages.length > 1) {
    sliderInterval = setInterval(nextSlide, SLIDE_DURATION)
  }
}

const stopSlider = () => {
  if (sliderInterval) {
    clearInterval(sliderInterval)
  }
}

// ==========================================
// LIFECYCLE HOOKS
// ==========================================
onMounted(async () => {
  startSlider()
  
  // 🎯 DETECTAR UBICACIÓN AUTOMÁTICAMENTE AL CARGAR
  await searchStore.detectUserLocation()
})

onBeforeUnmount(() => {
  stopSlider()
})
</script>

<style scoped>
/* ==========================================
   HERO SECTION
   ========================================== */
.hero-section {
  position: relative;
  padding: 4rem 1rem;
  min-height: 600px;
  display: flex;
  align-items: center;
  overflow: hidden;
  /* ✅ MANTENER Z-INDEX BAJO PARA NO INTERFERIR CON MODALES */
  z-index: 1;
}

/* ==========================================
   SLIDER DE FONDO
   ========================================== */
.hero-background-slider {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.hero-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg,  rgba(61, 0, 102, 0.50) 0%,rgba(156, 17, 249, 0.40) 100%);
  z-index: 1;
}

/* ==========================================
   TRANSICIONES DEL SLIDER
   ========================================== */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 1.5s ease-in-out;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
}

/* ==========================================
   CONTENIDO DEL HERO
   ========================================== */
.hero-content {
  position: relative;
  /* ✅ Z-INDEX BAJO PARA NO INTERFERIR CON MODALES (99999) */
  z-index: 2;
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  text-align: center;
  margin-bottom: 1rem;
  line-height: 1.2;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.hero-title .highlight {
  color: var(--color-yellow-primary);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.95);
  text-align: center;
  margin-bottom: 3rem;
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
  line-height: 1.6;
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
  background-color: var(--color-purple);
  color: white;
  transform: translateY(-2px);
  border-color: var(--color-purple);
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
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
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
  position: relative;
}

.location-icon {
  color: var(--color-yellow-primary);
  transition: transform 0.3s ease;
}

.location-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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

.location-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.location-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: rgba(92, 0, 153, 0.1);
  border: 1px solid rgba(92, 0, 153, 0.3);
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-purple);
  cursor: pointer;
  transition: all 0.2s ease;
}

.location-badge:hover {
  background: rgba(92, 0, 153, 0.2);
  transform: scale(1.05);
}

.search-button {
  border-radius: 12px;
  font-weight: 600;
  padding: 0 2rem;
  white-space: nowrap;
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
  color: rgba(255, 255, 255, 0.9);
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
  transition: all 0.3s ease;
}

.stat-item:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
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
  color: rgba(255, 255, 255, 0.9);
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .hero-stats {
    gap: 1.5rem;
  }

  .stat-item {
    padding: 1.25rem;
  }
}

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
    padding: 1rem;
  }

  .search-input-wrapper,
  .location-wrapper {
    padding: 0.75rem 1rem;
  }

  .location-wrapper {
    border-left: none;
    border-top: 2px solid #E0E0E0;
    padding-top: 0.75rem;
  }

  .search-button {
    width: 100%;
  }

  .hero-stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .popular-searches {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .popular-label {
    width: 100%;
    text-align: center;
    margin-bottom: 0.5rem;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 2rem 0.75rem;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .hero-subtitle {
    font-size: 0.95rem;
  }

  .category-tabs {
    flex-direction: column;
    width: 100%;
  }

  .category-tab {
    width: 100%;
    justify-content: center;
  }

  .search-bar {
    padding: 0.75rem;
  }

  .stat-item {
    padding: 1rem;
  }

  .stat-number {
    font-size: 1.5rem;
  }

  .stat-label {
    font-size: 0.85rem;
  }

  .popular-tag {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
}
</style>