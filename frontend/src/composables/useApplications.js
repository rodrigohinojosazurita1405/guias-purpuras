import { ref, computed, triggerRef } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'

// ========== SHARED STATE (SINGLETON) ==========
// Crear un estado compartido fuera de la función para que todas las instancias compartan los mismos datos
const applications = ref([])
const isLoading = ref(false)
const error = ref(null)
const isLoaded = ref(false)

/**
 * Composable para gestionar aplicaciones del usuario
 * Soporta cargar todas las aplicaciones a trabajos del usuario
 * SINGLETON: Todas las instancias comparten el mismo estado
 */
export function useApplications() {
  const authStore = useAuthStore()

  // ========== COMPUTED ==========
  const totalApplications = computed(() => applications.value.length)

  const receivedCount = computed(
    () => applications.value.filter(app => app.status === 'submitted').length
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
    // Evitar cargas múltiples simultáneas
    if (isLoading.value) {
      return
    }

    isLoading.value = true
    isLoaded.value = false
    error.value = null

    try {
      if (!authStore.user?.email && !authStore.accessToken) {
        applications.value = []
        return
      }

      const email = authStore.user?.email
      if (!email) {
        applications.value = []
        return
      }

      const accessToken = authStore.accessToken || localStorage.getItem('access_token')

      if (!accessToken) {
        applications.value = []
        return
      }

      // Obtener trabajos publicados por el usuario primero
      const jobsUrl = `http://localhost:8000/api/user/published?email=${encodeURIComponent(email)}`

      const jobsResponse = await fetch(
        jobsUrl,
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          },
          timeout: 10000
        }
      )

      if (!jobsResponse.ok) {
        applications.value = []
        return
      }

      const jobsData = await jobsResponse.json()

      if (!jobsData.success) {
        applications.value = []
        return
      }

      if (!jobsData.jobs || jobsData.jobs.length === 0) {
        applications.value = []
        isLoaded.value = true
        return
      }

      // Ahora cargar las aplicaciones para cada trabajo
      let allApplications = []

      for (const job of jobsData.jobs) {
        try {
          const appUrl = `http://localhost:8000/api/jobs/${job.id}/applications`

          const appResponse = await fetch(
            appUrl,
            {
              headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
              },
              timeout: 10000
            }
          )

          if (appResponse.ok) {
            const appData = await appResponse.json()

            if (appData.success && appData.applications) {
              const applicationsWithJob = appData.applications.map(app => ({
                ...app,
                jobTitle: job.title,
                jobId: job.id,
                jobCreatedAt: job.createdAt || null,
                companyProfile: job.companyProfile || null,
                companyLogo: job.companyLogo || null,
                companyName: job.companyName || null,
                companyAnonymous: job.companyAnonymous || false
              }))
              allApplications = [...allApplications, ...applicationsWithJob]
            }
          }
        } catch (err) {
          // Silently continue on error
        }
      }

      applications.value = allApplications
      triggerRef(applications)
    } catch (err) {
      error.value = err.message
      applications.value = []
    } finally {
      isLoading.value = false
      isLoaded.value = true
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
   * Actualizar rating de una aplicación
   */
  const updateApplicationRating = async (jobId, applicationId, rating) => {
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
          body: JSON.stringify({ rating })
        }
      )

      if (!response.ok) {
        throw new Error('Error al actualizar rating')
      }

      const data = await response.json()
      if (data.success) {
        // Actualizar en local
        const app = applications.value.find(a => a.id === applicationId)
        if (app) {
          app.rating = rating
        }
        triggerRef(applications)
      }

      return data
    } catch (err) {
      console.error('Error actualizando rating:', err)
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
    isLoaded.value = false
    isLoading.value = false
  }

  return {
    applications,
    isLoading,
    isLoaded,
    error,
    totalApplications,
    receivedCount,
    reviewingCount,
    shortlistedCount,
    acceptedCount,
    loadApplications,
    updateApplicationStatus,
    updateApplicationRating,
    saveRecruiterNotes,
    resetApplications
  }
}
