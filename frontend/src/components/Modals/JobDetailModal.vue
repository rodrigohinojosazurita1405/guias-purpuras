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
        <!-- Company Header with Logo -->
        <div class="company-header">
          <!-- Solo mostrar logo si NO es anónimo -->
          <template v-if="!job.companyAnonymous">
            <img
              v-if="job.companyLogo"
              :src="job.companyLogo"
              :alt="job.companyName"
              class="company-logo"
            />
            <div v-else class="company-logo-placeholder">
              <va-icon name="business" />
            </div>
          </template>
          <!-- Si es anónimo, mostrar ícono de empresa genérico -->
          <div v-else class="company-logo-placeholder anonymous">
            <va-icon name="domain" />
          </div>
          <div class="company-info-header">
            <h2 class="company-name">{{ job.companyName }}</h2>
            <div v-if="job.city" class="company-location">
              <va-icon name="location_on" />
              <span>{{ job.city }}</span>
            </div>
          </div>
        </div>

        <!-- Payment Verification Status -->
        <div
          v-if="job.paymentVerified && job.status === 'active'"
          class="payment-alert success"
        >
          <va-icon name="check_circle" />
          <div class="alert-content">
            <strong>Pago Verificado y Activo</strong>
            <p>Este anuncio está visible públicamente en el sitio.</p>
          </div>
        </div>

        <div
          v-else-if="job.paymentVerified && job.status !== 'active'"
          class="payment-alert info"
        >
          <va-icon name="visibility_off" />
          <div class="alert-content">
            <strong>Pago Verificado - Anuncio Inactivo</strong>
            <p>El pago fue verificado, pero el anuncio está desactivado. Puedes activarlo desde el panel de gestión.</p>
          </div>
        </div>

        <div
          v-else
          class="payment-alert warning"
        >
          <va-icon name="info" />
          <div class="alert-content">
            <strong>Pendiente de Verificación</strong>
            <p>Este anuncio no está visible públicamente hasta que se verifique el pago. El administrador debe aprobar el comprobante de pago para que se publique.</p>
          </div>
        </div>

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
              <span class="label">Salario:</span>
              <span class="value">{{ job.salary || 'No declarado' }}</span>
            </div>
            <div class="info-item">
              <span class="label">Categoría:</span>
              <span class="value">{{ job.jobCategory || 'No especificado' }}</span>
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
              <p class="value description">{{ stripHTML(job.description) || 'Sin descripción' }}</p>
            </div>
            <div class="info-item">
              <span class="label">Tipo de Aplicación:</span>
              <span class="value">
                <template v-if="job.applicationType === 'internal'">
                  Interna (en Guías Púrpuras)
                </template>
                <template v-else-if="job.applicationType === 'external'">
                  Externa
                </template>
                <template v-else-if="job.applicationType === 'both'">
                  Ambas
                </template>
                <template v-else>
                  No especificado
                </template>
              </span>
            </div>
            <div v-if="['external', 'both'].includes(job.applicationType)" class="info-item full-width">
              <span class="label">URL Externa de Aplicación:</span>
              <span class="value"><a :href="job.externalApplicationUrl" target="_blank" rel="noopener noreferrer">{{ job.externalApplicationUrl }}</a></span>
            </div>
            <div v-if="['internal', 'both'].includes(job.applicationType)" class="info-item full-width">
              <span class="label">Preguntas de Filtrado:</span>
              <div class="value">
                <template v-if="getScreeningQuestions(job.screeningQuestions).length > 0">
                  <ul class="screening-questions">
                    <li v-for="(question, index) in getScreeningQuestions(job.screeningQuestions)" :key="index">{{ question }}</li>
                  </ul>
                </template>
                <span v-else class="no-data">No se realizaron preguntas de filtrado para este anuncio</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Requirements & Details -->
        <div class="info-section" v-if="job.requirements || job.experience || job.education || job.languages || job.technicalSkills">
          <h3>Requisitos y Habilidades</h3>
          <div class="info-grid">
            <div class="info-item full-width" v-if="job.requirements">
              <span class="label">Requisitos:</span>
              <p class="value description">{{ stripHTML(job.requirements) }}</p>
            </div>
            <div class="info-item full-width" v-if="job.experience">
              <span class="label">Experiencia:</span>
              <p class="value description">{{ stripHTML(job.experience) }}</p>
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
              <p class="value description">{{ stripHTML(job.technicalSkills) }}</p>
            </div>
            <div class="info-item full-width" v-if="job.softSkills">
              <span class="label">Habilidades Blandas:</span>
              <p class="value description">{{ stripHTML(job.softSkills) }}</p>
            </div>
          </div>
        </div>

        <!-- Benefits & Contact -->
        <div class="info-section" v-if="job.benefits || job.whatsapp || job.website">
          <h3>Beneficios y Contacto</h3>
          <div class="info-grid">
            <div class="info-item full-width" v-if="job.benefits">
              <span class="label">Beneficios:</span>
              <p class="value description">{{ stripHTML(job.benefits) }}</p>
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
      </div>

      <!-- Footer -->
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="close">Cerrar</button>
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

const formatExactDateTime = (dateString) => {
  if (!dateString) return 'N/A'

  // Crear fecha en UTC y ajustar a Bolivia (UTC-4)
  const date = new Date(dateString)
  const boliviaOffset = -4 * 60 // Bolivia es UTC-4
  const localOffset = date.getTimezoneOffset() // Offset del navegador en minutos
  const totalOffset = boliviaOffset - localOffset

  // Crear nueva fecha ajustada
  const boliviaDate = new Date(date.getTime() + totalOffset * 60 * 1000)

  const day = String(boliviaDate.getDate()).padStart(2, '0')
  const month = String(boliviaDate.getMonth() + 1).padStart(2, '0')
  const year = boliviaDate.getFullYear()
  const hours = String(boliviaDate.getHours()).padStart(2, '0')
  const minutes = String(boliviaDate.getMinutes()).padStart(2, '0')
  const seconds = String(boliviaDate.getSeconds()).padStart(2, '0')

  return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`
}

const stripHTML = (html) => {
  if (!html) return ''
  // Crear un elemento temporal para extraer solo el texto
  const tmp = document.createElement('DIV')
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ''
}

const getScreeningQuestions = (questions) => {
  if (!questions) return []

  // Si ya es un array de objetos con propiedad 'text'
  if (Array.isArray(questions)) {
    const result = questions
      .map(q => {
        // Si es un objeto con propiedad text, extraerla
        if (typeof q === 'object' && q.text) {
          return q.text
        }
        // Si es un string simple, devolverlo
        if (typeof q === 'string' && q.trim()) {
          return q.trim()
        }
        return null
      })
      .filter(q => q)
    return result
  }

  // Si es un string, intentar parsearlo como JSON
  if (typeof questions === 'string') {
    try {
      const parsed = JSON.parse(questions)
      if (Array.isArray(parsed)) {
        return parsed
          .map(q => {
            if (typeof q === 'object' && q.text) {
              return q.text
            }
            if (typeof q === 'string' && q.trim()) {
              return q.trim()
            }
            return null
          })
          .filter(q => q)
      }
    } catch (e) {
      // Si falla el parse, intentar extraer preguntas con regex
      // Buscar patrones como "text":"..."
      const textMatches = questions.matchAll(/"text"\s*:\s*"([^"]+)"/g)
      const extractedQuestions = Array.from(textMatches).map(match => match[1])
      if (extractedQuestions.length > 0) {
        return extractedQuestions
      }
    }
  }

  return []
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

/* ========== PAYMENT ALERT ========== */
.payment-alert {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border-left: 4px solid;
  align-items: flex-start;
}

.payment-alert.warning {
  background-color: #fffbeb;
  border-color: #f59e0b;
  color: #78350f;
}

.payment-alert.warning i {
  color: #f59e0b;
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.payment-alert.success {
  background-color: #ecfdf5;
  border-color: #10b981;
  color: #065f46;
}

.payment-alert.success i {
  color: #10b981;
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.payment-alert.info {
  background-color: #eff6ff;
  border-color: #3b82f6;
  color: #1e3a8a;
}

.payment-alert.info i {
  color: #3b82f6;
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.payment-alert .alert-content {
  flex: 1;
}

.payment-alert strong {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 700;
  font-size: 1rem;
}

.payment-alert p {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.5;
}

.company-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #F9FAFB;
  border-radius: 12px;
  color: #1F2937;
  border: 1px solid #E5E7EB;
}

.company-logo {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  object-fit: contain;
  background: white;
  padding: 4px;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  flex-shrink: 0;
}

.company-logo-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid white;
  font-size: 2.5rem;
  flex-shrink: 0;
}

.company-logo-placeholder.anonymous {
  background: #f3f4f6;
  border-color: #9ca3af;
  color: #6b7280;
}

.company-info-header {
  flex: 1;
}

.company-name {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
  line-height: 1.3;
}

.company-location {
  margin: 0.5rem 0 0 0;
  font-size: 0.95rem;
  color: #6B7280;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.company-location svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
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
  color: #A78BFA;
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
  color: #A78BFA;
  text-decoration: none;
  word-break: break-all;
  transition: color 0.2s;
}

.info-item a:hover {
  color: #9F7AEA;
  text-decoration: underline;
}

.screening-questions {
  margin: 0;
  padding-left: 1.5rem;
  list-style: decimal;
}

.screening-questions li {
  color: #4B5563;
  line-height: 1.6;
  margin-bottom: 0.5rem;
  font-weight: 400;
}

.no-data {
  color: #9CA3AF;
  font-style: italic;
  font-size: 0.95rem;
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
  background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
  color: #ffffff;
}

.btn-secondary:hover {
   background: linear-gradient(135deg, #7c3aed 0%);
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
