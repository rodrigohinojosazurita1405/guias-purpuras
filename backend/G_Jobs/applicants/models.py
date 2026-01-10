from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import uuid


def validate_file_size(value):
    """Validar que el archivo no exceda 5MB"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("El archivo no debe superar los 5 MB")


def cv_upload_path(instance, filename):
    """
    Determinar la ruta de subida según el tipo de CV
    - CVs creados en builder: applicant_cvs_builder/
    - PDFs subidos externos: applicant_cvs_uploaded/
    """
    if instance.cv_type == 'created':
        return f'applicant_cvs_builder/{filename}'
    else:  # uploaded
        return f'applicant_cvs_uploaded/{filename}'


class ApplicantProfile(models.Model):
    """
    Perfil extendido para usuarios postulantes
    OneToOne con User model
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applicant_profile',
        verbose_name="Usuario"
    )

    # Información personal
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
    has_driver_license = models.BooleanField(
        default=False,
        verbose_name="¿Tiene licencia de conducir?"
    )
    driver_license_category = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Categoría de licencia",
        help_text="Ej: A, B, C, Profesional"
    )

    # Antecedentes penales
    has_criminal_record = models.BooleanField(
        default=False,
        verbose_name="¿Tiene antecedentes penales?"
    )

    # Información de contacto adicional
    # IMPORTANTE: Estos campos se usan en CandidatesView.vue para mostrar contacto en dashboard de reclutadores
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono"
    )
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="WhatsApp",
        help_text="Número de WhatsApp (ej: 59176543210) - Se usa para botón de contacto directo en dashboard"
    )
    linkedin_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Perfil de LinkedIn"
    )
    portfolio_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Portafolio/Sitio Web"
    )

    # Preferencias de búsqueda
    desired_job_categories = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Categorías de trabajo deseadas"
    )
    desired_cities = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Ciudades preferidas"
    )
    desired_modality = models.CharField(
        max_length=20,
        choices=[
            ('presencial', 'Presencial'),
            ('remoto', 'Remoto'),
            ('hibrido', 'Híbrido'),
            ('any', 'Cualquiera')
        ],
        default='any',
        blank=True,
        verbose_name="Modalidad preferida"
    )

    # Estadísticas
    total_applications = models.IntegerField(
        default=0,
        verbose_name="Total de postulaciones"
    )

    # Fechas
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Perfil de Postulante"
        verbose_name_plural = "Perfiles de Postulantes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.email}"


class ApplicantCV(models.Model):
    """
    CVs de los postulantes
    Pueden ser creados en plataforma o subidos como archivo
    Máximo 2 CVs por usuario
    """

    CV_TYPE_CHOICES = [
        ('created', 'CV Creado en Plataforma'),
        ('uploaded', 'CV Subido (PDF/DOC)')
    ]

    # ID único
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Relación con usuario
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cvs',
        verbose_name="Postulante"
    )

    # Tipo de CV
    cv_type = models.CharField(
        max_length=20,
        choices=CV_TYPE_CHOICES,
        verbose_name="Tipo de CV"
    )

    # Nombre del CV (definido por el usuario)
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre del CV",
        help_text="Ej: CV para Desarrollo Web, CV General"
    )

    # Datos del CV creado (formato Harvard)
    cv_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Datos del CV",
        help_text="Datos estructurados del CV en formato Harvard"
    )

    # Archivo subido
    file = models.FileField(
        upload_to=cv_upload_path,
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            validate_file_size
        ],
        verbose_name="Archivo CV"
    )

    # Fechas
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    # Soft delete
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Eliminado"
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de eliminación"
    )

    # Constantes para límite de CVs
    MAX_CREATED_CVS = 2  # Máximo de CVs creados en plataforma
    MAX_UPLOADED_CVS = 1  # Máximo de PDFs externos subidos

    class Meta:
        verbose_name = "CV de Postulante"
        verbose_name_plural = "CVs de Postulantes"
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(cv_type='created', cv_data__isnull=False) |
                      models.Q(cv_type='uploaded', file__isnull=False),
                name='cv_data_or_file_required'
            )
        ]

    def clean(self):
        """Validación personalizada"""
        super().clean()

        # Validar límites según el tipo de CV
        if not self.pk:  # Solo en creación
            if self.cv_type == 'created':
                # Validar máximo de CVs creados
                existing_created = ApplicantCV.objects.filter(
                    applicant=self.applicant,
                    cv_type='created',
                    is_deleted=False
                ).count()

                if existing_created >= self.MAX_CREATED_CVS:
                    raise ValidationError(
                        f"No puedes tener más de {self.MAX_CREATED_CVS} CVs creados. "
                        f"Elimina uno existente antes de crear uno nuevo."
                    )

            elif self.cv_type == 'uploaded':
                # Validar máximo de PDFs subidos
                existing_uploaded = ApplicantCV.objects.filter(
                    applicant=self.applicant,
                    cv_type='uploaded',
                    is_deleted=False
                ).count()

                if existing_uploaded >= self.MAX_UPLOADED_CVS:
                    raise ValidationError(
                        f"Ya tienes un PDF guardado. "
                        f"Elimina el PDF existente antes de subir uno nuevo."
                    )

        # Validar que el tipo de CV tenga los datos correspondientes
        if self.cv_type == 'created' and not self.cv_data:
            raise ValidationError("Un CV creado debe tener datos estructurados")

        if self.cv_type == 'uploaded' and not self.file:
            raise ValidationError("Un CV subido debe tener un archivo adjunto")

    def save(self, *args, **kwargs):
        """Override save para ejecutar validaciones"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.applicant.get_full_name() or self.applicant.email}"


class JobApplication(models.Model):
    """
    Aplicaciones/Postulaciones a trabajos
    Relación entre User, Job y CV
    """

    STATUS_CHOICES = [
        ('submitted', 'Enviada'),
        ('reviewing', 'En Revisión'),
        ('shortlisted', 'Pre-seleccionado'),
        ('interviewed', 'Entrevistado'),
        ('rejected', 'Rechazado'),
        ('accepted', 'Aceptado'),
        ('withdrawn', 'Retirada')
    ]

    # ID único
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Relaciones
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='applicant_applications',
        verbose_name="Trabajo"
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applicant_job_applications',
        verbose_name="Postulante"
    )
    cv = models.ForeignKey(
        ApplicantCV,
        on_delete=models.SET_NULL,
        null=True,
        related_name='applications',
        verbose_name="CV Utilizado"
    )

    # CV adjunto directamente (sin guardar en ApplicantCV)
    attached_cv_file = models.FileField(
        upload_to='application_cvs/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            validate_file_size
        ],
        verbose_name="CV Adjunto",
        help_text="CV enviado directamente con esta postulación"
    )

    # Datos de la aplicación
    cover_letter = models.TextField(
        blank=True,
        verbose_name="Carta de Presentación"
    )

    # Estado
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted',
        verbose_name="Estado"
    )

    # Respuestas a preguntas de filtrado
    screening_answers = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Respuestas a preguntas de filtrado"
    )

    # Notas del empleador
    employer_notes = models.TextField(
        blank=True,
        verbose_name="Notas del empleador"
    )

    # Calificación del candidato (1-5 estrellas)
    rating = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Calificación",
        help_text="Puntuación de 1 a 5 estrellas"
    )

    # Fechas
    applied_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de postulación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    # Visto por el empleador
    viewed_by_employer = models.BooleanField(
        default=False,
        verbose_name="Vista por empleador"
    )
    viewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de visualización"
    )

    class Meta:
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"
        ordering = ['-applied_at']
        unique_together = [['job', 'applicant']]
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['applicant', 'status']),
            models.Index(fields=['-applied_at']),
        ]

    def __str__(self):
        applicant_name = self.applicant.get_full_name() or self.applicant.email
        return f"{applicant_name} → {self.job.title}"


class SavedJob(models.Model):
    """
    Trabajos guardados por los postulantes
    """

    # ID único
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Relaciones
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_jobs',
        verbose_name="Usuario"
    )
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='saved_by_users',
        verbose_name="Trabajo"
    )

    # Fechas
    saved_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de guardado"
    )

    class Meta:
        verbose_name = "Trabajo Guardado"
        verbose_name_plural = "Trabajos Guardados"
        ordering = ['-saved_at']
        unique_together = [['user', 'job']]

    def __str__(self):
        user_name = self.user.get_full_name() or self.user.email
        return f"{user_name} guardó {self.job.title}"
