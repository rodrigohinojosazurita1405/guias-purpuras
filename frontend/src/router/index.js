// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  // ==========================================
  // RUTA PRINCIPAL - HOME
  // ==========================================
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'Guías Púrpuras - Encuentra todo en Bolivia'
    }
  },

  // ==========================================
  // RUTAS DE GUÍAS POR CATEGORÍA
  // ==========================================
  {
    path: '/guias/profesionales',
    name: 'guias-profesionales',
    component: () => import('../views/GuideView.vue'),
    props: { category: 'profesionales' },
    meta: {
      title: 'Guías Profesionales - Guías Púrpuras'
    }
  },
  {
    path: '/guias/gastronomia',
    name: 'guias-gastronomia',
    component: () => import('../views/GuideView.vue'),
    props: { category: 'gastronomia' },
    meta: {
      title: 'Guías Gastronómicas - Guías Púrpuras'
    }
  },
  {
    path: '/guias/trabajos',
    name: 'guias-trabajos',
    component: () => import('../views/GuideView.vue'),
    props: { category: 'trabajos' },
    meta: {
      title: 'Guías de Trabajos - Guías Púrpuras'
    }
  },
  {
    path: '/guias/servicios',
    name: 'guias-servicios',
    component: () => import('../views/GuideView.vue'),
    props: { category: 'servicios' },
    meta: {
      title: 'Guías de Servicios - Guías Púrpuras'
    }
  },

  // ==========================================
  // RUTA DE DETALLE DE ANUNCIO
  // ==========================================
  {
    path: '/anuncio/:id',
    name: 'listing-detail',
    component: () => import('../views/ListingDetailView.vue'),
    props: true,
    meta: {
      title: 'Detalle del Anuncio - Guías Púrpuras'
    }
  },

  // ==========================================
  // RUTA PARA PUBLICAR ANUNCIO
  // ==========================================
  {
    path: '/publicar',
    name: 'publicar',
    component: () => import('../views/PublishView.vue'),
    meta: {
      title: 'Publicar Anuncio - Guías Púrpuras',
      requiresAuth: false // TODO: Cambiar a true cuando tengamos autenticación
    }
  },

  // ==========================================
  // RUTA 404 - NO ENCONTRADO
  // ==========================================
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFoundView.vue'),
    meta: {
      title: 'Página no encontrada - Guías Púrpuras'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  // Scroll to top on route change
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// ==========================================
// GUARD PARA CAMBIAR TÍTULO DE PÁGINA
// ==========================================
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Guías Púrpuras'
  
  // TODO: Verificar autenticación cuando se implemente
  // if (to.meta.requiresAuth && !isAuthenticated()) {
  //   next({ name: 'login' })
  // } else {
  //   next()
  // }
  
  next()
})

export default router