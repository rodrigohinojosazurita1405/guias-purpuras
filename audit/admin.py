from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import AuditLog, AuditLogSummary
import json


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Admin personalizado para visualizar logs de auditoría con filtros avanzados
    """
    list_display = (
        'timestamp_display',
        'user_email_display',
        'action_badge',
        'severity_badge',
        'object_display',
        'ip_address_display',
    )

    list_filter = (
        'action',
        'severity',
        'content_type',
        'timestamp',
        'user_role',
    )

    search_fields = (
        'user_email',
        'object_repr',
        'action_description',
        'ip_address',
        'object_id',
    )

    readonly_fields = (
        'user',
        'user_email',
        'user_role',
        'content_type',
        'object_id',
        'content_object',
        'object_repr',
        'action',
        'action_description',
        'changes_display',
        'ip_address',
        'user_agent',
        'session_key',
        'timestamp',
        'severity',
    )

    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'user_email', 'user_role')
        }),
        ('Objeto Auditado', {
            'fields': ('content_type', 'object_id', 'object_repr')
        }),
        ('Acción Realizada', {
            'fields': ('action', 'action_description', 'changes_display', 'severity')
        }),
        ('Metadatos', {
            'fields': ('ip_address', 'user_agent', 'session_key', 'timestamp'),
            'classes': ('collapse',)
        }),
    )

    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        """No permitir crear registros manualmente"""
        return False

    def has_change_permission(self, request, obj=None):
        """No permitir editar registros (solo lectura)"""
        return False

    def timestamp_display(self, obj):
        """Mostrar timestamp formateado"""
        return obj.timestamp.strftime('%d/%m/%Y %H:%M:%S')
    timestamp_display.short_description = 'Fecha y Hora'
    timestamp_display.admin_order_field = 'timestamp'

    def user_email_display(self, obj):
        """Mostrar email del usuario con badge de rol"""
        role_colors = {
            'company': '#7c3aed',
            'applicant': '#3b82f6',
            '': '#6b7280',
        }
        role_labels = {
            'company': 'Empresa',
            'applicant': 'Postulante',
            '': 'Sistema',
        }
        color = role_colors.get(obj.user_role, '#6b7280')
        label = role_labels.get(obj.user_role, obj.user_role)

        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<strong>{}</strong>'
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">{}</span>'
            '</div>',
            obj.user_email,
            color,
            label
        )
    user_email_display.short_description = 'Usuario'

    def action_badge(self, obj):
        """Badge colorido para la acción"""
        colors = {
            'create': ('#10b981', '#d1fae5'),
            'update': ('#3b82f6', '#dbeafe'),
            'delete': ('#ef4444', '#fee2e2'),
            'soft_delete': ('#f59e0b', '#fef3c7'),
            'restore': ('#8b5cf6', '#ede9fe'),
            'pause': ('#f59e0b', '#fef3c7'),
            'activate': ('#10b981', '#d1fae5'),
            'close': ('#6b7280', '#f3f4f6'),
            'verify_payment': ('#10b981', '#d1fae5'),
            'reject_payment': ('#ef4444', '#fee2e2'),
            'duplicate': ('#3b82f6', '#dbeafe'),
            'view': ('#6b7280', '#f3f4f6'),
            'export': ('#7c3aed', '#ede9fe'),
            'other': ('#6b7280', '#f3f4f6'),
        }

        border_color, bg_color = colors.get(obj.action, ('#6b7280', '#f3f4f6'))

        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 12px; border-radius: 16px; font-size: 0.85rem; font-weight: 600; border: 2px solid {};">'
            '{}</span>',
            bg_color,
            border_color,
            border_color,
            obj.get_action_display()
        )
    action_badge.short_description = 'Acción'
    action_badge.admin_order_field = 'action'

    def severity_badge(self, obj):
        """Badge de severidad"""
        colors = {
            'info': ('#3b82f6', '#dbeafe'),
            'warning': ('#f59e0b', '#fef3c7'),
            'critical': ('#ef4444', '#fee2e2'),
        }

        border_color, bg_color = colors.get(obj.severity, ('#6b7280', '#f3f4f6'))

        icons = {
            'info': '&#9432;',  # ℹ
            'warning': '&#9888;',  # ⚠
            'critical': '&#10071;',  # ❗
        }

        return format_html(
            '<span style="background: {}; color: {}; padding: 4px 10px; border-radius: 16px; font-size: 0.8rem; font-weight: 600; border: 2px solid {};">'
            '{} {}</span>',
            bg_color,
            border_color,
            border_color,
            mark_safe(icons.get(obj.severity, '')),
            obj.get_severity_display()
        )
    severity_badge.short_description = 'Severidad'
    severity_badge.admin_order_field = 'severity'

    def object_display(self, obj):
        """Mostrar objeto modificado con tipo"""
        return format_html(
            '<div style="font-size: 0.9rem;">'
            '<strong style="color: #7c3aed;">{}</strong><br>'
            '<span style="color: #6b7280; font-size: 0.85rem;">ID: {}</span>'
            '</div>',
            obj.object_repr[:50],
            obj.object_id
        )
    object_display.short_description = 'Objeto'

    def ip_address_display(self, obj):
        """Mostrar IP con ícono"""
        if obj.ip_address:
            return format_html(
                '<code style="background: #f3f4f6; padding: 4px 8px; border-radius: 4px; font-size: 0.85rem;">{}</code>',
                obj.ip_address
            )
        return format_html('<span style="color: #9ca3af;">—</span>')
    ip_address_display.short_description = 'IP'

    def changes_display(self, obj):
        """Mostrar cambios formateados con colores"""
        if not obj.changes:
            return format_html('<span style="color: #9ca3af;">Sin cambios específicos</span>')

        html = '<div style="font-family: monospace; background: #f9fafb; padding: 12px; border-radius: 6px; border: 1px solid #e5e7eb;">'

        for field, change_data in obj.changes.items():
            if isinstance(change_data, dict) and 'old' in change_data and 'new' in change_data:
                old_val = change_data['old']
                new_val = change_data['new']

                html += f'''
                <div style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #e5e7eb;">
                    <strong style="color: #7c3aed;">{field}:</strong><br>
                    <span style="color: #ef4444; background: #fee2e2; padding: 2px 6px; border-radius: 4px; text-decoration: line-through;">
                        {old_val}
                    </span>
                    <span style="color: #6b7280; margin: 0 8px;">→</span>
                    <span style="color: #10b981; background: #d1fae5; padding: 2px 6px; border-radius: 4px;">
                        {new_val}
                    </span>
                </div>
                '''
            else:
                html += f'''
                <div style="margin-bottom: 8px;">
                    <strong style="color: #7c3aed;">{field}:</strong>
                    <span style="color: #374151;">{change_data}</span>
                </div>
                '''

        html += '</div>'

        return mark_safe(html)
    changes_display.short_description = 'Cambios Detallados'


@admin.register(AuditLogSummary)
class AuditLogSummaryAdmin(admin.ModelAdmin):
    """
    Admin para visualizar resúmenes diarios de auditoría
    """
    list_display = (
        'date',
        'total_actions_display',
        'creates_display',
        'updates_display',
        'deletes_display',
        'unique_users',
        'critical_events_display',
    )

    list_filter = ('date',)

    readonly_fields = (
        'date',
        'total_actions',
        'total_creates',
        'total_updates',
        'total_deletes',
        'unique_users',
        'critical_events',
        'created_at',
    )

    date_hierarchy = 'date'

    def has_add_permission(self, request):
        """No permitir crear manualmente"""
        return False

    def total_actions_display(self, obj):
        return format_html(
            '<strong style="color: #7c3aed; font-size: 1.1rem;">{}</strong>',
            obj.total_actions
        )
    total_actions_display.short_description = 'Total Acciones'
    total_actions_display.admin_order_field = 'total_actions'

    def creates_display(self, obj):
        return format_html(
            '<span style="background: #d1fae5; color: #065f46; padding: 4px 12px; border-radius: 12px; font-weight: 600;">'
            '+ {}</span>',
            obj.total_creates
        )
    creates_display.short_description = 'Creaciones'

    def updates_display(self, obj):
        return format_html(
            '<span style="background: #dbeafe; color: #1e3a8a; padding: 4px 12px; border-radius: 12px; font-weight: 600;">'
            '✎ {}</span>',
            obj.total_updates
        )
    updates_display.short_description = 'Actualizaciones'

    def deletes_display(self, obj):
        return format_html(
            '<span style="background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 12px; font-weight: 600;">'
            '✕ {}</span>',
            obj.total_deletes
        )
    deletes_display.short_description = 'Eliminaciones'

    def critical_events_display(self, obj):
        if obj.critical_events > 0:
            return format_html(
                '<span style="background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 12px; font-weight: 700;">'
                '❗ {}</span>',
                obj.critical_events
            )
        return format_html('<span style="color: #9ca3af;">—</span>')
    critical_events_display.short_description = 'Críticos'
