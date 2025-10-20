<!-- frontend/src/components/Publish/CategoryStep.vue -->
<template>
  <div class="category-step">
    <!-- 
      ==========================================
      PASO 1: CATEGORÍA Y UBICACIÓN
      ==========================================
      Permite seleccionar:
        - Categoría principal
        - Subcategoría (dinámica según categoría)
        - Departamento
        - Ciudad
      
      TODO Django:
        - GET /api/categories/ - Lista de categorías
        - GET /api/subcategories/?category_id=X - Subcategorías filtradas
        - GET /api/departments/ - Lista de departamentos
        - GET /api/cities/?department_id=X - Ciudades filtradas
    -->

    <h2 class="step-title">
      <va-icon name="category" color="purple" size="large" />
      Categoría y Ubicación
    </h2>

    <p class="step-description">
      Selecciona dónde aparecerá tu anuncio para que las personas correctas lo encuentren
    </p>

    <div class="form-grid">
      <!-- ==========================================
           CATEGORÍA PRINCIPAL
           ========================================== -->
      <div class="form-group">
        <label class="form-label required">
          <va-icon name="category" size="small" />
          Categoría
        </label>
        <select 
          v-model="localData.category" 
          @change="onCategoryChange"
          class="form-select"
          required
        >
          <option value="">Selecciona una categoría</option>
          <option 
            v-for="cat in categories" 
            :key="cat.id"
            :value="cat.id"
          >
            {{ cat.icon }} {{ cat.name }}
          </option>
        </select>
        <span v-if="errors.category" class="error-message">{{ errors.category }}</span>
      </div>

      <!-- ==========================================
           SUBCATEGORÍA (Depende de categoría)
           ========================================== -->
      <div class="form-group">
        <label class="form-label required">
          <va-icon name="label" size="small" />
          Subcategoría
        </label>
        <select 
          v-model="localData.subcategory" 
          class="form-select"
          :disabled="!localData.category"
          required
        >
          <option value="">
            {{ localData.category ? 'Selecciona una subcategoría' : 'Primero selecciona una categoría' }}
          </option>
          <option 
            v-for="sub in filteredSubcategories" 
            :key="sub"
            :value="sub"
          >
            {{ sub }}
          </option>
        </select>
        <span v-if="errors.subcategory" class="error-message">{{ errors.subcategory }}</span>
      </div>

      <!-- ==========================================
           DEPARTAMENTO
           ========================================== -->
      <div class="form-group">
        <label class="form-label required">
          <va-icon name="location_city" size="small" />
          Departamento
        </label>
        <select 
          v-model="localData.department" 
          @change="onDepartmentChange"
          class="form-select"
          required
        >
          <option value="">Selecciona un departamento</option>
          <option 
            v-for="dept in departments" 
            :key="dept.id"
            :value="dept.id"
          >
            {{ dept.name }}
          </option>
        </select>
        <span v-if="errors.department" class="error-message">{{ errors.department }}</span>
      </div>

      <!-- ==========================================
           CIUDAD
           ========================================== -->
      <div class="form-group">
        <label class="form-label required">
          <va-icon name="location_on" size="small" />
          Ciudad
        </label>
        <input
          v-model="localData.city"
          type="text"
          class="form-input"
          placeholder="Ej: Cochabamba, Quillacollo, Sacaba..."
          :disabled="!localData.department"
          required
        />
        <span v-if="errors.city" class="error-message">{{ errors.city }}</span>
        
        <!-- Hint informativo -->
        <span class="form-hint">
          <va-icon name="info" size="small" />
          Escribe la ciudad específica donde ofreces tu servicio
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// ==========================================
// PROPS
// ==========================================
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

// ==========================================
// EMITS
// ==========================================
const emit = defineEmits(['update:modelValue'])

// ==========================================
// STATE LOCAL
// ==========================================
const localData = ref({ ...props.modelValue })
const errors = ref({})

// TODO Django: Estos datos vendrán del backend
const categories = ref([
  { id: 'profesionales', name: 'Profesionales', icon: '📋' },
  { id: 'gastronomia', name: 'Gastronomía', icon: '🍽️' },
  { id: 'trabajos', name: 'Trabajos', icon: '💼' },
  { id: 'servicios', name: 'Servicios', icon: '🛠️' }
])

// TODO Django: GET /api/subcategories/?category_id=X
const subcategories = ref({
  profesionales: ['Abogados', 'Doctores', 'Contadores', 'Arquitectos', 'Ingenieros'],
  gastronomia: ['Restaurantes', 'Cafeterías', 'Comida Rápida', 'Catering', 'Pizzerías'],
  trabajos: ['Tiempo Completo', 'Medio Tiempo', 'Freelance', 'Pasantías', 'Temporal'],
  servicios: ['Plomería', 'Electricidad', 'Carpintería', 'Limpieza', 'Reparaciones']
})

// TODO Django: GET /api/departments/
const departments = ref([
  { id: 'la-paz', name: 'La Paz' },
  { id: 'cochabamba', name: 'Cochabamba' },
  { id: 'santa-cruz', name: 'Santa Cruz' },
  { id: 'oruro', name: 'Oruro' },
  { id: 'potosi', name: 'Potosí' },
  { id: 'tarija', name: 'Tarija' },
  { id: 'chuquisaca', name: 'Chuquisaca' },
  { id: 'beni', name: 'Beni' },
  { id: 'pando', name: 'Pando' }
])

// ==========================================
// COMPUTED
// ==========================================
const filteredSubcategories = computed(() => {
  if (!localData.value.category) return []
  return subcategories.value[localData.value.category] || []
})

// ==========================================
// MÉTODOS
// ==========================================
const onCategoryChange = () => {
  // Reset subcategoría cuando cambia la categoría
  localData.value.subcategory = ''
  errors.value.category = ''
}

const onDepartmentChange = () => {
  // Reset ciudad cuando cambia el departamento
  localData.value.city = ''
  errors.value.department = ''
}

const validate = () => {
  errors.value = {}
  let isValid = true

  if (!localData.value.category) {
    errors.value.category = 'Selecciona una categoría'
    isValid = false
  }

  if (!localData.value.subcategory) {
    errors.value.subcategory = 'Selecciona una subcategoría'
    isValid = false
  }

  if (!localData.value.department) {
    errors.value.department = 'Selecciona un departamento'
    isValid = false
  }

  if (!localData.value.city || localData.value.city.length < 3) {
    errors.value.city = 'Escribe una ciudad válida (mínimo 3 caracteres)'
    isValid = false
  }

  return isValid
}

// ==========================================
// WATCHERS - Sync con componente padre
// ==========================================
watch(localData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

watch(() => props.modelValue, (newValue) => {
  localData.value = { ...newValue }
}, { deep: true })

// ==========================================
// EXPOSE - Métodos accesibles desde el padre
// ==========================================
defineExpose({
  validate
})
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.category-step {
  padding: 1rem 0;
}

/* ==========================================
   TÍTULO Y DESCRIPCIÓN
   ========================================== */
.step-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 0.5rem;
}

.step-description {
  color: #666;
  font-size: 1rem;
  margin-bottom: 2rem;
  line-height: 1.5;
}

/* ==========================================
   GRID DE FORMULARIO
   ========================================== */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

/* ==========================================
   GRUPOS DE FORMULARIO
   ========================================== */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  font-size: 0.95rem;
}

.form-label.required::after {
  content: '*';
  color: #E34B4A;
  margin-left: 0.25rem;
}

/* ==========================================
   INPUTS Y SELECTS
   ========================================== */
.form-input,
.form-select {
  padding: 0.875rem 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: inherit;
  background-color: white;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

.form-input:disabled,
.form-select:disabled {
  background-color: #F5F5F5;
  cursor: not-allowed;
  opacity: 0.6;
}

.form-select {
  cursor: pointer;
}

/* ==========================================
   MENSAJES
   ========================================== */
.error-message {
  color: #E34B4A;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.form-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.85rem;
  font-style: italic;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .step-description {
    font-size: 0.95rem;
  }
}
</style>