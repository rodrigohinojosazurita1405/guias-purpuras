import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

// ========== VIEWS PRINCIPALES ==========
import HomeView from '@/views/HomeView.vue'
import GuideView from '@/views/GuideView.vue'
import PublishView from '@/views/PublishView.vue'

// ========== VIEWS DE DETALLE - SOLO TRABAJOS ==========
// JobDetailView eliminado - ahora se usa GuideView con split view

// ========== VIEWS DE PROCESO ==========
import ApplicationProcess from '@/components/Process/ApplicationProcess.vue'

// ========== VIEWS ESTÁTICAS ==========
import AboutView from '@/views/Static/AboutView.vue'
import ContactPage from '@/views/Static/ContactPage.vue'

// ========== VIEWS DE AUTENTICACIÓN ==========
import LoginView from '@/views/Auth/LoginView.vue'
import RegisterView from '@/views/Auth/RegisterView.vue'
import ForgotPasswordView from '@/views/Auth/ForgotPasswordView.vue'

const routes = [
  // ========== HOME - SOLO TRABAJOS ==========
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: {
      title: 'Guías Púrpuras - Ofertas de Trabajo',
      description: 'Encuentra las mejores oportunidades laborales en Bolivia'
    }
  },

  // ========== PUBLICAR TRABAJO ==========
  {
    path: '/publicar',
    name: 'PublishJob',
    component: PublishView,
    meta: {
      title: 'Publicar Oferta de Trabajo - Guías Púrpuras',
      description: 'Publica tu oferta de trabajo de forma rápida y segura',
      requiresAuth: true,
      requiredRole: 'company'  // Solo empresas pueden publicar
    }
  },

  // ========== LISTADO DE TRABAJOS ==========
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

  // ========== DETALLE DE TRABAJO ==========
  // Redirigir a GuideView con el trabajo preseleccionado
  {
    path: '/guias/trabajos/:id',
    name: 'JobDetail',
    redirect: (to) => {
      return {
        path: '/guias/trabajos',
        query: { selected: to.params.id }
      }
    },
    meta: {
      title: 'Detalle de Trabajo',
      requiresAuth: false
    }
  },

  // ========== POSTULAR A TRABAJO ==========
  {
    path: '/guias/trabajos/:id/aplicar',
    name: 'ApplicationProcess',
    component: ApplicationProcess,
    meta: {
      title: 'Aplicar a Oferta de Trabajo',
      requiresAuth: false // Se puede aplicar sin autenticación
    }
  },

  // ========== REDIRECCIONES PARA COMPATIBILIDAD ==========
  {
    path: '/crear/trabajo',
    redirect: '/publicar'
  },
  {
    path: '/publicar/trabajo',
    redirect: '/publicar'
  },

  // ========== DASHBOARD - USER PROFILE ==========
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: {
      title: 'Mi Dashboard - Guías Púrpuras',
      requiresAuth: true
    }
  },
  {
    path: '/dashboard/profile',
    name: 'DashboardProfile',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'profile' },
    meta: {
      title: 'Mi Perfil - Guías Púrpuras',
      requiresAuth: true,
      requiredRole: 'applicant'
    }
  },
  {
    path: '/dashboard/company',
    name: 'DashboardCompany',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'company' },
    meta: {
      title: 'Perfil De La Empresa - Guías Púrpuras',
      requiresAuth: true,
      requiredRole: 'company'
    }
  },
  {
    path: '/dashboard/jobs',
    name: 'DashboardJobs',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'jobs' },
    meta: {
      title: 'Mis Órdenes - Guías Púrpuras',
      requiresAuth: true,
      requiredRole: 'company'
    }
  },
  {
    path: '/dashboard/jobs-manager',
    name: 'DashboardJobsManager',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'jobs_manager' },
    meta: {
      title: 'Administrador De Empleos - Guías Púrpuras',
      requiresAuth: true,
      requiredRole: 'company'
    }
  },
  {
    path: '/dashboard/candidates',
    name: 'DashboardCandidates',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'candidates' },
    meta: {
      title: 'Mi Base De Talento - Guías Púrpuras',
      requiresAuth: true,
      requiredRole: 'company'
    }
  },
  {
    path: '/dashboard/messages',
    name: 'DashboardMessages',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'messages' },
    meta: {
      title: 'Mensajes - Guías Púrpuras',
      requiresAuth: true
    }
  },
  {
    path: '/dashboard/blocked',
    name: 'DashboardBlocked',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'blocked' },
    meta: {
      title: 'Bloqueados - Guías Púrpuras',
      requiresAuth: true
    }
  },
  {
    path: '/dashboard/cv',
    name: 'DashboardCV',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'cv' },
    meta: {
      title: 'Mi CV - Guías Púrpuras',
      requiresAuth: true,
      requiredRole: 'applicant'
    }
  },
  {
    path: '/dashboard/applications',
    name: 'DashboardApplications',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'applications' },
    meta: {
      title: 'Mis Postulaciones - Guías Púrpuras',
      requiresAuth: true,
      requiredRole: 'applicant'
    }
  },
  {
    path: '/dashboard/shortlisted',
    name: 'DashboardShortlisted',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'shortlisted' },
    meta: {
      title: 'Favoritos - Guías Púrpuras',
      requiresAuth: true,
      requiredRole: 'applicant'
    }
  },
  {
    path: '/dashboard/users',
    name: 'DashboardUsers',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'users' },
    meta: {
      title: 'Gestionar Usuarios - Guías Púrpuras',
      requiresAuth: true
    }
  },
  {
    path: '/dashboard/history',
    name: 'DashboardHistory',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'history' },
    meta: {
      title: 'Registro De Actividad - Guías Púrpuras',
      requiresAuth: true
    }
  },
  {
    path: '/dashboard/notifications',
    name: 'DashboardNotifications',
    component: () => import('@/views/DashboardView.vue'),
    props: { tab: 'notifications' },
    meta: {
      title: 'Alertas - Guías Púrpuras',
      requiresAuth: true
    }
  },

  // ========== PÁGINAS ESTÁTICAS ==========
  {
    path: '/nosotros',
    name: 'About',
    component: AboutView,
    meta: { title: 'Sobre Nosotros' }
  },
  {
    path: '/contacto',
    name: 'Contact',
    component: ContactPage,
    meta: { title: 'Contacto' }
  },

  // ========== AUTENTICACIÓN ==========
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: {
      title: 'Iniciar Sesión - Guías Púrpuras',
      requiresAuth: false
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: {
      title: 'Crear Cuenta - Guías Púrpuras',
      requiresAuth: false
    }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPasswordView,
    meta: {
      title: 'Recuperar Contraseña - Guías Púrpuras',
      requiresAuth: false
    }
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
    const authStore = useAuthStore()

    console.log(`🛡️ [GUARD] Ruta protegida: ${to.path}`)
    console.log(`🛡️ [GUARD] isInitialized: ${authStore.isInitialized}`)
    console.log(`🛡️ [GUARD] isAuthenticated: ${authStore.isAuthenticated}`)
    console.log(`🛡️ [GUARD] user: ${authStore.user?.email || 'null'}`)
    console.log(`🛡️ [GUARD] accessToken: ${authStore.accessToken ? '***' : 'null'}`)

    // Si NO está inicializado, reinicializar desde localStorage
    // Esto es importante cuando se hace logout y luego se intenta acceder a ruta protegida
    if (!authStore.isInitialized) {
      console.log(`🛡️ [GUARD] Store no inicializado, ejecutando initAuth()...`)
      authStore.initAuth()

      // Después de initAuth(), chequear si está autenticado
      if (!authStore.isAuthenticated) {
        console.log(`🛡️ [GUARD] No autenticado después de initAuth(), redirigiendo a /login`)
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
        return
      } else {
        console.log(`🛡️ [GUARD] Autenticado después de initAuth(), permitiendo acceso`)
        next()
        return
      }
    }

    // Si ya está inicializado, solo verificar isAuthenticated
    if (!authStore.isAuthenticated) {
      console.log(`🛡️ [GUARD] No autenticado, redirigiendo a /login`)
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      // Verificar si la ruta requiere un rol específico
      if (to.meta.requiredRole && authStore.user?.role !== to.meta.requiredRole) {
        console.log(`🛡️ [GUARD] Rol insuficiente. Required: ${to.meta.requiredRole}, Current: ${authStore.user?.role}`)
        // Redirigir al dashboard del usuario según su rol
        next({ path: '/dashboard', query: { redirect: to.fullPath } })
      } else {
        console.log(`🛡️ [GUARD] Autenticado y con rol correcto, permitiendo acceso`)
        next()
      }
    }
  } else {
    next()
  }
})

export default router