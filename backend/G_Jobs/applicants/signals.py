from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import JobApplication, ApplicantCV, SavedJob
from G_Jobs.audit.models import AuditLog


@receiver(post_save, sender=JobApplication)
def log_application_changes(sender, instance, created, **kwargs):
    """Registrar cambios en postulaciones"""
    if created:
        action = 'create'
        description = f'Nueva postulación de {instance.applicant.email} para {instance.job.title}'
    else:
        action = 'update'
        description = f'Actualización de postulación - Nuevo estado: {instance.status}'

    AuditLog.log_action(
        user=instance.applicant,
        obj=instance,
        action=action,
        description=description,
        severity='info'
    )


@receiver(post_save, sender=ApplicantCV)
def log_cv_changes(sender, instance, created, **kwargs):
    """Registrar cambios en CVs"""
    if instance.is_deleted:
        return  # No registrar cambios en CVs eliminados

    if created:
        action = 'create'
        description = f'Nuevo CV creado: {instance.name} ({instance.cv_type})'
    else:
        action = 'update'
        description = f'CV actualizado: {instance.name}'

    AuditLog.log_action(
        user=instance.applicant,
        obj=instance,
        action=action,
        description=description,
        severity='info'
    )


@receiver(post_delete, sender=ApplicantCV)
def log_cv_deletion(sender, instance, **kwargs):
    """Registrar eliminación de CVs"""
    AuditLog.log_action(
        user=instance.applicant,
        obj=instance,
        action='delete',
        description=f'CV eliminado: {instance.name}',
        severity='warning'
    )


@receiver(post_save, sender=SavedJob)
def log_job_saved(sender, instance, created, **kwargs):
    """Registrar trabajos guardados"""
    if created:
        AuditLog.log_action(
            user=instance.user,
            obj=instance,
            action='create',
            description=f'Trabajo guardado: {instance.job.title}',
            severity='info'
        )


@receiver(post_delete, sender=SavedJob)
def log_job_unsaved(sender, instance, **kwargs):
    """Registrar trabajos eliminados de guardados"""
    AuditLog.log_action(
        user=instance.user,
        obj=instance,
        action='delete',
        description=f'Trabajo removido de guardados: {instance.job.title}',
        severity='info'
    )
