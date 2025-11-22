<!-- frontend/src/components/Profile/CompanyLogoUpload.vue -->
<template>
  <div class="company-media-container">
    <!-- Contenedor Horizontal: Banner y Logo lado a lado -->
    <div class="media-row">
      <!-- SECCIÓN BANNER (Izquierda) -->
      <div class="media-section banner-section">
        <!-- Banner Display -->
        <div class="media-display banner-display">
          <div
            v-if="bannerPreviewUrl || companyBanner"
            class="banner-preview"
            :style="{ backgroundImage: `url('${bannerPreviewUrl || companyBanner}')` }"
          ></div>
          <div v-else class="banner-placeholder">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2"></rect>
              <circle cx="8.5" cy="8.5" r="1.5"></circle>
              <path d="M21 15l-5-5L5 21"></path>
            </svg>
          </div>
        </div>

        <!-- Banner Label -->
        <p class="media-label">Banner</p>

        <!-- Banner Controls -->
        <div class="media-controls">
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
            @click="() => bannerFileInput.click()"
            title="Subir banner"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            Subir
          </button>
          <button
            v-if="bannerPreviewUrl || companyBanner"
            type="button"
            class="upload-btn secondary"
            @click="clearBannerPreview"
            title="Eliminar banner"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6z"></path>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
            </svg>
            Eliminar
          </button>
        </div>

        <!-- Banner File Info -->
        <div v-if="selectedBannerFile" class="file-name">
          {{ selectedBannerFile.name }}
        </div>
      </div>

      <!-- SECCIÓN LOGO (Derecha) -->
      <div class="media-section logo-section">
        <!-- Logo Display -->
        <div class="media-display logo-display">
          <img
            v-if="logoPreviewUrl || companyLogo"
            :src="logoPreviewUrl || companyLogo"
            alt="Company Logo"
            class="logo-image"
          />
          <div v-else class="logo-placeholder">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
              <polyline points="13 2 13 9 20 9"></polyline>
            </svg>
          </div>
        </div>

        <!-- Logo Label -->
        <p class="media-label">Logo</p>

        <!-- Logo Controls -->
        <div class="media-controls">
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
            @click="() => logoFileInput.click()"
            title="Subir logo"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            Subir
          </button>
          <button
            v-if="logoPreviewUrl || companyLogo"
            type="button"
            class="upload-btn secondary"
            @click="clearLogoPreview"
            title="Eliminar logo"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6z"></path>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
            </svg>
            Eliminar
          </button>
        </div>

        <!-- Logo File Info -->
        <div v-if="selectedLogoFile" class="file-name">
          {{ selectedLogoFile.name }}
        </div>
      </div>
    </div>

    <!-- Help Text -->
    <p class="help-text">
      Logo: JPG, PNG o GIF. Máximo 5MB. | Banner: Máximo 10MB. (851 x 315px)
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCompanyStore } from '@/stores/useCompanyStore'

// ========== PROPS ==========
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

// ========== EMITS ==========
const emit = defineEmits(['logo-selected', 'banner-selected', 'logo-cleared', 'banner-cleared', 'logo-deleted', 'banner-deleted'])

// ========== STORE ==========
const companyStore = useCompanyStore()

// ========== DATA ==========
const logoFileInput = ref(null)
const bannerFileInput = ref(null)
const selectedLogoFile = ref(null)
const selectedBannerFile = ref(null)
const logoPreviewUrl = ref(null)
const bannerPreviewUrl = ref(null)

// ========== METHODS ==========
// ========== MÉTODOS DE LOGO ==========
const handleLogoFileSelect = (event) => {
  const file = event.target.files?.[0]

  if (!file) return

  if (!file.type.startsWith('image/')) {
    alert('Por favor selecciona un archivo de imagen válido')
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    alert('El archivo es demasiado grande. Máximo 5MB')
    return
  }

  selectedLogoFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    logoPreviewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)

  emit('logo-selected', file)
}

const clearLogoPreview = async () => {
  // Si existe un logo guardado en el servidor, eliminarlo
  if (props.companyLogo && props.companyId) {
    const result = await companyStore.deleteCompanyLogo(props.companyId)
    if (!result.success) {
      alert('Error al eliminar logo: ' + result.error)
      return
    }
  }

  // Limpiar valores locales
  selectedLogoFile.value = null
  logoPreviewUrl.value = null
  if (logoFileInput.value) {
    logoFileInput.value.value = ''
  }
  emit('logo-cleared')
  emit('logo-deleted')
}

// ========== MÉTODOS DE BANNER ==========
const handleBannerFileSelect = (event) => {
  const file = event.target.files?.[0]

  if (!file) return

  if (!file.type.startsWith('image/')) {
    alert('Por favor selecciona un archivo de imagen válido')
    return
  }

  if (file.size > 10 * 1024 * 1024) {
    alert('El archivo es demasiado grande. Máximo 10MB')
    return
  }

  selectedBannerFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    bannerPreviewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)

  emit('banner-selected', file)
}

const clearBannerPreview = async () => {
  // Si existe un banner guardado en el servidor, eliminarlo
  if (props.companyBanner && props.companyId) {
    const result = await companyStore.deleteCompanyBanner(props.companyId)
    if (!result.success) {
      alert('Error al eliminar banner: ' + result.error)
      return
    }
  }

  // Limpiar valores locales
  selectedBannerFile.value = null
  bannerPreviewUrl.value = null
  if (bannerFileInput.value) {
    bannerFileInput.value.value = ''
  }
  emit('banner-cleared')
  emit('banner-deleted')
}

// Exponer métodos para padre
defineExpose({
  getSelectedLogoFile: () => selectedLogoFile.value,
  getSelectedBannerFile: () => selectedBannerFile.value,
  logoPreviewUrl,
  bannerPreviewUrl,
  clearLogoPreview,
  clearBannerPreview
})
</script>

<style scoped>
.company-media-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ========== CONTENEDOR HORIZONTAL ========== */
.media-row {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* ========== SECCIÓN DE MEDIA (Banner o Logo) ========== */
.media-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  flex: 0 1 auto;
}

/* ========== DISPLAY DE MEDIA ========== */
.media-display {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
}

/* Banner Display */
.banner-display {
  width: 180px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  background: #f5f5f5;
}

.banner-preview {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.banner-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
  border: 2px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

/* Logo Display */
.logo-display {
  width: 150px;
  height: 150px;
}

.logo-image {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  object-fit: cover;
  border: 3px solid #7c3aed;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
  animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  transition: transform 0.3s ease;
}

.logo-image:hover {
  transform: scale(1.05);
}

.logo-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
  border: 3px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
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

/* ========== ETIQUETA DE MEDIA ========== */
.media-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  text-align: center;
}

/* ========== CONTROLES DE MEDIA ========== */
.media-controls {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-btn svg {
  width: 16px;
  height: 16px;
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
  transform: translateY(-2px);
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ========== NOMBRE DE ARCHIVO ========== */
.file-name {
  font-size: 0.75rem;
  color: #666;
  text-align: center;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ========== TEXTO DE AYUDA ========== */
.help-text {
  color: #999;
  font-size: 0.8rem;
  margin: 0;
  text-align: center;
  line-height: 1.4;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .media-row {
    gap: 1.5rem;
  }

  .banner-display {
    width: 150px;
    height: 100px;
  }

  .logo-display {
    width: 130px;
    height: 130px;
  }

  .upload-btn {
    padding: 0.5rem 0.9rem;
    font-size: 0.85rem;
  }
}

@media (max-width: 600px) {
  .media-row {
    flex-direction: column;
    gap: 1rem;
  }

  .media-section {
    width: 100%;
  }

  .banner-display {
    width: 160px;
    height: 110px;
  }

  .logo-display {
    width: 140px;
    height: 140px;
  }

  .upload-btn {
    padding: 0.5rem 0.8rem;
    font-size: 0.85rem;
  }
}
</style>
