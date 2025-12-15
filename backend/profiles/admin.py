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


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'companyName', 'email', 'contactEmail', 'category', 'verified', 'createdAt')
    search_fields = ('companyName', 'email', 'contactEmail', 'phone')
    list_filter = ('category', 'verified', 'createdAt')
    readonly_fields = ('id', 'createdAt', 'updatedAt')

    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'owner', 'companyName', 'description', 'category', 'verified')
        }),
        ('Contacto', {
            'fields': ('email', 'contactEmail', 'phone', 'website')
        }),
        ('Ubicación', {
            'fields': ('location', 'city')
        }),
        ('Imágenes', {
            'fields': ('logo', 'banner')
        }),
        ('Fechas', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )
