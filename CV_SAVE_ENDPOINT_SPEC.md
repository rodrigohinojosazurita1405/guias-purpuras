# Especificación del Endpoint: Guardar CV en Dashboard

## Resumen

Este endpoint permite a los usuarios postulantes guardar CVs en su dashboard para usarlos posteriormente al postular a ofertas. Cada postulante puede tener hasta **máximo 2 CVs guardados**.

## Endpoint

### POST /api/cvs/save/

**Autenticación**: Requerida (usuario debe estar autenticado)

**Rol permitido**: Solo `applicant` (postulantes)

**Content-Type**: `application/json`

## Request Body

```json
{
  "cv_data": {
    "personalInfo": {
      "fullName": "Juan Carlos Pérez López",
      "phone": "+591 70123456",
      "email": "juan.perez@email.com",
      "location": "La Paz, Bolivia",
      "linkedin": "linkedin.com/in/juanperez",
      "portfolio": "www.juanperez.dev"
    },
    "professionalProfile": "Desarrollador Full Stack con 5+ años de experiencia...",
    "education": [
      {
        "startYear": "2015",
        "endYear": "2019",
        "degree": "Licenciatura en Ingeniería de Sistemas",
        "institution": "Universidad Mayor de San Andrés",
        "achievements": "Graduado con honores, GPA: 3.8/4.0"
      }
    ],
    "experience": [
      {
        "startYear": "2019",
        "endYear": "Actual",
        "current": true,
        "position": "Desarrollador Full Stack Senior",
        "company": "Tech Solutions SRL",
        "achievements": [
          "Lideré equipo de 5 desarrolladores que incrementó productividad en 40%",
          "Implementé arquitectura microservicios reduciendo costos en 30%"
        ]
      }
    ],
    "technicalSkills": ["JavaScript", "Vue.js", "Django", "PostgreSQL"],
    "softSkills": ["Liderazgo", "Comunicación efectiva"],
    "certifications": [
      {
        "year": "2023",
        "name": "AWS Certified Solutions Architect",
        "institution": "Amazon Web Services"
      }
    ],
    "languages": [
      {
        "name": "Español",
        "level": "Nativo / Bilingüe"
      },
      {
        "name": "Inglés",
        "level": "Avanzado"
      }
    ],
    "projects": [
      {
        "year": "2024",
        "name": "Sistema ERP empresarial",
        "description": "Desarrollé plataforma que redujo tiempo de procesamiento en 50%"
      }
    ]
  }
}
```

## Response - Success (201 Created)

```json
{
  "success": true,
  "message": "CV guardado correctamente en tu dashboard",
  "cv": {
    "id": 15,
    "user_id": 123,
    "full_name": "Juan Carlos Pérez López",
    "created_at": "2025-12-16T14:30:00Z",
    "updated_at": "2025-12-16T14:30:00Z"
  },
  "total_cvs": 1
}
```

## Response - Error (400 Bad Request)

### Error: Límite de CVs alcanzado

```json
{
  "success": false,
  "detail": "Has alcanzado el límite máximo de 2 CVs. Elimina uno antes de crear otro."
}
```

### Error: Datos inválidos

```json
{
  "success": false,
  "detail": "Los datos del CV son inválidos",
  "errors": {
    "personalInfo.fullName": "El nombre completo es requerido",
    "personalInfo.email": "El email es requerido"
  }
}
```

## Response - Error (401 Unauthorized)

```json
{
  "detail": "Credenciales de autenticación no proporcionadas"
}
```

## Response - Error (403 Forbidden)

```json
{
  "detail": "Solo los postulantes pueden guardar CVs"
}
```

## Modelo Django

```python
# G_Jobs/cvs/models.py

from django.db import models
from django.contrib.auth.models import User

class SavedCV(models.Model):
    """CV guardado por un postulante en su dashboard"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_cvs',
        limit_choices_to={'role': 'applicant'}  # Solo postulantes
    )

    # Datos personales (extraídos para búsqueda rápida)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    location = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    # Perfil profesional
    professional_profile = models.TextField(max_length=500, blank=True)

    # Datos estructurados (JSON) - Formato Harvard
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
        db_table = 'g_jobs_saved_cvs'
        ordering = ['-created_at']
        verbose_name = 'CV Guardado'
        verbose_name_plural = 'CVs Guardados'

    def __str__(self):
        return f"CV: {self.full_name} (Usuario: {self.user.username})"

    @classmethod
    def can_user_add_cv(cls, user):
        """Verifica si el usuario puede agregar otro CV (máx 2)"""
        return cls.objects.filter(user=user).count() < 2
```

## Vista Django (DRF)

```python
# G_Jobs/cvs/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import SavedCV
from .serializers import SavedCVSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_cv(request):
    """
    Guardar CV en el dashboard del usuario postulante.
    Límite: 2 CVs por usuario.
    """

    try:
        # Validar que el usuario sea postulante
        if request.user.role != 'applicant':
            return Response(
                {'detail': 'Solo los postulantes pueden guardar CVs'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validar límite de CVs (máximo 2)
        if not SavedCV.can_user_add_cv(request.user):
            return Response(
                {
                    'success': False,
                    'detail': 'Has alcanzado el límite máximo de 2 CVs. Elimina uno antes de crear otro.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener datos del CV
        cv_data = request.data.get('cv_data')

        if not cv_data:
            return Response(
                {'detail': 'cv_data es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar datos personales requeridos
        personal_info = cv_data.get('personalInfo', {})
        required_fields = ['fullName', 'email', 'phone']

        for field in required_fields:
            if not personal_info.get(field):
                return Response(
                    {'detail': f'{field} es requerido en personalInfo'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Crear SavedCV
        with transaction.atomic():
            saved_cv = SavedCV.objects.create(
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

        # Contar CVs del usuario
        total_cvs = SavedCV.objects.filter(user=request.user).count()

        return Response({
            'success': True,
            'message': 'CV guardado correctamente en tu dashboard',
            'cv': {
                'id': saved_cv.id,
                'user_id': saved_cv.user.id,
                'full_name': saved_cv.full_name,
                'created_at': saved_cv.created_at.isoformat(),
                'updated_at': saved_cv.updated_at.isoformat()
            },
            'total_cvs': total_cvs
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'detail': f'Error al guardar CV: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_my_cvs(request):
    """
    Listar CVs guardados del usuario actual.
    """

    try:
        # Validar que el usuario sea postulante
        if request.user.role != 'applicant':
            return Response(
                {'detail': 'Solo los postulantes tienen CVs guardados'},
                status=status.HTTP_403_FORBIDDEN
            )

        cvs = SavedCV.objects.filter(user=request.user)
        serializer = SavedCVSerializer(cvs, many=True)

        return Response({
            'success': True,
            'cvs': serializer.data,
            'total': cvs.count(),
            'can_add_more': SavedCV.can_user_add_cv(request.user)
        })

    except Exception as e:
        return Response(
            {'detail': f'Error al obtener CVs: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cv(request, cv_id):
    """
    Eliminar un CV guardado del usuario.
    """

    try:
        cv = SavedCV.objects.get(id=cv_id, user=request.user)
        cv.delete()

        return Response({
            'success': True,
            'message': 'CV eliminado correctamente'
        })

    except SavedCV.DoesNotExist:
        return Response(
            {'detail': 'CV no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'detail': f'Error al eliminar CV: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

## Serializer

```python
# G_Jobs/cvs/serializers.py

from rest_framework import serializers
from .models import SavedCV

class SavedCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedCV
        fields = [
            'id',
            'full_name',
            'phone',
            'email',
            'location',
            'linkedin',
            'portfolio',
            'professional_profile',
            'education',
            'experience',
            'technical_skills',
            'soft_skills',
            'certifications',
            'languages',
            'projects',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
```

## URLs

```python
# G_Jobs/cvs/urls.py

from django.urls import path
from . import views

app_name = 'cvs'

urlpatterns = [
    path('save/', views.save_cv, name='save'),
    path('list/', views.list_my_cvs, name='list'),
    path('delete/<int:cv_id>/', views.delete_cv, name='delete'),
]
```

```python
# backend/urls.py (principal)

urlpatterns = [
    # ... otras urls
    path('api/cvs/', include('G_Jobs.cvs.urls')),
]
```

## Flujo Completo

### 1. Usuario crea CV en modal

```
Usuario completa formulario Harvard → Click "Guardar en Dashboard"
  ↓
Frontend valida: isAuthenticated && role === 'applicant'
  ↓
Envía POST /api/cvs/save/ con cv_data
  ↓
Backend valida:
  - Usuario autenticado ✓
  - Rol = applicant ✓
  - CVs actuales < 2 ✓
  - Datos válidos ✓
  ↓
Guarda en BD como SavedCV
  ↓
Retorna success + total_cvs
  ↓
Frontend muestra toast: "CV guardado correctamente"
```

### 2. Usuario intenta guardar 3er CV

```
Usuario ya tiene 2 CVs guardados
  ↓
Click "Guardar en Dashboard"
  ↓
POST /api/cvs/save/
  ↓
Backend detecta: CVs actuales >= 2
  ↓
Retorna 400: "Has alcanzado el límite máximo..."
  ↓
Frontend muestra toast warning con el mensaje
```

### 3. Dashboard de CVs (Vista futura)

```
Usuario va a /dashboard/cvs
  ↓
GET /api/cvs/list/
  ↓
Backend retorna lista de CVs guardados
  ↓
Frontend muestra:
  - Lista de CVs con preview
  - Botón "Usar este CV" para postular
  - Botón "Eliminar CV"
  - Indicador: "2/2 CVs guardados" o "1/2 CVs guardados"
  - Botón "Crear nuevo CV" (deshabilitado si tiene 2)
```

## Integración Frontend Completa

### JobDetailPanel.vue

```javascript
methods: {
  async handleSaveCV(data) {
    try {
      // Validar rol
      if (this.authStore.user?.role !== 'applicant') {
        this.$vaToast.init({
          message: 'Solo los postulantes pueden guardar CVs',
          color: 'danger'
        })
        return
      }

      // Enviar al backend
      const response = await fetch('/api/cvs/save/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCsrfToken()
        },
        body: JSON.stringify({ cv_data: data.cvData }),
        credentials: 'include'
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail)
      }

      const result = await response.json()

      // Toast de éxito
      this.$vaToast.init({
        message: result.message || 'CV guardado correctamente',
        color: 'success',
        duration: 3000
      })

    } catch (error) {
      // Toast de error (incluyendo límite de CVs)
      this.$vaToast.init({
        message: error.message || 'Error al guardar CV',
        color: error.message.includes('máximo') ? 'warning' : 'danger',
        duration: 5000
      })
    }
  }
}
```

## Migraciones

```bash
# Crear app si no existe
cd backend
mkdir -p G_Jobs/cvs
python manage.py startapp cvs
# Mover a G_Jobs/cvs/

# Crear migraciones
python manage.py makemigrations cvs

# Aplicar migraciones
python manage.py migrate cvs
```

## Checklist de Implementación

- [ ] Crear app `cvs` dentro de `G_Jobs/`
- [ ] Definir modelo `SavedCV`
- [ ] Crear migraciones y ejecutarlas
- [ ] Implementar vista `save_cv` con validación de límite
- [ ] Implementar vista `list_my_cvs`
- [ ] Implementar vista `delete_cv`
- [ ] Crear serializer `SavedCVSerializer`
- [ ] Configurar URLs
- [ ] Probar límite de 2 CVs
- [ ] Probar que solo postulantes pueden guardar
- [ ] Crear vista Dashboard de CVs (frontend)
- [ ] Implementar funcionalidad "Usar este CV" al postular

## Testing

```python
# G_Jobs/cvs/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import SavedCV

class SavedCVTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='applicant'
        )

    def test_can_add_cv_when_zero(self):
        self.assertTrue(SavedCV.can_user_add_cv(self.user))

    def test_can_add_cv_when_one(self):
        SavedCV.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@test.com',
            phone='123456',
            education=[],
            experience=[]
        )
        self.assertTrue(SavedCV.can_user_add_cv(self.user))

    def test_cannot_add_cv_when_two(self):
        # Crear 2 CVs
        for i in range(2):
            SavedCV.objects.create(
                user=self.user,
                full_name=f'Test User {i}',
                email='test@test.com',
                phone='123456',
                education=[],
                experience=[]
            )
        self.assertFalse(SavedCV.can_user_add_cv(self.user))
```

## Notas de Seguridad

1. **Validación de rol**: Solo usuarios con `role='applicant'` pueden guardar CVs
2. **Límite estricto**: Máximo 2 CVs por usuario (validado en backend)
3. **Ownership**: Solo el propietario puede ver/eliminar sus CVs
4. **Validación de datos**: Campos requeridos validados antes de guardar
5. **CSRF Protection**: Token CSRF incluido en todas las peticiones
