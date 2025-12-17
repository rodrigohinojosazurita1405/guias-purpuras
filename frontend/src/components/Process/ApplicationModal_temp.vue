<template>
  <!-- Modal overlay y contenedor custom para móvil -->
  <Transition name="modal-fade">
    <div v-if="internalOpen" class="custom-modal-overlay" @click.self="handleOverlayClick">
      <div class="custom-modal-container" :class="{ 'is-mobile': isMobile }">
        <div class="custom-modal-dialog">
          <!-- Header -->
          <div class="modal-header-content">
        <!-- Job Info -->
        <div class="job-header-info">
          <div class="company-logo-mini" v-if="job.companyLogo">
            <img :src="job.companyLogo" :alt="job.companyName" />
          </div>
          <div class="company-logo-placeholder-mini" v-else>
            <va-icon name="business" size="small" />
          </div>
          <div class="job-info-text">
            <h2 class="job-title-modal">{{ job.title }}</h2>
            <p class="company-name-modal">{{ job.companyName }}</p>
          </div>
        </div>

        <!-- Tabs -->
        <div class="tabs-header">
          <!-- Tab: Mis CVs (solo si tiene CVs guardados) -->
          <button
            v-if="hasSavedCVs"
            class="tab-btn"
            :class="{ active: activeTab === 'saved' }"
            @click="activeTab = 'saved'"
          >
            <va-icon name="folder" size="small" />
            Mis CVs
            <span class="cv-count">{{ savedCVs.length }}</span>
          </button>

          <button
            class="tab-btn"
            :class="{ active: activeTab === 'upload' }"
            @click="activeTab = 'upload'"
          >
            <va-icon name="upload_file" size="small" />
            Subir CV
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'create' }"
            @click="activeTab = 'create'"
          >
            <va-icon name="description" size="small" />
            Crear CV
          </button>
        </div>

        <button class="close-btn" @click="handleClose">
          <va-icon name="close" size="small" />
        </button>
      </div>
    </template>

    <!-- Tab Content -->
    <div class="modal-body">
      <!-- Tab: Mis CVs Guardados -->
      <div v-if="activeTab === 'saved'" class="saved-cvs-container">
        <p class="tab-intro">Selecciona un CV guardado para usar en tu postulación</p>

        <div v-if="isLoadingCVs" class="loading-state">
          <va-icon name="sync" size="large" class="spinning" />
          <p>Cargando tus CVs...</p>
        </div>

        <div v-else-if="savedCVs.length === 0" class="empty-state">
          <va-icon name="folder_open" size="3rem" color="#D1D5DB" />
          <p>No tienes CVs guardados todavía</p>
        </div>

        <div v-else class="cvs-list">
          <div
            v-for="cv in savedCVs"
            :key="cv.id"
            class="cv-card"
            :class="{ selected: selectedSavedCV?.id === cv.id }"
            @click="selectCV(cv)"
          >
            <div class="cv-card-header">
              <va-icon
                :name="cv.type === 'file' ? 'description' : 'article'"
                size="large"
                :color="selectedSavedCV?.id === cv.id ? '#7C3AED' : '#6B7280'"
              />
              <div class="cv-card-info">
                <h4>{{ cv.full_name || cv.file_name }}</h4>
                <p class="cv-meta">
                  <span>{{ cv.type === 'file' ? 'Archivo subido' : 'CV creado' }}</span>
                  <span>•</span>
                  <span>{{ formatDate(cv.created_at) }}</span>
                </p>
              </div>
              <va-icon
                v-if="selectedSavedCV?.id === cv.id"
                name="check_circle"
                color="#10B981"
                size="large"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Tab: Subir CV -->
      <UploadCVTab
        v-else-if="activeTab === 'upload'"
        :file="uploadedFile"
        :coverLetter="coverLetter"
        @update:file="uploadedFile = $event"
        @update:coverLetter="coverLetter = $event"
      />

      <!-- Tab: Crear CV -->
      <CreateCVTab
        v-else-if="activeTab === 'create'"
        v-model="cvData"
      />
          </div>

          <!-- Footer -->
          <div class="modal-footer-actions">
            <va-button color="secondary" @click="handleClose">
              Cancelar
            </va-button>

            <!-- Botón para guardar CV en dashboard (solo visible en tab "Crear CV") -->
            <va-button
              v-if="activeTab === 'create'"
              color="primary"
              class="btn-save-cv"
              @click="handleSaveCV"
              :disabled="!canSubmit || isSavingCV"
            >
              <va-icon name="save" size="small" />
              {{ isSavingCV ? 'Guardando...' : 'Guardar en Dashboard' }}
            </va-button>

            <va-button @click="handleSubmit" :disabled="!canSubmit">
              <va-icon name="send" size="small" />
              Enviar Postulación
            </va-button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import UploadCVTab from './UploadCVTab.vue'
import CreateCVTab from './CreateCVTab.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  job: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'submit', 'saveCV'])

// Estado interno del modal que sincroniza con el prop
const internalOpen = ref(false)
const allowClose = ref(false)

// Detectar si es dispositivo móvil
const isMobile = ref(window.innerWidth <= 768)

const updateIsMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  window.addEventListener('resize', updateIsMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateIsMobile)
})

const activeTab = ref('upload')
const uploadedFile = ref(null)
const coverLetter = ref('')
const isSavingCV = ref(false)
const savedCVs = ref([])
const selectedSavedCV = ref(null)
const isLoadingCVs = ref(false)
const cvData = ref({
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

/**
 * Cargar CVs guardados del usuario desde el backend
 */
const loadSavedCVs = async () => {
  isLoadingCVs.value = true
  try {
    const response = await fetch('/api/cvs/list/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
