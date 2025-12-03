<!-- frontend/src/components/Profile/CompanyProfileEdit.vue -->
<template>
  <div class="company-edit-container">
    <div class="edit-header">
      <h2>Perfil De La Empresa</h2>
      <va-button
        preset="plain"
        color="textPrimary"
        @click="$emit('close')"
      >
        <va-icon name="close" size="large" />
      </va-button>
    </div>

    <!-- No Company Message -->
    <div v-if="!showForm" class="no-company-message">
      <va-icon name="business" size="3rem" color="purple" />
      <h3>No tienes perfil de empresa aún</h3>
      <p>Crea uno para publicar anuncios y gestionar tu negocio</p>
      <button class="purple-btn-gradient" @click="showForm = true">
        <va-icon name="add" />
        Crear Perfil De Empresa
      </button>
    </div>

    <!-- Loading State -->
    <div v-else-if="companyStore.isLoading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
    </div>

    <!-- Form -->
    <form v-else @submit.prevent="handleSaveCompany" class="company-form">
      <!-- Logo & Banner Upload Section (Card Design) -->
      <div class="upload-section">
        <h3 class="section-title">Perfil de la Empresa</h3>

        <!-- Media Card Container -->
        <div class="media-card">
          <!-- Banner Section -->
          <div class="banner-section">
            <!-- Banner Background -->
            <div
              class="banner-background"
              :style="{ backgroundImage: bannerPreviewUrl ? `url('${bannerPreviewUrl}')` : (currentBanner ? `url('${currentBanner}')` : 'none') }"
            >
              <!-- Banner Controls (Top Right) -->
              <div class="banner-controls">
                <input
                  ref="bannerFileInput"
                  type="file"
                  accept="image/*"
                  hidden
                  @change="handleBannerFileSelect"
                />
                <button
                  type="button"
                  class="control-btn banner-btn"
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
                  v-if="bannerPreviewUrl || currentBanner"
                  type="button"
                  class="control-btn delete-btn"
                  @click="clearBannerPreview"
                  title="Eliminar banner"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 4 21 4 23 6 23 20a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V6"></polyline>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                    <line x1="4" y1="6" x2="20" y2="6"></line>
                  </svg>
                </button>
              </div>
            </div>
            <!-- Banner File Info -->
            <div v-if="selectedBannerFile" class="banner-file-info">
              {{ selectedBannerFile.name }}
            </div>
          </div>

          <!-- Logo Overlay Section (Centered on Banner) -->
          <div class="logo-overlay">
            <div class="logo-container">
              <img
                v-if="logoPreviewUrl || currentLogo"
                :src="logoPreviewUrl || currentLogo"
                alt="Company Logo"
                class="logo-image"
              />
              <div v-else class="logo-placeholder">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
                  <polyline points="13 2 13 9 20 9"></polyline>
                </svg>
              </div>

              <!-- Logo Controls (Bottom of Logo) -->
              <div class="logo-controls">
                <input
                  ref="logoFileInput"
                  type="file"
                  accept="image/*"
                  hidden
                  @change="handleLogoFileSelect"
                />
                <button
                  type="button"
                  class="control-btn logo-btn"
                  @click="() => logoFileInput.click()"
                  title="Subir logo"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                  </svg>
                </button>
                <button
                  v-if="logoPreviewUrl || currentLogo"
                  type="button"
                  class="control-btn delete-btn"
                  @click="clearLogoPreview"
                  title="Eliminar logo"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 4 21 4 23 6 23 20a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V6"></polyline>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                    <line x1="4" y1="6" x2="20" y2="6"></line>
                  </svg>
                </button>
              </div>
            </div>
            <!-- Logo File Info -->
            <div v-if="selectedLogoFile" class="logo-file-info">
              {{ selectedLogoFile.name }}
            </div>
          </div>
        </div>

        <!-- Help Text -->
        <p class="help-text">
          Logo: JPG, PNG o GIF. Máximo 5MB. | Banner: Máximo 10MB. (851 x 315px)
        </p>
      </div>

      <!-- Nombre de Empresa -->
      <div class="form-group">
        <label class="form-label">Nombre de la Empresa *</label>
        <va-input
          v-model="formData.companyName"
          placeholder="Tech Solutions Bolivia"
          class="form-input"
          required
        />
      </div>

      <!-- Email Empresa (Auto-capturado, no editable) -->
      <div class="form-group">
        <label class="form-label">Email de la Empresa *</label>
        <va-input
          v-model="formData.email"
          type="email"
          placeholder="contact@company.com"
          class="form-input"
          disabled
          required
        />
        <p class="field-hint">Este email está vinculado a tu cuenta y no puede ser modificado</p>
      </div>

      <!-- Email de Contacto Público (EDITABLE) -->
      <div class="form-group">
        <label class="form-label">Email de Contacto Público</label>
        <va-input
          v-model="formData.contactEmail"
          type="email"
          placeholder="contacto@empresa.com"
          class="form-input"
        />
        <p class="field-hint">Este email será visible para los candidatos que deseen contactarte</p>
      </div>

      <!-- Teléfono -->
      <div class="form-group">
        <label class="form-label">Teléfono</label>
        <va-input
          v-model="formData.phone"
          placeholder="+591..."
          type="tel"
          class="form-input"
        />
      </div>

      <!-- Sitio Web -->
      <div class="form-group">
        <label class="form-label">Sitio Web</label>
        <va-input
          v-model="formData.website"
          placeholder="https://company.com"
          type="url"
          class="form-input"
        />
      </div>

      <!-- Dirección -->
      <div class="form-group">
        <label class="form-label">Dirección</label>
        <va-input
          v-model="formData.location"
          placeholder="Av. Mariscal Santa Cruz 1234"
          class="form-input"
        />
      </div>

      <!-- Ciudad -->
      <div class="form-group">
        <label class="form-label">Ciudad</label>
        <va-select
          v-model="formData.city"
          :options="cities"
          class="form-input"
        />
      </div>

      <!-- Descripción -->
      <div class="form-group">
        <label class="form-label">Descripción</label>
        <va-textarea
          v-model="formData.description"
          placeholder="Cuéntanos sobre tu empresa..."
          rows="4"
          class="form-textarea"
        />
      </div>

      <!-- Categoría -->
      <div class="form-group">
        <label class="form-label">Categoría</label>
        <va-select
          :model-value="formData.category"
          @update:model-value="formData.category = $event.value || $event"
          :options="categories"
          track-by="value"
          text-by="text"
          class="form-input"
        />
      </div>

      <!-- Submit Button -->
      <div class="form-actions">
        <button type="submit" class="purple-btn-gradient" :disabled="companyStore.isLoading">
          <va-icon name="save" />
          {{ companyStore.isLoading ? 'Guardando...' : 'Guardar Cambios' }}
        </button>

        <va-button
          type="button"
          preset="plain"
          color="textSecondary"
          size="large"
          @click="$emit('close')"
          :disabled="companyStore.isLoading"
        >
          <va-icon name="close" />
          Cancelar
        </va-button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useToast } from 'vuestic-ui'
import { useCompanyStore } from '@/stores/useCompanyStore'

// ========== COMPOSABLES ==========
const { init: notify } = useToast()
const companyStore = useCompanyStore()

// ========== PROPS ==========
const props = defineProps({
  userProfileId: {
    type: [String, null],
    default: null
  },
  companyProfileId: {
    type: String,
    default: null
  }
})

// ========== EMITS ==========
const emit = defineEmits(['close', 'created', 'updated'])

// ========== DATA ==========
const showForm = ref(false)

// Media upload refs and state
const logoFileInput = ref(null)
const bannerFileInput = ref(null)
const selectedLogoFile = ref(null)
const selectedBannerFile = ref(null)
const logoPreviewUrl = ref(null)
const bannerPreviewUrl = ref(null)

const formData = ref({
  companyName: '',
  email: '',
  contactEmail: '',
  phone: '',
  website: '',
  location: '',
  city: '',
  description: '',
  category: 'other'
})

const cities = [
  'La Paz',
  'Cochabamba',
  'Santa Cruz',
  'Oruro',
  'Potosí',
  'Tarija',
  'Chuquisaca',
  'Beni',
  'Pando'
]

const categories = [
  { text: 'Empleador - Trabajos', value: 'jobs' },
  { text: 'Restaurante - Gastronomía', value: 'restaurant' },
  { text: 'Negocio', value: 'business' },
  { text: 'Profesional', value: 'professional' },
  { text: 'Otro', value: 'other' }
]

// ========== COMPUTED ==========
const currentLogo = computed(() => {
  return companyStore.currentCompany?.logo || null
})

const currentBanner = computed(() => {
  return companyStore.currentCompany?.banner || null
})

// ========== LIFECYCLE ==========
onMounted(() => {
  if (props.companyProfileId) {
    loadCompanyProfile()
    showForm.value = true
  }
})

watch(() => props.companyProfileId, (newId) => {
  if (newId) {
    loadCompanyProfile()
    showForm.value = true
  }
})

// ========== METHODS ==========
const loadCompanyProfile = async () => {
  try {
    const result = await companyStore.getCompanyById(props.companyProfileId)

    if (result.success && result.company) {
      formData.value = {
        companyName: result.company.companyName,
        email: result.company.email,
        contactEmail: result.company.contactEmail || '',
        phone: result.company.phone || '',
        website: result.company.website || '',
        location: result.company.location || '',
        city: result.company.city || '',
        description: result.company.description || '',
        category: result.company.category || 'other'
      }
    }
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  }
}

const handleSaveCompany = async () => {
  try {
    // Validación
    if (!formData.value.companyName.trim()) {
      notify({
        message: 'El nombre de la empresa es requerido',
        color: 'warning',
        duration: 3000
      })
      return
    }

    if (!formData.value.email.trim()) {
      notify({
        message: 'El email es requerido',
        color: 'warning',
        duration: 3000
      })
      return
    }

    // Preparar datos para enviar
    // Extraer el valor del category (puede ser string o objeto)
    let categoryValue = formData.value.category
    if (typeof categoryValue === 'object' && categoryValue !== null && categoryValue.value) {
      categoryValue = categoryValue.value
    }

    const dataToSend = {
      companyName: formData.value.companyName,
      email: formData.value.email,
      contactEmail: formData.value.contactEmail || '',
      phone: formData.value.phone || '',
      website: formData.value.website || '',
      location: formData.value.location || '',
      city: formData.value.city || '',
      description: formData.value.description || '',
      category: categoryValue || 'other'
    }

    // Obtener archivos seleccionados para logo y banner
    const files = {}
    if (selectedLogoFile.value) files.logo = selectedLogoFile.value
    if (selectedBannerFile.value) files.banner = selectedBannerFile.value

    // Crear o actualizar
    if (props.companyProfileId) {
      // ACTUALIZAR
      let result
      if (Object.keys(files).length > 0) {
        // Si hay archivos, usar updateCompanyWithFiles
        result = await companyStore.updateCompanyWithFiles(props.companyProfileId, dataToSend, files)
      } else {
        // Si no hay archivos, usar updateCompany
        result = await companyStore.updateCompany(props.companyProfileId, dataToSend)
      }

      if (result.success) {
        notify({
          message: 'Perfil de empresa actualizado',
          color: 'success',
          duration: 5000
        })
        // Limpiar archivos y previews después de guardar exitosamente
        selectedLogoFile.value = null
        selectedBannerFile.value = null
        logoPreviewUrl.value = null
        bannerPreviewUrl.value = null
        if (logoFileInput.value) logoFileInput.value.value = ''
        if (bannerFileInput.value) bannerFileInput.value.value = ''

        // Recargar datos en background (sin await) para que no bloquee el cierre
        loadCompanyProfile()
        emit('updated', result.company)
        setTimeout(() => emit('close'), 1000)
      } else {
        throw new Error(result.error)
      }
    } else {
      // CREAR
      const result = await companyStore.createCompany(
        dataToSend,
        props.userProfileId,
        files
      )

      if (result.success) {
        notify({
          message: 'Perfil de empresa creado',
          color: 'success',
          duration: 5000
        })
        // Limpiar archivos y previews después de crear exitosamente
        selectedLogoFile.value = null
        selectedBannerFile.value = null
        logoPreviewUrl.value = null
        bannerPreviewUrl.value = null
        if (logoFileInput.value) logoFileInput.value.value = ''
        if (bannerFileInput.value) bannerFileInput.value.value = ''

        emit('created', result.company)
        setTimeout(() => emit('close'), 1000)
      } else {
        throw new Error(result.error)
      }
    }
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  }
}

// ========== MEDIA UPLOAD METHODS ==========
const MAX_LOGO_SIZE = 5 * 1024 * 1024 // 5MB
const MAX_BANNER_SIZE = 10 * 1024 * 1024 // 10MB

const handleLogoFileSelect = (event) => {
  const file = event.target.files?.[0]

  if (!file) return

  if (!file.type.startsWith('image/')) {
    notify({
      message: 'Por favor selecciona un archivo de imagen válido',
      color: 'warning',
      duration: 3000
    })
    return
  }

  if (file.size > MAX_LOGO_SIZE) {
    notify({
      message: 'El archivo es demasiado grande. Máximo 5MB',
      color: 'warning',
      duration: 3000
    })
    return
  }

  selectedLogoFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    logoPreviewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const handleBannerFileSelect = (event) => {
  const file = event.target.files?.[0]

  if (!file) return

  if (!file.type.startsWith('image/')) {
    notify({
      message: 'Por favor selecciona un archivo de imagen válido',
      color: 'warning',
      duration: 3000
    })
    return
  }

  if (file.size > MAX_BANNER_SIZE) {
    notify({
      message: 'El archivo es demasiado grande. Máximo 10MB',
      color: 'warning',
      duration: 3000
    })
    return
  }

  selectedBannerFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    bannerPreviewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const clearLogoPreview = async () => {
  // Si existe un logo guardado en el servidor, eliminarlo
  if (currentLogo.value && props.companyProfileId) {
    const result = await companyStore.deleteCompanyLogo(props.companyProfileId)
    if (!result.success) {
      notify({
        message: `Error al eliminar logo: ${result.error}`,
        color: 'danger',
        duration: 5000
      })
      return
    }
  }

  // Limpiar valores locales
  selectedLogoFile.value = null
  logoPreviewUrl.value = null
  if (logoFileInput.value) {
    logoFileInput.value.value = ''
  }
}

const clearBannerPreview = async () => {
  // Si existe un banner guardado en el servidor, eliminarlo
  if (currentBanner.value && props.companyProfileId) {
    const result = await companyStore.deleteCompanyBanner(props.companyProfileId)
    if (!result.success) {
      notify({
        message: `Error al eliminar banner: ${result.error}`,
        color: 'danger',
        duration: 5000
      })
      return
    }
  }

  // Limpiar valores locales
  selectedBannerFile.value = null
  bannerPreviewUrl.value = null
  if (bannerFileInput.value) {
    bannerFileInput.value.value = ''
  }
}
</script>

<style scoped>
.company-edit-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  max-width: 900px;
  margin: 0 auto;
}

.edit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.edit-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.no-company-message {
  text-align: center;
  padding: 2rem;
}

.no-company-message h3 {
  color: #333;
  font-size: 1.3rem;
  margin: 1rem 0;
}

.no-company-message p {
  color: #666;
  margin-bottom: 1.5rem;
}

.loading-state {
  text-align: center;
  padding: 2rem;
}

.company-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.upload-section {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.field-hint {
  font-size: 0.8rem;
  color: #6B7280;
  font-style: italic;
  margin-top: 0.25rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f0f0f0;
  justify-content: flex-start;
}

.purple-btn-gradient {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.purple-btn-gradient:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
}

.purple-btn-gradient:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* ========== MEDIA CARD STYLES ========== */
.media-card {
  background: white;
  border-radius: 12px;
  overflow: visible;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 6rem;
  position: relative;
}

.banner-section {
  position: relative;
}

.banner-background {
  position: relative;
  width: 100%;
  aspect-ratio: 851 / 315;
  background-size: cover;
  background-position: center;
  background-color: #f5f5f5;
  border-radius: 12px 12px 0 0;
}

.banner-controls {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  display: flex;
  gap: 0.5rem;
  z-index: 10;
}

.banner-file-info {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
  color: #666;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.logo-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 5;
}

.logo-container {
  position: relative;
  width: 140px;
  height: 140px;
  background: white;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  overflow: visible;
  border: 4px solid #7c3aed;
}

.logo-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  transition: transform 0.3s ease;
}

.logo-image:hover {
  transform: scale(1.05);
}

.logo-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.logo-controls {
  position: absolute;
  bottom: -2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
  z-index: 10;
}

.logo-file-info {
  position: absolute;
  bottom: -3rem;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.7rem;
  color: #666;
  text-align: center;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  z-index: 5;
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

.control-group {
  display: contents;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1rem;
  background: white;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.control-btn:hover:not(:disabled) {
  background: #f5f5f5;
  border-color: #bbb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.control-btn.logo-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
}

.control-btn.logo-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.control-btn.banner-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
}

.control-btn.banner-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.control-btn.delete-btn {
  background: #dc2626;
  color: white;
  border: none;
}

.control-btn.delete-btn:hover:not(:disabled) {
  background: #991b1b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.control-btn svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.control-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.media-info {
  padding: 1rem;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.file-info {
  display: flex;
  gap: 0.5rem;
  font-size: 0.85rem;
  align-items: center;
}

.info-label {
  font-weight: 600;
  color: #666;
}

.file-name {
  color: #999;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.help-text {
  color: #999;
  font-size: 0.8rem;
  margin: 0.5rem 0 0 0;
  text-align: center;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .company-edit-container {
    padding: 1.5rem;
  }

  .edit-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .edit-header h2 {
    font-size: 1.25rem;
  }

  .banner-background {
    aspect-ratio: 600 / 250;
  }

  .logo-container {
    width: 120px;
    height: 120px;
  }

  .logo-controls {
    bottom: -2.5rem;
  }

  .logo-file-info {
    bottom: -3.5rem;
  }

  .control-btn {
    padding: 0.5rem 0.8rem;
    font-size: 0.8rem;
  }

  .control-btn svg {
    width: 14px;
    height: 14px;
  }
}

@media (max-width: 600px) {
  .media-card {
    margin-bottom: 7rem;
  }

  .banner-background {
    aspect-ratio: 1 / 0.8;
  }

  .logo-container {
    width: 100px;
    height: 100px;
  }

  .logo-controls {
    bottom: -2.5rem;
    gap: 0.25rem;
  }

  .logo-file-info {
    bottom: -3.5rem;
  }

  .control-btn {
    padding: 0.4rem 0.6rem;
    font-size: 0.75rem;
  }

  .control-btn svg {
    width: 12px;
    height: 12px;
  }
}
</style>
