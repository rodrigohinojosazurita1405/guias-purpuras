from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Job, Application
from datetime import datetime


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    # Lista mejorada con columnas importantes
    list_display = (
        'job_title_display',
        'company_display',
        'city',
        'status_badge',
        'payment_badge',
        'applications_count',
        'views_count',
        'created_date_display'
    )

    # Filtros avanzados
    list_filter = (
        'status',
        'paymentVerified',
        'city',
        'contractType',
        'salaryType',
        'createdAt',
        'applicationType',
    )

    # Búsqueda mejorada
    search_fields = ('title', 'companyName', 'description', 'email', 'id')

    # Campos de solo lectura
    readonly_fields = (
        'id',
        'views',
        'applications',
        'createdAt',
        'updatedAt',
        'payment_verification_summary',
        'job_analytics_display'
    )

    # Acciones personalizadas
    actions = [
        'mark_as_active',
        'mark_as_closed',
        'verify_payment_action',
        'reject_payment_action'
    ]

    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'title', 'companyName', 'companyAnonymous', 'description')
        }),
        ('Clasificación', {
            'fields': ('jobCategory', 'city', 'municipality', 'subcategory', 'contractType', 'modality')
        }),
        ('Requisitos', {
            'fields': ('requirements', 'responsibilities', 'education', 'experience', 'languages', 'technicalSkills', 'softSkills')
        }),
        ('Compensación', {
            'fields': ('salaryType', 'salaryMin', 'salaryMax', 'salaryFixed', 'benefits')
        }),
        ('Vacantes y Aplicaciones', {
            'fields': ('vacancies', 'applications', 'expiryDate')
        }),
        ('Contacto', {
            'fields': ('email', 'whatsapp', 'website', 'applicationInstructions')
        }),
        ('Tipo de Aplicación', {
            'fields': ('applicationType', 'externalApplicationUrl', 'screeningQuestions')
        }),
        ('Plan y Estado', {
            'fields': ('selectedPlan', 'status', 'views')
        }),
        ('Verificación de Pago (FASE 7.1)', {
            'fields': ('proofOfPayment', 'payment_verification_summary', 'paymentVerified', 'paymentVerifiedBy', 'paymentVerificationDate', 'paymentVerificationNotes'),
            'classes': ('wide',),
            'description': 'Información de verificación de pago obligatorio'
        }),
        ('Timestamps', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )

    # ========== MÉTODOS DE DISPLAY PARA LA LISTA ==========

    def job_title_display(self, obj):
        """Muestra el título del trabajo"""
        if obj.status == 'active':
            icon = '🔵'
        elif obj.status == 'closed':
            icon = '⚫'
        else:
            icon = '🟡'
        return f'{icon} {obj.title[:50]}'
    job_title_display.short_description = 'Título'

    def company_display(self, obj):
        """Muestra el nombre de la empresa"""
        if obj.companyAnonymous:
            return 'Anónimo'
        return obj.companyName
    company_display.short_description = 'Empresa'

    def status_badge(self, obj):
        """Badge de estado"""
        labels = {
            'active': 'ACTIVA',
            'closed': 'CERRADA',
            'draft': 'BORRADOR'
        }
        return labels.get(obj.status, obj.status.upper())
    status_badge.short_description = 'Estado'

    def payment_badge(self, obj):
        """Badge de estado de pago"""
        if obj.paymentVerified:
            return 'VERIFICADO'
        elif obj.proofOfPayment:
            return 'PENDIENTE'
        else:
            return 'SIN PAGO'
    payment_badge.short_description = 'Pago'

    def applications_count(self, obj):
        """Muestra el contador de aplicaciones"""
        return f'{obj.applications} aplicaciones'
    applications_count.short_description = 'Aplicaciones'

    def views_count(self, obj):
        """Muestra el contador de vistas"""
        return f'{obj.views} vistas'
    views_count.short_description = 'Vistas'

    def created_date_display(self, obj):
        """Muestra la fecha de creación de forma amigable"""
        return obj.createdAt.strftime('%d/%m/%Y')
    created_date_display.short_description = 'Publicado'

    def job_analytics_display(self, obj):
        """Muestra analíticas del trabajo"""
        return (
            f'Vistas: {obj.views}, Aplicaciones: {obj.applications}, '
            f'Publicado: {obj.createdAt.strftime("%d/%m/%Y")}'
        )
    job_analytics_display.short_description = 'Analíticas'

    def payment_verification_summary(self, obj):
        """Resumen de la verificación de pago"""
        if not obj.proofOfPayment:
            return 'Sin comprobante de pago'

        status = 'VERIFICADO' if obj.paymentVerified else 'PENDIENTE'
        verified_by = obj.paymentVerifiedBy.username if obj.paymentVerifiedBy else 'N/A'
        date_str = obj.paymentVerificationDate.strftime("%d/%m/%Y %H:%M") if obj.paymentVerificationDate else 'N/A'
        notes = obj.paymentVerificationNotes or ''

        return f'Estado: {status}, Verificado por: {verified_by}, Fecha: {date_str}'
    payment_verification_summary.short_description = 'Resumen de Verificación'

    # ========== ACCIONES PERSONALIZADAS ==========

    def mark_as_active(self, request, queryset):
        """Acción: Marcar como activa"""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} anuncios marcados como ACTIVOS')
    mark_as_active.short_description = 'Marcar como ACTIVA'

    def mark_as_closed(self, request, queryset):
        """Acción: Marcar como cerrada"""
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} anuncios marcados como CERRADOS')
    mark_as_closed.short_description = 'Marcar como CERRADA'

    def verify_payment_action(self, request, queryset):
        """Acción: Verificar pago"""
        updated = queryset.update(
            paymentVerified=True,
            paymentVerifiedBy=request.user,
            paymentVerificationDate=datetime.now()
        )
        self.message_user(request, f'{updated} pagos VERIFICADOS exitosamente')
    verify_payment_action.short_description = 'VERIFICAR pagos seleccionados'

    def reject_payment_action(self, request, queryset):
        """Acción: Rechazar pago"""
        updated = queryset.update(
            paymentVerified=False,
            paymentVerifiedBy=None,
            paymentVerificationDate=None
        )
        self.message_user(request, f'{updated} pagos RECHAZADOS')
    reject_payment_action.short_description = 'RECHAZAR pagos seleccionados'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin personalizado para gestionar aplicaciones de candidatos"""

    list_display = (
        'candidate_name_display',
        'job_title_link',
        'candidate_email',
        'status_badge',
        'application_date',
        'screening_answers_preview'
    )

    list_filter = (
        'status',
        'createdAt',
        'job__city',
    )

    search_fields = (
        'applicantName',
        'applicantEmail',
        'job__title',
        'id'
    )

    readonly_fields = (
        'id',
        'job',
        'createdAt',
        'updatedAt',
        'screening_answers_display',
        'candidate_contact_display'
    )

    actions = [
        'mark_as_reviewing',
        'mark_as_shortlisted',
        'mark_as_rejected',
        'mark_as_accepted'
    ]

    fieldsets = (
        ('Información del Candidato', {
            'fields': ('id', 'applicantName', 'applicantEmail', 'applicantPhone', 'applicantWhatsapp', 'candidate_contact_display')
        }),
        ('Oferta de Trabajo', {
            'fields': ('job',)
        }),
        ('Respuestas de Screening', {
            'fields': ('screening_answers_display',),
            'classes': ('wide',)
        }),
        ('Evaluación', {
            'fields': ('status', 'recruiterNotes')
        }),
        ('Timestamps', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )

    # ========== MÉTODOS DE DISPLAY ==========

    def candidate_name_display(self, obj):
        """Muestra el nombre del candidato"""
        return obj.applicantName
    candidate_name_display.short_description = 'Candidato'

    def job_title_link(self, obj):
        """Link al trabajo con título"""
        url = reverse('admin:jobs_job_change', args=[obj.job.id])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.job.title[:40]
        )
    job_title_link.short_description = 'Oferta'

    def candidate_email(self, obj):
        """Email del candidato"""
        return obj.applicantEmail
    candidate_email.short_description = 'Email'

    def status_badge(self, obj):
        """Badge con estado de la aplicación"""
        labels = {
            'received': 'RECIBIDA',
            'reviewing': 'EN REVISIÓN',
            'shortlisted': 'PRESELECCIONADA',
            'rejected': 'RECHAZADA',
            'accepted': 'ACEPTADA',
            'withdrawn': 'RETIRADA'
        }
        return labels.get(obj.status, obj.status.upper())
    status_badge.short_description = 'Estado'

    def application_date(self, obj):
        """Fecha de aplicación"""
        return obj.createdAt.strftime('%d/%m/%Y %H:%M')
    application_date.short_description = 'Fecha'

    def screening_answers_preview(self, obj):
        """Preview de respuestas de screening"""
        if not obj.screeningAnswers:
            return 'Sin respuestas'

        count = len(obj.screeningAnswers)
        return f'{count} respuestas'
    screening_answers_preview.short_description = 'Respuestas'

    def screening_answers_display(self, obj):
        """Muestra todas las respuestas de screening de forma legible"""
        if not obj.screeningAnswers:
            return 'Sin respuestas de screening'

        result = 'Respuestas de Screening:\n'
        for idx, (key, answer) in enumerate(obj.screeningAnswers.items()):
            result += f'\nPregunta {int(key) + 1}:\n'

            # Obtener la pregunta original del job
            job = obj.job
            if job.screeningQuestions and int(key) < len(job.screeningQuestions):
                question = job.screeningQuestions[int(key)]
                result += f'{question.get("text", "Pregunta no disponible")}\n'

            result += f'Respuesta: {answer}\n'

        return result
    screening_answers_display.short_description = 'Respuestas de Screening'

    def candidate_contact_display(self, obj):
        """Muestra información de contacto del candidato"""
        contact = f'Email: {obj.applicantEmail}'
        if obj.applicantPhone:
            contact += f', Teléfono: {obj.applicantPhone}'
        if obj.applicantWhatsapp:
            contact += f', WhatsApp: {obj.applicantWhatsapp}'
        return contact
    candidate_contact_display.short_description = 'Información de Contacto'

    # ========== ACCIONES PERSONALIZADAS ==========

    def mark_as_reviewing(self, request, queryset):
        """Cambiar estado a EN REVISIÓN"""
        updated = queryset.update(status='reviewing')
        self.message_user(request, f'{updated} aplicaciones marcadas como EN REVISIÓN')
    mark_as_reviewing.short_description = 'Marcar como EN REVISIÓN'

    def mark_as_shortlisted(self, request, queryset):
        """Cambiar estado a PRESELECCIONADA"""
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f'{updated} aplicaciones PRESELECCIONADAS')
    mark_as_shortlisted.short_description = 'Marcar como PRESELECCIONADA'

    def mark_as_rejected(self, request, queryset):
        """Cambiar estado a RECHAZADA"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} aplicaciones RECHAZADAS')
    mark_as_rejected.short_description = 'Marcar como RECHAZADA'

    def mark_as_accepted(self, request, queryset):
        """Cambiar estado a ACEPTADA"""
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} aplicaciones ACEPTADAS')
    mark_as_accepted.short_description = 'Marcar como ACEPTADA'
