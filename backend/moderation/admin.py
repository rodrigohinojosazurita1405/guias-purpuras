from django.contrib import admin
from django.utils.html import format_html
from .models import BlockedUser


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    """Admin para gestionar usuarios bloqueados"""

    list_display = (
        'company_display',
        'blocked_user_display',
        'reason_badge',
        'blocked_at_display',
        'duration_display'
    )

    list_filter = (
        'reason',
        'blocked_at',
    )

    search_fields = (
        'company__email',
        'blocked_user__email',
        'blocked_user__first_name',
        'blocked_user__last_name',
    )

    readonly_fields = (
        'blocked_at',
        'blocked_user_info_display',
    )

    fieldsets = (
        ('Empresa y Usuario', {
            'fields': ('company', 'blocked_user', 'blocked_user_info_display')
        }),
        ('Motivo del Bloqueo', {
            'fields': ('reason', 'notes')
        }),
        ('Información de Bloqueo', {
            'fields': ('blocked_at',)
        }),
    )

    def company_display(self, obj):
        """Muestra la empresa que bloquea"""
        return obj.company.email
    company_display.short_description = 'Empresa'

    def blocked_user_display(self, obj):
        """Muestra el usuario bloqueado"""
        name = f"{obj.blocked_user.first_name} {obj.blocked_user.last_name}".strip()
        if not name:
            name = obj.blocked_user.email
        return name
    blocked_user_display.short_description = 'Usuario Bloqueado'

    def reason_badge(self, obj):
        """Badge del motivo del bloqueo con colores tenues"""
        reason_styles = {
            'spam': {'bg': '#FEE2E2', 'color': '#991B1B'},           # Rojo tenue
            'inappropriate': {'bg': '#FEE2E2', 'color': '#991B1B'},  # Rojo tenue
            'unqualified': {'bg': '#FEF3C7', 'color': '#92400E'},    # Amarillo tenue
            'other': {'bg': '#E5E7EB', 'color': '#374151'},          # Gris tenue
        }
        reason_labels = {
            'spam': 'Spam',
            'inappropriate': 'Inapropiado',
            'unqualified': 'No Calificado',
            'other': 'Otro',
        }
        style = reason_styles.get(obj.reason, reason_styles['other'])
        label = reason_labels.get(obj.reason, obj.reason)

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 10px; '
            'border-radius: 6px; font-weight: 600; font-size: 11px; '
            'display: inline-block;">{}</span>',
            style['bg'], style['color'], label
        )
    reason_badge.short_description = 'Razón'

    def blocked_at_display(self, obj):
        """Muestra la fecha de bloqueo"""
        return obj.blocked_at.strftime('%d/%m/%Y %H:%M')
    blocked_at_display.short_description = 'Bloqueado el'

    def duration_display(self, obj):
        """Muestra que el bloqueo es permanente"""
        return format_html(
            '<span style="color: #DC2626; font-weight: bold;">∞ Permanente</span>'
        )
    duration_display.short_description = 'Duración'

    def blocked_user_info_display(self, obj):
        """Muestra información completa del usuario bloqueado"""
        html_content = (
            '<div style="background-color: #F3F4F6; padding: 12px; border-radius: 8px; '
            'font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto; font-size: 13px;">'
        )

        # Email
        html_content += (
            '<p style="margin: 0 0 8px 0; display: flex; align-items: center;">'
            '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">✉️</span>'
            f'<span style="color: #374151;">{obj.blocked_user.email}</span>'
            '</p>'
        )

        # Nombre completo
        if obj.blocked_user.first_name or obj.blocked_user.last_name:
            full_name = f"{obj.blocked_user.first_name} {obj.blocked_user.last_name}".strip()
            html_content += (
                '<p style="margin: 0 0 8px 0; display: flex; align-items: center;">'
                '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">👤</span>'
                f'<span style="color: #374151;">{full_name}</span>'
                '</p>'
            )

        # Role
        html_content += (
            '<p style="margin: 0; display: flex; align-items: center;">'
            '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">🔖</span>'
            f'<span style="color: #374151;">{obj.blocked_user.role}</span>'
            '</p>'
        )

        html_content += '</div>'
        return format_html(html_content)
    blocked_user_info_display.short_description = 'Información del Usuario'
