from django.contrib import admin
from django.utils.html import format_html
from .models import PlanOrder


@admin.register(PlanOrder)
class PlanOrderAdmin(admin.ModelAdmin):
    """Admin para gestionar órdenes de planes"""

    list_display = (
        'order_id_display',
        'razon_social_display',
        'plan_display',
        'amount_display',
        'status_badge',
        'order_date_display',
        'user_email'
    )

    list_filter = (
        'status',
        'created_at',
        'selected_plan',
    )

    search_fields = (
        'razon_social',
        'nit',
        'ci',
        'user__email',
        'email',
    )

    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Información General', {
            'fields': ('id', 'user', 'job', 'selected_plan', 'plan_price', 'status')
        }),
        ('Datos de Factura', {
            'fields': ('razon_social', 'nit', 'ci', 'ci_complement')
        }),
        ('Contacto', {
            'fields': ('email', 'whatsapp')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def order_id_display(self, obj):
        """Muestra el ID de orden"""
        return f"#{obj.id}"
    order_id_display.short_description = 'N.º Orden'

    def razon_social_display(self, obj):
        """Muestra la razón social de la empresa"""
        return obj.razon_social
    razon_social_display.short_description = 'Razón Social'

    def plan_display(self, obj):
        """Muestra el plan seleccionado"""
        return obj.selected_plan.capitalize()
    plan_display.short_description = 'Plan'

    def amount_display(self, obj):
        """Muestra el precio del plan formateado"""
        return format_html(
            '<span style="color: #7C3AED; font-weight: bold;">Bs {}</span>',
            f'{obj.plan_price:.2f}'
        )
    amount_display.short_description = 'Monto'

    def status_badge(self, obj):
        """Badge del estado de la orden con colores tenues"""
        status_styles = {
            'processing': {'bg': '#FEF3C7', 'color': '#92400E'},  # Amarillo tenue
            'completed': {'bg': '#D1FAE5', 'color': '#065F46'},   # Verde tenue
        }
        status_labels = {
            'processing': 'En Proceso',
            'completed': 'Completado',
        }
        style = status_styles.get(obj.status, {'bg': '#E5E7EB', 'color': '#374151'})
        label = status_labels.get(obj.status, obj.get_status_display())

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 10px; '
            'border-radius: 6px; font-weight: 600; font-size: 11px; '
            'display: inline-block;">{}</span>',
            style['bg'], style['color'], label
        )
    status_badge.short_description = 'Estado'

    def order_date_display(self, obj):
        """Muestra la fecha de la orden"""
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    order_date_display.short_description = 'Fecha'

    def user_email(self, obj):
        """Muestra el email del usuario"""
        return obj.user.email
    user_email.short_description = 'Usuario'
