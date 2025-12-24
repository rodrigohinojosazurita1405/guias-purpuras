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
        <button
          class="create-cv-btn"
          :disabled="cvs.length >= maxCVs"
          @click="goToCreateCV"
        >
          <va-icon name="add_circle" size="20px" />
          Crear CV en Plataforma
        </button>
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
          </div>

          <div class="cv-body">
            <div class="cv-icon-container">
              <va-icon
                :name="cv.cv_type === 'created' ? 'article' : 'upload_file'"
                size="3.5rem"
                :color="cv.cv_type === 'created' ? '#7C3AED' : '#3B82F6'"
              />
            </div>
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
            <button
              v-if="cv.cv_type === 'uploaded'"
              class="cv-action-btn download-btn"
              @click="downloadCV(cv)"
            >
              <va-icon name="download" size="16px" />
              Descargar
            </button>
            <button
              v-else
              class="cv-action-btn edit-btn"
              @click="editCV(cv)"
            >
              <va-icon name="edit" size="16px" />
              Editar
            </button>
            <button
              class="cv-action-btn preview-btn"
              @click="previewCV(cv)"
            >
              <va-icon name="visibility" size="16px" />
              Vista Previa
            </button>
            <button
              class="cv-action-btn delete-btn"
              @click="deleteCV(cv)"
            >
              <va-icon name="delete" size="16px" />
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { useToast } from 'vuestic-ui'

const router = useRouter()
const authStore = useAuthStore()
const { init: initToast } = useToast()

// Constants
const maxCVs = 2

// State
const cvs = ref([])
const isLoading = ref(false)

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

const goToCreateCV = () => {
  router.push('/dashboard/cv/builder')
}

const editCV = (cv) => {
  router.push({
    path: '/dashboard/cv/builder',
    query: { edit: cv.id }
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
  margin-bottom: 24px;
}

.create-cv-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  border: none;
  color: white;
  font-weight: 600;
  font-size: 15px;
  padding: 14px 28px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
}

.create-cv-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
}

.create-cv-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cv-icon-container {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.cv-card:hover .cv-icon-container {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.15);
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
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.cv-card:hover {
  border-color: #7C3AED;
  box-shadow: 0 12px 24px rgba(124, 58, 237, 0.15);
  transform: translateY(-4px);
}

.cv-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.cv-type-badge {
  flex: 1;
}

.cv-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  text-align: center;
  padding: 12px 0;
}

.cv-body h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  line-height: 1.3;
}

.cv-meta {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  background: #f3f4f6;
  padding: 12px 16px;
  border-radius: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.cv-footer {
  display: flex;
  gap: 8px;
  padding-top: 16px;
  border-top: 2px solid #e5e7eb;
}

.cv-action-btn {
  flex: 1;
  font-weight: 600;
  font-size: 13px;
  padding: 10px 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.edit-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
}

.edit-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35);
}

.preview-btn {
  background: linear-gradient(135deg, #10b981, #059669);
}

.preview-btn:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
}

.download-btn {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.download-btn:hover {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.35);
}

.delete-btn {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.delete-btn:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35);
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
