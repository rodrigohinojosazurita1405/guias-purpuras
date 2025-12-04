<template>
  <div class="filters-wrapper">
    <!--
      ═══════════════════════════════════════════════════════════
      FiltersSidebar.vue - Filtros laterales
      ═══════════════════════════════════════════════════════════

      Propósito: Sidebar con filtros para GuideView
      Props: subcategories, cities, showMobile
      Emits: filter-change (cuando se aplican filtros), close (para cerrar en móvil)
    -->

    <!-- Overlay en móvil -->
    <div v-if="showMobile" class="mobile-overlay" @click="$emit('close')"></div>

    <aside class="filters-sidebar" :class="{ 'mobile-open': showMobile }">
      <!-- Header -->
      <div class="filter-header">
        <h3>Filtros</h3>
        <div class="header-actions">
          <button class="clear-filters" @click="clearAll">Limpiar</button>
          <button class="close-mobile" @click="$emit('close')">
            <VaIcon name="close" />
          </button>
        </div>
      </div>

    <!-- Filtros principales en móvil (categoría, tipo empleo, ciudad) -->
    <div class="mobile-main-filters">
      <!-- Categoría (solo trabajos) -->
      <div v-if="category === 'trabajos'" class="filter-group">
        <h4><VaIcon name="category" size="small" /> Categoría</h4>
        <select v-model="selectedCategory" class="filter-select">
          <option value="">Todas las categorías</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>

      <!-- Tipo de empleo (solo trabajos) -->
      <div v-if="category === 'trabajos'" class="filter-group">
        <h4><VaIcon name="work" size="small" /> Tipo de empleo</h4>
        <select v-model="selectedContractType" class="filter-select">
          <option value="">Todos los tipos</option>
          <option v-for="ct in contractTypes" :key="ct" :value="ct">{{ ct }}</option>
        </select>
      </div>

      <!-- Subcategoría (otras categorías) -->
      <div v-if="category !== 'trabajos'" class="filter-group">
        <h4><VaIcon name="category" size="small" /> {{ subcategoryLabel }}</h4>
        <select v-model="selectedSubcategory" class="filter-select">
          <option value="">{{ subcategoryPlaceholder }}</option>
          <option v-for="sub in subcategories" :key="sub" :value="sub">{{ sub }}</option>
        </select>
      </div>

      <!-- Ciudad -->
      <div class="filter-group">
        <h4><VaIcon name="place" size="small" /> Ciudad</h4>
        <select v-model="selectedCity" class="filter-select">
          <option value="">Todas las ciudades</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>
    </div>

    <!-- Filtro: Fecha de Publicación -->
    <div class="filter-group">
      <h4><VaIcon name="schedule" size="small" /> Fecha de Publicación</h4>
      <select v-model="publishDate" class="filter-select">
        <option value="">Cualquier fecha</option>
        <option value="24h">Últimas 24 horas</option>
        <option value="7d">Última semana</option>
        <option value="30d">Último mes</option>
      </select>
    </div>

    <!-- Filtro: Rango Salarial -->
    <div class="filter-group">
      <h4><VaIcon name="payments" size="small" /> Rango Salarial (Bs)</h4>
      <div class="salary-inputs">
        <input
          type="number"
          v-model.number="salaryMin"
          placeholder="Mínimo"
          class="filter-input"
          min="0"
        />
        <span class="range-separator">-</span>
        <input
          type="number"
          v-model.number="salaryMax"
          placeholder="Máximo"
          class="filter-input"
          min="0"
        />
      </div>
    </div>

    <!-- Filtro: Años de Experiencia -->
    <div class="filter-group">
      <h4><VaIcon name="work_history" size="small" /> Años de Experiencia</h4>
      <select v-model="experienceYears" class="filter-select">
        <option value="">Cualquier experiencia</option>
        <option value="0-1">Sin experiencia / Junior (0-1 años)</option>
        <option value="1-3">Semi-Senior (1-3 años)</option>
        <option value="3-5">Senior (3-5 años)</option>
        <option value="5+">Experto (5+ años)</option>
      </select>
    </div>

    <!-- Filtro: Solo Verificados -->
    <div class="filter-group">
      <h4><VaIcon name="verified" size="small" /> Estado</h4>
      <label class="checkbox-single">
        <input type="checkbox" v-model="verifiedOnly" />
        <span>Solo Verificados</span>
      </label>
    </div>

      <!-- Botón Aplicar - ✅ COLOR CORREGIDO -->
      <VaButton block color="background: linear-gradient(135deg, #7c3aed, #6d28d9);" @click="applyFilters">
        Aplicar Filtros
      </VaButton>
    </aside>
  </div>
</template>

<script>
/**
 * FiltersSidebar Component
 *
 * Props:
 * - showMobile: Boolean para mostrar/ocultar en móvil
 * - category: Categoría actual (trabajos, profesionales, etc.)
 * - categories, contractTypes, subcategories, cities: Opciones para filtros
 *
 * Emits:
 * - filter-change: Todos los filtros seleccionados
 * - close: Para cerrar el sidebar en móvil
 */

export default {
  name: 'FiltersSidebar',
  props: {
    showMobile: {
      type: Boolean,
      default: false
    },
    category: {
      type: String,
      default: 'trabajos'
    },
    categories: {
      type: Array,
      default: () => []
    },
    contractTypes: {
      type: Array,
      default: () => []
    },
    subcategories: {
      type: Array,
      default: () => []
    },
    cities: {
      type: Array,
      default: () => []
    },
    subcategoryLabel: {
      type: String,
      default: 'Subcategoría'
    },
    subcategoryPlaceholder: {
      type: String,
      default: 'Todas'
    }
  },
  emits: ['filter-change', 'close'],
  data() {
    return {
      // Filtros principales (móvil)
      selectedCategory: '',
      selectedContractType: '',
      selectedSubcategory: '',
      selectedCity: '',
      // Filtros secundarios
      publishDate: '',
      salaryMin: null,
      salaryMax: null,
      experienceYears: '',
      verifiedOnly: false
    }
  },
  methods: {
    applyFilters() {
      this.$emit('filter-change', {
        // Filtros principales
        category: this.selectedCategory,
        contractType: this.selectedContractType,
        subcategory: this.selectedSubcategory,
        city: this.selectedCity,
        // Filtros secundarios
        publishDate: this.publishDate,
        salaryMin: this.salaryMin,
        salaryMax: this.salaryMax,
        experienceYears: this.experienceYears,
        verifiedOnly: this.verifiedOnly
      })
    },
    clearAll() {
      // Limpiar filtros principales
      this.selectedCategory = ''
      this.selectedContractType = ''
      this.selectedSubcategory = ''
      this.selectedCity = ''
      // Limpiar filtros secundarios
      this.publishDate = ''
      this.salaryMin = null
      this.salaryMax = null
      this.experienceYears = ''
      this.verifiedOnly = false
      this.applyFilters()
    }
  }
}
</script>

<style scoped>
.filters-wrapper {
  position: relative;
}

.filters-sidebar {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  height: fit-content;
  position: sticky;
  top: 1rem;
  min-width: 250px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.filter-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.clear-filters {
  background: none;
  border: none;
  color: #5C0099;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.clear-filters:hover {
  background: #f5f5f5;
}

.close-mobile {
  display: none;
  background: none;
  border: none;
  color: #333;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-mobile:hover {
  background: #f5f5f5;
}

/* Filtros principales - solo en móvil */
.mobile-main-filters {
  display: none;
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-group h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.75rem 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #555;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-group label,
.checkbox-single {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem 0;
  font-size: 0.9rem;
  color: #666;
}

.checkbox-group input[type="checkbox"],
.checkbox-single input[type="checkbox"] {
  margin: 0;
  width: 16px;
  height: 16px;
  accent-color: #5C0099;
}

.filter-select,
.filter-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
}

.filter-select:focus,
.filter-input:focus {
  outline: none;
  border-color: #5C0099;
  box-shadow: 0 0 0 2px rgba(92, 0, 153, 0.1);
}

/* Rango salarial */
.salary-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.salary-inputs .filter-input {
  flex: 1;
}

.range-separator {
  color: #999;
  font-weight: 600;
}

/* Overlay para móvil */
.mobile-overlay {
  display: none;
}

@media (max-width: 768px) {
  /* Mostrar filtros principales en móvil */
  .mobile-main-filters {
    display: block;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #E5E7EB;
  }

  /* Ocultar sidebar por defecto en móvil */
  .filters-sidebar {
    position: fixed;
    top: 0;
    left: -100%;
    bottom: 0;
    width: 85%;
    max-width: 320px;
    z-index: 1001;
    border-radius: 0;
    min-width: auto;
    transition: left 0.3s ease-in-out;
    overflow-y: auto;
    box-shadow: 2px 0 16px rgba(0, 0, 0, 0.2);
  }

  /* Mostrar sidebar cuando está abierto */
  .filters-sidebar.mobile-open {
    left: 0;
  }

  /* Overlay oscuro */
  .mobile-overlay {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    animation: fadeIn 0.3s ease-in-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  /* Mostrar botón de cerrar en móvil */
  .close-mobile {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>