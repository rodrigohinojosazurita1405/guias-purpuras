<!-- COMPONENTE DE UPLOAD DE ARCHIVOS COMPLETO -->
<!-- frontend/src/components/Upload/FileUpload.vue -->
<template>
  <div class="file-upload-container">
    <!-- INPUT OCULTO -->
    <input
      ref="fileInput"
      type="file"
      :accept="acceptedTypes"
      :multiple="multiple"
      @change="handleFileSelect"
      style="display: none"
    />

    <!-- ZONA DE DROP -->
    <div
      v-if="!files.length || multiple"
      class="drop-zone"
      :class="{ 
        'drag-over': isDragging,
        'has-error': error
      }"
      @click="openFileDialog"
      @dragenter.prevent="handleDragEnter"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
    >
      <!-- ÍCONO PRINCIPAL -->
      <div class="upload-icon">
        <va-icon 
          :name="isDragging ? 'file_download' : 'cloud_upload'" 
          size="3rem"
          :color="isDragging ? 'success' : 'purple'"
        />
      </div>

      <!-- TEXTOS -->
      <div class="upload-text">
        <p class="main-text">
          <strong v-if="isDragging">¡Suelta el archivo aquí!</strong>
          <strong v-else>Click para seleccionar</strong>
          <span v-if="!isDragging"> o arrastra tu {{ fileTypeText }} aquí</span>
        </p>
        <p class="hint-text">
          {{ allowedTypesText }} • Máximo {{ maxSizeMB }}MB
        </p>
      </div>

      <!-- PROGRESS BAR (durante subida simulada) -->
      <div v-if="isUploading" class="upload-progress">
        <VaProgressBar 
          :model-value="uploadProgress" 
          color="purple"
        />
        <p class="progress-text">Subiendo... {{ uploadProgress }}%</p>
      </div>
    </div>

    <!-- LISTA DE ARCHIVOS -->
    <div v-if="files.length" class="files-list">
      <TransitionGroup name="file-list">
        <div
          v-for="(file, index) in files"
          :key="file.id"
          class="file-item"
        >
          <!-- ÍCONO DEL ARCHIVO -->
          <div class="file-icon">
            <va-icon 
              :name="getFileIcon(file)" 
              size="2rem"
              color="purple"
            />
          </div>

          <!-- INFO DEL ARCHIVO -->
          <div class="file-info">
            <h4 class="file-name">{{ file.name }}</h4>
            <p class="file-meta">
              {{ formatFileSize(file.size) }}
              <span v-if="file.uploadedAt" class="file-date">
                • Subido {{ formatDate(file.uploadedAt) }}
              </span>
            </p>
            
            <!-- PROGRESS BAR POR ARCHIVO -->
            <VaProgressBar 
              v-if="file.uploading"
              :model-value="file.progress" 
              color="purple"
              size="small"
            />

            <!-- BADGES DE ESTADO -->
            <div class="file-badges">
              <VaBadge 
                v-if="file.uploaded"
                color="success"
                text="Subido"
              />
              <VaBadge 
                v-if="file.error"
                color="danger"
                :text="file.error"
              />
            </div>
          </div>

          <!-- ACCIONES -->
          <div class="file-actions">
            <!-- Ver/Descargar -->
            <VaButton
              v-if="file.uploaded"
              preset="plain"
              icon="visibility"
              @click="previewFile(file)"
              title="Ver archivo"
            />

            <!-- Eliminar -->
            <VaButton
              preset="plain"
              icon="delete"
              color="danger"
              @click="removeFile(index)"
              title="Eliminar"
            />
          </div>
        </div>
      </TransitionGroup>
    </div>

    <!-- MENSAJE DE ERROR -->
    <VaAlert
      v-if="error"
      color="danger"
      closeable
      @close="error = null"
      class="error-alert"
    >
      {{ error }}
    </VaAlert>

    <!-- BOTÓN PARA AGREGAR MÁS (si multiple) -->
    <VaButton
      v-if="multiple && files.length > 0"
      preset="secondary"
      @click="openFileDialog"
      block
      class="add-more-btn"
    >
      <va-icon name="add" />
      Agregar más archivos
    </VaButton>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useToast } from 'vuestic-ui'

// ========== PROPS ==========
const props = defineProps({
  // Tipos de archivo permitidos
  accept: {
    type: String,
    default: '.pdf,.doc,.docx'
  },
  // Tamaño máximo en MB
  maxSize: {
    type: Number,
    default: 5
  },
  // Permitir múltiples archivos
  multiple: {
    type: Boolean,
    default: false
  },
  // Tipo de archivo para el texto
  fileType: {
    type: String,
    default: 'CV'
  }
})

// ========== EMITS ==========
const emit = defineEmits(['upload', 'remove', 'error'])

// ========== COMPOSABLES ==========
const { init: notify } = useToast()

// ========== STATE ==========
const fileInput = ref(null)
const files = ref([])
const isDragging = ref(false)
const dragCounter = ref(0)
const error = ref(null)
const isUploading = ref(false)
const uploadProgress = ref(0)

// ========== COMPUTED ==========
const acceptedTypes = computed(() => props.accept)

const maxSizeMB = computed(() => props.maxSize)

const maxSizeBytes = computed(() => props.maxSize * 1024 * 1024)

const fileTypeText = computed(() => props.fileType)

const allowedTypesText = computed(() => {
  const extensions = props.accept.split(',').map(ext => ext.trim().toUpperCase())
  return extensions.join(', ')
})

// ========== METHODS ==========
const openFileDialog = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  processFiles(selectedFiles)
}

const handleDragEnter = (event) => {
  dragCounter.value++
  isDragging.value = true
}

const handleDragOver = (event) => {
  event.dataTransfer.dropEffect = 'copy'
}

const handleDragLeave = (event) => {
  dragCounter.value--
  if (dragCounter.value === 0) {
    isDragging.value = false
  }
}

const handleDrop = (event) => {
  dragCounter.value = 0
  isDragging.value = false
  
  const droppedFiles = Array.from(event.dataTransfer.files)
  processFiles(droppedFiles)
}

const processFiles = (fileList) => {
  error.value = null

  // Si no es múltiple, solo procesar el primero
  if (!props.multiple && fileList.length > 1) {
    notify({
      message: 'Solo puedes subir un archivo',
      color: 'warning'
    })
    fileList = [fileList[0]]
  }

  // Validar cada archivo
  for (const file of fileList) {
    if (validateFile(file)) {
      addFile(file)
    }
  }
}

const validateFile = (file) => {
  // Validar tipo
  const extension = '.' + file.name.split('.').pop().toLowerCase()
  const allowedExtensions = props.accept.split(',').map(ext => ext.trim())
  
  if (!allowedExtensions.includes(extension)) {
    error.value = `Tipo de archivo no permitido: ${extension}`
    notify({
      message: error.value,
      color: 'danger'
    })
    emit('error', error.value)
    return false
  }

  // Validar tamaño
  if (file.size > maxSizeBytes.value) {
    error.value = `El archivo supera el tamaño máximo de ${props.maxSize}MB`
    notify({
      message: error.value,
      color: 'danger'
    })
    emit('error', error.value)
    return false
  }

  return true
}

const addFile = (file) => {
  const fileObj = {
    id: Date.now() + Math.random(),
    file: file,
    name: file.name,
    size: file.size,
    type: file.type,
    uploading: false,
    uploaded: false,
    progress: 0,
    error: null,
    uploadedAt: null,
    url: null // Se asignará después de "subir"
  }

  // Si no es múltiple, reemplazar archivo existente
  if (!props.multiple) {
    files.value = [fileObj]
  } else {
    files.value.push(fileObj)
  }

  // Simular subida
  uploadFile(fileObj)
}

const uploadFile = (fileObj) => {
  // TODO: Aquí irá la subida real al backend
  // Por ahora, simularemos el upload
  
  fileObj.uploading = true
  fileObj.progress = 0

  // Simular progreso
  const interval = setInterval(() => {
    fileObj.progress += 10
    
    if (fileObj.progress >= 100) {
      clearInterval(interval)
      fileObj.uploading = false
      fileObj.uploaded = true
      fileObj.uploadedAt = new Date()
      
      // Crear URL temporal para preview (solo funciona en navegador)
      if (fileObj.file) {
        fileObj.url = URL.createObjectURL(fileObj.file)
      }
      
      notify({
        message: `✅ ${fileObj.name} subido correctamente`,
        color: 'success'
      })
      
      emit('upload', fileObj)
    }
  }, 200)
}

const removeFile = (index) => {
  const file = files.value[index]
  
  // Revocar URL si existe
  if (file.url) {
    URL.revokeObjectURL(file.url)
  }
  
  files.value.splice(index, 1)
  
  notify({
    message: `🗑️ ${file.name} eliminado`,
    color: 'info'
  })
  
  emit('remove', file)
  
  // Resetear input
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const previewFile = (file) => {
  if (file.url) {
    window.open(file.url, '_blank')
  } else {
    notify({
      message: '⚠️ No se puede previsualizar este archivo',
      color: 'warning'
    })
  }
}

const getFileIcon = (file) => {
  const ext = file.name.split('.').pop().toLowerCase()
  
  const iconMap = {
    pdf: 'picture_as_pdf',
    doc: 'description',
    docx: 'description',
    txt: 'text_snippet',
    jpg: 'image',
    jpeg: 'image',
    png: 'image',
    gif: 'image',
    zip: 'folder_zip',
    rar: 'folder_zip'
  }
  
  return iconMap[ext] || 'insert_drive_file'
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (date) => {
  if (!(date instanceof Date)) return ''
  
  const now = new Date()
  const diff = now - date
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  
  if (seconds < 60) return 'hace unos segundos'
  if (minutes < 60) return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`
  if (hours < 24) return `hace ${hours} hora${hours > 1 ? 's' : ''}`
  
  return date.toLocaleDateString()
}

// ========== EXPOSE ==========
defineExpose({
  files,
  openFileDialog,
  removeFile
})
</script>

<style scoped>
/* ========== CONTAINER ========== */
.file-upload-container {
  width: 100%;
}

/* ========== DROP ZONE ========== */
.drop-zone {
  border: 2px dashed #CCC;
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.drop-zone:hover {
  border-color: var(--color-purple);
  background: rgba(92, 0, 153, 0.02);
}

.drop-zone.drag-over {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.05);
  transform: scale(1.02);
}

.drop-zone.has-error {
  border-color: #F44336;
}

.upload-icon {
  margin-bottom: 1.5rem;
}

.upload-text {
  margin-bottom: 1rem;
}

.main-text {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.main-text strong {
  color: var(--color-purple);
}

.hint-text {
  font-size: 0.9rem;
  color: #999;
  margin: 0;
}

.upload-progress {
  max-width: 400px;
  margin: 1.5rem auto 0;
}

.progress-text {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-purple);
  font-weight: 600;
}

/* ========== FILES LIST ========== */
.files-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: white;
  border: 2px solid #E0E0E0;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.file-item:hover {
  border-color: var(--color-purple);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.file-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(92, 0, 153, 0.1);
  border-radius: 10px;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-meta {
  font-size: 0.85rem;
  color: #666;
  margin: 0 0 0.5rem;
}

.file-date {
  color: #999;
}

.file-badges {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.file-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

/* ========== TRANSITIONS ========== */
.file-list-enter-active,
.file-list-leave-active {
  transition: all 0.3s ease;
}

.file-list-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.file-list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* ========== ERROR ALERT ========== */
.error-alert {
  margin-top: 1rem;
}

/* ========== ADD MORE BUTTON ========== */
.add-more-btn {
  margin-top: 1rem;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .drop-zone {
    padding: 2rem 1rem;
  }

  .file-item {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }

  .file-info {
    width: 100%;
  }

  .file-actions {
    width: 100%;
    justify-content: center;
  }
}
</style>