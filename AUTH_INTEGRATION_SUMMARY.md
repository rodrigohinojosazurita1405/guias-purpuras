# Resumen de Integración: Autenticación y Sistema de Aplicaciones

## Sistema de Autenticación Implementado

### Tipos de Usuario

El sistema maneja dos tipos de usuarios (roles):

1. **Postulante** (`applicant`)
   - Puede ver ofertas laborales
   - Puede postular a trabajos
   - Puede crear/subir CV
   - Acceso a dashboard de perfil

2. **Empresa** (`company`)
   - Puede publicar ofertas laborales
   - Puede ver postulaciones recibidas
   - NO puede postular a trabajos
   - Acceso a dashboard de gestión de empleos

### Componentes de Autenticación

#### 1. LoginForm.vue
**Ubicación**: `frontend/src/components/Auth/LoginForm.vue`

**Funcionalidad**:
- Login con email y contraseña
- Validación de campos
- Checkbox "Mantener sesión iniciada"
- Animaciones y efectos visuales modernos
- Redirección inteligente según rol:
  - **Empresa** → `/dashboard/jobs-manager`
  - **Postulante** → `/dashboard/profile`
  - **Con URL guardada** → Redirige a esa URL (ej: volver a la oferta después de login)

**Integración con Sistema de Aplicaciones**:
```javascript
// Si el usuario intenta postular sin estar autenticado:
sessionStorage.setItem('redirectAfterLogin', '/guide/job-123')
router.push('/login')

// Después del login exitoso:
const redirectUrl = sessionStorage.getItem('redirectAfterLogin')
if (redirectUrl) {
  router.push(redirectUrl) // Vuelve a la oferta
}
```

#### 2. RegisterForm.vue
**Ubicación**: `frontend/src/components/Auth/RegisterForm.vue`

**Funcionalidad**:
- Registro con nombre, email, contraseña y **rol**
- Selector de rol con iconos dinámicos:
  - 👤 Postulante - Busco oportunidades de empleo
  - 🏢 Empresa - Busco talento para mi equipo
- Validación de contraseña con indicador de fortaleza
- Barra de progreso del formulario
- Acepta términos y condiciones
- Redirección automática según rol después del registro

#### 3. useAuthStore.js
**Ubicación**: `frontend/src/stores/useAuthStore.js`

**Estado Global**:
```javascript
{
  user: {
    id: Number,
    name: String,
    email: String,
    role: 'applicant' | 'company',
    profilePhoto: String (opcional)
  },
  accessToken: String,
  refreshToken: String,
  isAuthenticated: Boolean (computed),
  isLoading: Boolean
}
```

**Métodos**:
- `login(email, password)` - Inicia sesión
- `register(name, email, password, role)` - Registra nuevo usuario
- `logout()` - Cierra sesión (limpia todo)
- `refreshAccessToken()` - Refresca token expirado
- `initAuth()` - Restaura sesión desde localStorage
- `syncProfilePhoto()` - Sincroniza foto de perfil

**Persistencia**:
- Tokens y datos del usuario se guardan en `localStorage`
- Sesión persiste entre recargas de página
- Limpieza completa al hacer logout

## Integración con Sistema de Aplicaciones

### JobDetailPanel.vue - Validación de Autenticación

**Ubicación**: `frontend/src/views/Detail/JobDetailPanel.vue`

**Flujo de Postulación con Validaciones**:

```javascript
applyToJob() {
  // ✅ PASO 1: Verificar si está autenticado
  if (!this.authStore.isAuthenticated) {
    // Mostrar toast de advertencia
    this.$vaToast.init({
      message: 'Debes iniciar sesión para postular a esta oferta',
      color: 'warning'
    })

    // Guardar URL actual para volver después del login
    sessionStorage.setItem('redirectAfterLogin', this.$route.fullPath)

    // Redirigir a login
    this.$router.push('/login')
    return
  }

  // ✅ PASO 2: Verificar que sea postulante (no empresa)
  if (this.authStore.user?.role === 'company') {
    this.$vaToast.init({
      message: 'Solo los postulantes pueden aplicar a ofertas',
      color: 'danger'
    })
    return
  }

  // ✅ PASO 3: Proceder con la postulación
  if (this.listing.applicationType === 'internal') {
    this.showApplicationModal = true // Abrir modal
  } else if (this.listing.applicationType === 'external') {
    window.open(this.listing.externalApplicationUrl, '_blank')
  }
}
```

### ApplicationModal.vue - Modal de Postulación

**Ubicación**: `frontend/src/components/Process/ApplicationModal.vue`

**Tabs Disponibles**:
1. **Subir CV** - Upload de PDF/DOC/DOCX con carta de presentación
2. **Crear CV** - Formulario Harvard con 8 secciones

**Validación antes de enviar**:
- Usuario debe estar autenticado (validado en JobDetailPanel)
- Usuario debe ser postulante (validado en JobDetailPanel)
- Debe completar al menos un método (subir archivo o llenar formulario)

### Envío de Postulación con Autenticación

```javascript
async handleApplicationSubmit(applicationData) {
  const formData = new FormData()

  // Datos de la postulación
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

  // ✅ Enviar con token de autenticación
  const response = await fetch('/api/applications/submit/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': this.getCsrfToken(),
      // El token de acceso se puede agregar aquí si es necesario
      // 'Authorization': `Bearer ${this.authStore.accessToken}`
    },
    body: formData,
    credentials: 'include' // Envía cookies de sesión
  })

  if (response.ok) {
    this.$vaToast.init({
      message: 'Postulación enviada correctamente',
      color: 'success'
    })
  }
}
```

## Flujos de Usuario Completos

### Flujo 1: Usuario No Autenticado Intenta Postular

```
1. Usuario ve oferta laboral en GuideView
2. Click en "Postularme"
3. JobDetailPanel.applyToJob() detecta: !isAuthenticated
4. Muestra toast: "Debes iniciar sesión..."
5. Guarda URL actual en sessionStorage
6. Redirige a /login
7. Usuario completa login
8. LoginForm detecta redirectUrl en sessionStorage
9. Redirige de vuelta a la oferta laboral
10. Usuario puede ahora postular normalmente
```

### Flujo 2: Empresa Intenta Postular (Caso de Error)

```
1. Usuario empresa logueado ve oferta laboral
2. Click en "Postularme"
3. JobDetailPanel.applyToJob() detecta: role === 'company'
4. Muestra toast de error: "Solo postulantes pueden aplicar..."
5. Bloquea la acción
6. Usuario debe crear cuenta de postulante separada
```

### Flujo 3: Postulante Autenticado Postula

```
1. Usuario postulante logueado ve oferta laboral
2. Click en "Postularme"
3. JobDetailPanel.applyToJob() valida:
   ✅ isAuthenticated = true
   ✅ role = 'applicant'
4. Abre ApplicationModal
5. Usuario completa CV (upload o crear)
6. Click "Enviar Postulación"
7. handleApplicationSubmit() envía datos al backend
8. Backend asocia postulación con user.id del token
9. Muestra toast de éxito
10. Cierra modal
```

### Flujo 4: Registro y Postulación Inmediata

```
1. Usuario nuevo ve oferta laboral
2. Click en "Postularme"
3. Redirige a /login
4. Click en "Crear nueva cuenta"
5. Va a /register
6. Completa registro seleccionando rol "Postulante"
7. Registro exitoso, auto-login
8. RegisterForm redirige a /dashboard/profile
9. Usuario navega de nuevo a la oferta
10. Ahora puede postular normalmente
```

## Backend Django Requerido

### Endpoint de Autenticación

```python
# POST /api/auth/register
{
  "name": "Juan Pérez",
  "email": "juan@email.com",
  "password": "******",
  "role": "applicant"  # o "company"
}

Response:
{
  "success": true,
  "user": {
    "id": 123,
    "name": "Juan Pérez",
    "email": "juan@email.com",
    "role": "applicant"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1...",
    "refresh": "eyJ0eXAiOiJKV1..."
  }
}
```

```python
# POST /api/auth/login
{
  "email": "juan@email.com",
  "password": "******"
}

Response: (igual que register)
```

### Endpoint de Aplicaciones (con Autenticación)

```python
# POST /api/applications/submit/
# Headers: Authorization: Bearer {token}
# Content-Type: multipart/form-data

FormData:
- job_id: int
- application_type: 'upload' | 'create'
- cv_file: File (si type = 'upload')
- cover_letter: String (opcional)
- cv_data: JSON String (si type = 'create')

Backend debe:
1. Verificar token JWT válido
2. Extraer user_id del token
3. Verificar que user.role == 'applicant'
4. Verificar que no haya aplicado antes al mismo job
5. Crear registro de Application asociado a user_id
6. Guardar archivo CV o datos de CV Template
7. Retornar success/error
```

### Modelos Django Necesarios

```python
# users/models.py
class User(AbstractUser):
    ROLE_CHOICES = [
        ('applicant', 'Postulante'),
        ('company', 'Empresa'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='applicant')
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

# G_Jobs/applications/models.py
class Application(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=10)
    cv_file = models.FileField(upload_to='cvs/', null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    cv_template = models.OneToOneField('CVTemplate', null=True, blank=True)
    status = models.CharField(max_length=15, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['candidate', 'job']  # Una postulación por usuario por job
```

## Seguridad Implementada

### Frontend
- ✅ Validación de autenticación antes de postular
- ✅ Validación de rol (solo postulantes)
- ✅ CSRF token en requests POST
- ✅ Cookies con `credentials: 'include'`
- ✅ Tokens guardados en localStorage (no sessionStorage para persistencia)
- ✅ Limpieza completa en logout

### Backend (a implementar)
- ⏳ Validación de token JWT en cada request
- ⏳ Verificación de rol en endpoint de aplicaciones
- ⏳ Validación de tamaño y tipo de archivo CV
- ⏳ Prevención de postulaciones duplicadas (unique_together)
- ⏳ Rate limiting (max postulaciones por día)
- ⏳ Sanitización de nombres de archivo
- ⏳ Escaneo de virus en archivos subidos (ClamAV)

## Testing Checklist

### Frontend
- [ ] Login con credenciales válidas (postulante)
- [ ] Login con credenciales válidas (empresa)
- [ ] Registro nuevo postulante
- [ ] Registro nueva empresa
- [ ] Logout y limpieza de sesión
- [ ] Intentar postular sin autenticación (debe redirigir a login)
- [ ] Intentar postular siendo empresa (debe mostrar error)
- [ ] Postular siendo postulante autenticado (debe abrir modal)
- [ ] Redirección después de login a URL guardada
- [ ] Persistencia de sesión al recargar página

### Backend
- [ ] Endpoint de registro crea usuario con rol correcto
- [ ] Endpoint de login valida credenciales y retorna tokens
- [ ] Endpoint de aplicaciones verifica autenticación
- [ ] Endpoint de aplicaciones verifica rol postulante
- [ ] Endpoint previene postulaciones duplicadas
- [ ] Archivos CV se guardan correctamente
- [ ] CVTemplate JSON se guarda correctamente
- [ ] Validación de tamaño de archivo funciona
- [ ] Validación de tipo de archivo funciona

## Próximos Pasos

1. **Backend Django**:
   - Implementar modelos User con campo `role`
   - Implementar endpoints de autenticación con JWT
   - Implementar endpoint `/api/applications/submit/`
   - Configurar CORS y CSRF
   - Configurar MEDIA_ROOT para archivos

2. **Frontend**:
   - Agregar Authorization header con token en requests
   - Implementar interceptor para refrescar token expirado
   - Agregar loading states durante postulación
   - Implementar vista "Mis Postulaciones" para postulantes
   - Implementar vista "Postulaciones Recibidas" para empresas

3. **Mejoras Futuras**:
   - Notificaciones por email al postular
   - Notificaciones a empresa cuando recibe postulación
   - Sistema de seguimiento de estado de postulación
   - Chat entre postulante y empresa
   - Calendario de entrevistas
