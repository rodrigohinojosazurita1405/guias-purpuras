# 📋 PLAN ESTRATÉGICO DE INTEGRACIÓN - SISTEMA DE POSTULANTES

## 🎯 OBJETIVO PRINCIPAL
Crear una app modular e independiente para gestionar TODO el flujo de postulaciones (applications), CVs y perfiles de postulantes, sincronizada con el frontend (ApplicationModal, CreateCVTab, UploadCVTab) y el dashboard de postulantes.

---

## 📊 ANÁLISIS DE LA SITUACIÓN ACTUAL

### ✅ **Frontend Completado:**
- `ApplicationModal.vue` - Modal de postulación con 3 tabs
- `CreateCVTab.vue` - Formulario de creación de CV (formato Harvard)
- `UploadCVTab.vue` - Subida de CV en PDF/DOC/DOCX
- Sistema de persistencia con localStorage
- Validaciones de campos y archivos

### ⚠️ **Backend Pendiente:**
- **NO existe** una app dedicada para postulantes
- **NO existe** modelo `Application` (está comentado en admin.py línea 442)
- **NO existe** modelo `CV` o `ApplicantCV`
- **NO hay** endpoints para guardar CVs (`/api/cvs/save/`, `/api/cvs/list/`)
- **NO hay** almacenamiento de PDFs de CVs

### 🏗️ **Arquitectura Actual:**
```
backend/G_Jobs/
├── jobs/          # Gestión de ofertas de trabajo
├── catalogs/      # Catálogos dinámicos (cities, categories, etc.)
├── dashboard/     # Estadísticas y datos del dashboard
├── payments/      # Órdenes y pagos
├── moderation/    # Usuarios bloqueados
├── plans/         # Planes de publicación
├── audit/         # Auditoría de cambios
└── reports/       # Reportes (pendiente)
```

---

## 🎯 PROPUESTA: NUEVA APP `applicants`

### **Nombre de la App:**
```
backend/G_Jobs/applicants/
```

**Justificación del nombre:**
- **applicants** (postulantes) es más específico que "applications" (aplicaciones)
- Sigue el patrón de nombres en inglés de las otras apps
- Claramente identifica que maneja TODO lo relacionado con postulantes

---

## 📦 ESTRUCTURA DE LA NUEVA APP

```
backend/G_Jobs/applicants/
├── __init__.py
├── apps.py                      # Configuración de la app
├── models.py                    # Modelos principales
│   ├── ApplicantProfile         # Perfil del postulante (extiende User)
│   ├── JobApplication           # Postulación a un trabajo
│   ├── ApplicantCV              # CVs guardados (máx 2 por usuario)
│   └── ApplicationActivity      # Log de actividades (opcional)
├── admin.py                     # Interfaz de administración
├── views.py                     # Endpoints API
├── urls.py                      # Rutas de la app
├── serializers.py (opcional)    # Si usamos DRF
├── signals.py                   # Señales para auditoría
└── migrations/                  # Migraciones de BD
```

---

## 🗄️ MODELOS PROPUESTOS

### **1. ApplicantProfile** (Perfil del Postulante)
```python
class ApplicantProfile(models.Model):
    """
    Perfil extendido para usuarios postulantes
    Complementa el modelo User de Django
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applicant_profile'
    )

    # Información personal
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200)  # "La Paz, Bolivia"
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    # Preferencias de búsqueda
    desired_positions = models.JSONField(default=list)  # ["Desarrollador", "Analista"]
    desired_cities = models.JSONField(default=list)     # ["La Paz", "Cochabamba"]
    desired_modality = models.CharField(max_length=20, blank=True)  # remoto/presencial/hibrido

    # Estadísticas
    total_applications = models.IntegerField(default=0)
    total_cvs_created = models.IntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Límite de CVs guardados (regla de negocio)
    MAX_SAVED_CVS = 2
```

### **2. ApplicantCV** (CVs Guardados)
```python
class ApplicantCV(models.Model):
    """
    CVs guardados por el postulante
    Máximo 2 CVs por usuario
    """
    CV_TYPE_CHOICES = [
        ('created', 'CV Creado en Plataforma'),
        ('uploaded', 'CV Subido (PDF/DOC)')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_cvs'
    )

    # Tipo de CV
    cv_type = models.CharField(max_length=20, choices=CV_TYPE_CHOICES)

    # Datos del CV creado (si type='created')
    cv_data = models.JSONField(null=True, blank=True)
    # Estructura:
    # {
    #   "personalInfo": {...},
    #   "professionalProfile": "...",
    #   "education": [...],
    #   "experience": [...],
    #   "technicalSkills": [...],
    #   "softSkills": [...],
    #   "certifications": [...],
    #   "languages": [...],
    #   "projects": [...]
    # }

    # Archivo subido (si type='uploaded')
    file = models.FileField(
        upload_to='applicant_cvs/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(['pdf', 'doc', 'docx']),
            MaxFileSizeValidator(5 * 1024 * 1024)  # 5 MB
        ]
    )
    file_name = models.CharField(max_length=255, blank=True)

    # Metadata del CV
    title = models.CharField(max_length=200)  # "CV - Desarrollador Full Stack"
    full_name = models.CharField(max_length=200)  # Extraído de cv_data o archivo

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "CV del Postulante"
        verbose_name_plural = "CVs de Postulantes"
```

### **3. JobApplication** (Postulación a Trabajo)
```python
class JobApplication(models.Model):
    """
    Representa una postulación de un usuario a una oferta de trabajo
    """
    STATUS_CHOICES = [
        ('received', 'Recibida'),
        ('reviewing', 'En Revisión'),
        ('shortlisted', 'Preseleccionado'),
        ('interview', 'Entrevista'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado')
    ]

    APPLICATION_TYPE_CHOICES = [
        ('saved', 'CV Guardado'),
        ('uploaded', 'CV Subido'),
        ('created', 'CV Creado')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relaciones
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant_email = models.EmailField()  # Denormalizado para rapidez

    # Tipo de aplicación
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES)

    # CV utilizado (si usó un CV guardado)
    saved_cv = models.ForeignKey(
        'ApplicantCV',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )

    # Archivo subido directamente (si type='uploaded')
    uploaded_file = models.FileField(
        upload_to='application_cvs/%Y/%m/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(['pdf', 'doc', 'docx']),
            MaxFileSizeValidator(5 * 1024 * 1024)
        ]
    )

    # Datos del CV creado en el momento (si type='created')
    cv_data = models.JSONField(null=True, blank=True)

    # Carta de presentación
    cover_letter = models.TextField(blank=True, max_length=1000)

    # Estado de la aplicación
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received'
    )

    # Notas del reclutador
    recruiter_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Prevención de duplicados
    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-created_at']
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['applicant', 'created_at']),
        ]
```

---

## 🔌 ENDPOINTS API REQUERIDOS

### **📁 Gestión de CVs**

#### **1. POST `/api/cvs/save/`**
Guardar un CV creado en el dashboard
```json
Request:
{
  "cv_data": {...},
  "title": "CV - Desarrollador Full Stack"
}

Response:
{
  "success": true,
  "message": "CV guardado correctamente",
  "cv": {
    "id": "uuid",
    "title": "CV - Desarrollador Full Stack",
    "type": "created",
    "created_at": "2025-12-16T20:00:00Z"
  }
}
```

#### **2. GET `/api/cvs/list/`**
Listar CVs guardados del usuario
```json
Response:
{
  "success": true,
  "cvs": [
    {
      "id": "uuid",
      "type": "created",
      "title": "CV - Desarrollador",
      "full_name": "Juan Pérez",
      "created_at": "..."
    }
  ]
}
```

#### **3. GET `/api/cvs/<cv_id>/`**
Obtener detalles de un CV guardado

#### **4. PATCH `/api/cvs/<cv_id>/update/`**
Actualizar un CV guardado (CRUD - Update)
```json
Request:
{
  "cv_data": {...},  // Nuevos datos del CV
  "title": "CV Actualizado - Desarrollador Senior"
}

Response:
{
  "success": true,
  "message": "CV actualizado correctamente",
  "cv": {
    "id": "uuid",
    "title": "CV Actualizado - Desarrollador Senior",
    "updated_at": "2025-12-16T21:00:00Z"
  }
}
```

#### **5. DELETE `/api/cvs/<cv_id>/`**
Eliminar un CV guardado (CRUD - Delete)

---

### **📝 Gestión de Postulaciones**

#### **6. POST `/api/jobs/<job_id>/apply/`**
Postular a un trabajo
```json
Request:
{
  "application_type": "created",  // saved | uploaded | created
  "saved_cv_id": null,
  "uploaded_file": File,
  "cv_data": {...},
  "cover_letter": "..."
}

Response:
{
  "success": true,
  "message": "Postulación enviada correctamente",
  "application_id": "uuid"
}
```

#### **6. GET `/api/applications/me/`**
Listar todas las postulaciones del usuario
```json
Response:
{
  "success": true,
  "applications": [
    {
      "id": "uuid",
      "job": {...},
      "status": "received",
      "applied_at": "...",
      "recruiter_notes": "..."
    }
  ]
}
```

#### **7. GET `/api/applications/<application_id>/`**
Ver detalles de una postulación específica

#### **8. GET `/api/jobs/<job_id>/applications/`**
Listar postulaciones de un trabajo (solo para el reclutador/empresa)

#### **9. PATCH `/api/jobs/<job_id>/applications/<application_id>/`**
Actualizar estado de postulación (solo reclutador)
```json
Request:
{
  "status": "interview",
  "recruiter_notes": "Candidato prometedor"
}
```

---

### **👤 Perfil del Postulante**

#### **10. GET `/api/applicants/profile/me/`**
Obtener perfil del postulante

#### **11. PATCH `/api/applicants/profile/me/`**
Actualizar perfil del postulante

---

## 💾 ALMACENAMIENTO DE ARCHIVOS

### **Estructura de Media:**
```
backend/media/
├── applicant_cvs/              # CVs guardados por postulantes
│   ├── cv_uuid1.pdf
│   └── cv_uuid2.docx
│
├── application_cvs/            # CVs de postulaciones específicas
│   ├── 2025/
│   │   └── 12/
│   │       ├── app_uuid1.pdf
│   │       └── app_uuid2.pdf
│   └── 2026/...
│
├── payment_proofs/             # (Ya existe)
├── company_logos/              # (Ya existe)
└── company_banners/            # (Ya existe)
```

### **Validaciones de Archivos:**
```python
# En models.py
from django.core.validators import FileExtensionValidator

def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5 MB
    if file.size > max_size:
        raise ValidationError('El archivo no debe superar los 5 MB')

# Usar en FileField
file = models.FileField(
    validators=[
        FileExtensionValidator(['pdf', 'doc', 'docx']),
        validate_file_size
    ]
)
```

---

## 🎨 INTEGRACIÓN CON JAZZMIN ADMIN

### **Configuración en `admin.py`:**

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import ApplicantProfile, ApplicantCV, JobApplication

@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'location', 'total_applications', 'total_cvs_created', 'created_at')
    list_filter = ('created_at', 'desired_modality')
    search_fields = ('user__email', 'full_name', 'phone', 'location')
    readonly_fields = ('created_at', 'updated_at', 'total_applications', 'total_cvs_created')

    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'full_name', 'phone', 'location')
        }),
        ('Redes Sociales', {
            'fields': ('linkedin', 'portfolio')
        }),
        ('Preferencias de Búsqueda', {
            'fields': ('desired_positions', 'desired_cities', 'desired_modality')
        }),
        ('Estadísticas', {
            'fields': ('total_applications', 'total_cvs_created')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ApplicantCV)
class ApplicantCVAdmin(admin.ModelAdmin):
    list_display = ('title', 'applicant', 'cv_type', 'full_name', 'file_preview', 'created_at')
    list_filter = ('cv_type', 'created_at')
    search_fields = ('title', 'full_name', 'applicant__email')
    readonly_fields = ('id', 'created_at', 'updated_at', 'file_preview')

    fieldsets = (
        ('Información del CV', {
            'fields': ('id', 'applicant', 'cv_type', 'title', 'full_name')
        }),
        ('Contenido', {
            'fields': ('cv_data', 'file', 'file_name', 'file_preview')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def file_preview(self, obj):
        """Mostrar preview del archivo con ícono"""
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank"><i class="fas fa-file-pdf"></i> Ver Archivo</a>',
                obj.file.url
            )
        return format_html('<i class="fas fa-times text-muted"></i> Sin archivo')
    file_preview.short_description = 'Archivo CV'

    def get_queryset(self, request):
        """Limitar visibilidad según rol"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Si no es superuser, solo ver sus propios CVs
            qs = qs.filter(applicant=request.user)
        return qs


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id_short', 'job_title', 'applicant_name', 'status_badge',
        'application_type', 'created_at', 'actions_column'
    )
    list_filter = ('status', 'application_type', 'created_at', 'job__jobCategory')
    search_fields = (
        'applicant__email', 'applicant_email', 'job__title',
        'job__companyName', 'recruiter_notes'
    )
    readonly_fields = (
        'id', 'created_at', 'updated_at', 'reviewed_at',
        'file_preview', 'cv_data_preview'
    )

    fieldsets = (
        ('Información de la Postulación', {
            'fields': ('id', 'job', 'applicant', 'applicant_email', 'application_type')
        }),
        ('CV y Documentos', {
            'fields': ('saved_cv', 'uploaded_file', 'file_preview', 'cv_data', 'cv_data_preview', 'cover_letter')
        }),
        ('Estado y Revisión', {
            'fields': ('status', 'recruiter_notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def id_short(self, obj):
        """Mostrar ID corto"""
        return str(obj.id)[:8]
    id_short.short_description = 'ID'

    def job_title(self, obj):
        """Mostrar título del trabajo con link"""
        return format_html(
            '<a href="/admin/jobs/job/{}/change/">{}</a>',
            obj.job.id, obj.job.title
        )
    job_title.short_description = 'Trabajo'

    def applicant_name(self, obj):
        """Mostrar nombre del postulante"""
        if hasattr(obj.applicant, 'applicant_profile'):
            return obj.applicant.applicant_profile.full_name
        return obj.applicant.email
    applicant_name.short_description = 'Postulante'

    def status_badge(self, obj):
        """Badge de estado con colores"""
        status_colors = {
            'received': 'secondary',
            'reviewing': 'info',
            'shortlisted': 'warning',
            'interview': 'primary',
            'accepted': 'success',
            'rejected': 'danger'
        }
        color = status_colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Estado'

    def actions_column(self, obj):
        """Acciones rápidas"""
        if obj.uploaded_file or obj.saved_cv:
            return format_html(
                '<a class="button" href="{}"><i class="fas fa-download"></i></a>',
                obj.uploaded_file.url if obj.uploaded_file else ''
            )
        return '-'
    actions_column.short_description = 'Acciones'

    def file_preview(self, obj):
        """Preview del archivo subido"""
        if obj.uploaded_file:
            return format_html(
                '<a href="{}" target="_blank"><i class="fas fa-file-pdf"></i> Ver CV</a>',
                obj.uploaded_file.url
            )
        elif obj.saved_cv and obj.saved_cv.file:
            return format_html(
                '<a href="{}" target="_blank"><i class="fas fa-file-pdf"></i> Ver CV Guardado</a>',
                obj.saved_cv.file.url
            )
        return format_html('<i class="fas fa-file-alt"></i> CV Creado en Plataforma')
    file_preview.short_description = 'Archivo'

    def cv_data_preview(self, obj):
        """Preview de datos del CV en formato legible"""
        if obj.cv_data:
            import json
            return format_html(
                '<pre style="max-height: 300px; overflow-y: auto;">{}</pre>',
                json.dumps(obj.cv_data, indent=2, ensure_ascii=False)
            )
        return '-'
    cv_data_preview.short_description = 'Datos del CV'

    # Acciones personalizadas
    actions = ['mark_as_reviewing', 'mark_as_shortlisted', 'mark_as_rejected']

    def mark_as_reviewing(self, request, queryset):
        updated = queryset.update(status='reviewing')
        self.message_user(request, f'{updated} postulaciones marcadas como "En Revisión"')
    mark_as_reviewing.short_description = "Marcar como 'En Revisión'"

    def mark_as_shortlisted(self, request, queryset):
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f'{updated} postulaciones preseleccionadas')
    mark_as_shortlisted.short_description = "Preseleccionar candidatos"

    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} postulaciones rechazadas')
    mark_as_rejected.short_description = "Rechazar postulaciones"
```

### **Configuración Jazzmin en `settings.py`:**

```python
JAZZMIN_SETTINGS = {
    # ... configuración existente ...

    "icons": {
        # Apps existentes
        "jobs.Job": "fas fa-briefcase",
        "plans.Plan": "fas fa-star",

        # Nueva app applicants
        "applicants.ApplicantProfile": "fas fa-user-tie",
        "applicants.ApplicantCV": "fas fa-file-alt",
        "applicants.JobApplication": "fas fa-paper-plane",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # Orden de apps en el menú
    "order_with_respect_to": [
        "jobs",
        "applicants",  # Nueva app
        "plans",
        "payments",
        "catalogs",
        "dashboard",
        "moderation",
        "audit",
    ],
}

JAZZMIN_UI_TWEAKS = {
    # ... configuración existente ...
}
```

---

## ✏️ CRUD COMPLETO PARA CVs DEL POSTULANTE

### **En el Dashboard del Postulante (Frontend):**

#### **Vista: Mis CVs Guardados**
```vue
<template>
  <div class="my-cvs-section">
    <div class="section-header">
      <h2>Mis CVs Guardados</h2>
      <span class="cv-count">{{ cvs.length }} / 2</span>
      <button
        @click="createNewCV"
        :disabled="cvs.length >= 2"
        class="btn-create-cv"
      >
        <va-icon name="add" />
        Crear Nuevo CV
      </button>
    </div>

    <!-- Lista de CVs -->
    <div class="cvs-list">
      <div v-for="cv in cvs" :key="cv.id" class="cv-card">
        <div class="cv-info">
          <h3>{{ cv.title }}</h3>
          <p>{{ cv.full_name }}</p>
          <span class="cv-date">{{ formatDate(cv.created_at) }}</span>
        </div>
        <div class="cv-actions">
          <!-- Editar -->
          <button @click="editCV(cv)" class="btn-edit">
            <va-icon name="edit" />
            Editar
          </button>
          <!-- Ver Preview -->
          <button @click="previewCV(cv)" class="btn-preview">
            <va-icon name="visibility" />
            Ver
          </button>
          <!-- Eliminar -->
          <button @click="deleteCV(cv)" class="btn-delete">
            <va-icon name="delete" />
            Eliminar
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Edición -->
    <CVEditModal
      v-if="showEditModal"
      :cv="selectedCV"
      @save="handleSaveCV"
      @close="showEditModal = false"
    />
  </div>
</template>
```

### **Endpoints CRUD:**

1. **CREATE**: `POST /api/cvs/save/` ✅ (Ya definido)
2. **READ**: `GET /api/cvs/list/` ✅ (Ya definido)
3. **UPDATE**: `PATCH /api/cvs/<cv_id>/update/` ✅ (Ya agregado)
4. **DELETE**: `DELETE /api/cvs/<cv_id>/` ✅ (Ya definido)

### **Validaciones en el UPDATE:**

```python
@token_required
@require_http_methods(["PATCH"])
def update_cv(request, cv_id):
    """
    Actualizar un CV guardado
    Solo el dueño puede modificar su CV
    """
    try:
        # Verificar que el CV existe y pertenece al usuario
        cv = ApplicantCV.objects.get(id=cv_id, applicant=request.user)

        data = json.loads(request.body)

        # Actualizar campos permitidos
        if 'cv_data' in data:
            cv.cv_data = data['cv_data']
            # Actualizar full_name desde cv_data
            if 'personalInfo' in data['cv_data']:
                cv.full_name = data['cv_data']['personalInfo'].get('fullName', '')

        if 'title' in data:
            cv.title = data['title']

        cv.save()

        return JsonResponse({
            'success': True,
            'message': 'CV actualizado correctamente',
            'cv': {
                'id': str(cv.id),
                'title': cv.title,
                'full_name': cv.full_name,
                'updated_at': cv.updated_at.isoformat()
            }
        })

    except ApplicantCV.DoesNotExist:
        return JsonResponse({
            'error': 'CV no encontrado o no tienes permiso para editarlo'
        }, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

---

## 🔗 INTEGRACIÓN CON URLS

### **En `backend/G_Jobs/jobs/urls.py`:**
```python
from G_Jobs.applicants import views as applicant_views

urlpatterns = [
    # ... rutas existentes ...

    # ========== ENDPOINTS PARA POSTULANTES ==========
    # CVs Guardados (CRUD Completo)
    path('cvs/save/', applicant_views.save_cv, name='save_cv'),  # CREATE
    path('cvs/list/', applicant_views.list_cvs, name='list_cvs'),  # READ (list)
    path('cvs/<uuid:cv_id>/', applicant_views.get_cv_detail, name='get_cv_detail'),  # READ (detail)
    path('cvs/<uuid:cv_id>/update/', applicant_views.update_cv, name='update_cv'),  # UPDATE
    path('cvs/<uuid:cv_id>/delete/', applicant_views.delete_cv, name='delete_cv'),  # DELETE

    # Postulaciones
    path('jobs/<str:job_id>/apply/', applicant_views.apply_to_job, name='apply_to_job'),
    path('applications/me/', applicant_views.get_my_applications, name='get_my_applications'),
    path('applications/<uuid:app_id>/', applicant_views.get_application_detail, name='get_application_detail'),

    # Gestión de postulaciones (para reclutadores)
    path('jobs/<str:job_id>/applications/', applicant_views.list_job_applications, name='list_job_applications'),
    path('jobs/<str:job_id>/applications/<uuid:app_id>/', applicant_views.update_application_status, name='update_application_status'),

    # Perfil de postulante
    path('applicants/profile/me/', applicant_views.get_applicant_profile, name='get_applicant_profile'),
    path('applicants/profile/me/update/', applicant_views.update_applicant_profile, name='update_applicant_profile'),
]
```

---

## 🔐 SEGURIDAD Y PERMISOS

### **Decoradores Requeridos:**
```python
from functools import wraps
from django.http import JsonResponse

def applicant_required(view_func):
    """Solo usuarios con rol 'applicant' pueden acceder"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user_data'):
            return JsonResponse({'error': 'No autenticado'}, status=401)

        if request.user_data.get('role') != 'applicant':
            return JsonResponse({'error': 'Solo para postulantes'}, status=403)

        return view_func(request, *args, **kwargs)
    return wrapper

def company_required(view_func):
    """Solo usuarios con rol 'company' pueden acceder"""
    # Similar implementación
```

### **Validaciones de Límites:**
```python
def save_cv(request):
    # Verificar límite de CVs (máx 2)
    current_cvs = ApplicantCV.objects.filter(applicant=request.user).count()
    if current_cvs >= ApplicantCV.MAX_SAVED_CVS:
        return JsonResponse({
            'error': 'Has alcanzado el límite máximo de CVs guardados (2)',
            'code': 'MAX_CVS_REACHED'
        }, status=400)
```

---

## 📊 INTEGRACIÓN CON AUDIT

### **Registrar en Auditoría:**
```python
# En signals.py de la app applicants
from django.db.models.signals import post_save, post_delete
from G_Jobs.audit.models import AuditLog

@receiver(post_save, sender=JobApplication)
def log_application_created(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            action='application_created',
            user=instance.applicant,
            target_id=str(instance.id),
            details={
                'job_id': instance.job.id,
                'job_title': instance.job.title,
                'application_type': instance.application_type
            }
        )
```

---

## 🎯 PLAN DE IMPLEMENTACIÓN (FASES)

### **FASE 1: Configuración Base** (30 min)
- [ ] Crear app `applicants` con `python manage.py startapp applicants backend/G_Jobs/applicants`
- [ ] Configurar `apps.py`
- [ ] Registrar app en `INSTALLED_APPS`
- [ ] Crear `urls.py` y conectar con `jobs/urls.py`

### **FASE 2: Modelos** (1.5 horas)
- [ ] Crear modelo `ApplicantProfile`
- [ ] Crear modelo `ApplicantCV` con validaciones
- [ ] Crear modelo `JobApplication`
- [ ] Configurar `admin.py` para gestión
- [ ] Ejecutar migraciones: `python manage.py makemigrations applicants`
- [ ] Aplicar migraciones: `python manage.py migrate`

### **FASE 3: Endpoints de CVs** (2 horas)
- [ ] `POST /api/cvs/save/` - Guardar CV
- [ ] `GET /api/cvs/list/` - Listar CVs
- [ ] `GET /api/cvs/<cv_id>/` - Detalle de CV
- [ ] `DELETE /api/cvs/<cv_id>/` - Eliminar CV
- [ ] Testing con datos reales

### **FASE 4: Endpoints de Postulaciones** (2 horas)
- [ ] `POST /api/jobs/<job_id>/apply/` - Aplicar a trabajo
- [ ] `GET /api/applications/me/` - Mis postulaciones
- [ ] `GET /api/applications/<app_id>/` - Detalle de postulación
- [ ] Testing con ApplicationModal

### **FASE 5: Dashboard de Postulantes** (2 horas)
- [ ] `GET /api/applicants/profile/me/` - Obtener perfil
- [ ] `PATCH /api/applicants/profile/me/` - Actualizar perfil
- [ ] Integrar estadísticas en dashboard existente
- [ ] Vista de CVs guardados en dashboard
- [ ] Vista de postulaciones en dashboard

### **FASE 6: Gestión para Reclutadores** (1.5 horas)
- [ ] `GET /api/jobs/<job_id>/applications/` - Ver postulaciones de mi trabajo
- [ ] `PATCH /api/jobs/<job_id>/applications/<app_id>/` - Cambiar estado
- [ ] Notificaciones por email (opcional)

### **FASE 7: Auditoría y Signals** (30 min)
- [ ] Configurar signals para logging
- [ ] Integrar con `G_Jobs.audit`
- [ ] Testing de auditoría

### **FASE 8: Testing Final** (1 hora)
- [ ] Testing end-to-end del flujo completo
- [ ] Verificar límite de 2 CVs
- [ ] Verificar persistencia localStorage + backend
- [ ] Testing de archivos PDF/DOC

---

## ⚠️ CONSIDERACIONES IMPORTANTES

### **1. Compatibilidad con Código Existente**
- La app `jobs` ya tiene referencias a `applications` en `views.py` (línea 661, 760, 830)
- Necesitamos **migrar** o **deprecar** esas funciones antiguas
- Mantener **backward compatibility** si hay datos existentes

### **2. Nombres de Tablas en BD**
```python
# En models.py de applicants
class ApplicantCV(models.Model):
    class Meta:
        db_table = 'applicants_cv'  # Nombre explícito

class JobApplication(models.Model):
    class Meta:
        db_table = 'applicants_job_application'
```

### **3. Migración de Datos Existentes**
Si ya hay postulaciones en la BD (aunque parece que no):
```python
# Crear script de migración
python manage.py datamigration applicants migrate_old_applications
```

### **4. Permisos de Archivos**
```python
# En settings.py
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Asegurar que el servidor tiene permisos de escritura
os.chmod(MEDIA_ROOT, 0o755)
```

---

## 📝 CHECKLIST DE VALIDACIONES

### **Validaciones de Negocio:**
- [x] Usuario solo puede postular UNA VEZ al mismo trabajo
- [x] Usuario puede guardar MÁXIMO 2 CVs
- [x] Archivos PDF/DOC/DOCX máximo 5 MB
- [x] Solo postulantes (role='applicant') pueden postular
- [x] Solo empresas (role='company') pueden ver postulaciones de sus trabajos
- [x] No se puede postular a trabajos cerrados/expirados
- [x] Carta de presentación máximo 1000 caracteres

### **Validaciones Técnicas:**
- [x] CSRF token en todas las peticiones POST/PATCH/DELETE
- [x] Autenticación con `@token_required`
- [x] Sanitización de inputs (XSS prevention)
- [x] Validación de tipos de archivos (magic numbers, no solo extensión)
- [x] Rate limiting para prevenir spam

---

## 🚀 PRÓXIMOS PASOS RECOMENDADOS

1. **Aprobación del Plan**: Revisar y aprobar esta propuesta
2. **Crear la App**: Ejecutar `python manage.py startapp applicants backend/G_Jobs/applicants`
3. **Implementar Modelos**: Empezar con FASE 2
4. **Testing Incremental**: Probar cada endpoint antes de continuar
5. **Integración Frontend**: Conectar ApplicationModal con los nuevos endpoints
6. **Documentación**: Documentar cada endpoint en Postman/Swagger

---

## 📚 RECURSOS Y REFERENCIAS

- **Documentación Frontend**: Ver `CV_SAVE_ENDPOINT_SPEC.md`, `BACKEND_INTEGRATION_SPEC.md`
- **Modelos Existentes**: `backend/G_Jobs/jobs/models.py`
- **Patrón de URLs**: `backend/G_Jobs/jobs/urls.py`
- **Ejemplo de App Modular**: `backend/G_Jobs/payments/`, `backend/G_Jobs/catalogs/`

---

## ✅ RESULTADO ESPERADO

Al finalizar la implementación:
1. ✅ Usuario puede crear y guardar hasta 2 CVs en su dashboard
2. ✅ Usuario puede postular a trabajos con CV creado, guardado o subido
3. ✅ Datos persisten en localStorage Y backend
4. ✅ Empresa puede ver y gestionar postulaciones de sus trabajos
5. ✅ Sistema de auditoría registra todas las acciones
6. ✅ PDFs se almacenan de forma organizada en `media/`
7. ✅ Arquitectura modular y escalable

---

**Autor**: Claude (Sonnet 4.5)
**Fecha**: 2025-12-16
**Estado**: 📋 Propuesta - Pendiente de Aprobación
