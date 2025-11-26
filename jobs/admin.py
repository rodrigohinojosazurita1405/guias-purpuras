from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'companyName', 'city', 'status', 'payment_status_display', 'views', 'applications', 'createdAt')
    list_filter = ('status', 'paymentVerified', 'city', 'contractType', 'createdAt')
    search_fields = ('title', 'companyName', 'description')
    readonly_fields = ('id', 'views', 'applications', 'createdAt', 'updatedAt', 'payment_verification_summary')

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

    def payment_status_display(self, obj):
        """Muestra el estado de verificación de pago en la lista"""
        if obj.paymentVerified:
            return '✅ Verificado'
        elif obj.proofOfPayment:
            return '⏳ Pendiente'
        else:
            return '❌ Sin comprobante'
    payment_status_display.short_description = 'Pago'

    def payment_verification_summary(self, obj):
        """Resumen de la verificación de pago"""
        if not obj.proofOfPayment:
            return '⚠️ Sin comprobante de pago'

        summary = f'<strong>Comprobante:</strong> <a href="{obj.proofOfPayment.url}" target="_blank">Ver imagen</a><br>'

        if obj.paymentVerified:
            summary += f'<strong>Estado:</strong> ✅ Aprobado<br>'
            summary += f'<strong>Verificado por:</strong> {obj.paymentVerifiedBy.username if obj.paymentVerifiedBy else "N/A"}<br>'
            summary += f'<strong>Fecha:</strong> {obj.paymentVerificationDate.strftime("%d/%m/%Y %H:%M") if obj.paymentVerificationDate else "N/A"}<br>'
        else:
            summary += f'<strong>Estado:</strong> ⏳ Pendiente de verificación<br>'

        if obj.paymentVerificationNotes:
            summary += f'<strong>Notas:</strong> {obj.paymentVerificationNotes}'

        return summary
    payment_verification_summary.allow_tags = True
    payment_verification_summary.short_description = 'Resumen de Verificación'
