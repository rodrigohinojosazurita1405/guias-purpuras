<!-- frontend/src/views/ApplicationProcess.vue -->
<template>
  <MainLayout>
    <section class="application-process-section">
      <div class="container">
        
        <!-- Breadcrumb -->
        <nav class="breadcrumb">
          <router-link to="/">Inicio</router-link>
          <span class="separator">/</span>
          <router-link to="/guias/trabajos">Trabajos</router-link>
          <span class="separator">/</span>
          <router-link :to="`/guias/trabajos/${jobId}`">{{ jobTitle }}</router-link>
          <span class="separator">/</span>
          <span class="current">Postulación</span>
        </nav>

        <!-- Header con Info del Trabajo -->
        <div class="job-header">
          <div class="job-logo">
            <img 
              v-if="jobData.companyLogo" 
              :src="jobData.companyLogo" 
              :alt="jobData.companyName"
            />
            <div v-else class="placeholder-logo">
              <va-icon name="business" size="3rem" color="#999" />
            </div>
          </div>
          <div class="job-info">
            <h1 class="job-title">{{ jobTitle }}</h1>
            <p class="company-name">{{ jobData.companyName }}</p>
            <p class="job-location">
              <va-icon name="place" size="small" />
              {{ jobData.city }}
            </p>
          </div>
        </div>

        <!-- Stepper / Progress Bar -->
        <div class="stepper">
          <div 
            v-for="(step, index) in steps" 
            :key="index"
            class="step"
            :class="{
              active: currentStep === index,
              completed: currentStep > index
            }"
          >
            <div class="step-indicator">
              <div class="step-circle">
                <va-icon 
                  v-if="currentStep > index" 
                  name="check" 
                  size="1.25rem" 
                  color="white"
                />
                <span v-else>{{ index + 1 }}</span>
              </div>
              <span class="step-label">{{ step.label }}</span>
            </div>
            <div v-if="index < steps.length - 1" class="step-line"></div>
          </div>
        </div>

        <!-- Contenido de los Pasos -->
        <div class="step-content">
          
          <!-- PASO 1: Pretensión y Carta -->
          <div v-if="currentStep === 0" class="step-panel">
            <h2 class="panel-title">Pretensión y Carta</h2>
            <p class="panel-description">
              Cuéntanos sobre tu pretensión salarial y escribe una carta de presentación para esta posición.
            </p>

            <div class="form-section">
              <!-- Pretensión Salarial -->
              <div class="salary-section">
                <h3 class="section-subtitle">
                  <va-icon name="payments" color="purple" />
                  Pretensión Salarial
                </h3>

                <div class="salary-type-selector">
                  <VaRadio
                    v-model="applicationData.salaryType"
                    option="bruto"
                    label="Sueldo Bruto"
                  />
                  <VaRadio
                    v-model="applicationData.salaryType"
                    option="neto"
                    label="Sueldo Neto"
                  />
                </div>

                <div class="salary-input">
                  <VaSelect
                    v-model="applicationData.salaryCurrency"
                    :options="['Bs.', 'USD', '$us']"
                    style="max-width: 120px;"
                  />
                  <VaInput
                    v-model.number="applicationData.salaryAmount"
                    type="number"
                    placeholder="Monto"
                    :min="0"
                    style="flex: 1;"
                  />
                </div>

                <div class="salary-info-box">
                  <va-icon name="info" size="small" color="#2196F3" />
                  <div>
                    <p><strong>Pretensión salarial mensual {{ applicationData.salaryType }}</strong></p>
                    <p v-if="applicationData.salaryType === 'bruto'" class="salary-note">
                      Recibirás líquido Bs. {{ calculatedNetSalary }} después del aporte obligatorio a la Gestora de Seguridad Social
                    </p>
                    <p class="salary-final">
                      La pretensión salarial que enviarás a la empresa es:
                      <strong>{{ applicationData.salaryCurrency }} {{ applicationData.salaryAmount || 0 }}</strong>
                    </p>
                  </div>
                </div>
              </div>

              <!-- Carta de Presentación -->
              <div class="cover-letter-section">
                <h3 class="section-subtitle">
                  <va-icon name="edit_note" color="purple" />
                  Carta de Presentación (Recomendado)
                </h3>

               <VaTextarea
                  v-model="applicationData.coverLetter"
                  placeholder="Escribe aquí tu carta de presentación..."
                  :min-rows="8"
                  :max-rows="15"
                  counter
                  :max-length="2000"
                  class="cover-letter-input"
                  style="width: 100% !important;"
                />

                <div class="field-hint">
                  💡 Una buena carta de presentación aumenta tus posibilidades. Menciona por qué te interesa la posición y qué puedes aportar.
                </div>
              </div>
            </div>
          </div>

          <!-- PASO 2: Currículum -->
          <div v-if="currentStep === 1" class="step-panel">
            <h2 class="panel-title">Currículum</h2>
            <p class="panel-description">
              Revisa que tu currículum esté actualizado y con datos de contacto correctos.
            </p>

            <div class="cv-review">
              <!-- Opción de usar CV guardado -->
              <div v-if="hasSavedCV" class="saved-cv-option">
                <VaCheckbox
                  v-model="applicationData.useSavedCV"
                  label="Usar mi currículum guardado"
                />
                <div v-if="applicationData.useSavedCV" class="cv-preview">
                  <va-icon name="description" size="3rem" color="purple" />
                  <div class="cv-info">
                    <h4>{{ savedCV.title }}</h4>
                    <p>Última actualización: {{ savedCV.lastUpdate }}</p>
                  </div>
                  <VaButton preset="plain" @click="editCV">
                    Editar
                  </VaButton>
                </div>
              </div>

              <div v-if="!applicationData.useSavedCV || !hasSavedCV" class="cv-sections">
                <div class="cv-notice">
                  <va-icon name="info" color="#2196F3" />
                  <p>Revisa que tu currículum esté actualizado y con datos de contacto correctos.</p>
                </div>

                <!-- Botón para usar otro currículum -->
                <div class="cv-action">
                  <VaButton color="primary" @click="showUploadCVModal = true">
                    <va-icon name="upload_file" />
                    Usar otro currículum
                  </VaButton>
                </div>

                <!-- Resumen del CV -->
                <div class="cv-summary">
                  <div class="cv-section">
                    <div class="section-header">
                      <h4>
                        <va-icon name="person" />
                        Datos Personales
                      </h4>
                      <VaButton preset="plain" icon="edit" size="small">
                        Editar
                      </VaButton>
                    </div>
                    <div class="section-content">
                      <p><strong>CV actualizado:</strong> {{ cvData.lastUpdate }}</p>
                      <p><strong>Nombre:</strong> {{ cvData.fullName }}</p>
                      <p><strong>Email:</strong> {{ cvData.email }}</p>
                      <p><strong>Teléfono:</strong> {{ cvData.phone }}</p>
                      <p><strong>Ciudad:</strong> {{ cvData.city }}</p>
                    </div>
                  </div>

                  <div class="cv-section">
                    <div class="section-header">
                      <h4>
                        <va-icon name="school" />
                        Título Profesional
                      </h4>
                      <VaButton preset="plain" icon="edit" size="small">
                        Editar
                      </VaButton>
                    </div>
                    <div class="section-content">
                      <p>{{ cvData.professionalTitle }}</p>
                    </div>
                  </div>

                  <div class="cv-section">
                    <div class="section-header">
                      <h4>
                        <va-icon name="article" />
                        Presentación / Biografía
                      </h4>
                      <VaButton preset="plain" icon="edit" size="small">
                        Editar
                      </VaButton>
                    </div>
                    <div class="section-content">
                      <p>{{ cvData.bio }}</p>
                    </div>
                  </div>

                  <div class="cv-section">
                    <div class="section-header">
                      <h4>
                        <va-icon name="work_history" />
                        Resumen de Experiencia Laboral
                      </h4>
                      <VaButton preset="plain" icon="edit" size="small">
                        Editar
                      </VaButton>
                    </div>
                    <div class="section-content">
                      <div v-for="(exp, index) in cvData.experience" :key="index" class="experience-item">
                        <p><strong>{{ exp.position }}</strong></p>
                        <p>{{ exp.company }} | {{ exp.period }}</p>
                      </div>
                    </div>
                  </div>

                  <div class="cv-section">
                    <div class="section-header">
                      <h4>
                        <va-icon name="school" />
                        Experiencia Laboral
                      </h4>
                      <VaButton preset="plain" icon="edit" size="small">
                        Editar
                      </VaButton>
                    </div>
                    <div class="section-content">
                      <p>{{ cvData.workExperience }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- PASO 3: Revisión -->
          <div v-if="currentStep === 2" class="step-panel">
            <h2 class="panel-title">Revisión</h2>
            <p class="panel-description">
              Revisa tu postulación antes de enviarla. Asegúrate de que toda la información sea correcta.
            </p>

            <div class="review-content">
              <!-- Resumen de la Postulación -->
              <div class="review-card">
                <h3 class="review-title">
                  <va-icon name="work" color="purple" />
                  Oferta de Trabajo
                </h3>
                <div class="review-info">
                  <div class="review-row">
                    <span class="review-label">Puesto:</span>
                    <span class="review-value">{{ jobTitle }}</span>
                  </div>
                  <div class="review-row">
                    <span class="review-label">Empresa:</span>
                    <span class="review-value">{{ jobData.companyName }}</span>
                  </div>
                  <div class="review-row">
                    <span class="review-label">Ciudad:</span>
                    <span class="review-value">{{ jobData.city }}</span>
                  </div>
                </div>
              </div>

              <div class="review-card">
                <h3 class="review-title">
                  <va-icon name="payments" color="purple" />
                  Pretensión Salarial
                </h3>
                <div class="review-info">
                  <div class="review-row">
                    <span class="review-label">Tipo:</span>
                    <span class="review-value">Sueldo {{ applicationData.salaryType === 'bruto' ? 'Bruto' : 'Neto' }}</span>
                  </div>
                  <div class="review-row">
                    <span class="review-label">Monto:</span>
                    <span class="review-value">{{ applicationData.salaryCurrency }} {{ applicationData.salaryAmount }}</span>
                  </div>
                </div>
              </div>

              <div class="review-card">
                <h3 class="review-title">
                  <va-icon name="edit_note" color="purple" />
                  Carta de Presentación
                </h3>
                <div class="review-info">
                  <p v-if="applicationData.coverLetter" class="cover-letter-preview">
                    {{ applicationData.coverLetter }}
                  </p>
                  <p v-else class="no-content">No se incluyó carta de presentación</p>
                </div>
              </div>

              <div class="review-card">
                <h3 class="review-title">
                  <va-icon name="description" color="purple" />
                  Currículum
                </h3>
                <div class="review-info">
                  <div class="review-row">
                    <span class="review-label">Nombre:</span>
                    <span class="review-value">{{ cvData.fullName }}</span>
                  </div>
                  <div class="review-row">
                    <span class="review-label">Email:</span>
                    <span class="review-value">{{ cvData.email }}</span>
                  </div>
                  <div class="review-row">
                    <span class="review-label">Teléfono:</span>
                    <span class="review-value">{{ cvData.phone }}</span>
                  </div>
                  <div class="review-row">
                    <span class="review-label">Título:</span>
                    <span class="review-value">{{ cvData.professionalTitle }}</span>
                  </div>
                </div>
              </div>

              <!-- Aviso importante -->
              <div class="important-notice">
                <va-icon name="info" size="2rem" color="#2196F3" />
                <div>
                  <h4>Importante</h4>
                  <p>La empresa no recibirá tu postulación hasta que presiones el botón "Enviar Postulación".</p>
                  <p>Una vez enviada, no podrás modificar tu postulación.</p>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- Botones de Navegación -->
        <div class="navigation-buttons">
          <VaButton
            v-if="currentStep > 0"
            preset="secondary"
            size="large"
            @click="previousStep"
          >
            <va-icon name="arrow_back" />
            Anterior
          </VaButton>

          <VaButton
            color="secondary"
            size="large"
            @click="cancelApplication"
          >
            Cancelar
          </VaButton>

          <VaButton
            v-if="currentStep < steps.length - 1"
            color="primary"
            size="large"
            @click="nextStep"
            :disabled="!canProceed"
          >
            Siguiente
            <va-icon name="arrow_forward" />
          </VaButton>

          <VaButton
            v-else
            color="warning"
            size="large"
            @click="submitApplication"
            :loading="isSubmitting"
          >
            <va-icon name="send" />
            Enviar Postulación
          </VaButton>
        </div>

      </div>
    </section>

    <!-- Modal de Subir CV -->
    <VaModal
      v-model="showUploadCVModal"
      title="Subir Currículum"
      size="medium"
      hide-default-actions
    >
      <div class="upload-cv-modal">
        <p>Puedes subir tu currículum en formato PDF, DOC o DOCX (máximo 5MB)</p>
        <VaFileUpload
          v-model="uploadedCV"
          type="single"
          file-types=".pdf,.doc,.docx"
        />
        <div class="modal-actions">
          <VaButton preset="secondary" @click="showUploadCVModal = false">
            Cancelar
          </VaButton>
          <VaButton color="primary" @click="uploadCV">
            Subir
          </VaButton>
        </div>
      </div>
    </VaModal>

  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/Layout/MainLayout.vue'

const route = useRoute()
const router = useRouter()

// ========== DATOS ==========
const jobId = ref(route.params.id)
const currentStep = ref(0)
const isSubmitting = ref(false)
const showUploadCVModal = ref(false)
const uploadedCV = ref(null)

const steps = [
  { label: 'Pretensión y Carta' },
  { label: 'Currículum' },
  { label: 'Revisión' }
]

// Mock data del trabajo
const jobData = ref({
  companyName: 'Agropartners S.R.L.',
  companyLogo: 'https://via.placeholder.com/200x80/4CAF50/FFFFFF?text=Agropartners',
  city: 'Santa Cruz de la Sierra'
})

const jobTitle = ref('Técnico(a) Comercial Agrónomo(a)')

// Datos de la postulación
const applicationData = ref({
  salaryType: 'bruto',
  salaryCurrency: 'Bs.',
  salaryAmount: 4000,
  coverLetter: '',
  useSavedCV: true
})

// Mock CV guardado
const hasSavedCV = ref(true)
const savedCV = ref({
  title: 'CV_RodrigoHinojosa.pdf',
  lastUpdate: '15/10/2025'
})

// Mock datos del CV
const cvData = ref({
  lastUpdate: '15/10/2025',
  fullName: 'Rodrigo Hinojosa Zurita',
  email: 'rodrigohinojosazurita@gmail.com',
  phone: '65324767',
  city: 'Cochabamba',
  professionalTitle: 'Tec. Sup En informatica',
  bio: 'Soy una persona proactiva, emprendedora, analítica, eficaz y eficiente me gusta el trabajo en equipo y aprender cosas nuevas.',
  experience: [
    {
      position: 'Marketing y Publicidad',
      company: 'Por Industria',
      period: '7 años y 4 meses (1 trabajo)'
    }
  ],
  workExperience: 'Trabajos de tiempo completo o medio tiempo'
})

// ========== COMPUTED ==========
const calculatedNetSalary = computed(() => {
  if (applicationData.value.salaryType === 'bruto' && applicationData.value.salaryAmount) {
    // Aproximado: 13% de descuento
    const net = applicationData.value.salaryAmount * 0.87
    return Math.round(net).toFixed(2)
  }
  return 0
})

const canProceed = computed(() => {
  if (currentStep.value === 0) {
    return applicationData.value.salaryAmount > 0
  }
  if (currentStep.value === 1) {
    return true // Siempre puede avanzar si tiene CV
  }
  return true
})

// ========== MÉTODOS ==========
const nextStep = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const cancelApplication = () => {
  if (confirm('¿Estás seguro de que quieres cancelar tu postulación?')) {
    router.push(`/guias/trabajos/${jobId.value}`)
  }
}

const submitApplication = async () => {
  isSubmitting.value = true
  
  try {
    // TODO: Enviar postulación al backend
    // const response = await fetch('/api/applications/', {
    //   method: 'POST',
    //   body: JSON.stringify({
    //     job_id: jobId.value,
    //     salary: applicationData.value.salaryAmount,
    //     salary_type: applicationData.value.salaryType,
    //     cover_letter: applicationData.value.coverLetter
    //   })
    // })
    
    // Simular delay
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Mostrar mensaje de éxito
    alert('¡Postulación enviada exitosamente!')
    
    // Redirigir al detalle del trabajo o a mis postulaciones
    router.push('/dashboard/mis-postulaciones')
    
  } catch (error) {
    console.error('Error al enviar postulación:', error)
    alert('Hubo un error al enviar tu postulación. Por favor, intenta nuevamente.')
  } finally {
    isSubmitting.value = false
  }
}

const editCV = () => {
  // TODO: Navegar a editar CV
  router.push('/perfil/editar-cv')
}

const uploadCV = () => {
  if (uploadedCV.value) {
    console.log('CV subido:', uploadedCV.value)
    showUploadCVModal.value = false
    // TODO: Procesar CV subido
  }
}

// Cargar datos al montar
onMounted(() => {
  // TODO: Cargar datos del trabajo y del usuario
  console.log('Cargando datos para postulación al trabajo:', jobId.value)
})
</script>

<style scoped>
.application-process-section {
  min-height: calc(100vh - 200px);
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

/* ========== Breadcrumb ========== */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  flex-wrap: wrap;
}

.breadcrumb a {
  color: var(--color-purple);
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.breadcrumb .separator {
  color: #999;
}

.breadcrumb .current {
  color: #666;
}

/* ========== Job Header ========== */
.job-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.job-logo {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  background: #F5F5F5;
  border: 2px solid #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.job-logo img {
  max-width: 90px;
  max-height: 90px;
  object-fit: contain;
}

.placeholder-logo {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
}

.job-info {
  flex: 1;
}

.job-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.company-name {
  font-size: 1.125rem;
  color: #666;
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.job-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #999;
  margin: 0;
  font-size: 0.95rem;
}

/* ========== Stepper ========== */
.stepper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.step {
  display: flex;
  align-items: center;
  flex: 1;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.step-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #E0E0E0;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  transition: all 0.3s ease;
}

.step.active .step-circle {
  background: var(--color-purple);
  color: white;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

.step.completed .step-circle {
  background: #4CAF50;
  color: white;
}

.step-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #666;
  text-align: center;
}

.step.active .step-label {
  color: var(--color-purple);
}

.step.completed .step-label {
  color: #4CAF50;
}

.step-line {
  flex: 1;
  height: 3px;
  background: #E0E0E0;
  margin: 0 1rem;
  margin-bottom: 2rem;
}

.step.completed .step-line {
  background: #4CAF50;
}

/* ========== Step Content ========== */
.step-content {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  min-height: 500px;
}

.step-panel {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.panel-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.panel-description {
  font-size: 1.05rem;
  color: #666;
  margin: 0 0 2.5rem 0;
  line-height: 1.6;
}

/* ========== Form Sections ========== */
.form-section {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.section-subtitle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #F0F0F0;
}

/* ========== Salary Section ========== */
.salary-type-selector {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.salary-input {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.salary-info-box {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(33, 150, 243, 0.05);
  border-left: 4px solid #2196F3;
  border-radius: 8px;
}

.salary-info-box p {
  margin: 0 0 0.5rem 0;
  font-size: 0.95rem;
  color: #333;
}

.salary-note {
  font-size: 0.9rem;
  color: #666;
}

.salary-final {
  font-size: 1rem;
  margin-top: 0.75rem;
}

.salary-final strong {
  color: var(--color-purple);
  font-size: 1.125rem;
}

/* ========== Cover Letter ========== */
.cover-letter-input {
  margin-bottom: 1rem;
}

.field-hint {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

/* ========== CV Review ========== */
.cv-review {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.saved-cv-option {
  padding: 1.5rem;
  background: #F8F8F8;
  border-radius: 8px;
}

.cv-preview {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  margin-top: 1rem;
  border: 2px solid #E0E0E0;
}

.cv-info {
  flex: 1;
}

.cv-info h4 {
  margin: 0 0 0.35rem 0;
  color: var(--color-purple-darkest);
  font-size: 1.125rem;
}

.cv-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.cv-notice {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: rgba(33, 150, 243, 0.05);
  border-left: 4px solid #2196F3;
  border-radius: 8px;
}

.cv-notice p {
  margin: 0;
  color: #333;
}

.cv-action {
  display: flex;
  justify-content: center;
  padding: 1rem 0;
}

.cv-summary {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cv-section {
  padding: 1.5rem;
  background: #F8F8F8;
  border-radius: 8px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
}

.section-content {
  color: #333;
  line-height: 1.6;
}

.section-content p {
  margin: 0 0 0.5rem 0;
}

.experience-item {
  margin-bottom: 1rem;
}

.experience-item:last-child {
  margin-bottom: 0;
}

/* ========== Review Content ========== */
.review-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-card {
  padding: 2rem;
  background: #F8F8F8;
  border-radius: 12px;
  border: 2px solid #E0E0E0;
}

.review-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1.25rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #E0E0E0;
}

.review-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.review-row {
  display: flex;
  gap: 1rem;
  font-size: 1rem;
}

.review-label {
  font-weight: 600;
  color: #666;
  min-width: 120px;
}

.review-value {
  color: #333;
}

.cover-letter-preview {
  white-space: pre-wrap;
  line-height: 1.7;
  color: #333;
  margin: 0;
  padding: 1rem;
  background: white;
  border-radius: 8px;
}

.no-content {
  color: #999;
  font-style: italic;
  margin: 0;
}

.important-notice {
  display: flex;
  gap: 1.5rem;
  padding: 2rem;
  background: rgba(33, 150, 243, 0.08);
  border-left: 4px solid #2196F3;
  border-radius: 12px;
}

.important-notice h4 {
  margin: 0 0 0.75rem 0;
  color: #1976D2;
  font-size: 1.125rem;
}

.important-notice p {
  margin: 0 0 0.5rem 0;
  color: #333;
  line-height: 1.6;
}

/* ========== Navigation Buttons ========== */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.navigation-buttons .va-button {
  min-width: 150px;
}

/* ========== Upload Modal ========== */
.upload-cv-modal {
  padding: 1rem;
}

.upload-cv-modal p {
  margin: 0 0 1.5rem 0;
  color: #666;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .stepper {
    padding: 1.5rem 1rem;
    overflow-x: auto;
  }

  .step-indicator {
    min-width: 80px;
  }

  .step-circle {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }

  .step-label {
    font-size: 0.8rem;
  }

  .step-line {
    margin: 0 0.5rem;
  }

  .step-content {
    padding: 1.5rem;
  }

  .panel-title {
    font-size: 1.5rem;
  }

  .job-header {
    flex-direction: column;
    text-align: center;
  }

  .job-title {
    font-size: 1.25rem;
  }

  .salary-input {
    flex-direction: column;
  }

  .navigation-buttons {
    flex-wrap: wrap;
  }

  .navigation-buttons .va-button {
    flex: 1;
    min-width: 120px;
  }
}
</style>