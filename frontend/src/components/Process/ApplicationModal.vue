<template>
  <!-- Teleport para montar el modal directamente en body y evitar z-index issues -->
  <Teleport to="body">
    <!-- Modal overlay y contenedor custom para móvil -->
    <Transition name="modal-fade">
      <div v-if="internalOpen" class="custom-modal-overlay" @click.self="handleOverlayClick">
      <div class="custom-modal-container" :class="{ 'is-mobile': isMobile }">
        <div class="custom-modal-dialog">
          <!-- Header -->
          <div class="modal-header-content">
        <!-- Job Info -->
        <div class="job-header-info">
          <div class="company-logo-mini" v-if="job.companyLogo">
            <img :src="job.companyLogo" :alt="job.companyName" />
          </div>
          <div class="company-logo-placeholder-mini" v-else>
            <va-icon name="business" size="small" />
          </div>
          <div class="job-info-text">
            <h2 class="job-title-modal">{{ job.title }}</h2>
            <p class="company-name-modal">{{ job.companyName }}</p>
          </div>
        </div>

        <!-- Tabs -->
        <div class="tabs-header">
          <!-- Tab: Mis CVs (solo si tiene CVs guardados) -->
          <button
            v-if="hasSavedCVs"
            class="tab-btn"
            :class="{ active: activeTab === 'saved' }"
            @click="activeTab = 'saved'"
          >
            <va-icon name="folder" size="small" />
            Mis CVs
            <span class="cv-count">{{ savedCVs.length }}</span>
          </button>

          <button
            class="tab-btn"
            :class="{ active: activeTab === 'upload' }"
            @click="activeTab = 'upload'"
          >
            <va-icon name="upload_file" size="small" />
            Subir CV
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'create' }"
            @click="activeTab = 'create'"
          >
            <va-icon name="description" size="small" />
            Crear CV
          </button>
        </div>

        <button class="close-btn" @click="handleClose">
          <va-icon name="close" size="medium" />
        </button>
      </div>

    <!-- Tab Content -->
    <div class="modal-body">
      <!-- Tab: Mis CVs Guardados -->
      <div v-if="activeTab === 'saved'" class="saved-cvs-container">
        <p class="tab-intro">Selecciona un CV guardado para usar en tu postulación</p>

        <div v-if="isLoadingCVs" class="loading-state">
          <va-icon name="sync" size="large" class="spinning" />
          <p>Cargando tus CVs...</p>
        </div>

        <div v-else-if="savedCVs.length === 0" class="empty-state">
          <va-icon name="folder_open" size="3rem" color="#D1D5DB" />
          <p>No tienes CVs guardados todavía</p>
        </div>

        <div v-else class="cvs-list">
          <div
            v-for="cv in savedCVs"
            :key="cv.id"
            class="cv-card"
            :class="{ selected: selectedSavedCV?.id === cv.id }"
            @click="selectCV(cv)"
          >
            <div class="cv-card-header">
              <va-icon
                :name="cv.type === 'file' ? 'description' : 'article'"
                size="large"
                :color="selectedSavedCV?.id === cv.id ? '#7C3AED' : '#6B7280'"
              />
              <div class="cv-card-info">
                <h4>{{ cv.full_name || cv.file_name }}</h4>
                <p class="cv-meta">
                  <span>{{ cv.type === 'file' ? 'Archivo subido' : 'CV creado' }}</span>
                  <span>•</span>
                  <span>{{ formatDate(cv.created_at) }}</span>
                </p>
              </div>
              <va-icon
                v-if="selectedSavedCV?.id === cv.id"
                name="check_circle"
                color="#10B981"
                size="large"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Tab: Subir CV -->
      <UploadCVTab
        v-else-if="activeTab === 'upload'"
        :file="uploadedFile"
        :coverLetter="coverLetter"
        @update:file="uploadedFile = $event"
        @update:coverLetter="coverLetter = $event"
      />

      <!-- Tab: Crear CV -->
      <CreateCVTab
        v-else-if="activeTab === 'create'"
        v-model="cvData"
      />
          </div>

          <!-- Footer -->
          <div class="modal-footer-actions">
            <!-- Botón para guardar CV en dashboard (solo visible en tab "Crear CV") -->
            <button
              v-if="activeTab === 'create'"
              class="btn-save-cv btn-gradient-purple"
              @click="handleSaveCV"
              :disabled="!canSubmit || isSavingCV"
            >
              <va-icon name="save" size="small" />
              {{ isSavingCV ? 'Guardando...' : 'Guardar en Dashboard' }}
            </button>

            <button
              @click="handleSubmit"
              :disabled="!canSubmit"
              class="btn-submit btn-gradient-purple"
            >
              <va-icon name="send" size="small" />
              Enviar Postulación
            </button>

            <button class="btn-cancel" @click="handleClose">
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import UploadCVTab from './UploadCVTab.vue'
import CreateCVTab from './CreateCVTab.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  job: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'submit', 'saveCV'])

// Estado interno del modal que sincroniza con el prop
const internalOpen = ref(false)
const allowClose = ref(false)

// Detectar si es dispositivo móvil
const isMobile = ref(window.innerWidth <= 768)

const updateIsMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  window.addEventListener('resize', updateIsMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateIsMobile)
})

// Tab inicial depende del tipo de aplicación
const getInitialTab = () => {
  if (props.job?.applicationType === 'internal') {
    return 'create' // Para trabajos internos, abrir tab "Crear CV"
  }
  return 'upload' // Para trabajos externos, abrir tab "Subir CV"
}

const activeTab = ref(getInitialTab())
const uploadedFile = ref(null)
const coverLetter = ref('')
const isSavingCV = ref(false)
const savedCVs = ref([])
const selectedSavedCV = ref(null)
const isLoadingCVs = ref(false)
const cvData = ref({
  personalInfo: {
    fullName: '',
    phone: '',
    email: '',
    location: '',
    linkedin: '',
    portfolio: ''
  },
  professionalProfile: '',
  education: [],
  experience: [],
  technicalSkills: [],
  softSkills: [],
  certifications: [],
  languages: [],
  projects: []
})

/**
 * Cargar CVs guardados del usuario desde el backend
 */
const loadSavedCVs = async () => {
  isLoadingCVs.value = true
  try {
    const response = await fetch('/api/cvs/list/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      savedCVs.value = data.cvs || []
    }
  } catch (error) {
    // Silenciar error 404 hasta que se implemente el backend
    console.log('Backend de CVs no disponible aún')
    savedCVs.value = []
  } finally {
    isLoadingCVs.value = false
  }
}

/**
 * Seleccionar un CV guardado
 */
const selectCV = (cv) => {
  selectedSavedCV.value = cv
}

/**
 * Formatear fecha para mostrar
 */
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Hoy'
  if (diffDays === 1) return 'Ayer'
  if (diffDays < 7) return `Hace ${diffDays} días`

  return date.toLocaleDateString('es-BO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Sincronizar internalOpen con el prop externo
watch(() => props.modelValue, (newValue) => {
  console.log('👁️ [MODAL WATCH] props.modelValue cambió a:', newValue)
  console.log('📱 [MODAL] isMobile:', isMobile.value)
  console.log('🪟 [MODAL] Window size:', window.innerWidth, 'x', window.innerHeight)

  internalOpen.value = newValue

  if (newValue) {
    console.log('✅ [MODAL] Modal abierto, cargando CVs...')
    allowClose.value = false // Bloquear cierre automático

    // Resetear al tab correcto según el tipo de aplicación
    activeTab.value = getInitialTab()

    loadSavedCVs()
  } else {
    console.log('❌ [MODAL] Modal cerrado')
  }
})

// Sincronizar internalOpen de vuelta al padre
watch(internalOpen, (newValue) => {
  console.log('🔄 [MODAL] internalOpen cambió a:', newValue)

  // Si intenta cerrarse pero no está permitido, reabrir
  if (!newValue && !allowClose.value && props.modelValue) {
    console.log('⚠️ [MODAL] Cierre automático bloqueado, reabriendo...')
    // Usar nextTick para evitar loop
    setTimeout(() => {
      internalOpen.value = true
    }, 0)
    return
  }

  // Emitir el cambio al padre
  console.log('📤 [MODAL] Emitiendo update:modelValue al padre:', newValue)
  emit('update:modelValue', newValue)

  // Resetear datos cuando se cierra legítimamente
  if (!newValue) {
    console.log('🧹 [MODAL] Reseteando datos del modal')
    resetModalData()
  }
})

// Resetear todos los datos del modal
const resetModalData = () => {
  activeTab.value = savedCVs.value.length > 0 ? 'saved' : 'upload'
  uploadedFile.value = null
  coverLetter.value = ''
  selectedSavedCV.value = null
  cvData.value = {
    personalInfo: {
      fullName: '',
      phone: '',
      email: '',
      location: '',
      linkedin: '',
      portfolio: ''
    },
    professionalProfile: '',
    education: [],
    experience: [],
    technicalSkills: [],
    softSkills: [],
    certifications: [],
    languages: [],
    projects: []
  }
}

const hasSavedCVs = computed(() => savedCVs.value.length > 0)

const canSubmit = computed(() => {
  if (activeTab.value === 'saved') {
    return selectedSavedCV.value !== null
  } else if (activeTab.value === 'upload') {
    return uploadedFile.value !== null
  } else {
    return cvData.value.personalInfo.fullName &&
           cvData.value.personalInfo.email &&
           cvData.value.personalInfo.phone
  }
})

const handleClose = () => {
  console.log('🚪 [MODAL] handleClose - Usuario cerró el modal')
  allowClose.value = true // Permitir cierre
  internalOpen.value = false
}

const handleOverlayClick = () => {
  // No hacer nada - bloqueamos el cierre al hacer click fuera
  console.log('🚫 [MODAL] Click en overlay bloqueado')
}

const handleSubmit = () => {
  /**
   * Estructura de datos emitida al backend:
   *
   * Si type === 'saved':
   * {
   *   jobId: Number,
   *   type: 'saved',
   *   savedCVId: Number,            // ID del CV guardado
   *   uploadedFile: null,
   *   coverLetter: null,
   *   cvData: null
   * }
   *
   * Si type === 'upload':
   * {
   *   jobId: Number,
   *   type: 'upload',
   *   uploadedFile: File,           // Archivo PDF/DOC/DOCX
   *   coverLetter: String | null,   // Carta de presentación (opcional)
   *   cvData: null,
   *   savedCVId: null
   * }
   *
   * Si type === 'create':
   * {
   *   jobId: Number,
   *   type: 'create',
   *   uploadedFile: null,
   *   coverLetter: null,
   *   cvData: {
   *     personalInfo: { fullName, phone, email, location, linkedin, portfolio },
   *     professionalProfile: String,
   *     education: Array,
   *     experience: Array,
   *     technicalSkills: Array,
   *     softSkills: Array,
   *     certifications: Array,
   *     languages: Array,
   *     projects: Array
   *   },
   *   savedCVId: null
   * }
   */
  const applicationData = {
    jobId: props.job.id,
    type: activeTab.value,
    savedCVId: activeTab.value === 'saved' ? selectedSavedCV.value?.id : null,
    uploadedFile: activeTab.value === 'upload' ? uploadedFile.value : null,
    coverLetter: activeTab.value === 'upload' ? coverLetter.value : null,
    cvData: activeTab.value === 'create' ? cvData.value : null
  }

  emit('submit', applicationData)
  handleClose()
}

/**
 * Guardar CV en el dashboard del usuario (sin postular)
 * El usuario postulante puede tener hasta 2 CVs guardados
 */
const handleSaveCV = async () => {
  isSavingCV.value = true
  emit('saveCV', {
    cvData: cvData.value
  })
  // Recargar la lista después de guardar (con delay para dar tiempo al backend)
  setTimeout(() => {
    loadSavedCVs()
    isSavingCV.value = false
  }, 1000)
}
</script>

<style scoped>
/* ===== CUSTOM MODAL OVERLAY ===== */
.custom-modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  background: rgba(0, 0, 0, 0.5) !important;
  z-index: 999999 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  overflow: auto !important;
}

.custom-modal-container {
  background: white;
  border-radius: 12px;
  max-width: 900px;
  width: calc(100% - 2rem);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  margin: 1rem;
}

.custom-modal-container.is-mobile {
  max-width: 100vw !important;
  width: 100vw !important;
  height: 100vh !important;
  max-height: 100vh !important;
  border-radius: 0 !important;
  margin: 0 !important;
}

.custom-modal-dialog {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* Transiciones */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-header-content {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 0.5rem 0;
}

.job-header-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.company-logo-mini {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #E5E7EB;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.company-logo-mini img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 0.25rem;
}

.company-logo-placeholder-mini {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9CA3AF;
}

.job-info-text {
  flex: 1;
  min-width: 0;
}

.job-title-modal {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  line-height: 1.3;
}

.company-name-modal {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  color: #6B7280;
  font-weight: 500;
}

.tabs-header {
  display: flex;
  gap: 0.5rem;
  border-bottom: 2px solid #E5E7EB;
  margin: 0 -1.5rem;
  padding: 0 1.5rem;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: #7C3AED;
  background: #F9FAFB;
}

.tab-btn.active {
  color: #7C3AED;
  border-bottom-color: #7C3AED;
}

.close-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: white;
  border: 1px solid #E5E7EB;
  padding: 0.625rem;
  cursor: pointer;
  color: #6B7280;
  transition: all 0.2s;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.close-btn:hover {
  background: #FEE2E2;
  color: #DC2626;
  border-color: #FCA5A5;
  box-shadow: 0 4px 8px rgba(220, 38, 38, 0.15);
  transform: scale(1.05);
}

.close-btn:active {
  transform: scale(0.95);
}

.modal-body {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 200px;
  -webkit-overflow-scrolling: touch;
}

.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: #F3F4F6;
}

.modal-body::-webkit-scrollbar-thumb {
  background: #D1D5DB;
  border-radius: 3px;
}

/* Asegurar que el modal sea visible */
:deep(.va-modal) {
  z-index: 99999 !important;
}

:deep(.va-modal__overlay) {
  z-index: 99998 !important;
  background: rgba(0, 0, 0, 0.5) !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
}

:deep(.va-modal__container) {
  max-width: 90vw;
  z-index: 100000 !important;
  position: fixed !important;
}

:deep(.va-modal__dialog) {
  margin: 1rem;
  z-index: 100001 !important;
}

.modal-footer-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid #E5E7EB;
  flex-shrink: 0;
}

/* Tab: Mis CVs Guardados */
.cv-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.25rem;
  height: 1.25rem;
  padding: 0 0.375rem;
  background: #7C3AED;
  color: white;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 700;
  line-height: 1;
}

.tab-btn.active .cv-count {
  background: white;
  color: #7C3AED;
}

.saved-cvs-container {
  padding: 0.5rem 0;
}

.tab-intro {
  margin: 0 0 1.5rem;
  font-size: 0.9375rem;
  color: #6B7280;
  text-align: center;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.loading-state p,
.empty-state p {
  margin: 1rem 0 0;
  font-size: 0.9375rem;
  color: #6B7280;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.cvs-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.cv-card {
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  padding: 1rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.cv-card:hover {
  border-color: #D1D5DB;
  background: #F9FAFB;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.cv-card.selected {
  border-color: #7C3AED;
  background: #F5F3FF;
  box-shadow: 0 2px 12px rgba(124, 58, 237, 0.15);
}

.cv-card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cv-card-info {
  flex: 1;
  min-width: 0;
}

.cv-card-info h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cv-meta {
  margin: 0.25rem 0 0;
  font-size: 0.8125rem;
  color: #9CA3AF;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.btn-save-cv {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  /* Asegurar que el modal sea fullscreen en mobile */
  :deep(.va-modal) {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 99999 !important;
  }

  :deep(.va-modal__overlay) {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 99998 !important;
  }

  :deep(.va-modal__container) {
    max-width: 100vw !important;
    width: 100vw !important;
    height: 100vh !important;
    margin: 0 !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    z-index: 100000 !important;
  }

  :deep(.va-modal__dialog) {
    max-height: 100vh !important;
    height: 100vh !important;
    margin: 0 !important;
    border-radius: 0 !important;
    max-width: 100vw !important;
    width: 100vw !important;
    z-index: 100001 !important;
  }

  :deep(.va-modal__inner) {
    max-height: 100vh !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
  }

  .modal-header-content {
    padding: 1rem;
    gap: 1rem;
  }

  .job-header-info {
    gap: 0.75rem;
  }

  .company-logo-mini,
  .company-logo-placeholder-mini {
    width: 40px;
    height: 40px;
  }

  .job-title-modal {
    font-size: 1.125rem;
  }

  .company-name-modal {
    font-size: 0.8125rem;
  }

  .tabs-header {
    margin: 0 -1rem;
    padding: 0 1rem;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .tabs-header::-webkit-scrollbar {
    display: none;
  }

  .tab-btn {
    flex: 0 0 auto;
    min-width: fit-content;
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
    white-space: nowrap;
  }

  .cv-count {
    min-width: 1.125rem;
    height: 1.125rem;
    font-size: 0.6875rem;
  }

  .close-btn {
    top: 1rem;
    right: 1rem;
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(8px);
    z-index: 10;
  }

  .custom-modal-container.is-mobile .custom-modal-dialog {
    height: 100vh;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .custom-modal-container.is-mobile .modal-header-content {
    flex-shrink: 0;
    overflow: visible;
  }

  .custom-modal-container.is-mobile .modal-body {
    flex: 1 1 auto;
    min-height: 0;
    max-height: 100%;
    overflow-y: auto !important;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
    overscroll-behavior: contain;
    padding: 1rem;
    position: relative;
  }

  .custom-modal-container.is-mobile .modal-footer-actions {
    flex-shrink: 0;
    overflow: visible;
  }

  .tab-intro {
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }

  .cv-card {
    padding: 0.875rem;
  }

  .cv-card-info h4 {
    font-size: 0.9375rem;
  }

  .cv-meta {
    font-size: 0.75rem;
  }

  .modal-footer-actions {
    flex-direction: column;
    padding: 1rem;
    gap: 0.75rem;
    background: #F9FAFB;
    border-top: 1px solid #E5E7EB;
  }

  .modal-footer-actions button {
    width: 100%;
    justify-content: center;
    padding: 1rem 1.5rem;
    font-size: 1rem;
    font-weight: 600;
  }

  .btn-save-cv,
  .btn-submit,
  .btn-cancel {
    width: 100%;
  }
}

/* Botones personalizados HTML puro */
.modal-footer-actions button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  outline: none;
}

.btn-cancel {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: white;
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.25);
}

.btn-cancel:hover {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  box-shadow: 0 6px 18px rgba(251, 191, 36, 0.35);
  transform: translateY(-2px);
}

.btn-cancel:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(251, 191, 36, 0.25);
}

/* Botones con degradado morado */
.btn-gradient-purple {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35);
}

.btn-gradient-purple:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 6px 18px rgba(124, 58, 237, 0.45);
  transform: translateY(-2px);
}

.btn-gradient-purple:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.35);
}

.btn-gradient-purple:disabled {
  background: linear-gradient(135deg, #D1D5DB, #9CA3AF);
  box-shadow: none;
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
