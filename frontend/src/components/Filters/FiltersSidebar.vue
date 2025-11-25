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

    <!-- Botón Aplicar - ✅ COLOR CORREGIDO -->
    <VaButton block color="background: linear-gradient(135deg, #7c3aed, #6d28d9);" @click="applyFilters">
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

.filter-select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
}

.filter-select:focus {
  outline: none;
  border-color: #5C0099;
  box-shadow: 0 0 0 2px rgba(92, 0, 153, 0.1);
}

@media (max-width: 768px) {
  .filters-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    border-radius: 0;
    min-width: auto;
  }
}
</style>