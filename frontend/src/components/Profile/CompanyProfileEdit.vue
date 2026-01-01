<!-- frontend/src/components/Profile/CompanyProfileEdit.vue -->
<template>
  <div class="company-edit-container">
    <div class="edit-header">
      <div class="header-title-section">
        <h2>Perfil De La Empresa</h2>
        <div v-if="companyStore.currentCompany?.verified" class="verified-badge" title="Empresa Verificada">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="10" fill="#7C3AED"/>
            <path d="M9 12l2 2 4-4" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Empresa Verificada</span>
        </div>
      </div>
      <button class="close-btn" @click="$emit('close')" type="button">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
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
      <!-- Tabs Navigation -->
      <div class="tabs-navigation">
        <button
          type="button"
          class="tab-btn"
          :class="{ active: activeTab === 'general' }"
          @click="activeTab = 'general'"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          Información General
        </button>
        <button
          type="button"
          class="tab-btn"
          :class="{ active: activeTab === 'verification' }"
          @click="activeTab = 'verification'"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          Verificación
        </button>
      </div>

      <!-- Tab Content: General -->
      <div v-show="activeTab === 'general'" class="tab-content">
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
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 6h18"></path>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                    <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
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
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 6h18"></path>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                    <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
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
          placeholder="Ej: Constructora Andina S.R.L., Restaurante El Buen Sabor, Farmacia San Pedro"
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
          placeholder="correo@miempresa.com"
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
          placeholder="Ej: rrhh@miempresa.com, info@miempresa.com, contacto@miempresa.com"
          class="form-input"
        />
        <p class="field-hint">Este email será visible para los candidatos que deseen contactarte</p>
      </div>

      <!-- Teléfono -->
      <div class="form-group">
        <label class="form-label">Teléfono</label>
        <va-input
          v-model="formData.phone"
          placeholder="Ej: +591 2 2345678, +591 70123456, 4-4567890"
          type="tel"
          class="form-input"
        />
      </div>

      <!-- Sitio Web -->
      <div class="form-group">
        <label class="form-label">Sitio Web</label>
        <va-input
          v-model="formData.website"
          placeholder="Ej: https://www.miempresa.com, https://miempresa.com.bo"
          type="url"
          class="form-input"
        />
      </div>

      <!-- Dirección -->
      <div class="form-group">
        <label class="form-label">Dirección</label>
        <va-input
          v-model="formData.location"
          placeholder="Ej: Av. Ballivián #1234, Calle Sucre esq. Bolivar, Zona Sur, Achumani"
          class="form-input"
        />
      </div>

      <!-- Ciudad -->
      <div class="form-group">
        <label class="form-label">Ciudad</label>
        <va-select
          v-model="formData.city"
          :options="cities"
          placeholder="Selecciona tu ciudad"
          class="form-input"
        />
      </div>

      <!-- Descripción -->
      <div class="form-group">
        <label class="form-label">Descripción</label>
        <va-textarea
          v-model="formData.description"
          placeholder="Describe tu empresa: qué servicios o productos ofreces, cuál es tu misión, años de experiencia, áreas de especialización, etc. Ej: 'Somos una empresa constructora con 15 años de experiencia en proyectos residenciales y comerciales...'"
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
      </div>
      <!-- Fin Tab Content: General -->

      <!-- Tab Content: Verification -->
      <div v-show="activeTab === 'verification'" class="tab-content">
      <!-- Sección de Verificación -->
      <div class="verification-section">
        <h3 class="section-title">Verificación de Empresa</h3>

        <!-- Grid de 2 columnas para campos de verificación -->
        <div class="verification-grid">
          <div class="form-group">
            <label class="form-label">NIT *</label>
            <va-input
              v-model="formData.nit"
              placeholder="Ej: 1234567890, 123456789-0, 1234567-01-5"
              class="form-input"
            />
            <p class="field-hint">Número de Identificación Tributaria registrado en Impuestos Nacionales</p>
          </div>

          <div class="form-group">
            <label class="form-label">Razón Social *</label>
            <va-input
              v-model="formData.legalName"
              placeholder="Ej: CONSTRUCTORA ANDINA S.R.L., SEMAPA - SERVICIO MUNICIPAL DE AGUA POTABLE"
              class="form-input"
            />
            <p class="field-hint">Nombre legal completo tal como aparece en tu registro tributario</p>
          </div>

          <div class="form-group full-width">
            <label class="form-label">Código SEPREC (Opcional)</label>
            <va-input
              v-model="formData.seprecCode"
              placeholder="Ej: 00-005678-9-0, 01-123456-7-8 (Matrícula de Comercio FUNDEMPRESA)"
              class="form-input"
            />
            <p class="field-hint">Matrícula de Comercio de FUNDEMPRESA - Ayuda a acelerar el proceso de verificación</p>
          </div>
        </div>

        <!-- Info Box de Verificación -->
        <div class="info-box">
          <div class="info-content">
            <p><strong>¿Cómo verificar tu empresa?</strong></p>
            <p>Completa los datos de NIT y Razón Social. Opcionalmente, agrega tu Código SEPREC para una verificación más rápida.</p>
            <p class="contact-info">¿Necesitas ayuda? Contacta: <a href="mailto:info@guiaspurpuras.com.bo">info@guiaspurpuras.com.bo</a></p>
          </div>
        </div>

        <!-- Estado de verificación y acciones -->
        <div class="verification-status-section">
          <!-- Si ya está verificada -->
          <div v-if="companyStore.currentCompany?.verified" class="verification-status-message verified">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" fill="#7C3AED"/>
              <path d="M9 12l2 2 4-4" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>¡Tu empresa ya está verificada!</span>
          </div>

          <!-- Si ya solicitó verificación pero aún no está verificada -->
          <div v-else-if="companyStore.currentCompany?.verificationRequestedAt" class="verification-status-message pending">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <div class="status-content">
              <span class="status-title">Verificación en proceso</span>
              <span class="status-subtitle">Tu solicitud está siendo revisada. Puedes actualizar tus datos legales arriba si necesitas agregar información.</span>
            </div>
          </div>

          <!-- Si aún no ha solicitado verificación -->
          <div v-else class="verification-checkbox">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.requestVerification" class="custom-checkbox" />
              <span class="checkbox-text">Solicitar verificación de mi empresa</span>
            </label>
            <p class="checkbox-hint">Completa los datos de NIT y Razón Social arriba, luego marca esta casilla y haz clic en "Guardar Cambios" para enviar tu solicitud.</p>
          </div>
        </div>
      </div>
      </div>
      <!-- Fin Tab Content: Verification -->

      <!-- Submit Button -->
      <div class="form-actions">
        <button type="submit" class="purple-btn-gradient" :disabled="companyStore.isLoading">
          <va-icon name="save" />
          {{ companyStore.isLoading ? 'Guardando...' : 'Guardar Cambios' }}
        </button>

        <button
          type="button"
          class="red-btn-gradient"
          @click="$emit('close')"
          :disabled="companyStore.isLoading"
        >
          <va-icon name="close" />
          Cancelar
        </button>
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
const activeTab = ref('general') // 'general' o 'verification'

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
  category: 'other',
  nit: '',
  legalName: '',
  seprecCode: '',
  requestVerification: false
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
        category: result.company.category || 'other',
        nit: result.company.nit || '',
        legalName: result.company.legalName || '',
        seprecCode: result.company.seprecCode || '',
        requestVerification: false
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
      category: categoryValue || 'other',
      nit: formData.value.nit || '',
      legalName: formData.value.legalName || '',
      seprecCode: formData.value.seprecCode || ''
    }

    // Si se marca el checkbox de verificación y no está ya verificada, establecer fecha de solicitud
    if (formData.value.requestVerification && !companyStore.currentCompany?.verified) {
      dataToSend.verificationRequestedAt = new Date().toISOString()
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

.header-title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.edit-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.verified-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0;
  background: transparent;
  color: #7C3AED;
  border-radius: 0;
  font-size: 0.875rem;
  font-weight: 600;
  box-shadow: none;
}

.verified-badge svg {
  flex-shrink: 0;
  filter: drop-shadow(0 1px 2px rgba(124, 58, 237, 0.3));
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  background: #F3F4F6;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6B7280;
}

.close-btn:hover {
  background: #FEE2E2;
  color: #DC2626;
  transform: rotate(90deg);
}

.close-btn:active {
  transform: rotate(90deg) scale(0.95);
}

.close-btn svg {
  width: 20px;
  height: 20px;
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
  gap: 1.5rem;
}

/* ========== TABS STYLES ========== */
.tabs-navigation {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #F3F4F6;
  padding-bottom: 0;
}

.tab-btn {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  color: #6B7280;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.tab-btn svg {
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: #7C3AED;
  background: linear-gradient(180deg, transparent 0%, rgba(124, 58, 237, 0.05) 100%);
}

.tab-btn.active {
  color: #7C3AED;
  border-bottom-color: #7C3AED;
  background: linear-gradient(180deg, rgba(124, 58, 237, 0.05) 0%, transparent 100%);
}

.tab-btn.active svg {
  color: #7C3AED;
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.6rem;
  background: linear-gradient(135deg, #7C3AED, #9333EA);
  color: white;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 700;
  margin-left: 0.25rem;
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  margin-bottom: 1.25rem;
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

.red-btn-gradient {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.red-btn-gradient:hover:not(:disabled) {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  transform: translateY(-2px);
}

.red-btn-gradient:disabled {
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
  width: 168px;
  height: 168px;
  background: white;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: visible;
  border: 4px solid white;
}

.logo-image {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  object-fit: contain;
  animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  transition: transform 0.3s ease;
}

.logo-image:hover {
  transform: scale(1.05);
}

.logo-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 4px;
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

/* ========== VERIFICATION SECTION STYLES ========== */
.verification-section {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.verification-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.verification-grid .full-width {
  grid-column: 1 / -1;
}

.verification-grid .form-input {
  background: white !important;
}

.verification-grid .va-input-wrapper {
  background: white !important;
}

.verification-grid .va-input-wrapper__field {
  background: white !important;
}

.info-box {
  padding: 1rem 1.25rem;
  background: #fffbeb;
  border: 1px solid #fbbf24;
  border-left: 4px solid #fbbf24;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.info-content p {
  margin: 0 0 0.5rem 0;
  color: #78350f;
  font-size: 0.9rem;
  line-height: 1.5;
}

.info-content p:last-child {
  margin-bottom: 0;
}

.info-content strong {
  color: #78350f;
  font-weight: 600;
}

.contact-info {
  color: #92400e !important;
  font-size: 0.85rem !important;
}

.contact-info a {
  color: #7C3AED;
  text-decoration: none;
  font-weight: 600;
}

.contact-info a:hover {
  text-decoration: underline;
}

.verification-status-section {
  padding: 0;
  background: transparent;
  border: none;
}

.verification-checkbox {
  padding: 0;
  background: transparent;
  border: none;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  margin-bottom: 0.5rem;
}

.custom-checkbox {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #7C3AED;
}

.checkbox-text {
  font-weight: 600;
  color: #1F2937;
  font-size: 0.95rem;
}

.checkbox-hint {
  margin: 0 0 0 calc(20px + 0.75rem);
  color: #6B7280;
  font-size: 0.8rem;
  line-height: 1.4;
}

.verification-status-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
}

.verification-status-message.verified {
  background: transparent;
  color: #7C3AED;
  padding: 0;
}

.verification-status-message.verified svg {
  flex-shrink: 0;
  filter: drop-shadow(0 1px 2px rgba(124, 58, 237, 0.3));
}

.verification-status-message.pending {
  background: #fffbeb;
  border: 1px solid #fbbf24;
  color: #92400e;
}

.verification-status-message.pending svg {
  flex-shrink: 0;
  color: #f59e0b;
}

.status-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.status-title {
  font-weight: 600;
  font-size: 0.95rem;
}

.status-subtitle {
  font-weight: 400;
  font-size: 0.85rem;
  line-height: 1.4;
  opacity: 0.9;
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

  .tabs-navigation {
    gap: 0.25rem;
    overflow-x: auto;
  }

  .tab-btn {
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
  }

  .verification-grid {
    grid-template-columns: 1fr;
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
