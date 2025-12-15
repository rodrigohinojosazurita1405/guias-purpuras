from django.contrib import admin
from django.utils.html import format_html
from .models import JobCategory, ContractType, City


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    """Admin para gestionar categorias de trabajo dinamicamente"""

    list_display = ('name', 'slug', 'icon', 'order', 'is_active_badge', 'jobs_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'slug')
    list_editable = ('order', )
    ordering = ('order', 'name')

    fieldsets = (
        ('Informacion Basica', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Configuracion', {
            'fields': ('is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #10B981; color: white; padding: 4px 12px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px;">ACTIVA</span>'
            )
        return format_html(
            '<span style="background-color: #DC2626; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: bold; font-size: 11px;">INACTIVA</span>'
        )
    is_active_badge.short_description = 'Estado'

    def jobs_count(self, obj):
        from jobs.models import Job
        count = Job.objects.filter(jobCategory=obj.name).count()
        return f"{count} trabajos"
    jobs_count.short_description = 'Trabajos Asociados'


@admin.register(ContractType)
class ContractTypeAdmin(admin.ModelAdmin):
    """Admin para gestionar tipos de contrato dinamicamente"""

    list_display = ('name', 'slug', 'order', 'is_active_badge', 'jobs_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'slug')
    list_editable = ('order', )
    ordering = ('order', 'name')

    fieldsets = (
        ('Informacion Basica', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Configuracion', {
            'fields': ('is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #10B981; color: white; padding: 4px 12px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px;">ACTIVO</span>'
            )
        return format_html(
            '<span style="background-color: #DC2626; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: bold; font-size: 11px;">INACTIVO</span>'
        )
    is_active_badge.short_description = 'Estado'

    def jobs_count(self, obj):
        from jobs.models import Job
        count = Job.objects.filter(contractType=obj.name).count()
        return f"{count} trabajos"
    jobs_count.short_description = 'Trabajos Asociados'


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Admin para gestionar ciudades dinamicamente"""

    list_display = ('name', 'department', 'region_badge', 'order', 'is_active_badge', 'jobs_count', 'created_at')
    list_filter = ('is_active', 'region', 'created_at')
    search_fields = ('name', 'department', 'slug')
    list_editable = ('order', )
    ordering = ('order', 'name')

    fieldsets = (
        ('Informacion Basica', {
            'fields': ('name', 'slug', 'department', 'region')
        }),
        ('Configuracion', {
            'fields': ('is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def region_badge(self, obj):
        colors = {
            'altiplano': '#3B82F6',  # Azul
            'valles': '#10B981',      # Verde
            'llanos': '#F59E0B',      # Naranja
        }
        labels = {
            'altiplano': 'ALTIPLANO',
            'valles': 'VALLES',
            'llanos': 'LLANOS',
        }
        color = colors.get(obj.region, '#6B7280')
        label = labels.get(obj.region, obj.region.upper() if obj.region else 'N/A')

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            color, label
        )
    region_badge.short_description = 'Region'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #10B981; color: white; padding: 4px 12px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px;">ACTIVA</span>'
            )
        return format_html(
            '<span style="background-color: #DC2626; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: bold; font-size: 11px;">INACTIVA</span>'
        )
    is_active_badge.short_description = 'Estado'

    def jobs_count(self, obj):
        from jobs.models import Job
        count = Job.objects.filter(city=obj.name).count()
        return f"{count} trabajos"
    jobs_count.short_description = 'Trabajos Asociados'
