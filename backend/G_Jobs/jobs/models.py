from django.db import models
from django.conf import settings
import uuid
from datetime import datetime


def generate_job_id():
    """Genera un ID único para el trabajo"""
    return str(uuid.uuid4())[:8]


def payment_proof_upload_path(instance, filename):
    """
    Genera la ruta de almacenamiento para comprobantes de pago
    Formato: payment_proofs/YYYY/MM/filename
    """
    now = datetime.now()
    return f'payment_proofs/{now.year}/{now.month:02d}/{filename}'


class Job(models.Model):
    """Modelo para ofertas de trabajo"""

    # ID único
    id = models.CharField(max_length=8, primary_key=True, default=generate_job_id)

    # Relación con perfil de empresa (opcional por compatibilidad)
    companyProfile = models.ForeignKey(
        'profiles.CompanyProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='jobs',
        verbose_name="Perfil de Empresa"
    )

    # Información básica
    title = models.CharField(max_length=200, verbose_name="Título del puesto")
    companyName = models.CharField(max_length=200, verbose_name="Nombre de la empresa")
    companyAnonymous = models.BooleanField(default=False, verbose_name="Publicar de forma anónima")
    description = models.TextField(verbose_name="Descripción del trabajo")

    # Categoría y ubicación
    jobCategory = models.CharField(max_length=100, verbose_name="Categoría")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    municipality = models.CharField(max_length=100, blank=True, verbose_name="Provincia/Municipio")
    subcategory = models.CharField(max_length=100, blank=True, verbose_name="Subcategoría")

    # Tipo de contrato
    contractType = models.CharField(max_length=100, verbose_name="Tipo de contrato")
    modality = models.CharField(
        max_length=20,
        choices=[
            ('presencial', 'Presencial'),
            ('remoto', 'Remoto'),
            ('hibrido', 'Híbrido')
        ],
        default='presencial',
        verbose_name="Modalidad de trabajo"
    )

    # Salario
    salaryType = models.CharField(
        max_length=20,
        choices=[
            ('range', 'Rango'),
            ('fixed', 'Fijo'),
            ('negotiable', 'A convenir')
        ],
        default='negotiable',
        verbose_name="Tipo de salario"
    )
    salaryMin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salario mínimo")
    salaryMax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salario máximo")
    salaryFixed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salario fijo")

    # Otros detalles
    benefits = models.TextField(blank=True, verbose_name="Beneficios adicionales")
    vacancies = models.IntegerField(default=1, verbose_name="Número de vacantes")

    # Fechas importantes - CRÍTICO: Dos conceptos diferentes
    expiryDate = models.DateField(verbose_name="Fecha de vencimiento del plan (visibilidad del anuncio)")
    applicationDeadline = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha límite para postulaciones",
        help_text="Fecha límite en que los candidatos pueden postular. Si no se especifica, se usa expiryDate."
    )

    # Fechas
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    publishDate = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de publicación")

    # Estado
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pendiente'),
            ('active', 'Activo'),
            ('paused', 'Pausado'),
            ('closed', 'Cerrado'),
            ('draft', 'Borrador'),
            ('rejected', 'Rechazado')
        ],
        default='pending',
        verbose_name="Estado"
    )

    # Rechazo (para anuncios que violan políticas)
    rejectionReason = models.TextField(
        blank=True,
        verbose_name="Motivo de Rechazo",
        help_text="Razón por la cual el anuncio fue rechazado (violación de políticas, contenido inapropiado, etc.)"
    )
    rejectedAt = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Rechazo"
    )
    rejectedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_superuser': True},
        related_name='rejected_jobs',
        verbose_name="Rechazado por"
    )

    # Email del publicador
    email = models.EmailField(verbose_name="Email del publicador")

    # Estadísticas
    views = models.IntegerField(default=0, verbose_name="Número de vistas")
    applications = models.IntegerField(default=0, verbose_name="Número de aplicaciones")

    # FASE 6: Sistema de Aplicaciones
    applicationType = models.CharField(
        max_length=20,
        choices=[
            ('internal', 'Interna (en Guías Púrpuras)'),
            ('external', 'Externa (URL propia)')
        ],
        default='internal',
        verbose_name="Tipo de aplicación"
    )
    externalApplicationUrl = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL externa de aplicación"
    )
    screeningQuestions = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Preguntas de filtrado"
    )

    # FASE 7: Sistema de Pagos y Planes
    selectedPlan = models.CharField(
        max_length=50,
        choices=[
            ('estandar', 'Estándar'),
            ('purpura', 'Púrpura'),
            ('impulso', 'Impulso Pro')
        ],
        default='estandar',
        verbose_name="Plan seleccionado"
    )

    # Información de Verificación de Pago (FASE 7.1)
    proofOfPayment = models.ImageField(
        upload_to=payment_proof_upload_path,
        null=True,
        blank=False,
        verbose_name="Comprobante de pago"
    )
    paymentVerified = models.BooleanField(
        default=False,
        verbose_name="Pago verificado"
    )
    paymentVerifiedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_superuser': True},
        related_name='verified_jobs',
        verbose_name="Verificado por"
    )
    paymentVerificationDate = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de verificación"
    )
    paymentVerificationNotes = models.TextField(
        blank=True,
        verbose_name="Notas de verificación"
    )

    # Borrado lógico
    isDeleted = models.BooleanField(
        default=False,
        verbose_name="Eliminado (borrado lógico)"
    )
    deletedAt = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de eliminación"
    )

    class Meta:
        verbose_name = "Oferta de Trabajo"
        verbose_name_plural = "Ofertas de Trabajo"
        ordering = ['-createdAt']

    def clean(self):
        """
        Validaciones a nivel de modelo
        """
        from django.core.exceptions import ValidationError

        # Validación CRÍTICA: applicationDeadline debe ser <= expiryDate
        if self.applicationDeadline and self.expiryDate:
            if self.applicationDeadline > self.expiryDate:
                raise ValidationError({
                    'applicationDeadline': 'La fecha límite de postulación no puede ser posterior a la fecha de vencimiento del plan.'
                })

    def save(self, *args, **kwargs):
        """
        Sincronizar estado con verificación de pago automáticamente
        Si el pago es verificado, el trabajo pasa a 'active'
        """
        # Ejecutar validaciones
        self.clean()

        # Si el pago se acaba de verificar
        if self.paymentVerified and self.status == 'pending':
            from django.utils import timezone
            self.status = 'active'
            self.publishDate = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.companyName}"


# ============================================================
# NOTA SOBRE REFACTORIZACIÓN MODULAR
# ============================================================
# Los siguientes modelos han sido movidos a apps especializadas
# para mejor separación de responsabilidades y modularidad:
#
# - PlanOrder → app 'payments' (facturación y pagos)
# - BlockedUser → app 'moderation' (moderación de usuarios)
# - JobCategory, ContractType, City → app 'catalogs' (catálogos dinámicos)
#
# Se mantienen las tablas originales (jobs_planorder, jobs_blockeduser, etc.)
# mediante el atributo db_table en los nuevos modelos.
# Las migraciones históricas NO se modifican para preservar compatibilidad.
# ============================================================
