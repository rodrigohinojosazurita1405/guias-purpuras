from django.db import models
import uuid


def generate_profile_id():
    """Genera un ID único para perfiles"""
    return str(uuid.uuid4())[:8]


class UserProfile(models.Model):
    """Modelo para perfiles de usuarios personales"""

    # ID único
    id = models.CharField(max_length=8, primary_key=True, default=generate_profile_id)

    # Información personal
    fullName = models.CharField(max_length=200, verbose_name="Nombre Completo")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")

    # Foto de perfil
    profilePhoto = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        verbose_name="Foto de Perfil"
    )

    # Información adicional
    location = models.CharField(max_length=200, blank=True, verbose_name="Ubicación")
    bio = models.TextField(blank=True, verbose_name="Biografía")

    # Timestamps
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.fullName} ({self.email})"


class CompanyProfile(models.Model):
    """Modelo genérico para perfiles de empresas - reutilizable en todas las guías"""

    # ID único
    id = models.CharField(max_length=8, primary_key=True, default=generate_profile_id)

    # Relación con usuario propietario
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='company_profiles',
        verbose_name="Propietario"
    )

    # Información de la empresa
    companyName = models.CharField(max_length=200, verbose_name="Nombre de Empresa")
    description = models.TextField(blank=True, verbose_name="Descripción")

    # Logo de la empresa
    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True,
        verbose_name="Logo de Empresa"
    )

    # Banner de la empresa
    banner = models.ImageField(
        upload_to='company_banners/',
        blank=True,
        null=True,
        verbose_name="Banner de Empresa"
    )

    # Contacto
    email = models.EmailField(verbose_name="Email Empresa")
    contactEmail = models.EmailField(blank=True, verbose_name="Email de Contacto Público")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    website = models.URLField(blank=True, verbose_name="Sitio Web")

    # Ubicación
    location = models.CharField(max_length=200, verbose_name="Ubicación")
    city = models.CharField(max_length=100, blank=True, verbose_name="Ciudad")

    # Categoría (para identificar tipo de empresa)
    category = models.CharField(
        max_length=50,
        choices=[
            ('jobs', 'Empleador - Trabajos'),
            ('restaurant', 'Restaurante - Gastronomía'),
            ('business', 'Negocio'),
            ('professional', 'Profesional'),
            ('other', 'Otro')
        ],
        default='other',
        verbose_name="Categoría"
    )

    # Verificación
    verified = models.BooleanField(default=False, verbose_name="Verificada")

    # Timestamps
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Perfil de Empresa"
        verbose_name_plural = "Perfiles de Empresas"
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.companyName} ({self.category})"
