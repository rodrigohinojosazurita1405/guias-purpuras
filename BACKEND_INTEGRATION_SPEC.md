# Especificación de Integración Backend - Sistema de Aplicaciones

## Resumen
El sistema de aplicaciones permite a los candidatos postular a ofertas laborales mediante dos métodos:
1. **Subir CV**: Cargar archivo PDF/DOC/DOCX con carta de presentación opcional
2. **Crear CV**: Completar formulario en formato Harvard con 8 secciones

## Endpoint Requerido

### POST /api/applications/submit/

**Autenticación**: Requerida (usuario debe estar autenticado como candidato)

**Content-Type**: `multipart/form-data`

**Campos del FormData**:

```python
# Campos comunes (siempre presentes)
job_id: int                    # ID de la oferta laboral
application_type: str          # "upload" o "create"

# Si application_type == "upload"
cv_file: File                  # Archivo PDF/DOC/DOCX (máx 5MB)
cover_letter: str              # Opcional, texto de carta de presentación (máx 1000 chars)

# Si application_type == "create"
cv_data: JSON string           # Objeto JSON con datos del CV (ver estructura abajo)
```

## Estructura del CV Data (application_type == "create")

```json
{
  "personalInfo": {
    "fullName": "string (requerido)",
    "phone": "string (requerido)",
    "email": "string (requerido)",
    "location": "string (requerido)",
    "linkedin": "string (opcional)",
    "portfolio": "string (opcional)"
  },
  "professionalProfile": "string (máx 500 chars)",
  "education": [
    {
      "startYear": "YYYY",
      "endYear": "YYYY o 'Actual'",
      "degree": "string",
      "institution": "string",
      "achievements": "string (logros o GPA)"
    }
  ],
  "experience": [
    {
      "startYear": "YYYY",
      "endYear": "YYYY o 'Actual'",
      "current": boolean,
      "position": "string",
      "company": "string",
      "achievements": ["string", "string", "string"]  // 1-4 elementos
    }
  ],
  "technicalSkills": ["string", "string", ...],
  "softSkills": ["string", "string", ...],
  "certifications": [
    {
      "year": "YYYY",
      "name": "string",
      "institution": "string"
    }
  ],
  "languages": [
    {
      "name": "string",
      "level": "Básico | Intermedio | Avanzado | Nativo / Bilingüe"
    }
  ],
  "projects": [
    {
      "year": "YYYY",
      "name": "string",
      "description": "string"
    }
  ]
}
```

## Modelos Django Sugeridos

### 1. Modelo Application

```python
# G_Jobs/applications/models.py

from django.db import models
from django.contrib.auth.models import User
from G_Jobs.jobs.models import Job

class Application(models.Model):
    """Postulación a una oferta laboral"""

    APPLICATION_TYPE_CHOICES = [
        ('upload', 'CV Subido'),
        ('create', 'CV Creado'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('reviewed', 'Revisada'),
        ('shortlisted', 'Preseleccionado'),
        ('rejected', 'Rechazada'),
        ('accepted', 'Aceptada'),
    ]

    # Relaciones
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')

    # Tipo de postulación
    application_type = models.CharField(max_length=10, choices=APPLICATION_TYPE_CHOICES)

    # Si es tipo 'upload'
    cv_file = models.FileField(upload_to='applications/cvs/', null=True, blank=True)
    cover_letter = models.TextField(max_length=1000, blank=True)

    # Si es tipo 'create'
    cv_template = models.OneToOneField('CVTemplate', on_delete=models.CASCADE, null=True, blank=True)

    # Estado y timestamps
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'g_jobs_applications'
        unique_together = ['candidate', 'job']  # Un candidato solo puede postular una vez
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.candidate.username} -> {self.job.title}"
```

### 2. Modelo CVTemplate

```python
# G_Jobs/applications/models.py

class CVTemplate(models.Model):
    """CV creado en la plataforma (formato Harvard)"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cv_templates')

    # Datos personales
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    # Perfil profesional
    professional_profile = models.TextField(max_length=500, blank=True)

    # Datos estructurados (JSON)
    education = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    technical_skills = models.JSONField(default=list)
    soft_skills = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    languages = models.JSONField(default=list)
    projects = models.JSONField(default=list)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'g_jobs_cv_templates'
        ordering = ['-created_at']

    def __str__(self):
        return f"CV: {self.full_name}"
```

## Vista Django (DRF)

```python
# G_Jobs/applications/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import json

from .models import Application, CVTemplate
from G_Jobs.jobs.models import Job

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_application(request):
    """Endpoint para enviar postulación a una oferta laboral"""

    try:
        # Validar datos comunes
        job_id = request.data.get('job_id')
        application_type = request.data.get('application_type')

        if not job_id or not application_type:
            return Response(
                {'detail': 'job_id y application_type son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if application_type not in ['upload', 'create']:
            return Response(
                {'detail': 'application_type debe ser "upload" o "create"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que el job existe
        try:
            job = Job.objects.get(id=job_id, is_active=True)
        except Job.DoesNotExist:
            return Response(
                {'detail': 'Oferta laboral no encontrada o inactiva'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verificar que el usuario no ha aplicado antes
        if Application.objects.filter(candidate=request.user, job=job).exists():
            return Response(
                {'detail': 'Ya has postulado a esta oferta'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear aplicación según tipo
        with transaction.atomic():
            application = Application(
                candidate=request.user,
                job=job,
                application_type=application_type
            )

            if application_type == 'upload':
                # Tipo: Subir CV
                cv_file = request.FILES.get('cv_file')
                if not cv_file:
                    return Response(
                        {'detail': 'cv_file es requerido para tipo "upload"'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Validar tamaño (5MB)
                if cv_file.size > 5 * 1024 * 1024:
                    return Response(
                        {'detail': 'El archivo no debe superar los 5 MB'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Validar tipo
                allowed_types = ['application/pdf', 'application/msword',
                               'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
                if cv_file.content_type not in allowed_types:
                    return Response(
                        {'detail': 'Solo se permiten archivos PDF, DOC o DOCX'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                application.cv_file = cv_file
                application.cover_letter = request.data.get('cover_letter', '')

            else:  # application_type == 'create'
                # Tipo: Crear CV
                cv_data_str = request.data.get('cv_data')
                if not cv_data_str:
                    return Response(
                        {'detail': 'cv_data es requerido para tipo "create"'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    cv_data = json.loads(cv_data_str)
                except json.JSONDecodeError:
                    return Response(
                        {'detail': 'cv_data debe ser un JSON válido'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Validar campos requeridos
                personal_info = cv_data.get('personalInfo', {})
                if not all([personal_info.get('fullName'),
                           personal_info.get('email'),
                           personal_info.get('phone')]):
                    return Response(
                        {'detail': 'fullName, email y phone son requeridos en personalInfo'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Crear CVTemplate
                cv_template = CVTemplate.objects.create(
                    user=request.user,
                    full_name=personal_info.get('fullName'),
                    phone=personal_info.get('phone'),
                    email=personal_info.get('email'),
                    location=personal_info.get('location', ''),
                    linkedin=personal_info.get('linkedin', ''),
                    portfolio=personal_info.get('portfolio', ''),
                    professional_profile=cv_data.get('professionalProfile', ''),
                    education=cv_data.get('education', []),
                    experience=cv_data.get('experience', []),
                    technical_skills=cv_data.get('technicalSkills', []),
                    soft_skills=cv_data.get('softSkills', []),
                    certifications=cv_data.get('certifications', []),
                    languages=cv_data.get('languages', []),
                    projects=cv_data.get('projects', [])
                )

                application.cv_template = cv_template

            # Guardar aplicación
            application.save()

            # Opcional: Enviar notificación a la empresa
            # send_application_notification(job.company, application)

            return Response({
                'id': application.id,
                'message': 'Postulación enviada correctamente',
                'job_title': job.title,
                'application_type': application_type,
                'created_at': application.created_at.isoformat()
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'detail': f'Error al procesar la postulación: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

## URLs

```python
# G_Jobs/applications/urls.py

from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('submit/', views.submit_application, name='submit'),
]
```

```python
# backend/urls.py (principal)

from django.urls import path, include

urlpatterns = [
    # ... otras urls
    path('api/applications/', include('G_Jobs.applications.urls')),
]
```

## Configuración de Archivos

```python
# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Límites de carga
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

## Migraciones

```bash
# Crear app si no existe
cd backend
python manage.py startapp applications
# Mover a G_Jobs/applications/

# Crear migraciones
python manage.py makemigrations applications

# Aplicar migraciones
python manage.py migrate applications
```

## Serializers Opcionales (para respuestas más estructuradas)

```python
# G_Jobs/applications/serializers.py

from rest_framework import serializers
from .models import Application, CVTemplate

class CVTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVTemplate
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    cv_template = CVTemplateSerializer(read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    candidate_name = serializers.CharField(source='candidate.get_full_name', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'candidate', 'candidate_name', 'job', 'job_title',
            'application_type', 'cv_file', 'cover_letter', 'cv_template',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
```

## Checklist de Implementación

- [ ] Crear app `applications` dentro de `G_Jobs/`
- [ ] Definir modelos `Application` y `CVTemplate`
- [ ] Crear migraciones y ejecutarlas
- [ ] Implementar vista `submit_application`
- [ ] Configurar URLs
- [ ] Configurar `MEDIA_ROOT` y `MEDIA_URL` en settings
- [ ] Agregar validaciones de seguridad (tamaño archivo, tipo)
- [ ] Implementar serializers (opcional pero recomendado)
- [ ] Agregar permisos (solo candidatos pueden postular)
- [ ] Implementar notificaciones a empresas (opcional)
- [ ] Crear vista para que empresas vean postulaciones
- [ ] Crear vista para que candidatos vean sus postulaciones
- [ ] Agregar tests

## Notas de Seguridad

1. **Validación de archivos**: Verificar tipo MIME y extensión real (no solo la extensión del nombre)
2. **Sanitización**: Sanitizar nombres de archivos antes de guardar
3. **Antivirus**: Considerar escaneo de archivos subidos con ClamAV
4. **Permisos**: Solo candidatos autenticados pueden postular
5. **Rate limiting**: Limitar número de postulaciones por usuario/día
6. **CSRF**: El frontend ya incluye token CSRF en headers

## Ejemplo de Respuesta Exitosa

```json
{
  "id": 123,
  "message": "Postulación enviada correctamente",
  "job_title": "Desarrollador Full Stack Senior",
  "application_type": "create",
  "created_at": "2025-12-16T14:30:00Z"
}
```

## Ejemplo de Respuesta con Error

```json
{
  "detail": "Ya has postulado a esta oferta"
}
```
