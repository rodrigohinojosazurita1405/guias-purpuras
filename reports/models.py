from django.db import models
from django.utils import timezone


class DailyReport(models.Model):
    """
    Reporte diario consolidado del sistema
    """
    date = models.DateField(unique=True, db_index=True, verbose_name="Fecha")

    # === USUARIOS ===
    new_users = models.IntegerField(default=0, verbose_name="Nuevos Usuarios")
    new_companies = models.IntegerField(default=0, verbose_name="Nuevas Empresas")
    new_applicants = models.IntegerField(default=0, verbose_name="Nuevos Postulantes")
    total_active_users = models.IntegerField(default=0, verbose_name="Usuarios Activos Totales")

    # === TRABAJOS ===
    new_jobs = models.IntegerField(default=0, verbose_name="Trabajos Publicados")
    active_jobs = models.IntegerField(default=0, verbose_name="Trabajos Activos")
    closed_jobs = models.IntegerField(default=0, verbose_name="Trabajos Cerrados")
    total_views = models.IntegerField(default=0, verbose_name="Vistas Totales")

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
        from jobs.models import Job, PlanOrder
        from plans.models import Plan

        # Obtener o crear el reporte
        report, created = cls.objects.get_or_create(date=date)

        # USUARIOS
        report.new_users = CustomUser.objects.filter(created_at__date=date).count()
        report.new_companies = CustomUser.objects.filter(created_at__date=date, role='company').count()
        report.new_applicants = CustomUser.objects.filter(created_at__date=date, role='applicant').count()
        report.total_active_users = CustomUser.objects.filter(is_active=True).count()

        # TRABAJOS
        report.new_jobs = Job.objects.filter(createdAt__date=date, isDeleted=False).count()
        report.active_jobs = Job.objects.filter(status='active', paymentVerified=True, isDeleted=False).count()
        report.closed_jobs = Job.objects.filter(status='closed', isDeleted=False).count()
        report.total_views = Job.objects.filter(isDeleted=False).aggregate(models.Sum('views'))['views__sum'] or 0

        # PLANES VENDIDOS
        orders_today = PlanOrder.objects.filter(created_at__date=date, status='completed')
        report.plans_sold = orders_today.count()
        report.plan_estandar_count = orders_today.filter(selected_plan='estandar').count()
        report.plan_purpura_count = orders_today.filter(selected_plan='purpura').count()
        report.plan_impulso_count = orders_today.filter(selected_plan='impulso').count()

        # INGRESOS
        report.total_revenue = orders_today.aggregate(models.Sum('plan_price'))['plan_price__sum'] or 0
        report.revenue_estandar = orders_today.filter(selected_plan='estandar').aggregate(models.Sum('plan_price'))['plan_price__sum'] or 0
        report.revenue_purpura = orders_today.filter(selected_plan='purpura').aggregate(models.Sum('plan_price'))['plan_price__sum'] or 0
        report.revenue_impulso = orders_today.filter(selected_plan='impulso').aggregate(models.Sum('plan_price'))['plan_price__sum'] or 0

        report.save()
        return report
