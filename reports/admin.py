from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse
from .models import DailyReport
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
        'new_jobs', 'active_jobs', 'closed_jobs', 'total_views',
        'plans_sold', 'plan_estandar_count', 'plan_purpura_count', 'plan_impulso_count',
        'total_revenue', 'revenue_estandar', 'revenue_purpura', 'revenue_impulso',
        'created_at', 'updated_at',
    )

    fieldsets = (
        ('Fecha', {'fields': ('date',)}),
        ('Usuarios', {
            'fields': ('new_users', 'new_companies', 'new_applicants', 'total_active_users'),
            'classes': ('wide',)
        }),
        ('Trabajos', {
            'fields': ('new_jobs', 'active_jobs', 'closed_jobs', 'total_views'),
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
