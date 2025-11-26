from django.contrib import admin
from django.utils.html import format_html
from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Admin personalizado para gestionar planes de publicación"""

    list_display = (
        'plan_name_display',
        'price_display',
        'duration_display',
        'status_badge',
        'order'
    )

    list_filter = (
        'is_active',
        'created_at',
    )

    search_fields = ('name', 'label', 'description')

    readonly_fields = (
        'created_at',
        'updated_at',
        'features_preview',
    )

    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'label', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'currency')
        }),
        ('Validez del Anuncio', {
            'fields': ('duration_days',),
            'description': 'Duración en días que el anuncio permanecerá activo'
        }),
        ('Características', {
            'fields': ('features', 'features_preview'),
            'classes': ('wide',),
            'description': 'Define las características y límites de este plan en formato JSON'
        }),
        ('Visualización', {
            'fields': ('order', 'is_active'),
            'description': 'Orden para mostrar en UI y estado de disponibilidad'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def plan_name_display(self, obj):
        """Muestra el nombre del plan"""
        return obj.label
    plan_name_display.short_description = 'Plan'

    def price_display(self, obj):
        """Muestra el precio con formato"""
        return format_html(
            '<span style="background-color: #ECFDF5; color: #065F46; padding: 6px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 13px; '
            'display: inline-block;">💰 {} {}</span>',
            obj.price, obj.currency
        )
    price_display.short_description = 'Precio'

    def duration_display(self, obj):
        """Muestra la duración en días"""
        return format_html(
            '<span style="background-color: #DBEAFE; color: #1E40AF; padding: 6px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 13px; '
            'display: inline-block;">📅 {} días</span>',
            obj.duration_days
        )
    duration_display.short_description = 'Duración'

    def status_badge(self, obj):
        """Badge de estado del plan"""
        if obj.is_active:
            color = '#059669'  # Verde
            label = '✓ ACTIVO'
        else:
            color = '#6B7280'  # Gris
            label = '✗ INACTIVO'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 6px 14px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Estado'

    def features_preview(self, obj):
        """Preview de las características en formato JSON"""
        import json
        if not obj.features:
            return format_html(
                '<div style="background-color: #FEE2E2; padding: 12px; border-radius: 6px; '
                'text-align: center; color: #991B1B;"><strong>Sin características configuradas</strong></div>'
            )

        try:
            features_json = json.dumps(obj.features, indent=2, ensure_ascii=False)
            return format_html(
                '<pre style="background-color: #F3F4F6; padding: 12px; border-radius: 6px; '
                'overflow-x: auto; font-family: monospace; font-size: 12px;">{}</pre>',
                features_json
            )
        except:
            return 'Error al procesar características'

    features_preview.short_description = 'Vista Previa de Características'
