"""
Admin personalizado para gestión de Tokens JWT con interfaz visual.
Permite a administradores sin conocimientos técnicos gestionar la blacklist.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from io import StringIO
from django.core.management import call_command


class TokenBlacklistAdminSite(admin.ModelAdmin):
    """
    Admin personalizado para BlacklistedToken con botones de limpieza automática
    """

    list_display = (
        'token_jti_display',
        'token_user_display',
        'token_status',
        'token_created_display',
        'token_expires_display',
        'blacklisted_at_display',
    )

    search_fields = (
        'token__user__email',
        'token__jti',
    )

    list_filter = (
        'blacklisted_at',
    )

    ordering = ('-blacklisted_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('token__user')

    def token_jti_display(self, obj):
        """Muestra JTI abreviado"""
        jti = obj.token.jti
        return format_html(
            '<code style="background-color: #F3F4F6; padding: 4px 8px; '
            'border-radius: 4px; font-size: 11px;">{}</code>',
            jti[:12] + '...' if len(jti) > 12 else jti
        )
    token_jti_display.short_description = 'Token JTI'

    def token_user_display(self, obj):
        """Muestra usuario del token"""
        user = obj.token.user
        if user:
            return format_html(
                '<span style="font-weight: 600;">{}</span><br>'
                '<span style="font-size: 11px; color: #6B7280;">{}</span>',
                user.email,
                user.get_role_display() if hasattr(user, 'get_role_display') else 'Usuario'
            )
        return '—'
    token_user_display.short_description = 'Usuario'

    def token_status(self, obj):
        """Muestra si el token está expirado o activo"""
        now = timezone.now()
        if obj.token.expires_at < now:
            return format_html(
                '<span style="background-color: #F3F4F6; color: #6B7280; padding: 4px 10px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px; '
                'display: inline-block;">⏰ Expirado</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #FEE2E2; color: #DC2626; padding: 4px 10px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px; '
                'display: inline-block;">🚫 Revocado (Activo)</span>'
            )
    token_status.short_description = 'Estado'

    def token_created_display(self, obj):
        """Fecha de creación del token"""
        if obj.token.created_at:
            return obj.token.created_at.strftime('%d/%m/%Y %H:%M')
        return '—'
    token_created_display.short_description = 'Creado'

    def token_expires_display(self, obj):
        """Fecha de expiración del token"""
        return obj.token.expires_at.strftime('%d/%m/%Y %H:%M')
    token_expires_display.short_description = 'Expira'

    def blacklisted_at_display(self, obj):
        """Fecha en que fue blacklisted"""
        return obj.blacklisted_at.strftime('%d/%m/%Y %H:%M')
    blacklisted_at_display.short_description = 'Revocado el'

    # Read-only
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return request.method in ["GET", "HEAD"]

    # URLs personalizadas
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'clean-tokens/',
                self.admin_site.admin_view(self.clean_tokens_view),
                name='clean_tokens',
            ),
        ]
        return custom_urls + urls

    def clean_tokens_view(self, request):
        """Vista personalizada para limpiar tokens"""
        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'dry_run':
                # Simular limpieza sin borrar
                now = timezone.now()
                expired_outstanding = OutstandingToken.objects.filter(expires_at__lt=now).count()
                expired_blacklisted = BlacklistedToken.objects.filter(token__expires_at__lt=now).count()

                messages.info(
                    request,
                    f'SIMULACIÓN: Se eliminarían {expired_outstanding} Outstanding Tokens '
                    f'y {expired_blacklisted} Blacklisted Tokens expirados.'
                )

            elif action == 'clean':
                # Ejecutar limpieza real
                out = StringIO()
                call_command('clean_blacklist', stdout=out, verbosity=1)
                output = out.getvalue()

                messages.success(
                    request,
                    'Limpieza ejecutada exitosamente. Ver detalles en la consola del servidor.'
                )

            elif action == 'clean_verbose':
                # Ejecutar limpieza con detalles
                out = StringIO()
                call_command('clean_blacklist', '--verbose', stdout=out, verbosity=2)
                output = out.getvalue()

                messages.success(
                    request,
                    'Limpieza detallada ejecutada. Ver detalles en la consola del servidor.'
                )

            return redirect('..')

        # GET request - mostrar estadísticas
        now = timezone.now()

        total_outstanding = OutstandingToken.objects.count()
        total_blacklisted = BlacklistedToken.objects.count()
        expired_outstanding = OutstandingToken.objects.filter(expires_at__lt=now).count()
        expired_blacklisted = BlacklistedToken.objects.filter(token__expires_at__lt=now).count()
        active_blacklisted = total_blacklisted - expired_blacklisted

        context = {
            **self.admin_site.each_context(request),
            'title': 'Gestión de Tokens JWT',
            'stats': {
                'total_outstanding': total_outstanding,
                'total_blacklisted': total_blacklisted,
                'expired_outstanding': expired_outstanding,
                'expired_blacklisted': expired_blacklisted,
                'active_blacklisted': active_blacklisted,
            },
            'opts': self.model._meta,
        }

        return render(request, 'admin/token_cleanup.html', context)

    # Agregar botón en el changelist
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Estadísticas rápidas
        now = timezone.now()
        total_blacklisted = BlacklistedToken.objects.count()
        expired_blacklisted = BlacklistedToken.objects.filter(token__expires_at__lt=now).count()

        extra_context['total_blacklisted'] = total_blacklisted
        extra_context['expired_blacklisted'] = expired_blacklisted
        extra_context['cleanup_needed'] = expired_blacklisted > 50

        return super().changelist_view(request, extra_context=extra_context)


class OutstandingTokenAdminCustom(admin.ModelAdmin):
    """Admin personalizado para OutstandingToken con estadísticas"""

    list_display = (
        'jti_display',
        'user_display',
        'token_status',
        'created_at_display',
        'expires_at_display',
    )

    search_fields = (
        'user__email',
        'jti',
    )

    list_filter = (
        'created_at',
        'expires_at',
    )

    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')

    def jti_display(self, obj):
        """Muestra JTI abreviado"""
        return format_html(
            '<code style="background-color: #F3F4F6; padding: 4px 8px; '
            'border-radius: 4px; font-size: 11px;">{}</code>',
            obj.jti[:12] + '...' if len(obj.jti) > 12 else obj.jti
        )
    jti_display.short_description = 'JTI'

    def user_display(self, obj):
        """Muestra usuario del token"""
        if obj.user:
            return format_html(
                '<span style="font-weight: 600;">{}</span><br>'
                '<span style="font-size: 11px; color: #6B7280;">{}</span>',
                obj.user.email,
                obj.user.get_role_display() if hasattr(obj.user, 'get_role_display') else 'Usuario'
            )
        return '—'
    user_display.short_description = 'Usuario'

    def token_status(self, obj):
        """Muestra si el token está expirado o activo"""
        now = timezone.now()
        if obj.expires_at < now:
            return format_html(
                '<span style="background-color: #F3F4F6; color: #6B7280; padding: 4px 10px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px; '
                'display: inline-block;">⏰ Expirado</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ECFDF5; color: #059669; padding: 4px 10px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px; '
                'display: inline-block;">✓ Activo</span>'
            )
    token_status.short_description = 'Estado'

    def created_at_display(self, obj):
        """Fecha de creación"""
        if obj.created_at:
            return obj.created_at.strftime('%d/%m/%Y %H:%M')
        return '—'
    created_at_display.short_description = 'Creado'

    def expires_at_display(self, obj):
        """Fecha de expiración"""
        return obj.expires_at.strftime('%d/%m/%Y %H:%M')
    expires_at_display.short_description = 'Expira'

    # Read-only
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return request.method in ["GET", "HEAD"]


# Desregistrar los admins por defecto y registrar los personalizados
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)

admin.site.register(BlacklistedToken, TokenBlacklistAdminSite)
admin.site.register(OutstandingToken, OutstandingTokenAdminCustom)
