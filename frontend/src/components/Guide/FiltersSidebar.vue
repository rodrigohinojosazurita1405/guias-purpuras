<template>
  <!-- 
    ═══════════════════════════════════════════════════════════
    FiltersSidebar.vue - Filtros laterales
    ═══════════════════════════════════════════════════════════
    
    Propósito: Sidebar con filtros para GuideView
    Props: subcategories, cities
    Emits: filter-change (cuando se aplican filtros)
  -->
  <aside class="filters-sidebar">
    <!-- Header -->
    <div class="filter-header">
      <h3>Filtros</h3>
      <button class="clear-filters" @click="clearAll">Limpiar</button>
    </div>

    <!-- Filtro: Subcategorías -->
    <div class="filter-group">
      <h4><VaIcon name="category" size="small" /> Subcategoría</h4>
      <div class="checkbox-group">
        <label v-for="sub in subcategories" :key="sub">
          <input type="checkbox" :value="sub" v-model="selectedSubcategories" />
          <span>{{ sub }}</span>
        </label>
      </div>
    </div>

    <!-- Filtro: Ciudad -->
    <div class="filter-group">
      <h4><VaIcon name="location_on" size="small" /> Ciudad</h4>
      <select v-model="selectedCity" class="filter-select">
        <option value="">Todas</option>
        <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
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

    <!-- Botón Aplicar -->
    <VaButton block color="var(--color-purple-dark)" @click="applyFilters">
      Aplicar Filtros
    </VaButton>
  </aside>
</template>

<script>
/**
 * FiltersSidebar Component
 * 
 * Props:
 * - subcategories: Array de subcategorías disponibles
 * - cities: Array de ciudades
 * 
 * Emits:
 * - filter-change: { subcategories, city, verifiedOnly }
 */

export default {
  name: 'FiltersSidebar',
  props: {
    subcategories: {
      type: Array,
      required: true
    },
    cities: {
      type: Array,
      required: true
    }
  },
  emits: ['filter-change'],
  data() {
    return {
      selectedSubcategories: [],
      selectedCity: '',
      verifiedOnly: false
    }
  },
  methods: {
    applyFilters() {
      this.$emit('filter-change', {
        subcategories: this.selectedSubcategories,
        city: this.selectedCity,
        verifiedOnly: this.verifiedOnly
      })
    },
    clearAll() {
      this.selectedSubcategories = []
      this.selectedCity = ''
      this.verifiedOnly = false
      this.applyFilters()
    }
  }
}
</script>

<style scoped>
.filters-sidebar {
  background: var(--color-gray-50);
  border-radius: 12px;
  padding: 1.5rem;
  height: fit-content;
  position: sticky;
  top: 100px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--color-gray-200);
}

.filter-header h3 {
  font-size: 1.2rem;
  margin: 0;
}

.clear-filters {
  background: none;
  border: none;
  color: var(--color-danger);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-group h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  margin-bottom: 0.75rem;
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
  color: var(--color-gray-600);
  font-size: 0.9rem;
}

input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: var(--color-purple-dark);
}

.filter-select {
  width: 100%;
  padding: 0.5rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 6px;
  outline: none;
}
</style>