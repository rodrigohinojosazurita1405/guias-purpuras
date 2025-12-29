"""
Señales para generar notificaciones automáticas
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification


# ========== NOTIFICACIONES PARA EMPRESAS ==========

@receiver(post_save, sender='applicants.JobApplication')
def notify_new_application(sender, instance, created, **kwargs):
    """
    Notificar a la empresa cuando reciben una nueva postulación
    """
    if not created:
        return

    try:
        from auth_api.models import CustomUser
        from G_Jobs.jobs.models import Job

        # Obtener el job y la empresa
        job = instance.job
        company_user = CustomUser.objects.filter(email=job.email, role='company').first()

        if not company_user:
            return

        # Obtener nombre del postulante
        applicant_name = f"{instance.user.first_name} {instance.user.last_name}".strip()
        if not applicant_name:
            applicant_name = instance.user.email

        Notification.create_notification(
            user=company_user,
            notification_type='new_application',
            title='Nueva postulación recibida',
            message=f'{applicant_name} se postuló a tu anuncio "{job.title}"',
            metadata={
                'job_id': str(job.id),
                'application_id': str(instance.id),
                'applicant_email': instance.user.email
            }
        )

        print(f'[NOTIFICATION] Nueva postulación: {applicant_name} -> {job.title}')

    except Exception as e:
        print(f'[NOTIFICATION ERROR] Error al crear notificación de nueva postulación: {e}')
        import traceback
        traceback.print_exc()


@receiver(post_save, sender='jobs.Job')
def notify_payment_status(sender, instance, created, **kwargs):
    """
    Notificar a la empresa cuando su pago es verificado o rechazado
    """
    if created:
        return

    try:
        from auth_api.models import CustomUser

        # Obtener cambios del estado anterior
        from G_Jobs.audit.signals import _audit_state
        old_instance = None
        if hasattr(_audit_state, 'job_old_state') and instance.pk in _audit_state.job_old_state:
            old_instance = _audit_state.job_old_state[instance.pk]

        if not old_instance:
            return

        # Detectar cambio en paymentVerified
        old_payment = old_instance.paymentVerified
        new_payment = instance.paymentVerified

        if old_payment == new_payment:
            return

        # Obtener usuario de la empresa
        company_user = CustomUser.objects.filter(email=instance.email, role='company').first()
        if not company_user:
            return

        # Notificación de pago verificado
        if new_payment is True and old_payment is False:
            Notification.create_notification(
                user=company_user,
                notification_type='payment_verified',
                title='Pago verificado',
                message=f'Tu pago para el anuncio "{instance.title}" ha sido verificado exitosamente',
                metadata={
                    'job_id': str(instance.id),
                    'job_title': instance.title
                }
            )
            print(f'[NOTIFICATION] Pago verificado para: {instance.title}')

        # Notificación de pago rechazado
        elif new_payment is False and old_payment is True:
            Notification.create_notification(
                user=company_user,
                notification_type='payment_rejected',
                title='Pago rechazado',
                message=f'Tu pago para el anuncio "{instance.title}" ha sido rechazado. Por favor contacta con soporte.',
                metadata={
                    'job_id': str(instance.id),
                    'job_title': instance.title
                }
            )
            print(f'[NOTIFICATION] Pago rechazado para: {instance.title}')

    except Exception as e:
        print(f'[NOTIFICATION ERROR] Error al crear notificación de pago: {e}')
        import traceback
        traceback.print_exc()


# ========== NOTIFICACIONES PARA POSTULANTES ==========

@receiver(post_save, sender='applicants.JobApplication')
def notify_application_sent(sender, instance, created, **kwargs):
    """
    Notificar al postulante cuando envía una postulación exitosamente
    """
    if not created:
        return

    try:
        job = instance.job

        Notification.create_notification(
            user=instance.user,
            notification_type='application_sent',
            title='Postulación enviada exitosamente',
            message=f'Te has postulado exitosamente a "{job.title}"',
            metadata={
                'job_id': str(job.id),
                'application_id': str(instance.id),
                'job_title': job.title
            }
        )

        print(f'[NOTIFICATION] Postulación enviada: {instance.user.email} -> {job.title}')

    except Exception as e:
        print(f'[NOTIFICATION ERROR] Error al crear notificación de postulación enviada: {e}')
        import traceback
        traceback.print_exc()
