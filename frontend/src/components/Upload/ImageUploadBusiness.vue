<!-- frontend/src/components/Upload/ImageUploadBusiness.vue -->
<template>
  <div class="image-upload-business">
    
    <div class="upload-header">
      <h3 class="upload-title">
        <va-icon name="image" color="purple" />
        Imágenes del Negocio
      </h3>
      <p class="upload-subtitle">
        Sube tu logo y un banner creativo para destacar tu negocio
      </p>
    </div>

    <!-- Logo Upload -->
    <div class="upload-section">
      <div class="section-header">
        <div class="section-label">
          <va-icon name="business" size="small" />
          Logo de la Empresa *
        </div>
        <div class="section-specs">
          PNG, JPG • Máx 2MB • Cuadrado 500x500px
        </div>
      </div>

      <div class="upload-area logo-upload">
        <div v-if="!localLogo" class="upload-placeholder" @click="triggerLogoUpload">
          <va-icon name="add_photo_alternate" size="3rem" color="#CCC" />
          <p>Click para subir logo</p>
          <p class="upload-hint">O arrastra tu imagen aquí</p>
        </div>

        <div v-else class="upload-preview logo-preview">
          <img :src="localLogoPreview" alt="Logo preview" />
          <div class="preview-overlay">
            <VaButton
              preset="plain"
              icon="edit"
              color="white"
              @click="triggerLogoUpload"
            />
            <VaButton
              preset="plain"
              icon="delete"
              color="white"
              @click="removeLogo"
            />
          </div>
        </div>

        <input
          ref="logoInput"
          type="file"
          accept="image/png,image/jpeg,image/jpg"
          style="display: none"
          @change="handleLogoUpload"
        />
      </div>

      <div v-if="logoError" class="upload-error">
        <va-icon name="error" size="small" />
        <span>{{ logoError }}</span>
      </div>
    </div>

    <!-- Banner Upload -->
    <div class="upload-section">
      <div class="section-header">
        <div class="section-label">
          <va-icon name="panorama" size="small" />
          Banner Creativo *
        </div>
        <div class="section-specs">
          PNG, JPG • Máx 5MB • Horizontal 1200x400px
        </div>
      </div>

      <div class="upload-area banner-upload">
        <div v-if="!localBanner" class="upload-placeholder banner-placeholder" @click="triggerBannerUpload">
          <va-icon name="add_photo_alternate" size="3rem" color="#CCC" />
          <p>Click para subir banner</p>
          <p class="upload-hint">Tamaño recomendado: 1200x400px</p>
        </div>

        <div v-else class="upload-preview banner-preview">
          <img :src="localBannerPreview" alt="Banner preview" />
          <div class="preview-overlay">
            <VaButton
              preset="plain"
              icon="edit"
              color="white"
              @click="triggerBannerUpload"
            />
            <VaButton
              preset="plain"
              icon="delete"
              color="white"
              @click="removeBanner"
            />
          </div>
        </div>

        <input
          ref="bannerInput"
          type="file"
          accept="image/png,image/jpeg,image/jpg"
          style="display: none"
          @change="handleBannerUpload"
        />
      </div>

      <div v-if="bannerError" class="upload-error">
        <va-icon name="error" size="small" />
        <span>{{ bannerError }}</span>
      </div>
    </div>

    <!-- Tips -->
    <div class="upload-tips">
      <div class="tip-header">
        <va-icon name="lightbulb" size="small" />
        Consejos para mejores resultados
      </div>
      <ul>
        <li><strong>Logo:</strong> Usa fondo transparente (PNG) para mejor calidad</li>
        <li><strong>Banner:</strong> Incluye el nombre de tu empresa y un mensaje atractivo</li>
        <li><strong>Calidad:</strong> Usa imágenes de alta resolución para verse profesional</li>
        <li><strong>Colores:</strong> Mantén los colores de tu marca consistentes</li>
      </ul>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useToast } from 'vuestic-ui'

// ========== PROPS ==========
const props = defineProps({
  logo: {
    type: [File, String, null],
    default: null
  },
  banner: {
    type: [File, String, null],
    default: null
  }
})

const emit = defineEmits(['update:logo', 'update:banner'])

// ========== COMPOSABLES ==========
const { init: notify } = useToast()

// ========== REFS ==========
const logoInput = ref(null)
const bannerInput = ref(null)

// ========== STATE ==========
const localLogo = ref(props.logo)
const localLogoPreview = ref(props.logo)
const localBanner = ref(props.banner)
const localBannerPreview = ref(props.banner)
const logoError = ref('')
const bannerError = ref('')

// ========== WATCH ==========
watch(() => props.logo, (newVal) => {
  localLogo.value = newVal
  localLogoPreview.value = newVal
})

watch(() => props.banner, (newVal) => {
  localBanner.value = newVal
  localBannerPreview.value = newVal
})

// ========== METHODS ==========
const triggerLogoUpload = () => {
  logoInput.value?.click()
}

const triggerBannerUpload = () => {
  bannerInput.value?.click()
}

const handleLogoUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  logoError.value = ''

  // Validar tipo
  if (!file.type.match(/image\/(png|jpeg|jpg)/)) {
    logoError.value = 'Solo se permiten imágenes PNG o JPG'
    return
  }

  // Validar tamaño (2MB)
  if (file.size > 2 * 1024 * 1024) {
    logoError.value = 'El archivo no debe superar 2MB'
    return
  }

  // Crear preview
  const reader = new FileReader()
  reader.onload = (e) => {
    localLogoPreview.value = e.target.result
  }
  reader.readAsDataURL(file)

  localLogo.value = file
  emit('update:logo', file)

  notify({
    message: '✅ Logo cargado exitosamente',
    color: 'success',
    duration: 2000
  })
}

const handleBannerUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  bannerError.value = ''

  // Validar tipo
  if (!file.type.match(/image\/(png|jpeg|jpg)/)) {
    bannerError.value = 'Solo se permiten imágenes PNG o JPG'
    return
  }

  // Validar tamaño (5MB)
  if (file.size > 5 * 1024 * 1024) {
    bannerError.value = 'El archivo no debe superar 5MB'
    return
  }

  // Crear preview
  const reader = new FileReader()
  reader.onload = (e) => {
    localBannerPreview.value = e.target.result
  }
  reader.readAsDataURL(file)

  localBanner.value = file
  emit('update:banner', file)

  notify({
    message: '✅ Banner cargado exitosamente',
    color: 'success',
    duration: 2000
  })
}

const removeLogo = () => {
  localLogo.value = null
  localLogoPreview.value = null
  logoError.value = ''
  if (logoInput.value) logoInput.value.value = ''
  emit('update:logo', null)
  
  notify({
    message: 'Logo eliminado',
    color: 'info'
  })
}

const removeBanner = () => {
  localBanner.value = null
  localBannerPreview.value = null
  bannerError.value = ''
  if (bannerInput.value) bannerInput.value.value = ''
  emit('update:banner', null)
  
  notify({
    message: 'Banner eliminado',
    color: 'info'
  })
}
</script>

<style scoped>
/* ========== Container ========== */
.image-upload-business {
  padding: 2rem;
  background: white;
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

/* ========== Header ========== */
.upload-header {
  margin-bottom: 2rem;
}

.upload-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.upload-subtitle {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

/* ========== Upload Section ========== */
.upload-section {
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #333;
  font-size: 1rem;
}

.section-specs {
  font-size: 0.85rem;
  color: #666;
}

/* ========== Upload Area ========== */
.upload-area {
  border: 2px dashed #DDD;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
  cursor: pointer;
}

.upload-area:hover {
  border-color: var(--color-purple);
  background: rgba(92, 0, 153, 0.02);
}

.logo-upload {
  width: 200px;
  height: 200px;
}

.banner-upload {
  width: 100%;
  height: 200px;
}

/* ========== Upload Placeholder ========== */
.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 1rem;
}

.upload-placeholder p {
  margin: 0.5rem 0 0 0;
  color: #666;
  font-size: 0.95rem;
}

.upload-hint {
  font-size: 0.85rem !important;
  color: #999 !important;
}

.banner-placeholder {
  padding: 2rem;
}

/* ========== Upload Preview ========== */
.upload-preview {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.upload-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.logo-preview img {
  object-fit: contain;
  padding: 1rem;
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.upload-preview:hover .preview-overlay {
  opacity: 1;
}

/* ========== Upload Error ========== */
.upload-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: #FFEBEE;
  border-radius: 8px;
  color: #C62828;
  font-size: 0.85rem;
}

/* ========== Tips ========== */
.upload-tips {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #F8F4FF;
  border-radius: 12px;
}

.tip-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--color-purple);
  margin-bottom: 1rem;
}

.upload-tips ul {
  margin: 0;
  padding-left: 1.5rem;
}

.upload-tips li {
  margin-bottom: 0.5rem;
  color: #666;
  line-height: 1.6;
}

.upload-tips li:last-child {
  margin-bottom: 0;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .image-upload-business {
    padding: 1.5rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .logo-upload {
    width: 100%;
    max-width: 200px;
    margin: 0 auto;
  }
}
</style>