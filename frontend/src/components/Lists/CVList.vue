<!-- frontend/src/components/CV/CVList.vue -->
<template>
  <div class="cv-list">
    
    <!-- Header -->
    <div class="cv-list-header">
      <h3>
        <va-icon name="folder" />
        Mis CVs Guardados ({{ cvCount }}/{{ MAX_CVS }})
      </h3>
      <p class="cv-list-subtitle">
        Selecciona un CV para usar en tu postulación
      </p>
    </div>

    <!-- Lista de CVs -->
    <div v-if="savedCVs.length > 0" class="cv-items">
      <div 
        v-for="cv in savedCVs" 
        :key="cv.id"
        class="cv-item"
        :class="{ selected: selectedCVId === cv.id }"
      >
        <!-- Radio Button -->
        <div class="cv-radio">
          <VaRadio
            :model-value="selectedCVId"
            :option="cv.id"
            @update:model-value="handleSelect(cv.id)"
          />
        </div>

        <!-- CV Info -->
        <div class="cv-info" @click="handleSelect(cv.id)">
          <div class="cv-title-row">
            <h4 class="cv-title">{{ cv.title }}</h4>
            <VaChip
              v-if="cv.isDefault"
              size="small"
              color="warning"
            >
              <va-icon name="star" size="small" />
              Predeterminado
            </VaChip>
          </div>

          <div class="cv-meta">
            <span class="cv-date">
              <va-icon name="schedule" size="small" />
              Actualizado: {{ formatDate(cv.updatedAt) }}
            </span>
          </div>

          <!-- Mini stats -->
          <div class="cv-stats">
            <span class="stat" v-if="cv.data.education.length > 0">
              <va-icon name="school" size="small" />
              {{ cv.data.education.length }}
            </span>
            <span class="stat" v-if="cv.data.experience.length > 0">
              <va-icon name="work" size="small" />
              {{ cv.data.experience.length }}
            </span>
            <span class="stat" v-if="cv.data.skills.length > 0">
              <va-icon name="psychology" size="small" />
              {{ cv.data.skills.length }}
            </span>
            <span class="stat" v-if="cv.data.languages.length > 0">
              <va-icon name="translate" size="small" />
              {{ cv.data.languages.length }}
            </span>
          </div>
        </div>

        <!-- Actions -->
        <div class="cv-actions">
          <VaButton
            preset="plain"
            icon="visibility"
            size="small"
            @click.stop="handlePreview(cv)"
            title="Ver CV"
          />
          <VaButton
            preset="plain"
            icon="edit"
            size="small"
            @click.stop="handleEdit(cv)"
            title="Editar"
          />
          <VaButton
            v-if="!cv.isDefault"
            preset="plain"
            icon="star_border"
            size="small"
            @click.stop="handleSetDefault(cv.id)"
            title="Marcar como predeterminado"
          />
          <VaButton
            preset="plain"
            icon="delete"
            color="danger"
            size="small"
            @click.stop="handleDelete(cv.id)"
            title="Eliminar"
          />
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="cv-empty-state">
      <va-icon name="folder_open" size="4rem" color="#CCC" />
      <p>No tienes CVs guardados</p>
      <p class="empty-subtitle">Crea tu primer CV para poder reutilizarlo</p>
    </div>

    <!-- Create Button (si no ha llegado al límite) -->
    <div v-if="!hasReachedLimit" class="cv-list-footer">
      <VaButton
        @click="handleCreateNew"
        color="purple"
        preset="secondary"
        icon="add"
        block
      >
        Crear Nuevo CV ({{ cvCount }}/{{ MAX_CVS }})
      </VaButton>
    </div>

    <!-- Limit Warning -->
    <div v-else class="cv-limit-warning">
      <va-icon name="info" />
      <span>Has alcanzado el límite de {{ MAX_CVS }} CVs. Elimina uno para crear otro.</span>
    </div>

    <!-- Preview Modal -->
    <VaModal
      v-model="showPreviewModal"
      size="large"
      title="Vista Previa del CV"
      ok-text="Cerrar"
      :hide-default-actions="false"
    >
      <div v-if="previewCV" class="cv-full-preview">
        <!-- Datos Personales -->
        <div class="preview-section">
          <h4 class="preview-section-title">
            <va-icon name="person" size="small" />
            Datos Personales
          </h4>
          <div class="preview-content">
            <p><strong>Nombre:</strong> {{ previewCV.data.personalInfo.firstName }} {{ previewCV.data.personalInfo.lastName }}</p>
            <p><strong>Email:</strong> {{ previewCV.data.personalInfo.email }}</p>
            <p><strong>Teléfono:</strong> {{ previewCV.data.personalInfo.phone }}</p>
            <p><strong>Ciudad:</strong> {{ previewCV.data.personalInfo.city }}</p>
            <p v-if="previewCV.data.personalInfo.linkedin"><strong>LinkedIn:</strong> {{ previewCV.data.personalInfo.linkedin }}</p>
            <p class="preview-summary">{{ previewCV.data.personalInfo.summary }}</p>
          </div>
        </div>

        <!-- Formación -->
        <div v-if="previewCV.data.education.length > 0" class="preview-section">
          <h4 class="preview-section-title">
            <va-icon name="school" size="small" />
            Formación Académica
          </h4>
          <div 
            v-for="(edu, index) in previewCV.data.education"
            :key="index"
            class="preview-item"
          >
            <h5>{{ edu.degree }}</h5>
            <p>{{ edu.institution }} - {{ edu.level }}</p>
            <p v-if="edu.description">{{ edu.description }}</p>
          </div>
        </div>

        <!-- Experiencia -->
        <div v-if="previewCV.data.experience.length > 0" class="preview-section">
          <h4 class="preview-section-title">
            <va-icon name="work" size="small" />
            Experiencia Laboral
          </h4>
          <div 
            v-for="(exp, index) in previewCV.data.experience"
            :key="index"
            class="preview-item"
          >
            <h5>{{ exp.position }}</h5>
            <p>{{ exp.company }} - {{ exp.employmentType }}</p>
            <p>{{ exp.description }}</p>
          </div>
        </div>

        <!-- Habilidades -->
        <div v-if="previewCV.data.skills.length > 0" class="preview-section">
          <h4 class="preview-section-title">
            <va-icon name="psychology" size="small" />
            Habilidades
          </h4>
          <div class="preview-skills">
            <span 
              v-for="(skill, index) in previewCV.data.skills"
              :key="index"
              class="preview-skill"
            >
              {{ skill }}
            </span>
          </div>
        </div>

        <!-- Idiomas -->
        <div v-if="previewCV.data.languages.length > 0" class="preview-section">
          <h4 class="preview-section-title">
            <va-icon name="translate" size="small" />
            Idiomas
          </h4>
          <div class="preview-content">
            <p 
              v-for="(lang, index) in previewCV.data.languages"
              :key="index"
            >
              <strong>{{ lang.name }}:</strong> {{ lang.level }}
            </p>
          </div>
        </div>
      </div>
    </VaModal>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCVStore } from '@/composables/useCVStore'

// ========== PROPS & EMITS ==========
const props = defineProps({
  modelValue: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'create-new', 'edit'])

// ========== COMPOSABLES ==========
const { 
  savedCVs, 
  cvCount, 
  hasReachedLimit, 
  MAX_CVS,
  deleteCV,
  setDefaultCV,
  formatDate
} = useCVStore()

// ========== STATE ==========
const showPreviewModal = ref(false)
const previewCV = ref(null)

// ========== COMPUTED ==========
const selectedCVId = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// ========== METHODS ==========
const handleSelect = (cvId) => {
  selectedCVId.value = cvId
}

const handlePreview = (cv) => {
  previewCV.value = cv
  showPreviewModal.value = true
}

const handleEdit = (cv) => {
  emit('edit', cv)
}

const handleDelete = (cvId) => {
  if (confirm('¿Estás seguro de eliminar este CV? Esta acción no se puede deshacer.')) {
    deleteCV(cvId)
    
    // Si era el seleccionado, deseleccionar
    if (selectedCVId.value === cvId) {
      selectedCVId.value = null
    }
  }
}

const handleSetDefault = (cvId) => {
  setDefaultCV(cvId)
}

const handleCreateNew = () => {
  emit('create-new')
}
</script>

<style scoped>
/* ========== Container ========== */
.cv-list {
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

/* ========== Header ========== */
.cv-list-header {
  margin-bottom: 1.5rem;
}

.cv-list-header h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
}

.cv-list-subtitle {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

/* ========== CV Items ========== */
.cv-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.cv-item {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: #F8F8F8;
  border: 2px solid transparent;
  border-radius: 12px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.cv-item:hover {
  background: #F0F0F0;
  border-color: rgba(92, 0, 153, 0.2);
}

.cv-item.selected {
  background: rgba(92, 0, 153, 0.05);
  border-color: var(--color-purple);
}

.cv-radio {
  display: flex;
  align-items: flex-start;
  padding-top: 0.25rem;
}

.cv-info {
  flex: 1;
  min-width: 0;
}

.cv-title-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.cv-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.cv-meta {
  margin-bottom: 0.75rem;
}

.cv-date {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  color: #666;
}

.cv-stats {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.stat {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  color: var(--color-purple);
  font-weight: 500;
}

.cv-actions {
  display: flex;
  gap: 0.25rem;
  align-items: flex-start;
}

/* ========== Empty State ========== */
.cv-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.cv-empty-state p {
  margin: 1rem 0 0 0;
  color: #666;
  font-size: 1rem;
}

.empty-subtitle {
  color: #999 !important;
  font-size: 0.9rem !important;
}

/* ========== Footer ========== */
.cv-list-footer {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #E0E0E0;
}

/* ========== Limit Warning ========== */
.cv-limit-warning {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #FFF3E0;
  border: 1px solid #FFB74D;
  border-radius: 8px;
  color: #F57C00;
  font-size: 0.9rem;
  margin-top: 1rem;
}

/* ========== Preview Modal ========== */
.cv-full-preview {
  max-height: 70vh;
  overflow-y: auto;
  padding: 1rem;
}

.preview-section {
  padding: 1.5rem;
  background: #F8F8F8;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.preview-section:last-child {
  margin-bottom: 0;
}

.preview-section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #E0E0E0;
}

.preview-content p {
  margin: 0 0 0.5rem 0;
  color: #333;
  line-height: 1.6;
}

.preview-summary {
  margin-top: 1rem !important;
  font-style: italic;
  background: white;
  padding: 1rem;
  border-radius: 8px;
}

.preview-item {
  padding: 1rem;
  background: white;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.preview-item:last-child {
  margin-bottom: 0;
}

.preview-item h5 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.preview-item p {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.preview-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preview-skill {
  padding: 0.5rem 1rem;
  background: var(--color-purple);
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .cv-item {
    flex-direction: column;
  }

  .cv-radio {
    order: -1;
  }

  .cv-actions {
    justify-content: center;
    padding-top: 1rem;
    border-top: 1px solid #E0E0E0;
  }

  .cv-stats {
    gap: 0.5rem;
  }
}
</style>