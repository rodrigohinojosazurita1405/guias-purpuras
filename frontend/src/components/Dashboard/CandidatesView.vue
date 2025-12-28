<!-- frontend/src/components/Dashboard/CandidatesView.vue -->
<template>
  <div class="candidates-view">
    <!-- Header -->
    <div class="section-header">
      <h2>Base de Talento</h2>
      <p class="section-subtitle">Gestiona todos los candidatos de tus publicaciones</p>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid" v-if="!applicationMgr.isLoading">
      <div class="stat-card">
        <div class="stat-icon total">
          <va-icon name="people" />
        </div>
        <div class="stat-content">
          <h3>Total de Candidatos</h3>
          <div class="stat-number">{{ applicationMgr.totalApplications }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon received">
          <va-icon name="mail" />
        </div>
        <div class="stat-content">
          <h3>Recibidas</h3>
          <div class="stat-number">{{ applicationMgr.receivedCount }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon reviewing">
          <va-icon name="visibility" />
        </div>
        <div class="stat-content">
          <h3>En Revisión</h3>
          <div class="stat-number">{{ applicationMgr.reviewingCount }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon shortlisted">
          <va-icon name="check_circle" />
        </div>
        <div class="stat-content">
          <h3>Preseleccionados</h3>
          <div class="stat-number">{{ applicationMgr.shortlistedCount }}</div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <div class="search-box">
        <va-icon name="search" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar candidato o trabajo..."
          class="search-input"
        />
      </div>

      <select v-model="filterStatus" class="filter-select">
        <option value="">Todos los estados</option>
        <option value="submitted">Recibida</option>
        <option value="reviewing">En revisión</option>
        <option value="shortlisted">Preseleccionado</option>
        <option value="interviewed">Entrevistado</option>
        <option value="accepted">Aceptado</option>
        <option value="rejected">Rechazado</option>
      </select>

      <select v-model="filterDate" class="filter-select">
        <option value="">Todas las fechas</option>
        <option value="week">Última semana</option>
        <option value="month">Último mes</option>
        <option value="3months">Últimos 3 meses</option>
        <option value="6months">Últimos 6 meses</option>
      </select>

      <select v-model="filterRating" class="filter-select">
        <option value="">Todas las calificaciones</option>
        <option value="with-rating">Solo con calificación</option>
        <option value="no-rating">Sin calificar</option>
        <option value="3+">3+ estrellas</option>
        <option value="4+">4+ estrellas</option>
        <option value="5">5 estrellas</option>
      </select>

      <select v-model="sortBy" class="filter-select">
        <option value="date-desc">Aplicaciones recientes primero</option>
        <option value="date-asc">Aplicaciones antiguas primero</option>
        <option value="rating-desc">Mejor calificados primero (5→1)</option>
        <option value="rating-asc">Menor calificados primero (1→5)</option>
        <option value="name-asc">Nombre A→Z</option>
        <option value="name-desc">Nombre Z→A</option>
      </select>
    </div>

    <!-- Results Counter -->
    <div v-if="localIsReady && totalApplicationsCount > 0" class="results-counter">
      <span class="counter-text">
        Mostrando <strong>{{ filteredApplicationsCount }}</strong> de <strong>{{ totalApplicationsCount }}</strong> candidatos
      </span>
      <div class="counter-actions">
        <!-- Dropdown de Exportación -->
        <div class="export-dropdown" @click.stop>
          <button
            @click.stop="toggleExportMenu"
            class="export-btn"
            :disabled="filteredApplicationsCount === 0"
          >
            <va-icon name="download" size="small" />
            Exportar
            <va-icon :name="showExportMenu ? 'expand_less' : 'expand_more'" size="small" />
          </button>

          <transition name="dropdown-fade">
            <div v-if="showExportMenu" class="export-menu" @click.stop>
              <button @click="exportAllToCSV" class="export-menu-item">
                <va-icon name="file_download" size="small" />
                <div class="menu-item-content">
                  <span class="menu-item-title">Exportar Todo</span>
                  <span class="menu-item-desc">Todos los candidatos filtrados en un archivo</span>
                </div>
              </button>

              <div class="menu-divider"></div>

              <button @click="toggleBulkExportMode" class="export-menu-item">
                <va-icon name="checklist" size="small" />
                <div class="menu-item-content">
                  <span class="menu-item-title">Seleccionar Anuncios</span>
                  <span class="menu-item-desc">Exportar múltiples trabajos por separado</span>
                </div>
              </button>

              <button @click="exportAllJobsSeparately" class="export-menu-item">
                <va-icon name="folder_zip" size="small" />
                <div class="menu-item-content">
                  <span class="menu-item-title">Exportar Todos por Separado</span>
                  <span class="menu-item-desc">Cada trabajo en su propio archivo</span>
                </div>
              </button>
            </div>
          </transition>
        </div>

        <button
          v-if="hasActiveFilters"
          @click="clearAllFilters"
          class="clear-filters-btn"
        >
          <va-icon name="clear" size="small" />
          Limpiar filtros
        </button>
      </div>
    </div>

    <!-- Bulk Actions Toolbar -->
    <transition name="slide-down">
      <div v-if="selectedApplications.size > 0" class="bulk-actions-toolbar">
        <div class="bulk-info">
          <va-icon name="check_circle" color="#10B981" />
          <span class="bulk-count">
            <strong>{{ selectedApplications.size }}</strong>
            {{ selectedApplications.size === 1 ? 'candidato seleccionado' : 'candidatos seleccionados' }}
          </span>
        </div>

        <div class="bulk-actions">
          <!-- Cambiar Estado -->
          <div class="bulk-action-group">
            <span class="bulk-action-label">Cambiar estado a:</span>
            <div class="bulk-status-buttons">
              <button
                v-for="status in bulkStatusOptions"
                :key="status.value"
                @click="bulkChangeStatus(status.value)"
                class="bulk-status-btn"
                :class="`status-${status.value}`"
                :title="`Cambiar ${selectedApplications.size} candidatos a ${status.label}`"
              >
                <va-icon :name="status.icon" size="small" />
                {{ status.label }}
              </button>
            </div>
          </div>

          <!-- Acciones Rápidas -->
          <div class="bulk-quick-actions">
            <button
              @click="clearSelection"
              class="bulk-clear-btn"
            >
              <va-icon name="close" size="small" />
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Bulk Export Toolbar -->
    <transition name="slide-down">
      <div v-if="bulkExportMode" class="bulk-export-toolbar">
        <div class="bulk-info">
          <va-icon name="checklist" color="#7C3AED" />
          <span class="bulk-count">
            <strong>{{ selectedJobs.size }}</strong>
            {{ selectedJobs.size === 1 ? 'anuncio seleccionado' : 'anuncios seleccionados' }}
          </span>
        </div>

        <div class="bulk-actions">
          <button
            @click="exportSelectedJobs"
            class="export-selected-btn"
            :disabled="selectedJobs.size === 0"
          >
            <va-icon name="file_download" size="small" />
            Exportar Seleccionados
          </button>

          <button @click="cancelBulkExport" class="bulk-clear-btn">
            <va-icon name="close" size="small" />
            Cancelar
          </button>
        </div>
      </div>
    </transition>

    <!-- Modal de Confirmación de Acción en Lote -->
    <va-modal
      v-model="showBulkConfirmModal"
      size="small"
      :hide-default-actions="true"
      blur
    >
      <template #header>
        <h2 class="modal-title">
          <va-icon name="warning" color="warning" size="1.5rem" />
          Confirmar Acción en Lote
        </h2>
      </template>

      <div class="modal-content" v-if="pendingBulkAction">
        <p class="modal-message">
          ¿Estás seguro de cambiar el estado de
          <strong>{{ pendingBulkAction.count }}</strong>
          {{ pendingBulkAction.count === 1 ? 'candidato' : 'candidatos' }}
          a <strong class="status-highlight">"{{ pendingBulkAction.label }}"</strong>?
        </p>
        <p class="modal-warning">
          Se actualizarán {{ pendingBulkAction.count }} {{ pendingBulkAction.count === 1 ? 'candidato' : 'candidatos' }} a la vez.
        </p>
      </div>

      <template #footer>
        <div class="modal-actions">
          <va-button
            color="secondary"
            @click="cancelBulkAction"
            class="modal-btn-cancel"
          >
            Cancelar
          </va-button>
          <va-button
            color="primary"
            @click="confirmBulkAction"
            class="modal-btn-confirm"
          >
            <va-icon name="check" size="small" />
            Confirmar
          </va-button>
        </div>
      </template>
    </va-modal>

    <!-- Loading State -->
    <div v-if="!localIsReady" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
      <p>Cargando candidatos...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="applicationMgr.error" class="error-state">
      <va-icon name="error" size="3rem" color="danger" />
      <p>{{ applicationMgr.error }}</p>
      <button @click="resetAndLoad()" class="retry-btn">
        <va-icon name="refresh" />
        Reintentar
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="localIsReady && displayApplications.length === 0" class="empty-state">
      <va-icon name="person_add" size="3rem" />
      <h3>No hay candidatos registrados</h3>
      <p>Los candidatos aparecerán aquí cuando postulen a tus publicaciones</p>
      <p style="font-size: 0.9rem; color: #9CA3AF; margin-top: 1rem;">
        💡 Tip: Publica un anuncio de trabajo para empezar a recibir candidatos
      </p>
    </div>

    <!-- Applications List Grouped by Job -->
    <div v-else-if="localIsReady && groupedApplications.length > 0" class="applications-list">
      <!-- Job Group -->
      <div
        v-for="jobGroup in groupedApplications"
        :key="jobGroup.jobId"
        class="job-group"
      >
        <!-- Job Group Header -->
        <div class="job-group-header">
          <!-- Checkbox para modo de exportación en lote -->
          <div v-if="bulkExportMode" class="job-export-checkbox" @click.stop>
            <input
              type="checkbox"
              :checked="selectedJobs.has(jobGroup.jobId)"
              @change="toggleJobSelection(jobGroup.jobId)"
              class="custom-checkbox"
              :title="`Seleccionar ${jobGroup.jobTitle}`"
            />
          </div>

          <div class="job-group-info" @click="toggleJobGroup(jobGroup.jobId)">
            <va-icon
              :name="isJobExpanded(jobGroup.jobId) ? 'expand_less' : 'expand_more'"
              class="expand-icon"
            />
            <div class="job-group-title">
              <h3>{{ jobGroup.jobTitle }}</h3>
              <span class="applications-count">
                {{ jobGroup.applications.length }}
                {{ jobGroup.applications.length === 1 ? 'solicitud' : 'solicitudes' }}
              </span>
            </div>
          </div>
          <div class="job-group-actions">
            <button
              @click.stop="exportJobToCSV(jobGroup)"
              class="export-job-btn"
              v-tooltip="'Exportar candidatos de este anuncio'"
            >
              <va-icon name="download" size="small" />
            </button>
            <div class="job-group-stats">
              <span
                v-for="status in statusOptions"
                :key="status"
                class="mini-stat"
                :class="`status-${status}`"
                v-show="getStatusCount(jobGroup.applications, status) > 0"
              >
                {{ getStatusCount(jobGroup.applications, status) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Applications in this Job -->
        <div v-show="isJobExpanded(jobGroup.jobId)" class="job-group-applications">
          <div
            v-for="application in jobGroup.applications"
            :key="application.id"
            class="application-card"
            :class="{
              [`status-${application.status}`]: true,
              'is-selected': selectedApplications.has(application.id)
            }"
          >
        <!-- Card Header -->
        <div class="card-header">
          <!-- Checkbox de selección -->
          <div class="selection-checkbox">
            <input
              type="checkbox"
              :checked="selectedApplications.has(application.id)"
              @change="toggleSelection(application.id)"
              class="custom-checkbox"
              :title="`Seleccionar candidato ${application.applicantName}`"
            />
          </div>

          <div class="applicant-info">
            <div class="applicant-avatar">
              {{ getInitials(application.applicantName) }}
            </div>
            <div class="applicant-details">
              <h3 class="applicant-name">{{ application.applicantName }}</h3>
              <p class="applicant-email">{{ application.applicantEmail }}</p>
              <div class="applicant-meta">
                <span class="application-date">
                  Aplicó {{ formatRelativeDate(application.createdAt) }}
                </span>
                <StarRating
                  :model-value="application.rating"
                  @update:model-value="(rating) => updateRating(application, rating)"
                  :show-label="false"
                />
              </div>
            </div>
          </div>

          <div class="card-actions">
            <div class="status-badge" :class="`status-${application.status}`">
              {{ getStatusLabel(application.status) }}
            </div>
            <button
              @click="toggleExpanded(application.id)"
              class="expand-btn"
            >
              <va-icon :name="expandedId === application.id ? 'expand_less' : 'expand_more'" />
            </button>
          </div>
        </div>

        <!-- Card Body (Expandable) -->
        <div v-if="expandedId === application.id" class="card-body">
          <!-- CV Enviado -->
          <div class="section" v-if="application.cv">
            <h4 class="section-title">
              <va-icon name="description" size="small" />
              CV Enviado
            </h4>
            <div class="cv-info">
              <div class="cv-type-badge">
                {{ application.cv.type === 'file' ? 'PDF Subido' : 'CV de Plataforma' }}
              </div>
              <div class="cv-details">
                <p class="cv-name">{{ application.cv.file_name || application.cv.full_name || 'CV sin nombre' }}</p>
                <p class="cv-date">Enviado {{ formatRelativeDate(application.createdAt) }}</p>
              </div>
              <button
                v-if="application.cv.file_url"
                @click="downloadCV(application.cv.file_url)"
                class="btn-download"
              >
                <va-icon name="download" size="small" />
                Descargar
              </button>
            </div>
          </div>

          <!-- Carta de Presentación -->
          <div class="section" v-if="application.coverLetter">
            <h4 class="section-title">
              <va-icon name="mail" size="small" />
              Carta de Presentación
            </h4>
            <div class="cover-letter-content">
              {{ application.coverLetter }}
            </div>
          </div>

          <!-- Contact Information -->
          <div class="section">
            <h4 class="section-title">
              <va-icon name="contacts" size="small" />
              Información de Contacto
            </h4>
            <div class="contact-grid">
              <div class="contact-item">
                <span class="contact-label">Email:</span>
                <a :href="`mailto:${application.applicantEmail}`" class="contact-link">
                  {{ application.applicantEmail }}
                </a>
              </div>
              <div v-if="application.applicantWhatsapp" class="contact-item">
                <span class="contact-label">WhatsApp:</span>
                <span class="contact-value">{{ application.applicantWhatsapp }}</span>
              </div>
            </div>

            <!-- Botones de contacto -->
            <div class="contact-actions">
              <a
                v-if="application.applicantWhatsapp"
                :href="getWhatsAppLink(application.applicantWhatsapp, application.applicantName)"
                target="_blank"
                class="contact-btn whatsapp-btn"
              >
                <va-icon name="chat" size="small" />
                WhatsApp
              </a>

              <a
                :href="`mailto:${application.applicantEmail}?subject=Postulación - ${application.applicantName}`"
                class="contact-btn email-btn"
              >
                <va-icon name="email" size="small" />
                Enviar Email
              </a>
            </div>
          </div>

          <!-- Candidate Profile (si el CV tiene datos del perfil) -->
          <div class="section" v-if="application.cv && application.cv.cv_data">
            <h4 class="section-title">
              <va-icon name="person" size="small" />
              Perfil del Candidato
            </h4>
            <div class="candidate-profile">
              <!-- Información Personal -->
              <div class="profile-section" v-if="application.cv.cv_data.personalInfo">
                <h5 class="profile-subtitle">Información Personal</h5>
                <div class="profile-grid">
                  <div v-if="application.cv.cv_data.personalInfo.fullName" class="profile-item">
                    <span class="profile-label">Nombre Completo:</span>
                    <span class="profile-value">{{ application.cv.cv_data.personalInfo.fullName }}</span>
                  </div>
                  <div v-if="application.cv.cv_data.personalInfo.phone" class="profile-item">
                    <span class="profile-label">Teléfono:</span>
                    <span class="profile-value">{{ application.cv.cv_data.personalInfo.phone }}</span>
                  </div>
                  <div v-if="application.cv.cv_data.personalInfo.address" class="profile-item">
                    <span class="profile-label">Dirección:</span>
                    <span class="profile-value">{{ application.cv.cv_data.personalInfo.address }}</span>
                  </div>
                  <div v-if="application.cv.cv_data.personalInfo.city" class="profile-item">
                    <span class="profile-label">Ciudad:</span>
                    <span class="profile-value">{{ application.cv.cv_data.personalInfo.city }}</span>
                  </div>
                </div>
              </div>

              <!-- Perfil Profesional -->
              <div class="profile-section" v-if="application.cv.cv_data.professionalProfile">
                <h5 class="profile-subtitle">Perfil Profesional</h5>
                <p class="profile-description">{{ application.cv.cv_data.professionalProfile }}</p>
              </div>

              <!-- Experiencia Laboral -->
              <div class="profile-section" v-if="application.cv.cv_data.workExperience && application.cv.cv_data.workExperience.length > 0">
                <h5 class="profile-subtitle">Experiencia Laboral</h5>
                <div v-for="(exp, index) in application.cv.cv_data.workExperience" :key="index" class="experience-item">
                  <div class="experience-header">
                    <strong>{{ exp.position }}</strong>
                    <span v-if="exp.company"> - {{ exp.company }}</span>
                  </div>
                  <div class="experience-dates" v-if="exp.startDate">
                    {{ exp.startDate }} - {{ exp.endDate || 'Actualidad' }}
                  </div>
                  <p v-if="exp.description" class="experience-description">{{ exp.description }}</p>
                </div>
              </div>

              <!-- Educación -->
              <div class="profile-section" v-if="application.cv.cv_data.education && application.cv.cv_data.education.length > 0">
                <h5 class="profile-subtitle">Educación</h5>
                <div v-for="(edu, index) in application.cv.cv_data.education" :key="index" class="education-item">
                  <div class="education-header">
                    <strong>{{ edu.degree }}</strong>
                    <span v-if="edu.institution"> - {{ edu.institution }}</span>
                  </div>
                  <div class="education-dates" v-if="edu.startDate">
                    {{ edu.startDate }} - {{ edu.endDate || 'En curso' }}
                  </div>
                </div>
              </div>

              <!-- Habilidades -->
              <div class="profile-section" v-if="application.cv.cv_data.skills && application.cv.cv_data.skills.length > 0">
                <h5 class="profile-subtitle">Habilidades</h5>
                <div class="skills-list">
                  <span v-for="(skill, index) in application.cv.cv_data.skills" :key="index" class="skill-tag">
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Change Status -->
          <div class="section status-section">
            <h4 class="section-title">
              <va-icon name="swap_horiz" size="small" />
              Cambiar Estado
            </h4>

            <div class="status-buttons-compact">
              <button
                @click="changeStatus(application, 'submitted')"
                class="status-pill"
                :class="{ active: application.status === 'submitted' }"
                :disabled="updating"
              >
                <va-icon name="mail" size="small" />
                <span>Recibida</span>
              </button>
              <button
                @click="changeStatus(application, 'reviewing')"
                class="status-pill status-reviewing"
                :class="{ active: application.status === 'reviewing' }"
                :disabled="updating"
              >
                <va-icon name="visibility" size="small" />
                <span>En Revisión</span>
              </button>
              <button
                @click="changeStatus(application, 'shortlisted')"
                class="status-pill status-shortlisted"
                :class="{ active: application.status === 'shortlisted' }"
                :disabled="updating"
              >
                <va-icon name="star" size="small" />
                <span>Preseleccionado</span>
              </button>
              <button
                @click="changeStatus(application, 'interviewed')"
                class="status-pill status-interviewed"
                :class="{ active: application.status === 'interviewed' }"
                :disabled="updating"
              >
                <va-icon name="person" size="small" />
                <span>Entrevistado</span>
              </button>
              <button
                @click="changeStatus(application, 'accepted')"
                class="status-pill status-accepted"
                :class="{ active: application.status === 'accepted' }"
                :disabled="updating"
              >
                <va-icon name="check_circle" size="small" />
                <span>Aceptado</span>
              </button>
              <button
                @click="changeStatus(application, 'rejected')"
                class="status-pill status-rejected"
                :class="{ active: application.status === 'rejected' }"
                :disabled="updating"
              >
                <va-icon name="cancel" size="small" />
                <span>Rechazado</span>
              </button>
            </div>
          </div>

          <!-- Notes -->
          <div class="section">
            <h4 class="section-title">
              <va-icon name="note" size="small" />
              Notas del Reclutador
            </h4>
            <textarea
              v-model="application.recruiterNotes"
              @blur="saveNotes(application)"
              placeholder="Añade tus notas sobre este candidato..."
              class="notes-textarea"
              :disabled="updating"
            ></textarea>
          </div>
        </div>
      </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useToast } from 'vuestic-ui'
import { useApplications } from '@/composables/useApplications'
import StarRating from '@/components/Dashboard/StarRating.vue'

// ========== COMPOSABLES ==========
const { init: notify } = useToast()
const applicationMgr = useApplications()

// ========== DATA ==========
const searchQuery = ref('')
const filterStatus = ref('')
const filterDate = ref('')
const filterRating = ref('')
const sortBy = ref('date-desc')  // Por defecto: más recientes primero
const expandedId = ref(null)
const expandedJobIds = ref(new Set())  // IDs de trabajos expandidos
const updating = ref(false)
const localIsReady = ref(false)  // Variable local para forzar re-render

// Bulk Actions
const selectedApplications = ref(new Set())  // IDs de aplicaciones seleccionadas

// Export dropdown state
const showExportMenu = ref(false)
const bulkExportMode = ref(false)
const selectedJobs = ref(new Set())

// Bulk action confirmation modal
const showBulkConfirmModal = ref(false)
const pendingBulkAction = ref(null)

const statusOptions = ['submitted', 'reviewing', 'shortlisted', 'interviewed', 'accepted', 'rejected']

// Opciones de estado para acciones en lote (con íconos)
const bulkStatusOptions = [
  { value: 'reviewing', label: 'En Revisión', icon: 'visibility' },
  { value: 'shortlisted', label: 'Preseleccionar', icon: 'star' },
  { value: 'interviewed', label: 'Entrevistado', icon: 'person' },
  { value: 'accepted', label: 'Aceptar', icon: 'check_circle' },
  { value: 'rejected', label: 'Rechazar', icon: 'cancel' }
]

// ========== COMPUTED ==========
const displayApplications = computed(() => {
  const rawApps = applicationMgr.applications.value

  if (!rawApps || rawApps.length === 0) {
    return []
  }

  let result = [...rawApps]

  // Filter by status
  if (filterStatus.value) {
    result = result.filter(app => app.status === filterStatus.value)
  }

  // Filter by date
  if (filterDate.value) {
    const now = new Date()
    const cutoffDate = new Date()

    switch (filterDate.value) {
      case 'week':
        cutoffDate.setDate(now.getDate() - 7)
        break
      case 'month':
        cutoffDate.setMonth(now.getMonth() - 1)
        break
      case '3months':
        cutoffDate.setMonth(now.getMonth() - 3)
        break
      case '6months':
        cutoffDate.setMonth(now.getMonth() - 6)
        break
    }

    result = result.filter(app => {
      const appDate = new Date(app.createdAt)
      return appDate >= cutoffDate
    })
  }

  // Filter by rating
  if (filterRating.value) {
    switch (filterRating.value) {
      case 'with-rating':
        result = result.filter(app => app.rating !== null && app.rating > 0)
        break
      case 'no-rating':
        result = result.filter(app => !app.rating || app.rating === 0)
        break
      case '3+':
        result = result.filter(app => app.rating >= 3)
        break
      case '4+':
        result = result.filter(app => app.rating >= 4)
        break
      case '5':
        result = result.filter(app => app.rating === 5)
        break
    }
  }

  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(app =>
      (app.applicantName || '').toLowerCase().includes(query) ||
      (app.applicantEmail || '').toLowerCase().includes(query) ||
      (app.jobTitle || '').toLowerCase().includes(query)
    )
  }

  return result
})

// Agrupar solicitudes por trabajo
const groupedApplications = computed(() => {
  const apps = displayApplications.value

  if (!apps || apps.length === 0) {
    return []
  }

  // Agrupar por jobId
  const grouped = {}

  apps.forEach(app => {
    const jobId = app.jobId
    if (!grouped[jobId]) {
      grouped[jobId] = {
        jobId: jobId,
        jobTitle: app.jobTitle,
        applications: []
      }
    }
    grouped[jobId].applications.push(app)
  })

  // Ordenar las aplicaciones dentro de cada grupo según el criterio seleccionado
  Object.values(grouped).forEach(group => {
    group.applications.sort((a, b) => {
      switch (sortBy.value) {
        case 'date-desc':
          // Más recientes primero
          return new Date(b.createdAt) - new Date(a.createdAt)

        case 'date-asc':
          // Más antiguos primero
          return new Date(a.createdAt) - new Date(b.createdAt)

        case 'rating-desc':
          // Mejor calificados primero (5→1), sin rating al final
          const ratingA = a.rating || 0
          const ratingB = b.rating || 0
          return ratingB - ratingA

        case 'rating-asc':
          // Menor calificados primero (1→5), sin rating al inicio
          const ratingA2 = a.rating || 0
          const ratingB2 = b.rating || 0
          // Si ambos tienen rating, ordenar ascendente
          if (ratingA2 > 0 && ratingB2 > 0) {
            return ratingA2 - ratingB2
          }
          // Los que no tienen rating van primero
          if (ratingA2 === 0 && ratingB2 > 0) return -1
          if (ratingA2 > 0 && ratingB2 === 0) return 1
          return 0

        case 'name-asc':
          // Nombre A→Z
          return a.applicantName.localeCompare(b.applicantName)

        case 'name-desc':
          // Nombre Z→A
          return b.applicantName.localeCompare(a.applicantName)

        default:
          // Por defecto: más recientes primero
          return new Date(b.createdAt) - new Date(a.createdAt)
      }
    })
  })

  // Convertir a array y ordenar por número de solicitudes (descendente)
  return Object.values(grouped).sort((a, b) => b.applications.length - a.applications.length)
})

// Contador de aplicaciones totales
const totalApplicationsCount = computed(() => {
  const rawApps = applicationMgr.applications.value
  return rawApps ? rawApps.length : 0
})

// Contador de aplicaciones filtradas
const filteredApplicationsCount = computed(() => {
  return displayApplications.value.length
})

// Verificar si hay filtros activos
const hasActiveFilters = computed(() => {
  return !!(searchQuery.value || filterStatus.value || filterDate.value || filterRating.value)
})

// ========== WATCHERS ==========
watch(
  () => applicationMgr.applications.value,
  () => {
    // Force reactivity update
  },
  { deep: true, immediate: true }
)

// ========== LIFECYCLE ==========
onMounted(async () => {
  // Limpiar error anterior antes de cargar
  applicationMgr.error = null

  try {
    await applicationMgr.loadApplications()

    // Forzar acceso al computed para establecer dependencia reactiva
    displayApplications.value.length

    await nextTick()

    localIsReady.value = true
  } catch (error) {
    localIsReady.value = true
  }

  // Click outside handler para cerrar el dropdown de exportación
  document.addEventListener('click', (e) => {
    const exportDropdown = document.querySelector('.export-dropdown')
    if (exportDropdown && !exportDropdown.contains(e.target)) {
      showExportMenu.value = false
    }
  })
})

// ========== METHODS ==========
const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getWhatsAppLink = (phone, candidateName) => {
  // Limpiar el número de teléfono (quitar espacios, guiones, paréntesis)
  const cleanPhone = phone.replace(/[\s\-\(\)]/g, '')

  // Mensaje personalizado para el candidato
  const message = `Hola ${candidateName}, te contacto desde Guías Púrpuras respecto a tu postulación.`

  // Codificar el mensaje para URL
  const encodedMessage = encodeURIComponent(message)

  // Retornar enlace de WhatsApp
  return `https://wa.me/${cleanPhone}?text=${encodedMessage}`
}

const formatRelativeDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffMinutes = Math.floor(diffMs / (1000 * 60))

  if (diffMinutes < 1) return 'hace unos segundos'
  if (diffMinutes < 60) return `hace ${diffMinutes} minutos`
  if (diffHours < 24) return `hace ${diffHours} horas`
  if (diffDays < 30) return `hace ${diffDays} días`

  return date.toLocaleDateString('es-ES')
}

const getStatusLabel = (status) => {
  const labels = {
    submitted: 'Recibida',
    reviewing: 'En revisión',
    shortlisted: 'Preseleccionado',
    interviewed: 'Entrevistado',
    accepted: 'Aceptado',
    rejected: 'Rechazado',
    withdrawn: 'Retirada'
  }
  return labels[status] || status
}

const toggleExpanded = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

const toggleJobGroup = (jobId) => {
  if (expandedJobIds.value.has(jobId)) {
    expandedJobIds.value.delete(jobId)
  } else {
    expandedJobIds.value.add(jobId)
  }
  // Force reactivity
  expandedJobIds.value = new Set(expandedJobIds.value)
}

const isJobExpanded = (jobId) => {
  return expandedJobIds.value.has(jobId)
}

const getStatusCount = (applications, status) => {
  return applications.filter(app => app.status === status).length
}

const changeStatus = async (application, newStatus) => {
  try {
    updating.value = true
    await applicationMgr.updateApplicationStatus(
      application.jobId,
      application.id,
      newStatus
    )

    notify({
      message: `✅ Estado actualizado a ${getStatusLabel(newStatus)}`,
      color: 'success',
      duration: 3000
    })
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    updating.value = false
  }
}

const updateRating = async (application, rating) => {
  try {
    updating.value = true
    await applicationMgr.updateApplicationRating(
      application.jobId,
      application.id,
      rating
    )

    notify({
      message: rating ? `✅ Calificación actualizada: ${rating}/5` : '✅ Calificación eliminada',
      color: 'success',
      duration: 2000
    })
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    updating.value = false
  }
}

const clearAllFilters = () => {
  searchQuery.value = ''
  filterStatus.value = ''
  filterDate.value = ''
  filterRating.value = ''

  notify({
    message: 'Filtros limpiados',
    color: 'info',
    duration: 2000
  })
}

// ========== EXPORT DROPDOWN FUNCTIONS ==========
const toggleExportMenu = () => {
  showExportMenu.value = !showExportMenu.value
}

const exportAllToCSV = () => {
  showExportMenu.value = false
  exportToCSV()
}

const toggleBulkExportMode = () => {
  showExportMenu.value = false
  bulkExportMode.value = !bulkExportMode.value

  if (bulkExportMode.value) {
    notify({
      message: '📋 Modo de selección activado. Marca los anuncios que deseas exportar.',
      color: 'info',
      duration: 4000
    })
  } else {
    selectedJobs.value = new Set()
  }
}

const toggleJobSelection = (jobId) => {
  if (selectedJobs.value.has(jobId)) {
    selectedJobs.value.delete(jobId)
  } else {
    selectedJobs.value.add(jobId)
  }
  // Force reactivity
  selectedJobs.value = new Set(selectedJobs.value)
}

const exportSelectedJobs = async () => {
  if (selectedJobs.value.size === 0) {
    notify({
      message: 'Por favor, selecciona al menos un anuncio para exportar',
      color: 'warning',
      duration: 3000
    })
    return
  }

  // Usar TODAS las aplicaciones sin filtros
  const allApps = applicationMgr.applications.value

  // Agrupar TODAS las aplicaciones por trabajo
  const grouped = {}
  allApps.forEach(app => {
    const jobId = app.jobId
    if (!grouped[jobId]) {
      grouped[jobId] = {
        jobId: jobId,
        jobTitle: app.jobTitle,
        applications: []
      }
    }
    grouped[jobId].applications.push(app)
  })

  // Filtrar solo los trabajos seleccionados
  const jobsToExport = Object.values(grouped).filter(jobGroup =>
    selectedJobs.value.has(jobGroup.jobId)
  )

  // Notificar sobre descargas múltiples
  if (jobsToExport.length > 1) {
    notify({
      message: `Preparando ${jobsToExport.length} archivos para descarga. Si tu navegador solicita permiso, por favor acepta las descargas múltiples.`,
      color: 'info',
      duration: 5000
    })
    // Pequeño delay para que el usuario vea el mensaje
    await new Promise(resolve => setTimeout(resolve, 1000))
  }

  // Exportar con delay entre cada archivo para evitar bloqueo del navegador
  for (let i = 0; i < jobsToExport.length; i++) {
    exportJobToCSV(jobsToExport[i])
    // Esperar 300ms entre cada descarga
    if (i < jobsToExport.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 300))
    }
  }

  notify({
    message: `✅ ${jobsToExport.length} ${jobsToExport.length === 1 ? 'archivo exportado' : 'archivos exportados'}`,
    color: 'success',
    duration: 4000
  })

  // Salir del modo de selección
  bulkExportMode.value = false
  selectedJobs.value = new Set()
}

const cancelBulkExport = () => {
  bulkExportMode.value = false
  selectedJobs.value = new Set()
}

const exportAllJobsSeparately = async () => {
  showExportMenu.value = false

  // Usar TODAS las aplicaciones sin filtros
  const allApps = applicationMgr.applications.value

  if (!allApps || allApps.length === 0) {
    notify({
      message: 'No hay anuncios para exportar',
      color: 'warning',
      duration: 3000
    })
    return
  }

  // Agrupar TODAS las aplicaciones por trabajo (sin filtros)
  const grouped = {}
  allApps.forEach(app => {
    const jobId = app.jobId
    if (!grouped[jobId]) {
      grouped[jobId] = {
        jobId: jobId,
        jobTitle: app.jobTitle,
        applications: []
      }
    }
    grouped[jobId].applications.push(app)
  })

  const jobs = Object.values(grouped)

  // Notificar sobre descargas múltiples
  if (jobs.length > 1) {
    notify({
      message: `Preparando ${jobs.length} archivos para descarga. Si tu navegador solicita permiso, por favor acepta las descargas múltiples.`,
      color: 'info',
      duration: 5000
    })
    // Pequeño delay para que el usuario vea el mensaje
    await new Promise(resolve => setTimeout(resolve, 1000))
  }

  // Exportar con delay entre cada archivo para evitar bloqueo del navegador
  for (let i = 0; i < jobs.length; i++) {
    exportJobToCSV(jobs[i])
    // Esperar 300ms entre cada descarga
    if (i < jobs.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 300))
    }
  }

  notify({
    message: `${jobs.length} ${jobs.length === 1 ? 'archivo exportado' : 'archivos exportados'} exitosamente`,
    color: 'success',
    duration: 4000
  })
}

const exportToCSV = () => {
  try {
    const apps = displayApplications.value

    if (!apps || apps.length === 0) {
      notify({
        message: 'No hay candidatos para exportar',
        color: 'warning',
        duration: 3000
      })
      return
    }

    generateCSV(apps, 'candidatos_todos')
  } catch (error) {
    console.error('Error exporting CSV:', error)
    notify({
      message: 'Error al exportar. Intenta nuevamente.',
      color: 'danger',
      duration: 4000
    })
  }
}

const exportJobToCSV = (jobGroup) => {
  try {
    if (!jobGroup.applications || jobGroup.applications.length === 0) {
      notify({
        message: 'No hay candidatos en este anuncio para exportar',
        color: 'warning',
        duration: 3000
      })
      return
    }

    // Limpiar el título del trabajo para usarlo como nombre de archivo
    const jobTitleClean = jobGroup.jobTitle
      .replace(/[^a-zA-Z0-9áéíóúñÁÉÍÓÚÑ\s]/g, '')
      .replace(/\s+/g, '_')
      .substring(0, 50)

    generateCSV(jobGroup.applications, `candidatos_${jobTitleClean}`)
  } catch (error) {
    console.error('Error exporting job CSV:', error)
    notify({
      message: 'Error al exportar. Intenta nuevamente.',
      color: 'danger',
      duration: 4000
    })
  }
}

const generateCSV = (apps, fileNamePrefix) => {
  // Definir headers del CSV
  const headers = [
    'Nombre',
    'Email',
    'Teléfono',
    'Puesto',
    'Estado',
    'Calificación',
    'Fecha de Aplicación',
    'Notas'
  ]

  // Convertir aplicaciones a filas CSV
  const rows = apps.map(app => {
    const statusLabels = {
      submitted: 'Recibida',
      reviewing: 'En Revisión',
      shortlisted: 'Preseleccionado',
      interviewed: 'Entrevistado',
      accepted: 'Aceptado',
      rejected: 'Rechazado',
      withdrawn: 'Retirada'
    }

    return [
      `"${app.applicantName || ''}"`,
      `"${app.applicantEmail || ''}"`,
      `"${app.applicantPhone || ''}"`,
      `"${app.jobTitle || ''}"`,
      `"${statusLabels[app.status] || app.status}"`,
      app.rating ? `${app.rating}/5` : 'Sin calificar',
      app.createdAt ? new Date(app.createdAt).toLocaleDateString('es-ES') : '',
      `"${(app.recruiterNotes || '').replace(/"/g, '""')}"` // Escapar comillas dobles
    ].join(',')
  })

  // Crear contenido CSV
  const csvContent = [
    headers.join(','),
    ...rows
  ].join('\n')

  // Crear Blob y descargar
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)

  link.setAttribute('href', url)
  link.setAttribute('download', `${fileNamePrefix}_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  notify({
    message: `${apps.length} candidatos exportados exitosamente`,
    color: 'success',
    duration: 3000
  })
}

const saveNotes = async (application) => {
  try {
    updating.value = true
    await applicationMgr.saveRecruiterNotes(
      application.jobId,
      application.id,
      application.recruiterNotes || ''
    )

    notify({
      message: '✅ Notas guardadas',
      color: 'success',
      duration: 2000
    })
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    updating.value = false
  }
}

const resetAndLoad = () => {
  applicationMgr.resetApplications()
  applicationMgr.loadApplications()
}

const downloadCV = (fileUrl) => {
  if (!fileUrl) return

  // Asegurar URL absoluta
  const fullUrl = fileUrl.startsWith('http')
    ? fileUrl
    : `http://localhost:8000${fileUrl}`

  window.open(fullUrl, '_blank')
}

// ========== BULK ACTIONS ==========
const toggleSelection = (applicationId) => {
  if (selectedApplications.value.has(applicationId)) {
    selectedApplications.value.delete(applicationId)
  } else {
    selectedApplications.value.add(applicationId)
  }
  // Force reactivity
  selectedApplications.value = new Set(selectedApplications.value)
}

const clearSelection = () => {
  selectedApplications.value = new Set()  // Crear un Set completamente nuevo
}

const bulkChangeStatus = (newStatus) => {
  if (selectedApplications.value.size === 0) return

  // Guardar la acción pendiente y mostrar modal de confirmación
  pendingBulkAction.value = {
    status: newStatus,
    count: selectedApplications.value.size,
    label: getStatusLabel(newStatus)
  }
  showBulkConfirmModal.value = true
}

const confirmBulkAction = async () => {
  if (!pendingBulkAction.value) return

  const { status: newStatus, label: statusLabel } = pendingBulkAction.value
  showBulkConfirmModal.value = false

  try {
    updating.value = true

    // Obtener todas las aplicaciones seleccionadas
    const selectedApps = applicationMgr.applications.value.filter(app =>
      selectedApplications.value.has(app.id)
    )

    // Contador de éxitos y errores
    let successCount = 0
    let errorCount = 0

    // Actualizar cada aplicación
    for (const app of selectedApps) {
      try {
        await applicationMgr.updateApplicationStatus(
          app.jobId,
          app.id,
          newStatus
        )
        successCount++
      } catch (error) {
        console.error(`Error updating application ${app.id}:`, error)
        errorCount++
      }
    }

    // Limpiar selección
    clearSelection()
    pendingBulkAction.value = null

    // Notificar resultados
    if (errorCount === 0) {
      notify({
        message: `${successCount} ${successCount === 1 ? 'candidato actualizado' : 'candidatos actualizados'} a "${statusLabel}"`,
        color: 'success',
        duration: 4000
      })
    } else {
      notify({
        message: `${successCount} actualizados correctamente, ${errorCount} con errores`,
        color: 'warning',
        duration: 5000
      })
    }
  } catch (err) {
    notify({
      message: `Error al actualizar candidatos: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    updating.value = false
  }
}

const cancelBulkAction = () => {
  showBulkConfirmModal.value = false
  pendingBulkAction.value = null
}
</script>

<style scoped>
.candidates-view {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* ========== HEADER ========== */
.section-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #E4E7EC;
}

.section-header h2 {
  margin: 0 0 0.5rem;
  font-size: 2rem;
  font-weight: 700;
  color: #1F2937;
}

.section-subtitle {
  margin: 0;
  font-size: 0.95rem;
  color: #6B7280;
  font-weight: 500;
}

/* ========== STATS GRID ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #E4E7EC;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 8px;
  color: white;
  font-size: 1.5rem;
}

.stat-icon.total {
  background: var(--color-purple);
}

.stat-icon.received {
  background: #3B82F6;
}

.stat-icon.reviewing {
  background: #F59E0B;
}

.stat-icon.shortlisted {
  background: #10B981;
}

.stat-content h3 {
  margin: 0;
  font-size: 0.8rem;
  color: #6B7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-number {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0.5rem 0 0;
}

/* ========== FILTER BAR ========== */
.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 250px;
  padding: 0.75rem 1rem;
  background: white;
  border: 1px solid #E4E7EC;
  border-radius: 8px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 0.95rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #E4E7EC;
  border-radius: 8px;
  background: white;
  font-size: 0.95rem;
  cursor: pointer;
}

/* ========== RESULTS COUNTER ========== */
.results-counter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
  border-radius: 8px;
  border: 1px solid #E4E7EC;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.counter-text {
  font-size: 0.95rem;
  color: #4B5563;
}

.counter-text strong {
  color: #7C3AED;
  font-weight: 700;
}

.counter-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.export-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
}

.export-btn:disabled {
  background: linear-gradient(135deg, #D1D5DB 0%, #9CA3AF 100%);
  cursor: not-allowed;
  opacity: 0.6;
  box-shadow: none;
}

/* Export Dropdown */
.export-dropdown {
  position: relative;
}

.export-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 320px;
  background: white;
  border: 2px solid #7C3AED;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.25);
  z-index: 1000;
  overflow: hidden;
}

.export-menu-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem 1.25rem;
  background: white;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.export-menu-item:hover {
  background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
}

.menu-item-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.menu-item-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1F2937;
}

.menu-item-desc {
  font-size: 0.75rem;
  color: #6B7280;
  line-height: 1.3;
}

.menu-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #E4E7EC, transparent);
  margin: 0.25rem 0;
}

/* Dropdown Fade Animation */
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: all 0.2s ease;
}

.dropdown-fade-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}

.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.clear-filters-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #E4E7EC;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-filters-btn:hover {
  background: #F9FAFB;
  border-color: #7C3AED;
  color: #7C3AED;
}

/* ========== STATES ========== */
.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #E4E7EC;
}

.empty-state h3 {
  margin: 1rem 0 0.5rem;
  font-size: 1.25rem;
  color: #1F2937;
}

.empty-state p {
  margin: 0 0 1.5rem;
  color: #6B7280;
}

.retry-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-purple);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.retry-btn:hover {
  background: #5b21b6;
  transform: translateY(-2px);
}

/* ========== APPLICATIONS LIST ========== */
.applications-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ========== JOB GROUPS ========== */
.job-group {
  background: white;
  border-radius: 12px;
  border: 2px solid #E4E7EC;
  overflow: hidden;
  transition: all 0.3s;
}

.job-group:hover {
  border-color: #C4B5FD;
  box-shadow: 0 4px 16px rgba(124, 58, 237, 0.1);
}

.job-group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.75rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #F5F3FF 100%);
  transition: all 0.3s;
  border-bottom: 2px solid #E4E7EC;
}

.job-group-header:hover {
  background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
}

.job-group-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  flex: 1;
}

.job-group-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.expand-icon {
  color: #7C3AED;
  font-size: 1.75rem;
  transition: transform 0.3s;
}

.job-group-title h3 {
  margin: 0 0 0.375rem 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1F2937;
}

.applications-count {
  font-size: 0.875rem;
  font-weight: 600;
  color: #7C3AED;
  background: rgba(124, 58, 237, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
}

.export-job-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.export-job-btn:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.35);
}

.export-job-btn:active {
  transform: translateY(0);
}

.job-group-stats {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.mini-stat {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 28px;
  padding: 0 0.5rem;
  border-radius: 14px;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  box-shadow: 0 2px 4px rgba(124, 58, 237, 0.25);
  transition: all 0.3s ease;
}

.mini-stat:hover {
  background: linear-gradient(135deg, #6D28D9 0%, #5B21B6 100%);
  transform: scale(1.08);
  box-shadow: 0 3px 8px rgba(124, 58, 237, 0.4);
}

.job-group-applications {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: #FAFAFA;
}

.application-card {
  background: white;
  border-radius: 8px;
  border: 1px solid #E4E7EC;
  overflow: hidden;
  transition: all 0.2s;
}

.application-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #C4B5FD;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #F9FAFB;
  border-bottom: 1px solid #E4E7EC;
}

.applicant-info {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.applicant-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  font-weight: 700;
  flex-shrink: 0;
}

.applicant-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.applicant-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1F2937;
}

.applicant-email {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  color: #6B7280;
}

.job-title {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: #9CA3AF;
  font-weight: 500;
}

.applicant-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.application-date {
  font-size: 0.8rem;
  color: #9CA3AF;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}


.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge.status-received {
  background: #DBEAFE;
  color: #1E40AF;
}

.status-badge.status-reviewing {
  background: #FEF3C7;
  color: #92400E;
}

.status-badge.status-shortlisted {
  background: #DCFCE7;
  color: #15803D;
}

.status-badge.status-accepted {
  background: #D1FAE5;
  color: #065F46;
}

.status-badge.status-rejected {
  background: #FEE2E2;
  color: #991B1B;
}

.expand-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6B7280;
  transition: color 0.2s;
}

.expand-btn:hover {
  color: var(--color-purple);
}

.card-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: #FAFAFA;
}

.section {
  padding: 1rem;
  background: white;
  border-radius: 6px;
  border: 1px solid #E4E7EC;
}

.section-title {
  margin: 0 0 1rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1F2937;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
}

.contact-item {
  padding: 0.75rem;
  background: #F3F4F6;
  border-radius: 4px;
}

.contact-label {
  display: block;
  font-size: 0.8rem;
  color: #6B7280;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.contact-value,
.contact-link {
  display: block;
  font-size: 0.9rem;
  color: #1F2937;
}

.contact-link {
  color: var(--color-purple);
  text-decoration: none;
  transition: color 0.2s;
}

.contact-link:hover {
  color: #5b21b6;
  text-decoration: underline;
}

/* Status Section Mejorada */
.status-section {
  background: linear-gradient(135deg, #FAFAFA 0%, #F5F3FF 100%) !important;
  border: 2px solid #E4E7EC !important;
}

.status-buttons-compact {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  border: 2px solid #E4E7EC;
  border-radius: 20px;
  background: white;
  color: #6B7280;
  cursor: pointer;
  font-size: 0.8125rem;
  font-weight: 600;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.status-pill:hover:not(:disabled):not(.active) {
  border-color: #C4B5FD;
  background: #FAFAFA;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.15);
}

.status-pill:active:not(:disabled) {
  transform: translateY(0);
}

.status-pill:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Estado Activo General */
.status-pill.active {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  border-color: #7C3AED;
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35);
  transform: translateY(-1px);
}

/* Estados Específicos */
.status-pill.status-reviewing:not(.active) {
  border-color: #FEF3C7;
  color: #D97706;
  background: #FFFBEB;
}

.status-pill.status-reviewing:not(.active):hover {
  border-color: #F59E0B;
  background: #FEF3C7;
  box-shadow: 0 4px 8px rgba(245, 158, 11, 0.2);
}

.status-pill.status-reviewing.active {
  background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
  border-color: #F59E0B;
}

.status-pill.status-shortlisted:not(.active) {
  border-color: #D1FAE5;
  color: #059669;
  background: #ECFDF5;
}

.status-pill.status-shortlisted:not(.active):hover {
  border-color: #10B981;
  background: #D1FAE5;
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.2);
}

.status-pill.status-shortlisted.active {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  border-color: #10B981;
}

.status-pill.status-interviewed:not(.active) {
  border-color: #DBEAFE;
  color: #2563EB;
  background: #EFF6FF;
}

.status-pill.status-interviewed:not(.active):hover {
  border-color: #3B82F6;
  background: #DBEAFE;
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.2);
}

.status-pill.status-interviewed.active {
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  border-color: #3B82F6;
}

.status-pill.status-accepted:not(.active) {
  border-color: #D1FAE5;
  color: #047857;
  background: #ECFDF5;
}

.status-pill.status-accepted:not(.active):hover {
  border-color: #059669;
  background: #D1FAE5;
  box-shadow: 0 4px 8px rgba(5, 150, 105, 0.2);
}

.status-pill.status-accepted.active {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  border-color: #059669;
}

.status-pill.status-rejected:not(.active) {
  border-color: #FEE2E2;
  color: #DC2626;
  background: #FEF2F2;
}

.status-pill.status-rejected:not(.active):hover {
  border-color: #EF4444;
  background: #FEE2E2;
  box-shadow: 0 4px 8px rgba(239, 68, 68, 0.2);
}

.status-pill.status-rejected.active {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  border-color: #EF4444;
}

.notes-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #E4E7EC;
  border-radius: 6px;
  font-size: 0.9rem;
  font-family: inherit;
  resize: vertical;
  min-height: 100px;
}

.notes-textarea:focus {
  outline: none;
  border-color: var(--color-purple);
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

/* ========== CV INFO ========== */
.cv-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 6px;
  border: 1px solid #E4E7EC;
}

.cv-type-badge {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #7C3AED, #6D28D9);
  color: white;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.cv-details {
  flex: 1;
  min-width: 0;
}

.cv-name {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1F2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cv-date {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: #9CA3AF;
}

.btn-download {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: var(--color-purple);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-download:hover {
  background: #5b21b6;
  transform: translateY(-2px);
}

/* ========== COVER LETTER ========== */
.cover-letter-content {
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 6px;
  border: 1px solid #E4E7EC;
  font-size: 0.9rem;
  color: #374151;
  line-height: 1.6;
  white-space: pre-wrap;
}

/* ========== CANDIDATE PROFILE ========== */
.candidate-profile {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.profile-section {
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 6px;
  border: 1px solid #E4E7EC;
}

.profile-subtitle {
  margin: 0 0 1rem;
  font-size: 0.9rem;
  font-weight: 700;
  color: #7C3AED;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.profile-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.profile-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6B7280;
}

.profile-value {
  font-size: 0.9rem;
  color: #1F2937;
  font-weight: 500;
}

.profile-description {
  margin: 0;
  font-size: 0.9rem;
  color: #374151;
  line-height: 1.6;
}

/* Experience Items */
.experience-item,
.education-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid #E4E7EC;
}

.experience-item:last-child,
.education-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.experience-header,
.education-header {
  font-size: 0.95rem;
  color: #1F2937;
  margin-bottom: 0.25rem;
}

.experience-dates,
.education-dates {
  font-size: 0.8rem;
  color: #6B7280;
  margin-bottom: 0.5rem;
}

.experience-description {
  margin: 0;
  font-size: 0.875rem;
  color: #4B5563;
  line-height: 1.5;
}

/* Skills List */
.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  padding: 0.375rem 0.75rem;
  background: white;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  color: #374151;
  transition: all 0.2s;
}

.skill-tag:hover {
  border-color: #7C3AED;
  color: #7C3AED;
  transform: translateY(-2px);
}

/* ========== BULK ACTIONS ========== */
.selection-checkbox {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
}

.custom-checkbox {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #7C3AED;
  border-radius: 4px;
}

.application-card.is-selected {
  border-color: #7C3AED;
  background: linear-gradient(to right, rgba(124, 58, 237, 0.05) 0%, white 100%);
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.15);
}

.bulk-actions-toolbar {
  background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
  border: 2px solid #7C3AED;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: 0 4px 16px rgba(124, 58, 237, 0.2);
}

.bulk-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.bulk-count {
  font-size: 1rem;
  color: #1F2937;
}

.bulk-count strong {
  color: #7C3AED;
  font-weight: 700;
  font-size: 1.125rem;
}

.bulk-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: center;
  justify-content: space-between;
}

.bulk-action-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
  min-width: 300px;
}

.bulk-action-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #4B5563;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.bulk-status-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.bulk-status-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border: 2px solid transparent;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  background: white;
  color: #6B7280;
}

.bulk-status-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.bulk-status-btn.status-reviewing {
  border-color: #F59E0B;
  color: #F59E0B;
}

.bulk-status-btn.status-reviewing:hover {
  background: #F59E0B;
  color: white;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.bulk-status-btn.status-shortlisted {
  border-color: #10B981;
  color: #10B981;
}

.bulk-status-btn.status-shortlisted:hover {
  background: #10B981;
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.bulk-status-btn.status-interviewed {
  border-color: #3B82F6;
  color: #3B82F6;
}

.bulk-status-btn.status-interviewed:hover {
  background: #3B82F6;
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.bulk-status-btn.status-accepted {
  border-color: #059669;
  color: #059669;
}

.bulk-status-btn.status-accepted:hover {
  background: #059669;
  color: white;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.4);
}

.bulk-status-btn.status-rejected {
  border-color: #EF4444;
  color: #EF4444;
}

.bulk-status-btn.status-rejected:hover {
  background: #EF4444;
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.bulk-quick-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.bulk-clear-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: white;
  border: 2px solid #D1D5DB;
  border-radius: 8px;
  color: #6B7280;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.bulk-clear-btn:hover {
  background: #F9FAFB;
  border-color: #9CA3AF;
  color: #374151;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* ========== BULK EXPORT TOOLBAR ========== */
.bulk-export-toolbar {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border: 2px solid #F59E0B;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  box-shadow: 0 4px 16px rgba(245, 158, 11, 0.2);
}

.export-selected-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.export-selected-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.export-selected-btn:disabled {
  background: linear-gradient(135deg, #D1D5DB 0%, #9CA3AF 100%);
  cursor: not-allowed;
  opacity: 0.6;
  box-shadow: none;
}

.job-export-checkbox {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
}

/* Animación de entrada del toolbar */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .candidates-view {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }

  .filter-bar {
    flex-direction: column;
  }

  .search-box {
    min-width: 100%;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .card-actions {
    width: 100%;
    justify-content: space-between;
  }

  .contact-grid {
    grid-template-columns: 1fr;
  }

  /* Status Pills Responsive */
  .status-buttons-compact {
    flex-direction: column;
  }

  .status-pill {
    width: 100%;
    justify-content: center;
  }

  .cv-info {
    flex-direction: column;
    align-items: flex-start;
  }

  .btn-download {
    width: 100%;
    justify-content: center;
  }

  .profile-grid {
    grid-template-columns: 1fr;
  }

  .skills-list {
    gap: 0.375rem;
  }

  .skill-tag {
    font-size: 0.75rem;
    padding: 0.3rem 0.6rem;
  }

  /* Bulk Actions Responsive */
  .bulk-actions-toolbar {
    padding: 1rem;
  }

  .bulk-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .bulk-action-group {
    min-width: 100%;
  }

  .bulk-status-buttons {
    flex-direction: column;
  }

  .bulk-status-btn {
    width: 100%;
    justify-content: center;
  }

  .bulk-quick-actions {
    flex-direction: column;
  }

  .bulk-clear-btn {
    width: 100%;
    justify-content: center;
  }
}

/* ========== MODAL DE CONFIRMACIÓN ========== */
.modal-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
}

.modal-content {
  padding: 1rem 0;
}

.modal-message {
  font-size: 1rem;
  color: #374151;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.status-highlight {
  color: #7C3AED;
  font-weight: 700;
}

.modal-warning {
  font-size: 0.875rem;
  color: #DC2626;
  font-weight: 600;
  background: #FEF2F2;
  border-left: 4px solid #DC2626;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  margin: 0;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
}

.modal-btn-cancel {
  min-width: 120px;
}

.modal-btn-confirm {
  min-width: 120px;
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
}

.modal-btn-confirm:hover {
  background: linear-gradient(135deg, #6D28D9 0%, #5B21B6 100%);
}

/* ========== CONTACT ACTIONS ========== */
.contact-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.contact-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  border: none;
}

.whatsapp-btn {
  background: linear-gradient(135deg, #25D366 0%, #1EBE57 100%);
  color: white;
}

.whatsapp-btn:hover {
  background: linear-gradient(135deg, #1EBE57 0%, #128C7E 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);
  color: white;
}

.email-btn {
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  color: white;
}

.email-btn:hover {
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.contact-btn:active {
  transform: translateY(0);
}
</style>
