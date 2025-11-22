<!-- frontend/src/components/Common/SocialMediaFields.vue -->
<template>
  <div class="social-media-fields">
    
    <!-- Header -->
    <div class="section-header">
      <h3 class="section-title">
        <va-icon name="share" size="1.25rem" color="purple" />
        Redes Sociales
      </h3>
      <p class="section-subtitle">
        Agrega tus redes sociales para que tus clientes puedan seguirte y contactarte
      </p>
    </div>

    <!-- Social Media Inputs -->
    <div class="social-fields-grid">
      
      <!-- Facebook -->
      <div class="social-field">
        <div class="field-label">
          <div class="social-icon facebook">
            <va-icon name="facebook" />
          </div>
          <span>Facebook</span>
          <va-badge v-if="localSocialMedia.facebook" color="success" text="✓" />
        </div>
        <VaInput
          v-model="localSocialMedia.facebook"
          placeholder="https://facebook.com/tu-negocio"
          :rules="[validateUrl]"
          @blur="normalizeUrl('facebook')"
        >
          <template #prepend>
            <span class="input-prefix">facebook.com/</span>
          </template>
          <template #append v-if="localSocialMedia.facebook">
            <VaButton
              preset="plain"
              size="small"
              icon="open_in_new"
              @click="openUrl(localSocialMedia.facebook)"
              title="Abrir perfil"
            />
          </template>
        </VaInput>
      </div>

      <!-- Instagram -->
      <div class="social-field">
        <div class="field-label">
          <div class="social-icon instagram">
            <va-icon name="camera_alt" />
          </div>
          <span>Instagram</span>
          <va-badge v-if="localSocialMedia.instagram" color="success" text="✓" />
        </div>
        <VaInput
          v-model="localSocialMedia.instagram"
          placeholder="https://instagram.com/tu-negocio"
          :rules="[validateUrl]"
          @blur="normalizeUrl('instagram')"
        >
          <template #prepend>
            <span class="input-prefix">instagram.com/</span>
          </template>
          <template #append v-if="localSocialMedia.instagram">
            <VaButton
              preset="plain"
              size="small"
              icon="open_in_new"
              @click="openUrl(localSocialMedia.instagram)"
              title="Abrir perfil"
            />
          </template>
        </VaInput>
      </div>

      <!-- TikTok -->
      <div class="social-field">
        <div class="field-label">
          <div class="social-icon tiktok">
            <va-icon name="music_note" />
          </div>
          <span>TikTok</span>
          <va-badge v-if="localSocialMedia.tiktok" color="success" text="✓" />
        </div>
        <VaInput
          v-model="localSocialMedia.tiktok"
          placeholder="https://tiktok.com/@tu-negocio"
          :rules="[validateUrl]"
          @blur="normalizeUrl('tiktok')"
        >
          <template #prepend>
            <span class="input-prefix">tiktok.com/</span>
          </template>
          <template #append v-if="localSocialMedia.tiktok">
            <VaButton
              preset="plain"
              size="small"
              icon="open_in_new"
              @click="openUrl(localSocialMedia.tiktok)"
              title="Abrir perfil"
            />
          </template>
        </VaInput>
      </div>

      <!-- LinkedIn -->
      <div class="social-field">
        <div class="field-label">
          <div class="social-icon linkedin">
            <va-icon name="work" />
          </div>
          <span>LinkedIn</span>
          <va-badge v-if="localSocialMedia.linkedin" color="success" text="✓" />
        </div>
        <VaInput
          v-model="localSocialMedia.linkedin"
          placeholder="https://linkedin.com/company/tu-negocio"
          :rules="[validateUrl]"
          @blur="normalizeUrl('linkedin')"
        >
          <template #prepend>
            <span class="input-prefix">linkedin.com/</span>
          </template>
          <template #append v-if="localSocialMedia.linkedin">
            <VaButton
              preset="plain"
              size="small"
              icon="open_in_new"
              @click="openUrl(localSocialMedia.linkedin)"
              title="Abrir perfil"
            />
          </template>
        </VaInput>
      </div>

      <!-- Twitter/X -->
      <div class="social-field">
        <div class="field-label">
          <div class="social-icon twitter">
            <va-icon name="tag" />
          </div>
          <span>Twitter / X</span>
          <va-badge v-if="localSocialMedia.twitter" color="success" text="✓" />
        </div>
        <VaInput
          v-model="localSocialMedia.twitter"
          placeholder="https://twitter.com/tu-negocio"
          :rules="[validateUrl]"
          @blur="normalizeUrl('twitter')"
        >
          <template #prepend>
            <span class="input-prefix">x.com/</span>
          </template>
          <template #append v-if="localSocialMedia.twitter">
            <VaButton
              preset="plain"
              size="small"
              icon="open_in_new"
              @click="openUrl(localSocialMedia.twitter)"
              title="Abrir perfil"
            />
          </template>
        </VaInput>
      </div>

      <!-- YouTube -->
      <div class="social-field">
        <div class="field-label">
          <div class="social-icon youtube">
            <va-icon name="play_circle" />
          </div>
          <span>YouTube</span>
          <va-badge v-if="localSocialMedia.youtube" color="success" text="✓" />
        </div>
        <VaInput
          v-model="localSocialMedia.youtube"
          placeholder="https://youtube.com/@tu-negocio"
          :rules="[validateUrl]"
          @blur="normalizeUrl('youtube')"
        >
          <template #prepend>
            <span class="input-prefix">youtube.com/</span>
          </template>
          <template #append v-if="localSocialMedia.youtube">
            <VaButton
              preset="plain"
              size="small"
              icon="open_in_new"
              @click="openUrl(localSocialMedia.youtube)"
              title="Abrir canal"
            />
          </template>
        </VaInput>
      </div>

    </div>

    <!-- Tips -->
    <div class="social-tips">
      <va-icon name="tips_and_updates" size="small" color="info" />
      <div class="tips-content">
        <strong>Consejos:</strong>
        <ul>
          <li>Puedes ingresar solo el nombre de usuario o la URL completa</li>
          <li>Ejemplo: "tunegocio" o "https://facebook.com/tunegocio"</li>
          <li>Asegúrate de que tus perfiles sean públicos</li>
        </ul>
      </div>
    </div>

    <!-- Preview Section -->
    <div v-if="hasAnySocial" class="social-preview">
      <h4 class="preview-title">
        <va-icon name="visibility" size="small" />
        Vista previa de tus redes sociales
      </h4>
      <div class="preview-buttons">
        <a
          v-if="localSocialMedia.facebook"
          :href="getFullUrl('facebook')"
          target="_blank"
          class="social-preview-btn facebook"
        >
          <va-icon name="facebook" />
          <span>Facebook</span>
        </a>
        <a
          v-if="localSocialMedia.instagram"
          :href="getFullUrl('instagram')"
          target="_blank"
          class="social-preview-btn instagram"
        >
          <va-icon name="camera_alt" />
          <span>Instagram</span>
        </a>
        <a
          v-if="localSocialMedia.tiktok"
          :href="getFullUrl('tiktok')"
          target="_blank"
          class="social-preview-btn tiktok"
        >
          <va-icon name="music_note" />
          <span>TikTok</span>
        </a>
        <a
          v-if="localSocialMedia.linkedin"
          :href="getFullUrl('linkedin')"
          target="_blank"
          class="social-preview-btn linkedin"
        >
          <va-icon name="work" />
          <span>LinkedIn</span>
        </a>
        <a
          v-if="localSocialMedia.twitter"
          :href="getFullUrl('twitter')"
          target="_blank"
          class="social-preview-btn twitter"
        >
          <va-icon name="tag" />
          <span>Twitter/X</span>
        </a>
        <a
          v-if="localSocialMedia.youtube"
          :href="getFullUrl('youtube')"
          target="_blank"
          class="social-preview-btn youtube"
        >
          <va-icon name="play_circle" />
          <span>YouTube</span>
        </a>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// ========== PROPS & EMITS ==========
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      facebook: '',
      instagram: '',
      tiktok: '',
      linkedin: '',
      twitter: '',
      youtube: ''
    })
  }
})

const emit = defineEmits(['update:modelValue'])

// ========== STATE ==========
const localSocialMedia = ref({ ...props.modelValue })

// ========== COMPUTED ==========
const hasAnySocial = computed(() => {
  return Object.values(localSocialMedia.value).some(value => value && value.trim())
})

// ========== METHODS ==========
const validateUrl = (value) => {
  if (!value || !value.trim()) return true // Opcional
  
  // Permitir usernames o URLs completas
  const urlPattern = /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/
  const usernamePattern = /^[a-zA-Z0-9._-]+$/
  
  if (urlPattern.test(value) || usernamePattern.test(value)) {
    return true
  }
  
  return 'Ingresa un nombre de usuario válido o URL completa'
}

const normalizeUrl = (platform) => {
  const value = localSocialMedia.value[platform]
  if (!value || !value.trim()) return
  
  // Si ya es una URL completa, no hacer nada
  if (value.startsWith('http://') || value.startsWith('https://')) {
    return
  }
  
  // Si contiene el dominio, agregar https
  if (value.includes('.com') || value.includes('.co')) {
    localSocialMedia.value[platform] = `https://${value}`
    return
  }
  
  // Si es solo username, construir URL
  const username = value.replace(/^@/, '').trim()
  const baseUrls = {
    facebook: 'https://facebook.com/',
    instagram: 'https://instagram.com/',
    tiktok: 'https://tiktok.com/@',
    linkedin: 'https://linkedin.com/company/',
    twitter: 'https://x.com/',
    youtube: 'https://youtube.com/@'
  }
  
  localSocialMedia.value[platform] = baseUrls[platform] + username
}

const getFullUrl = (platform) => {
  const value = localSocialMedia.value[platform]
  if (!value) return ''
  
  if (value.startsWith('http://') || value.startsWith('https://')) {
    return value
  }
  
  const username = value.replace(/^@/, '').trim()
  const baseUrls = {
    facebook: 'https://facebook.com/',
    instagram: 'https://instagram.com/',
    tiktok: 'https://tiktok.com/@',
    linkedin: 'https://linkedin.com/company/',
    twitter: 'https://x.com/',
    youtube: 'https://youtube.com/@'
  }
  
  return baseUrls[platform] + username
}

const openUrl = (url) => {
  if (!url) return
  const fullUrl = url.startsWith('http') ? url : `https://${url}`
  window.open(fullUrl, '_blank')
}

// ========== WATCHERS ==========
watch(
  localSocialMedia,
  (newVal) => {
    emit('update:modelValue', { ...newVal })
  },
  { deep: true }
)

watch(
  () => props.modelValue,
  (newVal) => {
    localSocialMedia.value = { ...newVal }
  },
  { deep: true }
)
</script>

<style scoped>
/* ========== Container ========== */
.social-media-fields {
  width: 100%;
}

/* ========== Header ========== */
.section-header {
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.5rem 0;
}

.section-subtitle {
  margin: 0;
  color: #6B7280;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* ========== Social Fields Grid ========== */
.social-fields-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.social-field {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  color: #374151;
  font-size: 0.95rem;
}

/* ========== Social Icons ========== */
.social-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}

.social-icon.facebook {
  background: linear-gradient(135deg, #1877F2 0%, #0C63D4 100%);
}

.social-icon.instagram {
  background: linear-gradient(135deg, #E4405F 0%, #C13584 50%, #833AB4 100%);
}

.social-icon.tiktok {
  background: linear-gradient(135deg, #000000 0%, #333333 100%);
}

.social-icon.linkedin {
  background: linear-gradient(135deg, #0A66C2 0%, #004182 100%);
}

.social-icon.twitter {
  background: linear-gradient(135deg, #1DA1F2 0%, #0C85D0 100%);
}

.social-icon.youtube {
  background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
}

/* ========== Input Styling ========== */
.input-prefix {
  font-size: 0.85rem;
  color: #9CA3AF;
  font-weight: 500;
}

/* ========== Tips ========== */
.social-tips {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%);
  border-left: 4px solid #3B82F6;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.tips-content {
  flex: 1;
}

.tips-content strong {
  display: block;
  margin-bottom: 0.5rem;
  color: #1E40AF;
  font-size: 0.95rem;
}

.tips-content ul {
  margin: 0;
  padding-left: 1.25rem;
  color: #4B5563;
  font-size: 0.875rem;
  line-height: 1.6;
}

.tips-content li {
  margin-bottom: 0.25rem;
}

/* ========== Preview Section ========== */
.social-preview {
  padding: 1.5rem;
  background: #F9FAFB;
  border-radius: 12px;
  border: 2px solid #E5E7EB;
}

.preview-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 1rem 0;
}

.preview-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.social-preview-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  text-decoration: none;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.social-preview-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.social-preview-btn.facebook {
  background: linear-gradient(135deg, #1877F2 0%, #0C63D4 100%);
}

.social-preview-btn.instagram {
  background: linear-gradient(135deg, #E4405F 0%, #C13584 50%, #833AB4 100%);
}

.social-preview-btn.tiktok {
  background: linear-gradient(135deg, #000000 0%, #333333 100%);
}

.social-preview-btn.linkedin {
  background: linear-gradient(135deg, #0A66C2 0%, #004182 100%);
}

.social-preview-btn.twitter {
  background: linear-gradient(135deg, #1DA1F2 0%, #0C85D0 100%);
}

.social-preview-btn.youtube {
  background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .social-fields-grid {
    grid-template-columns: 1fr;
  }

  .social-tips {
    flex-direction: column;
    gap: 0.75rem;
  }

  .preview-buttons {
    flex-direction: column;
  }

  .social-preview-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>