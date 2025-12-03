from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser, AdminUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin personalizado para CustomUser - muestra solo Usuarios (Empresas y Postulantes)"""

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
        'permission_info_display',
    )

    # Organización de campos por secciones
    fieldsets = (
        ('Información Personal', {
            'fields': ('id', 'email', 'username', 'first_name', 'last_name')
        }),
        ('Type de Usuario', {
            'fields': ('role', 'is_active'),
            'description': 'Solo empresas y postulantes. Para administradores, ver sección de Administración.'
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
        'activate_users',
        'deactivate_users',
    ]

    def get_queryset(self, request):
        """
        Filtrar solo usuarios que NO son superadmin (Empresas y Postulantes)
        """
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)

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
    role_badge.short_description = 'Tipo'

    def status_indicators(self, obj):
        """Muestra indicadores de estado (activo/inactivo)"""
        if not obj.is_active:
            return format_html(
                '<span style="background-color: #F3F4F6; color: #6B7280; padding: 6px 12px; '
                'border-radius: 12px; font-weight: bold; font-size: 12px; '
                'display: inline-block;">🔒 Inactivo</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ECFDF5; color: #059669; padding: 6px 12px; '
                'border-radius: 12px; font-weight: bold; font-size: 12px; '
                'display: inline-block;">✓ Activo</span>'
            )
    status_indicators.short_description = 'Estado'

    def last_login_display(self, obj):
        """Muestra la última conexión"""
        if obj.last_login:
            return obj.last_login.strftime('%d/%m/%Y %H:%M')
        return 'Nunca ha iniciado sesión'
    last_login_display.short_description = 'Última Conexión'

    def permission_info_display(self, obj):
        """Muestra información de permisos"""
        html_content = (
            '<div style="background-color: #F0FDF4; padding: 12px; border-radius: 8px; '
            'border-left: 4px solid #059669; color: #065F46;">'
            '<p style="margin: 0 0 8px 0; font-weight: 600;">ℹ️ Información del Usuario</p>'
            '<p style="margin: 0 0 4px 0;"><strong>Role:</strong> ' + obj.get_role_display() + '</p>'
            '<p style="margin: 0;"><strong>Tipo:</strong> Usuario regular (no administrador)</p>'
            '</div>'
        )
        return format_html(html_content)
    permission_info_display.short_description = 'Información'

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

    def has_add_permission(self, request):
        """No permitir agregar usuarios desde aquí"""
        return False

    def has_delete_permission(self, request, obj=None):
        """No permitir eliminar usuarios (solo desactivar)"""
        return False


@admin.register(AdminUser)
class AdminUserAdmin(BaseUserAdmin):
    """Admin personalizado para Administradores (Superadmin y Staff)"""

    # Campos mostrados en la lista
    list_display = (
        'email_display',
        'admin_type_badge',
        'admin_status_indicators',
        'last_login_display'
    )

    # Filtros disponibles
    list_filter = (
        'is_superuser',
        'is_staff',
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
        'admin_info_display',
    )

    # Organización de campos por secciones
    fieldsets = (
        ('Información Personal', {
            'fields': ('id', 'email', 'username', 'first_name', 'last_name')
        }),
        ('Permisos de Administración', {
            'fields': ('is_superuser', 'is_staff', 'is_active'),
            'description': 'Configurar permisos de administrador'
        }),
        ('Información de Admin', {
            'fields': ('admin_info_display',),
            'classes': ('wide',)
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
        'make_superuser',
        'remove_superuser',
        'make_staff',
        'remove_staff',
        'activate_admins',
        'deactivate_admins',
    ]

    def get_queryset(self, request):
        """
        Mostrar solo usuarios que SON superadmin o staff
        """
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=True)

    def email_display(self, obj):
        """Muestra el email con icono"""
        return format_html(
            '<span style="font-weight: 600;">✉️ {}</span>',
            obj.email
        )
    email_display.short_description = 'Email'

    def admin_type_badge(self, obj):
        """Badge del tipo de administrador"""
        if obj.is_superuser:
            return format_html(
                '<span style="background-color: #FEE2E2; color: #DC2626; padding: 6px 12px; '
                'border-radius: 20px; font-weight: bold; font-size: 12px; '
                'display: inline-block;">👑 Superadmin</span>'
            )
        elif obj.is_staff:
            return format_html(
                '<span style="background-color: #FEF3C7; color: #F59E0B; padding: 6px 12px; '
                'border-radius: 20px; font-weight: bold; font-size: 12px; '
                'display: inline-block;">⚙️ Staff</span>'
            )
        return '—'
    admin_type_badge.short_description = 'Tipo Admin'

    def admin_status_indicators(self, obj):
        """Muestra indicadores de estado (permisos y actividad)"""
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
    admin_status_indicators.short_description = 'Estado'

    def last_login_display(self, obj):
        """Muestra la última conexión"""
        if obj.last_login:
            return obj.last_login.strftime('%d/%m/%Y %H:%M')
        return 'Nunca ha iniciado sesión'
    last_login_display.short_description = 'Última Conexión'

    def admin_info_display(self, obj):
        """Muestra información completa del administrador"""
        html_content = (
            '<div style="background-color: #FEE2E2; padding: 14px; border-radius: 8px; '
            'border-left: 4px solid #DC2626; color: #7C2D12;">'
            '<p style="margin: 0 0 12px 0; font-weight: 700; font-size: 14px;">👑 ADMINISTRADOR DEL SISTEMA</p>'
        )

        # Permisos
        permisos = []
        if obj.is_superuser:
            permisos.append('✓ Acceso Total (Superuser)')
        if obj.is_staff:
            permisos.append('✓ Acceso Admin')
        if obj.is_active:
            permisos.append('✓ Cuenta Activa')
        else:
            permisos.append('✗ Cuenta Desactivada')

        html_content += '<ul style="margin: 0; padding-left: 20px;">'
        for permiso in permisos:
            html_content += f'<li style="margin: 4px 0; color: #7C2D12;">{permiso}</li>'
        html_content += '</ul>'

        html_content += '</div>'
        return format_html(html_content)
    admin_info_display.short_description = 'Información Admin'

    def make_superuser(self, request, queryset):
        """Hacer usuario superuser"""
        updated = queryset.update(is_superuser=True, is_staff=True, is_active=True)
        self.message_user(request, f'{updated} admin(s) promovido(s) a SUPERUSER')
    make_superuser.short_description = '👑 Hacer SUPERUSER'

    def remove_superuser(self, request, queryset):
        """Quitar permisos de superuser"""
        updated = queryset.update(is_superuser=False)
        self.message_user(request, f'{updated} admin(s) ya no son SUPERUSER')
    remove_superuser.short_description = '✗ Quitar SUPERUSER'

    def make_staff(self, request, queryset):
        """Convertir en staff"""
        updated = queryset.update(is_staff=True, is_active=True)
        self.message_user(request, f'{updated} admin(s) ahora son STAFF')
    make_staff.short_description = '⚙️ Hacer STAFF'

    def remove_staff(self, request, queryset):
        """Quitar permisos de staff"""
        updated = queryset.update(is_staff=False)
        self.message_user(request, f'{updated} admin(s) ya no son STAFF')
    remove_staff.short_description = '✗ Quitar STAFF'

    def activate_admins(self, request, queryset):
        """Activar administradores"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} admin(s) ACTIVADO(s)')
    activate_admins.short_description = '✓ Activar Administradores'

    def deactivate_admins(self, request, queryset):
        """Desactivar administradores"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} admin(s) DESACTIVADO(s)')
    deactivate_admins.short_description = '✗ Desactivar Administradores'
