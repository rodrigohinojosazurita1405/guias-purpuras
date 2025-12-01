from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin personalizado para CustomUser"""

    # Campos mostrados en la lista
    list_display = (
        'email_display',
        'role_badge',
        'status_indicators',
        'last_login_display'
    )

    # Filtros disponibles
    list_filter = (
        'role',
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined',
        'last_login',
    )

    # Búsqueda
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'username',
    )

    # Campos de solo lectura
    readonly_fields = (
        'id',
        'date_joined',
        'last_login',
    )

    # Organización de campos por secciones
    fieldsets = (
        ('Información Personal', {
            'fields': ('id', 'email', 'username', 'first_name', 'last_name')
        }),
        ('Role y Permisos', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Contraseña', {
            'fields': ('password',),
            'classes': ('collapse',)
        }),
        ('Fechas Importantes', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )

    # Acciones personalizadas
    actions = [
        'make_staff',
        'remove_staff',
        'make_superuser',
        'remove_superuser',
        'activate_users',
        'deactivate_users',
    ]

    def email_display(self, obj):
        """Muestra el email con icono"""
        return format_html(
            '<span style="font-weight: 600;">✉️ {}</span>',
            obj.email
        )
    email_display.short_description = 'Email'

    def role_badge(self, obj):
        """Badge del role del usuario"""
        role_colors = {
            'company': {'color': '#3B82F6', 'bg': '#DBEAFE', 'label': '🏢 Empresa'},
            'applicant': {'color': '#10B981', 'bg': '#ECFDF5', 'label': '👤 Postulante'},
        }
        role_info = role_colors.get(obj.role, {'color': '#6B7280', 'bg': '#F3F4F6', 'label': '❓ ' + obj.role.upper()})

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 6px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block;">{}</span>',
            role_info['bg'], role_info['color'], role_info['label']
        )
    role_badge.short_description = 'Role'

    def status_indicators(self, obj):
        """Muestra indicadores de estado (staff, superuser, activo)"""
        indicators = []

        if obj.is_superuser:
            indicators.append(
                '<span style="background-color: #FEE2E2; color: #DC2626; padding: 4px 8px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px; margin-right: 4px; '
                'display: inline-block;">👑 Superuser</span>'
            )
        if obj.is_staff:
            indicators.append(
                '<span style="background-color: #FEF3C7; color: #F59E0B; padding: 4px 8px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px; margin-right: 4px; '
                'display: inline-block;">⚙️ Staff</span>'
            )
        if not obj.is_active:
            indicators.append(
                '<span style="background-color: #F3F4F6; color: #6B7280; padding: 4px 8px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px; margin-right: 4px; '
                'display: inline-block;">🔒 Inactivo</span>'
            )
        else:
            indicators.append(
                '<span style="background-color: #ECFDF5; color: #059669; padding: 4px 8px; '
                'border-radius: 12px; font-weight: bold; font-size: 11px; margin-right: 4px; '
                'display: inline-block;">✓ Activo</span>'
            )

        return format_html(' '.join(indicators)) if indicators else 'Sin estado'
    status_indicators.short_description = 'Estado'

    def last_login_display(self, obj):
        """Muestra la última conexión"""
        if obj.last_login:
            return obj.last_login.strftime('%d/%m/%Y %H:%M')
        return 'Nunca ha iniciado sesión'
    last_login_display.short_description = 'Última Conexión'

    # ========== ACCIONES PERSONALIZADAS ==========

    def make_staff(self, request, queryset):
        """Convertir usuarios en staff"""
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} usuario(s) ahora tienen permisos de STAFF')
    make_staff.short_description = 'Hacer STAFF'

    def remove_staff(self, request, queryset):
        """Quitar permisos de staff"""
        updated = queryset.update(is_staff=False)
        self.message_user(request, f'{updated} usuario(s) ya no tienen permisos de STAFF')
    remove_staff.short_description = 'Quitar STAFF'

    def make_superuser(self, request, queryset):
        """Convertir usuarios en superuser"""
        updated = queryset.update(is_superuser=True, is_staff=True)
        self.message_user(request, f'{updated} usuario(s) ahora son SUPERUSER')
    make_superuser.short_description = 'Hacer SUPERUSER'

    def remove_superuser(self, request, queryset):
        """Quitar permisos de superuser"""
        updated = queryset.update(is_superuser=False)
        self.message_user(request, f'{updated} usuario(s) ya no son SUPERUSER')
    remove_superuser.short_description = 'Quitar SUPERUSER'

    def activate_users(self, request, queryset):
        """Activar usuarios"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} usuario(s) ACTIVADO(s)')
    activate_users.short_description = 'Activar usuarios'

    def deactivate_users(self, request, queryset):
        """Desactivar usuarios"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} usuario(s) DESACTIVADO(s)')
    deactivate_users.short_description = 'Desactivar usuarios'
