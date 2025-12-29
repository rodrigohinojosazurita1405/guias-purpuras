from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import date, timedelta
from .models import DailyReport, Report
from .services.pdf_generator import generate_daily_report, generate_weekly_report, generate_monthly_report
import datetime


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    """Admin con visualizaciones para reportes diarios"""

    list_display = (
        'date',
        'users_summary',
        'jobs_summary',
        'plans_summary',
        'revenue_display',
        'actions_column',
    )

    list_filter = ('date',)
    date_hierarchy = 'date'

    readonly_fields = (
        'date', 'new_users', 'new_companies', 'new_applicants', 'total_active_users',
        'new_jobs', 'active_jobs', 'closed_jobs', 'jobs_closed_today', 'total_views', 'views_today',
        'plans_sold', 'plan_estandar_count', 'plan_purpura_count', 'plan_impulso_count',
        'total_revenue', 'revenue_estandar', 'revenue_purpura', 'revenue_impulso',
        'applications_received', 'created_at', 'updated_at',
    )

    fieldsets = (
        ('Fecha', {'fields': ('date',)}),
        ('Usuarios', {
            'fields': ('new_users', 'new_companies', 'new_applicants', 'total_active_users'),
            'classes': ('wide',)
        }),
        ('Trabajos', {
            'fields': ('new_jobs', 'active_jobs', 'closed_jobs', 'jobs_closed_today', 'total_views', 'views_today'),
            'classes': ('wide',)
        }),
        ('Planes Vendidos', {
            'fields': ('plans_sold', 'plan_estandar_count', 'plan_purpura_count', 'plan_impulso_count'),
            'classes': ('wide',)
        }),
        ('Ingresos', {
            'fields': ('total_revenue', 'revenue_estandar', 'revenue_purpura', 'revenue_impulso'),
            'classes': ('wide',)
        }),
        ('Aplicaciones', {
            'fields': ('applications_received',),
            'classes': ('wide',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def users_summary(self, obj):
        return format_html(
            '<div style="line-height: 1.6;">'
            '<strong style="color: #7c3aed; font-size: 1.2rem;">{}</strong> nuevos<br>'
            '<span style="color: #10b981;">📈 {} empresas</span> • '
            '<span style="color: #3b82f6;">👤 {} postulantes</span>'
            '</div>',
            obj.new_users,
            obj.new_companies,
            obj.new_applicants
        )
    users_summary.short_description = 'Usuarios'

    def jobs_summary(self, obj):
        return format_html(
            '<div>'
            '<strong style="color: #10b981;">+ {}</strong> nuevos | '
            '<span style="color: #3b82f6;">{} activos</span> | '
            '<span style="color: #6b7280;">{} vistas</span>'
            '</div>',
            obj.new_jobs,
            obj.active_jobs,
            obj.total_views
        )
    jobs_summary.short_description = 'Trabajos'

    def plans_summary(self, obj):
        return format_html(
            '<div style="display: flex; gap: 8px; flex-wrap: wrap;">'
            '<span style="background: #f3f4f6; padding: 4px 10px; border-radius: 8px; font-weight: 600;">Total: {}</span>'
            '<span style="background: #dbeafe; color: #1e40af; padding: 4px 8px; border-radius: 8px; font-size: 0.85rem;">{} Est</span>'
            '<span style="background: #ede9fe; color: #6d28d9; padding: 4px 8px; border-radius: 8px; font-size: 0.85rem;">{} Púr</span>'
            '<span style="background: #d1fae5; color: #065f46; padding: 4px 8px; border-radius: 8px; font-size: 0.85rem;">{} Imp</span>'
            '</div>',
            obj.plans_sold,
            obj.plan_estandar_count,
            obj.plan_purpura_count,
            obj.plan_impulso_count
        )
    plans_summary.short_description = 'Planes'

    def revenue_display(self, obj):
        return format_html(
            '<div style="font-size: 1.1rem; font-weight: 700; color: #10b981;">'
            '{} Bs'
            '</div>',
            f'{obj.total_revenue:.2f}'
        )
    revenue_display.short_description = 'Ingresos'
    revenue_display.admin_order_field = 'total_revenue'

    def actions_column(self, obj):
        return format_html(
            '<a class="button" style="padding: 6px 12px; background: #7c3aed; color: white; border-radius: 6px; text-decoration: none; font-size: 0.85rem;" '
            'href="{}">Regenerar</a>',
            f'/admin/reports/dailyreport/{obj.pk}/regenerate/'
        )
    actions_column.short_description = 'Acciones'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-today/', self.admin_site.admin_view(self.generate_today_report), name='reports_generate_today'),
            path('<path:object_id>/regenerate/', self.admin_site.admin_view(self.regenerate_report), name='reports_regenerate'),
        ]
        return custom_urls + urls

    def generate_today_report(self, request):
        """Vista para generar el reporte de hoy"""
        report = DailyReport.generate_report()
        self.message_user(request, f'Reporte generado: {report}')
        return HttpResponse(status=302, headers={'Location': '/admin/reports/dailyreport/'})

    def regenerate_report(self, request, object_id):
        """Vista para regenerar un reporte específico"""
        report = self.get_object(request, object_id)
        if report:
            DailyReport.generate_report(date=report.date)
            self.message_user(request, f'Reporte regenerado: {report.date}')
        return HttpResponse(status=302, headers={'Location': f'/admin/reports/dailyreport/{object_id}/change/'})

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_today_url'] = '/admin/reports/dailyreport/generate-today/'
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin para reportes PDF generados"""

    list_display = (
        'report_type_badge',
        'period_display',
        'status_badge',
        'metrics_summary',
        'pdf_download_button',
        'generated_at',
    )

    list_filter = (
        'report_type',
        'status',
        'generated_at',
    )

    search_fields = ('period_start', 'period_end')
    date_hierarchy = 'generated_at'

    readonly_fields = (
        'generated_at',
        'generated_by',
        'period_label',
        'metrics_display',
    )

    fieldsets = (
        ('Información del Reporte', {
            'fields': ('report_type', 'period_start', 'period_end', 'period_label', 'status')
        }),
        ('Archivo PDF', {
            'fields': ('pdf_file',)
        }),
        ('Métricas', {
            'fields': ('metrics_display',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('generated_at', 'generated_by', 'error_message'),
            'classes': ('collapse',)
        }),
    )

    def report_type_badge(self, obj):
        """Badge de color para el tipo de reporte"""
        colors = {
            'daily': '#3b82f6',    # Azul
            'weekly': '#10b981',   # Verde
            'monthly': '#7c3aed',  # Púrpura
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 0.85rem;">{}</span>',
            colors.get(obj.report_type, '#6b7280'),
            obj.get_report_type_display()
        )
    report_type_badge.short_description = 'Tipo'

    def period_display(self, obj):
        """Muestra el período del reporte"""
        return format_html(
            '<div style="line-height: 1.5;">'
            '<strong>{}</strong><br>'
            '<span style="color: #6b7280; font-size: 0.85rem;">{} - {}</span>'
            '</div>',
            obj.period_label,
            obj.period_start.strftime('%d/%m/%Y'),
            obj.period_end.strftime('%d/%m/%Y')
        )
    period_display.short_description = 'Período'

    def status_badge(self, obj):
        """Badge de color para el estado"""
        colors = {
            'pending': '#f59e0b',     # Amarillo
            'generating': '#3b82f6',  # Azul
            'completed': '#10b981',   # Verde
            'failed': '#ef4444',      # Rojo
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 0.85rem;">{}</span>',
            colors.get(obj.status, '#6b7280'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Estado'

    def metrics_summary(self, obj):
        """Resumen de métricas clave"""
        return format_html(
            '<div style="font-size: 0.9rem;">{}</div>',
            obj.get_key_metrics_summary()
        )
    metrics_summary.short_description = 'Métricas Clave'

    def pdf_download_button(self, obj):
        """Botones para ver y descargar el reporte"""
        if obj.status == 'completed':
            return format_html(
                '<a class="button" style="padding: 6px 12px; background: #7c3aed; color: white; border-radius: 6px; text-decoration: none; font-size: 0.85rem; margin-right: 5px;" '
                'href="/reports/{}/view/" target="_blank">Ver Reporte</a>'
                '<a class="button" style="padding: 6px 12px; background: #10b981; color: white; border-radius: 6px; text-decoration: none; font-size: 0.85rem;" '
                'href="/reports/{}/download/">Descargar HTML</a>',
                obj.id, obj.id
            )
        else:
            return format_html(
                '<span style="color: #6b7280; font-size: 0.85rem;">No disponible</span>'
            )
    pdf_download_button.short_description = 'Acciones'

    def metrics_display(self, obj):
        """Muestra las métricas en formato JSON legible"""
        import json
        if obj.metrics:
            return format_html(
                '<pre style="background: #f3f4f6; padding: 12px; border-radius: 6px; overflow: auto; max-height: 400px;">{}</pre>',
                json.dumps(obj.metrics, indent=2, ensure_ascii=False)
            )
        return "Sin métricas"
    metrics_display.short_description = 'Métricas JSON'

    def has_add_permission(self, request):
        """No permitir crear reportes manualmente desde el admin"""
        return False

    def get_urls(self):
        """Agregar URLs personalizadas para generar reportes"""
        urls = super().get_urls()
        custom_urls = [
            path('generate/daily/', self.admin_site.admin_view(self.generate_daily_view), name='reports_generate_daily'),
            path('generate/weekly/', self.admin_site.admin_view(self.generate_weekly_view), name='reports_generate_weekly'),
            path('generate/last7days/', self.admin_site.admin_view(self.generate_last_7_days_view), name='reports_generate_last7days'),
            path('generate/monthly/', self.admin_site.admin_view(self.generate_monthly_view), name='reports_generate_monthly'),
            path('cleanup/', self.admin_site.admin_view(self.cleanup_old_reports_view), name='reports_cleanup'),
        ]
        return custom_urls + urls

    def generate_daily_view(self, request):
        """Vista para generar reporte diario"""
        try:
            report = generate_daily_report(user=request.user)
            messages.success(request, f'Reporte diario generado exitosamente: {report.period_label}')
        except Exception as e:
            messages.error(request, f'Error al generar reporte diario: {str(e)}')
        return redirect('admin:reports_report_changelist')

    def generate_weekly_view(self, request):
        """Vista para generar reporte semanal (semana pasada: Lun-Dom)"""
        try:
            report = generate_weekly_report(user=request.user)
            messages.success(request, f'Reporte semanal generado exitosamente: {report.period_label}')
        except Exception as e:
            messages.error(request, f'Error al generar reporte semanal: {str(e)}')
        return redirect('admin:reports_report_changelist')

    def generate_last_7_days_view(self, request):
        """Vista para generar reporte de últimos 7 días"""
        try:
            from G_Jobs.reports.services.pdf_generator import generate_last_7_days_report
            report = generate_last_7_days_report(user=request.user)
            messages.success(request, f'Reporte de últimos 7 días generado exitosamente: {report.period_label}')
        except Exception as e:
            messages.error(request, f'Error al generar reporte de últimos 7 días: {str(e)}')
        return redirect('admin:reports_report_changelist')

    def generate_monthly_view(self, request):
        """Vista para generar reporte mensual"""
        try:
            report = generate_monthly_report(user=request.user)
            messages.success(request, f'Reporte mensual generado exitosamente: {report.period_label}')
        except Exception as e:
            messages.error(request, f'Error al generar reporte mensual: {str(e)}')
        return redirect('admin:reports_report_changelist')

    def cleanup_old_reports_view(self, request):
        """Vista para limpiar reportes antiguos (30+ días)"""
        from django.utils import timezone
        from datetime import timedelta

        cutoff_date = timezone.now() - timedelta(days=30)
        old_reports = Report.objects.filter(generated_at__lt=cutoff_date)
        count = old_reports.count()

        if count == 0:
            messages.info(request, 'No hay reportes antiguos para eliminar (30+ días)')
        else:
            try:
                old_reports.delete()
                messages.success(request, f'Se eliminaron {count} reportes antiguos exitosamente')
            except Exception as e:
                messages.error(request, f'Error al eliminar reportes: {str(e)}')

        return redirect('admin:reports_report_changelist')

    def changelist_view(self, request, extra_context=None):
        """Agregar contexto extra para botones de generación"""
        extra_context = extra_context or {}
        extra_context['show_generate_buttons'] = True
        return super().changelist_view(request, extra_context=extra_context)
