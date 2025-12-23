<template>
  <div class="cv-manager">
    <div class="section-header">
      <h1>Mis CVs</h1>
      <p class="subtitle">Gestiona tus currículum vitae (máximo 2 CVs)</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <va-progress-circle indeterminate color="purple" />
      <p>Cargando CVs...</p>
    </div>

    <!-- Content -->
    <div v-else class="cv-content">
      <!-- Action Buttons -->
      <div class="action-buttons">
        <va-button
          color="success"
          :disabled="cvs.length >= maxCVs"
          @click="showCreateModal = true"
        >
          <va-icon name="add" />
          Crear CV en Plataforma
        </va-button>
      </div>

      <!-- CVs Limit Warning -->
      <div v-if="cvs.length >= maxCVs" class="warning-message">
        <va-icon name="warning" color="warning" />
        <span>Has alcanzado el límite de {{ maxCVs }} CVs. Elimina uno para agregar otro.</span>
      </div>

      <!-- Empty State -->
      <div v-if="cvs.length === 0" class="empty-state">
        <va-icon name="description" size="4rem" color="#ccc" />
        <h3>No tienes CVs guardados</h3>
        <p>Sube un CV existente o crea uno nuevo en nuestra plataforma</p>
      </div>

      <!-- CVs List -->
      <div v-else class="cvs-grid">
        <div
          v-for="cv in cvs"
          :key="cv.id"
          class="cv-card"
        >
          <div class="cv-header">
            <div class="cv-type-badge">
              <va-badge
                :text="cv.cv_type === 'created' ? 'Creado' : 'Subido'"
                :color="cv.cv_type === 'created' ? 'success' : 'info'"
              />
            </div>
            <va-button
              icon="delete"
              preset="plain"
              color="danger"
              size="small"
              @click="deleteCV(cv)"
              title="Eliminar CV"
            />
          </div>

          <div class="cv-body">
            <va-icon
              :name="cv.cv_type === 'created' ? 'article' : 'upload_file'"
              size="3rem"
              color="purple"
            />
            <h3>{{ cv.name }}</h3>

            <div class="cv-meta">
              <div class="meta-item">
                <va-icon name="schedule" size="small" color="#666" />
                <span>Creado: {{ formatDate(cv.created_at) }}</span>
              </div>
              <div v-if="cv.updated_at !== cv.created_at" class="meta-item">
                <va-icon name="update" size="small" color="#666" />
                <span>Actualizado: {{ formatDate(cv.updated_at) }}</span>
              </div>
            </div>
          </div>

          <div class="cv-footer">
            <va-button
              v-if="cv.cv_type === 'uploaded'"
              size="small"
              @click="downloadCV(cv)"
            >
              <va-icon name="download" />
              Descargar
            </va-button>
            <va-button
              v-else
              size="small"
              @click="editCV(cv)"
            >
              <va-icon name="edit" />
              Editar
            </va-button>
            <va-button
              size="small"
              color="success"
              @click="previewCV(cv)"
            >
              <va-icon name="visibility" />
              Vista Previa
            </va-button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create CV Modal -->
    <va-modal
      v-model="showCreateModal"
      size="large"
      hide-default-actions
      :max-height="'90vh'"
      :overlay-opacity="0"
      mobile-fullscreen
    >
      <template #header>
        <h2 class="modal-title">Crear CV Profesional</h2>
      </template>

      <div class="create-cv-modal-content">
        <CreateCV v-model="cvFormData" />
      </div>

      <template #footer>
        <div class="modal-footer-buttons">
          <va-button
            color="danger"
            preset="secondary"
            @click="cancelCreateCV"
          >
            Cancelar
          </va-button>
          <va-button
            color="success"
            @click="saveCreatedCV"
            :disabled="!isValidCV"
          >
            <va-icon name="save" />
            Guardar CV
          </va-button>
        </div>
      </template>
    </va-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'
import CreateCV from '@/components/Process/CreateCV.vue'

const authStore = useAuthStore()
const { init: initToast } = useToast()

// Constants
const maxCVs = 2

// State
const cvs = ref([])
const isLoading = ref(false)
const showCreateModal = ref(false)
const cvFormData = ref({
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

// DEBUG: Verificar si cvFormData se actualiza
import { watch } from 'vue'
watch(() => cvFormData.value.personalInfo, (newVal) => {
  console.log('📝 PersonalInfo cambió:', newVal)
}, { deep: true })

// Computed
const isValidCV = computed(() => {
  const info = cvFormData.value?.personalInfo
  if (!info) return false

  return (
    info.fullName?.trim().length > 0 &&
    info.email?.trim().length > 0 &&
    info.phone?.trim().length > 0
  )
})

// Methods
const loadCVs = async () => {
  isLoading.value = true

  try {
    const response = await fetch('http://localhost:8000/api/cvs/list/', {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (!response.ok) {
      throw new Error('Error al cargar CVs')
    }

    const data = await response.json()
    cvs.value = data.cvs || []
  } catch (error) {
    console.error('Error loading CVs:', error)
    initToast({
      message: 'Error al cargar CVs',
      color: 'danger',
      duration: 3000
    })
  } finally {
    isLoading.value = false
  }
}

const saveCreatedCV = async () => {
  if (!isValidCV.value) {
    initToast({
      message: 'Por favor completa los campos obligatorios (Nombre, Email, Teléfono)',
      color: 'warning',
      duration: 3000
    })
    return
  }

  try {
    const cvName = `CV - ${cvFormData.value.personalInfo.fullName}`

    const response = await fetch('http://localhost:8000/api/cvs/save/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        cv_type: 'created',
        name: cvName,
        cv_data: cvFormData.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Error al guardar CV')
    }

    initToast({
      message: 'CV creado exitosamente',
      color: 'success',
      duration: 3000
    })

    showCreateModal.value = false
    resetCVForm()
    await loadCVs()
  } catch (error) {
    console.error('Error saving CV:', error)
    initToast({
      message: error.message,
      color: 'danger',
      duration: 3000
    })
  }
}

const cancelCreateCV = () => {
  if (confirm('¿Estás seguro? Se perderán todos los datos ingresados.')) {
    showCreateModal.value = false
    resetCVForm()
  }
}

const resetCVForm = () => {
  cvFormData.value = {
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

const deleteCV = async (cv) => {
  if (!confirm(`¿Estás seguro de que deseas eliminar "${cv.name}"?`)) {
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/api/cvs/${cv.id}/delete/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })

    if (!response.ok) {
      throw new Error('Error al eliminar CV')
    }

    initToast({
      message: 'CV eliminado exitosamente',
      color: 'success',
      duration: 3000
    })

    await loadCVs()
  } catch (error) {
    console.error('Error deleting CV:', error)
    initToast({
      message: 'Error al eliminar CV',
      color: 'danger',
      duration: 3000
    })
  }
}

const downloadCV = async (cv) => {
  if (!cv.file) {
    initToast({
      message: 'Este CV no tiene archivo para descargar',
      color: 'warning',
      duration: 3000
    })
    return
  }

  // Open file in new tab
  window.open(cv.file, '_blank')
}

const editCV = (cv) => {
  initToast({
    message: 'Editor de CV próximamente disponible',
    color: 'info',
    duration: 3000
  })
}

const previewCV = (cv) => {
  if (cv.cv_type === 'uploaded' && cv.file) {
    window.open(cv.file, '_blank')
  } else {
    initToast({
      message: 'Vista previa próximamente disponible',
      color: 'info',
      duration: 3000
    })
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-BO', { year: 'numeric', month: 'short', day: 'numeric' })
}

// Lifecycle
onMounted(() => {
  loadCVs()
})
</script>

<style scoped>
.cv-manager {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.section-header {
  margin-bottom: 30px;
}

.section-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
}

.subtitle {
  color: #666;
  margin: 0;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 20px;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.warning-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 8px;
  margin-bottom: 20px;
  color: #856404;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  gap: 15px;
}

.empty-state h3 {
  color: #666;
  margin: 0;
}

.empty-state p {
  color: #999;
  margin: 0;
}

.cvs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.cv-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  transition: all 0.3s ease;
}

.cv-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.cv-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cv-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  text-align: center;
}

.cv-body h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.cv-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #666;
}

.cv-footer {
  display: flex;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.modal-content {
  padding: 20px 0;
}

.info-box {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
  padding: 12px;
  background-color: #e3f2fd;
  border-radius: 6px;
  font-size: 13px;
  color: #1976d2;
}

.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.create-cv-modal-content {
  max-height: 70vh;
  overflow-y: auto;
  padding: 20px;
  background: #ffffff;
}

.modal-footer-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  width: 100%;
  padding: 15px 0;
}

/* FORZAR OVERLAY COMPLETAMENTE TRANSPARENTE - AGRESIVO */
:deep(.va-modal__overlay),
:deep(.va-backdrop),
:deep([class*="overlay"]),
:deep([class*="backdrop"]) {
  background: transparent !important;
  background-color: transparent !important;
  opacity: 0 !important;
  display: none !important;
}

:deep(.va-modal__container) {
  background: transparent !important;
  background-color: transparent !important;
}

:deep(.va-modal) {
  background: white !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2) !important;
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }

  .cvs-grid {
    grid-template-columns: 1fr;
  }
}
</style>
