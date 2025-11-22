<!-- frontend/src/components/SEO/SEOFields.vue -->
<template>
  <div class="seo-fields">

    <!-- ✨ CHECKLIST SEO -->
    <div class="seo-checklist">
      <div class="checklist-header">
        <div class="checklist-header-left">
          <h4 class="section-title">
            <va-icon name="checklist" size="small" />
            Checklist SEO
          </h4>
        </div>
        
        <!-- ✨ SEO SCORE INTEGRADO -->
        <div class="seo-score-badge">
          <span class="score-label">Puntuación</span>
          <div class="score-circle" :class="scoreClass">
            <span class="score-number">{{ seoScore }}</span>
            <span class="score-total">/100</span>
          </div>
          <span class="score-status">{{ scoreMessage }}</span>
        </div>
      </div>
      
      <div class="checklist-items">
        <div 
          v-for="item in checklistItems" 
          :key="item.id"
          class="checklist-item"
          :class="{ completed: item.completed }"
        >
          <va-icon 
            :name="item.completed ? 'check_circle' : 'radio_button_unchecked'" 
            :color="item.completed ? 'success' : 'secondary'"
            size="small"
          />
          <span>{{ item.label }}</span>
        </div>
      </div>
    </div>

    <!-- ✨ FORMULARIO DE CAMPOS SEO -->
    <div class="seo-form-section">
      
      <!-- Título SEO -->
      <div class="form-field-card">
        <VaInput
          v-model="localSeoData.title"
          label="Título SEO *"
          placeholder="Tu servicio principal | Tu ciudad"
          counter
          :max-length="60"
          :rules="[
            v => !!v || 'Campo requerido',
            v => v.length >= 30 || 'Mínimo 30 caracteres para mejor SEO',
            v => v.length <= 60 || 'Máximo 60 caracteres'
          ]"
        >
          <template #appendInner>
            <va-icon :name="titleValidation.icon" :color="titleValidation.color" />
          </template>
        </VaInput>
        <div class="field-hint" :style="{ color: titleValidation.color }">
          {{ titleValidation.message }}
        </div>
      </div>

      <!-- Slug con Auto-generación -->
      <div class="form-field-card">
        <div class="field-header">
          <VaInput
            v-model="localSeoData.slug"
            label="URL Personalizada (Slug) *"
            placeholder="tu-servicio-ciudad"
            :rules="[
              v => !!v || 'Campo requerido',
              v => /^[a-z0-9-]+$/.test(v) || 'Solo letras minúsculas, números y guiones',
              v => v.length >= 3 || 'Mínimo 3 caracteres',
              v => v.length <= 100 || 'Máximo 100 caracteres'
            ]"
            @update:model-value="handleSlugChange"
          >
            <template #appendInner>
              <va-button
                preset="plain"
                size="small"
                @click="generateSlugFromTitle"
                title="Generar desde título"
              >
                <va-icon name="auto_fix_high" />
              </va-button>
            </template>
          </VaInput>
        </div>
        
        <div class="slug-preview">
          <va-icon name="link" size="small" />
          <span>{{ previewUrl }}</span>
          <va-button
            v-if="!isSlugUnique"
            preset="plain"
            size="small"
            color="danger"
          >
            <va-icon name="warning" size="small" />
            No único
          </va-button>
        </div>

        <!-- ✨ AI Suggestion -->
        <div v-if="slugSuggestion" class="ai-suggestion">
          <va-icon name="lightbulb" size="small" color="warning" />
          <span>Sugerencia: </span>
          <button @click="applySuggestion('slug', slugSuggestion)" class="suggestion-btn">
            {{ slugSuggestion }}
          </button>
        </div>
      </div>

      <!-- Palabra Clave Principal con Densidad -->
      <div class="form-field-card">
        <VaInput
          v-model="localSeoData.mainKeyword"
          label="Palabra Clave Principal *"
          placeholder="Tu producto o servicio principal"
          :rules="[v => !!v || 'Campo requerido']"
          counter
          :max-length="100"
        >
          <template #appendInner>
            <VaIcon name="key" />
          </template>
        </VaInput>

        <!-- ✨ Densidad de Keyword -->
        <div v-if="keywordDensity > 0" class="keyword-density">
          <span class="density-label">Densidad en contenido:</span>
          <va-progress-bar 
            :model-value="keywordDensity * 100" 
            :color="densityColor"
            size="small"
            style="width: 100px;"
          />
          <span class="density-value">{{ (keywordDensity * 100).toFixed(1) }}%</span>
          <span class="density-status" :style="{ color: densityColor }">
            {{ densityStatus }}
          </span>
        </div>
      </div>

      <!-- Tags / Keywords con Sugerencias -->
      <div class="form-field-card">
        <div class="field-label">
          <label>
            <va-icon name="tag" size="small" />
            Palabras Clave / Tags (Máximo {{ maxTags }})
          </label>
        </div>
        
        <VaInput
          v-model="newTag"
          placeholder="Ej: restaurante, comida, lapaz"
          @keyup.enter="addTag"
        >
          <template #appendInner>
            <VaButton
              preset="plain"
              icon="add"
              size="small"
              @click="addTag"
              :disabled="localSeoData.tags.length >= maxTags"
            />
          </template>
        </VaInput>
        
        <div class="field-hint">
          💡 No uses # en tags SEO. Solo palabras clave simples para mejor indexación.
        </div>

        <!-- ✨ Tags Sugeridos -->
        <div v-if="suggestedTags.length > 0" class="suggested-tags">
          <span class="suggestion-label">
            <va-icon name="auto_awesome" size="small" />
            Sugeridos:
          </span>
          <va-chip
            v-for="tag in suggestedTags"
            :key="tag"
            size="small"
            color="purple"
            outline
            @click="addSuggestedTag(tag)"
          >
            + {{ tag }}
          </va-chip>
        </div>

        <div v-if="localSeoData.tags.length > 0" class="tags-container">
          <VaChip
            v-for="(tag, index) in localSeoData.tags"
            :key="index"
            closeable
            color="purple"
            @update:model-value="removeTag(index)"
          >
            {{ tag }}
          </VaChip>
        </div>
      </div>

      <!-- Meta Descripción con Análisis - FULL WIDTH -->
      <div class="form-field-card form-field-full">
        <VaTextarea
          v-model="localSeoData.metaDescription"
          label="Meta Descripción *"
          placeholder="Describe brevemente tu servicio o producto. Aparecerá en resultados de búsqueda."
          :min-rows="3"
          :max-rows="5"
          counter
          :max-length="160"
          :rules="[
            v => !!v || 'Campo requerido',
            v => v.length >= 120 || 'Mínimo 120 caracteres para mejor SEO',
            v => v.length <= 160 || 'Máximo 160 caracteres'
          ]"
        />
        
        <!-- ✨ Análisis de Meta -->
        <div class="meta-analysis">
          <div class="analysis-item" :class="metaAnalysis.length.status">
            <va-icon :name="metaAnalysis.length.icon" size="small" />
            <span>{{ metaAnalysis.length.message }}</span>
          </div>
          <div class="analysis-item" :class="metaAnalysis.keyword.status">
            <va-icon :name="metaAnalysis.keyword.icon" size="small" />
            <span>{{ metaAnalysis.keyword.message }}</span>
          </div>
          <div class="analysis-item" :class="metaAnalysis.cta.status">
            <va-icon :name="metaAnalysis.cta.icon" size="small" />
            <span>{{ metaAnalysis.cta.message }}</span>
          </div>
        </div>
      </div>

      <!-- Palabras Clave de Ubicación -->
      <div class="form-field-card">
        <VaInput
          v-model="localSeoData.locationKeywords"
          label="Palabras Clave de Ubicación"
          placeholder="Tu ciudad, zona, región"
        >
          <template #appendInner>
            <VaIcon name="place" />
          </template>
        </VaInput>
        <div class="field-hint">
          Separa múltiples ubicaciones con comas (Ej: La Paz, Zona Sur, Sopocachi)
        </div>
      </div>

    </div>

    <!-- ✨ Consejos SEO -->
    <div class="seo-tips">
      <h4 class="section-title">
        <va-icon name="tips_and_updates" size="small" />
        Consejos para mejorar tu SEO
      </h4>
      <ul class="tips-list">
        <li>
          <va-icon name="check_circle" size="small" color="success" />
          Usa palabras clave relevantes de forma natural en tu contenido
        </li>
        <li>
          <va-icon name="check_circle" size="small" color="success" />
          Mantén tu título entre 50-60 caracteres para mejor visualización
        </li>
        <li>
          <va-icon name="check_circle" size="small" color="success" />
          Incluye ubicación geográfica en tus palabras clave
        </li>
        <li>
          <va-icon name="check_circle" size="small" color="success" />
          Actualiza tu contenido regularmente para mantenerlo relevante
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { VaInput, VaTextarea, VaButton, VaIcon, VaChip, VaProgressBar } from 'vuestic-ui'

// ==================== PROPS & EMITS ====================
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  businessTitle: {
    type: String,
    default: ''
  },
  businessDescription: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'validation-change'])

// ==================== STATE ====================
const localSeoData = ref({
  slug: props.modelValue.slug || '',
  title: props.modelValue.title || '',
  mainKeyword: props.modelValue.mainKeyword || '',
  tags: props.modelValue.tags || [],
  metaDescription: props.modelValue.metaDescription || '',
  locationKeywords: props.modelValue.locationKeywords || ''
})

const newTag = ref('')
const maxTags = 10
const baseUrl = 'guiaspurpuras.com'
const isSlugUnique = ref(true)
const slugSuggestion = ref('')

// ==================== COMPUTED - Validaciones ====================
const isFormValid = computed(() => {
  const hasSlug = localSeoData.value.slug && 
                  localSeoData.value.slug.length >= 3 && 
                  /^[a-z0-9-]+$/.test(localSeoData.value.slug)
  
  const hasTitle = localSeoData.value.title && 
                   localSeoData.value.title.length >= 30 && 
                   localSeoData.value.title.length <= 60
  
  const hasKeyword = !!localSeoData.value.mainKeyword
  
  const hasDescription = localSeoData.value.metaDescription && 
                         localSeoData.value.metaDescription.length >= 120 && 
                         localSeoData.value.metaDescription.length <= 160

  return hasSlug && hasTitle && hasKeyword && hasDescription
})

// ==================== COMPUTED - SEO Score ====================
const seoScore = computed(() => {
  let score = 0
  
  if (localSeoData.value.slug && /^[a-z0-9-]+$/.test(localSeoData.value.slug)) {
    score += 20
  }
  
  if (localSeoData.value.title) {
    const titleLen = localSeoData.value.title.length
    if (titleLen >= 30 && titleLen <= 60) score += 25
    else if (titleLen >= 20) score += 15
  }
  
  if (localSeoData.value.mainKeyword) {
    score += 20
  }
  
  if (localSeoData.value.metaDescription) {
    const descLen = localSeoData.value.metaDescription.length
    if (descLen >= 120 && descLen <= 160) score += 25
    else if (descLen >= 80) score += 15
  }
  
  if (localSeoData.value.tags.length >= 3) score += 10
  else if (localSeoData.value.tags.length > 0) score += 5
  
  return score
})

const scoreColor = computed(() => {
  if (seoScore.value >= 80) return 'success'
  if (seoScore.value >= 50) return 'warning'
  return 'danger'
})

const scoreClass = computed(() => {
  if (seoScore.value >= 80) return 'score-excellent'
  if (seoScore.value >= 50) return 'score-good'
  return 'score-poor'
})

const scoreMessage = computed(() => {
  if (seoScore.value >= 80) return '¡Excelente! Tu SEO está bien optimizado'
  if (seoScore.value >= 50) return 'Bien, pero hay margen de mejora'
  return 'Necesitas optimizar más campos'
})

// ==================== COMPUTED - Checklist ====================
const checklistItems = computed(() => [
  {
    id: 'slug',
    label: 'URL amigable configurada',
    completed: localSeoData.value.slug && /^[a-z0-9-]+$/.test(localSeoData.value.slug)
  },
  {
    id: 'title',
    label: 'Título SEO optimizado (30-60 caracteres)',
    completed: localSeoData.value.title && 
               localSeoData.value.title.length >= 30 && 
               localSeoData.value.title.length <= 60
  },
  {
    id: 'keyword',
    label: 'Palabra clave principal definida',
    completed: !!localSeoData.value.mainKeyword
  },
  {
    id: 'description',
    label: 'Meta descripción completa (120-160 caracteres)',
    completed: localSeoData.value.metaDescription && 
               localSeoData.value.metaDescription.length >= 120 && 
               localSeoData.value.metaDescription.length <= 160
  },
  {
    id: 'tags',
    label: 'Al menos 3 tags relevantes',
    completed: localSeoData.value.tags.length >= 3
  }
])

// ==================== COMPUTED - Title Validation ====================
const titleValidation = computed(() => {
  const len = localSeoData.value.title?.length || 0
  
  if (len === 0) {
    return { icon: 'help', color: 'secondary', message: 'Escribe un título descriptivo' }
  }
  if (len < 30) {
    return { icon: 'warning', color: 'warning', message: `Añade ${30 - len} caracteres más` }
  }
  if (len <= 60) {
    return { icon: 'check_circle', color: 'success', message: '¡Longitud perfecta!' }
  }
  return { icon: 'error', color: 'danger', message: 'Título muy largo' }
})

// ==================== COMPUTED - Keyword Density ====================
const keywordDensity = computed(() => {
  const keyword = localSeoData.value.mainKeyword?.toLowerCase()
  if (!keyword) return 0
  
  const fullText = `${localSeoData.value.title} ${localSeoData.value.metaDescription}`.toLowerCase()
  const words = fullText.split(/\s+/).length
  const keywordCount = (fullText.match(new RegExp(keyword, 'g')) || []).length
  
  return words > 0 ? keywordCount / words : 0
})

const densityColor = computed(() => {
  const density = keywordDensity.value
  if (density >= 0.02 && density <= 0.05) return 'success'
  if (density > 0.05) return 'warning'
  return 'info'
})

const densityStatus = computed(() => {
  const density = keywordDensity.value
  if (density >= 0.02 && density <= 0.05) return 'Óptimo'
  if (density > 0.05) return 'Muy alto'
  return 'Bajo'
})

// ==================== COMPUTED - Meta Analysis ====================
const metaAnalysis = computed(() => {
  const desc = localSeoData.value.metaDescription || ''
  const keyword = localSeoData.value.mainKeyword?.toLowerCase() || ''
  
  return {
    length: desc.length >= 120 && desc.length <= 160
      ? { status: 'good', icon: 'check_circle', message: 'Longitud óptima' }
      : { status: 'warning', icon: 'warning', message: 'Ajusta la longitud (120-160)' },
    
    keyword: desc.toLowerCase().includes(keyword)
      ? { status: 'good', icon: 'check_circle', message: 'Contiene palabra clave' }
      : { status: 'info', icon: 'info', message: 'Considera incluir tu palabra clave' },
    
    cta: /contáctanos|llama|visita|descubre|conoce|solicita/i.test(desc)
      ? { status: 'good', icon: 'check_circle', message: 'Tiene llamado a la acción' }
      : { status: 'info', icon: 'lightbulb', message: 'Añade un llamado a la acción' }
  }
})

// ==================== COMPUTED - Suggested Tags ====================
const suggestedTags = computed(() => {
  const suggestions = []
  const keyword = localSeoData.value.mainKeyword?.toLowerCase()
  
  if (keyword && !localSeoData.value.tags.includes(keyword)) {
    suggestions.push(keyword)
  }
  
  if (localSeoData.value.locationKeywords) {
    const locations = localSeoData.value.locationKeywords.split(',').map(l => l.trim())
    locations.forEach(loc => {
      if (loc && !localSeoData.value.tags.includes(loc.toLowerCase())) {
        suggestions.push(loc.toLowerCase())
      }
    })
  }
  
  return suggestions.slice(0, 5)
})

// ==================== COMPUTED - Preview URL ====================
const previewUrl = computed(() => {
  return localSeoData.value.slug 
    ? `${baseUrl}/${localSeoData.value.slug}`
    : `${baseUrl}/tu-slug-aqui`
})

// ==================== METHODS ====================
const handleSlugChange = (value) => {
  localSeoData.value.slug = value
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '')
}

const generateSlugFromTitle = () => {
  const source = props.businessTitle || localSeoData.value.title
  if (source) {
    localSeoData.value.slug = source
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s-]/g, '')
      .trim()
      .replace(/\s+/g, '-')
      .substring(0, 100)
  }
}

const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !localSeoData.value.tags.includes(tag) && localSeoData.value.tags.length < maxTags) {
    localSeoData.value.tags.push(tag)
    newTag.value = ''
  }
}

const addSuggestedTag = (tag) => {
  if (!localSeoData.value.tags.includes(tag) && localSeoData.value.tags.length < maxTags) {
    localSeoData.value.tags.push(tag)
  }
}

const removeTag = (index) => {
  localSeoData.value.tags.splice(index, 1)
}

const formatTag = (tag) => {
  return tag
}

const applySuggestion = (field, value) => {
  localSeoData.value[field] = value
  if (field === 'slug') slugSuggestion.value = ''
}

const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

// ==================== WATCHERS ====================
let validationTimeout = null

watch(() => localSeoData.value, (newVal) => {
  emit('update:modelValue', { ...newVal })
  
  if (validationTimeout) {
    clearTimeout(validationTimeout)
  }
  
  validationTimeout = setTimeout(() => {
    emit('validation-change', isFormValid.value)
  }, 300)
}, { deep: true })

watch(() => props.businessTitle, (newTitle) => {
  if (newTitle && !localSeoData.value.slug) {
    generateSlugFromTitle()
  }
})
</script>

<style scoped>
/* ========== Variables ========== */
:root {
  --color-purple: #7C3AED;
  --color-purple-light: #A78BFA;
  --color-purple-dark: #5B21B6;
  --color-gray-50: #F9FAFB;
  --color-gray-100: #F3F4F6;
  --color-gray-200: #E5E7EB;
  --color-gray-600: #6B7280;
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
}

/* ========== Layout Principal ========== */
.seo-fields {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
}

/* ✨ Asegurar que todos los inputs sean full width */
.seo-fields :deep(.va-input-wrapper),
.seo-fields :deep(.va-text-area) {
  width: 100%;
}

.seo-fields :deep(.va-input-wrapper__field),
.seo-fields :deep(textarea),
.seo-fields :deep(input) {
  width: 100%;
  box-sizing: border-box;
}

/* ========== Títulos de Sección Unificados ========== */
.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 1.5rem 0;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1F2937;
}

.section-subtitle {
  color: var(--color-gray-600);
  font-size: 0.95rem;
  margin: 0;
}

/* ✨ Checklist SEO */
.seo-checklist {
  margin-bottom: 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
  border-radius: 16px;
  border: 2px solid #E5E7EB;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.checklist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 2rem;
}

.checklist-header-left {
  flex: 1;
}

/* ✨ SEO Score Badge Integrado */
.seo-score-badge {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px solid #E5E7EB;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.score-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.score-circle {
  display: flex;
  align-items: baseline;
  justify-content: center;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  flex-direction: column;
  align-items: center;
  padding: 0.75rem;
}

.score-circle.score-excellent {
  background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.score-circle.score-good {
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.score-circle.score-poor {
  background: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.score-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
  line-height: 1;
}

.score-total {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1;
}

.score-status {
  font-size: 0.875rem;
  font-weight: 600;
  color: #4B5563;
  max-width: 100px;
  line-height: 1.3;
}

.checklist-items {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
}

.checklist-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: white;
  border-radius: 10px;
  font-size: 0.9rem;
  color: #6B7280;
  transition: all 0.2s;
  border: 1px solid #F3F4F6;
}

.checklist-item.completed {
  color: var(--color-success);
  font-weight: 500;
  background: #F0FDF4;
  border-color: #BBF7D0;
}

/* ========== SECCIÓN DE FORMULARIO CON BORDES ========== */
.seo-form-section {
  padding: 2rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
  border-radius: 16px;
  border: 2px solid #E5E7EB;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  margin-bottom: 3rem;
  width: 100%; /* Asegurar ancho completo */
}

/* ✨ CADA CAMPO EN SU PROPIA CARD */
.form-field-card {
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px solid #F3F4F6;
  margin-bottom: 1.5rem;
  transition: all 0.2s;
  width: 100%; /* Asegurar ancho completo */
  box-sizing: border-box; /* Incluir padding en el ancho */
}

.form-field-card:hover {
  border-color: #E5E7EB;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.form-field-card:last-child {
  margin-bottom: 0;
}

/* ✨ META DESCRIPCIÓN FULL WIDTH */
.form-field-full {
  background: linear-gradient(135deg, #FEFBFF 0%, #FFFFFF 100%);
  border: 2px solid #E9D5FF;
  grid-column: 1 / -1; /* Ocupa todas las columnas disponibles */
}

.form-field-full:hover {
  border-color: #C084FC;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.1);
}

/* Asegurar que el VaTextarea interno también sea full width */
.form-field-full :deep(.va-input-wrapper) {
  width: 100%;
}

.form-field-full :deep(.va-input-wrapper__field) {
  width: 100%;
}

.form-field-full :deep(textarea) {
  width: 100% !important;
  resize: vertical; /* Permite redimensionar verticalmente */
}

.field-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: #374151;
}

.field-hint {
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: var(--color-gray-600);
  line-height: 1.4;
}

/* Slug Preview */
.slug-preview {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #FAFAFA;
  border-radius: 8px;
  color: var(--color-purple);
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  border: 1px solid #E5E7EB;
}

/* ✨ AI Suggestions */
.ai-suggestion {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #FFF9E6;
  border-radius: 8px;
  border-left: 3px solid #F59E0B;
  font-size: 0.875rem;
}

.suggestion-btn {
  background: none;
  border: none;
  color: var(--color-purple);
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
}

.suggestion-btn:hover {
  color: var(--color-purple-dark);
}

/* ✨ Keyword Density */
.keyword-density {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #FAFAFA;
  border-radius: 8px;
  border: 1px solid #E5E7EB;
  font-size: 0.875rem;
}

.density-label {
  font-weight: 600;
  color: #666;
}

.density-value {
  font-weight: 600;
  color: #333;
}

.density-status {
  font-weight: 500;
}

/* ✨ Suggested Tags */
.suggested-tags {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #F0F9FF;
  border-radius: 8px;
  border: 1px solid #BFDBFE;
}

.suggestion-label {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #1E40AF;
}

/* Tags Container */
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 1rem;
  background: #FAFAFA;
  border-radius: 8px;
  border: 1px solid #E5E7EB;
}

/* ✨ Meta Analysis */
.meta-analysis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
  margin-top: 1rem;
}

.analysis-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
}

.analysis-item.good {
  background: #F0FDF4;
  color: #15803D;
}

.analysis-item.warning {
  background: #FEF3C7;
  color: #B45309;
}

.analysis-item.info {
  background: #EFF6FF;
  color: #1E40AF;
}

/* ✨ SEO Tips */
.seo-tips {
  padding: 2rem;
  background: linear-gradient(135deg, #DBEAFE 0%, #FFFFFF 100%);
  border-radius: 16px;
  border: 2px solid #BFDBFE;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08);
}

.tips-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.tips-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  color: #0369A1;
  line-height: 1.5;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .seo-fields {
    padding: 1.5rem;
  }

  .checklist-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .seo-score-badge {
    width: 100%;
    justify-content: space-between;
  }

  .checklist-items {
    grid-template-columns: 1fr;
  }

  .seo-form-section {
    padding: 1.5rem;
  }

  .form-field-card {
    padding: 1.25rem;
  }
}
</style>