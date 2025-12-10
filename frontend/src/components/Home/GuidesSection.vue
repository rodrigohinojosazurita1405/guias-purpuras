<!-- frontend/src/components/Home/GuidesSection.vue -->
<template>
  <section class="featured-jobs-section">
    <div class="jobs-container">
      <!-- Header con título y botón ver todos -->
      <div class="section-header">
        <div>
          <h2 class="section-title">Empleos destacados en Bolivia</h2>
          <p class="section-subtitle">
            {{ loading ? 'Cargando...' : `${displayedJobs.length} oportunidades activas hoy` }}
          </p>
        </div>
        <button class="btn-see-all-top" @click="goToAllJobs">
          Ver todos
          <va-icon name="arrow_forward" size="16px" />
        </button>
      </div>

      <!-- Grid de Empleos - Estilo OLX -->
      <div v-if="!loading && displayedJobs.length > 0" class="jobs-grid">
        <div
          v-for="job in displayedJobs.slice(0, 8)"
          :key="job.id"
          class="job-card"
          @click="navigateToJob(job.id)"
        >
          <!-- Badges superiores -->
          <div class="card-badges">
            <span v-if="job.planType === 'impulso'" class="badge badge-impulso">Patrocinado</span>
            <span v-else-if="job.planType === 'purpura'" class="badge badge-purpura">Destacado</span>
            <span v-if="job.urgent" class="badge badge-urgent">Urgente</span>
          </div>

          <!-- Contenido principal -->
          <div class="card-content">
            <!-- Logo empresa -->
            <div class="company-logo">
              <img
                v-if="job.companyLogo"
                :src="job.companyLogo"
                :alt="job.companyName"
              />
              <va-icon v-else name="business" size="1.5rem" color="#9CA3AF" />
            </div>

            <!-- Info principal -->
            <div class="job-main-info">
              <h3 class="job-title">{{ job.title }}</h3>
              <p class="company-name">{{ job.companyName }}</p>

              <!-- Metadata en línea -->
              <div class="job-metadata">
                <span class="meta-item">
                  <va-icon name="location_on" size="14px" />
                  {{ job.city }}
                </span>
                <span class="meta-divider">•</span>
                <span class="meta-item">
                  <va-icon name="work" size="14px" />
                  {{ job.contractType }}
                </span>
              </div>

              <!-- Salario destacado -->
              <div v-if="formatSalary(job)" class="job-salary">
                {{ formatSalary(job) }}
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="card-footer">
            <span class="job-date">{{ formatDate(job.createdAt) }}</span>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="loading-state">
        <va-progress-circle indeterminate color="purple" />
        <p>Cargando empleos destacados...</p>
      </div>

      <!-- Empty state -->
      <div v-if="!loading && displayedJobs.length === 0" class="empty-state">
        <va-icon name="work_off" size="3rem" color="#D1D5DB" />
        <p>No hay empleos destacados disponibles en este momento</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// ==========================================
// DATA
// ==========================================
const jobs = ref([])
const loading = ref(true)
const error = ref(null)

// ==========================================
// COMPUTED
// ==========================================
const displayedJobs = computed(() => {
  return jobs.value
})

// ==========================================
// METHODS
// ==========================================
/**
 * Genera un número aleatorio determinístico basado en un seed
 * Usa el algoritmo Mulberry32 para generar números pseudo-aleatorios
 */
const seededRandom = (seed) => {
  let state = seed
  return () => {
    state = (state + 0x6D2B79F5) | 0
    let t = Math.imul(state ^ (state >>> 15), 1 | state)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

/**
 * Mezcla un array de forma determinística usando una fecha como seed
 * @param {Array} array - Array a mezclar
 * @param {Date} date - Fecha para usar como seed
 */
const shuffleWithDateSeed = (array, date) => {
  // Crear seed basado en día/mes/año (mismo seed todo el día)
  const seed = date.getFullYear() * 10000 + (date.getMonth() + 1) * 100 + date.getDate()
  const rng = seededRandom(seed)

  // Algoritmo Fisher-Yates con RNG determinístico
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }

  return shuffled
}

const fetchFeaturedJobs = async () => {
  try {
    loading.value = true
    error.value = null

    // Llamar a la API para obtener todos los trabajos activos
    const response = await axios.get('http://localhost:8000/api/jobs/')

    // La respuesta tiene estructura: {success, count, jobs: [...]}
    const allJobs = response.data.jobs || response.data || []

    // Filtrar solo los trabajos con plan purpura o impulso
    const featuredJobs = allJobs.filter(job =>
      job.plan === 'purpura' || job.plan === 'impulso'
    )

    // Separar por tipo de plan
    const impulsoJobs = featuredJobs.filter(job => job.plan === 'impulso')
    const purpuraJobs = featuredJobs.filter(job => job.plan === 'purpura')

    // Fecha de hoy (sin hora para que sea consistente todo el día)
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    // Mezclar cada grupo de forma determinística basada en la fecha de hoy
    const shuffledImpulso = shuffleWithDateSeed(impulsoJobs, today)
    const shuffledPurpura = shuffleWithDateSeed(purpuraJobs, today)

    // Combinar: primero los impulso mezclados, luego los purpura mezclados
    // Esto garantiza que "Patrocinado" siempre tenga prioridad
    const rotatedJobs = [...shuffledImpulso, ...shuffledPurpura]

    jobs.value = rotatedJobs

    console.log(`📊 Empleos destacados cargados: ${rotatedJobs.length} (${impulsoJobs.length} Patrocinados, ${purpuraJobs.length} Destacados)`)
    console.log(`🎲 Rotación diaria activa - Seed: ${today.toISOString().split('T')[0]}`)
  } catch (err) {
    console.error('Error fetching featured jobs:', err)
    error.value = 'Error al cargar los empleos destacados'
    jobs.value = []
  } finally {
    loading.value = false
  }
}

const formatSalary = (job) => {
  if (job.salaryType === 'negotiable') {
    return 'Salario a convenir'
  } else if (job.salaryType === 'fixed' && job.salaryFixed) {
    return `Bs. ${parseFloat(job.salaryFixed).toLocaleString('es-BO')}/mes`
  } else if (job.salaryType === 'range' && job.salaryMin && job.salaryMax) {
    return `Bs. ${parseFloat(job.salaryMin).toLocaleString('es-BO')} - ${parseFloat(job.salaryMax).toLocaleString('es-BO')}/mes`
  }
  return null
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0 || diffDays === 1) return 'Hoy'
  if (diffDays === 2) return 'Ayer'
  if (diffDays < 7) return `Hace ${diffDays - 1} días`
  if (diffDays < 30) {
    const weeks = Math.floor(diffDays / 7)
    return `Hace ${weeks} ${weeks === 1 ? 'semana' : 'semanas'}`
  }
  const months = Math.floor(diffDays / 30)
  return `Hace ${months} ${months === 1 ? 'mes' : 'meses'}`
}

const isNew = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays <= 3 // Consideramos "nuevo" si tiene 3 días o menos
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
  await fetchFeaturedJobs()
})
</script>

<style scoped>
/* ==========================================
   SECCIÓN - ESTILO OLX LIMPIO
   ========================================== */
.featured-jobs-section {
  width: 100%;
  padding: 4rem 2rem;
  background: #F9FAFB;
}

.jobs-container {
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.5rem 0;
}

.section-subtitle {
  font-size: 0.9375rem;
  color: #6B7280;
  margin: 0;
}

.btn-see-all-top {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  color: #374151;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-see-all-top:hover {
  border-color: var(--color-purple);
  color: var(--color-purple);
  transform: translateX(4px);
}

/* Grid */
.jobs-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

/* ==========================================
   TARJETA - ESTILO OLX
   ========================================== */
.job-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 1.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  position: relative;
}

.job-card:hover {
  border-color: var(--color-purple);
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.08);
  transform: translateY(-2px);
}

/* Badges */
.card-badges {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.badge {
  font-size: 0.7rem;
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  font-weight: 600;
  white-space: nowrap;
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

/* Contenido */
.card-content {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.company-logo {
  width: 60px;
  height: 60px;
  min-width: 60px;
  border-radius: 8px;
  border: 1px solid #E5E7EB;
  background: #F9FAFB;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.company-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 0.5rem;
}

.job-main-info {
  flex: 1;
  min-width: 0;
}

.job-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.375rem 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.company-name {
  font-size: 0.875rem;
  color: #6B7280;
  margin: 0 0 0.625rem 0;
  font-weight: 500;
}

.job-metadata {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: #6B7280;
  margin-bottom: 0.625rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.meta-divider {
  color: #D1D5DB;
}

.job-salary {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #10B981;
  margin: 0;
}

/* Footer */
.card-footer {
  padding-top: 0.875rem;
  border-top: 1px solid #E5E7EB;
  margin-top: auto;
}

.job-date {
  font-size: 0.75rem;
  color: #9CA3AF;
}

/* Loading state */
.loading-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-state p {
  color: #6B7280;
  font-size: 0.9375rem;
}

/* Empty state */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 2rem;
}

.empty-state p {
  margin-top: 1rem;
  color: #6B7280;
  font-size: 0.9375rem;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1200px) {
  .jobs-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .jobs-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .btn-see-all-top {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .featured-jobs-section {
    padding: 3rem 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .section-subtitle {
    font-size: 0.875rem;
  }

  .jobs-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  /* 📱 MÓVIL: Cambiar a diseño horizontal tipo lista */
  .job-card {
    padding: 1rem;
    flex-direction: column;
    gap: 0;
  }

  .card-badges {
    margin-bottom: 0.75rem;
    order: 1;
  }

  .card-content {
    flex-direction: row;
    gap: 0.75rem;
    order: 2;
    margin-bottom: 0.5rem;
  }

  .card-footer {
    order: 3;
    border-top: none;
    padding-top: 0;
    margin-top: 0;
    display: flex;
    justify-content: flex-end;
  }

  .company-logo {
    width: 64px;
    height: 64px;
    min-width: 64px;
  }

  .job-main-info {
    flex: 1;
  }

  .job-title {
    font-size: 0.9375rem;
    -webkit-line-clamp: 1;
    margin-bottom: 0.25rem;
  }

  .company-name {
    font-size: 0.8125rem;
    margin-bottom: 0.375rem;
  }

  .job-metadata {
    font-size: 0.75rem;
    gap: 0.375rem;
    margin-bottom: 0.375rem;
  }

  .job-salary {
    font-size: 0.875rem;
  }

  .job-date {
    font-size: 0.6875rem;
  }
}

@media (max-width: 480px) {
  .featured-jobs-section {
    padding: 2rem 0.75rem;
  }

  .section-title {
    font-size: 1.375rem;
  }

  .job-card {
    padding: 0.875rem;
  }

  .badge {
    font-size: 0.625rem;
    padding: 0.1875rem 0.5rem;
  }

  .company-logo {
    width: 56px;
    height: 56px;
    min-width: 56px;
  }

  .job-title {
    font-size: 0.875rem;
  }

  .company-name {
    font-size: 0.75rem;
  }

  .job-metadata {
    font-size: 0.6875rem;
  }

  .job-salary {
    font-size: 0.8125rem;
  }
}
</style>
