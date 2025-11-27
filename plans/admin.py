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
        # Ocultar el campo features ya que se genera automáticamente
        if 'features' in self.fields:
            self.fields['features'].widget = forms.HiddenInput()
            self.fields['features'].required = False


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
    )

    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'label', 'description', 'badge_label')
        }),
        ('Pricing', {
            'fields': ('price', 'currency')
        }),
        ('Validez del Anuncio', {
            'fields': ('duration_days',),
            'description': 'Duración en días que el anuncio permanecerá activo'
        }),
        ('📊 Características del Plan', {
            'fields': (
                'max_announcements',
                'is_featured',
                'featured_days',
                'has_highlighted_results',
                'announcement_substitutions',
            ),
            'classes': ('wide',),
            'description': 'Edita las características principales del plan. Todos los cambios se reflejarán automáticamente en el frontend.'
        }),
        ('📱 Difusión en Redes Sociales', {
            'fields': (
                'facebook_posts',
                'linkedin_posts',
                'tiktok_posts',
            ),
            'classes': ('wide',),
            'description': 'Configura cuántos posts se permiten en cada red social.'
        }),
        ('🔍 Vista Previa (Solo Lectura)', {
            'fields': (
                'features_preview',
            ),
            'classes': ('wide',),
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

    def features_preview(self, obj):
        """Vista previa auto-generada del JSON de características"""
        import json
        if not obj.features:
            return format_html(
                '<div style="background-color: #ECFDF5; padding: 12px; border-radius: 6px; '
                'border-left: 4px solid #059669; color: #065F46;"><strong>✓ Auto-generado (campos por defecto)</strong></div>'
            )

        try:
            features_json = json.dumps(obj.features, indent=2, ensure_ascii=False)
            preview_html = f'''
            <div style="background-color: #ECFDF5; padding: 12px; border-radius: 6px; border-left: 4px solid #059669;">
                <p style="margin: 0 0 8px 0; color: #065F46; font-weight: bold;">✓ JSON Auto-generado desde los campos</p>
                <pre style="background-color: #F0FDF4; padding: 8px; border-radius: 4px;
                overflow-x: auto; font-family: monospace; font-size: 11px; margin: 0; color: #166534;">{features_json}</pre>
            </div>
            '''
            return format_html(preview_html)
        except Exception as e:
            return f'Error al procesar características: {str(e)}'

    features_preview.short_description = 'Vista Previa JSON (Auto-generado)'
