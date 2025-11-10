<!-- frontend/src/components/Guide/TopFiltersBar.vue -->
<template>
  <div class="top-filters-bar">
    <div class="filters-container">
      <!-- Filtro de Especialidad/Tipo -->
      <div class="filter-group">
        <label class="filter-label">
          <va-icon :name="filterConfig.icon" size="small" />
          {{ filterConfig.label }}
        </label>
        <select 
          v-model="localFilters.subcategory" 
          class="filter-select"
          @change="emitFilters"
        >
          <option value="">{{ filterConfig.placeholder }}</option>
          <option 
            v-for="option in subcategories" 
            :key="option" 
            :value="option"
          >
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Filtro de Ciudad -->
      <div class="filter-group">
        <label class="filter-label">
          <va-icon name="place" size="small" />
          Ciudad
        </label>
        <select 
          v-model="localFilters.city" 
          class="filter-select"
          @change="emitFilters"
        >
          <option value="">Todas las ciudades</option>
          <option 
            v-for="city in cities" 
            :key="city" 
            :value="city"
          >
            {{ city }}
          </option>
        </select>
      </div>

      <!-- Campo de Búsqueda -->
      <div class="filter-group search-group">
        <label class="filter-label">
          <va-icon name="search" size="small" />
          Buscar
        </label>
        <input
          v-model="localFilters.search"
          type="text"
          :placeholder="searchPlaceholder"
          class="search-input"
          @input="emitFilters"
        />
      </div>
    </div>

    <!-- Contador de Resultados -->
    <div class="results-counter">
      Mostrando <strong>{{ resultsCount }}</strong> {{ resultsLabel }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  // Categoría actual (profesionales, gastronomia, trabajos, servicios)
  category: {
    type: String,
    required: true
  },
  
  // Subcategorías disponibles
  subcategories: {
    type: Array,
    default: () => []
  },
  
  // Ciudades disponibles
  cities: {
    type: Array,
    default: () => ['La Paz', 'Cochabamba', 'Santa Cruz', 'Oruro', 'Potosí', 'Tarija', 'Sucre', 'Beni', 'Pando']
  },
  
  // Número de resultados
  resultsCount: {
    type: Number,
    default: 0
  },

  // Filtros iniciales
  modelValue: {
    type: Object,
    default: () => ({
      subcategory: '',
      city: '',
      search: ''
    })
  }
})

const emit = defineEmits(['update:modelValue', 'filter-change'])

// Estado local de filtros
const localFilters = ref({
  subcategory: props.modelValue.subcategory || '',
  city: props.modelValue.city || '',
  search: props.modelValue.search || ''
})

// Configuración según categoría
const categoryConfigs = {
  profesionales: {
    icon: 'work',
    label: 'Especialidad',
    placeholder: 'Todas las especialidades',
    searchPlaceholder: 'Buscar por nombre o especialidad...',
    resultsLabel: 'profesionales'
  },
  gastronomia: {
    icon: 'restaurant',
    label: 'Tipo de cocina',
    placeholder: 'Todos los tipos',
    searchPlaceholder: 'Buscar por nombre o tipo de comida...',
    resultsLabel: 'restaurantes'
  },
  trabajos: {
    icon: 'business_center',
    label: 'Tipo de empleo',
    placeholder: 'Todos los tipos',
    searchPlaceholder: 'Buscar por cargo o empresa...',
    resultsLabel: 'ofertas de trabajo'
  },
  servicios: {
    icon: 'build',
    label: 'Tipo de servicio',
    placeholder: 'Todos los servicios',
    searchPlaceholder: 'Buscar por nombre o servicio...',
    resultsLabel: 'servicios'
  }
}

// Configuración actual según la categoría
const filterConfig = computed(() => {
  return categoryConfigs[props.category] || categoryConfigs.profesionales
})

// Placeholder del campo de búsqueda
const searchPlaceholder = computed(() => {
  return filterConfig.value.searchPlaceholder
})

// Label de resultados
const resultsLabel = computed(() => {
  return filterConfig.value.resultsLabel
})

// Emitir cambios de filtros
const emitFilters = () => {
  emit('update:modelValue', { ...localFilters.value })
  emit('filter-change', { ...localFilters.value })
}

// Limpiar filtros
const clearFilters = () => {
  localFilters.value = {
    subcategory: '',
    city: '',
    search: ''
  }
  emitFilters()
}

// Exponer método para limpiar desde el padre
defineExpose({
  clearFilters
})

// Watch para sincronizar con prop modelValue
watch(() => props.modelValue, (newValue) => {
  localFilters.value = { ...newValue }
}, { deep: true })
</script>

<style scoped>
.top-filters-bar {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.filters-container {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-purple-dark);
}

.filter-select,
.search-input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #333;
  background: white;
  transition: all 0.3s ease;
}

.filter-select:focus,
.search-input:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

.filter-select:hover,
.search-input:hover {
  border-color: var(--color-purple-light);
}

.search-input {
  font-family: inherit;
}

.search-input::placeholder {
  color: #999;
}

.results-counter {
  font-size: 0.95rem;
  color: #666;
  padding-top: 0.5rem;
  border-top: 1px solid #F0F0F0;
}

.results-counter strong {
  color: var(--color-purple);
  font-weight: 700;
}

/* Responsive */
@media (max-width: 1024px) {
  .filters-container {
    grid-template-columns: 1fr 1fr;
  }

  .search-group {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .top-filters-bar {
    padding: 1.25rem;
  }

  .filters-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .filter-select,
  .search-input {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }

  .results-counter {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .top-filters-bar {
    padding: 1rem;
  }

  .filter-label {
    font-size: 0.85rem;
  }

  .filter-select,
  .search-input {
    padding: 0.7rem 0.875rem;
    font-size: 0.85rem;
  }
}
</style>