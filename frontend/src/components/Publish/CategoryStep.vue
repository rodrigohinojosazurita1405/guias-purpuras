<!-- frontend/src/components/Publish/CategoryStep.vue -->
<template>
  <div class="category-step">
    
    <!-- ========================================
         NIVEL 1: SELECCIÓN DE PILAR (4 CARDS)
         ======================================== -->
    <div v-if="currentLevel === 1" class="level-container">
      <h2 class="step-title">
        <va-icon name="category" color="purple" size="1.8rem" />
        Selecciona la Categoría
      </h2>

      <p class="step-description">
        Elige dónde aparecerá tu anuncio para que las personas correctas lo encuentren
      </p>

      <!-- Categorías con Cards Visuales -->
      <div class="categories-grid">
        <div 
          v-for="cat in categories" 
          :key="cat.id"
          class="category-card"
          :class="{ selected: localData.category === cat.id }"
          @click="selectCategory(cat.id)"
        >
          <div class="card-icon">
            <va-icon :name="cat.icon" size="2.5rem" />
          </div>
          <h3 class="card-title">{{ cat.name }}</h3>
          <p class="card-description">{{ cat.description }}</p>
          <div class="card-check">
            <va-icon name="check_circle" size="1.5rem" />
          </div>
        </div>
      </div>

      <span v-if="errors.category" class="error-message">
        <va-icon name="error" size="small" />
        {{ errors.category }}
      </span>
    </div>

    <!-- ========================================
         NIVEL 2: SELECCIÓN DE SUBCATEGORÍA
         ======================================== -->
    <transition name="slide-fade">
      <div v-if="currentLevel === 2" class="level-container">
        
        <!-- Header con botón volver -->
        <div class="level-header">
          <button class="back-btn" @click="goBack">
            <va-icon name="arrow_back" />
            Volver
          </button>
          <div class="header-content">
            <h2 class="step-title">
              <va-icon :name="selectedCategoryIcon" color="purple" size="1.8rem" />
              ¿Qué tipo de {{ selectedCategoryName }}?
            </h2>
            <p class="step-description">
              Busca o selecciona la subcategoría que mejor describa tu servicio
            </p>
          </div>
        </div>

        <!-- BARRA DE BÚSQUEDA -->
        <div class="search-container">
          <div class="search-bar">
            <va-icon name="search" class="search-icon" />
            <input
              v-model="searchQuery"
              type="text"
              class="search-input"
              :placeholder="`Buscar en ${selectedCategoryName}...`"
              @input="handleSearch"
            />
            <button 
              v-if="searchQuery" 
              class="clear-btn"
              @click="clearSearch"
            >
              <va-icon name="close" size="small" />
            </button>
          </div>
        </div>

        <!-- RESULTADOS DE BÚSQUEDA -->
        <div v-if="searchQuery && searchResults.length > 0" class="search-results">
          <h3 class="results-title">
            <va-icon name="search" size="small" />
            Resultados de búsqueda ({{ searchResults.length }})
          </h3>
          <div class="results-grid">
            <button
              v-for="sub in searchResults"
              :key="sub"
              class="result-item"
              @click="selectSubcategory(sub)"
            >
              <va-icon name="label" size="small" />
              <span>{{ sub }}</span>
              <va-icon name="arrow_forward" size="small" class="arrow" />
            </button>
          </div>
        </div>

        <!-- NO HAY RESULTADOS -->
        <div v-else-if="searchQuery && searchResults.length === 0" class="no-results">
          <va-icon name="search_off" size="3rem" color="#9CA3AF" />
          <p>No se encontraron resultados para "<strong>{{ searchQuery }}</strong>"</p>
          <button class="link-btn" @click="clearSearch">Ver todas las opciones</button>
        </div>

        <!-- CONTENIDO NORMAL (cuando NO hay búsqueda) -->
        <div v-else>
          
          <!-- DESTACADAS (9 cards) -->
          <div class="featured-section">
            <h3 class="section-title">
              <va-icon name="star" color="#FDC500" size="1.5rem" />
              Más Populares
            </h3>
            <div class="featured-grid">
              <div
                v-for="sub in featuredSubcategories"
                :key="sub"
                class="featured-card"
                @click="selectSubcategory(sub)"
              >
                <div class="featured-icon">
                  <va-icon name="trending_up" size="1.5rem" />
                </div>
                <span class="featured-name">{{ sub }}</span>
                <va-icon name="arrow_forward" size="small" class="featured-arrow" />
              </div>
            </div>
          </div>

          <!-- EXPLORAR POR GRUPO -->
          <div class="groups-section">
            <h3 class="section-title">
              <va-icon name="folder_open" color="purple" size="1.5rem" />
              Explorar por Categoría
            </h3>

            <!-- Tabs de grupos -->
            <div class="groups-tabs">
              <button
                v-for="group in categoryGroups"
                :key="group.id"
                class="group-tab"
                :class="{ active: activeGroup === group.id }"
                @click="selectGroup(group.id)"
              >
                <va-icon :name="group.icon" size="1.2rem" />
                <span>{{ group.name }}</span>
                <span class="count">({{ group.items.length }})</span>
              </button>
            </div>

            <!-- Items del grupo activo -->
            <transition name="fade">
              <div v-if="activeGroup" class="group-items">
                <button
                  v-for="item in activeGroupItems"
                  :key="item"
                  class="group-item"
                  @click="selectSubcategory(item)"
                >
                  <va-icon name="radio_button_unchecked" size="small" />
                  <span>{{ item }}</span>
                  <va-icon name="arrow_forward" size="small" class="item-arrow" />
                </button>
              </div>
            </transition>
          </div>

          <!-- BOTÓN VER TODAS -->
          <div class="view-all-section">
            <button class="view-all-btn" @click="showAllModal = true">
              <va-icon name="list" />
              Ver todas las subcategorías ({{ allSubcategoriesCount }})
            </button>
          </div>
        </div>

        <span v-if="errors.subcategory" class="error-message">
          <va-icon name="error" size="small" />
          {{ errors.subcategory }}
        </span>
      </div>
    </transition>

    <!-- ========================================
         NIVEL 3: UBICACIÓN (SOLO CIUDAD)
         ======================================== -->
    <transition name="slide-fade">
      <div v-if="currentLevel === 3" class="level-container">
        
        <!-- Header con botón volver -->
        <div class="level-header">
          <button class="back-btn" @click="goBack">
            <va-icon name="arrow_back" />
            Volver
          </button>
          <div class="header-content">
            <h2 class="step-title">
              <va-icon name="location_city" color="purple" size="1.8rem" />
              ¿Dónde te encuentras?
            </h2>
            <p class="step-description">
              Selecciona tu ciudad para que los clientes puedan encontrarte
            </p>
          </div>
        </div>

        <!-- Selección de ciudad -->
        <div class="location-section">
          <div class="city-selector">
            <label class="form-label required">
              <va-icon name="location_city" size="small" />
              Ciudad
            </label>
            <select 
              v-model="localData.city" 
              class="form-select"
              required
            >
              <option value="">Selecciona tu ciudad</option>
              <option 
                v-for="city in cities" 
                :key="city.id"
                :value="city.id"
              >
                {{ city.name }}
              </option>
            </select>
            <span v-if="errors.city" class="error-message">
              <va-icon name="error" size="small" />
              {{ errors.city }}
            </span>
          </div>

          <!-- Info sobre GPS -->
          <div class="location-note">
            <va-icon name="info" size="small" color="#5C0099" />
            <p>Podrás agregar tu ubicación GPS exacta en el siguiente paso</p>
          </div>
        </div>
      </div>
    </transition>

    <!-- ========================================
         MODAL: VER TODAS LAS SUBCATEGORÍAS
         ======================================== -->
    <transition name="modal-fade">
      <div v-if="showAllModal" class="modal-overlay" @click="showAllModal = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>
              <va-icon name="list" />
              Todas las subcategorías
            </h3>
            <button class="close-btn" @click="showAllModal = false">
              <va-icon name="close" />
            </button>
          </div>
          
          <div class="modal-search">
            <va-icon name="search" class="search-icon" />
            <input
              v-model="modalSearchQuery"
              type="text"
              placeholder="Buscar..."
              class="modal-search-input"
            />
          </div>

          <div class="modal-body">
            <div class="alphabetical-list">
              <button
                v-for="sub in filteredAllSubcategories"
                :key="sub"
                class="list-item"
                @click="selectSubcategoryFromModal(sub)"
              >
                <va-icon name="label" size="small" />
                <span>{{ sub }}</span>
                <va-icon name="arrow_forward" size="small" />
              </button>
            </div>
            
            <div v-if="filteredAllSubcategories.length === 0" class="no-results-modal">
              <va-icon name="search_off" size="2rem" />
              <p>No se encontraron resultados</p>
            </div>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

// ========== STATE ==========
const currentLevel = ref(1)
const searchQuery = ref('')
const activeGroup = ref('')
const showAllModal = ref(false)
const modalSearchQuery = ref('')

const localData = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const errors = ref({
  category: '',
  subcategory: '',
  city: ''
})

// ========== DATA: CATEGORÍAS (4 PILARES) ==========
const categories = [
  { 
    id: 'profesionales', 
    name: 'Profesionales', 
    icon: 'work',
    description: 'Abogados, médicos, arquitectos'
  },
  { 
    id: 'gastronomia', 
    name: 'Gastronomía', 
    icon: 'restaurant',
    description: 'Restaurantes, cafés y comida'
  },
  { 
    id: 'trabajos', 
    name: 'Trabajos', 
    icon: 'badge',
    description: 'Ofertas laborales y empleos'
  },
  { 
    id: 'negocios', 
    name: 'Negocios', 
    icon: 'store',
    description: 'Tiendas, empresas y comercios'
  }
]

// ========== DATA: SUBCATEGORÍAS CON GRUPOS ==========
const subcategoriesData = {
  profesionales: {
    featured: [
      'Médico', 'Abogado', 'Arquitecto', 'Ingeniero Civil', 
      'Contador', 'Psicólogo', 'Dentista'
    ],
    groups: {
      salud: {
        name: 'Salud',
        icon: 'local_hospital',
        items: ['Médico', 'Dentista', 'Psicólogo', 'Nutricionista', 'Fisioterapeuta', 'Enfermera', 'Veterinario','Neurologo']
      },
      legal: {
        name: 'Legal',
        icon: 'gavel',
        items: ['Abogado', 'Notario', 'Asesor Legal', 'Gestor Trámites']
      },
      construccion: {
        name: 'Construcción',
        icon: 'construction',
        items: ['Arquitecto', 'Ingeniero Civil', 'Maestro Construcción', 'Topógrafo']
      },   
      tecnologia: {
        name: 'Tecnología',
        icon: 'computer',
        items: ['Desarrollador', 'Diseñador Gráfico', 'Técnico Computación', 'Fotógrafo', 'Videógrafo']
      },
      otros: {
        name: 'Otros',
        icon: 'more_horiz',
        items: ['Contador', 'Consultor', 'Coach', 'Profesor Particular', 'Traductor']
      }
    }
  },
  gastronomia: {
    featured: [
      'Restaurante', 'Café', 'Comida Rápida', 'Panadería',
      'Pizzería', 'Heladería', 'Bar', 'Comida Típica', 'Buffet'
    ],
    groups: {
      comida_rapida: {
        name: 'Comida Rápida',
        icon: 'fastfood',
        items: ['Hamburguesas', 'Hot Dogs', 'Salteñas', 'Empanadas', 'Sandwiches']
      },
      restaurantes: {
        name: 'Restaurantes',
        icon: 'restaurant',
        items: ['Restaurante', 'Buffet', 'Comida Típica', 'Comida Internacional', 'Comida China', 'Comida Mexicana']
      },
      cafes_postres: {
        name: 'Cafés y Postres',
        icon: 'local_cafe',
        items: ['Café', 'Cafetería', 'Heladería', 'Pastelería', 'Repostería']
      },
      panaderia: {
        name: 'Panadería',
        icon: 'bakery_dining',
        items: ['Panadería', 'Pastelería', 'Repostería']
      },
      bebidas: {
        name: 'Bares y Bebidas',
        icon: 'local_bar',
        items: ['Bar', 'Pub', 'Discoteca', 'Karaoke']
      },
      especializado: {
        name: 'Especializado',
        icon: 'dinner_dining',
        items: ['Pizzería', 'Sushi', 'Parrillada', 'Catering', 'Food Truck']
      }
    }
  },
  trabajos: {
    featured: [
      'Tiempo Completo', 'Medio Tiempo', 'Por Proyecto',
      'Remoto', 'Pasantía', 'Freelance'
    ],
    groups: {
      tipo: {
        name: 'Por Tipo',
        icon: 'work',
        items: ['Tiempo Completo', 'Medio Tiempo', 'Por Proyecto', 'Temporal', 'Permanente']
      },
      modalidad: {
        name: 'Por Modalidad',
        icon: 'laptop',
        items: ['Presencial', 'Remoto', 'Híbrido']
      },
      nivel: {
        name: 'Por Nivel',
        icon: 'trending_up',
        items: ['Pasantía', 'Junior', 'Senior', 'Gerencial']
      },
      contrato: {
        name: 'Por Contrato',
        icon: 'description',
        items: ['Planilla', 'Freelance', 'Consultoría', 'Contrato']
      }
    }
  },
  negocios: {
    featured: [
      'Tecnología', 'Moda y Ropa', 'Belleza y Salud',
      'Hogar y Decoración', 'Mascotas', 'Librería',
      'Ferretería', 'Farmacia', 'Supermercado'
    ],
    groups: {
      tecnologia: {
        name: 'Tecnología',
        icon: 'devices',
        items: ['Celulares', 'Computadoras', 'Electrónica', 'Accesorios Tech']
      },
      moda: {
        name: 'Moda y Ropa',
        icon: 'checkroom',
        items: ['Ropa', 'Calzado', 'Accesorios', 'Joyería', 'Boutique']
      },
      belleza: {
        name: 'Belleza y Salud',
        icon: 'spa',
        items: ['Salón de Belleza', 'Barbería', 'Spa', 'Farmacia', 'Óptica']
      },
      hogar: {
        name: 'Hogar',
        icon: 'home',
        items: ['Muebles', 'Decoración', 'Ferretería', 'Electrodomésticos']
      },
      alimentos: {
        name: 'Alimentos',
        icon: 'shopping_basket',
        items: ['Supermercado', 'Minimarket', 'Frutas y Verduras', 'Carnicería']
      },
      otros: {
        name: 'Otros',
        icon: 'store',
        items: ['Librería', 'Juguetería', 'Mascotas', 'Floristería', 'Imprenta']
      }
    }
  }
}

// ========== DATA: CIUDADES ==========
const cities = [
  { id: 'cochabamba', name: 'Cochabamba' },
  { id: 'la-paz', name: 'La Paz' },
  { id: 'santa-cruz', name: 'Santa Cruz' },
  { id: 'sucre', name: 'Sucre' },
  { id: 'tarija', name: 'Tarija' },
  { id: 'potosi', name: 'Potosí' },
  { id: 'oruro', name: 'Oruro' },
  { id: 'beni', name: 'Beni' },
  { id: 'pando', name: 'Pando' }
]

// ========== COMPUTED ==========
const selectedCategoryName = computed(() => {
  const cat = categories.find(c => c.id === localData.value.category)
  return cat ? cat.name : ''
})

const selectedCategoryIcon = computed(() => {
  const cat = categories.find(c => c.id === localData.value.category)
  return cat ? cat.icon : 'category'
})

const currentCategoryData = computed(() => {
  return subcategoriesData[localData.value.category] || { featured: [], groups: {} }
})

const featuredSubcategories = computed(() => {
  return currentCategoryData.value.featured || []
})

const categoryGroups = computed(() => {
  const groups = currentCategoryData.value.groups || {}
  return Object.keys(groups).map(key => ({
    id: key,
    ...groups[key]
  }))
})

const activeGroupItems = computed(() => {
  if (!activeGroup.value) return []
  const groups = currentCategoryData.value.groups || {}
  return groups[activeGroup.value]?.items || []
})

const allSubcategoriesFlat = computed(() => {
  const groups = currentCategoryData.value.groups || {}
  const all = []
  Object.values(groups).forEach(group => {
    all.push(...group.items)
  })
  return [...new Set(all)].sort()
})

const allSubcategoriesCount = computed(() => {
  return allSubcategoriesFlat.value.length
})

// Búsqueda en tiempo real
const searchResults = computed(() => {
  if (!searchQuery.value || searchQuery.value.length < 2) return []
  
  const query = searchQuery.value.toLowerCase()
  return allSubcategoriesFlat.value.filter(sub => 
    sub.toLowerCase().includes(query)
  )
})

// Búsqueda en modal
const filteredAllSubcategories = computed(() => {
  if (!modalSearchQuery.value) return allSubcategoriesFlat.value
  
  const query = modalSearchQuery.value.toLowerCase()
  return allSubcategoriesFlat.value.filter(sub =>
    sub.toLowerCase().includes(query)
  )
})

// ========== METHODS ==========

// Debounce para búsqueda
let searchTimeout = null
const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    // La búsqueda es reactiva via computed
  }, 300)
}

const clearSearch = () => {
  searchQuery.value = ''
}

const selectCategory = (categoryId) => {
  localData.value.category = categoryId
  localData.value.subcategory = ''
  errors.value.category = ''
  currentLevel.value = 2
  
  // Auto-seleccionar el primer grupo
  const groups = subcategoriesData[categoryId]?.groups || {}
  const firstGroupId = Object.keys(groups)[0]
  if (firstGroupId) {
    activeGroup.value = firstGroupId
  }
}

const selectGroup = (groupId) => {
  activeGroup.value = groupId
}

const selectSubcategory = (subcategory) => {
  localData.value.subcategory = subcategory
  errors.value.subcategory = ''
  currentLevel.value = 3
  searchQuery.value = ''
}

const selectSubcategoryFromModal = (subcategory) => {
  selectSubcategory(subcategory)
  showAllModal.value = false
  modalSearchQuery.value = ''
}

const goBack = () => {
  if (currentLevel.value === 2) {
    currentLevel.value = 1
    localData.value.category = ''
    localData.value.subcategory = ''
    searchQuery.value = ''
    activeGroup.value = ''
  } else if (currentLevel.value === 3) {
    currentLevel.value = 2
    localData.value.subcategory = ''
    localData.value.city = ''
  }
}

// Validación
const validate = () => {
  errors.value = {
    category: '',
    subcategory: '',
    city: ''
  }

  if (!localData.value.category) {
    errors.value.category = 'Debes seleccionar una categoría'
    currentLevel.value = 1
    return false
  }

  if (!localData.value.subcategory) {
    errors.value.subcategory = 'Debes seleccionar una subcategoría'
    currentLevel.value = 2
    return false
  }

  if (!localData.value.city) {
    errors.value.city = 'Debes seleccionar una ciudad'
    currentLevel.value = 3
    return false
  }

  return true
}

// Watch para limpiar cuando cambia categoría
watch(() => localData.value.category, () => {
  localData.value.subcategory = ''
  searchQuery.value = ''
})

defineExpose({ validate })
</script>

<style scoped>
/* ========== GENERAL ========== */
.category-step {
  padding: 1rem 0;
}

.level-container {
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ========== TRANSITIONS ========== */
.slide-fade-enter-active {
  transition: all 0.4s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from {
  transform: translateX(20px);
  opacity: 0;
}
.slide-fade-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* ========== LEVEL HEADER ========== */
.level-header {
  margin-bottom: 2rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  color: #6B7280;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}

.back-btn:hover {
  border-color: #5C0099;
  color: #5C0099;
  transform: translateX(-4px);
}

.header-content {
  text-align: center;
}

/* ========== TITLES ========== */
.step-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1F2937;
  margin-bottom: 0.75rem;
}

.step-description {
  font-size: 1rem;
  color: #6B7280;
  line-height: 1.5;
  text-align: center;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1F2937;
  margin-bottom: 1.5rem;
}

/* ========== NIVEL 1: CATEGORÍAS ========== */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.category-card {
  position: relative;
  background: white;
  border: 3px solid #E5E7EB;
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.category-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #5C0099, #9333EA);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.category-card:hover {
  border-color: #5C0099;
  transform: translateY(-8px);
  box-shadow: 0 12px 28px rgba(92, 0, 153, 0.15);
}

.category-card:hover::before {
  transform: scaleX(1);
}

.category-card.selected {
  border-color: #5C0099;
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.05), rgba(147, 51, 234, 0.05));
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.2);
}

.category-card.selected::before {
  transform: scaleX(1);
}

.card-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #F3E8FF, #E9D5FF);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
  color: #5C0099;
  transition: all 0.3s ease;
}

.category-card:hover .card-icon {
  transform: scale(1.1) rotate(5deg);
  background: linear-gradient(135deg, #5C0099, #9333EA);
  color: white;
}

.category-card.selected .card-icon {
  background: linear-gradient(135deg, #5C0099, #9333EA);
  color: white;
}

.card-title {
  font-size: 1.375rem;
  font-weight: 700;
  color: #1F2937;
  margin-bottom: 0.5rem;
}

.card-description {
  font-size: 0.9375rem;
  color: #6B7280;
  line-height: 1.5;
}

.card-check {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 32px;
  height: 32px;
  background: #10B981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s ease;
}

.category-card.selected .card-check {
  opacity: 1;
  transform: scale(1);
}

/* ========== NIVEL 2: BÚSQUEDA ========== */
.search-container {
  margin: 2rem 0;
}

.search-bar {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.search-icon {
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9CA3AF;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 1rem 3rem 1rem 3.5rem;
  font-size: 1rem;
  border: 2px solid #E5E7EB;
  border-radius: 50px;
  background: white;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #5C0099;
  box-shadow: 0 0 0 4px rgba(92, 0, 153, 0.1);
}

.clear-btn {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: #F3F4F6;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: #E5E7EB;
}

/* ========== RESULTADOS DE BÚSQUEDA ========== */
.search-results {
  margin: 2rem 0;
}

.results-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #6B7280;
  margin-bottom: 1rem;
}

.results-grid {
  display: grid;
  gap: 0.75rem;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  text-align: left;
  font-size: 1rem;
  font-weight: 500;
  color: #1F2937;
  cursor: pointer;
  transition: all 0.2s ease;
}

.result-item:hover {
  border-color: #5C0099;
  background: rgba(92, 0, 153, 0.05);
  transform: translateX(4px);
}

.result-item .arrow {
  margin-left: auto;
  color: #9CA3AF;
  transition: all 0.2s ease;
}

.result-item:hover .arrow {
  color: #5C0099;
  transform: translateX(4px);
}

.no-results {
  text-align: center;
  padding: 3rem 2rem;
  color: #6B7280;
}

.no-results p {
  margin: 1rem 0;
  font-size: 1rem;
}

.link-btn {
  background: none;
  border: none;
  color: #5C0099;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.link-btn:hover {
  color: #9333EA;
}

/* ========== DESTACADAS ========== */
.featured-section {
  margin: 3rem 0;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}

.featured-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem 1rem;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.featured-card:hover {
  border-color: #5c0099;
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(108, 3, 177, 0.15);
}

.featured-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #5c0099, #850ad7);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
}

.featured-card:hover .featured-icon {
  background: linear-gradient(135deg, #FDC500, #ffc400);
  color: white;
}

.featured-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1F2937;
  text-align: center;
}

.featured-arrow {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  color: #9CA3AF;
  opacity: 0;
  transition: all 0.2s ease;
}

.featured-card:hover .featured-arrow {
  opacity: 1;
}

/* ========== GRUPOS ========== */
.groups-section {
  margin: 3rem 0;
}

.groups-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.group-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.3s ease;
}

.group-tab:hover {
  border-color: #5C0099;
  color: #5C0099;
  background: rgba(92, 0, 153, 0.05);
}

.group-tab.active {
  border-color: #5C0099;
  background: linear-gradient(135deg, #5C0099, #9333EA);
  color: white;
}

.group-tab .count {
  font-size: 0.875rem;
  opacity: 0.8;
}

.group-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.group-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  text-align: left;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #1F2937;
  cursor: pointer;
  transition: all 0.2s ease;
}

.group-item:hover {
  border-color: #5C0099;
  background: rgba(92, 0, 153, 0.05);
  transform: translateX(4px);
}

.item-arrow {
  margin-left: auto;
  color: #9CA3AF;
  opacity: 0;
  transition: all 0.2s ease;
}

.group-item:hover .item-arrow {
  opacity: 1;
  color: #5C0099;
}

/* ========== VER TODAS ========== */
.view-all-section {
  margin: 3rem 0;
  text-align: center;
}

.view-all-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: white;
  border: 2px solid #5C0099;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  color: #5C0099;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-all-btn:hover {
  background: #5C0099;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(92, 0, 153, 0.3);
}

/* ========== NIVEL 3: UBICACIÓN ========== */
.location-section {
  max-width: 500px;
  margin: 2rem auto;
}

.city-selector {
  margin-bottom: 2rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.75rem;
}

.form-label.required::after {
  content: '*';
  color: #EF4444;
  margin-left: 0.25rem;
}

.form-select {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  background: white;
  color: #1F2937;
  cursor: pointer;
  transition: all 0.3s ease;
}

.form-select:focus {
  outline: none;
  border-color: #5C0099;
  box-shadow: 0 0 0 4px rgba(92, 0, 153, 0.1);
}

.location-note {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1.25rem;
  background: rgba(92, 0, 153, 0.05);
  border: 1px solid rgba(92, 0, 153, 0.2);
  border-radius: 12px;
}

.location-note p {
  font-size: 0.9375rem;
  color: #6B7280;
  line-height: 1.5;
}

/* ========== MODAL ========== */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 24px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideUp 0.3s ease;
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 2px solid #F3F4F6;
}

.modal-header h3 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: #1F2937;
}

.close-btn {
  width: 40px;
  height: 40px;
  background: #F3F4F6;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #E5E7EB;
  transform: rotate(90deg);
}

.modal-search {
  position: relative;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #F3F4F6;
}

.modal-search .search-icon {
  position: absolute;
  left: 3rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9CA3AF;
}

.modal-search-input {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 2.5rem;
  font-size: 0.9375rem;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.modal-search-input:focus {
  outline: none;
  border-color: #5C0099;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 2rem 2rem;
}

.alphabetical-list {
  display: grid;
  gap: 0.5rem;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  text-align: left;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #1F2937;
  cursor: pointer;
  transition: all 0.2s ease;
}

.list-item:hover {
  border-color: #5C0099;
  background: rgba(92, 0, 153, 0.05);
}

.list-item span {
  flex: 1;
}

.no-results-modal {
  text-align: center;
  padding: 3rem 1rem;
  color: #9CA3AF;
}

/* ========== ERROR MESSAGES ========== */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #DC2626;
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 0.5rem;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .categories-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .featured-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .groups-tabs {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 0.5rem;
  }

  .group-items {
    grid-template-columns: 1fr;
  }

  .modal-content {
    max-height: 90vh;
  }
}

@media (max-width: 480px) {
  .step-title {
    font-size: 1.5rem;
  }

  .featured-grid {
    grid-template-columns: 1fr;
  }
}
</style>