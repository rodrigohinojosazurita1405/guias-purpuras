from django.db import models
import uuid


def generate_job_id():
    """Genera un ID único para el trabajo"""
    return str(uuid.uuid4())[:8]


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
    expiryDate = models.DateField(verbose_name="Fecha de vencimiento")

    # Requisitos
    requirements = models.TextField(verbose_name="Requisitos")
    responsibilities = models.TextField(blank=True, verbose_name="Responsabilidades")
    education = models.CharField(max_length=200, blank=True, verbose_name="Formación requerida")
    experience = models.CharField(max_length=200, blank=True, verbose_name="Experiencia necesaria")
    languages = models.CharField(max_length=200, blank=True, verbose_name="Idiomas requeridos")
    technicalSkills = models.CharField(max_length=500, blank=True, verbose_name="Habilidades técnicas")
    softSkills = models.CharField(max_length=500, blank=True, verbose_name="Habilidades blandas")

    # Compensación
    salaryType = models.CharField(
        max_length=20,
        choices=[
            ('range', 'Rango salarial'),
            ('fixed', 'Salario fijo'),
            ('negotiable', 'A convenir'),
            ('hidden', 'No mostrar')
        ],
        default='range',
        verbose_name="Tipo de salario"
    )
    salaryMin = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salaryMax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salaryFixed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    benefits = models.TextField(blank=True, verbose_name="Beneficios adicionales")

    # Vacantes
    vacancies = models.IntegerField(default=1, verbose_name="Número de vacantes")

    # Contacto
    email = models.EmailField(verbose_name="Email de contacto")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    website = models.URLField(blank=True, verbose_name="Sitio web")
    applicationInstructions = models.TextField(blank=True, verbose_name="Instrucciones de aplicación")

    # Tipo de aplicación
    applicationType = models.CharField(
        max_length=20,
        choices=[
            ('internal', 'Interna'),
            ('external', 'Externa'),
            ('both', 'Ambas')
        ],
        default='internal',
        verbose_name="Tipo de aplicación"
    )
    externalApplicationUrl = models.URLField(blank=True, verbose_name="URL de aplicación externa")

    # Plan
    selectedPlan = models.CharField(
        max_length=20,
        choices=[
            ('escencial', 'Plan Escencial (35 Bs)'),
            ('purpura', 'Plan Púrpura (79 Bs)'),
            ('impulso', 'Plan Impulso Pro (169 Bs)')
        ],
        default='escencial',
        verbose_name="Plan seleccionado"
    )

    # Screening questions (JSON)
    screeningQuestions = models.JSONField(default=list, blank=True, verbose_name="Preguntas de filtrado")

    # Estadísticas
    views = models.IntegerField(default=0, verbose_name="Vistas")
    applications = models.IntegerField(default=0, verbose_name="Aplicaciones")

    # Timestamps
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Activa'),
            ('closed', 'Cerrada'),
            ('draft', 'Borrador')
        ],
        default='active',
        verbose_name="Estado"
    )

    # Información de Facturación (Opcional)
    billingBusinessName = models.CharField(max_length=200, blank=True, null=True, verbose_name="Razón Social")
    billingNIT = models.CharField(max_length=20, blank=True, null=True, verbose_name="NIT")
    billingInvoiceEmail = models.EmailField(blank=True, null=True, verbose_name="Email para factura")

    # Información de Verificación de Pago (FASE 7.1)
    proofOfPayment = models.ImageField(
        upload_to='payment_proofs/',
        null=True,
        blank=False,
        verbose_name="Comprobante de pago"
    )
    paymentVerified = models.BooleanField(
        default=False,
        verbose_name="Pago verificado"
    )
    paymentVerifiedBy = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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

    class Meta:
        verbose_name = "Oferta de Trabajo"
        verbose_name_plural = "Ofertas de Trabajo"
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.title} - {self.companyName}"


class Application(models.Model):
    """Modelo para aplicaciones de candidatos a trabajos"""

    # ID único
    id = models.CharField(max_length=8, primary_key=True, default=generate_job_id)

    # Relación con el trabajo
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_applications',
        verbose_name="Trabajo"
    )

    # Información del candidato
    applicantName = models.CharField(max_length=200, verbose_name="Nombre del candidato")
    applicantEmail = models.EmailField(verbose_name="Email del candidato")
    applicantPhone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    applicantWhatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")

    # Respuestas a preguntas de filtrado
    screeningAnswers = models.JSONField(default=dict, blank=True, verbose_name="Respuestas a preguntas")

    # Estado de la aplicación
    status = models.CharField(
        max_length=20,
        choices=[
            ('received', 'Recibida'),
            ('reviewing', 'En revisión'),
            ('shortlisted', 'Preseleccionada'),
            ('rejected', 'Rechazada'),
            ('accepted', 'Aceptada'),
            ('withdrawn', 'Retirada')
        ],
        default='received',
        verbose_name="Estado"
    )

    # Notas del reclutador
    recruiterNotes = models.TextField(blank=True, verbose_name="Notas del reclutador")

    # Timestamps
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de aplicación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Aplicación"
        verbose_name_plural = "Aplicaciones"
        ordering = ['-createdAt']
        unique_together = ('job', 'applicantEmail')

    def __str__(self):
        return f"{self.applicantName} - {self.job.title}"


class JobAuditLog(models.Model):
    """Modelo para auditoría de cambios en ofertas de trabajo"""

    ACTION_CHOICES = [
        ('created', 'Creado'),
        ('updated', 'Actualizado'),
        ('activated', 'Activado'),
        ('deactivated', 'Desactivado'),
        ('duplicated', 'Duplicado'),
        ('deleted', 'Eliminado'),
        ('payment_verified', 'Pago verificado'),
        ('payment_rejected', 'Pago rechazado'),
    ]

    # ID único
    id = models.CharField(max_length=8, primary_key=True, default=generate_job_id)

    # Relación con el trabajo
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='audit_logs',
        verbose_name="Trabajo"
    )

    # Información del evento
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name="Acción"
    )

    # Email del usuario que realizó la acción
    userEmail = models.EmailField(verbose_name="Email del usuario", blank=True)

    # Campos modificados (para updated)
    changedFields = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Campos modificados",
        help_text="JSON con before/after de los campos que cambieron"
    )

    # Notas/Razón del cambio
    notes = models.TextField(blank=True, verbose_name="Notas")

    # IP del cliente (para rastrear)
    clientIP = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP del cliente")

    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora")

    class Meta:
        verbose_name = "Auditoría de Trabajo"
        verbose_name_plural = "Auditorías de Trabajos"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['job', '-timestamp']),
            models.Index(fields=['userEmail', '-timestamp']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f"{self.job.title} - {self.get_action_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
