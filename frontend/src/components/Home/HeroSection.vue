<!-- frontend/src/components/Home/HeroSection.vue -->
<template>
  <section class="hero-section">
    <!-- Background animado -->
    <div class="hero-background">
      <div
        class="bg-image bg-image-1"
        :class="{ active: currentBgIndex === 0 }"
        :style="{ backgroundImage: 'url(' + bg1 + ')' }"
      ></div>
      <div
        class="bg-image bg-image-2"
        :class="{ active: currentBgIndex === 1 }"
        :style="{ backgroundImage: 'url(' + bg2 + ')' }"
      ></div>
    </div>

    <!-- Contenedor principal con grid -->
    <div class="hero-container">
      <!-- Lado izquierdo: Buscador y contenido -->
      <div class="hero-content">
        <!-- Título compacto -->
        <h1 class="hero-title">
          Encuentra trabajo en <span class="highlight">Bolivia</span>
          <img src="@/assets/bolivia.webp" alt="Escudo de Bolivia" class="bolivia-shield" />
        </h1>

        <!-- Subtítulo motivacional -->
        <p class="hero-subtitle">
          Tu próxima oportunidad laboral te está esperando.<br>
          Conecta con miles de empleos en todo el país.
        </p>

        <!-- Barra de Búsqueda Principal -->
        <div class="search-card">
          <!-- Tabs compactos arriba del buscador -->
          <div class="search-tabs">
            <button
              v-for="jobType in jobTypes"
              :key="jobType.id"
              @click="selectCategory(jobType.id)"
              :class="['search-tab', { active: searchStore.selectedCategory === jobType.id }]"
            >
              <va-icon :name="jobType.icon" size="16px" />
              <span>{{ jobType.label }}</span>
            </button>
          </div>

          <!-- Inputs de búsqueda -->
          <div class="search-inputs">
            <!-- Búsqueda por palabra clave -->
            <div class="input-group">
              <va-icon name="search" class="input-icon" />
              <input
                v-model="searchStore.searchQuery"
                type="text"
                placeholder="Cargo, empresa o palabra clave"
                class="search-input"
                @keyup.enter="handleSearch"
              />
            </div>

            <!-- Selector de ciudad -->
            <div class="input-group location-group">
              <va-icon
                :name="searchStore.isLoadingLocation ? 'refresh' : 'location_on'"
                :class="['input-icon', { spinning: searchStore.isLoadingLocation }]"
              />
              <select
                v-model="searchStore.selectedCity"
                class="search-input location-select"
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

              <!-- Badge pequeño de auto-detección -->
              <span
                v-if="searchStore.userDetectedCity && searchStore.locationMethod !== 'manual'"
                class="auto-badge"
                title="Ciudad detectada automáticamente"
              >
                <va-icon name="my_location" size="12px" />
              </span>
            </div>

            <!-- Botón de búsqueda -->
            <button
              @click="handleSearch"
              class="search-btn"
              :disabled="searchStore.isLoadingLocation"
            >
              <va-icon name="search" size="20px" />
              <span>Buscar empleos</span>
            </button>
          </div>
        </div>

        <!-- Estadísticas compactas -->
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-number">12.4K+</span>
            <span class="stat-label">Empleos</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">45K+</span>
            <span class="stat-label">Usuarios</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">3.4K+</span>
            <span class="stat-label">Verificados</span>
          </div>
        </div>
      </div>

      <!-- Lado derecho: Mapa de Bolivia decorativo -->
      <div class="hero-visual">
        <img
          src="@/assets/hero/bolivia2.png"
          alt="Mapa de Bolivia"
          class="bolivia-map"
        />
        <div class="map-overlay">
          <!-- Líneas de conexión animadas -->
          <svg class="connection-lines" viewBox="0 0 100 100" preserveAspectRatio="none">
            <line class="connect-line line-1" x1="44" y1="32" x2="36" y2="42" />
            <line class="connect-line line-2" x1="36" y1="42" x2="42" y2="54" />
            <line class="connect-line line-3" x1="42" y1="54" x2="52" y2="58" />
            <line class="connect-line line-4" x1="50" y1="44" x2="52" y2="58" />
          </svg>

          <!-- Puntos principales de ciudades -->
          <div class="pulse-dot" style="top: 32%; left: 44%" title="Pando">
            <span class="city-label">Pando</span>
          </div>
          <div class="pulse-dot pulse-delay-1" style="top: 42%; left: 36%" title="La Paz">
            <span class="city-label">La Paz</span>
          </div>
          <div class="pulse-dot pulse-delay-2" style="top: 44%; left: 50%" title="Beni">
            <span class="city-label">Beni</span>
          </div>
          <div class="pulse-dot pulse-delay-3" style="top: 54%; left: 42%" title="Cochabamba">
            <span class="city-label">Cochabamba</span>
          </div>
          <div class="pulse-dot pulse-delay-4" style="top: 58%; left: 52%" title="Santa Cruz">
            <span class="city-label">Santa Cruz</span>
          </div>
          <div class="pulse-dot pulse-delay-5" style="top: 52%; left: 34%" title="Oruro">
            <span class="city-label">Oruro</span>
          </div>
          <div class="pulse-dot pulse-delay-6" style="top: 64%; left: 38%" title="Potosí">
            <span class="city-label">Potosí</span>
          </div>

          <!-- Nuevos puntos adicionales -->
          <div class="pulse-dot pulse-delay-7" style="top: 72%; left: 40%" title="Tarija">
            <span class="city-label">Tarija</span>
          </div>
          <div class="pulse-dot pulse-delay-8" style="top: 68%; left: 34%" title="Chuquisaca">
            <span class="city-label">Chuquisaca</span>
          </div>

          <!-- Partículas tech flotantes -->
          <div class="tech-particle" style="top: 28%; left: 25%; animation-delay: 0s;"></div>
          <div class="tech-particle" style="top: 48%; left: 55%; animation-delay: 1.5s;"></div>
          <div class="tech-particle" style="top: 70%; left: 22%; animation-delay: 3s;"></div>
          <div class="tech-particle" style="top: 80%; left: 45%; animation-delay: 4.5s;"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSearchStore } from '@/stores/useSearchStore'
import bg1 from '@/assets/hero/bg1.jpg'
import bg2 from '@/assets/hero/bg2.jpg'

const router = useRouter()
const searchStore = useSearchStore()

// ==========================================
// BACKGROUND ANIMATION
// ==========================================
const currentBgIndex = ref(0)
let bgInterval = null

const startBackgroundRotation = () => {
  bgInterval = setInterval(() => {
    currentBgIndex.value = (currentBgIndex.value + 1) % 2
  }, 8000) // Cambia cada 8 segundos
}

// ==========================================
// DATOS
// ==========================================
const jobTypes = [
  { id: 'todas', label: 'Todas', icon: 'work' },
  { id: 'tiempo-completo', label: 'Tiempo Completo', icon: 'work_history' },
  { id: 'remoto', label: 'Remoto', icon: 'laptop' },
  { id: 'freelance', label: 'Freelance', icon: 'person_check' },
  { id: 'practicas', label: 'Pasantía', icon: 'school' }
]

// ✅ BÚSQUEDAS POPULARES DINÁMICAS SEGÚN TIPO DE TRABAJO
const popularSearches = computed(() => {
  const searches = {
    todas: ['Desarrollador', 'Diseñador', 'Contador', 'Ingeniero', 'Vendedor'],
    'tiempo-completo': ['Gerente', 'Analista', 'Especialista', 'Coordinador'],
    remoto: ['Frontend Developer', 'Backend Developer', 'UI/UX Designer', 'Virtual Assistant'],
    freelance: ['Diseñador Gráfico', 'Copywriter', 'Community Manager', 'Programador'],
    practicas: ['Practicante IT', 'Practicante RRHH', 'Practicante Ventas', 'Practicante Contabilidad']
  }
  return searches[searchStore.selectedCategory] || searches.todas
})

// ==========================================
// MÉTODOS
// ==========================================
const getPlaceholder = () => {
  const placeholders = {
    todas: 'Busca empleos, ofertas laborales...',
    'tiempo-completo': 'Busca trabajos de tiempo completo...',
    remoto: 'Busca trabajos remotos...',
    freelance: 'Busca trabajos por proyecto...',
    practicas: 'Busca programas de pasantía...'
  }
  return placeholders[searchStore.selectedCategory] || placeholders.todas
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
    path: '/guias/trabajos',
    query: searchStore.searchParams
  })
}

const quickSearch = (term) => {
  searchStore.setSearchQuery(term)
  handleSearch()
}

// ==========================================
// LIFECYCLE HOOKS
// ==========================================
onMounted(async () => {
  // 🎯 DETECTAR UBICACIÓN AUTOMÁTICAMENTE AL CARGAR
  await searchStore.detectUserLocation()

  // Iniciar rotación de background
  startBackgroundRotation()
})

onUnmounted(() => {
  // Limpiar el interval cuando el componente se desmonte
  if (bgInterval) {
    clearInterval(bgInterval)
  }
})
</script>

<style scoped>
/* ==========================================
   HERO SECTION - REDISEÑO FUNCIONAL
   ========================================== */
.hero-section {
  position: relative;
  width: 100%;
  min-height: 65vh;
  max-height: 70vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #5c0099 0%, #7c3aed 100%);
  padding: 2rem;
  overflow: hidden;
}

/* ==========================================
   BACKGROUND ANIMADO
   ========================================== */
.hero-background {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.bg-image {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0;
  transition: opacity 2s ease-in-out;
}

.bg-image.active {
  opacity: 0.80;
}

.bg-image::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.85) 0%, rgba(124, 58, 237, 0.85) 100%);
  z-index: 1;
}

/* Contenedor Grid */
.hero-container {
  position: relative;
  z-index: 2;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

/* ==========================================
   LADO IZQUIERDO - CONTENIDO
   ========================================== */
.hero-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  z-index: 2;
}

/* Título compacto */
.hero-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin: 0;
  line-height: 1.2;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.hero-title .highlight {
  color: var(--color-yellow-primary);
}

.bolivia-shield {
  width: 48px;
  height: 48px;
  object-fit: contain;
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3));
  animation: subtle-bounce 3s ease-in-out infinite;
}

@keyframes subtle-bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

.hero-subtitle {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0.25rem 0 1.5rem 0;
  line-height: 1.6;
  font-weight: 400;
}

/* ==========================================
   TARJETA DE BÚSQUEDA
   ========================================== */
.search-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

/* Tabs de búsqueda (arriba del input) */
.search-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
}

.search-tab {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  background: #F3F4F6;
  border: 2px solid transparent;
  border-radius: 8px;
  color: #6B7280;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-tab:hover {
  background: #E5E7EB;
  color: #374151;
}

.search-tab.active {
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  border-color: var(--color-yellow-primary);
}

/* Inputs de búsqueda */
.search-inputs {
  display: grid;
  grid-template-columns: 2fr 1.5fr auto;
  gap: 0.75rem;
  align-items: center;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: all 0.2s ease;
}

.input-group:focus-within {
  border-color: var(--color-purple);
  background: white;
}

.input-icon {
  color: #9CA3AF;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.input-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.95rem;
  color: #1F2937;
  font-weight: 500;
}

.search-input::placeholder {
  color: #9CA3AF;
}

.location-group {
  position: relative;
}

.location-select {
  appearance: none;
  cursor: pointer;
  padding-right: 2rem;
}

.location-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auto-badge {
  position: absolute;
  right: 1rem;
  display: inline-flex;
  align-items: center;
  padding: 0.25rem;
  background: var(--color-purple);
  border-radius: 50%;
  color: white;
}

/* Botón de búsqueda */
.search-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  background: linear-gradient(135deg, var(--color-yellow-light) 0%, var(--color-yellow-primary) 100%);
  color: #5c0099;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3);
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(253, 197, 0, 0.5);
  background: linear-gradient(135deg, var(--color-yellow-primary) 0%, var(--color-yellow-light) 100%);
}

.search-btn:active:not(:disabled) {
  transform: translateY(0);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ==========================================
   ESTADÍSTICAS COMPACTAS
   ========================================== */
.hero-stats {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-yellow-primary) !important;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: white !important;
  font-weight: 600;
}

.stat-divider {
  width: 1px;
  height: 2rem;
  background: rgba(255, 255, 255, 0.2);
}

/* ==========================================
   LADO DERECHO - MAPA BOLIVIA
   ========================================== */
.hero-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.bolivia-map {
  width: 100%;
  max-width: 450px;
  height: auto;
  filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.3));
  opacity: 0.95;
}

.map-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.pulse-dot {
  position: absolute;
  width: 14px;
  height: 14px;
  background: var(--color-yellow-primary);
  border-radius: 50%;
  box-shadow: 0 0 0 0 var(--color-yellow-primary);
  animation: pulse-ring 2.5s ease-out infinite;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.pulse-dot:hover {
  transform: scale(1.3);
}

/* Delays para animación escalonada */
.pulse-delay-1 {
  animation-delay: 0.3s;
}

.pulse-delay-2 {
  animation-delay: 0.6s;
}

.pulse-delay-3 {
  animation-delay: 0.9s;
}

.pulse-delay-4 {
  animation-delay: 1.2s;
}

.pulse-delay-5 {
  animation-delay: 1.5s;
}

.pulse-delay-6 {
  animation-delay: 1.8s;
}

.pulse-delay-7 {
  animation-delay: 2.1s;
}

.pulse-delay-8 {
  animation-delay: 2.4s;
}

/* Etiquetas de ciudades */
.city-label {
  position: absolute;
  top: -28px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(92, 0, 153, 0.95);
  color: var(--color-yellow-primary);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: 600;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.pulse-dot:hover .city-label {
  opacity: 1;
}

/* Líneas de conexión animadas */
.connection-lines {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.connect-line {
  stroke: var(--color-yellow-primary);
  stroke-width: 0.5;
  opacity: 0.3;
  stroke-dasharray: 5, 5;
  animation: dash-flow 3s linear infinite;
}

.line-1 {
  animation-delay: 0s;
}

.line-2 {
  animation-delay: 0.5s;
}

.line-3 {
  animation-delay: 1s;
}

.line-4 {
  animation-delay: 1.5s;
}

@keyframes dash-flow {
  0% {
    stroke-dashoffset: 0;
  }
  100% {
    stroke-dashoffset: 20;
  }
}

/* Partículas tech flotantes */
.tech-particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--color-yellow-primary);
  border-radius: 50%;
  opacity: 0;
  animation: float-particle 6s ease-in-out infinite;
  box-shadow: 0 0 8px var(--color-yellow-primary);
}

@keyframes float-particle {
  0%, 100% {
    opacity: 0;
    transform: translateY(0) scale(0.5);
  }
  25% {
    opacity: 0.6;
    transform: translateY(-30px) scale(1);
  }
  50% {
    opacity: 1;
    transform: translateY(-60px) scale(1.2);
  }
  75% {
    opacity: 0.6;
    transform: translateY(-30px) scale(1);
  }
}

@keyframes pulse-ring {
  0% {
    box-shadow: 0 0 0 0 var(--color-yellow-primary);
  }
  50% {
    box-shadow: 0 0 0 20px rgba(253, 197, 0, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(253, 197, 0, 0);
  }
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1200px) {
  .hero-container {
    gap: 3rem;
  }

  .bolivia-map {
    max-width: 380px;
  }
}

@media (max-width: 1024px) {
  .hero-section {
    min-height: 70vh;
    max-height: 75vh;
  }

  .hero-container {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .hero-visual {
    display: none; /* Ocultar mapa en tablets y móviles */
  }

  .hero-title {
    font-size: 2.2rem;
  }

  .search-inputs {
    grid-template-columns: 1fr;
  }

  .search-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .hero-section {
    min-height: auto;
    max-height: none;
    padding: 2rem 1rem;
  }

  .hero-content {
    gap: 1.5rem;
  }

  .hero-title {
    font-size: 1.875rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .bolivia-shield {
    width: 40px;
    height: 40px;
  }

  .hero-subtitle {
    font-size: 1rem;
    margin: 0.75rem 0 1.25rem 0;
  }

  .search-card {
    padding: 1.25rem;
  }

  .search-tabs {
    gap: 0.375rem;
  }

  .search-tab {
    font-size: 0.8125rem;
    padding: 0.4rem 0.75rem;
  }

  .hero-stats {
    gap: 1rem;
    padding: 0.875rem 1.25rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .stat-number {
    font-size: 1.125rem;
  }

  .stat-label {
    font-size: 0.6875rem;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 1.5rem 0.75rem;
  }

  .hero-title {
    font-size: 1.5rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .bolivia-shield {
    width: 36px;
    height: 36px;
  }

  .hero-subtitle {
    font-size: 0.9375rem;
    margin: 0.5rem 0 1rem 0;
  }

  .search-card {
    padding: 1rem;
  }

  .search-tabs {
    flex-direction: column;
    gap: 0.5rem;
  }

  .search-tab {
    width: 100%;
    justify-content: center;
  }

  .search-inputs {
    gap: 0.5rem;
  }

  .input-group {
    padding: 0.625rem 0.875rem;
  }

  .search-input {
    font-size: 0.875rem;
  }

  .search-btn {
    padding: 0.625rem 1.5rem;
    font-size: 0.875rem;
  }

  .hero-stats {
    gap: 0.75rem;
    padding: 0.75rem 1rem;
  }

  .stat-divider {
    height: 1.5rem;
  }

  .stat-number {
    font-size: 1rem;
  }

  .stat-label {
    font-size: 0.625rem;
  }
}
</style>