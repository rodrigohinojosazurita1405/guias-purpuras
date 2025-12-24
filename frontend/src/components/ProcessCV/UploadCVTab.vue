<template>
  <div class="upload-cv-container">
    <!-- Upload Zone -->
    <div
      class="upload-zone"
      :class="{ 'drag-over': isDragOver, 'has-file': file }"
      @drop.prevent="handleDrop"
      @dragover.prevent="isDragOver = true"
      @dragleave.prevent="isDragOver = false"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".pdf,.doc,.docx"
        @change="handleFileSelect"
        style="display: none"
      />

      <template v-if="!file">
        <va-icon name="cloud_upload" size="3rem" color="#7C3AED" />
        <h3 class="upload-title">Arrastra tu CV aquí</h3>
        <p class="upload-subtitle">o haz clic para seleccionar un archivo</p>
        <p class="upload-hint">Formatos: PDF, DOC, DOCX (máx. 5 MB)</p>
      </template>

      <template v-else>
        <va-icon name="description" size="3rem" color="#10B981" />
        <h3 class="upload-title">{{ file.name }}</h3>
        <p class="upload-subtitle">{{ formatFileSize(file.size) }}</p>
        <button class="remove-file-btn" @click.stop="removeFile">
          <va-icon name="delete" size="small" />
          Cambiar archivo
        </button>
      </template>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      <va-icon name="error" size="small" />
      <span>{{ error }}</span>
    </div>

    <!-- Cover Letter -->
    <div class="cover-letter-section">
      <label class="section-label">
        <va-icon name="edit_note" size="small" />
        Carta de Presentación (Opcional)
      </label>
      <va-textarea
        :model-value="coverLetter"
        @update:model-value="$emit('update:coverLetter', $event)"
        placeholder="Escribe una breve carta de presentación destacando tu interés en la posición y por qué eres el candidato ideal..."
        :min-rows="4"
        :max-rows="8"
        counter
        :max-length="1000"
      />
      <p class="field-hint">Una buena carta de presentación puede aumentar tus posibilidades de ser seleccionado.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  file: {
    type: File,
    default: null
  },
  coverLetter: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:file', 'update:coverLetter'])

const fileInput = ref(null)
const isDragOver = ref(false)
const error = ref('')
const file = ref(props.file)

const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5 MB

watch(() => props.file, (newValue) => {
  file.value = newValue
})

const validateFile = (selectedFile) => {
  error.value = ''

  if (!selectedFile) {
    return false
  }

  const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  if (!allowedTypes.includes(selectedFile.type)) {
    error.value = 'Solo se permiten archivos PDF, DOC o DOCX'
    return false
  }

  if (selectedFile.size > MAX_FILE_SIZE) {
    error.value = 'El archivo no debe superar los 5 MB'
    return false
  }

  return true
}

const handleFileSelect = (event) => {
  const selectedFile = event.target.files[0]
  if (validateFile(selectedFile)) {
    file.value = selectedFile
    emit('update:file', selectedFile)
  }
}

const handleDrop = (event) => {
  isDragOver.value = false
  const selectedFile = event.dataTransfer.files[0]
  if (validateFile(selectedFile)) {
    file.value = selectedFile
    emit('update:file', selectedFile)
  }
}

const triggerFileInput = () => {
  fileInput.value.click()
}

const removeFile = () => {
  file.value = null
  emit('update:file', null)
  error.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}
</script>

<style scoped>
.upload-cv-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.upload-zone {
  border: 2px dashed #D1D5DB;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #F9FAFB;
}

.upload-zone:hover {
  border-color: #7C3AED;
  background: #F5F3FF;
}

.upload-zone.drag-over {
  border-color: #7C3AED;
  background: #EDE9FE;
  transform: scale(1.02);
}

.upload-zone.has-file {
  border-color: #10B981;
  background: #F0FDF4;
}

.upload-title {
  margin: 1rem 0 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}

.upload-subtitle {
  margin: 0;
  font-size: 0.9375rem;
  color: #6B7280;
}

.upload-hint {
  margin: 0.75rem 0 0;
  font-size: 0.8125rem;
  color: #9CA3AF;
}

.remove-file-btn {
  margin-top: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-file-btn:hover {
  background: #F3F4F6;
  border-color: #D1D5DB;
  color: #DC2626;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #FEF2F2;
  border: 1px solid #FECACA;
  border-radius: 8px;
  color: #991B1B;
  font-size: 0.875rem;
  font-weight: 500;
}

.cover-letter-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #111827;
}

.field-hint {
  margin: 0;
  font-size: 0.8125rem;
  color: #6B7280;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .upload-zone {
    padding: 2rem 1.5rem;
  }

  .upload-title {
    font-size: 1rem;
  }
}
</style>
