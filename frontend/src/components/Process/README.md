# Sistema de Aplicaciones - Frontend

Este directorio contiene los componentes del sistema de aplicaciones que permite a los candidatos postular a ofertas laborales.

## Componentes

### 1. ApplicationModal.vue
Modal principal que gestiona el flujo de postulación.

**Props:**
- `modelValue` (Boolean): Controla visibilidad del modal
- `job` (Object): Objeto con información de la oferta laboral

**Eventos:**
- `update:modelValue`: Emitido al cerrar/abrir modal
- `submit`: Emitido al enviar postulación con datos completos

**Estructura del evento submit:**
```javascript
{
  jobId: Number,              // ID de la oferta
  type: 'upload' | 'create',  // Tipo de postulación
  uploadedFile: File | null,  // Solo si type === 'upload'
  coverLetter: String | null, // Solo si type === 'upload'
  cvData: Object | null       // Solo si type === 'create'
}
```

### 2. UploadCVTab.vue
Tab para subir CV en formato PDF/DOC/DOCX.

**Props:**
- `file` (File): Archivo seleccionado
- `coverLetter` (String): Carta de presentación

**Eventos:**
- `update:file`: Emitido al seleccionar/cambiar archivo
- `update:coverLetter`: Emitido al editar carta

**Validaciones:**
- Tipos permitidos: PDF, DOC, DOCX
- Tamaño máximo: 5 MB
- Carta de presentación: máx 1000 caracteres

### 3. CreateCVTab.vue
Formulario para crear CV en formato Harvard profesional.

**Props:**
- `modelValue` (Object): Datos del CV

**Eventos:**
- `update:modelValue`: Emitido al editar cualquier campo

**Estructura de datos CV (Harvard Format):**
```javascript
{
  personalInfo: {
    fullName: String,      // Requerido
    phone: String,         // Requerido
    email: String,         // Requerido
    location: String,      // Requerido
    linkedin: String,      // Opcional
    portfolio: String      // Opcional
  },
  professionalProfile: String,  // Máx 500 chars
  education: [
    {
      startYear: String,
      endYear: String,
      degree: String,
      institution: String,
      achievements: String
    }
  ],
  experience: [
    {
      startYear: String,
      endYear: String,
      current: Boolean,
      position: String,
      company: String,
      achievements: Array<String>  // 1-4 logros
    }
  ],
  technicalSkills: Array<String>,
  softSkills: Array<String>,
  certifications: [
    {
      year: String,
      name: String,
      institution: String
    }
  ],
  languages: [
    {
      name: String,
      level: 'Básico' | 'Intermedio' | 'Avanzado' | 'Nativo / Bilingüe'
    }
  ],
  projects: [
    {
      year: String,
      name: String,
      description: String
    }
  ]
}
```

## Integración en Vista

### Ejemplo de uso en JobDetailPanel.vue

```vue
<template>
  <div>
    <!-- Botón para abrir modal -->
    <button @click="showApplicationModal = true">
      Postularme
    </button>

    <!-- Modal de aplicación -->
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

  data() {
    return {
      showApplicationModal: false,
      listing: {
        id: 1,
        title: 'Desarrollador Full Stack',
        companyName: 'Tech Corp',
        companyLogo: 'https://...'
      }
    }
  },

  methods: {
    async handleApplicationSubmit(applicationData) {
      try {
        const formData = new FormData()

        // Datos comunes
        formData.append('job_id', applicationData.jobId)
        formData.append('application_type', applicationData.type)

        if (applicationData.type === 'upload') {
          // Subir CV
          formData.append('cv_file', applicationData.uploadedFile)
          if (applicationData.coverLetter) {
            formData.append('cover_letter', applicationData.coverLetter)
          }
        } else {
          // Crear CV
          formData.append('cv_data', JSON.stringify(applicationData.cvData))
        }

        // Enviar al backend
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
        console.log('Success:', result)

      } catch (error) {
        console.error('Error:', error)
      }
    },

    getCsrfToken() {
      const name = 'csrftoken'
      const cookies = document.cookie.split(';')
      for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=')
        if (key === name) return decodeURIComponent(value)
      }
      return null
    }
  }
}
</script>
```

## Flujo de Usuario

1. **Usuario hace clic en "Postularme"**
   - Se abre ApplicationModal con información del job
   - Modal muestra 2 tabs: "Subir CV" y "Crear CV"

2. **Opción A: Subir CV**
   - Usuario arrastra o selecciona archivo PDF/DOC/DOCX
   - Validación de formato y tamaño
   - Opcionalmente escribe carta de presentación
   - Click en "Enviar Postulación"

3. **Opción B: Crear CV**
   - Usuario completa formulario Harvard (8 secciones)
   - Validación de campos requeridos
   - Click en "Enviar Postulación"

4. **Envío al Backend**
   - Datos se empaquetan en FormData
   - Se envía POST a `/api/applications/submit/`
   - Backend valida y guarda en BD

5. **Respuesta**
   - Success: Toast de confirmación
   - Error: Toast con mensaje de error

## Validaciones Frontend

### UploadCVTab
- Formato: Solo PDF, DOC, DOCX
- Tamaño: Máximo 5 MB
- Carta: Máximo 1000 caracteres

### CreateCVTab
- Nombre completo: Requerido
- Email: Requerido, formato válido
- Teléfono: Requerido
- Ubicación: Requerida
- Perfil profesional: Máximo 500 caracteres
- Logros por experiencia: 1-4 bullets
- Al menos un campo completado en personalInfo para habilitar envío

## Estados del Modal

- **Botón "Enviar" deshabilitado cuando:**
  - Tab "Subir CV": No hay archivo seleccionado
  - Tab "Crear CV": Faltan campos requeridos (nombre, email, teléfono)

## Estilos y Diseño

- Colores principales:
  - Morado: `#7C3AED`, `#6D28D9`
  - Verde (skills soft): `#10B981`
  - Gris: `#6B7280`, `#9CA3AF`

- Iconos: Material Design Icons (via Vuestic)
- Responsive: Mobile-first design
- Accesibilidad: Labels claros, placeholders descriptivos

## Testing

### Casos de prueba recomendados:

1. **Upload Tab**
   - Subir archivo válido
   - Intentar subir archivo > 5MB (debe fallar)
   - Intentar subir formato inválido (debe fallar)
   - Escribir carta > 1000 chars (debe limitar)

2. **Create Tab**
   - Completar solo campos requeridos (debe permitir enviar)
   - Intentar enviar sin nombre/email/teléfono (botón disabled)
   - Agregar/eliminar secciones dinámicas
   - Agregar/eliminar logros en experiencia

3. **Integración**
   - Cambiar entre tabs (datos persisten)
   - Cerrar modal (se resetea)
   - Enviar postulación (llamada API correcta)

## Mejoras Futuras

- [ ] Autoguardado en localStorage
- [ ] Preview del CV antes de enviar
- [ ] Validación de email en tiempo real
- [ ] Sugerencias de skills basadas en job
- [ ] Parseo automático de CV subido
- [ ] Exportar CV creado a PDF
- [ ] Plantillas predefinidas de CV
- [ ] Importar datos de LinkedIn
