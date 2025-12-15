from django.db import models
from django.conf import settings


class PlanOrder(models.Model):
    """
    Modelo para órdenes de planes
    Almacena la información de facturación y el plan contratado
    """
    # Relación con el trabajo
    job = models.OneToOneField(
        'jobs.Job',
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
        db_table = 'jobs_planorder'  # Mantener nombre de tabla original

    def __str__(self):
        return f"Orden {self.id} - {self.razon_social} - {self.selected_plan}"
