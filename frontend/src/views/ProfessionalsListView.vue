<!-- frontend/src/views/ProfessionalsListView.vue -->
<template>
  <MainLayout>
    <section class="professionals-list-section">
      <div class="container">
        <!-- Header -->
        <div class="page-header">
          <div class="header-content">
            <h1 class="page-title">
              <va-icon name="work" size="2rem" color="purple" />
              Profesionales en Bolivia
            </h1>
            <p class="page-subtitle">
              Encuentra profesionales certificados y de confianza
            </p>
          </div>
          
          <va-button
            color="yellow-primary"
            size="large"
            @click="$router.push('/publicar')"
          >
            <va-icon name="add_circle" />
            Publicar Gratis
          </va-button>
        </div>

        <!-- Filtros -->
        <div class="filters-section">
          <div class="filters-grid">
            <!-- Subcategoría -->
            <div class="filter-group">
              <label class="filter-label">
                <va-icon name="category" size="small" />
                Especialidad
              </label>
              <select v-model="filters.subcategory" class="filter-select" @change="applyFilters">
                <option value="">Todas las especialidades</option>
                <option value="abogados">Abogados</option>
                <option value="doctores">Doctores</option>
                <option value="contadores">Contadores</option>
                <option value="arquitectos">Arquitectos</option>
                <option value="ingenieros">Ingenieros</option>
                <option value="psicologos">Psicólogos</option>
              </select>
            </div>

            <!-- Ciudad -->
            <div class="filter-group">
              <label class="filter-label">
                <va-icon name="place" size="small" />
                Ciudad
              </label>
              <select v-model="filters.city" class="filter-select" @change="applyFilters">
                <option value="">Todas las ciudades</option>
                <option value="cochabamba">Cochabamba</option>
                <option value="la-paz">La Paz</option>
                <option value="santa-cruz">Santa Cruz</option>
                <option value="oruro">Oruro</option>
                <option value="potosi">Potosí</option>
                <option value="tarija">Tarija</option>
                <option value="sucre">Sucre</option>
              </select>
            </div>

            <!-- Búsqueda -->
            <div class="filter-group search-group">
              <label class="filter-label">
                <va-icon name="search" size="small" />
                Buscar
              </label>
              <input
                v-model="filters.search"
                type="text"
                class="filter-input"
                placeholder="Buscar por nombre o especialidad..."
                @input="debouncedSearch"
              />
            </div>
          </div>

          <!-- Resultados count -->
          <div class="results-info">
            <p>
              Mostrando <strong>{{ filteredListings.length }}</strong> 
              {{ filteredListings.length === 1 ? 'profesional' : 'profesionales' }}
            </p>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="loading-container">
          <va-progress-circle indeterminate color="purple" />
          <p>Cargando profesionales...</p>
        </div>

        <!-- Grid de tarjetas -->
        <div v-else-if="filteredListings.length > 0" class="professionals-grid">
          <ProfessionalCard
            v-for="listing in filteredListings"
            :key="listing.id"
            :listing="listing"
          />
        </div>

        <!-- Empty state -->
        <div v-else class="empty-state">
          <va-icon name="search_off" size="4rem" color="#999" />
          <h3>No se encontraron profesionales</h3>
          <p>Intenta ajustar los filtros o buscar algo diferente</p>
          <va-button
            color="purple"
            @click="clearFilters"
          >
            Limpiar filtros
          </va-button>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '@/components/Layout/MainLayout.vue'
import ProfessionalCard from '@/components/Guide/ProfessionalCard.vue'

const router = useRouter()
const loading = ref(false)
const listings = ref([])

const filters = ref({
  subcategory: '',
  city: '',
  search: ''
})

// Mock data (reemplazar con API real)
const mockListings = ref([
  {
    id: 1,
    slug: 'juan-perez-abogado',
    title: 'Dr. Juan Pérez',
    professionalTitle: 'Abogado especializado en derecho civil y familiar',
    yearsExperience: 15,
    specialties: ['Derecho Civil', 'Derecho Familiar', 'Mediación'],
    city: 'Cochabamba',
    subcategory: 'abogados',
    plan: 'destacado',
    images: [{ url: 'https://via.placeholder.com/400x300/5C0099/FFFFFF?text=Dr.+Juan+P%C3%A9rez' }]
  },
  {
    id: 2,
    slug: 'maria-gomez-doctora',
    title: 'Dra. María Gómez',
    professionalTitle: 'Médico General con especialidad en Pediatría',
    yearsExperience: 10,
    specialties: ['Pediatría', 'Medicina General', 'Vacunación'],
    city: 'La Paz',
    subcategory: 'doctores',
    plan: 'premium',
    images: [{ url: 'https://via.placeholder.com/400x300/510087/FFFFFF?text=Dra.+Mar%C3%ADa' }]
  },
  {
    id: 3,
    slug: 'carlos-rodriguez-contador',
    title: 'Lic. Carlos Rodríguez',
    professionalTitle: 'Contador Público Autorizado',
    yearsExperience: 8,
    specialties: ['Contabilidad', 'Auditoría', 'Impuestos'],
    city: 'Santa Cruz',
    subcategory: 'contadores',
    plan: 'free',
    images: []
  },
  {
    id: 4,
    slug: 'ana-martinez-arquitecta',
    title: 'Arq. Ana Martínez',
    professionalTitle: 'Arquitecta especializada en diseño moderno',
    yearsExperience: 12,
    specialties: ['Diseño Arquitectónico', 'Remodelación', 'Construcción'],
    city: 'Cochabamba',
    subcategory: 'arquitectos',
    plan: 'premium',
    images: [{ url: 'https://via.placeholder.com/400x300/3D0066/FFFFFF?text=Arq.+Ana' }]
  }
])

// Filtrado
const filteredListings = computed(() => {
  let result = listings.value

  if (filters.value.subcategory) {
    result = result.filter(l => l.subcategory === filters.value.subcategory)
  }

  if (filters.value.city) {
    result = result.filter(l => l.city.toLowerCase().replace(/\s/g, '-') === filters.value.city)
  }

  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    result = result.filter(l => 
      l.title.toLowerCase().includes(search) ||
      l.professionalTitle.toLowerCase().includes(search) ||
      l.specialties.some(s => s.toLowerCase().includes(search))
    )
  }

  // Ordenar: destacados primero
  return result.sort((a, b) => {
    if (a.plan === 'destacado' && b.plan !== 'destacado') return -1
    if (a.plan !== 'destacado' && b.plan === 'destacado') return 1
    if (a.plan === 'premium' && b.plan === 'free') return -1
    if (a.plan === 'free' && b.plan === 'premium') return 1
    return 0
  })
})

const applyFilters = () => {
  // Aquí harías el fetch a la API con los filtros
  console.log('Aplicando filtros:', filters.value)
}

let searchTimeout = null
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 500)
}

const clearFilters = () => {
  filters.value = {
    subcategory: '',
    city: '',
    search: ''
  }
  applyFilters()
}

const fetchListings = async () => {
  loading.value = true
  
  try {
    // TODO: Reemplazar con llamada real a la API
    // const response = await fetch('/api/professionals/')
    // listings.value = await response.json()
    
    // Mock data por ahora
    await new Promise(resolve => setTimeout(resolve, 1000))
    listings.value = mockListings.value
  } catch (error) {
    console.error('Error cargando profesionales:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchListings()
})
</script>

<style scoped>
.professionals-list-section {
  min-height: calc(100vh - 200px);
  padding: 3rem 1rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  gap: 2rem;
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.page-subtitle {
  font-size: 1.125rem;
  color: #666;
  margin: 0;
}

/* Filtros */
.filters-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.search-group {
  grid-column: span 1;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  font-size: 0.95rem;
}

.filter-select,
.filter-input {
  padding: 0.875rem 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.filter-select:focus,
.filter-input:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

.results-info {
  padding-top: 1rem;
  border-top: 2px solid #F5F5F5;
  color: #666;
}

.results-info strong {
  color: var(--color-purple);
}

/* Grid */
.professionals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 4rem 2rem;
  color: #666;
}

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: var(--color-purple-darkest);
  margin: 0;
}

.empty-state p {
  color: #666;
  margin: 0;
}

@media (max-width: 1024px) {
  .filters-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .search-group {
    grid-column: span 2;
  }

  .professionals-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .professionals-list-section {
    padding: 2rem 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .filters-section {
    padding: 1.5rem;
  }

  .filters-grid {
    grid-template-columns: 1fr;
  }

  .search-group {
    grid-column: span 1;
  }

  .professionals-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
}
</style>