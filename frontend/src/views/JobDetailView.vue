<!-- frontend/src/views/JobDetailView.vue -->
<template>
  <MainLayout>
    <section class="job-detail-section">
      <div class="container">
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
                <span class="info-value">{{ job.category }}</span>
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
          <div class="action-buttons">
            <va-button
              @click="applyToJob"
              color="warning"
              size="large"
              class="apply-btn"
              :disabled="job.status !== 'abierta'"
            >
              <va-icon name="send" />
              POSTULAR A ESTE EMPLEO
            </va-button>

            <div class="secondary-actions">
              <va-button
                @click="saveJob"
                preset="secondary"
                icon="bookmark_border"
              >
                Guardar Empleo
              </va-button>
              
              <va-button
                @click="shareJob"
                preset="secondary"
                icon="share"
              >
                Compartir
              </va-button>

              <va-button
                @click="reportJob"
                preset="secondary"
                icon="flag"
              >
                Denunciar
              </va-button>
            </div>
          </div>
        </div>

        <!-- Tabs de Contenido -->
        <div class="content-section">
          <TabNavigation
            v-model="activeTab"
            :tabs="tabs"
          >
            <!-- Tab 1: Detalle del Anuncio -->
            <template #tab-0>
              <div class="tab-content">
                <!-- Descripción de la oferta -->
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="description" size="1.5rem" color="purple" />
                    Descripción de la oferta de empleo
                  </h3>
                  <div class="block-text" v-html="job.description"></div>
                </div>

                <!-- Como nos gustaría que seas (Requisitos) -->
                <div v-if="job.requirements" class="content-block">
                  <h3 class="block-title">
                    <va-icon name="checklist" size="1.5rem" color="purple" />
                    Como nos gustaría que seas:
                  </h3>
                  <ul class="requirements-list">
                    <li 
                      v-for="(requirement, index) in job.requirements" 
                      :key="index"
                    >
                      <va-icon name="check_circle" size="small" color="success" />
                      {{ requirement }}
                    </li>
                  </ul>
                </div>

                <!-- Tus principales responsabilidades -->
                <div v-if="job.responsibilities" class="content-block">
                  <h3 class="block-title">
                    <va-icon name="assignment" size="1.5rem" color="purple" />
                    Tus principales responsabilidades serán:
                  </h3>
                  <ul class="responsibilities-list">
                    <li 
                      v-for="(responsibility, index) in job.responsibilities" 
                      :key="index"
                    >
                      <va-icon name="arrow_right" size="small" color="purple" />
                      {{ responsibility }}
                    </li>
                  </ul>
                </div>

                <!-- Beneficios -->
                <div v-if="job.benefits && job.benefits.length > 0" class="content-block">
                  <h3 class="block-title">
                    <va-icon name="card_giftcard" size="1.5rem" color="purple" />
                    Beneficios
                  </h3>
                  <div class="benefits-grid">
                    <div 
                      v-for="(benefit, index) in job.benefits" 
                      :key="index"
                      class="benefit-item"
                    >
                      <va-icon name="check_circle" size="small" color="success" />
                      <span>{{ benefit }}</span>
                    </div>
                  </div>
                </div>

                <!-- CTA de Postulación -->
                <div class="cta-block">
                  <h3>¿Te interesa esta oportunidad?</h3>
                  <p>Postula ahora y forma parte de nuestro equipo</p>
                  <va-button
                    @click="applyToJob"
                    color="warning"
                    size="large"
                    :disabled="job.status !== 'abierta'"
                  >
                    <va-icon name="send" />
                    POSTULAR A ESTE EMPLEO
                  </va-button>
                </div>
              </div>
            </template>

            <!-- Tab 2: Datos de la Empresa -->
            <template #tab-1>
              <div class="tab-content">
                <div class="content-block">
                  <h3 class="block-title">
                    <va-icon name="business" size="1.5rem" color="purple" />
                    Sobre la empresa
                  </h3>

                  <div v-if="!job.confidential" class="company-info">
                    <!-- Logo y nombre -->
                    <div class="company-header">
                      <img 
                        v-if="job.companyLogo" 
                        :src="job.companyLogo" 
                        :alt="job.companyName"
                        class="company-logo-large"
                      />
                      <div>
                        <h4 class="company-name-large">{{ job.companyName }}</h4>
                        <p class="company-sector">{{ job.companySector }}</p>
                      </div>
                    </div>

                    <!-- Descripción -->
                    <div class="company-description">
                      <p>{{ job.companyDescription }}</p>
                    </div>

                    <!-- Info adicional -->
                    <div class="company-details">
                      <div class="detail-item" v-if="job.companySize">
                        <va-icon name="people" />
                        <span><strong>Tamaño:</strong> {{ job.companySize }}</span>
                      </div>
                      <div class="detail-item" v-if="job.companyWebsite">
                        <va-icon name="language" />
                        <a :href="job.companyWebsite" target="_blank">
                          Visitar sitio web
                        </a>
                      </div>
                    </div>

                    <!-- Otros empleos de esta empresa -->
                    <div v-if="otherJobs.length > 0" class="other-jobs">
                      <h4>Otros empleos de {{ job.companyName }}</h4>
                      <div class="jobs-list">
                        <div 
                          v-for="otherJob in otherJobs" 
                          :key="otherJob.id"
                          class="job-item"
                          @click="goToJob(otherJob.id)"
                        >
                          <div class="job-item-title">{{ otherJob.title }}</div>
                          <div class="job-item-meta">
                            <span>{{ otherJob.city }}</span>
                            <span>•</span>
                            <span>{{ otherJob.publishedDaysAgo }} días</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div v-else class="confidential-message">
                    <va-icon name="visibility_off" size="3rem" color="#999" />
                    <p>Esta es una publicación confidencial. La información de la empresa no está disponible públicamente.</p>
                  </div>
                </div>
              </div>
            </template>
          </TabNavigation>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/Layout/MainLayout.vue'
import TabNavigation from '@/components/Common/TabNavigation.vue'

const route = useRoute()
const router = useRouter()
const activeTab = ref(0)

const tabs = [
  { label: 'Detalle del Anuncio', icon: 'description' },
  { label: 'Datos de la Empresa', icon: 'business' }
]

// Mock data - TODO: Reemplazar con API
const job = ref({
  id: 1225662,
  title: 'Técnico(a) Comercial Agrónomo(a)',
  companyName: 'Agropartners S.R.L.',
  companyLogo: 'https://via.placeholder.com/200x80/4CAF50/FFFFFF?text=Agropartners',
  city: 'Santa Cruz de la Sierra',
  contractType: 'Tiempo Completo',
  publishDate: '22/10/2025',
  expiryDate: '21/11/2025',
  category: 'Agricultura y Campo',
  tags: ['Agronomía', 'Ingeniero Agrónomo', 'Agropecuaria'],
  salary: 'No Declarado',
  status: 'abierta',
  plan: 'destacado',
  verified: true,
  confidential: false,
  urgent: false,
  description: `
    <p><strong>¡Tu futuro en el agro comienza aquí!</strong> Sé parte de nuestro Programa Protection Team.</p>
    <br>
    <h4>Técnico(a) Comercial Agrónomo(a)</h4>
    <p>En Agropartners, buscamos a Técnicos(as) Comerciales apasionado(a) por el agro, con visión y ganas de hacer crecer el potencial de nuestros clientes. Tu misión será clave para acompañar a nuestros clientes, brindar visitas y soluciones técnicas e innovadoras y asegurar la prosperidad de sus cultivos, ¡sembrando juntos el éxito en cada parcela!</p>
  `,
  requirements: [
    'Licenciatura en Ingeniería Agronómica, Agropecuaria, Agronegocios o carreras afines.',
    'Experiencia mínima de 2 años en roles técnico-comerciales o de campo en el sector agrícola.',
    'Conocimientos sólidos en manejo de productos agrícolas, protocolos de ensayo, análisis de resultados y desarrollo de productos.',
    'Habilidad para interpretar y presentar datos técnicos de forma clara a equipos internos y clientes.',
    'Deseable: Cursos o formación especializada en protección vegetal y agronegocios.'
  ],
  responsibilities: [
    'Acompañar a nuestros clientes, brindando visitas técnicas e innovadoras',
    'Realizar seguimiento y análisis de cultivos',
    'Desarrollar estrategias de protección vegetal',
    'Mantener relación cercana con productores',
    'Reportar avances y resultados al equipo comercial'
  ],
  benefits: [
    'Seguro médico',
    'Capacitación continua',
    'Vehículo de empresa',
    'Comisiones por ventas',
    'Oportunidades de crecimiento'
  ],
  companySector: 'Agricultura y Agronegocios',
  companySize: '50-200 empleados',
  companyDescription: 'Agropartners es una empresa líder en el sector agrícola de Bolivia, especializada en soluciones innovadoras para el agro. Contamos con más de 15 años de experiencia en el mercado y un equipo comprometido con el desarrollo sostenible del sector.',
  companyWebsite: 'https://agropartners.com.bo'
})

const otherJobs = ref([
  { id: 2, title: 'Ingeniero Agrónomo Senior', city: 'Santa Cruz', publishedDaysAgo: 5 },
  { id: 3, title: 'Asistente de Campo', city: 'Santa Cruz', publishedDaysAgo: 12 }
])

const getCompanyDisplayName = computed(() => {
  if (job.value.confidential) {
    return 'Publicación Confidencial'
  }
  if (job.value.importantCompany) {
    return 'Importante Empresa'
  }
  return job.value.companyName
})

const applyToJob = () => {
  // TODO: Navegar a proceso de postulación
  router.push(`/guias/trabajos/${job.value.id}/postular`)
}

const saveJob = () => {
  console.log('Guardar empleo')
  // TODO: Implementar favoritos
}

const shareJob = () => {
  console.log('Compartir empleo')
  // TODO: Implementar compartir
}

const reportJob = () => {
  console.log('Denunciar empleo')
  // TODO: Implementar reporte
}

const goToJob = (jobId) => {
  router.push(`/guias/trabajos/${jobId}`)
}

const fetchJob = async () => {
  const jobId = route.params.id
  
  try {
    // TODO: Llamada real a la API
    // const response = await fetch(`/api/jobs/${jobId}/`)
    // job.value = await response.json()
    
    console.log('Cargando trabajo:', jobId)
  } catch (error) {
    console.error('Error cargando trabajo:', error)
  }
}

onMounted(() => {
  fetchJob()
})
</script>

<style scoped>
.job-detail-section {
  min-height: calc(100vh - 200px);
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* ========== Breadcrumb ========== */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  font-size: 0.95rem;
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

/* ========== Header Card ========== */
.job-header {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  margin-bottom: 2rem;
  display: grid;
  grid-template-columns: 200px 1fr auto;
  gap: 2.5rem;
  align-items: start;
}

.job-logo {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  background: #F5F5F5;
  border: 2px solid #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.job-logo img {
  max-width: 180px;
  max-height: 180px;
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

.badge-verified {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  background: #4CAF50;
  color: white;
  padding: 0.4rem 0.875rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.4);
}

.job-info {
  flex: 1;
}

.badges-row {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.badge-plan {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.badge-plan.destacado {
  background: var(--color-yellow-primary);
  color: var(--color-purple-darkest);
}

.badge-plan.premium {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #333;
}

.badge-urgent {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(244, 67, 54, 0.1);
  color: #D32F2F;
}

.job-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.company-name {
  font-size: 1.125rem;
  color: #666;
  margin: 0 0 1.5rem 0;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 1.25rem;
  background: #F8F8F8;
  border-radius: 12px;
}

.info-item {
  display: flex;
  gap: 0.5rem;
  font-size: 0.95rem;
}

.info-label {
  font-weight: 600;
  color: #666;
  min-width: 100px;
}

.info-value {
  color: #333;
}

.tags-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.tags-label {
  font-weight: 600;
  color: #666;
  font-size: 0.95rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.35rem 0.75rem;
  background: rgba(92, 0, 153, 0.08);
  color: var(--color-purple);
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.salary-box {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(46, 125, 50, 0.05) 100%);
  border-left: 4px solid #4CAF50;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.salary-label {
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
}

.salary-value {
  font-size: 1.125rem;
  font-weight: 700;
  color: #2E7D32;
}

.status-box {
  padding: 0.875rem 1.25rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.status-box.abierta {
  background: rgba(76, 175, 80, 0.1);
  color: #2E7D32;
  border-left: 4px solid #4CAF50;
}

.status-box.cerrada {
  background: rgba(158, 158, 158, 0.1);
  color: #666;
  border-left: 4px solid #999;
}

.job-id {
  font-size: 0.85rem;
  color: #999;
}

/* ========== Action Buttons ========== */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 250px;
}

.apply-btn {
  font-size: 1.05rem !important;
  font-weight: 700 !important;
  padding: 1.25rem 1.5rem !important;
}

.secondary-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* ========== Content Section ========== */
.content-section {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.content-block {
  padding: 2rem;
  background: #FAFAFA;
  border-radius: 12px;
}

.block-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1.5rem 0;
}

.block-text {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #333;
}

.requirements-list,
.responsibilities-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.requirements-list li,
.responsibilities-list li {
  display: flex;
  align-items: start;
  gap: 0.75rem;
  font-size: 1.05rem;
  line-height: 1.6;
  color: #333;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  background: white;
  border-radius: 8px;
  font-size: 1rem;
  color: #333;
  border: 1px solid #E0E0E0;
}

/* ========== CTA Block ========== */
.cta-block {
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  color: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
}

.cta-block h3 {
  font-size: 1.75rem;
  margin: 0 0 0.5rem 0;
}

.cta-block p {
  font-size: 1.05rem;
  margin: 0 0 2rem 0;
  opacity: 0.9;
}

/* ========== Company Info ========== */
.company-info {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.company-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #E0E0E0;
}

.company-logo-large {
  width: 120px;
  height: 120px;
  object-fit: contain;
  border: 2px solid #E0E0E0;
  border-radius: 12px;
  padding: 1rem;
  background: white;
}

.company-name-large {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.company-sector {
  font-size: 1rem;
  color: #666;
  margin: 0;
}

.company-description {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #333;
}

.company-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  color: #333;
}

.detail-item a {
  color: var(--color-purple);
  text-decoration: none;
}

.detail-item a:hover {
  text-decoration: underline;
}

.other-jobs h4 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 1rem 0;
}

.jobs-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.job-item {
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border: 2px solid #E0E0E0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.job-item:hover {
  border-color: var(--color-purple);
  transform: translateX(4px);
}

.job-item-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--color-purple-darkest);
  margin-bottom: 0.35rem;
}

.job-item-meta {
  font-size: 0.9rem;
  color: #666;
  display: flex;
  gap: 0.5rem;
}

.confidential-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: #666;
}

.confidential-message p {
  max-width: 500px;
  font-size: 1.05rem;
  line-height: 1.6;
  margin-top: 1rem;
}

/* ========== Responsive ========== */
@media (max-width: 1024px) {
  .job-header {
    grid-template-columns: 160px 1fr;
    gap: 2rem;
  }

  .job-logo {
    width: 160px;
    height: 160px;
  }

  .action-buttons {
    grid-column: 1 / -1;
    flex-direction: row;
    min-width: auto;
  }

  .secondary-actions {
    flex-direction: row;
    flex: 1;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .benefits-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .job-detail-section {
    padding: 1.5rem 1rem;
  }

  .job-header {
    grid-template-columns: 1fr;
    padding: 1.5rem;
    gap: 1.5rem;
  }

  .job-logo {
    width: 100%;
    height: 200px;
  }

  .job-title {
    font-size: 1.5rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .secondary-actions {
    flex-direction: column;
  }

  .content-section {
    padding: 1.5rem;
  }

  .content-block {
    padding: 1.5rem;
  }

  .block-title {
    font-size: 1.25rem;
  }

  .cta-block {
    padding: 2rem 1.5rem;
  }

  .cta-block h3 {
    font-size: 1.5rem;
  }
}
</style>