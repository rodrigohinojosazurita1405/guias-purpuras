"""
Señales automáticas para auditar cambios en modelos
Se conectan automáticamente cuando la app se inicia
"""

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog


def get_model_changes(instance, created=False):
    """
    Detecta cambios en un modelo comparando con la versión anterior en BD

    Args:
        instance: Instancia del modelo
        created: Si es una creación nueva

    Returns:
        Dict con cambios {field: {'old': val, 'new': val}}
    """
    if created:
        return {}

    # Obtener instancia anterior de la base de datos
    model_class = instance.__class__
    try:
        old_instance = model_class.objects.get(pk=instance.pk)
    except model_class.DoesNotExist:
        return {}

    changes = {}
    # Campos a ignorar en la auditoría
    ignored_fields = ['updatedAt', 'updated_at', 'createdAt', 'created_at']

    for field in instance._meta.fields:
        field_name = field.name

        # Ignorar ciertos campos
        if field_name in ignored_fields:
            continue

        # Ignorar campos de contraseña
        if 'password' in field_name.lower():
            continue

        old_value = getattr(old_instance, field_name, None)
        new_value = getattr(instance, field_name, None)

        # Si son diferentes, registrar el cambio
        if old_value != new_value:
            # Formatear valores para mejor legibilidad
            changes[field_name] = {
                'old': str(old_value) if old_value is not None else 'None',
                'new': str(new_value) if new_value is not None else 'None'
            }

    return changes


# ========== AUDITAR JOBS ==========

@receiver(post_save, sender='jobs.Job')
def audit_job_save(sender, instance, created, **kwargs):
    """Auditar cuando se crea o actualiza un Job"""
    from jobs.models import Job

    # No auditar si no hay cambios reales
    if not created and not get_model_changes(instance, created):
        return

    action = 'create' if created else 'update'
    changes = get_model_changes(instance, created)

    # Determinar severidad
    severity = 'info'
    if action == 'create':
        severity = 'info'
    elif 'status' in changes and changes['status']['new'] == 'closed':
        severity = 'warning'
    elif 'isDeleted' in changes and changes['isDeleted']['new'] == 'True':
        severity = 'warning'

    # Obtener usuario del thread local si está disponible
    # (esto se puede mejorar con middleware)
    user = getattr(instance, '_audit_user', None)

    description = f"Job '{instance.title}' fue {'creado' if created else 'actualizado'}"

    if user:
        AuditLog.log_action(
            user=user,
            obj=instance,
            action=action,
            changes=changes,
            description=description,
            severity=severity,
            request=getattr(instance, '_audit_request', None)
        )


@receiver(pre_delete, sender='jobs.Job')
def audit_job_delete(sender, instance, **kwargs):
    """Auditar cuando se elimina un Job"""
    user = getattr(instance, '_audit_user', None)

    description = f"Job '{instance.title}' fue eliminado permanentemente"

    if user:
        AuditLog.log_action(
            user=user,
            obj=instance,
            action='delete',
            changes={},
            description=description,
            severity='critical',
            request=getattr(instance, '_audit_request', None)
        )


# ========== AUDITAR PLANORDERS ==========

@receiver(post_save, sender='jobs.PlanOrder')
def audit_plan_order_save(sender, instance, created, **kwargs):
    """Auditar cuando se crea o actualiza una PlanOrder"""
    from jobs.models import PlanOrder

    action = 'create' if created else 'update'
    changes = get_model_changes(instance, created)

    severity = 'info'
    if 'status' in changes and changes['status']['new'] == 'completed':
        severity = 'info'  # Completado es normal

    user = getattr(instance, '_audit_user', None) or instance.user

    description = f"Orden #{instance.id} ({instance.razon_social}) fue {'creada' if created else 'actualizada'}"

    AuditLog.log_action(
        user=user,
        obj=instance,
        action=action,
        changes=changes,
        description=description,
        severity=severity,
        request=getattr(instance, '_audit_request', None)
    )


# ========== AUDITAR COMPANYPROFILES ==========

@receiver(post_save, sender='profiles.CompanyProfile')
def audit_company_profile_save(sender, instance, created, **kwargs):
    """Auditar cuando se crea o actualiza un CompanyProfile"""
    from profiles.models import CompanyProfile

    action = 'create' if created else 'update'
    changes = get_model_changes(instance, created)

    user = getattr(instance, '_audit_user', None)

    description = f"Perfil de empresa '{instance.companyName}' fue {'creado' if created else 'actualizado'}"

    if user:
        AuditLog.log_action(
            user=user,
            obj=instance,
            action=action,
            changes=changes,
            description=description,
            severity='info',
            request=getattr(instance, '_audit_request', None)
        )


# ========== AUDITAR USUARIOS ==========

@receiver(post_save, sender='auth_api.CustomUser')
def audit_user_save(sender, instance, created, **kwargs):
    """Auditar cuando se crea o actualiza un usuario"""

    action = 'create' if created else 'update'
    changes = get_model_changes(instance, created)

    # Filtrar campos sensibles
    if 'password' in changes:
        changes.pop('password')

    severity = 'info'
    if created:
        severity = 'info'
    elif 'is_active' in changes and changes['is_active']['new'] == 'False':
        severity = 'warning'

    user = getattr(instance, '_audit_user', None) or instance

    description = f"Usuario {instance.email} fue {'registrado' if created else 'actualizado'}"

    AuditLog.log_action(
        user=user,
        obj=instance,
        action=action,
        changes=changes,
        description=description,
        severity=severity,
        request=getattr(instance, '_audit_request', None)
    )
