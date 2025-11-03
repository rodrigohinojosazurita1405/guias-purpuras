<!-- frontend/src/components/SEO/SEOFields.vue -->
<template>
  <div class="seo-fields">
    
    <div class="seo-header">
      <h3 class="seo-title">
        <va-icon name="search" color="purple" />
        Optimización SEO
      </h3>
      <p class="seo-subtitle">
        Estos datos ayudarán a que tu {{ entityType }} aparezca en búsquedas relevantes
      </p>
    </div>

    <!-- Slug -->
    <div class="form-field">
      <VaInput
        v-model="localSeoData.slug"
        label="URL Personalizada (Slug) *"
        placeholder="mi-negocio-cochabamba"
        :rules="[
          v => !!v || 'Campo requerido',
          v => /^[a-z0-9-]+$/.test(v) || 'Solo letras minúsculas, números y guiones',
          v => v.length >= 3 || 'Mínimo 3 caracteres'
        ]"
        @update:model-value="handleSlugChange"
      >
        <template #messages>
          <div class="slug-preview">
            <va-icon name="link" size="small" />
            <span>{{ previewUrl }}</span>
          </div>
        </template>
      </VaInput>
    </div>

    <!-- Palabra Clave Principal -->
    <div class="form-field">
      <VaInput
        v-model="localSeoData.mainKeyword"
        label="Palabra Clave Principal *"
        placeholder="Ej: Fábrica de plásticos"
        :rules="[v => !!v || 'Campo requerido']"
        counter
        :max-length="100"
      >
        <template #appendInner>
          <VaIcon name="key" />
        </template>
      </VaInput>
    </div>

    <!-- Tags / Hashtags -->
    <div class="form-field">
      <div class="field-label">
        <label>
          <va-icon name="tag" size="small" />
          Tags / Hashtags (Máximo {{ maxTags }})
        </label>
      </div>
      
      <VaInput
        v-model="newTag"
        placeholder="Escribe un tag y presiona Enter"
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

      <div v-if="localSeoData.tags.length > 0" class="tags-container">
        <VaChip
          v-for="(tag, index) in localSeoData.tags"
          :key="index"
          closeable
          color="purple"
          @update:model-value="removeTag(index)"
        >
          {{ formatTag(tag) }}
        </VaChip>
      </div>

      <div v-else class="empty-tags">
        <p>No has agregado tags. Presiona Enter o el botón + para agregar.</p>
      </div>
    </div>

    <!-- Meta Descripción -->
    <div class="form-field">
      <VaTextarea
        v-model="localSeoData.metaDescription"
        label="Meta Descripción *"
        placeholder="Descripción breve que aparecerá en buscadores (Google, Bing, etc.)"
        :min-rows="3"
        :max-rows="5"
        counter
        :max-length="160"
        :rules="[
          v => !!v || 'Campo requerido',
          v => v.length >= 50 || 'Mínimo 50 caracteres para mejor SEO',
          v => v.length <= 160 || 'Máximo 160 caracteres'
        ]"
      />
      <div class="meta-tip">
        <va-icon name="info" size="small" />
        <span>Recomendado: 150-160 caracteres para aparecer completo en Google</span>
      </div>
    </div>

    <!-- Palabras Clave de Ubicación -->
    <div class="form-field">
      <VaInput
        v-model="localSeoData.locationKeywords"
        label="Palabras Clave de Ubicación"
        placeholder="Ej: Cochabamba, Zona Sur, Quillacollo"
      >
        <template #appendInner>
          <VaIcon name="place" />
        </template>
      </VaInput>
      <div class="field-hint">
        Separa múltiples ubicaciones con comas
      </div>
    </div>

    <!-- Categorías SEO -->
    <div class="form-field">
      <div class="field-label">
        <label>
          <va-icon name="category" size="small" />
          Categorías SEO (Selecciona hasta {{ maxCategories }})
        </label>
      </div>
      
      <div class="categories-grid">
        <VaCheckbox
          v-for="category in availableCategories"
          :key="category.id"
          v-model="category.selected"
          :label="category.name"
          :disabled="!category.selected && selectedCategoriesCount >= maxCategories"
          @update:model-value="handleCategoryChange(category)"
        />
      </div>

      <div v-if="selectedCategoriesCount === 0" class="empty-categories">
        <va-icon name="info" size="small" />
        <span>Selecciona al menos una categoría</span>
      </div>
    </div>

    <!-- Preview de Buscador -->
    <div class="search-preview">
      <div class="preview-label">
        <va-icon name="preview" size="small" />
        Vista previa en Google
      </div>
      <div class="google-preview">
        <div class="preview-url">{{ previewUrl }}</div>
        <div class="preview-title">{{ localSeoData.mainKeyword || 'Tu palabra clave principal' }}</div>
        <div class="preview-description">{{ localSeoData.metaDescription || 'Tu descripción aparecerá aquí...' }}</div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useToast } from 'vuestic-ui'

// ========== PROPS ==========
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      slug: '',
      mainKeyword: '',
      tags: [],
      metaDescription: '',
      locationKeywords: '',
      categories: []
    })
  },
  entityType: {
    type: String,
    default: 'negocio'
  },
  baseUrl: {
    type: String,
    default: 'guiaspurpuras.com/negocios'
  },
  maxTags: {
    type: Number,
    default: 10
  },
  maxCategories: {
    type: Number,
    default: 3
  },
  availableCategories: {
    type: Array,
    default: () => [
      { id: 1, name: 'Manufactura', selected: false },
      { id: 2, name: 'Servicios', selected: false },
      { id: 3, name: 'Comercio', selected: false },
      { id: 4, name: 'Tecnología', selected: false },
      { id: 5, name: 'Alimentación', selected: false },
      { id: 6, name: 'Construcción', selected: false },
      { id: 7, name: 'Textil', selected: false },
      { id: 8, name: 'Automotriz', selected: false }
    ]
  }
})

const emit = defineEmits(['update:modelValue'])

// ========== COMPOSABLES ==========
const { init: notify } = useToast()

// ========== STATE ==========
const localSeoData = ref({ ...props.modelValue })
const newTag = ref('')

// ========== COMPUTED ==========
const previewUrl = computed(() => {
  const slug = localSeoData.value.slug || 'tu-slug-aqui'
  return `${props.baseUrl}/${slug}`
})

const selectedCategoriesCount = computed(() => {
  return props.availableCategories.filter(cat => cat.selected).length
})

// ========== WATCH ==========
watch(localSeoData, (newVal) => {
  emit('update:modelValue', newVal)
}, { deep: true })

// ========== METHODS ==========
const handleSlugChange = (value) => {
  // Auto-format slug: lowercase, remove spaces, special chars
  const formatted = value
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove accents
    .replace(/[^a-z0-9-]/g, '-') // Replace special chars with -
    .replace(/-+/g, '-') // Replace multiple - with single
    .replace(/^-|-$/g, '') // Remove leading/trailing -
  
  if (formatted !== value) {
    localSeoData.value.slug = formatted
  }
}

const addTag = () => {
  const tag = newTag.value.trim()
  
  if (!tag) return
  
  if (localSeoData.value.tags.length >= props.maxTags) {
    notify({
      message: `⚠️ Máximo ${props.maxTags} tags permitidos`,
      color: 'warning'
    })
    return
  }

  if (localSeoData.value.tags.includes(tag)) {
    notify({
      message: '⚠️ Este tag ya existe',
      color: 'warning'
    })
    return
  }

  localSeoData.value.tags.push(tag)
  newTag.value = ''
}

const removeTag = (index) => {
  localSeoData.value.tags.splice(index, 1)
}

const formatTag = (tag) => {
  return tag.startsWith('#') ? tag : `#${tag}`
}

const handleCategoryChange = (category) => {
  const selectedCategories = props.availableCategories
    .filter(cat => cat.selected)
    .map(cat => cat.id)
  
  localSeoData.value.categories = selectedCategories
}
</script>

<style scoped>
/* ========== Container ========== */
.seo-fields {
  padding: 2rem;
  background: #F8F4FF;
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

/* ========== Header ========== */
.seo-header {
  margin-bottom: 2rem;
}

.seo-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.seo-subtitle {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

/* ========== Form Fields ========== */
.form-field {
  margin-bottom: 2rem;
}

.field-label {
  margin-bottom: 0.75rem;
}

.field-label label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.field-hint {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #666;
  font-style: italic;
}

/* ========== Slug Preview ========== */
.slug-preview {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  color: var(--color-purple);
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
}

/* ========== Tags ========== */
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
}

.empty-tags {
  margin-top: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  text-align: center;
}

.empty-tags p {
  margin: 0;
  color: #999;
  font-size: 0.9rem;
}

/* ========== Meta Tip ========== */
.meta-tip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: #E3F2FD;
  border-radius: 8px;
  color: #1976D2;
  font-size: 0.85rem;
}

/* ========== Categories ========== */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
}

.empty-categories {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem;
  background: #FFF3E0;
  border-radius: 8px;
  color: #F57C00;
  font-size: 0.85rem;
}

/* ========== Search Preview ========== */
.search-preview {
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #E0E0E0;
}

.preview-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.google-preview {
  padding: 1rem;
  background: #F8F9FA;
  border-radius: 8px;
}

.preview-url {
  font-size: 0.85rem;
  color: #1A73E8;
  margin-bottom: 0.25rem;
}

.preview-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1A0DAB;
  margin-bottom: 0.25rem;
}

.preview-description {
  font-size: 0.9rem;
  color: #545454;
  line-height: 1.5;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .seo-fields {
    padding: 1.5rem;
  }

  .categories-grid {
    grid-template-columns: 1fr;
  }
}
</style>