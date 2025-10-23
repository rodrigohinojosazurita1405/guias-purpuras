<!-- 
  ==========================================
  MENUSTEP.VUE
  ==========================================
  
  Paso del formulario de publicación donde el dueño del restaurante
  puede agregar múltiples platos/productos a su menú.
  
  Cada plato incluye:
    - Foto
    - Nombre
    - Precio
    - Descripción
    - Ingredientes
    - Tags (vegetariano, picante, etc.)
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
      MODAL: AGREGAR/EDITAR PLATO
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

        <!-- Tags -->
        <div class="tags-section">
          <label class="tags-label">Características (Opcional):</label>
          <div class="tags-grid">
            <va-checkbox
              v-model="currentItem.tags"
              label="🌱 Vegetariano"
              value="Vegetariano"
            />
            <va-checkbox
              v-model="currentItem.tags"
              label="🌿 Vegano"
              value="Vegano"
            />
            <va-checkbox
              v-model="currentItem.tags"
              label="🌶️ Picante"
              value="Picante"
            />
            <va-checkbox
              v-model="currentItem.tags"
              label="🌾 Sin Gluten"
              value="Sin Gluten"
            />
            <va-checkbox
              v-model="currentItem.tags"
              label="⭐ Especialidad"
              value="Especialidad de la casa"
            />
            <va-checkbox
              v-model="currentItem.tags"
              label="🔥 Popular"
              value="Más vendido"
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
 * Abre modal para editar plato existente
 */
const editItem = (index) => {
  editingIndex.value = index
  const item = localMenuItems.value[index]
  
  currentItem.value = {
    name: item.name,
    price: item.price,
    description: item.description || '',
    ingredientsText: Array.isArray(item.ingredients) 
      ? item.ingredients.join(', ') 
      : item.ingredients || '',
    ingredients: item.ingredients || [],
    tags: item.tags || [],
    featured: item.featured || false,
    image: item.image,
    imagePreview: item.image ? getImageUrl(item.image) : null
  }
  
  showItemModal.value = true
}

/**
 * Guarda el plato (nuevo o editado)
 */
const saveItem = () => {
  // Validar campos obligatorios
  if (!currentItem.value.name || currentItem.value.price === null) {
    alert('Por favor completa los campos obligatorios')
    return
  }

  // Procesar ingredientes (convertir texto a array)
  const ingredientsArray = currentItem.value.ingredientsText
    .split(',')
    .map(i => i.trim())
    .filter(i => i.length > 0)

  const itemData = {
    name: currentItem.value.name,
    price: parseFloat(currentItem.value.price),
    description: currentItem.value.description,
    ingredients: ingredientsArray,
    tags: currentItem.value.tags,
    featured: currentItem.value.featured,
    image: currentItem.value.image,
    imagePreview: currentItem.value.imagePreview
  }

  if (editingIndex.value !== null) {
    // Editar existente
    localMenuItems.value[editingIndex.value] = itemData
  } else {
    // Agregar nuevo
    localMenuItems.value.push(itemData)
  }

  closeItemModal()
}

/**
 * Cierra el modal de item
 */
const closeItemModal = () => {
  showItemModal.value = false
  editingIndex.value = null
  resetCurrentItem()
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
 * Maneja la carga de imagen
 */
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Validar tamaño (máx 5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('La imagen es muy grande. Máximo 5MB.')
    return
  }

  // Validar tipo
  if (!file.type.startsWith('image/')) {
    alert('Solo se permiten archivos de imagen')
    return
  }

  currentItem.value.image = file
  currentItem.value.imagePreview = URL.createObjectURL(file)
}

/**
 * Remueve la imagen
 */
const removeImage = () => {
  currentItem.value.image = null
  currentItem.value.imagePreview = null
  if (imageInput.value) {
    imageInput.value.value = ''
  }
}

/**
 * Confirma eliminación
 */
const confirmDelete = (index) => {
  deletingIndex.value = index
  showDeleteModal.value = true
}

/**
 * Elimina el plato
 */
const deleteItem = () => {
  if (deletingIndex.value !== null) {
    localMenuItems.value.splice(deletingIndex.value, 1)
    deletingIndex.value = null
  }
  showDeleteModal.value = false
}

/**
 * Obtiene URL de imagen
 */
const getImageUrl = (image) => {
  if (image instanceof File) {
    return URL.createObjectURL(image)
  }
  if (typeof image === 'string') {
    return image
  }
  if (image && image.url) {
    return image.url
  }
  return null
}

// ==========================================
// WATCHERS
// ==========================================
watch(localMenuItems, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

// ==========================================
// VALIDACIÓN
// ==========================================
const validate = () => {
  // Opcional: puede no tener platos
  // Pero si los tiene, deben estar completos
  for (const item of localMenuItems.value) {
    if (!item.name || item.price === null || item.price === undefined) {
      console.error('Todos los platos deben tener nombre y precio')
      return false
    }
  }
  return true
}

// Exponer método validate() para PublishView.vue
defineExpose({
  validate
})
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.menu-step {
  width: 100%;
}

/* ==========================================
   HEADER
   ========================================== */
.step-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #E0E0E0;
}

.header-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(92, 0, 153, 0.2);
}

.step-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
}

.step-subtitle {
  font-size: 1rem;
  color: #666;
  margin: 0.25rem 0 0 0;
}

/* ==========================================
   CONTROLES
   ========================================== */
.menu-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.25rem;
  background: #F8F8F8;
  border-radius: 12px;
}

.menu-count {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.count-text {
  font-size: 1rem;
  color: #666;
}

/* ==========================================
   GRID DE PLATOS
   ========================================== */
.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

/* ==========================================
   ESTADO VACÍO
   ========================================== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: #F8F8F8;
  border-radius: 16px;
  border: 2px dashed #CCC;
  margin-bottom: 2rem;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-dark);
  margin: 1rem 0 0.5rem 0;
}

.empty-text {
  font-size: 1rem;
  color: #666;
  max-width: 500px;
  line-height: 1.5;
  margin: 0 0 2rem 0;
}

/* ==========================================
   HINT INFORMATIVO
   ========================================== */
.info-hint {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: #FFF8E1;
  border-left: 4px solid var(--va-warning);
  border-radius: 8px;
  margin-top: 2rem;
}

.hint-content {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
}

/* ==========================================
   FORMULARIO DE ITEM (MODAL)
   ========================================== */
.item-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem 0;
}

/* ==========================================
   PREVIEW/UPLOAD DE IMAGEN
   ========================================== */
.image-preview-section {
  width: 100%;
  margin-bottom: 1rem;
}

.image-preview {
  position: relative;
  width: 100%;
  max-width: 400px;
  height: 250px;
  margin: 0 auto;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  border-radius: 50%;
}

.image-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: #F8F8F8;
  border: 2px dashed #CCC;
  border-radius: 12px;
  text-align: center;
}

.upload-btn {
  margin-bottom: 1rem;
}

.upload-hint {
  font-size: 0.875rem;
  color: #999;
  margin: 0;
}

/* ==========================================
   OTROS ELEMENTOS DEL FORM
   ========================================== */
.price-prefix {
  font-weight: 700;
  color: var(--color-purple);
  padding: 0.5rem;
  background: #F5F5F5;
  border-radius: 6px;
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
  font-weight: 600;
}

/* ==========================================
   RESPONSIVE - TABLET
   ========================================== */
@media (max-width: 768px) {
  .step-header {
    flex-direction: column;
    text-align: center;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .menu-controls {
    flex-direction: column;
    gap: 1rem;
  }

  .menu-grid {
    grid-template-columns: 1fr;
  }

  .tags-grid {
    grid-template-columns: 1fr;
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

  .image-preview {
    height: 200px;
  }
}
</style>