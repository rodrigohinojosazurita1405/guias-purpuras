<!-- 
  ==========================================
  MENUITEMCARD.VUE
  ==========================================
  
  Card para mostrar un plato/producto individual del menú.
  Se usa tanto para:
    - Vista del usuario (solo lectura)
    - Panel del dueño (editable/eliminable)
  
  Props:
    - item: Objeto con datos del plato
    - editable: Boolean para mostrar botones de editar/eliminar
    - compact: Boolean para versión compacta
-->

<template>
  <div 
    class="menu-item-card"
    :class="{ 
      'editable': editable, 
      'compact': compact,
      'no-image': !item.image 
    }"
  >
    <!-- 
      ==========================================
      IMAGEN DEL PLATO
      ==========================================
    -->
    <div class="item-image">
      <img 
        v-if="item.image" 
        :src="getImageUrl(item.image)" 
        :alt="item.name"
        @error="handleImageError"
      />
      <div v-else class="placeholder-image">
        <va-icon name="restaurant" size="3rem" color="#CCC" />
        <span class="placeholder-text">Sin imagen</span>
      </div>

      <!-- Badge de destacado (si aplica) -->
      <div v-if="item.featured" class="featured-badge">
        <va-icon name="star" size="small" />
        Destacado
      </div>
    </div>

    <!-- 
      ==========================================
      CONTENIDO DEL PLATO
      ==========================================
    -->
    <div class="item-content">
      <!-- Nombre y Precio -->
      <div class="item-header">
        <h3 class="item-name">{{ item.name }}</h3>
        <div class="item-price">
          <span class="currency">Bs.</span>
          <span class="amount">{{ formatPrice(item.price) }}</span>
        </div>
      </div>

      <!-- Descripción -->
      <p v-if="item.description" class="item-description">
        {{ item.description }}
      </p>

      <!-- Ingredientes -->
      <div v-if="item.ingredients && item.ingredients.length > 0" class="item-ingredients">
        <va-icon name="eco" size="small" color="success" />
        <span class="ingredients-label">Ingredientes:</span>
        <span class="ingredients-text">{{ formatIngredients(item.ingredients) }}</span>
      </div>

      <!-- Tags adicionales -->
      <div v-if="item.tags && item.tags.length > 0" class="item-tags">
        <va-chip
          v-for="tag in item.tags"
          :key="tag"
          size="small"
          color="purple"
          outline
        >
          {{ tag }}
        </va-chip>
      </div>

      <!-- 
        ==========================================
        BOTONES DE ACCIÓN (Solo en modo editable)
        ==========================================
      -->
      <div v-if="editable" class="item-actions">
        <va-button
          size="small"
          color="primary"
          @click="$emit('edit', item)"
          icon="edit"
        >
          Editar
        </va-button>
        
        <va-button
          size="small"
          color="danger"
          @click="$emit('delete', item)"
          icon="delete"
          preset="secondary"
        >
          Eliminar
        </va-button>
      </div>

      <!-- 
        ==========================================
        BOTÓN VER MÁS (Para usuarios)
        ==========================================
      -->
      <div v-if="!editable && showViewMore" class="item-view-more">
        <va-button
          size="small"
          color="purple"
          @click="$emit('view', item)"
          preset="secondary"
        >
          Ver detalles
          <va-icon name="arrow_forward" size="small" />
        </va-button>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==========================================
// IMPORTS
// ==========================================
import { computed } from 'vue'

// ==========================================
// PROPS
// ==========================================
const props = defineProps({
  // Objeto con datos del plato
  item: {
    type: Object,
    required: true,
    validator: (value) => {
      return value.name && (value.price !== null && value.price !== undefined)
    }
  },
  
  // Modo editable (para panel de dueño)
  editable: {
    type: Boolean,
    default: false
  },
  
  // Vista compacta
  compact: {
    type: Boolean,
    default: false
  },
  
  // Mostrar botón "Ver más"
  showViewMore: {
    type: Boolean,
    default: false
  }
})

// ==========================================
// EMITS
// ==========================================
const emit = defineEmits(['edit', 'delete', 'view'])

// ==========================================
// COMPUTED
// ==========================================

/**
 * Obtiene la URL de la imagen
 */
const getImageUrl = (image) => {
  // Si es un objeto File (recién subido)
  if (image instanceof File) {
    return URL.createObjectURL(image)
  }
  
  // Si es una URL de base64
  if (typeof image === 'string' && image.startsWith('data:')) {
    return image
  }
  
  // Si es una URL completa
  if (typeof image === 'string' && (image.startsWith('http') || image.startsWith('/'))) {
    return image
  }
  
  // Si es un objeto con url
  if (image && image.url) {
    return image.url
  }
  
  return null
}

// ==========================================
// METHODS
// ==========================================

/**
 * Formatea el precio
 */
const formatPrice = (price) => {
  if (!price && price !== 0) return '0.00'
  return parseFloat(price).toFixed(2)
}

/**
 * Formatea los ingredientes
 */
const formatIngredients = (ingredients) => {
  if (Array.isArray(ingredients)) {
    return ingredients.join(', ')
  }
  return ingredients
}

/**
 * Maneja error de carga de imagen
 */
const handleImageError = (e) => {
  console.error('Error cargando imagen:', e)
  e.target.src = '' // Mostrar placeholder
}
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.menu-item-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.menu-item-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.menu-item-card.editable {
  border: 2px dashed #E0E0E0;
}

.menu-item-card.editable:hover {
  border-color: var(--color-purple);
}

/* ==========================================
   IMAGEN
   ========================================== */
.item-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #F5F5F5;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.menu-item-card:hover .item-image img {
  transform: scale(1.05);
}

/* Placeholder cuando no hay imagen */
.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
}

.placeholder-text {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #999;
}

/* Badge destacado */
.featured-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 2px 8px rgba(253, 197, 0, 0.4);
}

/* ==========================================
   CONTENIDO
   ========================================== */
.item-content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

/* ==========================================
   HEADER (Nombre + Precio)
   ========================================== */
.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.item-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
  line-height: 1.3;
  flex: 1;
}

.item-price {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  color: white;
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  white-space: nowrap;
  font-weight: 700;
}

.item-price .currency {
  font-size: 0.875rem;
}

.item-price .amount {
  font-size: 1.125rem;
}

/* ==========================================
   DESCRIPCIÓN
   ========================================== */
.item-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ==========================================
   INGREDIENTES
   ========================================== */
.item-ingredients {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  padding: 0.5rem;
  background: #F8F8F8;
  border-radius: 8px;
  border-left: 3px solid var(--va-success);
}

.ingredients-label {
  font-weight: 600;
  color: var(--color-purple-dark);
}

.ingredients-text {
  flex: 1;
  line-height: 1.4;
}

/* ==========================================
   TAGS
   ========================================== */
.item-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: auto;
}

/* ==========================================
   BOTONES DE ACCIÓN
   ========================================== */
.item-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid #E0E0E0;
}

.item-view-more {
  margin-top: auto;
  padding-top: 0.75rem;
}

/* ==========================================
   VERSIÓN COMPACTA
   ========================================== */
.menu-item-card.compact {
  flex-direction: row;
  height: auto;
}

.menu-item-card.compact .item-image {
  width: 140px;
  height: 140px;
  flex-shrink: 0;
}

.menu-item-card.compact .item-content {
  padding: 1rem;
}

.menu-item-card.compact .item-header {
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

.menu-item-card.compact .item-description {
  -webkit-line-clamp: 1;
}

/* ==========================================
   SIN IMAGEN
   ========================================== */
.menu-item-card.no-image .item-image {
  height: 120px;
}

/* ==========================================
   RESPONSIVE - MOBILE
   ========================================== */
@media (max-width: 768px) {
  .item-image {
    height: 180px;
  }

  .item-content {
    padding: 1rem;
  }

  .item-header {
    flex-direction: column;
    gap: 0.5rem;
  }

  .item-price {
    align-self: flex-start;
  }

  .item-actions {
    flex-direction: column;
  }

  /* Compacto en mobile siempre horizontal */
  .menu-item-card.compact {
    flex-direction: row;
  }

  .menu-item-card.compact .item-image {
    width: 100px;
    height: 100px;
  }
}

@media (max-width: 480px) {
  .item-image {
    height: 160px;
  }

  .item-name {
    font-size: 1rem;
  }

  .item-price .amount {
    font-size: 1rem;
  }

  .item-description {
    font-size: 0.85rem;
  }

  .item-ingredients {
    font-size: 0.8rem;
  }
}
</style>