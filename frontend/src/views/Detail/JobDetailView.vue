<!-- frontend/src/views/Detail/JobDetailView.vue -->
<template>
  <MainLayout>
    <section class="job-detail-section">
      <div class="container">
        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <va-progress-bar indeterminate color="purple" size="large" />
          <p>Cargando detalles del empleo...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <va-icon name="error" size="4rem" color="danger" />
          <h2>Error al cargar el empleo</h2>
          <p>{{ error }}</p>
          <va-button @click="$router.back()" color="purple" class="btn-back">Volver</va-button>
        </div>

        <!-- Content -->
        <div v-else>
          <!-- Breadcrumb -->
          <nav class="breadcrumb">
            <router-link to="/">Inicio</router-link>
            <span class="separator">/</span>
            <router-link to="/guias/trabajos">Trabajos</router-link>
            <span class="separator">/</span>
            <span class="current">{{ job.title }}</span>
          </nav>

        <!-- Header Card -->
        <div class="job-header">
          <!-- Logo de la Empresa -->
          <div class="job-logo">
            <img 
              v-if="!job.confidential && job.companyLogo" 
              :src="job.companyLogo" 
              :alt="job.companyName"
            />
            <div v-else class="placeholder-logo">
              <va-icon 
                :name="job.confidential ? 'visibility_off' : 'business'" 
                size="5rem" 
                color="#999" 
              />
            </div>

            <!-- Badge Verificado -->
            <div v-if="job.verified && !job.confidential" class="badge-verified">
              <va-icon name="verified" size="small" />
              Empresa Verificada
            </div>
          </div>

          <!-- Información Principal -->
          <div class="job-info">
            <div class="badges-row">
              <div v-if="job.plan === 'destacado'" class="badge-plan destacado">
                <va-icon name="star" size="small" />
                Oferta Destacada
              </div>
              <div v-if="job.plan === 'premium'" class="badge-plan premium">
                <va-icon name="star" size="small" />
                Oferta Premium
              </div>
              <div v-if="job.urgent" class="badge-urgent">
                <va-icon name="error" size="small" />
                Urgente
              </div>
            </div>

            <h1 class="job-title">{{ job.title }}</h1>
            
            <p class="company-name">
              <va-icon 
                v-if="job.verified && !job.confidential" 
                name="verified" 
                size="small" 
                color="success" 
              />
              {{ getCompanyDisplayName }}
            </p>

            <!-- Info Grid -->
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Empresa:</span>
                <span class="info-value">{{ getCompanyDisplayName }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Contrato:</span>
                <span class="info-value">{{ job.contractType }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Ciudad:</span>
                <span class="info-value">{{ job.city }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Publicado:</span>
                <span class="info-value">{{ job.publishDate }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Vencimiento:</span>
                <span class="info-value">{{ job.expiryDate }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Categoría:</span>
                <span class="info-value">{{ job.jobCategory }}</span>
              </div>
            </div>

            <!-- Etiquetas -->
            <div v-if="job.tags && job.tags.length > 0" class="tags-row">
              <span class="tags-label">Etiquetas:</span>
              <div class="tags">
                <span 
                  v-for="(tag, index) in job.tags" 
                  :key="index"
                  class="tag"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <!-- Salario -->
            <div class="salary-box">
              <va-icon name="payments" size="1.5rem" />
              <div>
                <div class="salary-label">Sueldo:</div>
                <div class="salary-value">{{ job.salary || 'No Declarado' }}</div>
              </div>
            </div>

            <!-- Convocatoria -->
            <div class="status-box" :class="job.status">
              <va-icon name="campaign" size="small" />
              <span>Convocatoria: <strong>{{ job.status === 'abierta' ? 'ABIERTA' : 'CERRADA' }}</strong></span>
            </div>

            <!-- ID del Empleo -->
            <div class="job-id">
              ID Empleo: {{ job.id }}
            </div>
          </div>

          <!-- Botones de Acción -->
          <div class="job-actions">
            <!-- BOTÓN NUEVO -->
            <va-button
              @click="showApplicationForm = !showApplicationForm"
              color="purple"
              class="postular-btn"
              size="large"
            >
              <va-icon name="celebration" class="btn-icon" />
              <span class="btn-text">{{ showApplicationForm ? 'Cancelar' : 'Quiero postularme' }}</span>
            </va-button>

            <!-- Otros botones (guardar, compartir, denunciar) -->
            <div class="secondary-actions">
              <va-button
                preset="plain"
                color="purple"
                @click="guardarEmpleo"
              >
                <va-icon name="bookmark_border" />
                Guardar Empleo
              </va-button>

              <va-button
                preset="plain"
                color="purple"
                @click="compartirEmpleo"
              >
                <va-icon name="share" />
                Compartir
              </va-button>

              <va-button
                preset="plain"
                color="danger"
                @click="denunciarEmpleo"
              >
                <va-icon name="flag" />
                Denunciar
              </va-button>
            </div>
          </div>
        </div>

        <!-- Descripción del Trabajo -->
        <div class="job-content">
          <div class="content-section">
            <h2 class="section-title">
              <va-icon name="description" />
              Descripción del Empleo
            </h2>
            <div class="section-text" v-html="job.description"></div>
          </div>

          <div v-if="job.requirements" class="content-section">
            <h2 class="section-title">
              <va-icon name="checklist" />
              Requisitos
            </h2>
            <div class="section-text" v-html="job.requirements"></div>
          </div>

          <div v-if="job.benefits" class="content-section">
            <h2 class="section-title">
              <va-icon name="star" />
              Beneficios
            </h2>
            <div class="section-text" v-html="job.benefits"></div>
          </div>

          <div v-if="job.responsibilities" class="content-section">
            <h2 class="section-title">
              <va-icon name="assignment" />
              Responsabilidades
            </h2>
            <div class="section-text" v-html="job.responsibilities"></div>
          </div>
        </div>

        <!-- Application Form -->
        <div v-if="showApplicationForm" class="application-form-section">
          <div class="form-container">
            <div class="form-header">
              <h2>Aplicar para: {{ job.title }}</h2>
              <va-button
                preset="plain"
                color="textPrimary"
                @click="showApplicationForm = false"
              >
                <va-icon name="close" size="large" />
              </va-button>
            </div>

            <!-- Información del Candidato -->
            <div class="form-section">
              <h3 class="form-section-title">Tus Datos</h3>

              <div class="form-group">
                <label class="form-label">Nombre Completo *</label>
                <va-input
                  v-model="applicantData.applicantName"
                  placeholder="Juan Pérez"
                  type="text"
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Email *</label>
                <va-input
                  v-model="applicantData.applicantEmail"
                  placeholder="juan@example.com"
                  type="email"
                  class="form-input"
                />
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">Teléfono</label>
                  <va-input
                    v-model="applicantData.applicantPhone"
                    placeholder="+591..."
                    type="tel"
                    class="form-input"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label">WhatsApp</label>
                  <va-input
                    v-model="applicantData.applicantWhatsapp"
                    placeholder="+591..."
                    type="tel"
                    class="form-input"
                  />
                </div>
              </div>
            </div>

            <!-- Screening Questions -->
            <div v-if="job.screeningQuestions && job.screeningQuestions.length > 0" class="form-section">
              <h3 class="form-section-title">Preguntas de Filtrado</h3>

              <div
                v-for="(question, index) in job.screeningQuestions"
                :key="index"
                class="form-group"
              >
                <label class="form-label">{{ question }}</label>
                <va-textarea
                  v-model="formAnswers[index]"
                  :placeholder="`Responde la pregunta ${index + 1}...`"
                  class="form-textarea"
                  rows="3"
                />
              </div>
            </div>

            <!-- Submit Button -->
            <div class="form-actions">
              <va-button
                @click="handlePostular"
                color="purple"
                size="large"
                class="btn-submit"
                :loading="submitting"
                :disabled="submitting"
              >
                <va-icon name="send" class="btn-icon" />
                <span>{{ submitting ? 'Enviando...' : 'Enviar Aplicación' }}</span>
              </va-button>
            </div>
          </div>
        </div>

        </div>

      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vuestic-ui'
import MainLayout from '@/components/Layout/MainLayout.vue'

// ========== COMPOSABLES ==========
const router = useRouter()
const route = useRoute()
const { init: notify } = useToast()

// ========== DATA ==========
const job = ref({
  id: '',
  title: '',
  companyName: '',
  companyAnonymous: false,
  description: '',
  requirements: '',
  responsibilities: '',
  benefits: '',
  jobCategory: '',
  city: '',
  contractType: '',
  modality: 'Presencial',
  salary: 'No Declarado',
  status: 'active',
  email: '',
  whatsapp: '',
  website: '',
  expiryDate: '',
  createdAt: '',
  views: 0,
  applications: 0,
  publishedDaysAgo: 0,
  selectedPlan: 'free',
  screeningQuestions: [],
  companyAnonymous: false
})

const loading = ref(true)
const error = ref(null)
const submitting = ref(false)
const showApplicationForm = ref(false)
const formAnswers = ref({})
const applicantData = ref({
  applicantName: '',
  applicantEmail: '',
  applicantPhone: '',
  applicantWhatsapp: ''
})

// ========== COMPUTED ==========
const getCompanyDisplayName = computed(() => {
  return job.value.companyAnonymous ? 'Empresa Confidencial' : job.value.companyName
})

const getPlanName = computed(() => {
  const planMap = {
    'free': 'Gratuita',
    'featured': 'Destacada',
    'top': 'TOP',
    'premium': 'Premium'
  }
  return planMap[job.value.selectedPlan] || job.value.selectedPlan
})

const getPublishDate = computed(() => {
  if (job.value.publishedDaysAgo === 0) return 'Publicado hoy'
  if (job.value.publishedDaysAgo === 1) return 'Publicado hace 1 día'
  return `Publicado hace ${job.value.publishedDaysAgo} días`
})

// ========== LIFECYCLE ==========
onMounted(() => {
  loadJobDetail()
})

// ========== METHODS ==========
const loadJobDetail = async () => {
  try {
    loading.value = true
    error.value = null
    const jobId = route.params.id
    const response = await fetch(`/api/jobs/${jobId}/`)

    if (!response.ok) {
      throw new Error('No se pudo cargar el empleo')
    }

    const data = await response.json()
    if (data.success && data.job) {
      job.value = data.job
      // Inicializar formulario de screening questions
      if (job.value.screeningQuestions && Array.isArray(job.value.screeningQuestions)) {
        job.value.screeningQuestions.forEach((q, idx) => {
          formAnswers.value[idx] = ''
        })
      }
    }
  } catch (err) {
    error.value = err.message
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    loading.value = false
  }
}

const handlePostular = async () => {
  try {
    // Validar datos del candidato
    if (!applicantData.value.applicantName.trim()) {
      notify({
        message: '⚠️ Por favor, ingresa tu nombre',
        color: 'warning',
        duration: 3000
      })
      return
    }

    if (!applicantData.value.applicantEmail.trim()) {
      notify({
        message: '⚠️ Por favor, ingresa tu email',
        color: 'warning',
        duration: 3000
      })
      return
    }

    submitting.value = true
    const response = await fetch(`/api/jobs/${job.value.id}/apply`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        applicantName: applicantData.value.applicantName,
        applicantEmail: applicantData.value.applicantEmail,
        applicantPhone: applicantData.value.applicantPhone,
        applicantWhatsapp: applicantData.value.applicantWhatsapp,
        screeningAnswers: formAnswers.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.message || 'Error al aplicar')
    }

    const data = await response.json()
    if (data.success) {
      notify({
        message: '✅ ¡Aplicación registrada exitosamente!',
        color: 'success',
        duration: 5000
      })
      // Actualizar contador
      job.value.applications += 1
      // Limpiar formulario y ocultarlo
      showApplicationForm.value = false
      applicantData.value = {
        applicantName: '',
        applicantEmail: '',
        applicantPhone: '',
        applicantWhatsapp: ''
      }
      formAnswers.value = {}
      // Reinicializar formulario
      if (job.value.screeningQuestions && Array.isArray(job.value.screeningQuestions)) {
        job.value.screeningQuestions.forEach((q, idx) => {
          formAnswers.value[idx] = ''
        })
      }
    }
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    submitting.value = false
  }
}

const guardarEmpleo = () => {
  notify({
    message: '💾 Empleo guardado en tus favoritos',
    color: 'success'
  })
}

const compartirEmpleo = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url).then(() => {
    notify({
      message: '🔗 Enlace copiado al portapapeles',
      color: 'success'
    })
  })
}

const denunciarEmpleo = () => {
  notify({
    message: '🚨 Denuncia enviada. Gracias por tu reporte.',
    color: 'info'
  })
}
</script>

<style scoped>
/* ========== Section ========== */
.job-detail-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #F5F3FF 0%, #FFFFFF 100%);
  padding: 2rem 0;
}

/* ========== LOADING STATE ========== */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.loading-state p {
  margin-top: 1.5rem;
  color: #666;
  font-size: 1rem;
}

/* ========== ERROR STATE ========== */
.error-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.error-state h2 {
  margin: 1rem 0 0.5rem;
  color: var(--color-purple-darkest);
}

.error-state p {
  margin-bottom: 1.5rem;
  color: #666;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* ========== Breadcrumb ========== */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.breadcrumb a {
  color: var(--color-purple);
  text-decoration: none;
  transition: color 0.2s;
}

.breadcrumb a:hover {
  color: var(--color-purple-dark);
  text-decoration: underline;
}

.breadcrumb .separator {
  color: #999;
}

.breadcrumb .current {
  color: #666;
  font-weight: 500;
}

/* ========== Job Header ========== */
.job-header {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  margin-bottom: 2rem;
}

.job-logo {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 2rem;
}

.job-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 12px;
}

.placeholder-logo {
  width: 100%;
  height: 100%;
  background: #F5F5F5;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-verified {
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: #4CAF50;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

/* ========== Job Info ========== */
.job-info {
  text-align: center;
}

.badges-row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.badge-plan {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.35rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge-plan.destacado {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #fff;
}

.badge-plan.premium {
  background: linear-gradient(135deg, #9C27B0 0%, #6A1B9A 100%);
  color: #fff;
}

.badge-urgent {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.35rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  background: #FF5252;
  color: white;
}

.job-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.75rem 0;
}

.company-name {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  color: #666;
  margin: 0 0 2rem 0;
  font-weight: 500;
}

/* ========== Info Grid ========== */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: #F8F8F8;
  border-radius: 8px;
}

.info-label {
  font-weight: 600;
  color: #666;
}

.info-value {
  color: #333;
}

/* ========== Tags ========== */
.tags-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.tags-label {
  font-weight: 600;
  color: #666;
}

.tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  padding: 0.35rem 0.75rem;
  background: rgba(92, 0, 153, 0.1);
  color: var(--color-purple);
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

/* ========== Salary Box ========== */
.salary-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #F0F4FF 0%, #E8F0FF 100%);
  border-radius: 12px;
  margin-bottom: 1rem;
}

.salary-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.salary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple);
}

/* ========== Status Box ========== */
.status-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.status-box.abierta {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.status-box.cerrada {
  background: rgba(244, 67, 54, 0.1);
  color: #F44336;
}

/* ========== Job ID ========== */
.job-id {
  font-size: 0.85rem;
  color: #999;
  text-align: center;
}

/* ========== JOB ACTIONS ========== */
.job-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 2rem;
  background: linear-gradient(135deg, #F8F4FF 0%, #FFFFFF 100%);
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
  margin: 2rem 0;
}

/* BOTÓN PRINCIPAL - "QUIERO POSTULARME" */
.postular-btn {
  width: 100%;
  padding: 1.2rem 2rem !important;
  font-size: 1.1rem !important;
  font-weight: 600 !important;
  background: linear-gradient(135deg, var(--color-purple) 0%, #6A1B9A 100%) !important;
  border: none !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 16px rgba(92, 0, 153, 0.25) !important;
  transition: all 0.3s ease !important;
  position: relative;
  overflow: hidden;
}

.postular-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.postular-btn:hover::before {
  width: 300px;
  height: 300px;
}

.postular-btn:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 8px 24px rgba(92, 0, 153, 0.4) !important;
}

.postular-btn:active {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3) !important;
}

.btn-icon {
  margin-right: 0.5rem;
  font-size: 1.3rem !important;
  animation: celebrate 2s ease-in-out infinite;
}

@keyframes celebrate {
  0%, 100% {
    transform: rotate(0deg) scale(1);
  }
  25% {
    transform: rotate(-10deg) scale(1.1);
  }
  75% {
    transform: rotate(10deg) scale(1.1);
  }
}

.btn-text {
  position: relative;
  z-index: 1;
}

/* ACCIONES SECUNDARIAS */
.secondary-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(92, 0, 153, 0.1);
}

.secondary-actions button {
  font-size: 0.9rem !important;
  padding: 0.6rem 1rem !important;
}

.secondary-actions button:hover {
  background: rgba(92, 0, 153, 0.05) !important;
}

/* ========== Job Content ========== */
.job-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
}

.content-section {
  margin-bottom: 2.5rem;
}

.content-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #E0E0E0;
}

.section-text {
  color: #333;
  line-height: 1.8;
  font-size: 1rem;
}

.section-text ul {
  padding-left: 1.5rem;
  margin: 1rem 0;
}

.section-text li {
  margin-bottom: 0.75rem;
}

.section-text p {
  margin-bottom: 1rem;
}

.section-text strong {
  color: var(--color-purple-darkest);
  font-weight: 600;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .job-header {
    padding: 1.5rem;
  }

  .job-title {
    font-size: 1.5rem;
  }

  .company-name {
    font-size: 1rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .salary-value {
    font-size: 1.25rem;
  }

  .job-actions {
    padding: 1.5rem;
  }

  .postular-btn {
    padding: 1rem 1.5rem !important;
    font-size: 1rem !important;
  }

  .btn-icon {
    font-size: 1.1rem !important;
  }

  .secondary-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .secondary-actions button {
    width: 100%;
    justify-content: flex-start;
  }

  .job-content {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 1.25rem;
  }
}

/* ESTADOS ESPECIALES */
.postular-btn:disabled {
  background: #CCCCCC !important;
  cursor: not-allowed !important;
  box-shadow: none !important;
}

.postular-btn:disabled:hover {
  transform: none !important;
}

/* ========== APPLICATION FORM ========== */
.application-form-section {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-top: 2rem;
  padding: 2.5rem;
  animation: slideDown 0.3s ease-in-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-container {
  max-width: 600px;
  margin: 0 auto;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.form-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
}

.form-section {
  margin-bottom: 2.5rem;
}

.form-section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #f0f0f0;
}

.btn-submit {
  flex: 1;
  padding: 1rem !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
  background: linear-gradient(135deg, #5C0099 0%, #3D0066 100%) !important;
  border: none !important;
  border-radius: 8px !important;
  color: white !important;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3) !important;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .application-form-section {
    padding: 1.5rem;
  }

  .form-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .form-header h2 {
    font-size: 1.25rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-submit {
    width: 100%;
  }
}
</style>