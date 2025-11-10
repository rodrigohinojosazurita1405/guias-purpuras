import { createRouter, createWebHistory } from 'vue-router'

// ========== VIEWS PRINCIPALES ==========
import HomeView from '@/views/HomeView.vue'
import GuideView from '@/views/GuideView.vue'
import PublishView from '@/views/PublishView.vue'

// ========== VIEWS DE CREACIÓN (NUEVA ESTRUCTURA) ==========
import BusinessCreate from '@/views/Create/BusinessCreate.vue'
import JobCreate from '@/views/Create/JobCreate.vue'
import ProfessionalCreate from '@/views/Create/ProfessionalCreate.vue'
import RestaurantCreate from '@/views/Create/RestaurantCreate.vue'

// ========== VIEWS DE DETALLE (NUEVA ESTRUCTURA) ==========
import ProfessionalDetailView from '@/views/Detail/ProfessionalDetailView.vue'
import RestaurantDetailView from '@/views/Detail/RestaurantDetailView.vue'
import BusinessDetail from '@/views/Detail/BusinessDetail.vue'
import ListingDetailView from '@/views/Detail/ListingDetailView.vue'
import JobDetailView from '@/views/Detail/JobDetailView.vue'

// ========== VIEWS DE PROCESO ==========
import ApplicationProcess from '@/views/Process/ApplicationProcess.vue'

// ========== VIEWS ESTÁTICAS (NUEVA ESTRUCTURA) ==========
import AboutView from '@/views/Static/AboutView.vue'
import BlogPage from '@/views/Static/BlogPage.vue'
import ContactPage from '@/views/Static/ContactPage.vue'

const routes = [
  // ========== HOME ==========
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },

  // ========== PUBLICAR ANUNCIO (LANDING) ==========
  {
    path: '/publicar',
    name: 'Publish',
    component: PublishView,
    meta: {
      title: 'Publicar Anuncio - Guías Púrpuras',
      description: 'Elige el tipo de anuncio que quieres publicar',
      requiresAuth: false
    }
  },

  // ========== RUTAS DE CREACIÓN (NUEVA ESTRUCTURA) ==========
  {
    path: '/crear/negocio',
    name: 'CreateBusiness',
    component: BusinessCreate,
    meta: {
      title: 'Crear Negocio - Guías Púrpuras',
      description: 'Publica tu negocio y llega a miles de clientes',
      requiresAuth: false
    }
  },
  {
    path: '/crear/trabajo',
    name: 'CreateJob',
    component: JobCreate,
    meta: {
      title: 'Publicar Trabajo - Guías Púrpuras',
      description: 'Encuentra al candidato ideal para tu empresa',
      requiresAuth: false
    }
  },
  {
    path: '/crear/profesional',
    name: 'CreateProfessional',
    component: ProfessionalCreate,
    meta: {
      title: 'Crear Perfil Profesional - Guías Púrpuras',
      description: 'Crea tu perfil y encuentra oportunidades laborales',
      requiresAuth: false
    }
  },
  {
    path: '/crear/restaurante',
    name: 'CreateRestaurant',
    component: RestaurantCreate,
    meta: {
      title: 'Publicar Restaurante - Guías Púrpuras',
      description: 'Promociona tu restaurante y atrae más clientes',
      requiresAuth: false
    }
  },

  // ========== RUTAS DE LISTAS - TODAS USANDO GUIDEVIEW ==========
  {
    path: '/guias/negocios',
    name: 'BusinessList',
    component: GuideView,  // ✅ CAMBIO: Ahora usa GuideView
    props: { category: 'negocios' },  // ✅ CAMBIO: Nueva categoría
    meta: {
      title: 'Guías de Negocios en Bolivia',
      description: 'Encuentra empresas y PyMEs verificadas en Bolivia',
      requiresAuth: false
    }
  },
  {
    path: '/guias/profesionales',
    name: 'ProfessionalsList',
    component: GuideView,
    props: { category: 'profesionales' },
    meta: {
      title: 'Profesionales en Bolivia',
      description: 'Encuentra profesionales calificados en Bolivia',
      requiresAuth: false
    }
  },
  {
    path: '/guias/trabajos',
    name: 'JobsList',
    component: GuideView,
    props: { category: 'trabajos' },
    meta: {
      title: 'Ofertas de Trabajo en Bolivia',
      description: 'Encuentra las mejores oportunidades laborales',
      requiresAuth: false
    }
  },
  {
    path: '/guias/gastronomia',
    name: 'RestaurantsList',
    component: GuideView,
    props: { category: 'gastronomia' },
    meta: {
      title: 'Restaurantes y Gastronomía en Bolivia',
      description: 'Descubre los mejores lugares para comer',
      requiresAuth: false
    }
  },

  // ========== RUTAS DE DETALLE ==========
  {
    path: '/guias/negocios/:slug',
    name: 'BusinessDetail',
    component: BusinessDetail,
    meta: {
      title: 'Detalle de Negocio',
      requiresAuth: false
    }
  },
  {
    path: '/guias/profesionales/:slug',
    name: 'ProfessionalDetail',
    component: ProfessionalDetailView
  },
  {
    path: '/guias/gastronomia/:slug',
    name: 'RestaurantDetail',
    component: RestaurantDetailView
  },
  {
    path: '/guias/trabajos/:id',
    name: 'JobDetail',
    component: JobDetailView,
    meta: {
      title: 'Detalle de Trabajo',
      requiresAuth: false
    }
  },
  {
    path: '/anuncio/:id',
    name: 'ListingDetail',
    component: ListingDetailView
  },

  // ========== RUTAS DE PROCESO ==========
  {
    path: '/guias/trabajos/:id/postular',
    name: 'ApplicationProcess',
    component: ApplicationProcess,
    meta: {
      requiresAuth: false // TODO: Cambiar a true cuando haya autenticación
    }
  },

  // ========== COMPATIBILIDAD CON RUTAS ANTERIORES (REDIRECTS) ==========
  {
    path: '/guias/negocios/crear',
    redirect: '/crear/negocio'
  },
  {
    path: '/guias/trabajos/crear',
    redirect: '/crear/trabajo'
  },
  {
    path: '/negocios/crear',
    redirect: '/crear/negocio'
  },
  {
    path: '/trabajos/crear',
    redirect: '/crear/trabajo'
  },
  {
    path: '/profesionales/crear',
    redirect: '/crear/profesional'
  },
  {
    path: '/gastronomia/crear',
    redirect: '/crear/restaurante'
  },
  {
    path: '/restaurantes/crear',
    redirect: '/crear/restaurante'
  },

  // ========== RUTAS ALTERNATIVAS CORTAS ==========
  {
    path: '/profesionales',
    redirect: '/guias/profesionales'
  },
  {
    path: '/gastronomia',
    redirect: '/guias/gastronomia'
  },
  {
    path: '/trabajos',
    redirect: '/guias/trabajos'
  },
  {
    path: '/negocios',
    redirect: '/guias/negocios'
  },

  // ========== PÁGINAS ESTÁTICAS ==========
  {
    path: '/nosotros',
    name: 'About',
    component: AboutView,
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
  // Actualizar título de la página
  if (to.meta.title) {
    document.title = to.meta.title
  }

  // Verificar autenticación si es requerida
  if (to.meta.requiresAuth) {
    const isAuthenticated = false // TODO: Cambiar por lógica real
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