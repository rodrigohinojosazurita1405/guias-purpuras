<!-- 
  ==========================================
  MENUSTEP.VUE - VERSIÓN ORIGINAL SIMPLE
  ==========================================
  
  ✅ Solo checkboxes corregidos
  
-->

<template>
  <div class="menu-step">
    <!-- 
      ==========================================
      HEADER
      ==========================================
    -->
    <div class="step-header">
      <div class="header-icon">
        <va-icon name="restaurant_menu" size="2rem" color="purple" />
      </div>
      <div>
        <h2 class="step-title">Menú / Productos</h2>
        <p class="step-subtitle">
          Agrega los platos y productos que ofreces con fotos atractivas
        </p>
      </div>
    </div>

    <!-- 
      ==========================================
      CONTADOR Y BOTÓN AGREGAR
      ==========================================
    -->
    <div class="menu-controls">
      <div class="menu-count">
        <va-icon name="fastfood" color="purple" />
        <span class="count-text">
          <strong>{{ localMenuItems.length }}</strong> 
          {{ localMenuItems.length === 1 ? 'plato agregado' : 'platos agregados' }}
        </span>
      </div>

      <va-button
        @click="openAddItemModal"
        color="purple"
        icon="add"
        size="large"
      >
        Agregar Plato
      </va-button>
    </div>

    <!-- 
      ==========================================
      GRID DE PLATOS
      ==========================================
    -->
    <div v-if="localMenuItems.length > 0" class="menu-grid">
      <MenuItemCard
        v-for="(item, index) in localMenuItems"
        :key="index"
        :item="item"
        :editable="true"
        @edit="editItem(index)"
        @delete="confirmDelete(index)"
      />
    </div>

    <!-- 
      ==========================================
      ESTADO VACÍO
      ==========================================
    -->
    <div v-else class="empty-state">
      <va-icon name="restaurant" size="4rem" color="#CCC" />
      <h3 class="empty-title">Aún no has agregado platos</h3>
      <p class="empty-text">
        Comienza agregando tu primer plato con una foto atractiva, precio e ingredientes.
        Esto ayudará a tus clientes a conocer tu oferta.
      </p>
      <va-button
        @click="openAddItemModal"
        color="purple"
        size="large"
        icon="add"
      >
        Agregar Primer Plato
      </va-button>
    </div>

    <!-- 
      ==========================================
      HINT INFORMATIVO
      ==========================================
    -->
    <div class="info-hint">
      <va-icon name="lightbulb" color="warning" />
      <div class="hint-content">
        <strong>Tip:</strong> Las fotos de calidad atraen más clientes. 
        Asegúrate de que tus imágenes sean claras, bien iluminadas y muestren el plato de manera apetitosa.
      </div>
    </div>

    <!-- 
      ==========================================
      MODAL: AGREGAR/EDITAR PLATO - SIN TOCAR Z-INDEX
      ==========================================
    -->
    <va-modal
      v-model="showItemModal"
      size="large"
      :title="editingIndex !== null ? 'Editar Plato' : 'Agregar Nuevo Plato'"
      @ok="saveItem"
      @cancel="closeItemModal"
      ok-text="Guardar"
      cancel-text="Cancelar"
    >
      <div class="item-form">
        <!-- Preview de Imagen -->
        <div class="image-preview-section">
          <div v-if="currentItem.imagePreview" class="image-preview">
            <img :src="currentItem.imagePreview" alt="Preview" />
            <va-button
              @click="removeImage"
              preset="plain"
              color="danger"
              icon="close"
              class="remove-image-btn"
              size="small"
            />
          </div>
          
          <!-- Upload de Imagen -->
          <div v-else class="image-upload">
            <input
              ref="imageInput"
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              style="display: none"
            />
            <va-button
              @click="$refs.imageInput.click()"
              color="primary"
              icon="add_photo_alternate"
              size="large"
              class="upload-btn"
            >
              Subir Foto del Plato
            </va-button>
            <p class="upload-hint">JPG, PNG - Máx. 5MB</p>
          </div>
        </div>

        <!-- Nombre del Plato -->
        <va-input
          v-model="currentItem.name"
          label="Nombre del Plato"
          placeholder="Ej: Pique Macho"
          required-mark
          :rules="[(v) => !!v || 'El nombre es obligatorio']"
        >
          <template #prepend>
            <va-icon name="restaurant" color="purple" />
          </template>
        </va-input>

        <!-- Precio -->
        <va-input
          v-model.number="currentItem.price"
          label="Precio"
          placeholder="45.00"
          type="number"
          step="0.01"
          min="0"
          required-mark
          :rules="[
            (v) => v !== null && v !== undefined && v !== '' || 'El precio es obligatorio',
            (v) => v >= 0 || 'El precio debe ser mayor o igual a 0'
          ]"
        >
          <template #prepend>
            <span class="price-prefix">Bs.</span>
          </template>
        </va-input>

        <!-- Descripción -->
        <va-textarea
          v-model="currentItem.description"
          label="Descripción (Opcional)"
          placeholder="Describe el plato: sabor, preparación, tamaño de porción..."
          :min-rows="3"
          :max-rows="5"
          counter
          maxlength="250"
        >
          <template #prepend>
            <va-icon name="description" color="purple" />
          </template>
        </va-textarea>

        <!-- Ingredientes -->
        <va-input
          v-model="currentItem.ingredientsText"
          label="Ingredientes (Opcional)"
          placeholder="Ej: Carne de res, papa, cebolla, tomate, locoto"
        >
          <template #prepend>
            <va-icon name="eco" color="success" />
          </template>
        </va-input>
        <div class="input-hint">
          <va-icon name="info" size="small" />
          <span>Separa los ingredientes con comas</span>
        </div>

        <!-- ✅ Tags - SOLO ESTE ES EL CAMBIO -->
        <div class="tags-section">
          <label class="tags-label">Características (Opcional):</label>
          <div class="tags-grid">
            <va-checkbox
              :model-value="isTagSelected('Vegetariano')"
              @update:model-value="(checked) => toggleTag('Vegetariano', checked)"
              label="🌱 Vegetariano"
            />
            <va-checkbox
              :model-value="isTagSelected('Vegano')"
              @update:model-value="(checked) => toggleTag('Vegano', checked)"
              label="🌿 Vegano"
            />
            <va-checkbox
              :model-value="isTagSelected('Picante')"
              @update:model-value="(checked) => toggleTag('Picante', checked)"
              label="🌶️ Picante"
            />
            <va-checkbox
              :model-value="isTagSelected('Sin Gluten')"
              @update:model-value="(checked) => toggleTag('Sin Gluten', checked)"
              label="🌾 Sin Gluten"
            />
            <va-checkbox
              :model-value="isTagSelected('Especialidad de la casa')"
              @update:model-value="(checked) => toggleTag('Especialidad de la casa', checked)"
              label="⭐ Especialidad"
            />
            <va-checkbox
              :model-value="isTagSelected('Más vendido')"
              @update:model-value="(checked) => toggleTag('Más vendido', checked)"
              label="🔥 Popular"
            />
          </div>
        </div>

        <!-- Destacar plato (opcional) -->
        <va-switch
          v-model="currentItem.featured"
          label="Marcar como plato destacado"
          color="warning"
        >
          <template #innerLabel>
            <div class="switch-label">
              <va-icon name="star" />
              <span>{{ currentItem.featured ? 'Destacado' : 'Normal' }}</span>
            </div>
          </template>
        </va-switch>
      </div>
    </va-modal>

    <!-- 
      ==========================================
      MODAL: CONFIRMAR ELIMINACIÓN
      ==========================================
    -->
    <va-modal
      v-model="showDeleteModal"
      title="¿Eliminar plato?"
      message="Esta acción no se puede deshacer. ¿Estás seguro de eliminar este plato?"
      ok-text="Sí, eliminar"
      cancel-text="Cancelar"
      @ok="deleteItem"
    />
  </div>
</template>

<script setup>
// ==========================================
// IMPORTS
// ==========================================
import { ref, watch } from 'vue'
import MenuItemCard from './MenuItemCard.vue'

// ==========================================
// PROPS & EMITS
// ==========================================
const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

// ==========================================
// STATE
// ==========================================
const localMenuItems = ref([...props.modelValue])
const showItemModal = ref(false)
const showDeleteModal = ref(false)
const editingIndex = ref(null)
const deletingIndex = ref(null)
const imageInput = ref(null)

// Item actual siendo editado/creado
const currentItem = ref({
  name: '',
  price: null,
  description: '',
  ingredientsText: '',
  ingredients: [],
  tags: [],
  featured: false,
  image: null,
  imagePreview: null
})

// ==========================================
// METHODS
// ==========================================

/**
 * Abre modal para agregar nuevo plato
 */
const openAddItemModal = () => {
  editingIndex.value = null
  resetCurrentItem()
  showItemModal.value = true
}

/**
 * Editar plato existente
 */
const editItem = (index) => {
  editingIndex.value = index
  const item = localMenuItems.value[index]
  
  // Copiar datos del item al formulario
  currentItem.value = {
    ...item,
    ingredientsText: item.ingredients?.join(', ') || ''
  }
  
  showItemModal.value = true
}

/**
 * Confirmar eliminación
 */
const confirmDelete = (index) => {
  deletingIndex.value = index
  showDeleteModal.value = true
}

/**
 * Resetea el item actual
 */
const resetCurrentItem = () => {
  currentItem.value = {
    name: '',
    price: null,
    description: '',
    ingredientsText: '',
    ingredients: [],
    tags: [],
    featured: false,
    image: null,
    imagePreview: null
  }
}

/**
 * ✅ Verificar si un tag está seleccionado
 */
const isTagSelected = (tag) => {
  return currentItem.value.tags && currentItem.value.tags.includes(tag)
}

/**
 * ✅ Toggle de tags (agregar/quitar)
 */
const toggleTag = (tag, checked) => {
  if (!currentItem.value.tags) {
    currentItem.value.tags = []
  }
  
  if (checked) {
    // Agregar tag si no existe
    if (!currentItem.value.tags.includes(tag)) {
      currentItem.value.tags.push(tag)
    }
  } else {
    // Remover tag si existe
    const index = currentItem.value.tags.indexOf(tag)
    if (index > -1) {
      currentItem.value.tags.splice(index, 1)
    }
  }
}

/**
 * Maneja el upload de imagen
 */
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) { // 5MB
      alert('La imagen es muy grande. Máximo 5MB.')
      return
    }

    currentItem.value.image = file

    // Crear preview
    const reader = new FileReader()
    reader.onload = (e) => {
      currentItem.value.imagePreview = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

/**
 * Remueve la imagen actual
 */
const removeImage = () => {
  currentItem.value.image = null
  currentItem.value.imagePreview = null
  if (imageInput.value) {
    imageInput.value.value = ''
  }
}

/**
 * Cierra el modal sin guardar
 */
const closeItemModal = () => {
  showItemModal.value = false
}

/**
 * Guarda el plato (nuevo o editado)
 */
const saveItem = () => {
  if (!currentItem.value.name || currentItem.value.price === null || currentItem.value.price === '') {
    return // Validation handled by VA components
  }

  // Procesar ingredientes si los hay
  if (currentItem.value.ingredientsText) {
    currentItem.value.ingredients = currentItem.value.ingredientsText
      .split(',')
      .map(ingredient => ingredient.trim())
      .filter(ingredient => ingredient)
  }

  const newItem = { ...currentItem.value }
  delete newItem.ingredientsText // No necesitamos esto

  if (editingIndex.value !== null) {
    // Editando item existente
    localMenuItems.value[editingIndex.value] = newItem
  } else {
    // Agregando nuevo item
    localMenuItems.value.push(newItem)
  }

  emit('update:modelValue', localMenuItems.value)
  showItemModal.value = false
}

/**
 * Elimina definitivamente el plato
 */
const deleteItem = () => {
  if (deletingIndex.value !== null) {
    localMenuItems.value.splice(deletingIndex.value, 1)
    emit('update:modelValue', localMenuItems.value)
  }
  
  showDeleteModal.value = false
  deletingIndex.value = null
}

// ==========================================
// WATCHERS
// ==========================================
watch(
  () => props.modelValue,
  (newValue) => {
    localMenuItems.value = [...newValue]
  },
  { deep: true }
)
</script>

<style scoped>
/* ==========================================
   HEADER
   ========================================== */
.step-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.header-icon {
  width: 64px;
  height: 64px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-dark);
  margin: 0;
}

.step-subtitle {
  color: #666;
  margin: 0.25rem 0 0 0;
  font-size: 1rem;
}

/* ==========================================
   CONTROLS
   ========================================== */
.menu-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.25rem;
  background: rgba(139, 92, 246, 0.05);
  border-radius: 12px;
  border-left: 4px solid var(--color-purple);
}

.menu-count {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.count-text {
  font-size: 1.1rem;
  color: var(--color-purple-dark);
}

/* ==========================================
   GRID
   ========================================== */
.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

/* ==========================================
   EMPTY STATE
   ========================================== */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: #f9fafb;
  border-radius: 16px;
  border: 2px dashed #d1d5db;
  margin-bottom: 2rem;
}

.empty-title {
  margin: 1.5rem 0 0.75rem 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
}

.empty-text {
  color: #6b7280;
  margin: 0 0 2rem 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.5;
}

/* ==========================================
   INFO HINT
   ========================================== */
.info-hint {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: rgba(251, 191, 36, 0.1);
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 8px;
  margin-bottom: 2rem;
}

.hint-content {
  color: #92400e;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* ==========================================
   FORM
   ========================================== */
.item-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: none;
}

.image-preview-section {
  margin-bottom: 1rem;
}

.image-preview {
  position: relative;
  display: inline-block;
}

.image-preview img {
  width: 300px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid #e5e7eb;
}

.remove-image-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
}

.image-upload {
  text-align: center;
  padding: 2rem;
  border: 2px dashed var(--color-purple);
  border-radius: 8px;
  background: rgba(139, 92, 246, 0.02);
  transition: background-color 0.2s;
}

.image-upload:hover {
  background: rgba(139, 92, 246, 0.05);
}

.upload-btn {
  margin-bottom: 0.5rem;
}

.upload-hint {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.price-prefix {
  font-weight: 600;
  color: var(--color-purple);
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  margin-top: -0.75rem;
}

.tags-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tags-label {
  font-weight: 600;
  color: var(--color-purple-dark);
}

.tags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
}

.switch-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* ==========================================
   RESPONSIVE - TABLET
   ========================================== */
@media (max-width: 768px) {
  .menu-controls {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .menu-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }

  .tags-grid {
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  }
}

/* ==========================================
   RESPONSIVE - MOBILE
   ========================================== */
@media (max-width: 480px) {
  .header-icon {
    width: 56px;
    height: 56px;
  }

  .step-title {
    font-size: 1.25rem;
  }

  .empty-state {
    padding: 3rem 1.5rem;
  }

  .empty-title {
    font-size: 1.25rem;
  }

  .image-preview img {
    width: 100%;
    max-width: 300px;
  }
}
</style>