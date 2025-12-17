from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ApplicantProfile, ApplicantCV, JobApplication, SavedJob
from datetime import datetime


@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    """Admin para perfiles de postulantes"""

    list_display = (
        'user_display',
        'email_display',
        'phone',
        'total_applications_badge',
        'has_linkedin',
        'has_portfolio',
        'created_date_display'
    )

    list_filter = (
        'desired_modality',
        'created_at',
    )

    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'phone'
    )

    readonly_fields = (
        'user',
        'total_applications',
        'created_at',
        'updated_at'
    )

    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Contacto', {
            'fields': ('phone', 'linkedin_url', 'portfolio_url')
        }),
        ('Preferencias de Búsqueda', {
            'fields': (
                'desired_job_categories',
                'desired_cities',
                'desired_modality'
            ),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('total_applications',),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def user_display(self, obj):
        """Mostrar nombre completo o email del usuario"""
        name = obj.user.get_full_name()
        if name:
            return format_html('<strong>{}</strong>', name)
        return format_html('<em>{}</em>', obj.user.email)
    user_display.short_description = 'Postulante'

    def email_display(self, obj):
        """Mostrar email del usuario"""
        return obj.user.email
    email_display.short_description = 'Email'

    def total_applications_badge(self, obj):
        """Badge con el total de postulaciones"""
        if obj.total_applications == 0:
            color = '#9CA3AF'
        elif obj.total_applications < 5:
            color = '#3B82F6'
        elif obj.total_applications < 10:
            color = '#8B5CF6'
        else:
            color = '#10B981'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-weight: 600; font-size: 0.875rem;">{}</span>',
            color, obj.total_applications
        )
    total_applications_badge.short_description = 'Postulaciones'

    def has_linkedin(self, obj):
        """Indicador de perfil de LinkedIn"""
        if obj.linkedin_url:
            return format_html('<span style="color: #0A66C2;">✓ LinkedIn</span>')
        return format_html('<span style="color: #D1D5DB;">-</span>')
    has_linkedin.short_description = 'LinkedIn'

    def has_portfolio(self, obj):
        """Indicador de portafolio"""
        if obj.portfolio_url:
            return format_html('<span style="color: #7C3AED;">✓ Portfolio</span>')
        return format_html('<span style="color: #D1D5DB;">-</span>')
    has_portfolio.short_description = 'Portfolio'

    def created_date_display(self, obj):
        """Fecha de creación formateada"""
        return obj.created_at.strftime('%d/%m/%Y')
    created_date_display.short_description = 'Registrado'


@admin.register(ApplicantCV)
class ApplicantCVAdmin(admin.ModelAdmin):
    """Admin para CVs de postulantes"""

    list_display = (
        'id_short',
        'applicant_display',
        'name',
        'cv_type_badge',
        'applications_count',
        'is_deleted_badge',
        'created_date_display'
    )

    list_filter = (
        'cv_type',
        'is_deleted',
        'created_at',
    )

    search_fields = (
        'name',
        'applicant__email',
        'applicant__first_name',
        'applicant__last_name',
        'id'
    )

    readonly_fields = (
        'id',
        'applicant',
        'created_at',
        'updated_at',
        'deleted_at',
        'cv_data_display',
        'file_info_display'
    )

    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'applicant', 'name', 'cv_type')
        }),
        ('Contenido del CV', {
            'fields': ('cv_data_display', 'file', 'file_info_display')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'deleted_at')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    actions = ['mark_as_deleted', 'restore_cv']

    def id_short(self, obj):
        """ID corto para visualización"""
        return str(obj.id)[:8]
    id_short.short_description = 'ID'

    def applicant_display(self, obj):
        """Mostrar información del postulante"""
        name = obj.applicant.get_full_name()
        if name:
            return format_html(
                '<a href="{}" style="font-weight: 500;">{}</a><br>'
                '<small style="color: #6B7280;">{}</small>',
                reverse('admin:auth_api_customuser_change', args=[obj.applicant.id]),
                name,
                obj.applicant.email
            )
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:auth_api_customuser_change', args=[obj.applicant.id]),
            obj.applicant.email
        )
    applicant_display.short_description = 'Postulante'

    def cv_type_badge(self, obj):
        """Badge para el tipo de CV"""
        if obj.cv_type == 'created':
            return format_html(
                '<span style="background-color: #7C3AED; color: white; padding: 3px 10px; '
                'border-radius: 12px; font-weight: 600; font-size: 0.875rem;">📝 Creado</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #3B82F6; color: white; padding: 3px 10px; '
                'border-radius: 12px; font-weight: 600; font-size: 0.875rem;">📄 Subido</span>'
            )
    cv_type_badge.short_description = 'Tipo'

    def applications_count(self, obj):
        """Número de veces que se usó este CV"""
        count = obj.applications.count()
        if count == 0:
            color = '#9CA3AF'
        else:
            color = '#10B981'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-weight: 600; font-size: 0.875rem;">{}</span>',
            color, count
        )
    applications_count.short_description = 'Usos'

    def is_deleted_badge(self, obj):
        """Badge para CV eliminado"""
        if obj.is_deleted:
            return format_html(
                '<span style="background-color: #EF4444; color: white; padding: 3px 10px; '
                'border-radius: 12px; font-weight: 600; font-size: 0.875rem;">Eliminado</span>'
            )
        return format_html(
            '<span style="background-color: #10B981; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-weight: 600; font-size: 0.875rem;">Activo</span>'
        )
    is_deleted_badge.short_description = 'Estado'

    def created_date_display(self, obj):
        """Fecha de creación formateada"""
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    created_date_display.short_description = 'Creado'

    def cv_data_display(self, obj):
        """Mostrar datos del CV de forma legible (solo para CVs creados)"""
        if obj.cv_type == 'created' and obj.cv_data:
            import json
            formatted_json = json.dumps(obj.cv_data, indent=2, ensure_ascii=False)
            return format_html('<pre style="max-height: 400px; overflow: auto;">{}</pre>', formatted_json)
        return '-'
    cv_data_display.short_description = 'Datos del CV'

    def file_info_display(self, obj):
        """Información del archivo subido"""
        if obj.cv_type == 'uploaded' and obj.file:
            return format_html(
                '<a href="{}" target="_blank" style="color: #7C3AED; font-weight: 500;">📎 Descargar CV</a><br>'
                '<small style="color: #6B7280;">Archivo: {}</small>',
                obj.file.url,
                obj.file.name
            )
        return '-'
    file_info_display.short_description = 'Archivo'

    def mark_as_deleted(self, request, queryset):
        """Acción para marcar CVs como eliminados"""
        from django.utils import timezone
        count = queryset.update(is_deleted=True, deleted_at=timezone.now())
        self.message_user(request, f'{count} CV(s) marcado(s) como eliminado(s).')
    mark_as_deleted.short_description = 'Marcar como eliminado'

    def restore_cv(self, request, queryset):
        """Acción para restaurar CVs eliminados"""
        count = queryset.update(is_deleted=False, deleted_at=None)
        self.message_user(request, f'{count} CV(s) restaurado(s).')
    restore_cv.short_description = 'Restaurar CV'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """Admin para postulaciones a trabajos"""

    list_display = (
        'id_short',
        'job_title_display',
        'applicant_name_display',
        'status_badge',
        'cv_name_display',
        'viewed_badge',
        'applied_date_display'
    )

    list_filter = (
        'status',
        'viewed_by_employer',
        'applied_at',
    )

    search_fields = (
        'job__title',
        'job__companyName',
        'applicant__email',
        'applicant__first_name',
        'applicant__last_name',
        'id'
    )

    readonly_fields = (
        'id',
        'job',
        'applicant',
        'cv',
        'applied_at',
        'updated_at',
        'viewed_at',
        'cover_letter_display',
        'screening_answers_display'
    )

    fieldsets = (
        ('Información de la Postulación', {
            'fields': ('id', 'job', 'applicant', 'cv', 'status')
        }),
        ('Documentos', {
            'fields': ('cover_letter_display', 'screening_answers_display')
        }),
        ('Revisión del Empleador', {
            'fields': ('viewed_by_employer', 'viewed_at', 'employer_notes')
        }),
        ('Fechas', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    actions = [
        'mark_as_reviewing',
        'mark_as_shortlisted',
        'mark_as_rejected',
        'mark_as_viewed'
    ]

    def id_short(self, obj):
        """ID corto para visualización"""
        return str(obj.id)[:8]
    id_short.short_description = 'ID'

    def job_title_display(self, obj):
        """Mostrar título del trabajo con enlace"""
        return format_html(
            '<a href="{}" style="font-weight: 500;">{}</a><br>'
            '<small style="color: #6B7280;">{}</small>',
            reverse('admin:jobs_job_change', args=[obj.job.id]),
            obj.job.title,
            obj.job.companyName
        )
    job_title_display.short_description = 'Trabajo'

    def applicant_name_display(self, obj):
        """Mostrar nombre del postulante con enlace"""
        name = obj.applicant.get_full_name()
        if name:
            return format_html(
                '<a href="{}" style="font-weight: 500;">{}</a><br>'
                '<small style="color: #6B7280;">{}</small>',
                reverse('admin:auth_api_customuser_change', args=[obj.applicant.id]),
                name,
                obj.applicant.email
            )
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:auth_api_customuser_change', args=[obj.applicant.id]),
            obj.applicant.email
        )
    applicant_name_display.short_description = 'Postulante'

    def status_badge(self, obj):
        """Badge colorido según el estado"""
        status_colors = {
            'submitted': '#3B82F6',     # Azul
            'reviewing': '#F59E0B',     # Amarillo
            'shortlisted': '#8B5CF6',   # Púrpura
            'interviewed': '#7C3AED',   # Púrpura oscuro
            'rejected': '#EF4444',      # Rojo
            'accepted': '#10B981',      # Verde
            'withdrawn': '#6B7280'      # Gris
        }

        status_icons = {
            'submitted': '📨',
            'reviewing': '👀',
            'shortlisted': '⭐',
            'interviewed': '💼',
            'rejected': '❌',
            'accepted': '✅',
            'withdrawn': '🔙'
        }

        color = status_colors.get(obj.status, '#9CA3AF')
        icon = status_icons.get(obj.status, '📋')

        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 12px; '
            'border-radius: 12px; font-weight: 600; font-size: 0.875rem;">{} {}</span>',
            color, icon, obj.get_status_display()
        )
    status_badge.short_description = 'Estado'

    def cv_name_display(self, obj):
        """Mostrar nombre del CV usado"""
        if obj.cv:
            return format_html(
                '<a href="{}" style="color: #7C3AED;">{}</a>',
                reverse('admin:applicants_applicantcv_change', args=[obj.cv.id]),
                obj.cv.name
            )
        return format_html('<span style="color: #9CA3AF;">-</span>')
    cv_name_display.short_description = 'CV Usado'

    def viewed_badge(self, obj):
        """Badge de si fue visto por el empleador"""
        if obj.viewed_by_employer:
            return format_html(
                '<span style="color: #10B981; font-weight: 600;">👁️ Visto</span>'
            )
        return format_html(
            '<span style="color: #9CA3AF;">⚪ No visto</span>'
        )
    viewed_badge.short_description = 'Visualización'

    def applied_date_display(self, obj):
        """Fecha de postulación formateada"""
        return obj.applied_at.strftime('%d/%m/%Y %H:%M')
    applied_date_display.short_description = 'Postulado'

    def cover_letter_display(self, obj):
        """Mostrar carta de presentación de forma legible"""
        if obj.cover_letter:
            return format_html(
                '<div style="max-height: 200px; overflow: auto; padding: 10px; '
                'background: #F9FAFB; border-radius: 8px; border: 1px solid #E5E7EB;">{}</div>',
                obj.cover_letter
            )
        return '-'
    cover_letter_display.short_description = 'Carta de Presentación'

    def screening_answers_display(self, obj):
        """Mostrar respuestas a preguntas de filtrado"""
        if obj.screening_answers:
            import json
            formatted_json = json.dumps(obj.screening_answers, indent=2, ensure_ascii=False)
            return format_html('<pre style="max-height: 200px; overflow: auto;">{}</pre>', formatted_json)
        return '-'
    screening_answers_display.short_description = 'Respuestas de Filtrado'

    def mark_as_reviewing(self, request, queryset):
        """Marcar postulaciones como en revisión"""
        count = queryset.update(status='reviewing')
        self.message_user(request, f'{count} postulación(es) marcada(s) como "En Revisión".')
    mark_as_reviewing.short_description = 'Marcar como "En Revisión"'

    def mark_as_shortlisted(self, request, queryset):
        """Marcar postulaciones como pre-seleccionadas"""
        count = queryset.update(status='shortlisted')
        self.message_user(request, f'{count} postulación(es) pre-seleccionada(s).')
    mark_as_shortlisted.short_description = 'Pre-seleccionar'

    def mark_as_rejected(self, request, queryset):
        """Marcar postulaciones como rechazadas"""
        count = queryset.update(status='rejected')
        self.message_user(request, f'{count} postulación(es) rechazada(s).')
    mark_as_rejected.short_description = 'Rechazar'

    def mark_as_viewed(self, request, queryset):
        """Marcar como visto por empleador"""
        from django.utils import timezone
        count = queryset.update(viewed_by_employer=True, viewed_at=timezone.now())
        self.message_user(request, f'{count} postulación(es) marcada(s) como vista(s).')
    mark_as_viewed.short_description = 'Marcar como visto'


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    """Admin para trabajos guardados"""

    list_display = (
        'id_short',
        'user_display',
        'job_title_display',
        'saved_date_display'
    )

    list_filter = (
        'saved_at',
    )

    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'job__title',
        'job__companyName'
    )

    readonly_fields = (
        'id',
        'user',
        'job',
        'saved_at'
    )

    fieldsets = (
        ('Información', {
            'fields': ('id', 'user', 'job')
        }),
        ('Fechas', {
            'fields': ('saved_at',)
        })
    )

    def id_short(self, obj):
        """ID corto para visualización"""
        return str(obj.id)[:8]
    id_short.short_description = 'ID'

    def user_display(self, obj):
        """Mostrar usuario"""
        name = obj.user.get_full_name()
        if name:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:auth_api_customuser_change', args=[obj.user.id]),
                name
            )
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:auth_api_customuser_change', args=[obj.user.id]),
            obj.user.email
        )
    user_display.short_description = 'Usuario'

    def job_title_display(self, obj):
        """Mostrar trabajo guardado"""
        return format_html(
            '<a href="{}" style="font-weight: 500;">{}</a><br>'
            '<small style="color: #6B7280;">{}</small>',
            reverse('admin:jobs_job_change', args=[obj.job.id]),
            obj.job.title,
            obj.job.companyName
        )
    job_title_display.short_description = 'Trabajo Guardado'

    def saved_date_display(self, obj):
        """Fecha de guardado formateada"""
        return obj.saved_at.strftime('%d/%m/%Y %H:%M')
    saved_date_display.short_description = 'Guardado'
