<!-- frontend/src/components/Layout/Footer.vue -->
<template>
  <footer class="footer">
    <!-- Sección Principal del Footer -->
    <div class="footer-top">
      <div class="footer-container">
        <!-- Columna 1: Sobre Nosotros -->
        <div class="footer-col footer-about">
          <div class="footer-logo">
            <img src="/src/assets/guiaspurpuras.ico" alt="Logo" class="logo-icon" />
            <div class="logo-text">
              <h3>Guías Púrpuras</h3>
              <span class="logo-subtitle">Bolivia</span>
            </div>
          </div>
          <p class="footer-desc">
            Somos un ecosistema digital que conecta el talento, gastronomía, empresas PyMe y oportunidades de Bolivia. 
            Organizamos el caos digital de nuestro amada Bolivia con diseño moderno, orden y propósito.
          </p>
          
          <!-- Redes Sociales -->
          <div class="social-section">
            <h4 class="social-title">Síguenos</h4>
            <div class="social-links">
              <a 
                href="https://www.facebook.com/profile.php?id=61582734578250" 
                target="_blank"
                rel="noopener noreferrer"
                class="social-link facebook"
                aria-label="Facebook"
                title="Síguenos en Facebook"
              >
                <svg viewBox="0 0 24 24" width="20" height="20">
                  <path fill="currentColor" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </a>
              
              <a 
                href="https://twitter.com/guiaspurpuras" 
                target="_blank"
                rel="noopener noreferrer"
                class="social-link twitter"
                aria-label="Twitter/X"
                title="Síguenos en X (Twitter)"
              >
                <svg viewBox="0 0 24 24" width="20" height="20">
                  <path fill="currentColor" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </a>
              
              <a 
                href="https://instagram.com/guiaspurpuras" 
                target="_blank"
                rel="noopener noreferrer"
                class="social-link instagram"
                aria-label="Instagram"
                title="Síguenos en Instagram"
              >
                <svg viewBox="0 0 24 24" width="20" height="20">
                  <path fill="currentColor" d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
              </a>
              
              <a 
                href="https://tiktok.com/@guiaspurpuras" 
                target="_blank"
                rel="noopener noreferrer"
                class="social-link tiktok"
                aria-label="TikTok"
                title="Síguenos en TikTok"
              >
                <svg viewBox="0 0 24 24" width="20" height="20">
                  <path fill="currentColor" d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/>
                </svg>
              </a>
              
              <a 
                href="https://linkedin.com/company/guiaspurpuras" 
                target="_blank"
                rel="noopener noreferrer"
                class="social-link linkedin"
                aria-label="LinkedIn"
                title="Síguenos en LinkedIn"
              >
                <svg viewBox="0 0 24 24" width="20" height="20">
                  <path fill="currentColor" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
              
              <a 
                href="https://wa.me/59165324767" 
                target="_blank"
                rel="noopener noreferrer"
                class="social-link whatsapp"
                aria-label="WhatsApp"
                title="Contáctanos por WhatsApp"
              >
                <svg viewBox="0 0 24 24" width="20" height="20">
                  <path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>

        <!-- Columna 2: Empresa -->
        <div class="footer-col">
          <h4>Empresa</h4>
          <ul class="footer-links">
            <li>
              <router-link to="/nosotros">
                <va-icon name="info" size="small" />
                Acerca de Nosotros
              </router-link>
            </li>
            <li>
              <router-link to="/como-funciona">
                <va-icon name="help_outline" size="small" />
                ¿Cómo Funciona?
              </router-link>
            </li>
            <li>
              <router-link to="/blog">
                <va-icon name="article" size="small" />
                Blog
              </router-link>
            </li>
            <li>
              <router-link to="/contacto">
                <va-icon name="mail" size="small" />
                Contacto
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Columna 3: Categorías -->
        <div class="footer-col">
          <h4>Categorías</h4>
          <ul class="footer-links">
            <li>
              <router-link to="/guias/trabajos">
                <va-icon name="business_center" size="small" />
                Trabajos
              </router-link>
            </li>
               <li>
              <router-link to="/guias/gastronomia">
                <va-icon name="restaurant" size="small" />
                Gastronomía
              </router-link>
            </li>
            <li>
              <router-link to="/guias/profesionales">
                <va-icon name="work" size="small" />
                Profesionales
              </router-link>
            </li>
            <li>
              <router-link to="/guias/negocios">
                <va-icon name="store" size="small" />
                Negocios
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Columna 4: Soporte -->
        <div class="footer-col">
          <h4>Soporte</h4>
          <ul class="footer-links">
            <li>
              <router-link to="/ayuda">
                <va-icon name="support_agent" size="small" />
                Centro de Ayuda
              </router-link>
            </li>
            <li>
              <router-link to="/faq">
                <va-icon name="quiz" size="small" />
                Preguntas Frecuentes
              </router-link>
            </li>
            <li>
              <a href="mailto:info@guiaspurpuras.com.bo">
                <va-icon name="email" size="small" />
                info@guiaspurpuras.com.bo
              </a>
            </li>
            <li>
              <a href="tel:+59163356311">
                <va-icon name="phone" size="small" />
                +591 63356311
              </a>
            </li>
            <li>
              <a href="https://wa.me/59163356311" target="_blank">
                <va-icon name="chat" size="small" />
                WhatsApp
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Barra Inferior del Footer -->
    <div class="footer-bottom">
      <div class="footer-container">
        <p class="copyright">
          &copy; {{ currentYear }} Todos los derechos reservados. El uso no autorizado será sancionado por el SENAPI 
          (Servicio Nacional de Propiedad Intelectual) 
          conforme a la Ley 1322 y normativa andina, pudiendo incluir el 
          cese de actos infractores y la destrucción del material ilegal, que se efectuen de forma perjudicial y dolosa. 
        </p>
        
        <div class="footer-bottom-links">
          <router-link to="/terminos">Términos y Condiciones</router-link>
          <span class="separator">•</span>
          <router-link to="/privacidad">Política de Privacidad</router-link>
          <span class="separator">•</span>
          <router-link to="/cookies">Cookies</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

// Año actual dinámico
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
/* ==========================================
   FOOTER PRINCIPAL
   ========================================== */
.footer {
  background: linear-gradient(135deg, #2D0050 0%, #3D0066 100%);
  color: #ffffff;
  margin-top: 5rem;
  width: 100%;
}

/* ==========================================
   SECCIÓN TOP
   ========================================== */
.footer-top {
  padding: 4rem 0 3rem;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 3rem;
}

.footer-col h3,
.footer-col h4 {
  color: #ffffff;
  margin-bottom: 1.5rem;
  font-weight: 700;
  font-size: 1.1rem;
}

/* ==========================================
   LOGO DEL FOOTER
   ========================================== */
.footer-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.logo-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

.logo-text h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: white;
}

.logo-subtitle {
  color: var(--color-yellow-primary);
  font-size: 0.85rem;
  font-weight: 600;
}

.footer-desc {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.7;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

/* ==========================================
   REDES SOCIALES
   ========================================== */
.social-section {
  margin-top: 2rem;
}

.social-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.social-links {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.social-link {
  width: 42px;
  height: 42px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.social-link:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.social-link.facebook:hover {
  background: #1877F2;
  border-color: #1877F2;
}

.social-link.twitter:hover {
  background: #000000;
  border-color: #000000;
}

.social-link.instagram:hover {
  background: linear-gradient(135deg, #833AB4 0%, #FD1D1D 50%, #FCAF45 100%);
  border-color: transparent;
}

.social-link.tiktok:hover {
  background: #000000;
  border-color: #000000;
}

.social-link.linkedin:hover {
  background: #0A66C2;
  border-color: #0A66C2;
}

.social-link.whatsapp:hover {
  background: #25D366;
  border-color: #25D366;
}

/* ==========================================
   ENLACES DEL FOOTER
   ========================================== */
.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.875rem;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  padding: 0.25rem 0;
}

.footer-links a:hover {
  color: var(--color-yellow-primary);
  transform: translateX(5px);
}

.footer-links a :deep(.va-icon) {
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.footer-links a:hover :deep(.va-icon) {
  opacity: 1;
}

/* ==========================================
   FOOTER BOTTOM
   ========================================== */
.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem 0;
  background: rgba(0, 0, 0, 0.2);
}

.footer-bottom .footer-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  grid-template-columns: 1fr;
}

.copyright {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 0.9rem;
}

.footer-bottom-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.footer-bottom-links a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 0.9rem;
}

.footer-bottom-links a:hover {
  color: var(--color-yellow-primary);
}

.separator {
  color: rgba(255, 255, 255, 0.3);
  font-size: 0.8rem;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1024px) {
  .footer-container {
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
    padding: 0 2rem;
  }

  .footer-about {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .footer-top {
    padding: 3rem 0 2rem;
  }

  .footer-container {
    grid-template-columns: 1fr;
    padding: 0 1.5rem;
    gap: 2rem;
  }

  .footer-about {
    grid-column: auto;
  }

  .footer-bottom .footer-container {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }

  .footer-bottom-links {
    flex-wrap: wrap;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .footer-container {
    padding: 0 1rem;
  }

  .footer-col h4 {
    font-size: 1rem;
  }

  .footer-links a {
    font-size: 0.9rem;
  }

  .social-links {
    gap: 0.5rem;
  }

  .social-link {
    width: 38px;
    height: 38px;
  }
}
</style>