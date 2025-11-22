<template>
  <div class="avatar-upload-container">
    <div class="upload-box">
      <!-- Display Current Avatar or Placeholder -->
      <div class="avatar-display">
        <img
          v-if="previewUrl || profileStore.userProfile?.profilePhoto"
          :src="previewUrl || profileStore.userProfile.profilePhoto"
          alt="Profile Avatar"
          class="avatar-image"
        />
        <div v-else class="avatar-placeholder">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
      </div>

      <!-- Upload Controls -->
      <div class="upload-controls">
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          hidden
          @change="handleFileSelect"
        />

        <button
          type="button"
          class="upload-btn primary"
          @click="!selectedFile ? fileInput.click() : handleUpload()"
          :disabled="isUploading || !userProfileId"
        >
          <span v-if="!isUploading">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            {{ selectedFile ? 'Guardar Foto' : 'Subir Foto' }}
          </span>
          <span v-else class="spinner"></span>
        </button>

        <button
          v-if="previewUrl"
          type="button"
          class="upload-btn secondary"
          @click="clearPreview"
          :disabled="isUploading"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 4 21 4 23 6 23 20a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V6"></polyline>
            <line x1="10" y1="11" x2="10" y2="17"></line>
            <line x1="14" y1="11" x2="14" y2="17"></line>
            <line x1="4" y1="6" x2="20" y2="6"></line>
          </svg>
          Limpiar
        </button>

        <button
          v-if="profileStore.userProfile?.profilePhoto && !previewUrl"
          type="button"
          class="upload-btn danger"
          @click="handleDeletePhoto"
          :disabled="isDeleting || !userProfileId"
        >
          <span v-if="!isDeleting">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 4 21 4 23 6 23 20a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V6"></polyline>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
              <line x1="4" y1="6" x2="20" y2="6"></line>
            </svg>
            Eliminar Foto
          </span>
          <span v-else class="spinner"></span>
        </button>
      </div>

      <!-- File Info -->
      <div v-if="selectedFile" class="file-info">
        <p>Archivo: {{ selectedFile.name }}</p>
        <p>Tamaño: {{ formatFileSize(selectedFile.size) }}</p>
      </div>

      <!-- Error Message -->
      <div v-if="uploadError" class="error-message">
        <p>{{ uploadError }}</p>
      </div>

      <!-- Success Message -->
      <div v-if="uploadSuccess" class="success-message">
        <p>{{ uploadSuccess }}</p>
      </div>

      <!-- Help Text -->
      <p class="help-text">
        JPG, PNG o GIF. Máximo 5MB.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useProfileStore } from '@/stores/useProfileStore'

const props = defineProps({
  userProfileId: {
    type: [String, null],
    default: null
  }
})

const profileStore = useProfileStore()

const fileInput = ref(null)
const selectedFile = ref(null)
const previewUrl = ref(null)
const isUploading = ref(false)
const isDeleting = ref(false)
const uploadError = ref(null)
const uploadSuccess = ref(null)

const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB

const handleFileSelect = (event) => {
  uploadError.value = null
  uploadSuccess.value = null
  const file = event.target.files?.[0]

  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    uploadError.value = 'Por favor selecciona un archivo de imagen válido'
    return
  }

  // Validate file size
  if (file.size > MAX_FILE_SIZE) {
    uploadError.value = `El archivo es demasiado grande. Máximo ${MAX_FILE_SIZE / 1024 / 1024}MB`
    return
  }

  selectedFile.value = file

  // Create preview
  const reader = new FileReader()
  reader.onload = (e) => {
    previewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const clearPreview = () => {
  selectedFile.value = null
  previewUrl.value = null
  uploadError.value = null
  uploadSuccess.value = null
  if (fileInput.value) {
    fileInput.value.value = '' // Limpiar el input file
  }
}

const handleUpload = async () => {
  if (!selectedFile.value || !props.userProfileId) return

  isUploading.value = true
  uploadError.value = null
  uploadSuccess.value = null

  try {
    const result = await profileStore.uploadProfilePhoto(props.userProfileId, selectedFile.value)

    if (result.success) {
      uploadSuccess.value = 'Foto de perfil actualizada exitosamente'
      clearPreview()
      // Auto-clear success message after 3 seconds
      setTimeout(() => {
        uploadSuccess.value = null
      }, 3000)
    } else {
      uploadError.value = result.error || 'Error al cargar la foto'
    }
  } catch (err) {
    uploadError.value = err.message || 'Error al cargar la foto'
  } finally {
    isUploading.value = false
  }
}

const handleDeletePhoto = async () => {
  if (!props.userProfileId) return

  // Confirm deletion
  if (!confirm('¿Estás seguro de que deseas eliminar tu foto de perfil?')) {
    return
  }

  isDeleting.value = true
  uploadError.value = null
  uploadSuccess.value = null

  try {
    const result = await profileStore.deleteProfilePhoto(props.userProfileId)

    if (result.success) {
      uploadSuccess.value = 'Foto de perfil eliminada exitosamente'
      // Auto-clear success message after 3 seconds
      setTimeout(() => {
        uploadSuccess.value = null
      }, 3000)
    } else {
      uploadError.value = result.error || 'Error al eliminar la foto'
    }
  } catch (err) {
    uploadError.value = err.message || 'Error al eliminar la foto'
  } finally {
    isDeleting.value = false
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
.avatar-upload-container {
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.upload-box {
  text-align: center;
}

.avatar-display {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}

.avatar-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #7c3aed;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
  animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes popIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.avatar-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
  border: 4px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.upload-controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-btn.primary {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
}

.upload-btn.primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px #7c3aed4d;
}

.upload-btn.secondary {
  background: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
}

.upload-btn.secondary:hover {
  background: #efefef;
  border-color: #bbb;
}

.upload-btn.danger {
  background: #dc2626;
  color: white;
  border: none;
}

.upload-btn.danger:hover:not(:disabled) {
  background: #991b1b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.file-info {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: left;
}

.file-info p {
  margin: 0.25rem 0;
  font-size: 0.85rem;
  color: #666;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid #f5c6cb;
}

.error-message p {
  margin: 0;
  font-size: 0.95rem;
}

.success-message {
  background: #d4edda;
  color: #155724;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid #c3e6cb;
}

.success-message p {
  margin: 0;
  font-size: 0.95rem;
}

.help-text {
  color: #999;
  font-size: 0.85rem;
  margin: 0;
}

@media (max-width: 600px) {
  .avatar-upload-container {
    padding: 1.5rem;
  }

  .upload-controls {
    flex-direction: column;
  }

  .upload-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
