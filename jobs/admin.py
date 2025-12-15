from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Job
from catalogs.models import JobCategory, ContractType, City
from payments.models import PlanOrder
from moderation.models import BlockedUser
from auth_api.models import CustomUser
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
        'isDeleted',
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
        'reject_payment_action',
        'delete_jobs_with_audit'
    ]

    fieldsets = (
        ('Verificación de Pago', {
            'fields': ('proofOfPayment', 'proof_of_payment_preview', 'payment_verification_summary', 'paymentVerified', 'paymentVerifiedBy', 'paymentVerificationDate', 'paymentVerificationNotes'),
            'classes': ('wide',),
            'description': 'Gestión de comprobantes y verificación de pagos. Solo administradores pueden aprobar pagos.'
        }),
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
            'fields': ('email',)
        }),
        ('Tipo de Aplicación', {
            'fields': ('applicationType', 'externalApplicationUrl', 'screeningQuestions')
        }),
        ('Plan y Estado', {
            'fields': ('selectedPlan', 'status', 'views')
        }),
        ('Timestamps', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Personalizar el queryset del campo paymentVerifiedBy
        para mostrar solo superadmins
        """
        if db_field.name == 'paymentVerifiedBy':
            kwargs['queryset'] = CustomUser.objects.filter(is_superuser=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        """
        Por defecto, mostrar solo trabajos NO eliminados
        El admin puede usar el filtro para ver los eliminados
        """
        qs = super().get_queryset(request)
        # Si no hay filtro específico de isDeleted, mostrar solo no eliminados
        if 'isDeleted__exact' not in request.GET:
            return qs.filter(isDeleted=False)
        return qs

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
        """Badge de estado con colores tenues y sutiles"""
        # Colores tenues con backgrounds claros y texto oscuro
        status_styles = {
            'pending': {'bg': '#FEF3C7', 'color': '#92400E'},    # Amarillo tenue
            'active': {'bg': '#D1FAE5', 'color': '#065F46'},     # Verde tenue
            'closed': {'bg': '#FEE2E2', 'color': '#991B1B'},     # Rojo tenue
            'draft': {'bg': '#E5E7EB', 'color': '#374151'}       # Gris tenue
        }
        status_labels = {
            'pending': 'Pendiente',
            'active': 'Activa',
            'closed': 'Cerrada',
            'draft': 'Borrador'
        }
        style = status_styles.get(obj.status, status_styles['draft'])
        label = status_labels.get(obj.status, obj.status.capitalize())

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 10px; '
            'border-radius: 6px; font-weight: 600; font-size: 11px; '
            'display: inline-block;">{}</span>',
            style['bg'], style['color'], label
        )
    status_badge.short_description = 'Estado'

    def payment_badge(self, obj):
        """Badge de estado de pago con colores tenues"""
        if obj.paymentVerified:
            style = {'bg': '#D1FAE5', 'color': '#065F46'}  # Verde tenue
            label = 'Verificado'
        elif obj.proofOfPayment:
            style = {'bg': '#FEF3C7', 'color': '#92400E'}  # Amarillo tenue
            label = 'Pendiente'
        else:
            style = {'bg': '#FEE2E2', 'color': '#991B1B'}  # Rojo tenue
            label = 'Sin pago'

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 10px; '
            'border-radius: 6px; font-weight: 600; font-size: 11px; '
            'display: inline-block;">{}</span>',
            style['bg'], style['color'], label
        )
    payment_badge.short_description = 'Estado Pago'

    def applications_count(self, obj):
        """Muestra el contador de aplicaciones con estilo tenue"""
        count = obj.applications
        return format_html(
            '<span style="background-color: #F3E8FF; color: #6B21A8; padding: 3px 10px; '
            'border-radius: 6px; font-weight: 600; font-size: 11px; '
            'display: inline-block;">👥 {}</span>',
            count
        )
    applications_count.short_description = 'Aplicaciones'

    def views_count(self, obj):
        """Muestra el contador de vistas con estilo tenue"""
        count = obj.views
        return format_html(
            '<span style="background-color: #DBEAFE; color: #1E3A8A; padding: 3px 10px; '
            'border-radius: 6px; font-weight: 600; font-size: 11px; '
            'display: inline-block;">👁️ {}</span>',
            count
        )
    views_count.short_description = 'Vistas'

    def created_date_display(self, obj):
        """Muestra la fecha de creación con estilo tenue"""
        return format_html(
            '<span style="background-color: #D1FAE5; color: #065F46; padding: 3px 10px; '
            'border-radius: 6px; font-weight: 600; font-size: 11px; '
            'display: inline-block;">📅 {}</span>',
            obj.createdAt.strftime('%d/%m/%Y')
        )
    created_date_display.short_description = 'Publicado'

    def plan_display(self, obj):
        """Muestra el plan seleccionado con colores tenues"""
        from plans.models import Plan

        # Colores tenues para cada plan
        plan_colors = {
            'escencial': {'color': '#1E3A8A', 'bg': '#DBEAFE'},  # Azul tenue
            'purpura': {'color': '#6B21A8', 'bg': '#F3E8FF'},     # Púrpura tenue
            'impulso': {'color': '#BE185D', 'bg': '#FCE7F3'}      # Rosa tenue
        }

        # Obtener datos del plan desde BD
        try:
            plan_obj = Plan.objects.get(name=obj.selectedPlan)
            label = plan_obj.label
            duration = f"{plan_obj.duration_days}d"
            colors = plan_colors.get(obj.selectedPlan, plan_colors['escencial'])
        except Plan.DoesNotExist:
            # Fallback si el plan no existe en BD
            label = obj.selectedPlan.capitalize()
            duration = "N/A"
            colors = plan_colors.get(obj.selectedPlan, plan_colors['escencial'])

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 10px; '
            'border-radius: 6px; font-weight: 600; font-size: 11px; '
            'display: inline-block;">💎 {} ({})</span>',
            colors['bg'], colors['color'], label, duration
        )
    plan_display.short_description = 'Plan'

    def expiry_countdown(self, obj):
        """Muestra días restantes y fecha exacta de vencimiento con colores tenues según urgencia"""
        from datetime import date, timedelta

        today = date.today()
        days_remaining = (obj.expiryDate - today).days
        expiry_date_str = obj.expiryDate.strftime('%d/%m/%Y')

        # Determinar color según urgencia (colores tenues)
        if days_remaining < 0:
            color = '#991B1B'      # Rojo oscuro
            bg_color = '#FEE2E2'   # Rojo tenue
            status = f'Expirado ({expiry_date_str})'
            icon = '✗'
        elif days_remaining == 0:
            color = '#991B1B'
            bg_color = '#FEE2E2'
            status = f'Hoy ({expiry_date_str})'
            icon = '⚠️'
        elif days_remaining <= 3:
            color = '#991B1B'
            bg_color = '#FEE2E2'
            status = f'{days_remaining}d ({expiry_date_str})'
            icon = '🔴'
        elif days_remaining <= 7:
            color = '#92400E'      # Amarillo oscuro
            bg_color = '#FEF3C7'   # Amarillo tenue
            status = f'{days_remaining}d ({expiry_date_str})'
            icon = '🟡'
        elif days_remaining <= 14:
            color = '#92400E'
            bg_color = '#FEF3C7'
            status = f'{days_remaining}d ({expiry_date_str})'
            icon = '🟡'
        else:
            color = '#065F46'      # Verde oscuro
            bg_color = '#D1FAE5'   # Verde tenue
            status = f'{days_remaining}d ({expiry_date_str})'
            icon = '🟢'

        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 10px; '
            'border-radius: 6px; font-weight: 600; font-size: 11px; '
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
            status_label = 'Verificado'
            status_icon = '✓'
            status_color = '#059669'
        else:
            bg_color = '#FFFBEB'
            border_color = '#F59E0B'
            text_color = '#78350F'
            status_label = 'Pendiente'
            status_icon = '⏳'
            status_color = '#F59E0B'

        # Mostrar nombre completo del admin, si no tiene nombre mostrar username
        if obj.paymentVerifiedBy:
            full_name = f"{obj.paymentVerifiedBy.first_name} {obj.paymentVerifiedBy.last_name}".strip()
            verified_by = full_name if full_name else obj.paymentVerifiedBy.username
        else:
            verified_by = 'Sin verificar'
        date_str = obj.paymentVerificationDate.strftime("%d/%m/%Y %H:%M") if obj.paymentVerificationDate else 'N/A'
        notes = obj.paymentVerificationNotes or '(Sin notas)'

        html_content = (
            f'<div style="background-color: {bg_color}; padding: 14px; border-radius: 6px; '
            f'border-left: 4px solid {border_color}; color: {text_color}; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto;">'
            f'<p style="margin: 0 0 8px 0; font-weight: bold; font-size: 14px;">'
            f'<span style="color: {status_color}; font-size: 14px; margin-right: 6px;">'
            f'{status_icon}</span>{status_label}</p>'
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
        updated = 0
        for job in queryset:
            job.status = 'active'
            job._audit_user = request.user
            job._audit_request = request
            job.save()
            updated += 1
        self.message_user(request, f'{updated} anuncios marcados como ACTIVOS')
    mark_as_active.short_description = 'Marcar como ACTIVA'

    def mark_as_closed(self, request, queryset):
        """Acción: Marcar como cerrada"""
        updated = 0
        for job in queryset:
            job.status = 'closed'
            job._audit_user = request.user
            job._audit_request = request
            job.save()
            updated += 1
        self.message_user(request, f'{updated} anuncios marcados como CERRADOS')
    mark_as_closed.short_description = 'Marcar como CERRADA'

    def verify_payment_action(self, request, queryset):
        """Acción: Verificar pago y activar anuncio automáticamente"""
        updated = 0
        for job in queryset:
            job.paymentVerified = True
            job.paymentVerifiedBy = request.user
            job.paymentVerificationDate = datetime.now()
            job.status = 'active'
            job._audit_user = request.user
            job._audit_request = request
            job.save()
            updated += 1
        from django.contrib.admin import messages as admin_messages
        self.message_user(request, f'✓ {updated} pago(s) VERIFICADO(s) y anuncio(s) ACTIVADO(s) exitosamente', admin_messages.SUCCESS)
    verify_payment_action.short_description = '✓ VERIFICAR pagos y ACTIVAR anuncios'

    def reject_payment_action(self, request, queryset):
        """Acción: Rechazar pago"""
        updated = 0
        for job in queryset:
            job.paymentVerified = False
            job.paymentVerifiedBy = None
            job.paymentVerificationDate = None
            job._audit_user = request.user
            job._audit_request = request
            job.save()
            updated += 1
        from django.contrib.admin import messages as admin_messages
        self.message_user(request, f'✗ {updated} pago(s) RECHAZADO(s)', admin_messages.WARNING)
    reject_payment_action.short_description = '✗ RECHAZAR pagos seleccionados'

    def delete_jobs_with_audit(self, request, queryset):
        """Acción: Eliminar ofertas de trabajo con registro de auditoría"""
        count = queryset.count()

        for job in queryset:
            # Crear log de auditoría antes de eliminar
            JobAuditLog.objects.create(
                job=job,
                action='deleted',
                userEmail=request.user.email,
                notes=f'Oferta de trabajo eliminada desde panel de administración por {request.user.email}'
            )
            # Eliminar la oferta
            job.delete()

        from django.contrib.admin import messages as admin_messages
        self.message_user(request, f'✓ {count} oferta(s) de trabajo ELIMINADA(s) con registro de auditoría', admin_messages.SUCCESS)
    delete_jobs_with_audit.short_description = '🗑️ Eliminar ofertas (con auditoría)'


# @admin.register(Application)
# class ApplicationAdmin(admin.ModelAdmin):
#     """Admin personalizado para gestionar aplicaciones de candidatos"""
# 
#     list_display = (
#         'candidate_name_display',
#         'job_title_link',
#         'candidate_email',
#         'status_badge',
#         'application_date',
#         'screening_answers_preview'
#     )
# 
#     list_filter = (
#         'status',
#         'createdAt',
#         'job__city',
#     )
# 
#     search_fields = (
#         'applicantName',
#         'applicantEmail',
#         'job__title',
#         'id'
#     )
# 
#     readonly_fields = (
#         'id',
#         'job',
#         'createdAt',
#         'updatedAt',
#         'screening_answers_display',
#         'candidate_contact_display'
#     )
# 
#     actions = [
#         'mark_as_reviewing',
#         'mark_as_shortlisted',
#         'mark_as_rejected',
#         'mark_as_accepted'
#     ]
# 
#     fieldsets = (
#         ('Información del Candidato', {
#             'fields': ('id', 'applicantName', 'applicantEmail', 'applicantPhone', 'applicantWhatsapp', 'candidate_contact_display')
#         }),
#         ('Oferta de Trabajo', {
#             'fields': ('job',)
#         }),
#         ('Respuestas de Screening', {
#             'fields': ('screening_answers_display',),
#             'classes': ('wide',)
#         }),
#         ('Evaluación', {
#             'fields': ('status', 'recruiterNotes')
#         }),
#         ('Timestamps', {
#             'fields': ('createdAt', 'updatedAt'),
#             'classes': ('collapse',)
#         }),
#     )
# 
#     # ========== MÉTODOS DE DISPLAY ==========
# 
#     def candidate_name_display(self, obj):
#         """Muestra el nombre del candidato"""
#         return obj.applicantName
#     candidate_name_display.short_description = 'Candidato'
# 
#     def job_title_link(self, obj):
#         """Link al trabajo con título"""
#         url = reverse('admin:jobs_job_change', args=[obj.job.id])
#         return format_html(
#             '<a href="{}">{}</a>',
#             url,
#             obj.job.title[:40]
#         )
#     job_title_link.short_description = 'Oferta'
# 
#     def candidate_email(self, obj):
#         """Email del candidato"""
#         return obj.applicantEmail
#     candidate_email.short_description = 'Email'
# 
#     def status_badge(self, obj):
#         """Badge con estado de la aplicación con colores sobrios"""
#         status_colors = {
#             'received': '#3B82F6',        # Azul
#             'reviewing': '#F59E0B',       # Naranja
#             'shortlisted': '#10B981',     # Verde
#             'rejected': '#DC2626',        # Rojo
#             'accepted': '#059669',        # Verde oscuro
#             'withdrawn': '#6B7280'        # Gris
#         }
#         labels = {
#             'received': 'RECIBIDA',
#             'reviewing': 'EN REVISIÓN',
#             'shortlisted': 'PRESELECCIONADA',
#             'rejected': 'RECHAZADA',
#             'accepted': 'ACEPTADA',
#             'withdrawn': 'RETIRADA'
#         }
#         color = status_colors.get(obj.status, '#6B7280')
#         label = labels.get(obj.status, obj.status.upper())
# 
#         return format_html(
#             '<span style="background-color: {}; color: white; padding: 6px 14px; '
#             'border-radius: 20px; font-weight: bold; font-size: 12px; '
#             'display: inline-block;">{}</span>',
#             color, label
#         )
#     status_badge.short_description = 'Estado'
# 
#     def application_date(self, obj):
#         """Fecha de aplicación"""
#         return obj.createdAt.strftime('%d/%m/%Y %H:%M')
#     application_date.short_description = 'Fecha'
# 
#     def screening_answers_preview(self, obj):
#         """Preview de respuestas de screening"""
#         if not obj.screeningAnswers:
#             return 'Sin respuestas'
# 
#         count = len(obj.screeningAnswers)
#         return f'{count} respuestas'
#     screening_answers_preview.short_description = 'Respuestas'
# 
#     def screening_answers_display(self, obj):
#         """Muestra todas las respuestas de screening de forma legible"""
#         if not obj.screeningAnswers:
#             return 'Sin respuestas de screening'
# 
#         result = 'Respuestas de Screening:\n'
#         for idx, (key, answer) in enumerate(obj.screeningAnswers.items()):
#             result += f'\nPregunta {int(key) + 1}:\n'
# 
#             # Obtener la pregunta original del job
#             job = obj.job
#             if job.screeningQuestions and int(key) < len(job.screeningQuestions):
#                 question = job.screeningQuestions[int(key)]
#                 result += f'{question.get("text", "Pregunta no disponible")}\n'
# 
#             result += f'Respuesta: {answer}\n'
# 
#         return result
#     screening_answers_display.short_description = 'Respuestas de Screening'
# 
#     def candidate_contact_display(self, obj):
#         """Muestra información de contacto del candidato con estilos"""
#         html_content = (
#             '<div style="background-color: #F3F4F6; padding: 12px; border-radius: 8px; '
#             'font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto; font-size: 13px;">'
#         )
# 
#         # Email
#         if obj.applicantEmail:
#             html_content += (
#                 '<p style="margin: 0 0 8px 0; display: flex; align-items: center;">'
#                 '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">✉️</span>'
#                 f'<span style="color: #374151;">{obj.applicantEmail}</span>'
#                 '</p>'
#             )
# 
#         # Teléfono
#         if obj.applicantPhone:
#             html_content += (
#                 '<p style="margin: 0 0 8px 0; display: flex; align-items: center;">'
#                 '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">☎️</span>'
#                 f'<span style="color: #374151;">{obj.applicantPhone}</span>'
#                 '</p>'
#             )
# 
#         # WhatsApp
#         if obj.applicantWhatsapp:
#             html_content += (
#                 '<p style="margin: 0; display: flex; align-items: center;">'
#                 '<span style="color: #1F2937; font-weight: 600; margin-right: 8px;">💬</span>'
#                 f'<span style="color: #374151;">{obj.applicantWhatsapp}</span>'
#                 '</p>'
#             )
# 
#         html_content += '</div>'
#         return format_html(html_content)
#     candidate_contact_display.short_description = 'Información de Contacto'
# 
#     # ========== ACCIONES PERSONALIZADAS ==========
# 
#     def mark_as_reviewing(self, request, queryset):
#         """Cambiar estado a EN REVISIÓN"""
#         updated = queryset.update(status='reviewing')
#         self.message_user(request, f'{updated} aplicaciones marcadas como EN REVISIÓN')
#     mark_as_reviewing.short_description = 'Marcar como EN REVISIÓN'
# 
#     def mark_as_shortlisted(self, request, queryset):
#         """Cambiar estado a PRESELECCIONADA"""
#         updated = queryset.update(status='shortlisted')
#         self.message_user(request, f'{updated} aplicaciones PRESELECCIONADAS')
#     mark_as_shortlisted.short_description = 'Marcar como PRESELECCIONADA'
# 
#     def mark_as_rejected(self, request, queryset):
#         """Cambiar estado a RECHAZADA"""
#         updated = queryset.update(status='rejected')
#         self.message_user(request, f'{updated} aplicaciones RECHAZADAS')
#     mark_as_rejected.short_description = 'Marcar como RECHAZADA'
# 
#     def mark_as_accepted(self, request, queryset):
#         """Cambiar estado a ACEPTADA"""
#         updated = queryset.update(status='accepted')
#         self.message_user(request, f'{updated} aplicaciones ACEPTADAS')
#     mark_as_accepted.short_description = 'Marcar como ACEPTADA'
# 
# 
# @admin.register(JobAuditLog)
# class JobAuditLogAdmin(admin.ModelAdmin):
#     """Admin para auditoría de cambios en trabajos"""
# 
#     list_display = (
#         'timestamp_display',
#         'job_link',
#         'action_badge',
#         'user_display',
#         'client_ip_display'
#     )
# 
#     list_filter = (
#         'action',
#         'timestamp',
#         'userEmail',
#     )
# 
#     search_fields = (
#         'job__title',
#         'job__id',
#         'userEmail',
#         'clientIP',
#         'notes'
#     )
# 
#     readonly_fields = (
#         'id',
#         'job',
#         'timestamp',
#         'changed_fields_display',
#         'user_email_display',
#         'action_display'
#     )
# 
#     fieldsets = (
#         ('Información del Evento', {
#             'fields': ('id', 'job', 'action_display', 'timestamp')
#         }),
#         ('Usuario y IP', {
#             'fields': ('user_email_display', 'clientIP')
#         }),
#         ('Cambios Realizados', {
#             'fields': ('changed_fields_display',),
#             'classes': ('wide',)
#         }),
#         ('Notas', {
#             'fields': ('notes',),
#             'classes': ('wide',)
#         }),
#     )
# 
#     def timestamp_display(self, obj):
#         """Muestra la fecha y hora formateada"""
#         return obj.timestamp.strftime('%d/%m/%Y %H:%M:%S')
#     timestamp_display.short_description = 'Fecha y Hora'
# 
#     def job_link(self, obj):
#         """Link al trabajo"""
#         # Si el trabajo fue eliminado, job será None
#         if obj.job is None:
#             return format_html(
#                 '<span style="color: #999; font-style: italic;">[Trabajo Eliminado]</span>'
#             )
# 
#         url = reverse('admin:jobs_job_change', args=[obj.job.id])
#         return format_html(
#             '<a href="{}">{}</a>',
#             url,
#             obj.job.title[:40]
#         )
#     job_link.short_description = 'Trabajo'
# 
#     def action_badge(self, obj):
#         """Badge con el tipo de acción"""
#         action_colors = {
#             'created': '#10B981',        # Verde
#             'updated': '#3B82F6',        # Azul
#             'activated': '#059669',      # Verde oscuro
#             'deactivated': '#DC2626',    # Rojo
#             'duplicated': '#F59E0B',     # Naranja
#             'deleted': '#7C2D12',        # Marrón
#             'payment_verified': '#10B981', # Verde
#             'payment_rejected': '#DC2626',  # Rojo
#         }
#         color = action_colors.get(obj.action, '#6B7280')
# 
#         return format_html(
#             '<span style="background-color: {}; color: white; padding: 6px 14px; '
#             'border-radius: 20px; font-weight: bold; font-size: 12px; '
#             'display: inline-block;">{}</span>',
#             color, obj.get_action_display()
#         )
#     action_badge.short_description = 'Acción'
# 
#     def user_display(self, obj):
#         """Muestra el email del usuario"""
#         return obj.userEmail or 'Sistema'
#     user_display.short_description = 'Usuario'
# 
#     def client_ip_display(self, obj):
#         """Muestra la IP del cliente"""
#         return obj.clientIP or 'N/A'
#     client_ip_display.short_description = 'IP Cliente'
# 
#     def user_email_display(self, obj):
#         """Display del email del usuario"""
#         return obj.userEmail or 'No registrado'
#     user_email_display.short_description = 'Email del Usuario'
# 
#     def action_display(self, obj):
#         """Display amigable de la acción"""
#         return obj.get_action_display()
#     action_display.short_description = 'Tipo de Acción'
# 
#     def changed_fields_display(self, obj):
#         """Muestra los cambios realizados de forma legible"""
#         if not obj.changedFields:
#             return 'Sin cambios específicos'
# 
#         html_content = '<div style="background-color: #F3F4F6; padding: 12px; border-radius: 8px; font-family: monospace; font-size: 13px;">'
# 
#         for field, changes in obj.changedFields.items():
#             if isinstance(changes, dict) and 'before' in changes and 'after' in changes:
#                 before = changes['before']
#                 after = changes['after']
#                 html_content += f'<div style="margin-bottom: 10px; padding: 8px; background-color: white; border-radius: 4px; border-left: 3px solid #3B82F6;">'
#                 html_content += f'<strong style="color: #1F2937;">{field}:</strong><br>'
#                 html_content += f'<span style="color: #7C3AED;">❌ Antes:</span> <code style="background: #F9FAFB; padding: 2px 4px; border-radius: 3px; color: #1F2937;">{before}</code><br>'
#                 html_content += f'<span style="color: #059669;">✅ Después:</span> <code style="background: #F9FAFB; padding: 2px 4px; border-radius: 3px; color: #1F2937;">{after}</code>'
#                 html_content += '</div>'
# 
#         html_content += '</div>'
#         return format_html(html_content)
#     changed_fields_display.short_description = 'Campos Modificados'
# 
#     # No permitir editar registros de auditoría
#     def has_add_permission(self, request):
#         return False
# 
#     def has_delete_permission(self, request, obj=None):
#         return False
# 
#     def has_change_permission(self, request, obj=None):
#         return False
# 
# 
# ============================================================
# NOTA: Los modelos PlanOrder, BlockedUser, JobCategory, ContractType y City
# han sido movidos a sus respectivas apps (payments, moderation, catalogs)
# Sus configuraciones de admin también están ahora en esas apps
# ============================================================
