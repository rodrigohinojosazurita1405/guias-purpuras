<!--
  ═══════════════════════════════════════════════════════════
  JobDetailPanel.vue - Panel Simple y Directo
  ═══════════════════════════════════════════════════════════
-->
<template>
  <div ref="detailPanel" class="job-detail-panel" v-if="listing">
    <!-- Botón cerrar (solo móvil) -->
    <button class="close-btn-mobile" @click="$emit('close')" title="Cerrar">
      <va-icon name="close" size="large" />
    </button>

    <!-- Application Modal -->
    <ApplicationModal
      v-model="showApplicationModal"
      :job="listing"
      @submit="handleApplicationSubmit"
      @saveCV="handleSaveCV"
    />

    <!-- Application Success Modal -->
    <ApplicationSuccessModal
      v-model="showSuccessModal"
      :applicationData="applicationResult"
      @search-more="handleSearchMore"
    />

    <!-- Sistema de Tabs -->
    <div class="tabs-container">
      <div class="tabs-header">
        <button
          class="tab-button"
          :class="{ active: activeTab === 'oferta' }"
          @click="activeTab = 'oferta'"
        >
          <va-icon name="work_outline" size="small" />
          Oferta Laboral
        </button>
        <button
          v-if="listing.companyProfile && !listing.companyAnonymous"
          class="tab-button"
          :class="{ active: activeTab === 'empresa' }"
          @click="activeTab = 'empresa'"
        >
          <va-icon name="business" size="small" />
          Perfil de Empresa
        </button>
      </div>

      <!-- Tab Content: Oferta Laboral -->
      <div v-show="activeTab === 'oferta'" class="tab-content">
        <!-- Header simple -->
        <div class="detail-header">
          <div class="header-info">
            <span class="publish-date">{{ publishDate }}</span>
            <div class="badges">
              <span v-if="listing.planType === 'impulso'" class="badge badge-impulso">Patrocinado</span>
              <span v-else-if="listing.planType === 'purpura'" class="badge badge-purpura">Destacado</span>
              <span v-if="listing.urgent" class="badge badge-urgent">Urgente</span>
            </div>
          </div>
          <div class="header-actions">
            <button @click="applyToJob" class="btn-apply-header" title="Postularme">
              <va-icon name="send" size="small" />
              <span class="btn-text">Postularme</span>
            </button>
            <button
              class="save-btn"
              :class="{ saved: isJobSaved }"
              @click="toggleSaveJob"
              :title="isJobSaved ? 'Guardado' : 'Guardar trabajo'"
            >
              <va-icon :name="isJobSaved ? 'bookmark' : 'bookmark_border'" size="small" />
            </button>
            <button class="share-btn" @click="shareJob" title="Compartir">
              <va-icon name="share" size="small" />
            </button>
          </div>
        </div>

        <!-- Sección con Logo + Título + Empresa -->
        <div class="title-section">
          <!-- Logo de la empresa (NO mostrar si es anónima) -->
          <div v-if="listing.companyLogo && !listing.companyAnonymous" class="company-logo-box">
            <img :src="listing.companyLogo" :alt="listing.companyName" />
          </div>
          <div v-else class="company-logo-placeholder">
            <va-icon name="business" size="large" />
          </div>

          <!-- Título y empresa -->
          <div class="title-content">
            <h1 class="job-title">{{ listing.title }}</h1>
            <div class="company-info">
              <span class="company-name">{{ listing.companyName }}</span>
              <va-icon v-if="listing.verified" name="verified" size="small" class="verified-icon" />
            </div>
          </div>
        </div>

        <div class="job-meta">
          <span class="meta-item">
            <va-icon name="place" size="small" />
            {{ listing.city }}<template v-if="listing.municipality">, {{ listing.municipality }}</template>
          </span>
          <span class="meta-item">
            <va-icon name="work" size="small" />
            {{ listing.contractType }}
          </span>
          <span class="meta-item" v-if="listing.modality">
            <va-icon name="laptop" size="small" />
            {{ listing.modality }}
          </span>
          <span class="meta-item" v-if="listing.jobCategory">
            <va-icon name="category" size="small" />
            {{ listing.jobCategory }}
          </span>
          <span class="meta-item" v-if="listing.vacancies">
            <va-icon name="groups" size="small" />
            {{ listing.vacancies }} {{ listing.vacancies === 1 ? 'vacante' : 'vacantes' }}
          </span>
          <span class="meta-item" v-if="listing.applicationDeadline || listing.expiryDate">
            <va-icon name="event" size="small" />
            Cierra: {{ formatExpiryDate(listing.applicationDeadline || listing.expiryDate) }}
          </span>
          <span class="meta-item">
            <span class="job-status-badge" :class="jobStatusClass">
              {{ jobStatusText }}
            </span>
          </span>
        </div>

        <!-- Salario destacado -->
        <div class="salary-box">
          <span class="salary-label">Salario:</span>
          <span class="salary-value">{{ formattedSalary }}</span>
        </div>

        <div class="divider"></div>

        <!-- Descripción -->
    <section class="detail-section">
      <h2 class="section-title">Descripción del puesto</h2>
      <div class="description-text" v-html="formattedDescription"></div>
    </section>

    <!-- Información adicional -->
    <section class="detail-section" v-if="listing.schedule || listing.experienceLevel">
      <h2 class="section-title">Detalles adicionales</h2>
      <div class="info-list">
        <div class="info-row" v-if="listing.schedule">
          <span class="info-label">Horario:</span>
          <span class="info-value">{{ listing.schedule }}</span>
        </div>
        <div class="info-row" v-if="listing.experienceLevel">
          <span class="info-label">Experiencia:</span>
          <span class="info-value">{{ listing.experienceLevel }}</span>
        </div>
      </div>
    </section>

    <!-- Beneficios -->
    <section class="detail-section" v-if="listing.benefits && benefitsList.length > 0">
      <h2 class="section-title">Beneficios</h2>
      <ul class="benefits-list">
        <li v-for="(benefit, index) in benefitsList" :key="index">{{ benefit }}</li>
      </ul>
    </section>

        <!-- Cómo postular (solo si es externa o email) -->
        <section class="detail-section application-section" v-if="listing.applicationType !== 'internal'">
          <h2 class="section-title">Cómo postular</h2>

          <template v-if="listing.applicationType === 'external'">
            <p class="application-note">Esta empresa recibe postulaciones en su propio enlace externo.</p>
            <a :href="listing.externalApplicationUrl" target="_blank" class="btn-external">
              <va-icon name="open_in_new" size="small" />
              Ir al enlace de la empresa
            </a>
          </template>

          <template v-if="listing.applicationType === 'email'">
            <p class="application-note">Envía tu CV al siguiente correo:</p>
            <a :href="`mailto:${listing.email}?subject=Postulación - ${listing.title}`" class="email-link">
              <va-icon name="email" size="small" />
              {{ listing.email }}
            </a>
          </template>
        </section>
      </div>

      <!-- Tab Content: Perfil de Empresa -->
      <div v-show="activeTab === 'empresa'" class="tab-content">
        <template v-if="listing.companyProfile && !listing.companyAnonymous">
          <!-- Banner de la empresa -->
          <div v-if="listing.companyProfile.banner" class="company-banner">
            <img :src="listing.companyProfile.banner" :alt="listing.companyName" />
          </div>

          <!-- Descripción de la empresa -->
          <section class="detail-section" v-if="listing.companyProfile.description">
            <h2 class="section-title">
              <va-icon name="info" size="small" />
              Sobre la empresa
            </h2>
            <p class="company-description">{{ listing.companyProfile.description }}</p>
          </section>

          <!-- Categoría -->
          <section class="detail-section" v-if="listing.companyProfile.category">
            <div class="info-row">
              <span class="info-label">Categoría:</span>
              <span class="info-value">{{ listing.companyProfile.category }}</span>
            </div>
          </section>

          <!-- Ubicación -->
          <section class="detail-section" v-if="listing.companyProfile.location || listing.companyProfile.city">
            <h2 class="section-title">
              <va-icon name="place" size="small" />
              Ubicación
            </h2>
            <p class="company-location">
              {{ listing.companyProfile.location }}
              <span v-if="listing.companyProfile.city">, {{ listing.companyProfile.city }}</span>
            </p>
          </section>

          <!-- Información de contacto -->
          <section class="detail-section">
            <h2 class="section-title">
              <va-icon name="contacts" size="small" />
              Información de contacto
            </h2>
            <div class="contact-info">
              <a
                v-if="listing.companyProfile.website"
                :href="listing.companyProfile.website"
                target="_blank"
                class="contact-link"
              >
                <va-icon name="language" size="small" />
                <span>{{ listing.companyProfile.website }}</span>
              </a>
              <a
                v-if="listing.companyProfile.contactEmail"
                :href="`mailto:${listing.companyProfile.contactEmail}`"
                class="contact-link"
              >
                <va-icon name="email" size="small" />
                <span>{{ listing.companyProfile.contactEmail }}</span>
              </a>
              <a
                v-if="listing.companyProfile.phone"
                :href="`tel:${listing.companyProfile.phone}`"
                class="contact-link"
              >
                <va-icon name="phone" size="small" />
                <span>{{ listing.companyProfile.phone }}</span>
              </a>
            </div>
          </section>
        </template>
      </div>
    </div>

    <!-- Botón postular final -->
    <div class="detail-footer">
      <button @click="applyToJob" class="btn-apply-footer">
        <va-icon name="send" size="small" />
        Postularme a esta vacante
      </button>
    </div>
  </div>
</template>

<script>
import ApplicationModal from '@/components/ProcessCV/ApplicationModal.vue'
import ApplicationSuccessModal from '@/components/Modals/ApplicationSuccessModal.vue'
import { useAuthStore } from '@/stores/useAuthStore'

export default {
  name: 'JobDetailPanel',

  components: {
    ApplicationModal,
    ApplicationSuccessModal
  },

  props: {
    listing: {
      type: Object,
      default: null
    }
  },

  emits: ['close'],

  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },

  data() {
    return {
      activeTab: 'oferta',
      showApplicationModal: false,
      showSuccessModal: false,
      applicationResult: null,
      isJobSaved: false,
      isSaving: false
    }
  },

  computed: {
    publishDate() {
      if (!this.listing) return ''
      const days = this.listing.publishedDaysAgo || 0
      if (days === 0) return 'Publicado hoy'
      if (days === 1) return 'Publicado ayer'
      return `Publicado hace ${days} días`
    },

    formattedSalary() {
      if (!this.listing || !this.listing.salary || this.listing.salary === 'A convenir') {
        return 'A convenir'
      }

      if (this.listing.salaryMin && this.listing.salaryMax) {
        return `Bs ${this.formatNumber(this.listing.salaryMin)} - ${this.formatNumber(this.listing.salaryMax)}`
      }

      if (this.listing.salaryFixed) {
        return `Bs ${this.formatNumber(this.listing.salaryFixed)}`
      }

      return this.listing.salary
    },

    formattedDescription() {
      if (!this.listing || !this.listing.description) return ''
      return this.listing.description.replace(/\n/g, '<br>')
    },

    benefitsList() {
      if (!this.listing || !this.listing.benefits) return []
      if (Array.isArray(this.listing.benefits)) return this.listing.benefits
      return this.listing.benefits.split('\n').filter(b => b.trim())
    },

    jobStatusText() {
      if (!this.listing) return ''

      // Verificar si está cerrado manualmente
      if (this.listing.status === 'closed') {
        return 'Cerrado'
      }

      // Verificar si expiró por fecha
      if (this.listing.expiryDate) {
        // Parsear como fecha local para evitar problemas de zona horaria
        const [year, month, day] = this.listing.expiryDate.split('-')
        const expiryDate = new Date(year, month - 1, day)
        const today = new Date()
        today.setHours(0, 0, 0, 0)
        expiryDate.setHours(0, 0, 0, 0)
        if (expiryDate < today) {
          return 'Cerrado'
        }
      }

      return 'Vigente'
    },

    jobStatusClass() {
      return this.jobStatusText === 'Vigente' ? 'status-active' : 'status-closed'
    }
  },

  methods: {
    formatNumber(num) {
      return new Intl.NumberFormat('es-BO').format(num)
    },

    formatExpiryDate(dateStr) {
      if (!dateStr) return ''
      // Parsear como fecha local para evitar problemas de zona horaria
      const [year, month, day] = dateStr.split('-')
      return `${day}/${month}/${year}`
    },

    async applyToJob() {
      // Validar autenticación
      if (!this.authStore.isAuthenticated) {
        this.$vaToast.init({
          message: 'Debes iniciar sesión para postular a esta oferta',
          color: 'warning',
          duration: 4000,
          position: 'top-right'
        })
        // Guardar la URL actual para redirigir después del login
        sessionStorage.setItem('redirectAfterLogin', this.$route.fullPath)
        // Redirigir a login
        this.$router.push('/login')
        return
      }

      // Validar que el usuario sea postulante (no empresa)
      if (this.authStore.user?.role === 'company') {
        this.$vaToast.init({
          message: 'Solo los postulantes pueden aplicar a ofertas. Cambia a una cuenta de postulante.',
          color: 'danger',
          duration: 4000,
          position: 'top-right'
        })
        return
      }

      // Proceder según el tipo de aplicación
      if (this.listing.applicationType === 'internal') {
        // Verificar si ya se postuló antes de abrir el modal
        const alreadyApplied = await this.checkIfAlreadyApplied()
        if (alreadyApplied) {
          this.$vaToast.init({
            message: 'Ya te has postulado a este trabajo anteriormente.',
            color: 'warning',
            duration: 5000,
            position: 'top-right'
          })
          return
        }

        this.showApplicationModal = true
      } else if (this.listing.applicationType === 'external') {
        window.open(this.listing.externalApplicationUrl, '_blank')
      } else if (this.listing.applicationType === 'email') {
        window.location.href = `mailto:${this.listing.email}?subject=Postulación - ${this.listing.title}`
      }
    },

    async checkIfAlreadyApplied() {
      try {
        const response = await fetch('/api/applications/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.authStore.accessToken}`,
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          const applications = data.applications || []

          // Verificar si ya existe una postulación para este trabajo
          const alreadyApplied = applications.some(app => app.job_id === this.listing.id)
          return alreadyApplied
        }

        return false
      } catch (error) {
        console.error('Error checking if already applied:', error)
        return false // En caso de error, permitir que intente postular
      }
    },

    async handleApplicationSubmit(applicationData) {
      try {
        // Primero guardar o crear el CV si es necesario
        let cvId = null

        if (applicationData.type === 'upload' && applicationData.uploadedFile) {
          // Subir CV como archivo
          const cvFormData = new FormData()
          cvFormData.append('file', applicationData.uploadedFile)
          cvFormData.append('name', `CV ${new Date().toLocaleDateString()}`)

          const cvResponse = await fetch('/api/cvs/save/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.authStore.accessToken}`,
              'X-CSRFToken': this.getCsrfToken()
            },
            body: cvFormData,
            credentials: 'include'
          })

          if (cvResponse.ok) {
            const cvData = await cvResponse.json()
            cvId = cvData.cv.id
          }
        } else if (applicationData.type === 'create' && applicationData.cvData) {
          // Crear CV con datos
          const cvResponse = await fetch('/api/cvs/save/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.authStore.accessToken}`,
              'Content-Type': 'application/json',
              'X-CSRFToken': this.getCsrfToken()
            },
            body: JSON.stringify({
              cv_type: 'created',
              name: `CV ${applicationData.cvData.personalInfo?.fullName || 'Profesional'}`,
              cv_data: applicationData.cvData
            }),
            credentials: 'include'
          })

          if (cvResponse.ok) {
            const cvData = await cvResponse.json()
            cvId = cvData.cv.id
          }
        } else if (applicationData.type === 'select' && applicationData.selectedCvId) {
          cvId = applicationData.selectedCvId
        }

        // Ahora enviar la postulación
        const response = await fetch(`/api/apply/${applicationData.jobId}/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.authStore.accessToken}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCsrfToken()
          },
          body: JSON.stringify({
            cv_id: cvId,
            cover_letter: applicationData.coverLetter || '',
            screening_answers: {}
          }),
          credentials: 'include'
        })

        if (!response.ok) {
          const errorData = await response.json()

          // Manejar caso específico de postulación duplicada
          if (response.status === 400 && errorData.error &&
              (errorData.error.includes('Ya te has postulado') ||
               errorData.error.includes('ya postulado') ||
               errorData.error.includes('duplicate'))) {
            throw new Error('Ya te has postulado a este trabajo anteriormente.')
          }

          throw new Error(errorData.error || errorData.detail || 'Error al enviar la postulación')
        }

        const result = await response.json()

        // Cerrar el modal de postulación
        this.showApplicationModal = false

        // Esperar a que el modal de postulación se cierre completamente
        await new Promise(resolve => setTimeout(resolve, 300))

        // Preparar datos para el modal de éxito
        this.applicationResult = {
          id: result.application.id,
          job_title: result.application.job_title,
          company: this.listing.companyName,
          applied_at: result.application.applied_at,
          status: result.application.status
        }

        // Mostrar modal de éxito
        this.showSuccessModal = true

      } catch (error) {
        console.error('Error submitting application:', error)

        // Cerrar el modal de postulación si hay error
        this.showApplicationModal = false

        // Determinar el color del mensaje según el tipo de error
        const isDuplicateError = error.message.includes('Ya te has postulado')
        const toastColor = isDuplicateError ? 'warning' : 'danger'
        const toastDuration = isDuplicateError ? 5000 : 4000

        this.$vaToast.init({
          message: error.message || 'Error al enviar la postulación. Intenta nuevamente.',
          color: toastColor,
          duration: toastDuration,
          position: 'top-right'
        })
      }
    },

    async handleSaveCV(data) {
      try {
        // Verificar que el usuario sea postulante
        if (this.authStore.user?.role !== 'applicant') {
          this.$vaToast.init({
            message: 'Solo los postulantes pueden guardar CVs',
            color: 'danger',
            duration: 3000
          })
          return
        }

        // Preparar datos para enviar al backend
        const response = await fetch('/api/cvs/save/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCsrfToken()
          },
          body: JSON.stringify({
            cv_data: data.cvData
          }),
          credentials: 'include'
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Error al guardar CV')
        }

        const result = await response.json()

        // Mostrar mensaje de éxito
        this.$vaToast.init({
          message: result.message || 'CV guardado correctamente en tu dashboard',
          color: 'success',
          duration: 3000,
          position: 'top-right'
        })

      } catch (error) {
        console.error('Error saving CV:', error)

        // Si el error es por límite de CVs (máx 2)
        if (error.message.includes('máximo') || error.message.includes('límite')) {
          this.$vaToast.init({
            message: error.message,
            color: 'warning',
            duration: 5000,
            position: 'top-right'
          })
        } else {
          this.$vaToast.init({
            message: error.message || 'Error al guardar CV. Intenta nuevamente.',
            color: 'danger',
            duration: 4000,
            position: 'top-right'
          })
        }
      }
    },

    getCsrfToken() {
      // Obtener token CSRF de las cookies
      const name = 'csrftoken'
      let cookieValue = null
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }
      return cookieValue
    },

    async toggleSaveJob() {
      // Validar autenticación
      if (!this.authStore.isAuthenticated) {
        this.$vaToast.init({
          message: 'Debes iniciar sesión para guardar trabajos',
          color: 'warning',
          duration: 3000,
          position: 'top-right'
        })
        sessionStorage.setItem('redirectAfterLogin', this.$route.fullPath)
        this.$router.push('/login')
        return
      }

      // Validar que sea postulante
      if (this.authStore.user?.role !== 'applicant') {
        this.$vaToast.init({
          message: 'Solo los postulantes pueden guardar trabajos',
          color: 'warning',
          duration: 3000,
          position: 'top-right'
        })
        return
      }

      if (this.isSaving) return

      // Verificar que tengamos un token válido
      if (!this.authStore.accessToken) {
        console.error('❌ No hay accessToken disponible')
        this.$vaToast.init({
          message: 'Sesión expirada. Por favor inicia sesión nuevamente.',
          color: 'warning',
          duration: 3000,
          position: 'top-right'
        })
        this.$router.push('/login')
        return
      }

      this.isSaving = true

      try {
        const endpoint = this.isJobSaved ? '/api/saved-jobs/unsave/' : '/api/saved-jobs/save/'
        const method = this.isJobSaved ? 'DELETE' : 'POST'

        const response = await fetch(endpoint, {
          method: method,
          headers: {
            'Authorization': `Bearer ${this.authStore.accessToken}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCsrfToken()
          },
          body: JSON.stringify({
            job_id: this.listing.id
          }),
          credentials: 'include'
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || errorData.detail || 'Error al guardar trabajo')
        }

        await response.json()

        // Toggle estado
        this.isJobSaved = !this.isJobSaved

        // Mostrar mensaje
        this.$vaToast.init({
          message: this.isJobSaved ? 'Trabajo guardado en tu dashboard' : 'Trabajo removido de guardados',
          color: 'success',
          duration: 2500,
          position: 'top-right'
        })

      } catch (error) {
        console.error('Error saving job:', error)
        this.$vaToast.init({
          message: error.message || 'Error al guardar trabajo. Intenta nuevamente.',
          color: 'danger',
          duration: 3000,
          position: 'top-right'
        })
      } finally {
        this.isSaving = false
      }
    },

    async checkIfJobSaved() {
      // Solo verificar si está autenticado y es postulante
      if (!this.authStore.isAuthenticated || this.authStore.user?.role !== 'applicant') {
        this.isJobSaved = false
        return
      }

      // Verificar que tengamos un token válido
      if (!this.authStore.accessToken) {
        this.isJobSaved = false
        return
      }

      try {
        const response = await fetch(`/api/saved-jobs/check/${this.listing.id}/`, {
          headers: {
            'Authorization': `Bearer ${this.authStore.accessToken}`
          },
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          this.isJobSaved = data.is_saved || false
        } else if (response.status === 401) {
          // Token podría haber expirado, intentar refrescar
          await this.authStore.refreshTokens()
        }
      } catch (error) {
        console.error('Error checking if job is saved:', error)
      }
    },

    shareJob() {
      if (navigator.share) {
        navigator.share({
          title: this.listing.title,
          text: `${this.listing.title} en ${this.listing.companyName}`,
          url: window.location.href
        })
      } else {
        navigator.clipboard.writeText(window.location.href)
        alert('Enlace copiado al portapapeles')
      }
    },

    handleSearchMore() {
      // Cerrar el panel de detalles y volver a la búsqueda
      this.$emit('close')
    }
  },

  mounted() {
    // Verificar si el trabajo ya está guardado cuando se monta el componente
    if (this.listing) {
      this.checkIfJobSaved()
    }
  },

  watch: {
    listing: {
      handler(newListing, oldListing) {
        if (newListing && oldListing && newListing.id !== oldListing.id) {
          this.$nextTick(() => {
            if (this.$refs.detailPanel) {
              this.$refs.detailPanel.scrollTop = 0
            }
          })
          // Verificar si el nuevo trabajo está guardado
          this.checkIfJobSaved()
        } else if (newListing && !oldListing) {
          // Primera carga
          this.checkIfJobSaved()
        }
      },
      immediate: true
    }
  }
}
</script>

<style scoped>
/* Panel principal */
.job-detail-panel {
  background: white;
  border-radius: 8px;
  padding: 0 2rem 2rem 2rem; /* Sin padding superior para alinear tabs */
  overflow-y: auto;
  max-height: calc(100vh - 2rem);
}

/* Scrollbar */
.job-detail-panel::-webkit-scrollbar {
  width: 6px;
}

.job-detail-panel::-webkit-scrollbar-track {
  background: #F3F4F6;
}

.job-detail-panel::-webkit-scrollbar-thumb {
  background: #D1D5DB;
  border-radius: 3px;
}

/* Botón cerrar móvil */
.close-btn-mobile {
  display: none;
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  width: 44px;
  height: 44px;
  cursor: pointer;
  z-index: 10;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.close-btn-mobile:hover {
  background: rgba(0, 0, 0, 0.08);
  transform: scale(1.05);
}

.close-btn-mobile:active {
  transform: scale(0.98);
}

/* Header */
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header-info {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.publish-date {
  font-size: 0.875rem;
  color: #6B7280;
}

.badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.badges {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.badge-impulso {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
  border: 1px solid rgba(16, 185, 129, 0.5);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.badge-purpura {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  color: white;
  border: 1px solid rgba(124, 58, 237, 0.5);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.badge-urgent {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  color: white;
  border: 1px solid rgba(220, 38, 38, 0.5);
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
}

.header-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-apply-header {
  background: #7C3AED;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.625rem 1.25rem;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  transition: all 0.2s;
}

.btn-apply-header:hover {
  background: #6D28D9;
  transform: translateY(-1px);
}

.save-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  border: none;
  border-radius: 6px;
  padding: 0.625rem;
  cursor: pointer;
  color: white;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
}

.save-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35);
}

.save-btn.saved {
  background: linear-gradient(135deg, #10B981, #059669);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.25);
}

.save-btn.saved:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
}

.share-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  border: none;
  border-radius: 6px;
  padding: 0.625rem;
  cursor: pointer;
  color: white;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
}

.share-btn:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35);
}

/* Sección Título con Logo */
.title-section {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

/* Logo de la empresa */
.company-logo-box {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  border: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: center;
}

.company-logo-box img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 0.5rem;
}

.company-logo-placeholder {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9CA3AF;
}

/* Contenido del título */
.title-content {
  flex: 1;
  min-width: 0;
}

/* Título */
.job-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
}

/* Empresa */
.company-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0;
}

.company-name {
  font-size: 1.125rem;
  color: #7C3AED;
  font-weight: 600;
}

.verified-icon {
  color: #3B82F6;
}

/* Meta info */
.job-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #F3F4F6;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9375rem;
  color: #1F2937;
  font-weight: 600;
  letter-spacing: 0.01em;
}

.meta-item va-icon,
.meta-item .va-icon {
  color: #7C3AED;
  font-size: 1.125rem;
}

/* Badge de estado del trabajo */
.job-status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.125rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.job-status-badge.status-active {
  background: rgba(16, 185, 129, 0.1);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.job-status-badge.status-closed {
  background: rgba(239, 68, 68, 0.1);
  color: #DC2626;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

/* Salario */
.salary-box {
  background: #F0FDF4;
  border: 1px solid #86EFAC;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.salary-label {
  font-size: 0.875rem;
  color: #166534;
  font-weight: 600;
}

.salary-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #15803D;
}

/* Divider */
.divider {
  height: 1px;
  background: #E5E7EB;
  margin: 1.5rem 0;
}

/* Secciones */
.detail-section {
  margin-bottom: 1.75rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 1rem 0;
}

/* Descripción */
.description-text {
  font-size: 0.9375rem;
  color: #374151;
  line-height: 1.7;
}

/* Info list */
.info-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-row {
  display: flex;
  gap: 0.75rem;
}

.info-label {
  font-size: 0.9375rem;
  color: #6B7280;
  font-weight: 500;
  min-width: 100px;
}

.info-value {
  font-size: 0.9375rem;
  color: #111827;
  font-weight: 600;
}

/* Beneficios */
.benefits-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.benefits-list li {
  padding-left: 1.5rem;
  margin-bottom: 0.5rem;
  position: relative;
  font-size: 0.9375rem;
  color: #374151;
  line-height: 1.6;
}

.benefits-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #10B981;
  font-weight: 700;
}

/* Aplicación externa */
.application-section {
  background: #F9FAFB;
  padding: 1.25rem;
  border-radius: 8px;
}

.application-note {
  font-size: 0.9375rem;
  color: #4B5563;
  margin: 0 0 1rem 0;
}

.btn-external {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  color: #7C3AED;
  border: 1px solid #7C3AED;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 0.9375rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-external:hover {
  background: #7C3AED;
  color: white;
}

.email-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #7C3AED;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
}

.email-link:hover {
  text-decoration: underline;
}

/* Sistema de Tabs */
.tabs-container {
  margin-top: 0;
  margin-bottom: 0;
  padding-top: 1.5rem; /* Pequeño padding para no quedar al ras del borde */
}

.tabs-header {
  display: flex;
  gap: 0.5rem;
  border-bottom: 2px solid #E5E7EB;
  margin-bottom: 1.5rem;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.25rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.tab-button:hover {
  color: #7C3AED;
  background: #F9FAFB;
}

.tab-button.active {
  color: #7C3AED;
  border-bottom-color: #7C3AED;
}

.tab-content {
  animation: fadeIn 0.3s ease-out;
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

/* Tab Empresa - Banner */
.company-banner {
  width: 100%;
  height: 180px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
}

.company-banner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.company-description,
.company-location {
  font-size: 0.9375rem;
  color: #4B5563;
  line-height: 1.7;
  margin: 0;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.contact-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  color: #111827;
  text-decoration: none;
  transition: all 0.2s;
  font-size: 0.9375rem;
}

.contact-link:hover {
  background: #F3F4F6;
  border-color: #7C3AED;
}

.contact-link va-icon {
  color: #7C3AED;
  flex-shrink: 0;
}

/* Footer */
.detail-footer {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E5E7EB;
}

.btn-apply-footer {
  width: 100%;
  background: #7C3AED;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.btn-apply-footer:hover {
  background: #6D28D9;
  transform: translateY(-1px);
}

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 400px;
  text-align: center;
  padding: 2rem;
}

.empty-state h3 {
  font-size: 1.25rem;
  color: #6B7280;
  margin: 1rem 0 0.5rem 0;
}

.empty-state p {
  color: #9CA3AF;
  font-size: 0.9375rem;
}

/* Responsive */
@media (max-width: 1024px) {
  .job-detail-panel {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    max-height: 100vh;
    border-radius: 0;
    z-index: 1001;
    padding: 4.5rem 1.5rem 1.5rem; /* Más espacio arriba para el botón X */
    box-shadow: 0 0 50px rgba(0, 0, 0, 0.3);
  }

  .close-btn-mobile {
    display: flex;
    z-index: 1002;
    top: 1.25rem; /* Más separación desde arriba */
    right: 1.25rem; /* Más separación desde la derecha */
  }

  .job-title {
    font-size: 1.5rem;
  }

  /* Ajustar el header para que no choque con el botón X */
  .detail-header {
    padding-right: 2.5rem; /* Espacio para el botón X */
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .header-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  /* Badges en línea horizontal */
  .badges {
    display: flex;
    flex-direction: row;
    gap: 0.375rem;
    flex-wrap: nowrap;
  }

  .badge {
    font-size: 0.6875rem;
    padding: 0.1875rem 0.5rem;
  }

  /* Mejorar botones en móvil */
  .header-actions {
    gap: 0.375rem;
  }

  /* Ocultar texto del botón, solo mostrar ícono */
  .btn-apply-header .btn-text {
    display: none !important;
  }

  .btn-apply-header {
    padding: 0.5rem !important;
    min-width: 40px;
    min-height: 40px;
    justify-content: center;
  }

  .save-btn,
  .share-btn {
    padding: 0.5rem;
    min-width: 40px;
    min-height: 40px;
  }
}

@media (max-width: 768px) {
  /* Asegurar que el texto se oculte en tablets también */
  .btn-apply-header .btn-text {
    display: none !important;
  }

  .btn-apply-header {
    padding: 0.5rem !important;
  }
}

@media (max-width: 480px) {
  .header-actions {
    gap: 0.25rem;
  }

  .btn-apply-header .btn-text {
    display: none !important;
  }

  .btn-apply-header,
  .save-btn,
  .share-btn {
    min-width: 36px;
    min-height: 36px;
    padding: 0.4375rem !important;
  }

  .badge {
    font-size: 0.625rem;
    padding: 0.125rem 0.375rem;
  }
}

@media (max-width: 375px) {
  /* iPhone 5/SE y dispositivos muy pequeños */
  .btn-apply-header .btn-text {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
  }

  .btn-apply-header,
  .save-btn,
  .share-btn {
    min-width: 34px;
    min-height: 34px;
    max-width: 34px;
    padding: 0.375rem !important;
  }

  .header-actions {
    gap: 0.1875rem;
  }

  .badge {
    font-size: 0.5625rem;
    padding: 0.125rem 0.25rem;
  }
}
</style>
