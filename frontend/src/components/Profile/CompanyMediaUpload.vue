<!-- frontend/src/components/Profile/CompanyMediaUpload.vue -->
<template>
  <div class="media-upload-container">
    <!-- Logo Section -->
    <div class="media-section">
      <h4 class="section-label">Logo</h4>
      <div class="media-display">
        <img
          v-if="logoPreviewUrl || companyLogo"
          :src="logoPreviewUrl || companyLogo"
          alt="Company Logo"
          class="media-image"
        />
        <div v-else class="media-placeholder">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
            <polyline points="13 2 13 9 20 9"></polyline>
          </svg>
        </div>
      </div>

      <div class="upload-controls">
        <input
          ref="logoFileInput"
          type="file"
          accept="image/*"
          hidden
          @change="handleLogoFileSelect"
        />

        <button
          type="button"
          class="upload-btn primary"
          @click="logoFileInput.click()"
          :disabled="isUploadingLogo || !companyId"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
          {{ selectedLogoFile ? 'Cambiar Logo' : 'Subir Logo' }}
        </button>

        <button
          v-if="logoPreviewUrl"
          type="button"
          class="upload-btn secondary"
          @click="clearLogoPreview"
          :disabled="isUploadingLogo"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 4 21 4 23 6 23 20a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V6"></polyline>
            <line x1="10" y1="11" x2="10" y2="17"></line>
            <line x1="14" y1="11" x2="14" y2="17"></line>
          </svg>
          Limpiar
        </button>

      </div>

      <div v-if="selectedLogoFile" class="file-info">
        <p>{{ selectedLogoFile.name }}</p>
      </div>
    </div>

    <!-- Banner Section -->
    <div class="media-section">
      <h4 class="section-label">Banner</h4>
      <div class="media-display banner">
        <img
          v-if="bannerPreviewUrl || companyBanner"
          :src="bannerPreviewUrl || companyBanner"
          alt="Company Banner"
          class="media-image"
        />
        <div v-else class="media-placeholder">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
            <polyline points="13 2 13 9 20 9"></polyline>
          </svg>
        </div>
      </div>

      <div class="upload-controls">
        <input
          ref="bannerFileInput"
          type="file"
          accept="image/*"
          hidden
          @change="handleBannerFileSelect"
        />

        <button
          type="button"
          class="upload-btn primary"
          @click="bannerFileInput.click()"
          :disabled="isUploadingBanner || !companyId"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
          {{ selectedBannerFile ? 'Cambiar Banner' : 'Subir Banner' }}
        </button>

        <button
          v-if="bannerPreviewUrl"
          type="button"
          class="upload-btn secondary"
          @click="clearBannerPreview"
          :disabled="isUploadingBanner"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 4 21 4 23 6 23 20a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V6"></polyline>
            <line x1="10" y1="11" x2="10" y2="17"></line>
            <line x1="14" y1="11" x2="14" y2="17"></line>
          </svg>
          Limpiar
        </button>

      </div>

      <div v-if="selectedBannerFile" class="file-info">
        <p>{{ selectedBannerFile.name }}</p>
      </div>
    </div>

    <!-- Help Text -->
    <p class="help-text">Logo: JPG, PNG o GIF. Máximo 5MB | Banner: JPG, PNG o GIF. Máximo 10MB. Los cambios se guardarán al hacer clic en "Guardar Cambios"</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCompanyStore } from '@/stores/useCompanyStore'

const props = defineProps({
  companyId: {
    type: [String, null],
    default: null
  },
  companyLogo: {
    type: String,
    default: null
  },
  companyBanner: {
    type: String,
    default: null
  }
})

const companyStore = useCompanyStore()

const logoFileInput = ref(null)
const bannerFileInput = ref(null)
const selectedLogoFile = ref(null)
const selectedBannerFile = ref(null)
const logoPreviewUrl = ref(null)
const bannerPreviewUrl = ref(null)
const isUploadingLogo = ref(false)
const isUploadingBanner = ref(false)
const isDeletingLogo = ref(false)
const isDeletingBanner = ref(false)
const uploadError = ref(null)
const uploadSuccess = ref(null)

const MAX_LOGO_SIZE = 5 * 1024 * 1024 // 5MB
const MAX_BANNER_SIZE = 10 * 1024 * 1024 // 10MB

// Logo handlers
const handleLogoFileSelect = (event) => {
  uploadError.value = null
  uploadSuccess.value = null
  const file = event.target.files?.[0]

  if (!file) return

  if (!file.type.startsWith('image/')) {
    uploadError.value = 'Por favor selecciona una imagen válida'
    return
  }

  if (file.size > MAX_LOGO_SIZE) {
    uploadError.value = 'El logo es demasiado grande. Máximo 5MB'
    return
  }

  selectedLogoFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    logoPreviewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const clearLogoPreview = () => {
  selectedLogoFile.value = null
  logoPreviewUrl.value = null
  uploadError.value = null
  uploadSuccess.value = null
  if (logoFileInput.value) {
    logoFileInput.value.value = ''
  }
}

const handleUploadLogo = async () => {
  if (!selectedLogoFile.value || !props.companyId) return

  isUploadingLogo.value = true
  uploadError.value = null
  uploadSuccess.value = null

  try {
    const result = await companyStore.uploadCompanyLogo(props.companyId, selectedLogoFile.value)

    if (result.success) {
      uploadSuccess.value = 'Logo actualizado exitosamente'
      clearLogoPreview()
      setTimeout(() => {
        uploadSuccess.value = null
      }, 3000)
    } else {
      uploadError.value = result.error || 'Error al cargar el logo'
    }
  } catch (err) {
    uploadError.value = err.message || 'Error al cargar el logo'
  } finally {
    isUploadingLogo.value = false
  }
}

const handleDeleteLogo = async () => {
  if (!props.companyId) return

  if (!confirm('¿Estás seguro de que deseas eliminar el logo?')) {
    return
  }

  isDeletingLogo.value = true
  uploadError.value = null
  uploadSuccess.value = null

  try {
    const result = await companyStore.deleteCompanyLogo(props.companyId)

    if (result.success) {
      uploadSuccess.value = 'Logo eliminado exitosamente'
      setTimeout(() => {
        uploadSuccess.value = null
      }, 3000)
    } else {
      uploadError.value = result.error || 'Error al eliminar el logo'
    }
  } catch (err) {
    uploadError.value = err.message || 'Error al eliminar el logo'
  } finally {
    isDeletingLogo.value = false
  }
}

// Banner handlers
const handleBannerFileSelect = (event) => {
  uploadError.value = null
  uploadSuccess.value = null
  const file = event.target.files?.[0]

  if (!file) return

  if (!file.type.startsWith('image/')) {
    uploadError.value = 'Por favor selecciona una imagen válida'
    return
  }

  if (file.size > MAX_BANNER_SIZE) {
    uploadError.value = 'El banner es demasiado grande. Máximo 10MB'
    return
  }

  selectedBannerFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    bannerPreviewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const clearBannerPreview = () => {
  selectedBannerFile.value = null
  bannerPreviewUrl.value = null
  uploadError.value = null
  uploadSuccess.value = null
  if (bannerFileInput.value) {
    bannerFileInput.value.value = ''
  }
}

const handleUploadBanner = async () => {
  if (!selectedBannerFile.value || !props.companyId) return

  isUploadingBanner.value = true
  uploadError.value = null
  uploadSuccess.value = null

  try {
    const result = await companyStore.uploadCompanyBanner(props.companyId, selectedBannerFile.value)

    if (result.success) {
      uploadSuccess.value = 'Banner actualizado exitosamente'
      clearBannerPreview()
      setTimeout(() => {
        uploadSuccess.value = null
      }, 3000)
    } else {
      uploadError.value = result.error || 'Error al cargar el banner'
    }
  } catch (err) {
    uploadError.value = err.message || 'Error al cargar el banner'
  } finally {
    isUploadingBanner.value = false
  }
}

const handleDeleteBanner = async () => {
  if (!props.companyId) return

  if (!confirm('¿Estás seguro de que deseas eliminar el banner?')) {
    return
  }

  isDeletingBanner.value = true
  uploadError.value = null
  uploadSuccess.value = null

  try {
    const result = await companyStore.deleteCompanyBanner(props.companyId)

    if (result.success) {
      uploadSuccess.value = 'Banner eliminado exitosamente'
      setTimeout(() => {
        uploadSuccess.value = null
      }, 3000)
    } else {
      uploadError.value = result.error || 'Error al eliminar el banner'
    }
  } catch (err) {
    uploadError.value = err.message || 'Error al eliminar el banner'
  } finally {
    isDeletingBanner.value = false
  }
}

// Métodos para obtener archivos (usados por CompanyProfileEdit)
const getSelectedLogoFile = () => {
  return selectedLogoFile.value
}

const getSelectedBannerFile = () => {
  return selectedBannerFile.value
}

// Exposer métodos publicamente
defineExpose({
  getSelectedLogoFile,
  getSelectedBannerFile,
  clearLogoPreview,
  clearBannerPreview
})
</script>

<style scoped>
.media-upload-container {
  padding: 0;
}

.media-section {
  margin-bottom: 2rem;
}

.section-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 0.75rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.media-display {
  width: 100%;
  height: 150px;
  border-radius: 8px;
  overflow: hidden;
  background: #f5f5f5;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.media-display.banner {
  height: 100px;
  aspect-ratio: 851 / 315;
}

.media-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.media-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
  background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
}

.upload-controls {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.75rem;
}

.upload-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.upload-btn svg {
  flex-shrink: 0;
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

.upload-btn.secondary:hover:not(:disabled) {
  background: #efefef;
  border-color: #bbb;
}

.upload-btn.danger {
  background: #dc2626;
  color: white;
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
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.file-info {
  background: #f5f5f5;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  text-align: left;
}

.file-info p {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  border: 1px solid #f5c6cb;
}

.error-message p {
  margin: 0;
  font-size: 0.85rem;
}

.success-message {
  background: #d4edda;
  color: #155724;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  border: 1px solid #c3e6cb;
}

.success-message p {
  margin: 0;
  font-size: 0.85rem;
}

.help-text {
  color: #999;
  font-size: 0.75rem;
  margin: 0.5rem 0 0 0;
  line-height: 1.4;
}
</style>
