from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Job, Application, JobAuditLog, PlanOrder, BlockedUser
from datetime import datetime
import json


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    # Lista mejorada con columnas importantes
    list_display = (
        'job_title_display',
        'company_display',
        'city',
        'status_badge',
        'payment_badge',
        'plan_display',
        'expiry_countdown',
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
        """Badge de estado con colores sobrios"""
        status_colors = {
            'active': '#059669',     # Verde sobrio
            'closed': '#DC2626',     # Rojo sobrio
            'draft': '#6B7280'       # Gris sobrio
        }
        status_labels = {
            'active': 'ACTIVA',
            'closed': 'CERRADA',
            'draft': 'BORRADOR'
        }
        color = status_colors.get(obj.status, '#6B7280')
        label = status_labels.get(obj.status, obj.status.upper())

        return format_html(
            '<span style="background-color: {}; color: white; padding: 6px 14px; '
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
            'display: inline-block;">👥 {}</span>',
            f'{count} aplicación{"es" if count != 1 else ""}'
        )
    applications_count.short_description = 'Aplicaciones'

    def views_count(self, obj):
        """Muestra el contador de vistas con estilo"""
        count = obj.views
        return format_html(
            '<span style="background-color: #DBEAFE; color: #1E40AF; padding: 6px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 13px; '
            'display: inline-block;">👁️ {}</span>',
            f'{count} vista{"s" if count != 1 else ""}'
        )
    views_count.short_description = 'Vistas'

    def created_date_display(self, obj):
        """Muestra la fecha de creación con estilo"""
        return format_html(
            '<span style="background-color: #ECFDF5; color: #065F46; padding: 6px 12px; '
            'border-radius: 20px; font-weight: bold; font-size: 13px; '
            'display: inline-block;">📅 {}</span>',
            obj.createdAt.strftime('%d/%m/%Y')
        )
    created_date_display.short_description = 'Publicado'

    def plan_display(self, obj):
        """Muestra el plan seleccionado con colores temáticos y duración"""
        from plans.models import Plan

        # Colores para cada plan
        plan_colors = {
            'escencial': {'color': '#3B82F6', 'bg': '#DBEAFE'},  # Azul
            'purpura': {'color': '#8B5CF6', 'bg': '#EDE9FE'},     # Púrpura
            'impulso': {'color': '#EC4899', 'bg': '#FCE7F3'}      # Rosa
        }

        # Obtener datos del plan desde BD
        try:
            plan_obj = Plan.objects.get(name=obj.selectedPlan)
            label = plan_obj.label
            duration = f"{plan_obj.duration_days} días"
            colors = plan_colors.get(obj.selectedPlan, plan_colors['escencial'])
        except Plan.DoesNotExist:
            # Fallback si el plan no existe en BD
            label = obj.selectedPlan.upper()
            duration = "N/A"
            colors = plan_colors.get(obj.selectedPlan, plan_colors['escencial'])

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 6px 14px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block;">💰 {} ({} vigencia)</span>',
            colors['bg'], colors['color'], label, duration
        )
    plan_display.short_description = 'Plan'

    def expiry_countdown(self, obj):
        """Muestra días restantes con color dinámico según urgencia"""
        from datetime import date, timedelta

        today = date.today()
        days_remaining = (obj.expiryDate - today).days

        # Determinar color según urgencia
        if days_remaining < 0:
            color = '#DC2626'      # Rojo - Expirado
            bg_color = '#FEE2E2'
            status = 'EXPIRADO'
            icon = '✗'
        elif days_remaining == 0:
            color = '#DC2626'      # Rojo - Vence hoy
            bg_color = '#FEE2E2'
            status = 'VENCE HOY'
            icon = '⚠️'
        elif days_remaining <= 3:
            color = '#DC2626'      # Rojo - Menos de 3 días
            bg_color = '#FEE2E2'
            status = f'{days_remaining} día{"s" if days_remaining != 1 else ""} restante{"s" if days_remaining != 1 else ""}'
            icon = '🔴'
        elif days_remaining <= 7:
            color = '#F59E0B'      # Naranja - Una semana
            bg_color = '#FFFBEB'
            status = f'{days_remaining} días restantes'
            icon = '🟡'
        elif days_remaining <= 14:
            color = '#F59E0B'      # Naranja claro - Dos semanas
            bg_color = '#FFFBEB'
            status = f'{days_remaining} días restantes'
            icon = '🟡'
        else:
            color = '#10B981'      # Verde - Tiempo suficiente
            bg_color = '#ECFDF5'
            status = f'{days_remaining} días restantes'
            icon = '🟢'

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 6px 14px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block;">{} {}</span>',
            bg_color, color, icon, status
        )
    expiry_countdown.short_description = 'Vencimiento'

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
        """Badge con estado de la aplicación con colores sobrios"""
        status_colors = {
            'received': '#3B82F6',        # Azul
            'reviewing': '#F59E0B',       # Naranja
            'shortlisted': '#10B981',     # Verde
            'rejected': '#DC2626',        # Rojo
            'accepted': '#059669',        # Verde oscuro
            'withdrawn': '#6B7280'        # Gris
        }
        labels = {
            'received': 'RECIBIDA',
            'reviewing': 'EN REVISIÓN',
            'shortlisted': 'PRESELECCIONADA',
            'rejected': 'RECHAZADA',
            'accepted': 'ACEPTADA',
            'withdrawn': 'RETIRADA'
        }
        color = status_colors.get(obj.status, '#6B7280')
        label = labels.get(obj.status, obj.status.upper())

        return format_html(
            '<span style="background-color: {}; color: white; padding: 6px 14px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block;">{}</span>',
            color, label
        )
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
        """Muestra información de contacto del candidato con estilos"""
        html_content = (
            '<div style="background-color: #F3F4F6; padding: 12px; border-radius: 8px; '
            'font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto; font-size: 13px;">'
        )

        # Email
        if obj.applicantEmail:
            html_content += (
                '<p style="margin: 0 0 8px 0; display: flex; align-items: center;">'
                '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">✉️</span>'
                f'<span style="color: #374151;">{obj.applicantEmail}</span>'
                '</p>'
            )

        # Teléfono
        if obj.applicantPhone:
            html_content += (
                '<p style="margin: 0 0 8px 0; display: flex; align-items: center;">'
                '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">☎️</span>'
                f'<span style="color: #374151;">{obj.applicantPhone}</span>'
                '</p>'
            )

        # WhatsApp
        if obj.applicantWhatsapp:
            html_content += (
                '<p style="margin: 0; display: flex; align-items: center;">'
                '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">💬</span>'
                f'<span style="color: #374151;">{obj.applicantWhatsapp}</span>'
                '</p>'
            )

        html_content += '</div>'
        return format_html(html_content)
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


@admin.register(JobAuditLog)
class JobAuditLogAdmin(admin.ModelAdmin):
    """Admin para auditoría de cambios en trabajos"""

    list_display = (
        'timestamp_display',
        'job_link',
        'action_badge',
        'user_display',
        'client_ip_display'
    )

    list_filter = (
        'action',
        'timestamp',
        'userEmail',
    )

    search_fields = (
        'job__title',
        'job__id',
        'userEmail',
        'clientIP',
        'notes'
    )

    readonly_fields = (
        'id',
        'job',
        'timestamp',
        'changed_fields_display',
        'user_email_display',
        'action_display'
    )

    fieldsets = (
        ('Información del Evento', {
            'fields': ('id', 'job', 'action_display', 'timestamp')
        }),
        ('Usuario y IP', {
            'fields': ('user_email_display', 'clientIP')
        }),
        ('Cambios Realizados', {
            'fields': ('changed_fields_display',),
            'classes': ('wide',)
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('wide',)
        }),
    )

    def timestamp_display(self, obj):
        """Muestra la fecha y hora formateada"""
        return obj.timestamp.strftime('%d/%m/%Y %H:%M:%S')
    timestamp_display.short_description = 'Fecha y Hora'

    def job_link(self, obj):
        """Link al trabajo"""
        url = reverse('admin:jobs_job_change', args=[obj.job.id])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.job.title[:40]
        )
    job_link.short_description = 'Trabajo'

    def action_badge(self, obj):
        """Badge con el tipo de acción"""
        action_colors = {
            'created': '#10B981',        # Verde
            'updated': '#3B82F6',        # Azul
            'activated': '#059669',      # Verde oscuro
            'deactivated': '#DC2626',    # Rojo
            'duplicated': '#F59E0B',     # Naranja
            'deleted': '#7C2D12',        # Marrón
            'payment_verified': '#10B981', # Verde
            'payment_rejected': '#DC2626',  # Rojo
        }
        color = action_colors.get(obj.action, '#6B7280')

        return format_html(
            '<span style="background-color: {}; color: white; padding: 6px 14px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block;">{}</span>',
            color, obj.get_action_display()
        )
    action_badge.short_description = 'Acción'

    def user_display(self, obj):
        """Muestra el email del usuario"""
        return obj.userEmail or 'Sistema'
    user_display.short_description = 'Usuario'

    def client_ip_display(self, obj):
        """Muestra la IP del cliente"""
        return obj.clientIP or 'N/A'
    client_ip_display.short_description = 'IP Cliente'

    def user_email_display(self, obj):
        """Display del email del usuario"""
        return obj.userEmail or 'No registrado'
    user_email_display.short_description = 'Email del Usuario'

    def action_display(self, obj):
        """Display amigable de la acción"""
        return obj.get_action_display()
    action_display.short_description = 'Tipo de Acción'

    def changed_fields_display(self, obj):
        """Muestra los cambios realizados de forma legible"""
        if not obj.changedFields:
            return 'Sin cambios específicos'

        html_content = '<div style="background-color: #F3F4F6; padding: 12px; border-radius: 8px; font-family: monospace; font-size: 13px;">'

        for field, changes in obj.changedFields.items():
            if isinstance(changes, dict) and 'before' in changes and 'after' in changes:
                before = changes['before']
                after = changes['after']
                html_content += f'<div style="margin-bottom: 10px; padding: 8px; background-color: white; border-radius: 4px; border-left: 3px solid #3B82F6;">'
                html_content += f'<strong style="color: #1F2937;">{field}:</strong><br>'
                html_content += f'<span style="color: #7C3AED;">❌ Antes:</span> <code style="background: #F9FAFB; padding: 2px 4px; border-radius: 3px; color: #1F2937;">{before}</code><br>'
                html_content += f'<span style="color: #059669;">✅ Después:</span> <code style="background: #F9FAFB; padding: 2px 4px; border-radius: 3px; color: #1F2937;">{after}</code>'
                html_content += '</div>'

        html_content += '</div>'
        return format_html(html_content)
    changed_fields_display.short_description = 'Campos Modificados'

    # No permitir editar registros de auditoría
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PlanOrder)
class PlanOrderAdmin(admin.ModelAdmin):
    """Admin para gestionar órdenes de planes"""

    list_display = (
        'invoice_number_display',
        'razon_social_display',
        'plan_link',
        'amount_display',
        'status_badge',
        'order_date_display',
        'invoice_sent_status'
    )

    list_filter = (
        'status',
        'order_date',
        'plan__name',
        'electronic_invoice_sent_date',
    )

    search_fields = (
        'invoice_number',
        'razon_social',
        'nit',
        'ci',
        'user__email',
        'plan__label'
    )

    readonly_fields = (
        'id',
        'order_date',
        'created_at',
        'updated_at',
        'company_data_display',
    )

    fieldsets = (
        ('Información General', {
            'fields': ('id', 'user', 'plan', 'order_date')
        }),
        ('Datos de Factura', {
            'fields': ('invoice_number', 'razon_social', 'nit', 'ci')
        }),
        ('Información de Pago', {
            'fields': ('amount_paid', 'payment_proof', 'status')
        }),
        ('Factura Electrónica', {
            'fields': ('electronic_invoice_email', 'electronic_invoice_whatsapp', 'electronic_invoice_sent_date')
        }),
        ('Datos de la Empresa', {
            'fields': ('company_data_display',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def invoice_number_display(self, obj):
        """Muestra el número de factura"""
        return f"#{obj.invoice_number}"
    invoice_number_display.short_description = 'Factura'

    def razon_social_display(self, obj):
        """Muestra la razón social de la empresa"""
        return obj.razon_social
    razon_social_display.short_description = 'Razón Social'

    def plan_link(self, obj):
        """Link al plan"""
        return obj.plan.label
    plan_link.short_description = 'Plan'

    def amount_display(self, obj):
        """Muestra el monto pagado formateado"""
        return format_html(
            '<span style="color: #7C3AED; font-weight: bold;">Bs {}</span>',
            f'{obj.amount_paid:.2f}'
        )
    amount_display.short_description = 'Monto'

    def status_badge(self, obj):
        """Badge del estado de la orden"""
        status_colors = {
            'PENDING': '#F59E0B',
            'PAID': '#3B82F6',
            'INVOICE_SENT': '#8B5CF6',
            'COMPLETED': '#10B981',
        }
        status_labels = {
            'PENDING': 'Pendiente',
            'PAID': 'Pagado',
            'INVOICE_SENT': 'Factura Enviada',
            'COMPLETED': 'Completado',
        }
        color = status_colors.get(obj.status, '#6B7280')
        label = status_labels.get(obj.status, obj.status)

        return format_html(
            '<span style="background-color: {}; color: white; padding: 6px 14px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Estado'

    def order_date_display(self, obj):
        """Muestra la fecha de la orden"""
        return obj.order_date.strftime('%d/%m/%Y %H:%M')
    order_date_display.short_description = 'Fecha'

    def invoice_sent_status(self, obj):
        """Indica si la factura fue enviada"""
        if obj.electronic_invoice_sent_date:
            return format_html(
                '<span style="color: #10B981; font-weight: bold;">✓ Enviada</span>'
            )
        return format_html(
            '<span style="color: #999; font-weight: bold;">⏳ Pendiente</span>'
        )
    invoice_sent_status.short_description = 'Factura'

    def company_data_display(self, obj):
        """Muestra los datos de la empresa en JSON"""
        if not obj.company_data:
            return 'Sin datos'
        return format_html(
            '<pre style="background-color: #F3F4F6; padding: 12px; border-radius: 6px; '
            'overflow: auto; max-height: 300px;">{}</pre>',
            json.dumps(obj.company_data, ensure_ascii=False, indent=2)
        )
    company_data_display.short_description = 'Datos de la Empresa'


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    """Admin para gestionar usuarios bloqueados"""

    list_display = (
        'company_display',
        'blocked_user_display',
        'reason_badge',
        'blocked_at_display',
        'duration_display'
    )

    list_filter = (
        'reason',
        'blocked_at',
        'is_permanent',
    )

    search_fields = (
        'company__email',
        'blocked_user__email',
        'blocked_user__first_name',
        'blocked_user__last_name',
    )

    readonly_fields = (
        'blocked_at',
        'blocked_user_info_display',
    )

    fieldsets = (
        ('Empresa y Usuario', {
            'fields': ('company', 'blocked_user', 'blocked_user_info_display')
        }),
        ('Motivo del Bloqueo', {
            'fields': ('reason', 'reason_notes')
        }),
        ('Información de Bloqueo', {
            'fields': ('is_permanent', 'blocked_at', 'blocked_until')
        }),
    )

    def company_display(self, obj):
        """Muestra la empresa que bloquea"""
        return obj.company.email
    company_display.short_description = 'Empresa'

    def blocked_user_display(self, obj):
        """Muestra el usuario bloqueado"""
        name = f"{obj.blocked_user.first_name} {obj.blocked_user.last_name}".strip()
        if not name:
            name = obj.blocked_user.email
        return name
    blocked_user_display.short_description = 'Usuario Bloqueado'

    def reason_badge(self, obj):
        """Badge del motivo del bloqueo"""
        reason_colors = {
            'SPAM': '#DC2626',
            'UNQUALIFIED': '#F59E0B',
            'OTHER': '#6B7280',
        }
        reason_labels = {
            'SPAM': 'Spam',
            'UNQUALIFIED': 'No Calificado',
            'OTHER': 'Otro',
        }
        color = reason_colors.get(obj.reason, '#6B7280')
        label = reason_labels.get(obj.reason, obj.reason)

        return format_html(
            '<span style="background-color: {}; color: white; padding: 6px 14px; '
            'border-radius: 20px; font-weight: bold; font-size: 12px; '
            'display: inline-block;">{}</span>',
            color, label
        )
    reason_badge.short_description = 'Razón'

    def blocked_at_display(self, obj):
        """Muestra la fecha de bloqueo"""
        return obj.blocked_at.strftime('%d/%m/%Y %H:%M')
    blocked_at_display.short_description = 'Bloqueado el'

    def duration_display(self, obj):
        """Muestra si es permanente o temporal"""
        if obj.is_permanent:
            return format_html(
                '<span style="color: #DC2626; font-weight: bold;">∞ Permanente</span>'
            )
        else:
            if obj.blocked_until:
                return format_html(
                    '<span style="color: #F59E0B; font-weight: bold;">⏰ Hasta {}</span>',
                    obj.blocked_until.strftime('%d/%m/%Y')
                )
        return 'No especificado'
    duration_display.short_description = 'Duración'

    def blocked_user_info_display(self, obj):
        """Muestra información completa del usuario bloqueado"""
        html_content = (
            '<div style="background-color: #F3F4F6; padding: 12px; border-radius: 8px; '
            'font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto; font-size: 13px;">'
        )

        # Email
        html_content += (
            '<p style="margin: 0 0 8px 0; display: flex; align-items: center;">'
            '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">✉️</span>'
            f'<span style="color: #374151;">{obj.blocked_user.email}</span>'
            '</p>'
        )

        # Nombre completo
        if obj.blocked_user.first_name or obj.blocked_user.last_name:
            full_name = f"{obj.blocked_user.first_name} {obj.blocked_user.last_name}".strip()
            html_content += (
                '<p style="margin: 0 0 8px 0; display: flex; align-items: center;">'
                '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">👤</span>'
                f'<span style="color: #374151;">{full_name}</span>'
                '</p>'
            )

        # Role
        html_content += (
            '<p style="margin: 0; display: flex; align-items: center;">'
            '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">🔖</span>'
            f'<span style="color: #374151;">{obj.blocked_user.role}</span>'
            '</p>'
        )

        html_content += '</div>'
        return format_html(html_content)
    blocked_user_info_display.short_description = 'Información del Usuario'
