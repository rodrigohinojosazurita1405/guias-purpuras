<!-- frontend/src/components/Home/GuidesSection.vue -->
<template>
  <section class="featured-jobs-section">
    <!-- Encabezado de Empleos Destacados -->
    <div class="section-header">
      <h2 class="section-title">Empleos Destacados</h2>
      <p class="section-subtitle">Oportunidades laborales seleccionadas actualizadas diariamente</p>
    </div>

    <!-- Grid de Empleos -->
    <div class="jobs-container">
      <div class="jobs-grid">
        <!-- Mostrar todos los empleos dinámicamente (sin limitar a 4) -->
        <div
          v-for="job in displayedJobs"
          :key="job.id"
          class="job-card"
          @click="navigateToJob(job.id)"
        >
          <!-- Badge Nuevo/Destacado -->
          <div v-if="job.isNew" class="job-badge new-badge">
            <va-icon name="new_releases" size="small" />
            Nuevo
          </div>
          <div v-if="job.isFeatured" class="job-badge featured-badge">
            <va-icon name="star" size="small" />
            Destacado
          </div>

          <!-- Logo de Empresa -->
          <div class="company-logo-container">
            <img
              v-if="job.companyLogo"
              :src="job.companyLogo"
              :alt="job.company"
              class="company-logo"
            />
            <div v-else class="company-logo-placeholder">
              <va-icon name="business" size="2rem" />
            </div>
          </div>

          <!-- Información del Empleo -->
          <h3 class="job-title">{{ job.title }}</h3>
          <p class="company-name">{{ job.company }}</p>

          <!-- Ubicación -->
          <div class="job-info">
            <va-icon name="location_on" size="small" />
            <span>{{ job.location }}</span>
          </div>

          <!-- Tipo de Trabajo -->
          <div class="job-info">
            <va-icon name="work_history" size="small" />
            <span>{{ job.jobType }}</span>
          </div>

          <!-- Salario (si está disponible) -->
          <div v-if="job.salary" class="job-salary">
            <va-icon name="monetization_on" size="small" />
            <span>{{ job.salary }}</span>
          </div>

          <!-- Footer con fecha -->
          <div class="job-footer">
            <span class="job-date">{{ formatDate(job.createdAt) }}</span>
            <va-icon name="arrow_forward" size="small" class="forward-icon" />
          </div>
        </div>
      </div>

      <!-- Mensaje si no hay empleos -->
      <div v-if="displayedJobs.length === 0" class="empty-state">
        <va-icon name="search_off" size="4rem" />
        <h3>No hay empleos disponibles</h3>
        <p>Intenta con otros filtros o vuelve más tarde</p>
      </div>
    </div>

    <!-- CTA Ver Todos -->
    <div class="section-cta">
      <button class="btn-see-all" @click="goToAllJobs">
        Ver todos los empleos
        <va-icon name="arrow_forward" size="small" />
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ==========================================
// DATA
// ==========================================
const jobs = ref([])
const loading = ref(true)

// Datos de ejemplo mientras no tenemos backend
const mockJobs = [
  {
    id: 1,
    title: 'Desarrollador Frontend React',
    company: 'Tech Solutions Bolivia',
    companyLogo: null,
    location: 'La Paz',
    jobType: 'Tiempo Completo',
    salary: '$2,500 - $3,500/mes',
    isNew: true,
    isFeatured: true,
    createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
  },
  {
    id: 2,
    title: 'Diseñador UX/UI',
    company: 'Digital Minds',
    companyLogo: null,
    location: 'Santa Cruz',
    jobType: 'Remoto',
    salary: '$2,000 - $2,800/mes',
    isNew: true,
    isFeatured: false,
    createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
  },
  {
    id: 3,
    title: 'Especialista en Marketing Digital',
    company: 'Growth Agency',
    companyLogo: null,
    location: 'Cochabamba',
    jobType: 'Tiempo Completo',
    salary: '$1,800 - $2,400/mes',
    isNew: false,
    isFeatured: true,
    createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
  },
  {
    id: 4,
    title: 'Contador General',
    company: 'Financial Consulting',
    companyLogo: null,
    location: 'La Paz',
    jobType: 'Tiempo Completo',
    salary: '$1,600 - $2,200/mes',
    isNew: false,
    isFeatured: false,
    createdAt: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000)
  },
  {
    id: 5,
    title: 'Community Manager Freelance',
    company: 'Social Brands',
    companyLogo: null,
    location: 'Remoto',
    jobType: 'Freelance',
    salary: '$800 - $1,200/proyecto',
    isNew: true,
    isFeatured: false,
    createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
  },
  {
    id: 6,
    title: 'Practicante Desarrollo Backend',
    company: 'Code Academy Bolivia',
    companyLogo: null,
    location: 'La Paz',
    jobType: 'Pasantía',
    salary: 'Pasantía remunerada',
    isNew: true,
    isFeatured: true,
    createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
  }
]

// ==========================================
// COMPUTED
// ==========================================
const displayedJobs = computed(() => {
  return jobs.value.length > 0 ? jobs.value : mockJobs
})

// ==========================================
// METHODS
// ==========================================
const formatDate = (date) => {
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Hoy'
  if (diffDays === 1) return 'Ayer'
  if (diffDays < 7) return `Hace ${diffDays} días`
  return date.toLocaleDateString('es-BO')
}

const navigateToJob = (jobId) => {
  router.push(`/guias/trabajos/${jobId}`)
}

const goToAllJobs = () => {
  router.push('/guias/trabajos')
}

// ==========================================
// LIFECYCLE
// ==========================================
onMounted(async () => {
  // TODO: Aquí irá la llamada a la API cuando esté lista
  // const response = await fetch('/api/jobs/featured')
  // jobs.value = await response.json()

  // Por ahora usamos datos mock
  loading.value = false
})
</script>

<style scoped>
/* ==========================================
   SECCIÓN DE EMPLEOS DESTACADOS
   ========================================== */
.featured-jobs-section {
  width: 100%;
  margin: 0;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
}

.jobs-container {
  max-width: 1200px;
  margin: 0 auto;
  margin-bottom: 3rem;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

/* ==========================================
   TARJETA DE EMPLEO
   ========================================== */
.job-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  color: #333;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border: 1px solid #e5e5e5;
}

.job-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
  border-color: #ddd;
}

/* Badge de Empleo */
.job-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  z-index: 10;
}

.new-badge {
  background: var(--color-success);
  color: white;
}

.featured-badge {
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

/* Logo de Empresa */
.company-logo-container {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  overflow: hidden;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.25rem;
}

.company-logo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.company-logo-placeholder {
  color: var(--color-purple);
}

/* Título del Empleo */
.job-title {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--color-purple-darkest);
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Nombre de Empresa */
.company-name {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
  font-weight: 500;
}

/* Info de Empleo (ubicación, tipo) */
.job-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #555;
  margin-top: 0.25rem;
}

.job-info :deep(svg) {
  color: var(--color-purple);
  flex-shrink: 0;
}

/* Salario */
.job-salary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-success);
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: rgba(16, 185, 129, 0.08);
  border-radius: 8px;
}

.job-salary :deep(svg) {
  color: var(--color-success);
}

/* Footer con Fecha */
.job-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e5e5;
}

.job-date {
  font-size: 0.8rem;
  color: #999;
}

.forward-icon {
  color: var(--color-purple);
  opacity: 0;
  transform: translateX(-4px);
  transition: all 0.3s ease;
}

.job-card:hover .forward-icon {
  opacity: 1;
  transform: translateX(0);
}

/* Estado Vacío */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 2rem;
  color: #999;
}

.empty-state :deep(svg) {
  color: #ddd;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.empty-state p {
  font-size: 1rem;
  color: #999;
}

/* Botón Ver Todos */
.section-cta {
  text-align: center;
  margin-top: 2rem;
}

.btn-see-all {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2.5rem;
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(92, 0, 153, 0.2);
}

.btn-see-all:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(92, 0, 153, 0.35);
}

.btn-see-all:active {
  transform: translateY(-1px);
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1200px) {
  .featured-jobs-section {
    padding: 3.5rem 2rem;
  }

  .section-title {
    font-size: 2.2rem;
  }

  .jobs-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 968px) {
  .featured-jobs-section {
    padding: 3rem 1.5rem;
  }

  .section-header {
    margin-bottom: 2.5rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .section-subtitle {
    font-size: 1rem;
  }

  .jobs-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }

  .job-card {
    padding: 1.25rem;
  }

  .company-logo-container {
    width: 50px;
    height: 50px;
  }

  .job-title {
    font-size: 1rem;
  }
}

@media (max-width: 640px) {
  .featured-jobs-section {
    padding: 2rem 1rem;
  }

  .section-header {
    margin-bottom: 2rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .section-subtitle {
    font-size: 0.95rem;
  }

  .jobs-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .job-card {
    padding: 1rem;
  }

  .job-badge {
    top: 0.75rem;
    right: 0.75rem;
    font-size: 0.7rem;
    padding: 0.3rem 0.6rem;
  }

  .company-logo-container {
    width: 50px;
    height: 50px;
  }

  .job-title {
    font-size: 0.95rem;
  }

  .company-name {
    font-size: 0.85rem;
  }

  .job-info {
    font-size: 0.8rem;
  }

  .btn-see-all {
    width: 100%;
    padding: 0.9rem 2rem;
    font-size: 1rem;
  }

  .empty-state {
    padding: 3rem 1rem;
  }

  .empty-state h3 {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .featured-jobs-section {
    padding: 1.5rem 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .section-subtitle {
    font-size: 0.9rem;
  }

  .jobs-container {
    margin-bottom: 2rem;
  }

  .job-card {
    padding: 0.9rem;
    gap: 0.5rem;
  }

  .job-badge {
    top: 0.5rem;
    right: 0.5rem;
    font-size: 0.65rem;
    padding: 0.25rem 0.5rem;
  }

  .company-logo-container {
    width: 45px;
    height: 45px;
  }

  .job-title {
    font-size: 0.9rem;
  }

  .company-name {
    font-size: 0.8rem;
  }

  .job-info {
    font-size: 0.75rem;
  }

  .job-salary {
    font-size: 0.85rem;
  }

  .job-date {
    font-size: 0.75rem;
  }

  .btn-see-all {
    padding: 0.8rem 1.5rem;
    font-size: 0.95rem;
    width: 100%;
  }
}
</style>