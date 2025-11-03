import { createRouter, createWebHistory } from 'vue-router'

// ========== VIEWS ==========
import HomeView from '@/views/HomeView.vue'
import GuideView from '@/views/GuideView.vue'
import PublishView from '@/views/PublishView.vue'

// Profesionales
import ProfessionalDetailView from '@/views/ProfessionalDetailView.vue'

// Gastronomía
import RestaurantDetailView from '@/views/RestaurantDetailView.vue'

// Trabajos
import JobDetailView from '@/views/JobDetailView.vue'
import ApplicationProcess from '@/views/ApplicationProcess.vue'
import JobCreate from '@/views/JobCreate.vue'

// Negocios
import BusinessList from '@/views/BusinessList.vue'
import BusinessDetail from '@/views/BusinessDetail.vue'
import BusinessCreate from '@/views/BusinessCreate.vue'

// Genéricos (para categorías no implementadas aún)
import ListingDetailView from '@/views/ListingDetailView.vue'

// ========== PAGES ==========
import AboutPage from '@/pages/AboutPage.vue'
import BlogPage from '@/pages/BlogPage.vue'
import ContactPage from '@/pages/ContactPage.vue'

const routes = [
  // ========== HOME ==========
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },

  // ========== PUBLICAR ANUNCIO ==========
  {
    path: '/publicar',
    name: 'Publish',
    component: PublishView,
    meta: {
      requiresAuth: false // TODO: Cambiar a true cuando haya autenticación
    }
  },

  // ========== GUÍAS - PROFESIONALES ==========
  {
    path: '/guias/profesionales',
    name: 'ProfessionalsGuide',
    component: GuideView,
    props: { category: 'profesionales' }
  },
  {
    path: '/guias/profesionales/:slug',
    name: 'ProfessionalDetail',
    component: ProfessionalDetailView
  },

  // ========== GUÍAS - GASTRONOMÍA ==========
  {
    path: '/guias/gastronomia',
    name: 'GastronomyGuide',
    component: GuideView,
    props: { category: 'gastronomia' }
  },
  {
    path: '/guias/gastronomia/:slug',
    name: 'RestaurantDetail',
    component: RestaurantDetailView
  },

  // ========== GUÍAS - TRABAJOS ==========
  {
    path: '/guias/trabajos',
    name: 'JobsGuide',
    component: GuideView,
    props: { category: 'trabajos' }
  },
  {
    path: '/guias/trabajos/crear',  // ⚠️ ESTA RUTA DEBE IR ANTES DE /:id
    name: 'JobCreate',
    component: JobCreate,
    meta: {
      title: 'Publicar Trabajo',
      requiresAuth: false
    }
  },
  {
    path: '/guias/trabajos/:id',
    name: 'JobDetail',
    component: JobDetailView
  },
  {
    path: '/guias/trabajos/:id/postular',
    name: 'ApplicationProcess',
    component: ApplicationProcess,
    meta: {
      requiresAuth: false // TODO: Cambiar a true cuando haya autenticación
    }
  },

  // ========== GUÍAS - NEGOCIOS ==========
  {
  path: '/guias/negocios',
  name: 'Negocios',
  component: BusinessList,
  meta: {
    title: 'Guías de Negocios',
    requiresAuth: false
  }
},
{
  path: '/guias/negocios/crear',  // ⚠️ ESTA RUTA DEBE IR ANTES DE /:slug
  name: 'NegociosCrear',
  component: BusinessCreate,
  meta: {
    title: 'Publicar Negocio',
    requiresAuth: false  // ✅ ACCESO LIBRE
  }
},
{
  path: '/guias/negocios/:slug',  // ⚠️ ESTA RUTA DEBE IR DESPUÉS DE /crear
  name: 'NegociosDetalle',
  component: BusinessDetail,
  meta: {
    title: 'Detalle de Negocio',
    requiresAuth: false
  }
},

  // ========== PÁGINAS ESTÁTICAS ==========
  {
    path: '/nosotros',
    name: 'About',
    component: AboutPage,
    meta: { title: 'Sobre Nosotros' }
  },
  {
    path: '/blog',
    name: 'Blog',
    component: BlogPage,
    meta: { title: 'Blog' }
  },
  {
    path: '/contacto',
    name: 'Contact',
    component: ContactPage,
    meta: { title: 'Contacto' }
  },

  // ========== 404 - NOT FOUND ==========
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// ========== NAVIGATION GUARDS ==========
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const isAuthenticated = false // Cambiar por lógica real
    if (!isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router