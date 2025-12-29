"""
Admin interface para el sistema de notificaciones
"""
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from datetime import timedelta
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Interfaz de administracion para Notificaciones
    """
    list_display = [
        'id_short',
        'user_email',
        'notification_type',
        'title',
        'status_badge',
        'created_at',
        'dismissed_badge'
    ]

    list_filter = [
        'notification_type',
        'is_read',
        'is_dismissed',
        'created_at',
    ]

    search_fields = [
        'user__email',
        'title',
        'message',
    ]

    readonly_fields = [
        'id',
        'created_at',
        'read_at',
        'dismissed_at',
    ]

    fieldsets = (
        ('Informacion basica', {
            'fields': ('id', 'user', 'notification_type', 'title', 'message', 'metadata')
        }),
        ('Estado', {
            'fields': ('is_read', 'read_at', 'is_dismissed', 'dismissed_at')
        }),
        ('Fechas', {
            'fields': ('created_at',)
        }),
    )

    actions = [
        'mark_as_read',
        'mark_as_dismissed',
        'cleanup_old_dismissed',
        'cleanup_very_old_dismissed',
    ]

    def id_short(self, obj):
        """Mostrar ID corto"""
        return str(obj.id)[:8]
    id_short.short_description = 'ID'

    def user_email(self, obj):
        """Mostrar email del usuario"""
        return obj.user.email
    user_email.short_description = 'Usuario'
    user_email.admin_order_field = 'user__email'

    def status_badge(self, obj):
        """Badge de estado leido/no leido"""
        if obj.is_read:
            return format_html(
                '<span style="background: #10b981; color: white; padding: 3px 8px; '
                'border-radius: 4px; font-size: 11px;">Leida</span>'
            )
        else:
            return format_html(
                '<span style="background: #ef4444; color: white; padding: 3px 8px; '
                'border-radius: 4px; font-size: 11px;">No leida</span>'
            )
    status_badge.short_description = 'Estado'

    def dismissed_badge(self, obj):
        """Badge de descartada"""
        if obj.is_dismissed:
            return format_html(
                '<span style="background: #6b7280; color: white; padding: 3px 8px; '
                'border-radius: 4px; font-size: 11px;">Archivada</span>'
            )
        else:
            return format_html(
                '<span style="background: #3b82f6; color: white; padding: 3px 8px; '
                'border-radius: 4px; font-size: 11px;">Activa</span>'
            )
    dismissed_badge.short_description = 'Visibilidad'

    # ========== ACCIONES ==========

    @admin.action(description='Marcar como leidas')
    def mark_as_read(self, request, queryset):
        """Marcar notificaciones seleccionadas como leidas"""
        count = 0
        for notification in queryset:
            if not notification.is_read:
                notification.mark_as_read()
                count += 1

        self.message_user(
            request,
            f'{count} notificaciones marcadas como leidas'
        )

    @admin.action(description='Descartar/archivar notificaciones')
    def mark_as_dismissed(self, request, queryset):
        """Descartar notificaciones seleccionadas"""
        count = 0
        for notification in queryset:
            if not notification.is_dismissed:
                notification.dismiss()
                count += 1

        self.message_user(
            request,
            f'{count} notificaciones descartadas'
        )

    @admin.action(description='Limpiar descartadas +30 dias')
    def cleanup_old_dismissed(self, request, queryset):
        """Eliminar notificaciones descartadas de mas de 30 dias"""
        cutoff_date = timezone.now() - timedelta(days=30)

        old_notifications = Notification.objects.filter(
            is_dismissed=True,
            dismissed_at__lt=cutoff_date
        )

        count = old_notifications.count()
        old_notifications.delete()

        self.message_user(
            request,
            f'Se eliminaron {count} notificaciones descartadas de hace mas de 30 dias',
            level='success' if count > 0 else 'info'
        )

    @admin.action(description='Limpiar descartadas +90 dias')
    def cleanup_very_old_dismissed(self, request, queryset):
        """Eliminar notificaciones descartadas de mas de 90 dias"""
        cutoff_date = timezone.now() - timedelta(days=90)

        old_notifications = Notification.objects.filter(
            is_dismissed=True,
            dismissed_at__lt=cutoff_date
        )

        count = old_notifications.count()
        old_notifications.delete()

        self.message_user(
            request,
            f'Se eliminaron {count} notificaciones descartadas de hace mas de 90 dias',
            level='success' if count > 0 else 'info'
        )

    def get_queryset(self, request):
        """Optimizar queries"""
        qs = super().get_queryset(request)
        return qs.select_related('user')
