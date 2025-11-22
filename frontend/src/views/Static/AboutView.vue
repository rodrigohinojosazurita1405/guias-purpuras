<!-- frontend/src/views/Static/AboutView.vue -->
<template>
  <MainLayout>
    <!-- Hero Section -->
    <section class="about-hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="hero-badge">
          <va-icon name="info" size="small" />
          <span>Sobre Nosotros</span>
        </div>
        <h1 class="hero-title">
          Conectando el <span class="highlight">Talento Boliviano</span>
        </h1>
        <p class="hero-subtitle">
          Somos más que una plataforma. Somos el puente entre oportunidades y personas en Bolivia.
        </p>
      </div>
    </section>

    <!-- Nuestra Historia -->
    <section class="about-section our-story">
      <div class="section-container">
        <div class="section-grid">
          <div class="content-col">
            <div class="section-badge">
              <va-icon name="history" />
              <span>Nuestra Historia</span>
            </div>
            <h2 class="section-title">¿Por qué creamos Guías Púrpuras?</h2>
            <div class="text-content">
              <p>
                <strong> El Problema que Vimos:</strong><i> El Caos Oculta el Talento:</i><br>
                Creemos firmemente que Bolivia está llena de talento, esfuerzo y una creatividad que merece ser vista. 
                Sin embargo, ese potencial a menudo se diluye y se pierde en el ruido caótico de redes sociales impersonales y 
                plataformas digitales dispersas, a menudo miles de usuarios en Bolivia recurren a grupos de Facebook como 
                ¿Alguien sabe?, ¿Alguien conoce? o variantes similares buscando información, recomendaciones, lugares entre otros. 
                Es ahí donde encontramos una profunda necesidad de orden y claridad.
              </p>
              <p>
               <strong> La Inspiración en las Clásicas Guias Telofónicas:</strong> <i>Recuperando la Confianza:</i> <br>
                Nuestra base conceptual rinde homenaje a la utilidad y la confiabilidad de las antiguas guías telefónicas. 
                Eran la herramienta esencial: lo buscabas, lo encontrabas y funcionaba. 
                <strong>Guías Púrpuras</strong> nace con el compromiso de replicar esa sensación de acceso fácil y seguro, 
                pero modernizada para la era digital. 
                Nuestro objetivo es devolver la confianza al encuentro entre quienes buscan y quienes ofrecen.
              </p>
               <p>
               <strong>El Color que lo Transforma Todo:</strong><i> La Filosofía de la Vaca Púrpura:</i> <br>
                Una guía útil es buena, pero una Guía Púrpura es inolvidable.
                El color púrpura es nuestro compromiso con la diferenciación. 
                Inspirados en el concepto de la Vaca Púrpura de Seth Godin, nos negamos a ser otra plataforma genérica como los muchos
                que existen en Bolivia, ocea (una "vaca marrón"). 
                <b><i> "Somos el destino donde lo extraordinario se encuentra con la utilidad".</i></b> <br>
                <b>Para el usuario:</b> Somos el filtro que destaca lo mejor de Bolivia. <br>
                <b>Para el negocio Boliviano:</b> Somos la plataforma que te ayuda a ser esa Vaca Púrpura, la opción visible y preferida en tu mercado.
              </p>
              <p>
                Por eso creamos <strong>Guías Púrpuras</strong>, un ecosistema digital diseñado 
                para ordenar el caos y conectar a las personas con oportunidades reales.
              </p>
              <p>
                
              </p>
              <p>
                No somos una simple app de comidas o un portal de empleos. Somos una red viva de servicios profesionales, 
                empresas PyMe, ofertas laborales y gastronomía, organizada, clara y moderna.
              </p>
              <p>
                Un espacio donde lo Boliviano se ve bien, se encuentra fácil y se valora.
              </p>
            </div>
          </div>
          <div class="image-col">
            <div class="image-card">
              <img 
                :src="historyImage" 
                alt="Historia de Guías Púrpuras" 
                class="history-image"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Misión y Visión -->
    <section class="about-section mission-vision">
      <div class="section-container">
        <div class="mv-grid">
          <div class="mv-card mission">
            <div class="mv-icon">
              <va-icon name="flag" size="large" />
            </div>
            <h3>Nuestra Misión</h3>
            <p>
              Conectar el talento, empresas y oportunidades de Bolivia en un ecosistema digital 
              organizado, moderno y accesible para todos. Facilitamos el encuentro entre quienes 
              buscan y quienes ofrecen, eliminando barreras y generando valor real.
            </p>
          </div>

          <div class="mv-card vision">
            <div class="mv-icon">
              <va-icon name="visibility" size="large" />
            </div>
            <h3>Nuestra Visión</h3>
            <p>
              Ser la plataforma líder en Bolivia para descubrir profesionales, negocios, empleos 
              y gastronomía, reconocida por su diseño, confiabilidad y impacto positivo en la 
              economía local. Queremos que cada boliviano encuentre lo que busca en un solo lugar.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Valores -->
    <section class="about-section values">
      <div class="section-container">
        <div class="section-header-center">
          <div class="section-badge">
            <va-icon name="favorite" />
            <span>Nuestros Valores</span>
          </div>
          <h2 class="section-title">Lo que nos define</h2>
          <p class="section-subtitle">
            Principios que guían cada decisión y acción en Guías Púrpuras
          </p>
        </div>

        <div class="values-grid">
          <div class="value-card">
            <div class="value-icon">
              <va-icon name="verified_user" size="large" />
            </div>
            <h4>Confianza</h4>
            <p>
              Verificamos y validamos cada anuncio para garantizar información real y confiable.
            </p>
          </div>

          <div class="value-card">
            <div class="value-icon">
              <va-icon name="palette" size="large" />
            </div>
            <h4>Diseño</h4>
            <p>
              Creemos que lo boliviano merece verse bien. Cuidamos cada detalle visual.
            </p>
          </div>

          <div class="value-card">
            <div class="value-icon">
              <va-icon name="groups" size="large" />
            </div>
            <h4>Comunidad</h4>
            <p>
              Construimos un espacio donde todos pueden crecer, conectar y prosperar juntos.
            </p>
          </div>

          <div class="value-card">
            <div class="value-icon">
              <va-icon name="lightbulb" size="large" />
            </div>
            <h4>Innovación</h4>
            <p>
              Mejoramos constantemente, adaptándonos a las necesidades de los bolivianos.
            </p>
          </div>

          <div class="value-card">
            <div class="value-icon">
              <va-icon name="balance" size="large" />
            </div>
            <h4>Transparencia</h4>
            <p>
              Operamos con honestidad, precios claros y sin costos ocultos para nadie.
            </p>
          </div>

          <div class="value-card">
            <div class="value-icon">
              <va-icon name="local_fire_department" size="large" />
            </div>
            <h4>Pasión</h4>
            <p>
              Amamos Bolivia y trabajamos con dedicación para impulsar su crecimiento digital.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Equipo (2 personas) -->
    <section class="about-section team">
      <div class="section-container">
        <div class="section-header-center">
          <div class="section-badge">
            <va-icon name="group" />
            <span>Nuestro Equipo</span>
          </div>
          <h2 class="section-title">Conoce a las personas detrás de Guías Púrpuras</h2>
          <p class="section-subtitle">
            Un equipo comprometido con el crecimiento digital de Bolivia
          </p>
        </div>

        <div class="team-grid">
          <div class="team-card">
            <div class="team-photo">
              <img 
                :src="teamMember1" 
                alt="Fundador de Guías Púrpuras" 
                class="team-image"
              />
            </div>
            <h4>Rodrigo Hinojosa Zurita</h4>
            <p class="team-role">CEO & Fundador</p>
            <p class="team-bio">Nacido en la bella Ciudad de Cochabamba, titulado de la carrera
              de Sistemas Informáticos, Mercadotecnia y Abogado de profesión: Experiencia en Desarrollo
              Frontend y Backend, experto en Marketing Digital y registro de Marcas. 
            </p>
          </div>

          <div class="team-card">
            <div class="team-photo">
              <img 
                :src="teamMember2" 
                alt="Director de Tecnología" 
                class="team-image"
              />
            </div>
            <h4>María Eugenia Varquera Santa Cruz</h4>
            <p class="team-role">Directora de Marketing y Comunicación</p>
            <p class="team-bio">Nacida en la bella ciudad  de Cochabamba: Experta en diseño publicitario branding corporativo y atención al cliente</p>
          </div>
        </div>
      </div>
    </section>

    <!-- TECH STACK SLIDER - NUEVA SECCIÃ"N -->
    <section class="about-section tech-stack">
      <div class="section-container">
        <div class="section-header-center">
          <div class="section-badge">
            <va-icon name="code" />
            <span>Tecnología</span>
          </div>
          <h2 class="section-title">Construido con tecnología de vanguardia</h2>
          <p class="section-subtitle">
            Utilizamos tecnologias modernas acorde a nuestra época para garantizar velocidad, seguridad y escalabilidad
          </p>
        </div>

        <!-- Slider con scroll infinito -->
        <div class="tech-slider-wrapper">
          <div class="tech-slider">
            <!-- Primera iteración de logos -->
            <div class="tech-logo-item">
              <img :src="techLogos.vue" alt="Vue.js" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.javascript" alt="JavaScript" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.django" alt="Django" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.python" alt="Python" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.postgresql" alt="PostgreSQL" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.graphql" alt="GraphQL" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.git" alt="Git" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.typescritp" alt="Typescript" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.nginx" alt="Nginx" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.aws" alt="AWS" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.mongo" alt="MongoDB" class="tech-logo" />
            </div>
            

            <!-- Segunda iteración (duplicado para efecto infinito) -->
            <div class="tech-logo-item">
              <img :src="techLogos.vue" alt="Vue.js" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.javascript" alt="JavaScript" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.django" alt="Django" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.python" alt="Python" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.postgresql" alt="PostgreSQL" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.graphql" alt="GraphQL" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.git" alt="Git" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.typescritp" alt="Typescript" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.nginx" alt="Nginx" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.aws" alt="AWS" class="tech-logo" />
            </div>
            <div class="tech-logo-item">
              <img :src="techLogos.mongo" alt="MongoDB" class="tech-logo" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Final - MEJORADO -->
    <section class="about-cta">
      <div class="cta-container">
        <div class="cta-content">
          <div class="cta-badge">
            <va-icon name="star" size="small" />
            <span>Únete a la comunidad</span>
          </div>
          <h2>¿Listo para dar el siguiente paso?</h2>
          <p>Únete a miles de bolivianos que ya confían en Guías Púrpuras para conectar con oportunidades reales</p>
          
          <div class="cta-buttons">
            <va-button 
              size="large" 
              class="cta-btn-primary"
              @click="goToPublish"
            >
              <va-icon name="add_circle" />
              Empieza ¡AHORA!
            </va-button>
            <va-button 
              size="large" 
              class="cta-btn-secondary"
              @click="goToHome"
            >
              <va-icon name="explore" />
              Explorar Guías
            </va-button>
          </div>

          <div class="cta-features">
            <div class="cta-feature">
              <va-icon name="check_circle" />
              <span>Anuncios reales</span>
            </div>
            <div class="cta-feature">
              <va-icon name="check_circle" />
              <span>100% Intuitivo</span>
            </div>
            <div class="cta-feature">
              <va-icon name="check_circle" />
              <span>Resultados Inmediatos</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import MainLayout from '@/components/Layout/MainLayout.vue'

// ============================================
// IMPORTAR IMÃGENES DEL EQUIPO E HISTORIA
// ============================================
import historyImage from '@/assets/images/amarillas.png'
import teamMember1 from '@/assets/images/ceo.jpg'
import teamMember2 from '@/assets/images/creativo.png'

// ============================================
// IMPORTAR LOGOS DE TECNOLOGÃAS
// ============================================
// TODO: Coloca los logos de tecnologías en: frontend/src/assets/images/tech/
// Descarga los logos en formato PNG o SVG desde: https://simpleicons.org
// Nombres sugeridos para los archivos:
// - vue.png (o vue.svg)
// - vuestic.png
// - javascript.png
// - django.png
// - python.png
// - postgresql.png
// - graphql.png
// - django-rest.png
// - git.png

import vueLogoImg from '@/assets/images/tech/vue-svgrepo-com.svg'
import javascriptLogoImg from '@/assets/images/tech/javascript-svgrepo-com.svg'
import djangoLogoImg from '@/assets/images/tech/django-svgrepo-com.svg'
import pythonLogoImg from '@/assets/images/tech/python-svgrepo-com.svg'
import postgresqlLogoImg from '@/assets/images/tech/pgsql-svgrepo-com.svg'
import graphqlLogoImg from '@/assets/images/tech/graphql-svgrepo-com.svg'
import gitLogoImg from '@/assets/images/tech/git-svgrepo-com.svg'
import typescriptLogoImg from '@/assets/images/tech/typescript-official-svgrepo-com.svg'
import nginxLogoImg from '@/assets/images/tech/nginx-svgrepo-com.svg'
import awsLogoImg from '@/assets/images/tech/aws-svgrepo-com.svg'
import mongoLogoImg from '@/assets/images/tech/mongo-svgrepo-com.svg'

const techLogos = {
  vue: vueLogoImg,
  javascript: javascriptLogoImg,
  django: djangoLogoImg,
  python: pythonLogoImg,
  postgresql: postgresqlLogoImg,
  graphql: graphqlLogoImg,
  git: gitLogoImg,
  typescritp: typescriptLogoImg,
  nginx: nginxLogoImg,
  aws: awsLogoImg,
  mongo: mongoLogoImg,
}

const router = useRouter()

const goToPublish = () => {
  router.push('/publicar')
}

const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
/* ==========================================
   HERO SECTION
   ========================================== */
.about-hero {
  position: relative;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-purple-dark) 0%, var(--color-purple) 100%);
  overflow: hidden;
  padding: 4rem 2rem;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
  background-size: cover;
  opacity: 0.3;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.15);
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-title .highlight {
  color: var(--color-yellow-primary);
}

.hero-subtitle {
  font-size: 1.35rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
}

/* ==========================================
   SECTIONS
   ========================================== */
.about-section {
  padding: 5rem 0;
}

.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(92, 0, 153, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-purple);
  margin-bottom: 1rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-purple-darkest);
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 1.15rem;
  color: #666;
  margin-bottom: 3rem;
  line-height: 1.6;
}

.section-header-center {
  text-align: center;
  margin-bottom: 4rem;
}

/* ==========================================
   NUESTRA HISTORIA
   ========================================== */
.our-story {
  background: #FAFAFA;
}

.section-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.text-content p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #555;
  margin-bottom: 1.5rem;
}

.text-content strong {
  color: var(--color-purple);
  font-weight: 700;
}

.image-card {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.history-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ==========================================
   MISIÃ"N Y VISIÃ"N
   ========================================== */
.mission-vision {
  background: white;
}

.mv-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

.mv-card {
  padding: 3rem;
  border-radius: 20px;
  background: #FAFAFA;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.mv-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
}

.mv-card.mission {
  border-color: var(--color-purple);
}

.mv-card.vision {
  border-color: var(--color-yellow-primary);
}

.mv-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.mission .mv-icon {
  background: rgba(92, 0, 153, 0.1);
  color: var(--color-purple);
}

.vision .mv-icon {
  background: rgba(253, 197, 0, 0.1);
  color: var(--color-yellow-primary);
}

.mv-card h3 {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 1rem;
}

.mv-card p {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #666;
}

/* ==========================================
   VALORES
   ========================================== */
.values {
  background: #FAFAFA;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.value-card {
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 16px;
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.value-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  border-color: var(--color-purple);
}

.value-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  background: rgba(92, 0, 153, 0.1);
  color: var(--color-purple);
  display: flex;
  align-items: center;
  justify-content: center;
}

.value-card h4 {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 1rem;
}

.value-card p {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #666;
}

/* ==========================================
   EQUIPO (2 PERSONAS)
   ========================================== */
.team {
  background: white;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3rem;
  max-width: 800px;
  margin: 0 auto;
}

.team-card {
  text-align: center;
  background: #FAFAFA;
  padding: 2rem;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.team-photo {
  width: 150px;
  height: 150px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid var(--color-purple);
  box-shadow: 0 5px 20px rgba(92, 0, 153, 0.2);
}

.team-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.team-card h4 {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin-bottom: 0.5rem;
}

.team-role {
  font-size: 0.95rem;
  color: var(--color-purple);
  font-weight: 600;
  margin-bottom: 1rem;
}

.team-bio {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #666;
}

/* ==========================================
   TECH STACK SLIDER - NUEVO
   ========================================== */
.tech-stack {
  background: white;
  padding: 4rem 0 5rem;
  overflow: hidden;
}

.tech-slider-wrapper {
  position: relative;
  width: 100%;
  overflow: hidden;
  padding: 2rem 0;
}

/* Efecto fade en los extremos */
.tech-slider-wrapper::before,
.tech-slider-wrapper::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 150px;
  z-index: 2;
  pointer-events: none;
}

.tech-slider-wrapper::before {
  left: 0;
  background: linear-gradient(to right, white, transparent);
}

.tech-slider-wrapper::after {
  right: 0;
  background: linear-gradient(to left, white, transparent);
}

.tech-slider {
  display: flex;
  gap: 4rem;
  animation: scroll-infinite 30s linear infinite;
  width: fit-content;
}

/* Pausa la animación al hacer hover */
.tech-slider:hover {
  animation-play-state: paused;
}

@keyframes scroll-infinite {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

.tech-logo-item {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  height: 80px;
}

.tech-logo {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  filter: grayscale(100%) opacity(0.7);
  transition: all 0.4s ease;
}

/* Efecto hover: recupera color y aumenta opacidad */
.tech-logo-item:hover .tech-logo {
  filter: grayscale(0%) opacity(1);
  transform: scale(1.1);
}

/* ==========================================
   CTA FINAL - MEJORADO
   ========================================== */
.about-cta {
  background: linear-gradient(135deg, var(--color-purple-dark) 0%, var(--color-purple) 100%);
  padding: 6rem 2rem;
  position: relative;
  overflow: hidden;
}

.about-cta::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
}

.about-cta::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -5%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(253, 197, 0, 0.15) 0%, transparent 70%);
  border-radius: 50%;
}

.cta-container {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.cta-content {
  text-align: center;
}

.cta-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(253, 197, 0, 0.2);
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-yellow-primary);
  margin-bottom: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(253, 197, 0, 0.3);
}

.cta-content h2 {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.cta-content p {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 3rem;
  line-height: 1.6;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

.cta-btn-primary {
  --va-background-color: var(--color-yellow-primary) !important;
  color: var(--color-purple-darkest) !important;
  font-weight: 700 !important;
  padding: 1.2rem 2.5rem !important;
  border-radius: 12px !important;
  border: none !important;
  box-shadow: 0 8px 25px rgba(253, 197, 0, 0.4) !important;
  transition: all 0.3s ease !important;
}

.cta-btn-primary:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 12px 35px rgba(253, 197, 0, 0.5) !important;
  background: #FFD633 !important;
}

.cta-btn-secondary {
  background: rgba(255, 255, 255, 0.15) !important;
  color: white !important;
  font-weight: 700 !important;
  padding: 1.2rem 2.5rem !important;
  border-radius: 12px !important;
  border: 2px solid rgba(255, 255, 255, 0.3) !important;
  backdrop-filter: blur(10px) !important;
  transition: all 0.3s ease !important;
}

.cta-btn-secondary:hover {
  transform: translateY(-3px) !important;
  background: rgba(255, 255, 255, 0.25) !important;
  border-color: rgba(255, 255, 255, 0.5) !important;
}

.cta-features {
  display: flex;
  gap: 2.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-feature {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: white;
  font-size: 1rem;
  font-weight: 600;
}

.cta-feature .va-icon {
  color: var(--color-yellow-primary);
  font-size: 1.3rem;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1024px) {
  .section-grid,
  .mv-grid {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .values-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .tech-logo-item {
    min-width: 100px;
    height: 70px;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .values-grid,
  .team-grid {
    grid-template-columns: 1fr;
  }

  .about-section {
    padding: 3rem 0;
  }

  .cta-buttons {
    flex-direction: column;
    gap: 1rem;
  }

  .cta-features {
    flex-direction: column;
    gap: 1rem;
  }

  .cta-content h2 {
    font-size: 2rem;
  }

  .cta-content p {
    font-size: 1.1rem;
  }

  .tech-slider {
    gap: 3rem;
  }

  .tech-logo-item {
    min-width: 80px;
    height: 60px;
  }

  .tech-slider-wrapper::before,
  .tech-slider-wrapper::after {
    width: 80px;
  }
}
</style>