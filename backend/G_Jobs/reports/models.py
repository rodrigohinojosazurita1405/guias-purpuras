from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile
from decimal import Decimal


class DailyReport(models.Model):
    """
    Reporte diario consolidado del sistema
    """
    date = models.DateField(unique=True, db_index=True, verbose_name="Fecha")

    # === USUARIOS ===
    new_users = models.IntegerField(default=0, verbose_name="Nuevos Usuarios")
    new_companies = models.IntegerField(default=0, verbose_name="Nuevas Empresas")
    new_applicants = models.IntegerField(default=0, verbose_name="Nuevos Postulantes")
    total_active_users = models.IntegerField(default=0, verbose_name="Usuarios Activos (Snapshot)")

    # === TRABAJOS ===
    new_jobs = models.IntegerField(default=0, verbose_name="Trabajos Publicados")
    active_jobs = models.IntegerField(default=0, verbose_name="Trabajos Activos (Snapshot)")
    closed_jobs = models.IntegerField(default=0, verbose_name="Trabajos Cerrados (Snapshot)")
    jobs_closed_today = models.IntegerField(default=0, verbose_name="Trabajos Cerrados Hoy")
    total_views = models.IntegerField(default=0, verbose_name="Vistas Totales (Snapshot)")
    views_today = models.IntegerField(default=0, verbose_name="Vistas del Día")

    # === PLANES ===
    plans_sold = models.IntegerField(default=0, verbose_name="Planes Vendidos")
    plan_estandar_count = models.IntegerField(default=0, verbose_name="Plan Estándar")
    plan_purpura_count = models.IntegerField(default=0, verbose_name="Plan Púrpura")
    plan_impulso_count = models.IntegerField(default=0, verbose_name="Plan Impulso")

    # === INGRESOS ===
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ingresos Totales (Bs)")
    revenue_estandar = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ingresos Estándar")
    revenue_purpura = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ingresos Púrpura")
    revenue_impulso = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ingresos Impulso")

    # === APLICACIONES ===
    applications_received = models.IntegerField(default=0, verbose_name="Aplicaciones Recibidas")

    # === METADATA ===
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Generado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Reporte Diario"
        verbose_name_plural = "Reportes Diarios"
        ordering = ['-date']

    def __str__(self):
        return f"Reporte {self.date} - {self.plans_sold} planes - {self.total_revenue} Bs"

    @classmethod
    def generate_report(cls, date=None):
        """Genera o actualiza el reporte para una fecha específica"""
        if date is None:
            date = timezone.now().date()

        from auth_api.models import CustomUser
        from G_Jobs.jobs.models import Job
        from G_Jobs.payments.models import PlanOrder
        from G_Jobs.applicants.models import JobApplication
        from django.db.models import Sum, Q

        # Obtener o crear el reporte
        report, created = cls.objects.get_or_create(date=date)

        # === USUARIOS (DIARIOS) ===
        report.new_users = CustomUser.objects.filter(created_at__date=date).count()
        report.new_companies = CustomUser.objects.filter(created_at__date=date, role='company').count()
        report.new_applicants = CustomUser.objects.filter(created_at__date=date, role='applicant').count()
        # Snapshot: Total de usuarios activos al momento de generar el reporte
        report.total_active_users = CustomUser.objects.filter(is_active=True).count()

        # === TRABAJOS (DIARIOS + SNAPSHOTS) ===
        # Trabajos creados ese día
        report.new_jobs = Job.objects.filter(createdAt__date=date, isDeleted=False).count()

        # Trabajos cerrados ese día específicamente
        report.jobs_closed_today = Job.objects.filter(
            isDeleted=False,
            status='closed',
            updatedAt__date=date  # Asumiendo que updatedAt refleja el cambio de estado
        ).count()

        # Snapshots: Estado actual al generar el reporte
        report.active_jobs = Job.objects.filter(status='active', paymentVerified=True, isDeleted=False).count()
        report.closed_jobs = Job.objects.filter(status='closed', isDeleted=False).count()
        report.total_views = Job.objects.filter(isDeleted=False).aggregate(Sum('views'))['views__sum'] or 0

        # Vistas del día (si existe tracking de vistas diarias, por ahora usamos 0)
        # TODO: Implementar tracking de vistas diarias si es necesario
        report.views_today = 0

        # === PLANES VENDIDOS (DIARIOS) ===
        orders_today = PlanOrder.objects.filter(created_at__date=date, status='completed')
        report.plans_sold = orders_today.count()
        report.plan_estandar_count = orders_today.filter(selected_plan='estandar').count()
        report.plan_purpura_count = orders_today.filter(selected_plan='purpura').count()
        report.plan_impulso_count = orders_today.filter(selected_plan='impulso').count()

        # === INGRESOS (DIARIOS) ===
        report.total_revenue = orders_today.aggregate(Sum('plan_price'))['plan_price__sum'] or Decimal('0')
        report.revenue_estandar = orders_today.filter(selected_plan='estandar').aggregate(Sum('plan_price'))['plan_price__sum'] or Decimal('0')
        report.revenue_purpura = orders_today.filter(selected_plan='purpura').aggregate(Sum('plan_price'))['plan_price__sum'] or Decimal('0')
        report.revenue_impulso = orders_today.filter(selected_plan='impulso').aggregate(Sum('plan_price'))['plan_price__sum'] or Decimal('0')

        # === APLICACIONES (DIARIAS) ===
        report.applications_received = JobApplication.objects.filter(applied_at__date=date).count()

        report.save()
        return report


class Report(models.Model):
    """
    Modelo para reportes PDF generados (diarios, semanales, mensuales)
    """
    REPORT_TYPES = [
        ('daily', 'Diario'),
        ('weekly', 'Semanal (Lun-Dom)'),
        ('last_7_days', 'Últimos 7 Días'),
        ('monthly', 'Mensual'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('generating', 'Generando'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]

    # Información básica
    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPES,
        verbose_name="Tipo de Reporte"
    )
    period_start = models.DateField(verbose_name="Inicio del Período")
    period_end = models.DateField(verbose_name="Fin del Período")

    # Archivo PDF
    pdf_file = models.FileField(
        upload_to='reports/pdf/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Archivo PDF"
    )

    # Métricas calculadas (JSON)
    metrics = models.JSONField(
        default=dict,
        verbose_name="Métricas Calculadas",
        help_text="JSON con todas las métricas del período"
    )

    # Estado del reporte
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado"
    )

    # Metadata
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name="Generado el")
    generated_by = models.ForeignKey(
        'auth_api.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Generado por"
    )
    error_message = models.TextField(
        blank=True,
        verbose_name="Mensaje de Error",
        help_text="Si falló, guardar el error aquí"
    )

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['-generated_at']),
            models.Index(fields=['report_type', 'status']),
        ]

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.period_start} a {self.period_end}"

    @property
    def period_label(self):
        """Retorna una etiqueta legible del período"""
        if self.report_type == 'daily':
            return self.period_start.strftime('%d de %B %Y')
        elif self.report_type == 'weekly':
            return f"{self.period_start.strftime('%d/%m')} - {self.period_end.strftime('%d/%m/%Y')}"
        elif self.report_type == 'last_7_days':
            return f"Ultimos 7 dias ({self.period_start.strftime('%d/%m')} - {self.period_end.strftime('%d/%m/%Y')})"
        else:  # monthly
            return self.period_start.strftime('%B %Y')

    @property
    def has_pdf(self):
        """Retorna True si el PDF fue generado"""
        return bool(self.pdf_file)

    def get_key_metrics_summary(self):
        """Retorna resumen de métricas clave para mostrar en admin"""
        if not self.metrics:
            return "Sin métricas"

        revenue = self.metrics.get('revenue', {})
        plans = self.metrics.get('plans', {})

        total_revenue = revenue.get('total', 0)
        total_plans = plans.get('total_sold', 0)

        return f"{total_revenue} Bs • {total_plans} planes"
