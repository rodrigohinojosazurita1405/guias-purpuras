<!-- frontend/src/components/Publish/ImagesStep.vue -->
<template>
  <div class="images-step">
    <!-- 
      ==========================================
      PASO 3: SUBIDA DE IMÁGENES
      ==========================================
      Permite:
        - Subir hasta 5 imágenes (plan gratis: 3, TOP: ilimitadas)
        - Preview de imágenes antes de subir
        - Eliminar imágenes
        - Reordenar imágenes (drag & drop)
        - Validar tamaño (máx 5MB) y formato (JPG, PNG, WEBP)
      
      TODO Django:
        - POST /api/listings/{id}/images/ - Subir imagen
        - DELETE /api/listings/{id}/images/{image_id}/ - Eliminar
        - PATCH /api/listings/{id}/images/{image_id}/ - Reordenar
        - Integrar con Cloudinary o AWS S3
        - Generar thumbnails automáticamente
    -->

    <h2 class="step-title">
      <va-icon name="image" color="purple" size="large" />
      Imágenes de tu Anuncio
    </h2>

    <p class="step-description">
      Las imágenes aumentan hasta 10x la visibilidad de tu anuncio. ¡Sube fotos de calidad!
    </p>

    <!-- ==========================================
         INFORMACIÓN DEL PLAN
         ========================================== -->
    <div class="plan-info">
      <va-icon name="info" color="info" />
      <div class="plan-info-text">
        <strong>Límite según tu plan:</strong>
        <span v-if="maxImages === 3">Plan Gratis - Hasta 3 imágenes</span>
        <span v-else-if="maxImages === 5">Plan Destacado - Hasta 5 imágenes</span>
        <span v-else>Plan TOP - Imágenes ilimitadas</span>
      </div>
    </div>

    <!-- ==========================================
         ÁREA DE CARGA
         ========================================== -->
    <div 
      class="upload-area"
      :class="{ 'drag-over': isDragging }"
      @drop.prevent="handleDrop"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        accept="image/jpeg,image/png,image/webp"
        multiple
        @change="handleFileSelect"
        style="display: none"
      />

      <div class="upload-content">
        <va-icon name="cloud_upload" size="4rem" color="purple" />
        <h3 class="upload-title">
          {{ images.length === 0 ? 'Sube tus imágenes' : 'Agregar más imágenes' }}
        </h3>
        <p class="upload-text">
          Haz clic o arrastra imágenes aquí
        </p>
        <p class="upload-hint">
          JPG, PNG o WEBP - Máximo 5MB por imagen
        </p>
      </div>
    </div>

    <!-- ==========================================
         MENSAJE DE ERROR GENERAL
         ========================================== -->
    <div v-if="errorMessage" class="error-banner">
      <va-icon name="error" color="danger" />
      <span>{{ errorMessage }}</span>
      <button @click="errorMessage = ''" class="close-error">
        <va-icon name="close" size="small" />
      </button>
    </div>

    <!-- ==========================================
         PREVIEW DE IMÁGENES
         ========================================== -->
    <div v-if="images.length > 0" class="images-preview">
      <h3 class="preview-title">
        Tus imágenes ({{ images.length }}/{{ maxImages === 999 ? '∞' : maxImages }})
      </h3>

      <div class="images-grid">
        <div 
          v-for="(image, index) in images" 
          :key="index"
          class="image-item"
          :class="{ 'is-main': index === 0 }"
        >
          <!-- Badge de imagen principal -->
          <div v-if="index === 0" class="main-badge">
            <va-icon name="star" size="small" />
            Principal
          </div>

          <!-- Preview de la imagen -->
          <img :src="image.preview" :alt="`Imagen ${index + 1}`" class="image-preview" />

          <!-- Overlay con acciones -->
          <div class="image-overlay">
            <div class="image-actions">
              <!-- Mover a principal -->
              <button 
                v-if="index !== 0"
                @click="setAsMain(index)"
                class="action-btn"
                title="Establecer como principal"
              >
                <va-icon name="star" size="small" />
              </button>

              <!-- Eliminar -->
              <button 
                @click="removeImage(index)"
                class="action-btn danger"
                title="Eliminar imagen"
              >
                <va-icon name="delete" size="small" />
              </button>
            </div>

            <!-- Información del archivo -->
            <div class="image-info">
              <span class="image-size">{{ formatFileSize(image.size) }}</span>
            </div>
          </div>

          <!-- Indicador de orden -->
          <div class="image-order">{{ index + 1 }}</div>
        </div>

        <!-- Botón agregar más (si no alcanzó el límite) -->
        <div 
          v-if="images.length < maxImages"
          class="add-more-card"
          @click="triggerFileInput"
        >
          <va-icon name="add" size="3rem" color="purple" />
          <span>Agregar más</span>
        </div>
      </div>
    </div>

    <!-- ==========================================
         TIPS PARA BUENAS FOTOS
         ========================================== -->
    <div class="tips-section">
      <h4 class="tips-title">
        <va-icon name="lightbulb" color="warning" />
        Tips para buenas fotos
      </h4>
      <ul class="tips-list">
        <li><va-icon name="check" size="small" color="success" /> Usa buena iluminación natural</li>
        <li><va-icon name="check" size="small" color="success" /> Muestra el producto/servicio claramente</li>
        <li><va-icon name="check" size="small" color="success" /> Usa fondos limpios y sin distracciones</li>
        <li><va-icon name="check" size="small" color="success" /> La primera imagen es la más importante</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// ==========================================
// PROPS
// ==========================================
const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  plan: {
    type: String,
    default: 'free' // free, featured, top
  }
})

// ==========================================
// EMITS
// ==========================================
const emit = defineEmits(['update:modelValue'])

// ==========================================
// STATE
// ==========================================
const images = ref([...props.modelValue])
const fileInput = ref(null)
const isDragging = ref(false)
const errorMessage = ref('')

// Límites según el plan
const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB en bytes
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

// ==========================================
// COMPUTED
// ==========================================
const maxImages = computed(() => {
  if (props.plan === 'free') return 3
  if (props.plan === 'featured') return 5
  return 999 // TOP = ilimitadas
})

// ==========================================
// MÉTODOS DE VALIDACIÓN
// ==========================================
const validateFile = (file) => {
  // Validar tipo
  if (!ALLOWED_TYPES.includes(file.type)) {
    return {
      valid: false,
      error: `Formato no permitido: ${file.name}. Usa JPG, PNG o WEBP`
    }
  }

  // Validar tamaño
  if (file.size > MAX_FILE_SIZE) {
    return {
      valid: false,
      error: `${file.name} supera 5MB. Comprime la imagen`
    }
  }

  // Validar límite de imágenes
  if (images.value.length >= maxImages.value) {
    return {
      valid: false,
      error: `Límite alcanzado: Máximo ${maxImages.value} imágenes en tu plan`
    }
  }

  return { valid: true }
}

// ==========================================
// MÉTODOS DE CARGA
// ==========================================
const processFile = (file) => {
  const validation = validateFile(file)
  
  if (!validation.valid) {
    errorMessage.value = validation.error
    return
  }

  // Crear preview con FileReader
  const reader = new FileReader()
  
  reader.onload = (e) => {
    images.value.push({
      file: file,
      preview: e.target.result,
      name: file.name,
      size: file.size,
      type: file.type
    })
    
    // Emitir cambios al padre
    emit('update:modelValue', images.value)
    
    errorMessage.value = '' // Limpiar errores
  }

  reader.onerror = () => {
    errorMessage.value = 'Error al cargar la imagen. Inténtalo de nuevo'
  }

  reader.readAsDataURL(file)
}

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  files.forEach(processFile)
  
  // Reset input para permitir subir la misma imagen nuevamente
  event.target.value = ''
}

const handleDrop = (event) => {
  isDragging.value = false
  const files = Array.from(event.dataTransfer.files)
  files.forEach(processFile)
}

// ==========================================
// MÉTODOS DE GESTIÓN DE IMÁGENES
// ==========================================
const removeImage = (index) => {
  if (confirm('¿Eliminar esta imagen?')) {
    images.value.splice(index, 1)
    emit('update:modelValue', images.value)
    
    // TODO Django: DELETE /api/listings/{id}/images/{image_id}/
  }
}

const setAsMain = (index) => {
  // Mover imagen al inicio del array
  const image = images.value.splice(index, 1)[0]
  images.value.unshift(image)
  emit('update:modelValue', images.value)
  
  // TODO Django: PATCH /api/listings/{id}/images/ - actualizar orden
}

// ==========================================
// UTILIDADES
// ==========================================
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const validate = () => {
  if (images.value.length === 0) {
    errorMessage.value = 'Sube al menos 1 imagen para tu anuncio'
    return false
  }
  return true
}

// ==========================================
// EXPOSE
// ==========================================
defineExpose({
  validate
})
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.images-step {
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
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

/* ==========================================
   INFORMACIÓN DEL PLAN
   ========================================== */
.plan-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #E3F2FD;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.plan-info-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  color: #1565C0;
  font-size: 0.95rem;
}

/* ==========================================
   ÁREA DE CARGA
   ========================================== */
.upload-area {
  border: 3px dashed #E0E0E0;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  background: #FAFAFA;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}

.upload-area:hover {
  border-color: var(--color-purple);
  background: rgba(92, 0, 153, 0.02);
}

.upload-area.drag-over {
  border-color: var(--color-yellow-primary);
  background: rgba(253, 197, 0, 0.05);
  transform: scale(1.02);
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.upload-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
}

.upload-text {
  font-size: 1rem;
  color: #666;
  margin: 0;
}

.upload-hint {
  font-size: 0.85rem;
  color: #999;
  margin: 0;
}

/* ==========================================
   ERROR BANNER
   ========================================== */
.error-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #FFEBEE;
  border: 1px solid #EF5350;
  border-radius: 8px;
  color: #C62828;
  margin-bottom: 1.5rem;
  position: relative;
}

.close-error {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #C62828;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.close-error:hover {
  background: rgba(0, 0, 0, 0.05);
}

/* ==========================================
   PREVIEW DE IMÁGENES
   ========================================== */
.images-preview {
  margin-bottom: 2rem;
}

.preview-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 1rem;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}

/* ==========================================
   ITEM DE IMAGEN
   ========================================== */
.image-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  background: #F5F5F5;
  border: 2px solid #E0E0E0;
  transition: all 0.3s ease;
}

.image-item.is-main {
  border-color: var(--color-yellow-primary);
  box-shadow: 0 4px 12px rgba(253, 197, 0, 0.3);
}

.image-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.main-badge {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
  padding: 0.4rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  z-index: 3;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.image-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ==========================================
   OVERLAY DE IMAGEN
   ========================================== */
.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.7) 0%, transparent 30%, transparent 70%, rgba(0,0,0,0.7) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0.75rem;
}

.image-item:hover .image-overlay {
  opacity: 1;
}

.image-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.action-btn:hover {
  transform: scale(1.1);
}

.action-btn.danger {
  background: #EF5350;
  color: white;
}

.action-btn.danger:hover {
  background: #C62828;
}

.image-info {
  display: flex;
  justify-content: flex-end;
}

.image-size {
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.image-order {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  z-index: 2;
}

/* ==========================================
   AGREGAR MÁS
   ========================================== */
.add-more-card {
  aspect-ratio: 1;
  border: 2px dashed var(--color-purple);
  border-radius: 12px;
  background: rgba(92, 0, 153, 0.02);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--color-purple);
  font-weight: 600;
}

.add-more-card:hover {
  background: rgba(92, 0, 153, 0.05);
  transform: scale(1.05);
}

/* ==========================================
   TIPS
   ========================================== */
.tips-section {
  background: #FFF9E6;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #FFD54F;
}

.tips-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 1rem;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tips-list li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.95rem;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
  .upload-area {
    padding: 2rem 1rem;
  }

  .images-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .step-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .images-grid {
    grid-template-columns: 1fr;
  }
}
</style>