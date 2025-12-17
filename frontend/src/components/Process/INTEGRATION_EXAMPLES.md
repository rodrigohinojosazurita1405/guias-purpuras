# Ejemplos de Integración - Sistema de Aplicaciones

## Requisitos del objeto `job`

El componente `ApplicationModal` requiere un objeto `job` con la siguiente estructura mínima:

```javascript
{
  id: Number,              // ID único de la oferta (requerido)
  title: String,           // Título del puesto (requerido)
  companyName: String,     // Nombre de la empresa (requerido)
  companyLogo: String      // URL del logo (opcional)
}
```

### Ejemplo completo:

```javascript
const job = {
  id: 123,
  title: 'Desarrollador Full Stack Senior',
  companyName: 'Tech Corporation S.A.',
  companyLogo: 'https://example.com/logos/tech-corp.png'
}
```

### Ejemplo sin logo:

```javascript
const job = {
  id: 456,
  title: 'Analista de Datos',
  companyName: 'DataAnalytics Inc.',
  companyLogo: null  // O simplemente omitir el campo
}
```

## Ejemplo 1: Uso básico en un componente

```vue
<template>
  <div class="job-listing">
    <h2>{{ job.title }}</h2>
    <p>{{ job.companyName }}</p>

    <!-- Botón para abrir modal -->
    <button @click="openApplicationModal">
      Postularme
    </button>

    <!-- Modal de aplicación -->
    <ApplicationModal
      v-model="showModal"
      :job="job"
      @submit="handleSubmit"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ApplicationModal from '@/components/Process/ApplicationModal.vue'

const showModal = ref(false)

const job = ref({
  id: 789,
  title: 'Diseñador UX/UI',
  companyName: 'Creative Studio',
  companyLogo: 'https://example.com/logos/creative.png'
})

const openApplicationModal = () => {
  showModal.value = true
}

const handleSubmit = async (applicationData) => {
  console.log('Application submitted:', applicationData)

  // Aquí iría la lógica para enviar al backend
  // Ver ejemplo completo más abajo
}
</script>
```

## Ejemplo 2: Integración con llamada al backend (completo)

```vue
<template>
  <div class="job-detail">
    <h1>{{ job.title }}</h1>
    <button @click="showModal = true" class="apply-btn">
      Postularme ahora
    </button>

    <ApplicationModal
      v-model="showModal"
      :job="job"
      @submit="submitApplication"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'vuestic-ui'
import ApplicationModal from '@/components/Process/ApplicationModal.vue'

const toast = useToast()
const showModal = ref(false)

const job = ref({
  id: 101,
  title: 'Ingeniero DevOps',
  companyName: 'CloudTech Solutions',
  companyLogo: '/media/logos/cloudtech.png'
})

const submitApplication = async (applicationData) => {
  try {
    // Crear FormData
    const formData = new FormData()
    formData.append('job_id', applicationData.jobId)
    formData.append('application_type', applicationData.type)

    if (applicationData.type === 'upload') {
      // Usuario subió un CV
      formData.append('cv_file', applicationData.uploadedFile)

      if (applicationData.coverLetter) {
        formData.append('cover_letter', applicationData.coverLetter)
      }
    } else if (applicationData.type === 'create') {
      // Usuario creó un CV
      formData.append('cv_data', JSON.stringify(applicationData.cvData))
    }

    // Enviar al backend
    const response = await fetch('/api/applications/submit/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken()
      },
      body: formData,
      credentials: 'include'
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Error al enviar postulación')
    }

    const result = await response.json()

    // Mostrar éxito
    toast.init({
      message: 'Postulación enviada correctamente',
      color: 'success',
      duration: 3000
    })

    console.log('Application created:', result)

    // Opcional: Cerrar modal, redirigir, etc.
    showModal.value = false

  } catch (error) {
    console.error('Error:', error)

    toast.init({
      message: error.message || 'Error al enviar la postulación',
      color: 'danger',
      duration: 4000
    })
  }
}

const getCsrfToken = () => {
  const name = 'csrftoken'
  const cookies = document.cookie.split(';')

  for (let cookie of cookies) {
    const trimmed = cookie.trim()
    if (trimmed.startsWith(name + '=')) {
      return decodeURIComponent(trimmed.substring(name.length + 1))
    }
  }

  return null
}
</script>

<style scoped>
.apply-btn {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.apply-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}
</style>
```

## Ejemplo 3: Con Options API (JobDetailPanel.vue actual)

```vue
<template>
  <div class="job-detail-panel">
    <h1>{{ listing.title }}</h1>
    <button @click="applyToJob">Postularme</button>

    <ApplicationModal
      v-model="showApplicationModal"
      :job="listing"
      @submit="handleApplicationSubmit"
    />
  </div>
</template>

<script>
import ApplicationModal from '@/components/Process/ApplicationModal.vue'

export default {
  components: {
    ApplicationModal
  },

  props: {
    listing: {
      type: Object,
      required: true
    }
  },

  data() {
    return {
      showApplicationModal: false
    }
  },

  methods: {
    applyToJob() {
      // Verificar tipo de aplicación
      if (this.listing.applicationType === 'internal') {
        this.showApplicationModal = true
      } else if (this.listing.applicationType === 'external') {
        window.open(this.listing.externalApplicationUrl, '_blank')
      }
    },

    async handleApplicationSubmit(applicationData) {
      try {
        const formData = new FormData()
        formData.append('job_id', applicationData.jobId)
        formData.append('application_type', applicationData.type)

        if (applicationData.type === 'upload') {
          formData.append('cv_file', applicationData.uploadedFile)
          if (applicationData.coverLetter) {
            formData.append('cover_letter', applicationData.coverLetter)
          }
        } else {
          formData.append('cv_data', JSON.stringify(applicationData.cvData))
        }

        const response = await fetch('/api/applications/submit/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': this.getCsrfToken()
          },
          body: formData,
          credentials: 'include'
        })

        if (!response.ok) {
          throw new Error('Error al enviar postulación')
        }

        const result = await response.json()

        this.$vaToast.init({
          message: 'Postulación enviada correctamente',
          color: 'success'
        })

      } catch (error) {
        console.error('Error:', error)
        this.$vaToast.init({
          message: 'Error al enviar la postulación',
          color: 'danger'
        })
      }
    },

    getCsrfToken() {
      const name = 'csrftoken'
      let cookieValue = null

      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }

      return cookieValue
    }
  }
}
</script>
```

## Ejemplo 4: Datos que se envían al backend

### Cuando el usuario sube un CV (type: 'upload'):

```javascript
// FormData enviado:
{
  job_id: 123,
  application_type: 'upload',
  cv_file: File {
    name: 'mi-curriculum.pdf',
    size: 245678,
    type: 'application/pdf'
  },
  cover_letter: 'Estimados señores, me dirijo a ustedes...'
}
```

### Cuando el usuario crea un CV (type: 'create'):

```javascript
// FormData enviado:
{
  job_id: 123,
  application_type: 'create',
  cv_data: JSON.stringify({
    personalInfo: {
      fullName: 'Juan Carlos Pérez López',
      phone: '+591 70123456',
      email: 'juan.perez@email.com',
      location: 'La Paz, Bolivia',
      linkedin: 'linkedin.com/in/juanperez',
      portfolio: 'www.juanperez.dev'
    },
    professionalProfile: 'Desarrollador Full Stack con 5 años...',
    education: [
      {
        startYear: '2015',
        endYear: '2019',
        degree: 'Licenciatura en Ingeniería de Sistemas',
        institution: 'Universidad Mayor de San Andrés',
        achievements: 'Graduado con honores, GPA: 3.8/4.0'
      }
    ],
    experience: [
      {
        startYear: '2019',
        endYear: 'Actual',
        current: true,
        position: 'Desarrollador Full Stack Senior',
        company: 'Tech Solutions SRL',
        achievements: [
          'Lideré equipo de 5 desarrolladores que incrementó productividad en 40%',
          'Implementé arquitectura microservicios reduciendo costos en 30%',
          'Desarrollé sistema de reportes usado por 1000+ usuarios diarios'
        ]
      }
    ],
    technicalSkills: ['JavaScript', 'Vue.js', 'Django', 'PostgreSQL', 'Docker'],
    softSkills: ['Liderazgo', 'Comunicación efectiva', 'Trabajo en equipo'],
    certifications: [
      {
        year: '2023',
        name: 'AWS Certified Solutions Architect',
        institution: 'Amazon Web Services'
      }
    ],
    languages: [
      { name: 'Español', level: 'Nativo / Bilingüe' },
      { name: 'Inglés', level: 'Avanzado' }
    ],
    projects: [
      {
        year: '2024',
        name: 'Sistema ERP empresarial',
        description: 'Desarrollé plataforma que redujo tiempo de procesamiento en 50%'
      }
    ]
  })
}
```

## Ejemplo 5: Manejo de errores comunes

```javascript
const submitApplication = async (applicationData) => {
  try {
    // ... código de envío

    const response = await fetch('/api/applications/submit/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken()
      },
      body: formData,
      credentials: 'include'
    })

    // Manejar diferentes códigos de error
    if (response.status === 400) {
      const error = await response.json()
      // Usuario ya aplicó, datos inválidos, etc.
      showError(error.detail)
    } else if (response.status === 401) {
      // Usuario no autenticado
      redirectToLogin()
    } else if (response.status === 404) {
      // Oferta no encontrada
      showError('Esta oferta ya no está disponible')
    } else if (response.status === 413) {
      // Archivo muy grande
      showError('El archivo CV es muy grande. Máximo 5 MB.')
    } else if (!response.ok) {
      // Otro error
      throw new Error('Error al procesar la postulación')
    }

    // Éxito
    const result = await response.json()
    showSuccess('Postulación enviada correctamente')

  } catch (error) {
    console.error('Error:', error)
    showError('Error de conexión. Verifica tu internet.')
  }
}
```

## Ejemplo 6: Validación antes de abrir el modal

```javascript
const applyToJob = () => {
  // Verificar si el usuario está autenticado
  if (!isAuthenticated.value) {
    toast.init({
      message: 'Debes iniciar sesión para postular',
      color: 'warning'
    })
    router.push('/login')
    return
  }

  // Verificar si el usuario tiene perfil completo
  if (!userProfileComplete.value) {
    toast.init({
      message: 'Completa tu perfil antes de postular',
      color: 'warning'
    })
    router.push('/profile/edit')
    return
  }

  // Verificar si ya postuló
  if (hasAlreadyApplied.value) {
    toast.init({
      message: 'Ya has postulado a esta oferta',
      color: 'info'
    })
    return
  }

  // Todo OK, abrir modal
  showApplicationModal.value = true
}
```

## Notas importantes

1. **CSRF Token**: Siempre incluir el token CSRF en las peticiones POST
2. **Credentials**: Usar `credentials: 'include'` para enviar cookies de sesión
3. **FormData**: No establecer manualmente `Content-Type` cuando se usa FormData
4. **Validación**: El modal ya valida campos requeridos antes de permitir envío
5. **Tamaño de archivo**: El componente valida máx 5MB, pero backend debe validar también
6. **Tipos de archivo**: El componente valida PDF/DOC/DOCX, backend debe validar también
