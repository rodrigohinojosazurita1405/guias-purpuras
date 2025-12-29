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


# Signal pre_save propio para capturar el estado ANTES de guardar
from django.db.models.signals import pre_save

@receiver(pre_save, sender='jobs.Job')
def capture_job_state_for_notifications(sender, instance, **kwargs):
    """
    Capturar estado anterior del Job ANTES de guardar
    Este signal se ejecuta ANTES que el post_save
    """
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            # Guardar en el atributo de la instancia (no en thread-local)
            instance._old_payment_verified = old_instance.paymentVerified
            instance._old_status = old_instance.status
            print(f'[NOTIFICATION PRE_SAVE] Estado capturado: paymentVerified={old_instance.paymentVerified}')
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender='jobs.Job')
def notify_payment_status(sender, instance, created, **kwargs):
    """
    Notificar a la empresa cuando su pago es verificado o rechazado
    """
    print(f'[NOTIFICATION DEBUG] Signal notify_payment_status iniciado')
    print(f'[NOTIFICATION DEBUG] Job: {instance.title}, created={created}')

    if created:
        print(f'[NOTIFICATION DEBUG] Es creación, saltando...')
        return

    try:
        from auth_api.models import CustomUser

        # Obtener estado anterior desde el atributo de la instancia
        if not hasattr(instance, '_old_payment_verified'):
            print(f'[NOTIFICATION DEBUG] No hay estado anterior capturado, saltando...')
            return

        old_payment = instance._old_payment_verified
        new_payment = instance.paymentVerified

        print(f'[NOTIFICATION DEBUG] old_payment={old_payment}, new_payment={new_payment}')

        if old_payment == new_payment:
            print(f'[NOTIFICATION DEBUG] No hay cambio en paymentVerified, saltando...')
            return

        # Obtener usuario de la empresa
        print(f'[NOTIFICATION DEBUG] Buscando usuario de empresa con email={instance.email}')
        company_user = CustomUser.objects.filter(email=instance.email, role='company').first()

        if not company_user:
            print(f'[NOTIFICATION DEBUG] No se encontró usuario de empresa!')
            print(f'[NOTIFICATION DEBUG] Usuarios encontrados con ese email: {CustomUser.objects.filter(email=instance.email).values("email", "role")}')
            return

        print(f'[NOTIFICATION DEBUG] Usuario encontrado: {company_user.email} (role={company_user.role})')

        # Notificación de pago verificado
        if new_payment is True and old_payment is False:
            print(f'[NOTIFICATION DEBUG] Creando notificación de pago verificado...')
            notif = Notification.create_notification(
                user=company_user,
                notification_type='payment_verified',
                title='Pago verificado',
                message=f'Tu pago para el anuncio "{instance.title}" ha sido verificado exitosamente',
                metadata={
                    'job_id': str(instance.id),
                    'job_title': instance.title
                }
            )
            print(f'[NOTIFICATION] Pago verificado para: {instance.title} - Notificacion ID: {notif.id}')

        # Notificación de pago rechazado
        elif new_payment is False and old_payment is True:
            print(f'[NOTIFICATION DEBUG] Creando notificación de pago rechazado...')
            notif = Notification.create_notification(
                user=company_user,
                notification_type='payment_rejected',
                title='Pago rechazado',
                message=f'Tu pago para el anuncio "{instance.title}" ha sido rechazado. Por favor contacta con soporte.',
                metadata={
                    'job_id': str(instance.id),
                    'job_title': instance.title
                }
            )
            print(f'[NOTIFICATION] Pago rechazado para: {instance.title} - Notificacion ID: {notif.id}')

    except Exception as e:
        print(f'[NOTIFICATION ERROR] Error al crear notificación de pago: {e}')
        import traceback
        traceback.print_exc()


@receiver(post_save, sender='jobs.Job')
def notify_saved_job_closed(sender, instance, created, **kwargs):
    """
    Notificar a postulantes cuando un trabajo que guardaron es cerrado
    """
    if created:
        return

    try:
        # Obtener estado anterior desde el atributo de la instancia
        if not hasattr(instance, '_old_status'):
            return

        # Detectar si el trabajo cambió a cerrado
        old_status = instance._old_status
        new_status = instance.status

        if new_status != 'closed' or old_status == 'closed':
            return

        # Obtener todos los usuarios que guardaron este trabajo
        from G_Jobs.applicants.models import SavedJob

        saved_jobs = SavedJob.objects.filter(job=instance).select_related('user')

        for saved_job in saved_jobs:
            Notification.create_notification(
                user=saved_job.user,
                notification_type='saved_job_closed',
                title='Trabajo guardado cerrado',
                message=f'El trabajo "{instance.title}" que guardaste ha sido cerrado',
                metadata={
                    'job_id': str(instance.id),
                    'job_title': instance.title
                }
            )

        if saved_jobs.exists():
            print(f'[NOTIFICATION] Trabajo cerrado notificado a {saved_jobs.count()} usuarios: {instance.title}')

    except Exception as e:
        print(f'[NOTIFICATION ERROR] Error al crear notificación de trabajo cerrado: {e}')
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


# ========== NOTIFICACIONES DE SEGURIDAD ==========

@receiver(post_save, sender='auth_api.CustomUser')
def notify_password_changed(sender, instance, created, **kwargs):
    """
    Notificar al usuario cuando su contraseña es cambiada
    """
    if created:
        return

    try:
        # Obtener cambios del estado anterior
        from G_Jobs.audit.signals import _audit_state
        old_instance = None

        # Buscar en el thread-local storage
        if hasattr(_audit_state, 'customuser_old_state') and instance.pk in _audit_state.customuser_old_state:
            old_instance = _audit_state.customuser_old_state[instance.pk]

        if not old_instance:
            return

        # Detectar cambio en password
        old_password = old_instance.password
        new_password = instance.password

        if old_password == new_password:
            return

        # Crear notificación de seguridad
        Notification.create_notification(
            user=instance,
            notification_type='password_changed',
            title='Contraseña cambiada',
            message='Tu contraseña ha sido cambiada exitosamente. Si no realizaste este cambio, contacta con soporte inmediatamente.',
            metadata={
                'user_email': instance.email,
                'timestamp': instance.updated_at.isoformat() if hasattr(instance, 'updated_at') else None
            }
        )

        print(f'[NOTIFICATION] Contraseña cambiada para: {instance.email}')

    except Exception as e:
        print(f'[NOTIFICATION ERROR] Error al crear notificación de cambio de contraseña: {e}')
        import traceback
        traceback.print_exc()


# Signal pre_save para capturar estado anterior del usuario
from django.db.models.signals import pre_save

@receiver(pre_save, sender='auth_api.CustomUser')
def customuser_pre_save(sender, instance, **kwargs):
    """Capturar estado anterior del CustomUser antes de guardar"""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            # Guardar estado anterior en thread-local
            from G_Jobs.audit.signals import _audit_state
            if not hasattr(_audit_state, 'customuser_old_state'):
                _audit_state.customuser_old_state = {}
            _audit_state.customuser_old_state[instance.pk] = old_instance
        except sender.DoesNotExist:
            pass
