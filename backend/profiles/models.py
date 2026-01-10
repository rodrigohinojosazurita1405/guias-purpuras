from django.db import models
from django.core.files.base import ContentFile
import uuid
from PIL import Image
from io import BytesIO
import os


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

    # Información personal adicional
    ci = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Cédula de Identidad",
        help_text="Número de CI o documento de identidad"
    )
    nationality = models.CharField(
        max_length=100,
        blank=True,
        default="Boliviana",
        verbose_name="Nacionalidad"
    )

    # Licencia de conducir
    hasDriverLicense = models.BooleanField(
        default=False,
        verbose_name="¿Tiene licencia de conducir?"
    )
    driverLicenseCategory = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Categoría de licencia",
        help_text="Ej: A, B, C, Profesional"
    )

    # Antecedentes penales
    hasCriminalRecord = models.BooleanField(
        default=False,
        verbose_name="¿Tiene antecedentes penales?"
    )

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

    def compress_profile_photo(self):
        """
        Comprime y redimensiona la foto de perfil a 400x400px

        Returns:
            ContentFile con la imagen comprimida o None si no hay imagen
        """
        if not self.profilePhoto:
            return None

        try:
            # Abrir la imagen
            img = Image.open(self.profilePhoto)

            # Convertir a RGB si es necesario (para soportar PNG con transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Crear fondo blanco
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Redimensionar a 400x400px (cuadrado) con crop inteligente
            target_size = (400, 400)

            # Calcular crop para mantener el centro
            width, height = img.size

            if width != height:
                # Hacer la imagen cuadrada recortando desde el centro
                min_dimension = min(width, height)
                left = (width - min_dimension) / 2
                top = (height - min_dimension) / 2
                right = (width + min_dimension) / 2
                bottom = (height + min_dimension) / 2

                img = img.crop((left, top, right, bottom))

            # Redimensionar con antialiasing de alta calidad
            img = img.resize(target_size, Image.Resampling.LANCZOS)

            # Guardar en buffer
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)

            # Obtener el nombre del archivo original
            filename = os.path.basename(self.profilePhoto.name)
            # Cambiar extensión a .jpg
            filename = os.path.splitext(filename)[0] + '.jpg'

            return ContentFile(output.read(), name=filename)

        except Exception as e:
            print(f"Error comprimiendo foto de perfil: {e}")
            return None

    def save(self, *args, **kwargs):
        """Sobrescribe save() para comprimir foto de perfil antes de guardar"""

        # Comprimir foto de perfil si existe
        if self.profilePhoto:
            compressed_photo = self.compress_profile_photo()
            if compressed_photo:
                self.profilePhoto = compressed_photo

        super().save(*args, **kwargs)


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
    # MVP: Solo categoría 'jobs' activa
    category = models.CharField(
        max_length=50,
        choices=[
            ('jobs', 'Empleador - Trabajos'),
            # FUTURO: Descomentar cuando se expanda a otros tipos de perfiles
            # ('restaurant', 'Restaurante - Gastronomía'),
            # ('business', 'Negocio'),
            # ('professional', 'Profesional'),
            # ('other', 'Otro')
        ],
        default='jobs',  # Cambiado de 'other' a 'jobs' para MVP
        verbose_name="Categoría"
    )

    # Información Legal (para verificación)
    nit = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="NIT (Número de Identificación Tributaria)"
    )
    legalName = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Razón Social"
    )
    seprecCode = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Código SEPREC (Matrícula de Comercio)"
    )

    # Verificación
    verified = models.BooleanField(default=False, verbose_name="Verificada")
    verificationRequestedAt = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Solicitud de Verificación"
    )
    verificationNotes = models.TextField(
        blank=True,
        verbose_name="Notas de Verificación (solo admin)"
    )

    # Timestamps
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Perfil de Empresa"
        verbose_name_plural = "Perfiles de Empresas"
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.companyName} ({self.category})"

    def compress_image(self, image_field, max_width, max_height, quality=85):
        """
        Comprime y redimensiona una imagen manteniendo la relación de aspecto

        Args:
            image_field: Campo de imagen (logo o banner)
            max_width: Ancho máximo permitido
            max_height: Alto máximo permitido
            quality: Calidad de compresión JPEG (1-100, default 85)

        Returns:
            ContentFile con la imagen comprimida o None si no hay imagen
        """
        if not image_field:
            return None

        try:
            # Abrir la imagen
            img = Image.open(image_field)

            # Convertir a RGB si es necesario (para soportar PNG con transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Crear fondo blanco
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Obtener dimensiones originales
            original_width, original_height = img.size

            # Calcular nuevas dimensiones manteniendo aspect ratio
            if original_width > max_width or original_height > max_height:
                # Calcular ratio de redimensionamiento
                width_ratio = max_width / original_width
                height_ratio = max_height / original_height
                ratio = min(width_ratio, height_ratio)

                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)

                # Redimensionar con antialiasing de alta calidad
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Guardar en buffer
            output = BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)

            # Obtener el nombre del archivo original
            filename = os.path.basename(image_field.name)
            # Cambiar extensión a .jpg
            filename = os.path.splitext(filename)[0] + '.jpg'

            return ContentFile(output.read(), name=filename)

        except Exception as e:
            print(f"Error comprimiendo imagen: {e}")
            return None

    def save(self, *args, **kwargs):
        """Sobrescribe save() para comprimir imágenes antes de guardar"""

        # Comprimir logo si existe
        if self.logo:
            compressed_logo = self.compress_image(
                self.logo,
                max_width=800,
                max_height=800,
                quality=85
            )
            if compressed_logo:
                self.logo = compressed_logo

        # Comprimir banner si existe
        if self.banner:
            compressed_banner = self.compress_image(
                self.banner,
                max_width=2400,
                max_height=600,
                quality=90  # Mayor calidad para banners
            )
            if compressed_banner:
                self.banner = compressed_banner

        super().save(*args, **kwargs)
