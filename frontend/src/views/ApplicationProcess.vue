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

          <!-- PASO 2: Currículum - VERSIÓN CORREGIDA -->
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
                  @update:model-value="handleCVCheckboxChange"
                >
                  Usar mi currículum guardado
                </VaCheckbox>

                <!-- Preview del CV guardado (solo si está activado el checkbox) -->
                <transition name="fade">
                  <div v-if="applicationData.useSavedCV" class="cv-preview">
                    <va-icon name="description" size="3rem" color="purple" />
                    <div class="cv-info">
                      <h4>{{ savedCV.title }}</h4>
                      <p>Última actualización: {{ savedCV.lastUpdate }}</p>
                    </div>
                    <VaButton 
                      preset="plain" 
                      color="purple"
                      @click="editCV"
                    >
                      Editar
                    </VaButton>
                  </div>
                </transition>
              </div>

              <!-- Mensaje si no hay CV guardado -->
              <VaAlert
                v-if="!hasSavedCV"
                color="warning"
                border="left"
              >
                <template #icon>
                  <va-icon name="info" />
                </template>
                No tienes un currículum guardado. Por favor, sube uno nuevo o crea tu CV.
              </VaAlert>

              <!-- Sección para subir nuevo CV o crear uno -->
              <transition name="fade">
                <div v-if="!applicationData.useSavedCV || !hasSavedCV" class="cv-sections">
                  
                  <!-- Notice informativo -->
                  <div class="cv-notice">
                    <va-icon name="info" color="#2196F3" />
                    <p>
                      Puedes subir tu CV en formato PDF, DOC o DOCX, o llenar tu información directamente en nuestra plataforma.
                    </p>
                  </div>

                  <!-- Opciones: Subir archivo o llenar formulario -->
                  <div class="cv-options">
                    <VaButton 
                      color="purple"
                      @click="showUploadCVModal = true"
                      size="large"
                      class="cv-option-btn"
                    >
                      <va-icon name="upload_file" size="large" />
                      <div class="btn-content">
                        <span class="btn-title">Subir mi CV</span>
                        <span class="btn-subtitle">PDF, DOC o DOCX</span>
                      </div>
                    </VaButton>

                    <div class="option-divider">
                      <span>o</span>
                    </div>

                    <VaButton 
                      preset="secondary"
                      @click="showFillCVForm = true"
                      size="large"
                      class="cv-option-btn"
                    >
                      <va-icon name="edit" size="large" />
                      <div class="btn-content">
                        <span class="btn-title">Crear mi CV</span>
                        <span class="btn-subtitle">Llenar formulario</span>
                      </div>
                    </VaButton>
                  </div>

                  <!-- Mostrar CV subido (si existe) -->
                  <transition name="fade">
                    <div v-if="applicationData.uploadedCV" class="uploaded-cv-card">
                      <div class="cv-file-info">
                        <va-icon name="check_circle" color="success" size="2.5rem" />
                        <div class="file-details">
                          <h4>{{ applicationData.uploadedCV.name }}</h4>
                          <p>{{ formatFileSize(applicationData.uploadedCV.size) }} • {{ applicationData.uploadedCV.type }}</p>
                          <p class="upload-date">Subido {{ formatUploadDate(applicationData.uploadedCV.uploadedAt) }}</p>
                        </div>
                      </div>
                      <div class="cv-file-actions">
                        <VaButton
                          preset="plain"
                          icon="visibility"
                          @click="previewCV"
                          title="Ver CV"
                        />
                        <VaButton
                          preset="plain"
                          icon="delete"
                          color="danger"
                          @click="removeUploadedCV"
                          title="Eliminar"
                        />
                      </div>
                    </div>
                  </transition>

                  <!-- Resumen del CV (si está llenando el formulario) -->
                  <transition name="fade">
                    <div v-if="showFillCVForm && !applicationData.useSavedCV" class="cv-summary">
                      
                      <!-- Datos Personales -->
                      <div class="cv-section">
                        <div class="section-header">
                          <h4>
                            <va-icon name="person" />
                            Datos Personales
                          </h4>
                          <VaButton 
                            preset="plain" 
                            icon="edit" 
                            size="small"
                            @click="editSection('personal')"
                          >
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

                      <!-- Título Profesional -->
                      <div class="cv-section">
                        <div class="section-header">
                          <h4>
                            <va-icon name="school" />
                            Título Profesional
                          </h4>
                          <VaButton 
                            preset="plain" 
                            icon="edit" 
                            size="small"
                            @click="editSection('title')"
                          >
                            Editar
                          </VaButton>
                        </div>
                        <div class="section-content">
                          <p>{{ cvData.professionalTitle || 'No especificado' }}</p>
                        </div>
                      </div>

                      <!-- Presentación / Biografía -->
                      <div class="cv-section">
                        <div class="section-header">
                          <h4>
                            <va-icon name="article" />
                            Presentación / Biografía
                          </h4>
                          <VaButton 
                            preset="plain" 
                            icon="edit" 
                            size="small"
                            @click="editSection('bio')"
                          >
                            Editar
                          </VaButton>
                        </div>
                        <div class="section-content">
                          <p>{{ cvData.bio || 'No especificado' }}</p>
                        </div>
                      </div>

                      <!-- Resumen de Experiencia Laboral -->
                      <div class="cv-section">
                        <div class="section-header">
                          <h4>
                            <va-icon name="work_history" />
                            Experiencia Laboral
                          </h4>
                          <VaButton 
                            preset="plain" 
                            icon="edit" 
                            size="small"
                            @click="editSection('experience')"
                          >
                            Editar
                          </VaButton>
                        </div>
                        <div class="section-content">
                          <div 
                            v-if="cvData.experience.length > 0"
                            v-for="(exp, index) in cvData.experience" 
                            :key="index" 
                            class="experience-item"
                          >
                            <p><strong>{{ exp.position }}</strong></p>
                            <p>{{ exp.company }} | {{ exp.period }}</p>
                          </div>
                          <p v-else class="no-content">No has agregado experiencia laboral</p>
                        </div>
                      </div>

                    </div>
                  </transition>
                </div>
              </transition>
            </div>
          </div>

          <!-- PASO 3: Revisión -->
          <div v-if="currentStep === 2" class="step-panel">
            <h2 class="panel-title">Revisión</h2>
            <p class="panel-description">
              Revisa tu postulación antes de enviarla. Asegúrate de que toda la información sea correcta.
            </p>

            <div class="review-content">
              <!-- Revisión de Pretensión Salarial y Carta -->
              <div class="review-card">
                <h3 class="review-title">
                  <va-icon name="payments" />
                  Pretensión Salarial
                </h3>
                <div class="review-info">
                  <div class="review-row">
                    <span class="review-label">Tipo:</span>
                    <span class="review-value">{{ applicationData.salaryType === 'bruto' ? 'Sueldo Bruto' : 'Sueldo Neto' }}</span>
                  </div>
                  <div class="review-row">
                    <span class="review-label">Monto:</span>
                    <span class="review-value">{{ applicationData.salaryCurrency }} {{ applicationData.salaryAmount || 0 }}</span>
                  </div>
                </div>
              </div>

              <div class="review-card">
                <h3 class="review-title">
                  <va-icon name="edit_note" />
                  Carta de Presentación
                </h3>
                <div class="review-info">
                  <p v-if="applicationData.coverLetter" class="cover-letter-preview">{{ applicationData.coverLetter }}</p>
                  <p v-else class="no-content">No has incluido carta de presentación</p>
                </div>
              </div>

              <!-- Revisión de CV -->
              <div class="review-card">
                <h3 class="review-title">
                  <va-icon name="description" />
                  Currículum
                </h3>
                <div class="review-info">
                  <div v-if="applicationData.useSavedCV && hasSavedCV" class="review-row">
                    <span class="review-label">CV:</span>
                    <span class="review-value">{{ savedCV.title }}</span>
                  </div>
                  <div v-else-if="applicationData.uploadedCV" class="review-row">
                    <span class="review-label">CV:</span>
                    <span class="review-value">{{ applicationData.uploadedCV.name }}</span>
                  </div>
                  <p v-else class="no-content">No has adjuntado un CV</p>
                </div>
              </div>

              <!-- Aviso importante -->
              <div class="important-notice">
                <va-icon name="info" size="2rem" color="#2196F3" />
                <div>
                  <h4>Antes de enviar</h4>
                  <p>• Asegúrate de que todos tus datos sean correctos.</p>
                  <p>• Una vez enviada, no podrás modificar tu postulación.</p>
                  <p>• La empresa recibirá tu información y se pondrá en contacto si hay interés.</p>
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
            @click="previousStep"
          >
            <va-icon name="arrow_back" />
            Anterior
          </VaButton>
          
          <div style="flex: 1;"></div>
          
          <VaButton
            v-if="currentStep < steps.length - 1"
            color="purple"
            @click="nextStep"
            :disabled="!canProceed"
          >
            Siguiente
            <va-icon name="arrow_forward" />
          </VaButton>

          <VaButton
            v-if="currentStep === steps.length - 1"
            color="success"
            @click="submitApplication"
            :loading="isSubmitting"
          >
            <va-icon name="send" />
            Enviar Postulación
          </VaButton>
        </div>

      </div>
    </section>

    <!-- Modal de Upload de CV -->
    <VaModal
      v-model="showUploadCVModal"
      size="large"
      title="Subir mi Currículum"
      :hide-default-actions="true"
      no-padding
    >
      <div class="upload-cv-modal-content">
        <p class="modal-description">
          Sube tu CV en formato PDF, DOC o DOCX. El archivo no debe superar 5MB.
        </p>

        <!-- Componente de Upload -->
        <FileUpload
          ref="cvUploadRef"
          accept=".pdf,.doc,.docx"
          :max-size="5"
          :multiple="false"
          file-type="CV"
          @upload="handleCVUpload"
          @remove="handleCVRemove"
          @error="handleUploadError"
        />

        <!-- Botones del Modal -->
        <div class="modal-actions">
          <VaButton
            preset="secondary"
            @click="closeUploadModal"
          >
            Cancelar
          </VaButton>
          <VaButton
            color="purple"
            @click="confirmUploadCV"
            :disabled="!uploadedFile"
          >
            <va-icon name="check" />
            Usar este CV
          </VaButton>
        </div>
      </div>
    </VaModal>

  </MainLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vuestic-ui'
import MainLayout from '@/components/Layout/MainLayout.vue'
import FileUpload from '@/components/Upload/FileUpload.vue'

// ========== COMPOSABLES ==========
const router = useRouter()
const route = useRoute()
const { init: notify } = useToast()

// ========== DATA SIMULADA ==========
const jobId = ref(route.params.id || '123')
const jobTitle = ref('Técnico(a) Comercial Agrónomo(a)')
const jobData = ref({
  companyName: 'Agropartners S.R.L.',
  companyLogo: null,
  city: 'Santa Cruz de la Sierra'
})

// ========== STATE ==========
const currentStep = ref(0)
const isSubmitting = ref(false)

const steps = ref([
  { label: 'Pretensión y Carta' },
  { label: 'Currículum' },
  { label: 'Revisión' }
])

// Datos de la aplicación
const applicationData = ref({
  salaryType: 'bruto',
  salaryCurrency: 'Bs.',
  salaryAmount: null,
  coverLetter: '',
  useSavedCV: false,
  uploadedCV: null
})

// Variables para CV
const showFillCVForm = ref(false)
const cvUploadRef = ref(null)
const uploadedFile = ref(null)
const showUploadCVModal = ref(false)

// Mock de CV guardado
const hasSavedCV = ref(true)
const savedCV = ref({
  title: 'CV_RodrigoHinojosa.pdf',
  lastUpdate: '15/10/2025'
})

// Mock de datos del CV
const cvData = ref({
  lastUpdate: '15/10/2025',
  fullName: 'Rodrigo Hinojosa Zurita',
  email: 'rodrigohinojosazurita@gmail.com',
  phone: '65324767',
  city: 'Cochabamba',
  professionalTitle: 'Tec. Sup En Informática',
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
  if (!applicationData.value.salaryAmount) return 0
  // Cálculo simplificado (restar 12.71% del AFP)
  const afpDeduction = applicationData.value.salaryAmount * 0.1271
  return Math.round(applicationData.value.salaryAmount - afpDeduction)
})

const canProceed = computed(() => {
  if (currentStep.value === 0) {
    // Paso 1: Al menos debe tener monto salarial
    return applicationData.value.salaryAmount > 0
  }
  
  if (currentStep.value === 1) {
    // Paso 2: Debe tener CV (guardado o subido)
    return (applicationData.value.useSavedCV && hasSavedCV.value) || 
           applicationData.value.uploadedCV !== null
  }
  
  return true
})

// ========== METHODS - NAVEGACIÓN ==========
const nextStep = () => {
  if (!canProceed.value) {
    notify({
      message: 'Por favor completa la información requerida',
      color: 'warning'
    })
    return
  }
  
  if (currentStep.value < steps.value.length - 1) {
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

const submitApplication = async () => {
  isSubmitting.value = true
  
  // Simular envío
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  notify({
    message: '🎉 ¡Postulación enviada exitosamente!',
    color: 'success',
    duration: 4000
  })
  
  isSubmitting.value = false
  
  // Redirigir a la página del empleo
  router.push(`/guias/trabajos/${jobId.value}`)
}

// ========== METHODS - CV CHECKBOX ==========
const handleCVCheckboxChange = (value) => {
  console.log('Checkbox CV cambió a:', value)
  
  // Si activa el checkbox pero no hay CV guardado
  if (value && !hasSavedCV.value) {
    notify({
      message: '⚠️ No tienes un CV guardado. Por favor, sube uno nuevo.',
      color: 'warning',
      duration: 3000
    })
    
    // Desactivar automáticamente después de un momento
    setTimeout(() => {
      applicationData.value.useSavedCV = false
    }, 100)
    return
  }
  
  // Si destiquea, limpiar el CV subido y cerrar formulario
  if (!value) {
    showFillCVForm.value = false
  }
}

const editCV = () => {
  notify({
    message: '🚧 Edición de CV próximamente',
    color: 'info'
  })
  // TODO: Redirigir a editar CV
}

// ========== METHODS - UPLOADED CV ==========
const removeUploadedCV = () => {
  if (confirm('¿Estás seguro de eliminar este archivo?')) {
    applicationData.value.uploadedCV = null
    notify({
      message: '🗑️ CV eliminado correctamente',
      color: 'info'
    })
  }
}

const previewCV = () => {
  if (applicationData.value.uploadedCV?.url) {
    window.open(applicationData.value.uploadedCV.url, '_blank')
  } else {
    notify({
      message: '⚠️ No se puede previsualizar este archivo',
      color: 'warning'
    })
  }
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatUploadDate = (date) => {
  if (!date) return ''
  const now = new Date()
  const uploadDate = new Date(date)
  const diff = now - uploadDate
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (minutes < 1) return 'hace unos segundos'
  if (minutes < 60) return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`
  if (hours < 24) return `hace ${hours} hora${hours > 1 ? 's' : ''}`
  if (days < 7) return `hace ${days} día${days > 1 ? 's' : ''}`
  return uploadDate.toLocaleDateString()
}

const editSection = (section) => {
  notify({
    message: `🚧 Editando sección: ${section}`,
    color: 'info'
  })
  // TODO: Abrir modal de edición
}

// ========== METHODS - UPLOAD MODAL ==========
const handleCVUpload = (fileData) => {
  console.log('CV subido:', fileData)
  uploadedFile.value = fileData
  
  notify({
    message: `✅ ${fileData.name} cargado correctamente`,
    color: 'success'
  })
}

const handleCVRemove = (fileData) => {
  console.log('CV eliminado:', fileData)
  uploadedFile.value = null
}

const handleUploadError = (errorMessage) => {
  notify({
    message: errorMessage,
    color: 'danger'
  })
}

const confirmUploadCV = () => {
  if (!uploadedFile.value) {
    notify({
      message: '⚠️ Debes subir un archivo primero',
      color: 'warning'
    })
    return
  }

  // Guardar el CV subido en applicationData
  applicationData.value.uploadedCV = {
    ...uploadedFile.value,
    uploadedAt: new Date()
  }

  // Asegurarse de que no esté usando el CV guardado
  applicationData.value.useSavedCV = false

  notify({
    message: '✅ CV adjuntado correctamente a tu postulación',
    color: 'success',
    duration: 3000
  })

  // Cerrar el modal
  closeUploadModal()
}

const closeUploadModal = () => {
  showUploadCVModal.value = false
  
  // Limpiar el archivo temporal después de un momento
  setTimeout(() => {
    uploadedFile.value = null
    if (cvUploadRef.value) {
      // Resetear el componente de upload
      cvUploadRef.value.files = []
    }
  }, 300)
}
</script>

<style scoped>
/* ========== Section ========== */
.application-process-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #F5F3FF 0%, #FFFFFF 100%);
  padding: 2rem 0;
}

.container {
  max-width: 900px;
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
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.job-logo {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.job-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 8px;
}

.placeholder-logo {
  width: 100%;
  height: 100%;
  background: #F5F5F5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
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
  gap: 0.35rem;
  color: #999;
  font-size: 0.95rem;
  margin: 0;
}

/* ========== Stepper ========== */
.stepper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
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
  font-weight: 700;
  font-size: 1.125rem;
  transition: all 0.3s ease;
}

.step.active .step-circle {
  background: var(--color-purple);
  color: white;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
  transform: scale(1.1);
}

.step.completed .step-circle {
  background: #4CAF50;
  color: white;
}

.step-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #666;
  text-align: center;
  max-width: 100px;
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
  position: relative;
  top: -25px;
}

.step.completed + .step .step-line {
  background: #4CAF50;
}

/* ========== Step Content ========== */
.step-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 3rem;
  margin-bottom: 2rem;
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
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1rem 0;
}

.panel-description {
  font-size: 1rem;
  color: #666;
  margin: 0 0 2.5rem 0;
  line-height: 1.6;
}

/* ========== Form Section ========== */
.form-section {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.section-subtitle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin: 0 0 1.5rem 0;
}

/* ========== Salary Section ========== */
.salary-section {
  padding: 2rem;
  background: #F8F8F8;
  border-radius: 12px;
}

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
  padding: 1.25rem;
  background: rgba(33, 150, 243, 0.05);
  border-left: 4px solid #2196F3;
  border-radius: 8px;
}

.salary-info-box p {
  margin: 0 0 0.5rem 0;
  color: #333;
  line-height: 1.6;
}

.salary-note {
  color: #666;
  font-size: 0.9rem;
}

.salary-final {
  font-weight: 600;
  color: var(--color-purple-darkest);
  font-size: 1.05rem;
}

/* ========== Cover Letter ========== */
.cover-letter-section {
  padding: 2rem;
  background: #F8F8F8;
  border-radius: 12px;
}

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
  border: 2px solid var(--color-purple);
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

/* ========== CV Options ========== */
.cv-options {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  justify-content: center;
  margin: 2rem 0;
}

.cv-option-btn {
  flex: 1;
  max-width: 300px;
  height: auto !important;
  padding: 2rem 1.5rem !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  gap: 1rem !important;
  border-radius: 16px !important;
  transition: all 0.3s ease !important;
}

.cv-option-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}

.btn-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.btn-title {
  font-size: 1.1rem;
  font-weight: 600;
}

.btn-subtitle {
  font-size: 0.85rem;
  opacity: 0.8;
}

.option-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #E0E0E0;
  border-radius: 50%;
  flex-shrink: 0;
}

.option-divider span {
  font-size: 1rem;
  font-weight: 600;
  color: #666;
}

/* ========== Uploaded CV Card ========== */
.uploaded-cv-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: #F0FFF0;
  border: 2px solid #4CAF50;
  border-radius: 12px;
  margin-top: 1.5rem;
}

.cv-file-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
}

.file-details h4 {
  margin: 0 0 0.25rem;
  color: #333;
  font-size: 1.1rem;
}

.file-details p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.upload-date {
  color: #4CAF50 !important;
  font-weight: 500;
}

.cv-file-actions {
  display: flex;
  gap: 0.5rem;
}

/* ========== CV Summary ========== */
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

.no-content {
  color: #999;
  font-style: italic;
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
.upload-cv-modal-content {
  padding: 2rem;
}

.modal-description {
  margin: 0 0 2rem;
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #E0E0E0;
}

/* ========== Transitions ========== */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
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

  .cv-options {
    flex-direction: column;
  }

  .cv-option-btn {
    max-width: 100%;
    width: 100%;
  }

  .option-divider {
    transform: rotate(90deg);
  }

  .uploaded-cv-card {
    flex-direction: column;
    gap: 1rem;
  }

  .cv-file-actions {
    width: 100%;
    justify-content: center;
  }

  .navigation-buttons {
    flex-wrap: wrap;
  }

  .navigation-buttons .va-button {
    flex: 1;
    min-width: 120px;
  }

  .upload-cv-modal-content {
    padding: 1.5rem;
  }

  .modal-actions {
    flex-direction: column-reverse;
  }

  .modal-actions .va-button {
    width: 100%;
  }
}
</style>