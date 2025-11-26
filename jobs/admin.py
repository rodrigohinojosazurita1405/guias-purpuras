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
        'job_analytics_display',
        'proof_of_payment_preview'
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
            'fields': ('proofOfPayment', 'proof_of_payment_preview', 'payment_verification_summary', 'paymentVerified', 'paymentVerifiedBy', 'paymentVerificationDate', 'paymentVerificationNotes'),
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
        return obj.title[:50]
    job_title_display.short_description = 'Título'

    def company_display(self, obj):
        """Muestra el nombre de la empresa"""
        return 'Anónimo' if obj.companyAnonymous else obj.companyName
    company_display.short_description = 'Empresa'

    def status_badge(self, obj):
        """Badge de estado con colores"""
        status_colors = {
            'active': '#10B981',     # Verde
            'closed': '#EF4444',     # Rojo
            'draft': '#9CA3AF'       # Gris
        }
        status_labels = {
            'active': 'ACTIVA',
            'closed': 'CERRADA',
            'draft': 'BORRADOR'
        }
        color = status_colors.get(obj.status, '#6B7280')
        label = status_labels.get(obj.status, obj.status.upper())

        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Estado'

    def payment_badge(self, obj):
        """Badge de estado de pago con colores y estilos"""
        if obj.paymentVerified:
            color = '#059669'  # Verde oscuro
            label = '✓ VERIFICADO'
            icon = '✓'
        elif obj.proofOfPayment:
            color = '#F59E0B'  # Naranja
            label = '⏳ PENDIENTE'
            icon = '⏳'
        else:
            color = '#DC2626'  # Rojo oscuro
            label = '✗ SIN PAGO'
            icon = '✗'

        return format_html(
            '<span style="background-color: {}; color: white; padding: 6px 14px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block; letter-spacing: 0.5px;">{}</span>',
            color, label
        )
    payment_badge.short_description = 'Estado Pago'

    def applications_count(self, obj):
        """Muestra el contador de aplicaciones con estilo"""
        count = obj.applications
        return format_html(
            '<span style="background-color: #EDE9FE; color: #6D28D9; padding: 6px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 13px; '
            'display: inline-block; border-left: 4px solid #7C3AED;">👥 {}</span>',
            f'{count} aplicación{"es" if count != 1 else ""}'
        )
    applications_count.short_description = 'Aplicaciones'

    def views_count(self, obj):
        """Muestra el contador de vistas con estilo"""
        count = obj.views
        return format_html(
            '<span style="background-color: #DBEAFE; color: #1E40AF; padding: 6px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 13px; '
            'display: inline-block; border-left: 4px solid #3B82F6;">👁️ {}</span>',
            f'{count} vista{"s" if count != 1 else ""}'
        )
    views_count.short_description = 'Vistas'

    def created_date_display(self, obj):
        """Muestra la fecha de creación con estilo"""
        return format_html(
            '<span style="background-color: #ECFDF5; color: #065F46; padding: 6px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 13px; '
            'display: inline-block; border-left: 4px solid #10B981;">📅 {}</span>',
            obj.createdAt.strftime('%d/%m/%Y')
        )
    created_date_display.short_description = 'Publicado'

    def job_analytics_display(self, obj):
        """Muestra analíticas del trabajo"""
        return (
            f'Vistas: {obj.views}, Aplicaciones: {obj.applications}, '
            f'Publicado: {obj.createdAt.strftime("%d/%m/%Y")}'
        )
    job_analytics_display.short_description = 'Analíticas'

    def proof_of_payment_preview(self, obj):
        """Muestra preview de la imagen de comprobante de pago"""
        if not obj.proofOfPayment:
            return format_html(
                '<div style="background-color: #FEE2E2; padding: 12px; border-radius: 6px; '
                'text-align: center; color: #991B1B;"><strong>✗ Sin comprobante</strong></div>'
            )

        return format_html(
            '<div style="border: 2px solid #E5E7EB; border-radius: 8px; padding: 10px; '
            'max-width: 400px; background-color: #F9FAFB;">'
            '<img src="{}" style="max-width: 100%; height: auto; border-radius: 6px; '
            'box-shadow: 0 4px 6px rgba(0,0,0,0.1);" alt="Comprobante de pago">'
            '</div>',
            obj.proofOfPayment.url
        )
    proof_of_payment_preview.short_description = 'Vista Previa'

    def payment_verification_summary(self, obj):
        """Resumen de la verificación de pago con estilos CSS"""
        if not obj.proofOfPayment:
            return format_html(
                '<div style="background-color: #FEE2E2; padding: 12px; border-radius: 6px; '
                'border-left: 4px solid #DC2626; color: #991B1B;">'
                '<strong>✗ Sin comprobante de pago</strong>'
                '</div>'
            )

        # Determinar color según estado
        if obj.paymentVerified:
            bg_color = '#ECFDF5'
            border_color = '#059669'
            text_color = '#065F46'
            status_label = '✓ VERIFICADO'
            status_color = '#059669'
        else:
            bg_color = '#FFFBEB'
            border_color = '#F59E0B'
            text_color = '#78350F'
            status_label = '⏳ PENDIENTE'
            status_color = '#F59E0B'

        verified_by = obj.paymentVerifiedBy.username if obj.paymentVerifiedBy else 'Sin verificar'
        date_str = obj.paymentVerificationDate.strftime("%d/%m/%Y %H:%M") if obj.paymentVerificationDate else 'N/A'
        notes = obj.paymentVerificationNotes or '(Sin notas)'

        html_content = (
            f'<div style="background-color: {bg_color}; padding: 14px; border-radius: 6px; '
            f'border-left: 4px solid {border_color}; color: {text_color}; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto;">'
            f'<p style="margin: 0 0 8px 0; font-weight: bold; font-size: 14px;">'
            f'<span style="color: {status_color}; font-size: 16px; margin-right: 6px;">'
            f'{status_label.split()[0]}</span>{status_label}</p>'
            f'<p style="margin: 0 0 4px 0; font-size: 13px;">Verificado por: <strong>{verified_by}</strong></p>'
            f'<p style="margin: 0 0 4px 0; font-size: 13px;">Fecha: <strong>{date_str}</strong></p>'
            f'<p style="margin: 0; font-size: 13px; font-style: italic; color: {text_color}; opacity: 0.8;">Notas: {notes}</p>'
            f'</div>'
        )

        return format_html(html_content)
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
        from django.contrib.admin import messages as admin_messages
        self.message_user(request, f'✓ {updated} pago(s) VERIFICADO(s) exitosamente', admin_messages.SUCCESS)
    verify_payment_action.short_description = '✓ VERIFICAR pagos seleccionados'

    def reject_payment_action(self, request, queryset):
        """Acción: Rechazar pago"""
        updated = queryset.update(
            paymentVerified=False,
            paymentVerifiedBy=None,
            paymentVerificationDate=None
        )
        from django.contrib.admin import messages as admin_messages
        self.message_user(request, f'✗ {updated} pago(s) RECHAZADO(s)', admin_messages.WARNING)
    reject_payment_action.short_description = '✗ RECHAZAR pagos seleccionados'


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
