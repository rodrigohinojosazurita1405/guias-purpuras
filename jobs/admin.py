from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'companyName', 'city', 'contractType', 'status', 'views', 'applications', 'createdAt')
    list_filter = ('status', 'city', 'contractType', 'createdAt')
    search_fields = ('title', 'companyName', 'description')
    readonly_fields = ('id', 'views', 'applications', 'createdAt', 'updatedAt')

    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'title', 'companyName', 'companyAnonymous', 'description')
        }),
        ('Clasificación', {
            'fields': ('jobCategory', 'city', 'subcategory', 'contractType')
        }),
        ('Requisitos', {
            'fields': ('requirements', 'responsibilities', 'education', 'experience', 'languages', 'technicalSkills')
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
        ('Timestamps', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )
