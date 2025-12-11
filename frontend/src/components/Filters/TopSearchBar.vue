<!--
  ═══════════════════════════════════════════════════════════
  TopSearchBar.vue - Barra de Búsqueda Superior Estilo OCC
  ═══════════════════════════════════════════════════════════

  Diseño inspirado en portales de empleo modernos
  Ubicación: Debajo del navbar, sticky al hacer scroll

  Características:
  - Búsqueda dual: Puesto/área + Ciudad
  - Filtros horizontales en dropdown
  - Botón CTA destacado
  - Responsive con hamburguesa en móvil
-->
<template>
  <div class="top-search-bar">
    <!-- Sección Principal de Búsqueda -->
    <div class="search-section">
      <div class="search-container">
        <!-- Input 1: Búsqueda de Puesto -->
        <div class="search-input-wrapper primary">
          <va-icon name="search" class="input-icon" />
          <input
            v-model="localFilters.search"
            type="text"
            class="search-input"
            :placeholder="searchPlaceholder"
            @input="handleSearch"
          />
          <button
            v-if="localFilters.search"
            class="clear-btn"
            @click="clearSearch"
            title="Limpiar búsqueda"
          >
            <va-icon name="close" size="small" />
          </button>
        </div>

        <!-- Input 2: Ciudad -->
        <div class="search-input-wrapper secondary">
          <va-icon name="place" class="input-icon" />
          <select
            v-model="localFilters.city"
            class="search-select"
            @change="emitFilters"
          >
            <option value="">Ciudad o Departamento</option>
            <option
              v-for="city in cities"
              :key="city"
              :value="city"
            >
              {{ city }}
            </option>
          </select>
        </div>

        <!-- Botón Buscar -->
        <button class="search-cta-btn" @click="handleSearchClick">
          <va-icon name="search" size="small" />
          <span class="btn-text">Buscar</span>
        </button>
      </div>
    </div>

    <!-- Sección de Filtros Horizontales -->
    <div class="filters-section">
      <!-- Overlay oscuro para dropdowns en móvil -->
      <div
        v-if="activeDropdown"
        class="dropdown-backdrop"
        @click="activeDropdown = null"
      ></div>

      <!-- Botón scroll izquierda (móvil) -->
      <button
        v-if="showScrollButtons"
        class="scroll-btn scroll-left"
        @click="scrollFilters('left')"
        :disabled="!canScrollLeft"
      >
        <va-icon name="chevron_left" size="small" />
      </button>

      <div ref="filtersContainer" class="filters-container" @scroll="handleFiltersScroll">
        <!-- Filtros dinámicos según categoría -->
        <template v-if="category === 'trabajos'">
          <!-- Filtro: Sueldo -->
          <div class="filter-dropdown">
            <button
              class="filter-btn"
              :class="{ active: sidebarFilters.salaryMin || sidebarFilters.salaryMax }"
              @click.stop="toggleDropdown('salary')"
            >
              <span>Sueldo</span>
              <va-icon name="expand_more" size="small" />
            </button>
            <div v-if="activeDropdown === 'salary'" class="dropdown-menu">
              <div class="dropdown-content">
                <div class="salary-inputs">
                  <input
                    v-model.number="sidebarFilters.salaryMin"
                    type="number"
                    placeholder="Mínimo Bs"
                    class="salary-input"
                    @input="emitFilters"
                  />
                  <span class="separator">-</span>
                  <input
                    v-model.number="sidebarFilters.salaryMax"
                    type="number"
                    placeholder="Máximo Bs"
                    class="salary-input"
                    @input="emitFilters"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Filtro: Fecha -->
          <div class="filter-dropdown">
            <button
              class="filter-btn"
              :class="{ active: sidebarFilters.publishDate }"
              @click.stop="toggleDropdown('date')"
            >
              <span>Fecha</span>
              <va-icon name="expand_more" size="small" />
            </button>
            <div v-if="activeDropdown === 'date'" class="dropdown-menu">
              <div class="dropdown-content">
                <label class="dropdown-option">
                  <input
                    v-model="sidebarFilters.publishDate"
                    type="radio"
                    value="24h"
                    @change="emitFilters"
                  />
                  <span>Últimas 24 horas</span>
                </label>
                <label class="dropdown-option">
                  <input
                    v-model="sidebarFilters.publishDate"
                    type="radio"
                    value="7d"
                    @change="emitFilters"
                  />
                  <span>Última semana</span>
                </label>
                <label class="dropdown-option">
                  <input
                    v-model="sidebarFilters.publishDate"
                    type="radio"
                    value="30d"
                    @change="emitFilters"
                  />
                  <span>Último mes</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Filtro: Categoría -->
          <div class="filter-dropdown">
            <button
              class="filter-btn"
              :class="{ active: localFilters.category }"
              @click.stop="toggleDropdown('category')"
            >
              <span>Categoría</span>
              <va-icon name="expand_more" size="small" />
            </button>
            <div v-if="activeDropdown === 'category'" class="dropdown-menu">
              <div class="dropdown-content scrollable">
                <label class="dropdown-option">
                  <input
                    v-model="localFilters.category"
                    type="radio"
                    value=""
                    @change="emitFilters"
                  />
                  <span>Todas las categorías</span>
                </label>
                <label
                  v-for="cat in categories"
                  :key="cat"
                  class="dropdown-option"
                >
                  <input
                    v-model="localFilters.category"
                    type="radio"
                    :value="cat"
                    @change="emitFilters"
                  />
                  <span>{{ cat }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Filtro: Tipo de Contratación -->
          <div class="filter-dropdown">
            <button
              class="filter-btn"
              :class="{ active: localFilters.contractType }"
              @click.stop="toggleDropdown('contract')"
            >
              <span>Tipo de contratación</span>
              <va-icon name="expand_more" size="small" />
            </button>
            <div v-if="activeDropdown === 'contract'" class="dropdown-menu">
              <div class="dropdown-content">
                <label class="dropdown-option">
                  <input
                    v-model="localFilters.contractType"
                    type="radio"
                    value=""
                    @change="emitFilters"
                  />
                  <span>Todos los tipos</span>
                </label>
                <label
                  v-for="ct in contractTypes"
                  :key="ct"
                  class="dropdown-option"
                >
                  <input
                    v-model="localFilters.contractType"
                    type="radio"
                    :value="ct"
                    @change="emitFilters"
                  />
                  <span>{{ ct }}</span>
                </label>
              </div>
            </div>
          </div>
        </template>

        <!-- Ubicación y Contador de Resultados -->
        <div class="results-info-inline">
          <!-- Switch de Geolocalización -->
          <div class="location-toggle-wrapper">
            <label class="location-switch">
              <input
                type="checkbox"
                v-model="useGeolocation"
                @change="handleLocationToggle"
                class="switch-checkbox"
              />
              <span class="switch-slider"></span>
            </label>
          </div>

          <div class="location-display">
            <p class="location-prefix">Mostrando anuncios para:</p>
            <va-icon
              :name="searchStore.isLoadingLocation ? 'refresh' : 'location_on'"
              :class="['location-icon', { spinning: searchStore.isLoadingLocation }]"
              size="small"
            />
            <span class="location-text">{{ useGeolocation ? searchStore.displayCity : 'Todo Bolivia' }}</span>
            <button
              v-if="!searchStore.isLoadingLocation && useGeolocation"
              @click="openLocationModal"
              class="change-btn"
              title="Cambiar ubicación"
            >
              cambiar
            </button>
          </div>
          <span class="divider">|</span>
          <span class="results-count">{{ resultsCount }} resultado{{ resultsCount !== 1 ? 's' : '' }}</span>
        </div>

        <!-- Botón Limpiar Filtros - Siempre visible -->
        <button
          class="clear-filters-btn"
          :class="{ 'has-filters': hasActiveFilters }"
          :disabled="!hasActiveFilters"
          @click="clearFilters"
        >
          Limpiar filtros
        </button>
      </div>

      <!-- Botón scroll derecha (móvil) -->
      <button
        v-if="showScrollButtons"
        class="scroll-btn scroll-right"
        @click="scrollFilters('right')"
        :disabled="!canScrollRight"
      >
        <va-icon name="chevron_right" size="small" />
      </button>
    </div>

    <!-- Modal para cambiar ubicación -->
    <va-modal
      v-model="showLocationModal"
      title="Cambiar ubicación"
      size="small"
      :hide-default-actions="true"
      class="location-modal"
    >
      <div class="location-modal-content">
        <p class="modal-description">
          Selecciona tu ciudad para ver anuncios relevantes cerca de ti
        </p>

        <va-select
          v-model="selectedCityOption"
          :options="cityOptions"
          label="Ciudad"
          placeholder="Selecciona una ciudad"
          class="city-select"
        >
          <template #prepend>
            <va-icon name="location_city" />
          </template>
        </va-select>

        <div class="modal-actions">
          <va-button
            @click="detectLocationManual"
            preset="secondary"
            :loading="searchStore.isLoadingLocation"
          >
            <va-icon name="my_location" />
            Detectar automáticamente
          </va-button>

          <va-button
            @click="saveLocation"
            color="primary"
            :disabled="!selectedCityOption"
          >
            Guardar
          </va-button>
        </div>
      </div>
    </va-modal>
  </div>
</template>

<script>
import { useSearchStore } from '@/stores/useSearchStore'
import { useToast } from 'vuestic-ui'

export default {
  name: 'TopSearchBar',

  setup() {
    const searchStore = useSearchStore()
    const { init: notify } = useToast()

    return {
      searchStore,
      notify
    }
  },

  props: {
    category: {
      type: String,
      required: true
    },
    categories: {
      type: Array,
      default: () => []
    },
    contractTypes: {
      type: Array,
      default: () => []
    },
    cities: {
      type: Array,
      default: () => []
    },
    resultsCount: {
      type: Number,
      default: 0
    },
    locationInfo: {
      type: Object,
      default: () => null
    }
  },

  emits: ['filter-change', 'search-click'],

  data() {
    return {
      localFilters: {
        search: '',
        city: '',
        category: '',
        contractType: '',
        modality: ''
      },
      sidebarFilters: {
        publishDate: '',
        salaryMin: null,
        salaryMax: null,
        education: ''
      },
      activeDropdown: null,
      // Scroll de filtros
      showScrollButtons: false,
      canScrollLeft: false,
      canScrollRight: false,
      // Modal de ubicación
      showLocationModal: false,
      selectedCityOption: null,
      // Switch de geolocalización
      useGeolocation: true // Activado por defecto
    }
  },

  computed: {
    searchPlaceholder() {
      const placeholders = {
        trabajos: 'Puesto, área laboral o empresa',
        profesionales: 'Profesional, especialidad o servicio',
        gastronomia: 'Restaurante, tipo de comida o plato',
        negocios: 'Negocio, producto o servicio'
      }
      return placeholders[this.category] || 'Buscar...'
    },

    hasActiveFilters() {
      return (
        this.localFilters.search ||
        this.localFilters.city ||
        this.localFilters.category ||
        this.localFilters.contractType ||
        this.localFilters.modality ||
        this.sidebarFilters.publishDate ||
        this.sidebarFilters.salaryMin ||
        this.sidebarFilters.salaryMax ||
        this.sidebarFilters.education
      )
    },

    cityOptions() {
      return [
        { value: '', text: 'Toda Bolivia' },
        { value: 'la-paz', text: 'La Paz' },
        { value: 'cochabamba', text: 'Cochabamba' },
        { value: 'santa-cruz', text: 'Santa Cruz' },
        { value: 'oruro', text: 'Oruro' },
        { value: 'potosi', text: 'Potosí' },
        { value: 'tarija', text: 'Tarija' },
        { value: 'chuquisaca', text: 'Chuquisaca (Sucre)' },
        { value: 'beni', text: 'Beni' },
        { value: 'pando', text: 'Pando' }
      ]
    }
  },

  methods: {
    handleSearch() {
      // Debounce para no emitir en cada tecla
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.emitFilters()
      }, 300)
    },

    handleSearchClick() {
      this.emitFilters()
      this.$emit('search-click')
    },

    toggleDropdown(name) {
      this.activeDropdown = this.activeDropdown === name ? null : name
    },

    emitFilters() {
      this.$emit('filter-change', {
        ...this.localFilters,
        ...this.sidebarFilters
      })
      // Cerrar dropdown después de seleccionar
      this.activeDropdown = null
    },

    clearSearch() {
      this.localFilters.search = ''
      this.emitFilters()
    },

    clearFilters() {
      this.localFilters = {
        search: '',
        city: '',
        category: '',
        contractType: '',
        modality: ''
      }
      this.sidebarFilters = {
        publishDate: '',
        salaryMin: null,
        salaryMax: null,
        education: ''
      }
      this.emitFilters()
    },

    // Métodos para scroll de filtros
    scrollFilters(direction) {
      const container = this.$refs.filtersContainer
      if (!container) return

      const scrollAmount = 200 // Píxeles a desplazar
      const targetScroll = direction === 'left'
        ? container.scrollLeft - scrollAmount
        : container.scrollLeft + scrollAmount

      container.scrollTo({
        left: targetScroll,
        behavior: 'smooth'
      })
    },

    handleFiltersScroll() {
      const container = this.$refs.filtersContainer
      if (!container) return

      this.canScrollLeft = container.scrollLeft > 0
      this.canScrollRight = container.scrollLeft < (container.scrollWidth - container.clientWidth - 5)
    },

    checkScrollButtons() {
      // Verificar si necesitamos mostrar los botones de scroll
      const container = this.$refs.filtersContainer
      if (!container) return

      const needsScroll = container.scrollWidth > container.clientWidth
      this.showScrollButtons = needsScroll && window.innerWidth <= 768

      if (this.showScrollButtons) {
        this.handleFiltersScroll()
      }
    },

    // Métodos del modal de ubicación
    openLocationModal() {
      // Inicializar con la ciudad actual del store
      const currentCity = this.searchStore.selectedCity
      this.selectedCityOption = this.cityOptions.find(c => c.value === currentCity) || this.cityOptions[0]
      this.showLocationModal = true
    },

    async detectLocationManual() {
      const detectedCity = await this.searchStore.resetLocation()

      if (detectedCity) {
        // Actualizar el option seleccionado en el modal
        this.selectedCityOption = this.cityOptions.find(c => c.value === detectedCity) || this.cityOptions[0]

        this.notify({
          message: `Ubicación detectada: ${this.searchStore.displayCity}`,
          color: 'success',
          duration: 3000
        })

        this.showLocationModal = false

        // Actualizar filtros locales y emitir
        this.localFilters.city = detectedCity
        this.emitFilters()
      } else {
        this.notify({
          message: 'No se pudo detectar tu ubicación. Por favor selecciona manualmente.',
          color: 'warning',
          duration: 4000
        })
      }
    },

    saveLocation() {
      if (!this.selectedCityOption) return

      // Actualizar el store con la ciudad seleccionada usando el método correcto
      this.searchStore.setSelectedCity(this.selectedCityOption.value)

      this.notify({
        message: `Ubicación actualizada: ${this.selectedCityOption.text}`,
        color: 'success',
        duration: 2500
      })

      this.showLocationModal = false

      // Actualizar filtros locales y emitir cambios
      this.localFilters.city = this.selectedCityOption.value
      this.emitFilters()
    },

    // Toggle de geolocalización
    handleLocationToggle() {
      // Guardar preferencia en localStorage
      localStorage.setItem('useGeolocation', this.useGeolocation)

      if (this.useGeolocation) {
        // Activar: usar ciudad detectada
        this.localFilters.city = this.searchStore.selectedCity
        this.notify({
          message: `Ubicación activada: ${this.searchStore.displayCity}`,
          color: 'success',
          duration: 2500
        })
      } else {
        // Desactivar: mostrar todo Bolivia
        this.localFilters.city = ''
        this.notify({
          message: 'Mostrando anuncios de todo Bolivia',
          color: 'info',
          duration: 2500
        })
      }

      // Emitir cambios
      this.emitFilters()
    }
  },

  mounted() {
    // Cargar preferencia de geolocalización desde localStorage
    const savedPreference = localStorage.getItem('useGeolocation')
    if (savedPreference !== null) {
      this.useGeolocation = savedPreference === 'true'
    }

    // Si la geolocalización está activada, aplicar el filtro de ciudad
    if (this.useGeolocation && this.searchStore.selectedCity) {
      this.localFilters.city = this.searchStore.selectedCity
    }

    // Cerrar dropdowns al hacer click fuera
    this.closeDropdownListener = (e) => {
      if (!e.target.closest('.filter-dropdown')) {
        this.activeDropdown = null
      }
    }
    document.addEventListener('click', this.closeDropdownListener)

    // Verificar scroll buttons
    this.$nextTick(() => {
      this.checkScrollButtons()
    })

    // Listener para resize
    this.resizeListener = () => {
      this.checkScrollButtons()
    }
    window.addEventListener('resize', this.resizeListener)
  },

  beforeUnmount() {
    // Limpiar listeners
    if (this.closeDropdownListener) {
      document.removeEventListener('click', this.closeDropdownListener)
    }
    if (this.resizeListener) {
      window.removeEventListener('resize', this.resizeListener)
    }
  }
}
</script>

<style scoped>
/* ========== CONTENEDOR PRINCIPAL ========== */
.top-search-bar {
  background: linear-gradient(135deg, #510d89 0%, #4a10ad 100%); /* Tono intermedio entre navbar y púrpura estándar */
  box-shadow: 0 4px 12px rgba(107, 33, 168, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1); /* Sutil separación */
  position: sticky;
  top: 0; /* Sin TopBar, pegado directamente al navbar */
  z-index: 40;
}

/* ========== SECCIÓN DE BÚSQUEDA ========== */
.search-section {
  padding: 1.5rem 1rem;
}

.search-container {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1.5fr auto;
  gap: 0.75rem;
  align-items: center;
}

/* ========== INPUTS DE BÚSQUEDA ========== */
.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.search-input-wrapper:focus-within {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.input-icon {
  padding: 0 1rem;
  color: #7C3AED;
  flex-shrink: 0;
}

.search-input,
.search-select {
  flex: 1;
  border: none;
  outline: none;
  padding: 0.875rem 0.5rem;
  font-size: 0.95rem;
  color: #1F2937;
  background: transparent;
}

.search-input::placeholder {
  color: #9CA3AF;
}

.search-select {
  cursor: pointer;
  padding-right: 1rem;
}

.clear-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #9CA3AF;
  transition: color 0.2s;
}

.clear-btn:hover {
  color: #EF4444;
}

/* ========== BOTÓN CTA ========== */
.search-cta-btn {
  background: rgb(253, 197, 0); /* Amarillo oficial GP */
  color: #1F2937;
  border: none;
  border-radius: 8px;
  padding: 0.875rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3);
  transition: all 0.2s ease;
  white-space: nowrap;
}

.search-cta-btn:hover {
  background: rgb(230, 180, 0);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(253, 197, 0, 0.4);
}

.search-cta-btn:active {
  transform: translateY(0);
}

/* ========== SECCIÓN DE FILTROS ========== */
.filters-section {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.75rem 1rem;
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filters-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
  flex: 1;
}

/* Botones de scroll para móvil */
.scroll-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  transition: all 0.2s;
  flex-shrink: 0;
  z-index: 10;
}

.scroll-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.scroll-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.scroll-btn:active:not(:disabled) {
  transform: scale(0.95);
}

/* Backdrop - oculto por defecto (solo móvil) */
.dropdown-backdrop {
  display: none;
}

/* ========== FILTROS DROPDOWN ========== */
.filter-dropdown {
  position: relative;
}

.filter-btn {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
}

.filter-btn.active {
  background: white;
  color: #7C3AED;
  font-weight: 600;
  border-color: white;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  z-index: 50;
  min-width: 220px;
  animation: slideDown 0.2s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-content {
  padding: 0.5rem;
  max-height: 300px;
  overflow-y: auto;
}

.dropdown-content.scrollable {
  max-height: 250px;
}

.dropdown-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.15s;
  font-size: 0.9rem;
  color: #374151;
}

.dropdown-option:hover {
  background: #F3F4F6;
}

.dropdown-option input[type="radio"] {
  cursor: pointer;
  accent-color: #7C3AED;
}

/* ========== SALARY INPUTS ========== */
.salary-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
}

.salary-input {
  flex: 1;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  padding: 0.5rem;
  font-size: 0.875rem;
  outline: none;
}

.salary-input:focus {
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.separator {
  color: #9CA3AF;
  font-weight: 600;
}

/* ========== BOTÓN LIMPIAR FILTROS ========== */
/* ========== CONTADOR DE RESULTADOS INLINE ========== */
.results-info-inline {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-left: 1rem;
  padding: 0 0.5rem;
}

/* ========== SWITCH DE GEOLOCALIZACIÓN (ESTILO FACEBOOK) ========== */
.location-toggle-wrapper {
  display: flex;
  align-items: center;
}

.location-switch {
  position: relative;
  display: inline-block;
  width: 32px;
  height: 18px;
  cursor: pointer;
}

.switch-checkbox {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 18px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.switch-slider::before {
  content: '';
  position: absolute;
  height: 14px;
  width: 14px;
  left: 2px;
  bottom: 2px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Estado ACTIVADO - Verde esmeralda */
.switch-checkbox:checked + .switch-slider {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
}

.switch-checkbox:checked + .switch-slider::before {
  transform: translateX(14px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
}

/* Hover */
.location-switch:hover .switch-slider {
  background: rgba(255, 255, 255, 0.4);
}

.location-switch:hover .switch-checkbox:checked + .switch-slider {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  box-shadow: 0 2px 10px rgba(16, 185, 129, 0.5);
}

/* Animación de pulso cuando se activa */
.switch-checkbox:checked + .switch-slider::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 18px;
  background: rgba(16, 185, 129, 0.3);
  animation: pulse-green 0.6s ease-out;
}

@keyframes pulse-green {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.4);
    opacity: 0;
  }
}

/* Ubicación - Estilo TopBar */
.location-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: white;
}

.location-prefix {
  margin: 0;
  font-weight: 500;
  opacity: 0.9;
}

.location-icon {
  color: rgb(253, 197, 0);
  transition: transform 0.3s ease;
}

.location-icon.spinning {
  animation: spin 1s linear infinite;
}

.location-text {
  font-weight: 600;
  color: white;
}

.change-btn {
  background: none;
  border: none;
  color: rgb(253, 197, 0);
  cursor: pointer;
  font-size: 0.85rem;
  text-decoration: underline;
  padding: 0;
  transition: all 0.2s;
  font-weight: 500;
}

.change-btn:hover {
  color: rgb(230, 180, 0);
  text-decoration: none;
}

.divider {
  color: rgba(255, 255, 255, 0.4);
  font-weight: 300;
  font-size: 1.1rem;
}

.results-count {
  font-size: 0.95rem;
  color: white;
  font-weight: 600;
  white-space: nowrap;
}

/* Modal de ubicación */
.location-modal-content {
  padding: 1rem 0;
}

.modal-description {
  color: #6B7280;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.city-select {
  margin-bottom: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.spinning-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.clear-filters-btn {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: not-allowed;
  transition: all 0.2s;
  margin-left: 0.5rem;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  opacity: 0.6;
}

/* Estado activo cuando hay filtros */
.clear-filters-btn.has-filters {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.6);
  cursor: pointer;
  opacity: 1;
}

.clear-filters-btn.has-filters:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.clear-filters-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .search-container {
    grid-template-columns: 1fr 1fr;
  }

  .search-cta-btn {
    grid-column: 1 / -1;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .top-search-bar {
    top: 0;
  }

  .search-section {
    padding: 1rem 0.75rem;
  }

  .search-container {
    display: flex;
    gap: 0.5rem;
  }

  /* Ocultar input de búsqueda en móvil */
  .search-input-wrapper.primary {
    display: none;
  }

  /* Ciudad ocupa todo el ancho disponible */
  .search-input-wrapper.secondary {
    flex: 1;
  }

  .btn-text {
    display: none;
  }

  .search-cta-btn {
    padding: 0.75rem;
    justify-content: center;
  }

  .filters-section {
    padding: 0.5rem 0.25rem;
    gap: 0.5rem;
  }

  /* Mostrar botones de scroll en móvil */
  .scroll-btn {
    display: flex;
    width: 32px;
    height: 32px;
    font-size: 0.9rem;
  }

  .filters-container {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 0.25rem;
    -webkit-overflow-scrolling: touch;

    /* Ocultar scrollbar pero mantener funcionalidad */
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE and Edge */
  }

  /* Ocultar scrollbar en Chrome, Safari y Opera */
  .filters-container::-webkit-scrollbar {
    display: none;
  }

  .filter-btn {
    font-size: 0.85rem;
    padding: 0.4rem 0.75rem;
  }

  /* Dropdown en móvil - posición fija centrado */
  .dropdown-menu {
    position: fixed;
    left: 1rem;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    max-width: none;
    width: auto;
    z-index: 1000;
    max-height: 50vh;
    overflow-y: auto;
  }

  .dropdown-content {
    max-height: none;
    padding: 1rem;
  }

  /* Ajustar inputs de salario en móvil para que sean verticales */
  .salary-inputs {
    flex-direction: column !important;
    gap: 0.75rem !important;
  }

  .salary-input {
    width: 100% !important;
  }

  .separator {
    display: none !important;
  }

  /* Backdrop oscuro para dropdowns en móvil */
  .dropdown-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: block;
    animation: fadeIn 0.2s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  /* Compactar ubicación en móvil */
  .location-prefix {
    display: none;
  }

  .location-display {
    font-size: 0.8rem;
    gap: 0.375rem;
  }

  .location-text {
    font-size: 0.85rem;
  }

  .change-btn {
    font-size: 0.75rem;
  }

  .results-count {
    font-size: 0.85rem;
  }

  .divider {
    font-size: 1rem;
    margin: 0 0.5rem;
  }

  /* Switch más pequeño en móvil */
  .location-switch {
    width: 28px;
    height: 16px;
  }

  .switch-slider::before {
    height: 12px;
    width: 12px;
  }

  .switch-checkbox:checked + .switch-slider::before {
    transform: translateX(12px);
  }
}
</style>
