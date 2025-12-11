from django.db import models
from django.conf import settings
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
    expiryDate = models.DateField(verbose_name="Fecha de vencimiento")

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
            ('draft', 'Borrador')
        ],
        default='pending',
        verbose_name="Estado"
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

    def save(self, *args, **kwargs):
        """
        Sincronizar estado con verificación de pago automáticamente
        Si el pago es verificado, el trabajo pasa a 'active'
        """
        # Si el pago se acaba de verificar
        if self.paymentVerified and self.status == 'pending':
            from django.utils import timezone
            self.status = 'active'
            self.publishDate = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.companyName}"


class PlanOrder(models.Model):
    """
    Modelo para órdenes de planes
    Almacena la información de facturación y el plan contratado
    """
    # Relación con el trabajo
    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name='plan_order',
        verbose_name="Trabajo asociado",
        null=True,
        blank=True
    )

    # Información del usuario que solicita el plan
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plan_orders',
        verbose_name="Usuario"
    )

    # Datos de facturación
    razon_social = models.CharField(
        max_length=200,
        verbose_name="Razón Social"
    )
    nit = models.CharField(
        max_length=50,
        verbose_name="NIT"
    )
    ci = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="CI"
    )
    ci_complement = models.CharField(
        max_length=5,
        blank=True,
        verbose_name="Complemento CI"
    )

    # Datos de contacto
    email = models.EmailField(
        verbose_name="Email para factura",
        default='noreply@guiaspurpuras.com',
        blank=True,
        help_text="Solo requerido si el usuario solicitó factura"
    )
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="WhatsApp"
    )

    # Plan contratado
    selected_plan = models.CharField(
        max_length=50,
        choices=[
            ('estandar', 'Estándar'),
            ('purpura', 'Púrpura'),
            ('impulso', 'Impulso Pro')
        ],
        verbose_name="Plan seleccionado",
        default='estandar'
    )
    plan_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio del plan",
        default=0.00
    )

    # Estado de la orden
    status = models.CharField(
        max_length=20,
        choices=[
            ('processing', 'En Proceso'),
            ('completed', 'Completado')
        ],
        default='processing',
        verbose_name="Estado"
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
        verbose_name = 'Orden de Plan'
        verbose_name_plural = 'Órdenes de Planes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Orden {self.id} - {self.razon_social} - {self.selected_plan}"


class BlockedUser(models.Model):
    """
    Modelo para usuarios bloqueados por empresas
    Permite a las empresas bloquear candidatos específicos
    """
    # Empresa que realiza el bloqueo
    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='users_blocked_by_me',
        limit_choices_to={'role': 'company'},
        verbose_name="Empresa"
    )

    # Usuario bloqueado
    blocked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_by_companies',
        limit_choices_to={'role': 'applicant'},
        verbose_name="Usuario bloqueado"
    )

    # Razón del bloqueo
    reason = models.CharField(
        max_length=50,
        choices=[
            ('spam', 'Spam'),
            ('inappropriate', 'Comportamiento inapropiado'),
            ('unqualified', 'No calificado repetidamente'),
            ('other', 'Otra razón')
        ],
        verbose_name="Razón"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notas adicionales"
    )

    # Fecha del bloqueo
    blocked_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Bloqueado el"
    )

    class Meta:
        verbose_name = 'Usuario Bloqueado'
        verbose_name_plural = 'Usuarios Bloqueados'
        ordering = ['-blocked_at']
        unique_together = ['company', 'blocked_user']
        indexes = [
            models.Index(fields=['company', '-blocked_at']),
            models.Index(fields=['blocked_user']),
        ]

    def __str__(self):
        return f"{self.company.email} bloqueó a {self.blocked_user.email} - {self.get_reason_display()}"


# ============================================================
# NUEVOS MODELOS DINÁMICOS PARA CRUD
# ============================================================

class JobCategory(models.Model):
    """
    Categorías de trabajo dinámicas
    Permite gestionar categorías desde Django Admin
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la categoría"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="Slug (auto-generado)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Nombre del ícono (Material Icons)",
        verbose_name="Ícono"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Categoría de Trabajo"
        verbose_name_plural = "Categorías de Trabajo"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ContractType(models.Model):
    """
    Tipos de contrato dinámicos
    Permite gestionar tipos de contrato desde Django Admin
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre del tipo de contrato"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="Slug (auto-generado)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Tipo de Contrato"
        verbose_name_plural = "Tipos de Contrato"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Ciudades/Departamentos dinámicos
    Permite gestionar ciudades desde Django Admin
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la ciudad"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="Slug (auto-generado)"
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Departamento"
    )
    region = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('altiplano', 'Altiplano'),
            ('valles', 'Valles'),
            ('llanos', 'Llanos'),
        ],
        verbose_name="Región"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
            models.Index(fields=['region']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.department})" if self.department else self.name
