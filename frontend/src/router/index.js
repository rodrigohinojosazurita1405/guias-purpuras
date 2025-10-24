// frontend/src/router/index.js
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

// Genéricos (para categorías no implementadas aún)
import ListingDetailView from '@/views/ListingDetailView.vue'

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

  // ========== GUÍAS - SERVICIOS ==========
  {
    path: '/guias/servicios',
    name: 'ServicesGuide',
    component: GuideView,
    props: { category: 'servicios' }
  },
  {
    path: '/guias/servicios/:slug',
    name: 'ServiceDetail',
    component: ListingDetailView // Temporal, cambiar cuando esté ServiceDetailView
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
  // Verificar si la ruta requiere autenticación
  if (to.meta.requiresAuth) {
    // TODO: Verificar si el usuario está autenticado
    const isAuthenticated = false // Cambiar por lógica real
    
    if (!isAuthenticated) {
      // Redirigir al login
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