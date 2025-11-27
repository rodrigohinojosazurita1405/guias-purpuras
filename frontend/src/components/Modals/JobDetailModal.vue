<!-- frontend/src/components/Modals/JobDetailModal.vue -->
<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-content job-detail-modal">
      <!-- Header -->
      <div class="modal-header">
        <h2>{{ job.title }}</h2>
        <button class="close-btn" @click="close">
          <va-icon name="close" />
        </button>
      </div>

      <!-- Body -->
      <div class="modal-body">
        <!-- Company Info -->
        <div class="info-section">
          <h3>Información de la Empresa</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Empresa:</span>
              <span class="value">{{ job.companyName }}</span>
            </div>
            <div class="info-item">
              <span class="label">Ciudad:</span>
              <span class="value">{{ job.city }}</span>
            </div>
            <div class="info-item">
              <span class="label">Tipo de Contrato:</span>
              <span class="value">{{ job.contractType || 'No especificado' }}</span>
            </div>
            <div class="info-item">
              <span class="label">Modalidad:</span>
              <span class="value">{{ job.modality || 'No especificado' }}</span>
            </div>
          </div>
        </div>

        <!-- Job Details -->
        <div class="info-section">
          <h3>Detalles del Puesto</h3>
          <div class="info-grid">
            <div class="info-item full-width">
              <span class="label">Descripción:</span>
              <p class="value description">{{ job.description || 'Sin descripción' }}</p>
            </div>
            <div class="info-item">
              <span class="label">Salario:</span>
              <span class="value">{{ job.salary || 'No declarado' }}</span>
            </div>
            <div class="info-item">
              <span class="label">Categoría:</span>
              <span class="value">{{ job.jobCategory || 'No especificado' }}</span>
            </div>
          </div>
        </div>

        <!-- Requirements & Details -->
        <div class="info-section" v-if="job.requirements || job.experience || job.education || job.languages || job.technicalSkills">
          <h3>Requisitos y Habilidades</h3>
          <div class="info-grid">
            <div class="info-item full-width" v-if="job.requirements">
              <span class="label">Requisitos:</span>
              <p class="value description">{{ job.requirements }}</p>
            </div>
            <div class="info-item full-width" v-if="job.experience">
              <span class="label">Experiencia:</span>
              <p class="value description">{{ job.experience }}</p>
            </div>
            <div class="info-item" v-if="job.education">
              <span class="label">Formación:</span>
              <span class="value">{{ job.education }}</span>
            </div>
            <div class="info-item" v-if="job.languages">
              <span class="label">Idiomas:</span>
              <span class="value">{{ job.languages }}</span>
            </div>
            <div class="info-item full-width" v-if="job.technicalSkills">
              <span class="label">Habilidades Técnicas:</span>
              <p class="value description">{{ job.technicalSkills }}</p>
            </div>
            <div class="info-item full-width" v-if="job.softSkills">
              <span class="label">Habilidades Blandas:</span>
              <p class="value description">{{ job.softSkills }}</p>
            </div>
          </div>
        </div>

        <!-- Benefits & Contact -->
        <div class="info-section" v-if="job.benefits || job.whatsapp || job.website">
          <h3>Beneficios y Contacto</h3>
          <div class="info-grid">
            <div class="info-item full-width" v-if="job.benefits">
              <span class="label">Beneficios:</span>
              <p class="value description">{{ job.benefits }}</p>
            </div>
            <div class="info-item" v-if="job.whatsapp">
              <span class="label">WhatsApp:</span>
              <span class="value">{{ job.whatsapp }}</span>
            </div>
            <div class="info-item" v-if="job.website">
              <span class="label">Sitio Web:</span>
              <span class="value"><a :href="job.website" target="_blank">{{ job.website }}</a></span>
            </div>
          </div>
        </div>

        <!-- Stats -->
        <div class="info-section">
          <h3>Estadísticas</h3>
          <div class="stats-grid">
            <div class="stat">
              <va-icon name="visibility" />
              <div>
                <span class="stat-value">{{ job.views || 0 }}</span>
                <span class="stat-label">Vistas</span>
              </div>
            </div>
            <div class="stat">
              <va-icon name="people" />
              <div>
                <span class="stat-value">{{ job.applications || 0 }}</span>
                <span class="stat-label">Aplicaciones</span>
              </div>
            </div>
            <div class="stat">
              <va-icon name="calendar_today" />
              <div>
                <span class="stat-value">{{ formatDate(job.createdAt) }}</span>
                <span class="stat-label">Publicado</span>
              </div>
            </div>
            <div class="stat">
              <va-icon name="info" />
              <div>
                <span class="stat-value">{{ job.status }}</span>
                <span class="stat-label">Estado</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="close">Cerrar Modal</button>
        <button
          v-if="job.status === 'active'"
          class="btn btn-danger"
          @click="$emit('deactivate-job')"
        >
          <va-icon name="visibility_off" />
          Desactivar Anuncio
        </button>
        <button
          v-else
          class="btn btn-success"
          @click="$emit('activate-job')"
        >
          <va-icon name="visibility" />
          Activar Anuncio
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue'

defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  job: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'deactivate-job', 'activate-job'])

const close = () => {
  emit('close')
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const today = new Date()
  const diff = today - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return 'Hoy'
  if (days === 1) return 'Ayer'
  if (days < 7) return `Hace ${days} días`
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  border-bottom: 1px solid #E5E7EB;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6B7280;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #1F2937;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.info-section {
  margin-bottom: 2rem;
}

.info-section h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1F2937;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #7C3AED;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-item .label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.info-item .value {
  font-size: 1rem;
  color: #1F2937;
  font-weight: 500;
}

.info-item .description {
  line-height: 1.6;
  color: #4B5563;
  font-weight: 400;
}

.info-item a {
  color: #7C3AED;
  text-decoration: none;
  word-break: break-all;
  transition: color 0.2s;
}

.info-item a:hover {
  color: #6D28D9;
  text-decoration: underline;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #F3F4F6;
  border-radius: 8px;
}

.stat svg {
  width: 24px;
  height: 24px;
  color: #7C3AED;
  flex-shrink: 0;
}

.stat-value {
  display: block;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1F2937;
}

.stat-label {
  display: block;
  font-size: 0.8rem;
  color: #6B7280;
  margin-top: 0.25rem;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 2rem;
  border-top: 1px solid #E5E7EB;
  justify-content: flex-end;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.btn-secondary {
  background: #E5E7EB;
  color: #374151;
}

.btn-secondary:hover {
  background: #D1D5DB;
}

.btn-danger {
  background: #EF4444;
  color: white;
}

.btn-danger:hover {
  background: #DC2626;
}

.btn-success {
  background: #10B981;
  color: white;
}

.btn-success:hover {
  background: #059669;
}

/* Responsive */
@media (max-width: 640px) {
  .modal-content {
    max-height: 100vh;
    border-radius: 0;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .modal-footer {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
