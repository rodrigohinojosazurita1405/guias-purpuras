<template>
  <div class="category-step">
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

    <!-- Subcategorías (solo si hay categoría seleccionada) -->
    <transition name="fade">
      <div v-if="localData.category" class="subcategories-section">
        <h3 class="section-subtitle">
          <va-icon name="label" color="purple" size="1.5rem" />
          ¿Qué tipo específicamente?
        </h3>

        <div class="subcategories-grid">
          <button
            v-for="sub in filteredSubcategories"
            :key="sub"
            class="subcategory-btn"
            :class="{ selected: localData.subcategory === sub }"
            @click="selectSubcategory(sub)"
            type="button"
          >
            <va-icon 
              :name="localData.subcategory === sub ? 'check_circle' : 'radio_button_unchecked'" 
              size="small" 
            />
            {{ sub }}
          </button>
        </div>

        <span v-if="errors.subcategory" class="error-message">
          <va-icon name="error" size="small" />
          {{ errors.subcategory }}
        </span>
      </div>
    </transition>

    <!-- Ubicación -->
    <transition name="fade">
      <div v-if="localData.subcategory" class="location-section">
        <h3 class="section-subtitle">
          <va-icon name="location_city" color="purple" size="1.5rem" />
          Ubicación
        </h3>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label required">
              <va-icon name="location_city" size="small" />
              Ciudad
            </label>
            <select 
              v-model="localData.city" 
              class="form-select"
              required
            >
              <option value="">Selecciona una ciudad</option>
              <option 
                v-for="city in cities" 
                :key="city.id"
                :value="city.id"
              >
                {{ city.name }}
              </option>
            </select>
            <span v-if="errors.city" class="error-message">{{ errors.city }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">
              <va-icon name="home" size="small" />
              Dirección / Ubicación
            </label>
            <input 
              v-model="localData.address" 
              type="text"
              class="form-input"
              placeholder="Ej: Zona Sur, Av. Ejemplo 123"
            />
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

const localData = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const errors = ref({
  category: '',
  subcategory: '',
  city: ''
})

// Mock data de categorías del MVP (4 pilares)
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

const subcategories = {
  profesionales: [
    'Abogado', 'Médico', 'Arquitecto', 'Ingeniero', 
    'Contador', 'Psicólogo', 'Dentista', 'Veterinario',
    'Diseñador', 'Fotógrafo', 'Consultor', 'Coach'
  ],
  gastronomia: [
    'Restaurante', 'Café', 'Comida Rápida', 'Panadería',
    'Heladería', 'Bar', 'Pizzería', 'Comida Típica',
    'Buffet', 'Catering'
  ],
  trabajos: [
    'Tiempo Completo', 'Medio Tiempo', 'Por Proyecto',
    'Remoto', 'Pasantía', 'Freelance'
  ],
  negocios: [
    'Tecnología', 'Moda y Ropa', 'Belleza y Salud', 
    'Hogar y Decoración', 'Mascotas', 'Librería', 
    'Ferretería', 'Farmacia', 'Supermercado', 'Electrónica'
  ]
}

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

const filteredSubcategories = computed(() => {
  return subcategories[localData.value.category] || []
})

const selectCategory = (categoryId) => {
  localData.value.category = categoryId
  localData.value.subcategory = ''
  errors.value.category = ''
}

const selectSubcategory = (subcategory) => {
  localData.value.subcategory = subcategory
  errors.value.subcategory = ''
}

watch(() => localData.value.category, () => {
  localData.value.subcategory = ''
})

const validate = () => {
  errors.value = {
    category: '',
    subcategory: '',
    city: ''
  }

  if (!localData.value.category) {
    errors.value.category = 'Debes seleccionar una categoría'
    return false
  }

  if (!localData.value.subcategory) {
    errors.value.subcategory = 'Debes seleccionar una subcategoría'
    return false
  }

  if (!localData.value.city) {
    errors.value.city = 'Debes seleccionar una ciudad'
    return false
  }

  return true
}

defineExpose({ validate })
</script>

<style scoped>
.category-step {
  animation: fadeIn 0.5s ease;
}

/* ===================================
   TÍTULOS
   =================================== */
.step-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  font-weight: 800;
  color: #1F2937;
  margin-bottom: 0.75rem;
}

.step-description {
  font-size: 1.05rem;
  color: #6B7280;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.section-subtitle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #374151;
  margin-bottom: 1.5rem;
}

/* ===================================
   CARDS DE CATEGORÍAS
   =================================== */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.category-card {
  position: relative;
  background: white;
  border: 3px solid #E5E7EB;
  border-radius: 16px;
  padding: 2rem 1.5rem;
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
  height: 4px;
  background: linear-gradient(90deg, #5C0099, #9333EA);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.category-card:hover {
  border-color: #9333EA;
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(92, 0, 153, 0.15);
}

.category-card:hover::before {
  transform: scaleX(1);
}

.category-card.selected {
  border-color: #5C0099;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFF 100%);
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.2);
}

.category-card.selected::before {
  transform: scaleX(1);
}

.card-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F3F4F6, #E5E7EB);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.category-card:hover .card-icon,
.category-card.selected .card-icon {
  background: linear-gradient(135deg, #5C0099, #9333EA);
  color: white;
  transform: scale(1.1) rotate(5deg);
}

.card-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.5rem 0;
}

.card-description {
  font-size: 0.9rem;
  color: #6B7280;
  margin: 0;
}

.card-check {
  position: absolute;
  top: 1rem;
  right: 1rem;
  color: #5C0099;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s ease;
}

.category-card.selected .card-check {
  opacity: 1;
  transform: scale(1);
}

/* ===================================
   SUBCATEGORÍAS
   =================================== */
.subcategories-section {
  margin-bottom: 2.5rem;
  padding: 2rem;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFF 100%);
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

.subcategories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.subcategory-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.subcategory-btn:hover {
  border-color: #9333EA;
  background: #FAFAFA;
  transform: translateX(4px);
}

.subcategory-btn.selected {
  border-color: #5C0099;
  background: linear-gradient(135deg, #5C0099, #9333EA);
  color: white;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

/* ===================================
   UBICACIÓN
   =================================== */
.location-section {
  padding: 2rem;
  background: linear-gradient(135deg, #FFF9F0 0%, #FFF 100%);
  border-radius: 16px;
  border: 2px solid rgba(253, 197, 0, 0.2);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #374151;
}

.form-label.required::after {
  content: '*';
  color: #DC2626;
  margin-left: 0.25rem;
}

.form-select,
.form-input {
  padding: 0.875rem 1rem;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: #5C0099;
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

/* ===================================
   MENSAJES DE ERROR
   =================================== */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #DC2626;
  font-size: 0.875rem;
  font-weight: 600;
  margin-top: 0.5rem;
  padding: 0.75rem 1rem;
  background: #FEF2F2;
  border-radius: 8px;
  border-left: 4px solid #DC2626;
}

/* ===================================
   ANIMACIONES
   =================================== */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===================================
   RESPONSIVE
   =================================== */
@media (max-width: 768px) {
  .categories-grid {
    grid-template-columns: 1fr;
    max-width: 100%;
    gap: 1rem;
  }

  .category-card {
    padding: 1.5rem 1rem;
  }

  .card-icon {
    width: 60px;
    height: 60px;
  }

  .subcategories-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>