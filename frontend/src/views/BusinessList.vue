<!-- frontend/src/views/BusinessList.vue -->
<!-- 🔥 VERSIÓN DEFINITIVA - GRID ESTILO PROFESIONALES -->
<template>
  <MainLayout>
    <div class="business-list">
      
      <!-- Hero Header -->
      <div class="list-hero">
        <h1 class="hero-title">Guías de Negocios</h1>
        <p class="hero-subtitle">
          Descubre Empresas y PyMEs Bolivianas verificadas y legalmente establecidas
        </p>
      </div>

      <!-- Filters & Search -->
      <div class="filters-section">
        
        <!-- Filters Container - ALINEADO -->
        <div class="filters-container">
          
          <!-- Search -->
          <div class="filter-item filter-search">
            <label class="filter-label">BUSCAR</label>
            <VaInput
              v-model="filters.search"
              placeholder="Buscar negocios..."
              @input="handleSearch"
            >
              <template #prependInner>
                <VaIcon name="search" />
              </template>
            </VaInput>
          </div>

          <!-- Category Filter -->
          <div class="filter-item">
            <label class="filter-label">CATEGORÍA</label>
            <VaSelect
              v-model="filters.category"
              :options="['Todas', ...categories]"
              placeholder="Todas"
              @update:model-value="applyFilters"
            />
          </div>

          <!-- City Filter -->
          <div class="filter-item">
            <label class="filter-label">CIUDAD</label>
            <VaSelect
              v-model="filters.city"
              :options="['Todas', ...cities]"
              placeholder="Todas"
              @update:model-value="applyFilters"
            />
          </div>

          <!-- Plan Filter -->
          <div class="filter-item">
            <label class="filter-label">PLAN</label>
            <VaSelect
              v-model="filters.plan"
              :options="['Todos', 'Top', 'Destacado', 'Sugerido', 'Básico']"
              placeholder="Todos"
              @update:model-value="applyFilters"
            />
          </div>

        </div>

        <!-- Results Info -->
        <div class="results-info">
          <div class="results-count">
            Mostrando <strong>{{ filteredBusinesses.length }}</strong>
            {{ filteredBusinesses.length === 1 ? 'negocio' : 'negocios' }}
          </div>
          
          <div class="results-actions">
            <!-- Clear Filters -->
            <VaButton
              v-if="hasActiveFilters"
              preset="plain"
              icon="close"
              @click="clearFilters"
            >
              Limpiar Filtros
            </VaButton>
            
         
            
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <VaProgressCircle indeterminate color="purple" size="large" />
        <p>Cargando negocios...</p>
      </div>

      <!-- Business Grid -->
      <div v-else-if="filteredBusinesses.length > 0" class="business-grid">
        <BusinessCard
          v-for="business in paginatedBusinesses"
          :key="business.id"
          :business="business"
        />
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <va-icon name="store" size="5rem" color="#CCC" />
        <h3>No se encontraron negocios</h3>
        <p>Intenta ajustar tus filtros de búsqueda</p>
        <VaButton color="purple" @click="clearFilters">
          Limpiar Filtros
        </VaButton>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <VaPagination
          v-model="currentPage"
          :pages="totalPages"
          :visible-pages="5"
        />
      </div>

    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '@/components/Layout/MainLayout.vue'
import BusinessCard from '@/components/Guide/BusinessCard.vue'

// ⭐ IMPORTAR DATOS DE PRUEBA
import { mockBusinesses, filterBusinesses } from '@/data/mockBusinesses'

// ========== COMPOSABLES ==========
const router = useRouter()

// ========== STATE ==========
const loading = ref(false)
const allBusinesses = ref([])
const currentPage = ref(1)
const itemsPerPage = ref(12)

const filters = ref({
  search: '',
  category: 'Todas',
  city: 'Todas',
  plan: 'Todos'
})

const categories = [
  'Manufactura',
  'Servicios',
  'Comercio',
  'Tecnología',
  'Alimentación',
  'Construcción',
  'Textil',
  'Automotriz'
]

const cities = [
  'La Paz',
  'Santa Cruz',
  'Cochabamba',
  'Oruro',
  'Potosí',
  'Tarija',
  'Sucre',
  'Beni',
  'Pando'
]

// ========== COMPUTED ==========
const filteredBusinesses = computed(() => {
  return filterBusinesses({
    search: filters.value.search,
    category: filters.value.category,
    city: filters.value.city,
    plan: filters.value.plan
  })
})

const paginatedBusinesses = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredBusinesses.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredBusinesses.value.length / itemsPerPage.value)
})

const hasActiveFilters = computed(() => {
  return filters.value.search ||
         (filters.value.category && filters.value.category !== 'Todas') ||
         (filters.value.city && filters.value.city !== 'Todas') ||
         (filters.value.plan && filters.value.plan !== 'Todos')
})

// ========== METHODS ==========
const fetchBusinesses = async () => {
  loading.value = true
  
  // Simular delay de API
  await new Promise(resolve => setTimeout(resolve, 500))
  
  // ⭐ USAR DATOS DE PRUEBA
  allBusinesses.value = mockBusinesses
  
  loading.value = false
}

const handleSearch = () => {
  currentPage.value = 1
  applyFilters()
}

const applyFilters = () => {
  currentPage.value = 1
}

const clearFilters = () => {
  filters.value = {
    search: '',
    category: 'Todas',
    city: 'Todas',
    plan: 'Todos'
  }
  currentPage.value = 1
}

const goToCreate = () => {
  router.push('/guias/negocios/crear')
}

// ========== LIFECYCLE ==========
onMounted(() => {
  fetchBusinesses()
})
</script>

<style scoped>
/* ========== Container ========== */
.business-list {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}

/* ========== Hero ========== */
.list-hero {
  text-align: center;
  margin-bottom: 3rem;
}

.hero-title {
  margin: 0 0 1rem 0;
  font-size: 3rem;
  font-weight: 700;
  color: #5C0099;
}

.hero-subtitle {
  margin: 0;
  font-size: 1.25rem;
  color: #666;
}

/* ========== Filters ========== */
.filters-section {
  margin-bottom: 3rem;
}

.filters-container {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  align-items: end;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #5C0099;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.filter-search {
  grid-column: 1 / 2;
}

/* ========== Results Info ========== */
.results-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0.5rem;
}

.results-count {
  color: #666;
  font-size: 1rem;
}

.results-count strong {
  color: #5C0099;
  font-size: 1.25rem;
  font-weight: 700;
}

.results-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

/* ========== Loading ========== */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1.5rem;
}

.loading-state p {
  margin: 0;
  color: #666;
  font-weight: 500;
}

/* ========== Grid - ESTILO PROFESIONALES ========== */
.business-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

/* ========== Empty State ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1.5rem;
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.empty-state h3 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
  font-weight: 700;
}

.empty-state p {
  margin: 0;
  color: #666;
}

/* ========== Pagination ========== */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 3rem;
}

/* ========== Responsive ========== */
@media (max-width: 1400px) {
  .business-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 1200px) {
  .business-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 1024px) {
  .filters-container {
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .filter-search {
    grid-column: 1 / -1;
  }

  .business-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  }
}

@media (max-width: 768px) {
  .business-list {
    padding: 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .filters-container {
    grid-template-columns: 1fr;
    padding: 1.5rem;
  }

  .filter-search {
    grid-column: 1;
  }

  .results-info {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .results-actions {
    flex-direction: column;
  }

  .business-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
}

@media (max-width: 480px) {
  .business-grid {
    grid-template-columns: 1fr;
  }
}
</style>