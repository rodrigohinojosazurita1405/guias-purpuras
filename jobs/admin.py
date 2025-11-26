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
        """Muestra el título del trabajo con línea activa/inactiva"""
        if obj.status == 'active':
            color = '#10B981'  # Verde
            icon = '🔵'
        elif obj.status == 'closed':
            color = '#EF4444'  # Rojo
            icon = '⚫'
        else:
            color = '#F59E0B'  # Naranja
            icon = '🟡'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.title[:50]
        )
    job_title_display.short_description = 'Título'

    def company_display(self, obj):
        """Muestra el nombre de la empresa"""
        if obj.companyAnonymous:
            return format_html(
                '<span style="color: #999; font-style: italic;">Anónimo</span>'
            )
        return obj.companyName
    company_display.short_description = 'Empresa'

    def status_badge(self, obj):
        """Badge de estado"""
        colors = {
            'active': '#10B981',
            'closed': '#EF4444',
            'draft': '#F59E0B'
        }
        labels = {
            'active': 'ACTIVA',
            'closed': 'CERRADA',
            'draft': 'BORRADOR'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#999'),
            labels.get(obj.status, obj.status.upper())
        )
    status_badge.short_description = 'Estado'

    def payment_badge(self, obj):
        """Badge de estado de pago"""
        if obj.paymentVerified:
            return format_html(
                '<span style="background-color: #10B981; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">VERIFICADO</span>'
            )
        elif obj.proofOfPayment:
            return format_html(
                '<span style="background-color: #F59E0B; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">PENDIENTE</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #EF4444; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">SIN PAGO</span>'
            )
    payment_badge.short_description = 'Pago'

    def applications_count(self, obj):
        """Muestra el contador de aplicaciones"""
        return format_html(
            '<strong style="color: #7C3AED;">{}</strong> aplicaciones',
            obj.applications
        )
    applications_count.short_description = 'Aplicaciones'

    def views_count(self, obj):
        """Muestra el contador de vistas"""
        return format_html(
            '<span style="color: #666;">{} vistas</span>',
            obj.views
        )
    views_count.short_description = 'Vistas'

    def created_date_display(self, obj):
        """Muestra la fecha de creación de forma amigable"""
        return obj.createdAt.strftime('%d/%m/%Y')
    created_date_display.short_description = 'Publicado'

    def job_analytics_display(self, obj):
        """Muestra analíticas del trabajo"""
        html = f'<div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px;">'
        html += f'<h3 style="margin-top: 0; color: #7C3AED;">Analíticas</h3>'
        html += f'<p><strong>Vistas:</strong> {obj.views}</p>'
        html += f'<p><strong>Aplicaciones:</strong> {obj.applications}</p>'
        html += f'<p><strong>Publicado:</strong> {obj.createdAt.strftime("%d de %B de %Y")}</p>'
        html += f'<p><strong>Actualizado:</strong> {obj.updatedAt.strftime("%d de %B de %Y")}</p>'
        html += f'</div>'
        return mark_safe(html)
    job_analytics_display.short_description = 'Analíticas'

    def payment_verification_summary(self, obj):
        """Resumen de la verificación de pago"""
        if not obj.proofOfPayment:
            return format_html(
                '<div style="background-color: #FEE2E2; padding: 15px; border-radius: 8px; color: #991B1B;"><strong>Sin comprobante de pago</strong></div>'
            )

        html = f'<div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px;">'
        html += f'<p><strong>Comprobante:</strong> <a href="{obj.proofOfPayment.url}" target="_blank" style="color: #7C3AED;">Ver imagen</a></p>'

        if obj.paymentVerified:
            html += f'<p><strong>Estado:</strong> <span style="color: #10B981; font-weight: bold;">VERIFICADO</span></p>'
            html += f'<p><strong>Verificado por:</strong> {obj.paymentVerifiedBy.username if obj.paymentVerifiedBy else "N/A"}</p>'
            html += f'<p><strong>Fecha:</strong> {obj.paymentVerificationDate.strftime("%d/%m/%Y %H:%M") if obj.paymentVerificationDate else "N/A"}</p>'
        else:
            html += f'<p><strong>Estado:</strong> <span style="color: #F59E0B; font-weight: bold;">PENDIENTE</span></p>'

        if obj.paymentVerificationNotes:
            html += f'<p><strong>Notas:</strong> {obj.paymentVerificationNotes}</p>'

        html += '</div>'
        return mark_safe(html)
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
        return format_html(
            '<strong style="color: #7C3AED;">{}</strong>',
            obj.applicantName
        )
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
        return format_html(
            '<a href="mailto:{}">{}</a>',
            obj.applicantEmail,
            obj.applicantEmail
        )
    candidate_email.short_description = 'Email'

    def status_badge(self, obj):
        """Badge con estado de la aplicación"""
        colors = {
            'received': '#3B82F6',
            'reviewing': '#F59E0B',
            'shortlisted': '#8B5CF6',
            'rejected': '#EF4444',
            'accepted': '#10B981',
            'withdrawn': '#6B7280'
        }
        labels = {
            'received': 'RECIBIDA',
            'reviewing': 'EN REVISIÓN',
            'shortlisted': 'PRESELECCIONADA',
            'rejected': 'RECHAZADA',
            'accepted': 'ACEPTADA',
            'withdrawn': 'RETIRADA'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#999'),
            labels.get(obj.status, obj.status.upper())
        )
    status_badge.short_description = 'Estado'

    def application_date(self, obj):
        """Fecha de aplicación"""
        return obj.createdAt.strftime('%d/%m/%Y %H:%M')
    application_date.short_description = 'Fecha'

    def screening_answers_preview(self, obj):
        """Preview de respuestas de screening"""
        if not obj.screeningAnswers:
            return format_html('<span style="color: #999;">Sin respuestas</span>')

        count = len(obj.screeningAnswers)
        return format_html(
            '<span style="color: #7C3AED; font-weight: bold;">{}</span> respuestas',
            count
        )
    screening_answers_preview.short_description = 'Respuestas'

    def screening_answers_display(self, obj):
        """Muestra todas las respuestas de screening de forma legible"""
        if not obj.screeningAnswers:
            return format_html(
                '<div style="color: #999; font-style: italic;">Sin respuestas de screening</div>'
            )

        html = '<div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px;">'
        html += '<h3 style="margin-top: 0; color: #7C3AED;">Respuestas de Screening</h3>'

        for idx, (key, answer) in enumerate(obj.screeningAnswers.items()):
            html += f'<div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #ddd;">'
            html += f'<strong style="color: #333;">Pregunta {int(key) + 1}:</strong><br>'

            # Obtener la pregunta original del job
            job = obj.job
            if job.screeningQuestions and int(key) < len(job.screeningQuestions):
                question = job.screeningQuestions[int(key)]
                html += f'<em style="color: #666;">{question.get("text", "Pregunta no disponible")}</em><br>'

            html += f'<strong style="color: #7C3AED;">Respuesta:</strong> {answer}<br>'
            html += '</div>'

        html += '</div>'
        return mark_safe(html)
    screening_answers_display.short_description = 'Respuestas de Screening'

    def candidate_contact_display(self, obj):
        """Muestra información de contacto del candidato"""
        html = '<div style="background-color: #f0f9ff; padding: 12px; border-radius: 8px; border-left: 4px solid #7C3AED;">'
        html += f'<p><strong>Email:</strong> <a href="mailto:{obj.applicantEmail}">{obj.applicantEmail}</a></p>'
        if obj.applicantPhone:
            html += f'<p><strong>Teléfono:</strong> {obj.applicantPhone}</p>'
        if obj.applicantWhatsapp:
            html += f'<p><strong>WhatsApp:</strong> <a href="https://wa.me/{obj.applicantWhatsapp.replace(" ", "").replace("+", "")}" target="_blank">{obj.applicantWhatsapp}</a></p>'
        html += '</div>'
        return mark_safe(html)
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
