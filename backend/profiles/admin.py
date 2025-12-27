from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, CompanyProfile


class ProfileTypeFilter(admin.SimpleListFilter):
    """Filtro personalizado para distinguir entre candidatos y owners de empresas"""
    title = 'Tipo de Perfil'
    parameter_name = 'profile_type'

    def lookups(self, request, model_admin):
        return (
            ('candidate', 'Solo Candidatos'),
            ('company_owner', 'Owners de Empresas'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'candidate':
            # Mostrar solo UserProfiles que NO tienen CompanyProfile asociado
            return queryset.filter(company_profiles__isnull=True)
        if self.value() == 'company_owner':
            # Mostrar solo UserProfiles que tienen CompanyProfile asociado
            return queryset.filter(company_profiles__isnull=False).distinct()
        return queryset


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullName', 'email', 'phone', 'profile_type_badge', 'location', 'createdAt')
    search_fields = ('fullName', 'email', 'phone')
    list_filter = (ProfileTypeFilter, 'createdAt',)
    readonly_fields = ('id', 'createdAt', 'updatedAt')

    fieldsets = (
        ('Información Personal', {
            'fields': ('id', 'fullName', 'email', 'phone', 'profilePhoto')
        }),
        ('Ubicación', {
            'fields': ('location', 'bio')
        }),
        ('Fechas', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )

    def profile_type_badge(self, obj):
        """Muestra un badge indicando si es candidato o owner de empresa"""
        has_company = obj.company_profiles.exists()
        if has_company:
            company_count = obj.company_profiles.count()
            return format_html(
                '<span style="background-color: #6366f1; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">'
                '🏢 Owner ({} empresa{})'
                '</span>',
                company_count,
                's' if company_count > 1 else ''
            )
        else:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">'
                '👤 Candidato'
                '</span>'
            )

    profile_type_badge.short_description = 'Tipo'
    profile_type_badge.admin_order_field = 'company_profiles'


class VerificationStatusFilter(admin.SimpleListFilter):
    """Filtro para el estado de verificación"""
    title = 'Estado de Verificación'
    parameter_name = 'verification_status'

    def lookups(self, request, model_admin):
        return (
            ('verified', 'Verificadas'),
            ('pending', 'Pendientes de Verificación'),
            ('not_requested', 'Sin Solicitud'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'verified':
            return queryset.filter(verified=True)
        if self.value() == 'pending':
            return queryset.filter(verified=False, verificationRequestedAt__isnull=False)
        if self.value() == 'not_requested':
            return queryset.filter(verified=False, verificationRequestedAt__isnull=True)
        return queryset


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'companyName', 'nit', 'legalName', 'verification_status_badge', 'verification_actions', 'verificationRequestedAt', 'createdAt')
    search_fields = ('companyName', 'email', 'contactEmail', 'phone', 'nit', 'legalName')
    list_filter = (VerificationStatusFilter, 'category', 'verified', 'createdAt')
    readonly_fields = ('id', 'createdAt', 'updatedAt', 'verificationRequestedAt')
    actions = ['approve_verification', 'reject_verification']

    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'owner', 'companyName', 'description', 'category')
        }),
        ('Contacto', {
            'fields': ('email', 'contactEmail', 'phone', 'website')
        }),
        ('Ubicación', {
            'fields': ('location', 'city')
        }),
        ('Información Legal', {
            'fields': ('nit', 'legalName', 'seprecCode'),
            'description': 'Datos legales de la empresa para verificación'
        }),
        ('Verificación', {
            'fields': ('verified', 'verificationRequestedAt', 'verificationNotes'),
            'description': 'Estado de verificación de la empresa'
        }),
        ('Imágenes', {
            'fields': ('logo', 'banner')
        }),
        ('Fechas', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )

    def verification_status_badge(self, obj):
        """Badge visual del estado de verificación"""
        if obj.verified:
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 6px;">'
                '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="filter: drop-shadow(0 1px 2px rgba(124, 58, 237, 0.3));">'
                '<circle cx="12" cy="12" r="10" fill="#7C3AED"/>'
                '<path d="M9 12l2 2 4-4" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
                '</svg>'
                '<span style="font-weight: 600; color: #7C3AED;">Verificada</span>'
                '</span>'
            )
        elif obj.verificationRequestedAt:
            return format_html(
                '<span style="background-color: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">'
                '⏳ Pendiente de Verificación'
                '</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6B7280; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">'
                '— Sin Solicitud'
                '</span>'
            )

    verification_status_badge.short_description = 'Estado de Verificación'

    def verification_actions(self, obj):
        """Botones de acción para aprobar/rechazar verificación"""
        from django.urls import reverse
        from django.utils.http import urlencode

        if obj.verified:
            # Si ya está verificada, mostrar botón para revocar
            return format_html(
                '<a class="button" href="{}?verified=0" style="background-color: #ef4444; color: white; padding: 5px 12px; border-radius: 6px; text-decoration: none; font-size: 11px; font-weight: 600; display: inline-block;">'
                '❌ Revocar'
                '</a>',
                reverse('admin:profiles_companyprofile_change', args=[obj.pk])
            )
        elif obj.verificationRequestedAt:
            # Si tiene solicitud pendiente, mostrar botón para aprobar
            return format_html(
                '<a class="button" href="{}?verified=1" style="background-color: #7C3AED; color: white; padding: 5px 12px; border-radius: 6px; text-decoration: none; font-size: 11px; font-weight: 600; display: inline-block;">'
                '✅ Aprobar'
                '</a>',
                reverse('admin:profiles_companyprofile_change', args=[obj.pk])
            )
        else:
            return format_html(
                '<span style="color: #9CA3AF; font-size: 11px;">Sin solicitud</span>'
            )

    verification_actions.short_description = 'Acciones Rápidas'

    def approve_verification(self, request, queryset):
        """Acción para aprobar verificación"""
        count = queryset.filter(verified=False).update(verified=True)
        self.message_user(request, f'{count} empresa(s) verificada(s) exitosamente.')

    approve_verification.short_description = '✅ Aprobar Verificación'

    def reject_verification(self, request, queryset):
        """Acción para rechazar verificación"""
        count = queryset.filter(verified=True).update(verified=False)
        self.message_user(request, f'{count} empresa(s) marcada(s) como no verificada(s).')

    reject_verification.short_description = '❌ Rechazar Verificación'

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """Interceptar parámetros GET para aprobar/revocar verificación rápidamente"""
        if object_id and 'verified' in request.GET:
            try:
                obj = self.get_object(request, object_id)
                verified_value = request.GET.get('verified') == '1'

                if obj:
                    obj.verified = verified_value
                    obj.save(update_fields=['verified'])

                    if verified_value:
                        self.message_user(request, f'✅ Empresa "{obj.companyName}" verificada exitosamente.', level='success')
                    else:
                        self.message_user(request, f'❌ Verificación de "{obj.companyName}" revocada.', level='warning')

                    # Redirigir a la lista sin el parámetro
                    from django.shortcuts import redirect
                    return redirect('admin:profiles_companyprofile_changelist')
            except Exception as e:
                self.message_user(request, f'Error: {str(e)}', level='error')

        return super().changeform_view(request, object_id, form_url, extra_context)
