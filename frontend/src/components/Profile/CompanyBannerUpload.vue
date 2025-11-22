<!-- frontend/src/components/Profile/CompanyBannerUpload.vue -->
<template>
  <div class="banner-upload-container">
    <div class="upload-box">
      <!-- Display Current Banner or Placeholder -->
      <div class="banner-display">
        <img
          v-if="previewUrl || companyBanner"
          :src="previewUrl || companyBanner"
          alt="Company Banner"
          class="banner-image"
        />
        <div v-else class="banner-placeholder">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
      </div>

      <!-- Message if no company ID -->
      <div v-if="!companyId" class="no-company-notice">
        <p>Guarda la empresa primero para poder subir un banner</p>
      </div>

      <!-- Upload Controls -->
      <div v-else class="upload-controls">
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
          :disabled="isUploading"
        >
          <span v-if="!isUploading">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            {{ selectedFile ? 'Guardar Banner' : 'Subir Banner' }}
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
          v-if="companyBanner && !previewUrl"
          type="button"
          class="upload-btn danger"
          @click="handleDeleteBanner"
          :disabled="isDeleting"
        >
          <span v-if="!isDeleting">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 4 21 4 23 6 23 20a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V6"></polyline>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
              <line x1="4" y1="6" x2="20" y2="6"></line>
            </svg>
            Eliminar Banner
          </span>
          <span v-else class="spinner"></span>
        </button>

        <!-- File Info -->
        <div v-if="selectedFile" class="file-info">
          <p>Archivo: {{ selectedFile.name }}</p>
          <p>Tamaño: {{ formatFileSize(selectedFile.size) }}</p>
        </div>

        <!-- Error Message -->
        <div v-if="errorMsg" class="error-message">
          <p>{{ errorMsg }}</p>
        </div>

        <!-- Success Message -->
        <div v-if="successMsg" class="success-message">
          <p>{{ successMsg }}</p>
        </div>

        <!-- Help Text -->
        <p class="help-text">
          JPG, PNG o GIF. Máximo 10MB. Recomendado: 1200x300px
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCompanyLogoUpload } from '@/composables/useCompanyLogoUpload'

// ========== PROPS ==========
const props = defineProps({
  companyId: {
    type: [String, null],
    default: null
  },
  companyBanner: {
    type: String,
    default: null
  }
})

// ========== EMITS ==========
const emit = defineEmits(['banner-uploaded', 'banner-deleted'])

// ========== COMPOSABLES ==========
const logoUpload = useCompanyLogoUpload()

// ========== DATA ==========
const fileInput = ref(null)
const selectedFile = ref(null)
const previewUrl = ref(null)

const errorMsg = computed(() => logoUpload.uploadError.value)
const successMsg = computed(() => logoUpload.uploadSuccess.value)
const isUploading = computed(() => logoUpload.isUploading.value)
const isDeleting = computed(() => logoUpload.isDeleting.value)

// ========== METHODS ==========
const handleFileSelect = (event) => {
  logoUpload.clearMessages()
  const file = event.target.files?.[0]

  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    logoUpload.uploadError.value = 'Por favor selecciona un archivo de imagen válido'
    return
  }

  // Validate file size (10MB para banner)
  if (file.size > 10 * 1024 * 1024) {
    logoUpload.uploadError.value = 'El archivo es demasiado grande. Máximo 10MB'
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
  logoUpload.clearMessages()
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handleUpload = async () => {
  if (!selectedFile.value || !props.companyId) return

  // Usar el mismo composable pero con "banner" como tipo de archivo
  const result = await logoUpload.uploadCompanyLogo(props.companyId, selectedFile.value)

  if (result.success) {
    clearPreview()
    setTimeout(() => {
      logoUpload.uploadSuccess.value = null
    }, 3000)
    emit('banner-uploaded', result.logoUrl)
  }
}

const handleDeleteBanner = async () => {
  if (!props.companyId) return

  if (!confirm('¿Estás seguro de que deseas eliminar el banner de la empresa?')) {
    return
  }

  const result = await logoUpload.deleteCompanyLogo(props.companyId)

  if (result.success) {
    setTimeout(() => {
      logoUpload.uploadSuccess.value = null
    }, 3000)
    emit('banner-deleted')
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
.banner-upload-container {
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.upload-box {
  text-align: center;
}

.banner-display {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 8px;
  padding: 1rem;
  min-height: 180px;
  align-items: center;
}

.banner-image {
  width: 100%;
  max-width: 500px;
  max-height: 160px;
  object-fit: cover;
  border-radius: 4px;
  border: 2px solid #7c3aed;
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

.banner-placeholder {
  width: 100%;
  max-width: 500px;
  height: 140px;
  border-radius: 4px;
  background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
  border: 2px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.no-company-notice {
  padding: 1rem;
  background: #fef3c7;
  border: 1px solid #fcd34d;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.no-company-notice p {
  margin: 0;
  color: #92400e;
  font-size: 0.9rem;
  font-weight: 500;
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
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
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
  width: 100%;
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
  width: 100%;
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
  width: 100%;
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
  .banner-upload-container {
    padding: 1rem;
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
