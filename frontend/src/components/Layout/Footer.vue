<template>
  <!-- 
    Footer.vue - Pie de página del sitio
    
    Propósito: Información de contacto, enlaces y newsletter
    Conecta con: MainLayout.vue (componente padre)
    Ubicación: Parte inferior de todas las páginas
  -->
  <footer class="footer">
    <!-- Sección Principal del Footer -->
    <div class="footer-top">
      <div class="footer-container">
        <!-- Columna: Sobre Nosotros -->
        <div class="footer-col">
          <div class="footer-logo">
            <div class="logo-icon">
              <VaIcon name="bookmark" size="large" />
            </div>
            <h3>Guías Púrpuras</h3>
          </div>
          <p class="footer-desc">
            Creemos que Bolivia está llena de talento, esfuerzo y creatividad, pero que ese
            potencial se pierde en el ruido de redes caóticas y plataformas impersonales. Por eso
            creamos Guías Púrpuras, un ecosistema digital diseñado para ordenar el caos y
            conectar a las personas con oportunidades reales.
            No somos una simple app de clasificados. Somos una red viva de servicios profesionales,
            empresas y PyMe, empleos y gastronomía, organizada, clara y moderna. Un espacio donde lo
            boliviano se ve bien, se encuentra fácil y se valora.
            No venimos a competir con las redes sociales; venimos a complementarlas, trayendo
            orden, diseño y propósito al mundo digital boliviano
          </p>
          <!-- Redes Sociales -->
          <div class="social-links">
            <a href="#" class="social-link" aria-label="Facebook">
              <VaIcon name="facebook" />
            </a>
            <a href="#" class="social-link" aria-label="Twitter">
              <VaIcon name="share" />
            </a>
            <a href="#" class="social-link" aria-label="Instagram">
              <VaIcon name="camera_alt" />
            </a>
            <a href="#" class="social-link" aria-label="LinkedIn">
              <VaIcon name="link" />
            </a>
          </div>
        </div>

        <!-- Columna: Enlaces Rápidos -->
        <div class="footer-col">
          <h4>Enlaces Rápidos</h4>
          <ul class="footer-links">
            <li><a href="#">Acerca de Nosotros</a></li>
            <li><a href="#">Cómo Funciona</a></li>
            <li><a href="#">Precios y Planes</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Contacto</a></li>
          </ul>
        </div>

        <!-- Columna: Categorías -->
        <div class="footer-col">
          <h4>Categorías</h4>
          <ul class="footer-links">
            <li><a href="#">Guías Profesionales</a></li>
            <li><a href="#">Guías Gastronómicas</a></li>
            <li><a href="#">Guías de Trabajos</a></li>
            <li><a href="#">Guías de Servicios</a></li>
          </ul>
        </div>

        <!-- Columna: Newsletter -->
        <div class="footer-col">
          <h4>Newsletter</h4>
          <p class="newsletter-text">Recibe las mejores ofertas directamente en tu correo</p>
          <div class="newsletter-form">
            <input 
              type="email" 
              placeholder="Tu correo electrónico" 
              v-model="newsletterEmail"
            />
            <VaButton 
              class="newsletter-btn" 
              icon="send" 
              @click="subscribeNewsletter"
            >
              Suscribir
            </VaButton>
          </div>
          <!-- Badges de Apps -->
          <div class="app-badges">
            <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Google Play" />
            <img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Download_on_the_App_Store_Badge.svg" alt="App Store" />
          </div>
        </div>
      </div>
    </div>

    <!-- Barra Inferior del Footer -->
    <div class="footer-bottom">
      <div class="footer-container">
        <p class="copyright">&copy; 2025 Guías Púrpuras. Todos los derechos reservados.</p>
        <div class="footer-bottom-links">
          <a href="#">Términos y Condiciones</a>
          <span class="separator">|</span>
          <a href="#">Política de Privacidad</a>
          <span class="separator">|</span>
          <a href="#">Cookies</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
/**
 * Footer Component
 * 
 * State:
 * - newsletterEmail: email del usuario para suscripción
 * 
 * Methods:
 * - subscribeNewsletter: envía email al backend para suscripción
 */

export default {
  name: 'Footer',
  data() {
    return {
      newsletterEmail: ''
    }
  },
  methods: {
    subscribeNewsletter() {
      if (!this.newsletterEmail) {
        console.warn('Email vacío')
        return
      }
      
      console.log('Suscribir email:', this.newsletterEmail)
      // TODO: Conectar con Django API endpoint /api/newsletter/subscribe/
      
      // Limpiar campo después de enviar
      this.newsletterEmail = ''
    }
  }
}
</script>

<style scoped>
/**
 * Estilos del Footer
 * Usa variables CSS de App.vue
 */

.footer {
  background: var(--color-purple-dark);
  color: #ffffff;
  margin-top: 5rem;
  width: 100%;
}

/* Sección Principal */
.footer-top {
  padding: 4rem 0 2rem;
}

.footer-container {
  max-width: 100%;
  padding: 0 3rem;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 3rem;
}

.footer-col h3,
.footer-col h4 {
  color: #ffffff;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

/* Logo del Footer */
.footer-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.footer-logo .logo-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-orange-primary) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
}

.footer-desc {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

/* Redes Sociales */
.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  text-decoration: none;
  transition: all 0.3s;
}

.social-link:hover {
  background: var(--color-orange-primary);
  transform: translateY(-3px);
}

/* Enlaces del Footer */
.footer-links {
  list-style: none;
}

.footer-links li {
  margin-bottom: 0.75rem;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: var(--color-orange-primary);
}

/* Newsletter */
.newsletter-text {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1rem;
  line-height: 1.6;
}

.newsletter-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.newsletter-form input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  outline: none;
  transition: all 0.3s;
}

.newsletter-form input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.newsletter-form input:focus {
  background: rgba(255, 255, 255, 0.15);
  border-color: var(--color-orange-primary);
}

.newsletter-btn {
  background: var(--color-orange-primary) !important;
  color: #ffffff !important;
}

/* App Badges */
.app-badges {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.app-badges img {
  height: 40px;
  cursor: pointer;
  transition: transform 0.3s;
}

.app-badges img:hover {
  transform: scale(1.05);
}

/* Footer Bottom */
.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem 0;
}

.footer-bottom .footer-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  grid-template-columns: 1fr;
}

.copyright {
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

.footer-bottom-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.footer-bottom-links a {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  transition: color 0.3s;
}

.footer-bottom-links a:hover {
  color: var(--color-orange-primary);
}

.separator {
  color: rgba(255, 255, 255, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .footer-container {
    grid-template-columns: 1fr;
    padding: 0 1.5rem;
  }

  .footer-bottom .footer-container {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .app-badges {
    align-items: center;
  }
}
</style>