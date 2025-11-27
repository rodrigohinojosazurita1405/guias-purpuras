from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Plan


class PlanForm(forms.ModelForm):
    """Formulario personalizado para editar características de forma visual"""

    class Meta:
        model = Plan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el campo features un textarea más grande
        self.fields['features'].widget = forms.Textarea(attrs={
            'rows': 8,
            'cols': 60,
            'style': 'font-family: monospace; font-size: 12px;'
        })


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Admin personalizado para gestionar planes de publicación"""

    form = PlanForm

    list_display = (
        'plan_name_display',
        'actual_price_display',
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
        'features_help_text',
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
        ('Características del Plan', {
            'fields': ('features', 'features_help_text', 'features_preview'),
            'classes': ('wide',),
            'description': 'Edita las características en formato JSON. Ver ayuda abajo para valores válidos.'
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

    def actual_price_display(self, obj):
        """Muestra el precio actual de la BD con formato"""
        return format_html(
            '<span style="background-color: #ECFDF5; color: #065F46; padding: 6px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 13px; '
            'display: inline-block;">💰 {} {}</span>',
            obj.price, obj.currency
        )
    actual_price_display.short_description = 'Precio (BD)'

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

    def features_help_text(self, obj):
        """Muestra ayuda sobre qué características se pueden editar"""
        help_html = '''
        <div style="background-color: #F0F9FF; padding: 16px; border-radius: 8px; border-left: 4px solid #3B82F6;">
            <h4 style="margin-top: 0; color: #1E40AF;">Características Disponibles (JSON):</h4>
            <p style="margin: 8px 0; font-size: 13px; color: #374151;">
                <strong>maxAnnouncements</strong>: Número máximo de anuncios (ej: 1, 3)<br>
                <strong>maxEditions</strong>: Ediciones permitidas (ej: 999 = sin límite)<br>
                <strong>applicationForm</strong>: "standard" o "custom" (tipo de formulario)<br>
                <strong>featured</strong>: true/false (anuncio destacado)<br>
                <strong>highlightedResults</strong>: true/false (resultados destacados)<br>
                <strong>premiumBadge</strong>: true/false (mostrar badge premium)<br>
                <strong>socialMediaShare</strong>: true/false (permitir compartir en redes)
            </p>
            <p style="margin: 8px 0; font-size: 12px; color: #6B7280; font-style: italic;">
                💡 Estos valores se mostrarán automáticamente en el frontend y tabla de comparación
            </p>
        </div>
        '''
        return format_html(help_html)

    features_help_text.short_description = 'Guía de Características'

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

    features_preview.short_description = 'Vista Previa (Lectura)'
