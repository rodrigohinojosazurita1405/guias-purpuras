import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'

/**
 * Composable para gestionar aplicaciones del usuario
 * Soporta cargar todas las aplicaciones a trabajos del usuario
 */
export function useApplications() {
  const authStore = useAuthStore()

  // ========== DATA ==========
  const applications = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  // ========== COMPUTED ==========
  const totalApplications = computed(() => applications.value.length)

  const receivedCount = computed(
    () => applications.value.filter(app => app.status === 'received').length
  )

  const reviewingCount = computed(
    () => applications.value.filter(app => app.status === 'reviewing').length
  )

  const shortlistedCount = computed(
    () => applications.value.filter(app => app.status === 'shortlisted').length
  )

  const acceptedCount = computed(
    () => applications.value.filter(app => app.status === 'accepted').length
  )

  // ========== METHODS ==========
  /**
   * Cargar todas las aplicaciones a trabajos del usuario autenticado
   */
  const loadApplications = async () => {
    isLoading.value = true
    error.value = null

    try {
      if (!authStore.user?.email && !authStore.accessToken) {
        console.log('Usuario no autenticado, no se pueden cargar aplicaciones')
        return
      }

      const email = authStore.user?.email
      if (!email) {
        console.log('Email no disponible')
        return
      }

      const accessToken = authStore.accessToken || localStorage.getItem('access_token')

      if (!accessToken) {
        console.warn('No hay token de autenticación disponible')
        return
      }

      // Obtener trabajos publicados por el usuario primero
      const jobsResponse = await fetch(
        `http://localhost:8000/api/user/published?email=${encodeURIComponent(email)}`,
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      )

      if (!jobsResponse.ok) {
        throw new Error('Error al obtener trabajos publicados')
      }

      const jobsData = await jobsResponse.json()
      if (!jobsData.success) {
        console.log('Error al obtener trabajos publicados')
        applications.value = []
        isLoading.value = false
        return
      }

      if (!jobsData.jobs || jobsData.jobs.length === 0) {
        console.log('No hay trabajos publicados')
        applications.value = []
        isLoading.value = false
        return
      }

      // Ahora cargar las aplicaciones para cada trabajo
      let allApplications = []

      for (const job of jobsData.jobs) {
        try {
          const appResponse = await fetch(
            `http://localhost:8000/api/jobs/${job.id}/applications`,
            {
              headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
              }
            }
          )

          if (appResponse.ok) {
            const appData = await appResponse.json()
            if (appData.success && appData.applications) {
              // Añadir el título del job a cada aplicación
              const applicationsWithJob = appData.applications.map(app => ({
                ...app,
                jobTitle: job.title,
                jobId: job.id
              }))
              allApplications = [...allApplications, ...applicationsWithJob]
            }
          }
        } catch (err) {
          console.warn(`Error cargando aplicaciones para trabajo ${job.id}:`, err)
        }
      }

      applications.value = allApplications
    } catch (err) {
      console.error('Error cargando aplicaciones:', err)
      error.value = err.message
      applications.value = []
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Actualizar estado de una aplicación
   */
  const updateApplicationStatus = async (jobId, applicationId, newStatus) => {
    try {
      const accessToken = authStore.accessToken || localStorage.getItem('access_token')

      if (!accessToken) {
        throw new Error('No hay autenticación')
      }

      const response = await fetch(
        `http://localhost:8000/api/jobs/${jobId}/applications/${applicationId}`,
        {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ status: newStatus })
        }
      )

      if (!response.ok) {
        throw new Error('Error al actualizar estado')
      }

      const data = await response.json()
      if (data.success) {
        // Actualizar en local
        const app = applications.value.find(a => a.id === applicationId)
        if (app) {
          app.status = newStatus
        }
      }

      return data
    } catch (err) {
      console.error('Error actualizando aplicación:', err)
      throw err
    }
  }

  /**
   * Guardar notas del reclutador
   */
  const saveRecruiterNotes = async (jobId, applicationId, notes) => {
    try {
      const accessToken = authStore.accessToken || localStorage.getItem('access_token')

      if (!accessToken) {
        throw new Error('No hay autenticación')
      }

      const response = await fetch(
        `http://localhost:8000/api/jobs/${jobId}/applications/${applicationId}`,
        {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ recruiterNotes: notes })
        }
      )

      if (!response.ok) {
        throw new Error('Error al guardar notas')
      }

      return await response.json()
    } catch (err) {
      console.error('Error guardando notas:', err)
      throw err
    }
  }

  /**
   * Resetear aplicaciones
   */
  const resetApplications = () => {
    applications.value = []
    error.value = null
  }

  return {
    applications,
    isLoading,
    error,
    totalApplications,
    receivedCount,
    reviewingCount,
    shortlistedCount,
    acceptedCount,
    loadApplications,
    updateApplicationStatus,
    saveRecruiterNotes,
    resetApplications
  }
}
