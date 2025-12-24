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
            <div class="cv-badges">
              <va-badge
                v-if="isNewCV(cv)"
                text="NUEVO"
                color="#7C3AED"
              />
              <va-badge
                v-else-if="isRecentlyUpdated(cv)"
                text="ACTUALIZADO"
                color="#10B981"
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

            <!-- Editable CV Name -->
            <div class="cv-name-wrapper">
              <h3
                v-if="editingCVId !== cv.id"
                class="cv-name"
                @click="startEditingName(cv)"
                :title="'Click para editar nombre'"
              >
                {{ cv.name }}
                <va-icon name="edit" size="14px" class="edit-icon" />
              </h3>
              <div v-else class="cv-name-edit">
                <input
                  v-model="editingName"
                  @blur="saveName(cv)"
                  @keyup.enter="saveName(cv)"
                  @keyup.esc="cancelEdit"
                  class="cv-name-input"
                  ref="nameInput"
                  :placeholder="cv.name"
                  autofocus
                />
                <div class="edit-actions">
                  <button @click="saveName(cv)" class="save-name-btn" title="Guardar">
                    <va-icon name="check" size="14px" />
                  </button>
                  <button @click="cancelEdit" class="cancel-name-btn" title="Cancelar">
                    <va-icon name="close" size="14px" />
                  </button>
                </div>
              </div>
            </div>

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
const editingCVId = ref(null)
const editingName = ref('')

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

// Badge helper functions
const isNewCV = (cv) => {
  const createdDate = new Date(cv.created_at)
  const now = new Date()
  const hoursDiff = (now - createdDate) / (1000 * 60 * 60)

  // Mostrar badge "NUEVO" si fue creado hace menos de 48 horas
  return hoursDiff < 48
}

const isRecentlyUpdated = (cv) => {
  // Solo mostrar si la fecha de actualización es diferente a la de creación
  if (cv.updated_at === cv.created_at) return false

  const updatedDate = new Date(cv.updated_at)
  const now = new Date()
  const hoursDiff = (now - updatedDate) / (1000 * 60 * 60)

  // Mostrar badge "ACTUALIZADO" si fue modificado hace menos de 24 horas
  return hoursDiff < 24
}

// Name editing functions
const startEditingName = (cv) => {
  editingCVId.value = cv.id
  editingName.value = cv.name
}

const cancelEdit = () => {
  editingCVId.value = null
  editingName.value = ''
}

const saveName = async (cv) => {
  const newName = editingName.value.trim()

  if (!newName) {
    initToast({
      message: 'El nombre no puede estar vacío',
      color: 'warning',
      duration: 3000
    })
    return
  }

  if (newName === cv.name) {
    cancelEdit()
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/api/cvs/${cv.id}/update/`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: newName
      })
    })

    if (!response.ok) {
      throw new Error('Error al actualizar nombre del CV')
    }

    initToast({
      message: 'Nombre actualizado exitosamente',
      color: 'success',
      duration: 3000
    })

    // Actualizar el nombre localmente
    cv.name = newName
    cancelEdit()
  } catch (error) {
    console.error('Error updating CV name:', error)
    initToast({
      message: 'Error al actualizar nombre del CV',
      color: 'danger',
      duration: 3000
    })
  }
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
  justify-content: flex-end;
  align-items: flex-start;
  min-height: 32px;
}

.cv-badges {
  display: flex;
  gap: 8px;
}

.cv-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  text-align: center;
  padding: 12px 0;
}

.cv-name-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cv-name {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  line-height: 1.3;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.cv-name:hover {
  background: #f3f4f6;
  color: #7c3aed;
}

.cv-name .edit-icon {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.cv-name:hover .edit-icon {
  opacity: 0.6;
}

.cv-name-edit {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.cv-name-input {
  width: 100%;
  max-width: 300px;
  padding: 8px 12px;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  border: 2px solid #7c3aed;
  border-radius: 8px;
  outline: none;
  text-align: center;
  background: white;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
  transition: all 0.2s ease;
}

.cv-name-input:focus {
  border-color: #6d28d9;
  box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.15);
}

.edit-actions {
  display: flex;
  gap: 8px;
}

.save-name-btn,
.cancel-name-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-name-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.save-name-btn:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3);
}

.cancel-name-btn {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.cancel-name-btn:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.3);
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
