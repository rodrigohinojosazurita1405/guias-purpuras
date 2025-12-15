"""
Señales automáticas para auditar cambios en modelos
Se conectan automáticamente cuando la app se inicia
"""

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog
from .middleware import get_current_request, get_current_user
import threading

# Thread-local storage para almacenar estado anterior de modelos
_audit_state = threading.local()


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

    # Intentar obtener estado anterior del thread-local
    old_instance = None
    model_name = instance.__class__.__name__.lower()
    state_key = f'{model_name}_old_state'

    print(f"[AUDIT DEBUG] Buscando estado anterior: model={model_name}, key={state_key}, pk={instance.pk}")
    print(f"[AUDIT DEBUG] hasattr={hasattr(_audit_state, state_key)}")
    if hasattr(_audit_state, state_key):
        print(f"[AUDIT DEBUG] Estado keys: {getattr(_audit_state, state_key, {}).keys()}")

    if hasattr(_audit_state, state_key) and instance.pk in getattr(_audit_state, state_key, {}):
        old_instance = _audit_state.__dict__[state_key][instance.pk]
        print(f"[AUDIT DEBUG] Estado anterior encontrado!")
        # NO limpiar aquí - se limpiará al final del signal

    if not old_instance:
        print(f"[AUDIT DEBUG] No hay estado anterior, retornando vacío")
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

@receiver(pre_save, sender='jobs.Job')
def job_pre_save(sender, instance, **kwargs):
    """Capturar estado anterior del Job antes de guardar"""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            # Guardar estado anterior en thread-local
            if not hasattr(_audit_state, 'job_old_state'):
                _audit_state.job_old_state = {}
            _audit_state.job_old_state[instance.pk] = old_instance
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender='jobs.Job')
def audit_job_save(sender, instance, created, **kwargs):
    """Auditar cuando se crea o actualiza un Job"""
    from jobs.models import Job

    print(f"[AUDIT] Signal post_save ejecutado para Job: {instance.title}, created={created}")

    # Obtener cambios UNA SOLA VEZ para evitar limpiar el estado
    changes = get_model_changes(instance, created)

    # No auditar si no hay cambios reales
    if not created and not changes:
        print(f"[AUDIT] No hay cambios, saltando auditoría")
        return

    # No auditar si solo cambió el campo 'views' (visitas de usuarios anónimos)
    if not created and changes and list(changes.keys()) == ['views']:
        print(f"[AUDIT] Solo cambió 'views', saltando auditoría (visita anónima)")
        # Limpiar el estado anterior
        if hasattr(_audit_state, 'job_old_state') and instance.pk in _audit_state.job_old_state:
            del _audit_state.job_old_state[instance.pk]
        return

    # No auditar si solo cambió 'applications' (incremento automático al aplicar)
    if not created and changes and list(changes.keys()) == ['applications']:
        print(f"[AUDIT] Solo cambió 'applications', saltando auditoría (aplicación nueva)")
        # Limpiar el estado anterior
        if hasattr(_audit_state, 'job_old_state') and instance.pk in _audit_state.job_old_state:
            del _audit_state.job_old_state[instance.pk]
        return

    # Detectar si es una eliminación lógica (soft delete)
    is_soft_delete = 'isDeleted' in changes and changes['isDeleted']['new'] == 'True'

    # Determinar acción
    if created:
        action = 'create'
    elif is_soft_delete:
        action = 'soft_delete'  # Acción especial para eliminación lógica
    else:
        action = 'update'

    # Determinar severidad
    severity = 'info'
    if action == 'create':
        severity = 'info'
    elif action == 'soft_delete':
        severity = 'critical'  # Eliminación es crítica
    elif 'status' in changes and changes['status']['new'] == 'closed':
        severity = 'warning'

    # ⚠️ FIX CRÍTICO: Priorizar usuario del atributo _audit_user (pasado desde el view)
    # Si no existe, intentar obtenerlo del middleware (pero puede estar desincronizado)
    user = getattr(instance, '_audit_user', None)
    request = getattr(instance, '_audit_request', None)

    if not user:
        user = get_current_user()
        request = get_current_request()
        print(f"[AUDIT WARNING] Usuario obtenido del middleware (puede estar desincronizado)")

    print(f"[AUDIT] Usuario: {user}, Request: {request}")
    if user and user.is_authenticated:
        print(f"[AUDIT] Email del usuario: {user.email}")
        print(f"[AUDIT] Rol del usuario: {user.role if hasattr(user, 'role') else 'NO TIENE ROL'}")
    else:
        print(f"[AUDIT] Usuario no autenticado (AnonymousUser)")
    print(f"[AUDIT] Cambios: {changes}")
    print(f"[AUDIT] Acción detectada: {action}")

    # Descripción según acción
    if created:
        description = f"Job '{instance.title}' fue creado"
    elif is_soft_delete:
        description = f"Job '{instance.title}' fue eliminado (soft delete)"
    else:
        description = f"Job '{instance.title}' fue actualizado"

    try:
        # Auditar incluso sin usuario (puede ser acción del sistema)
        log = AuditLog.log_action(
            user=user,
            obj=instance,
            action=action,
            changes=changes,
            description=description,
            severity=severity,
            request=request
        )
        print(f"[AUDIT] Log creado exitosamente: {log.id}")
    except Exception as e:
        print(f"[AUDIT ERROR] Error al crear log: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Limpiar el estado anterior después de auditar
        if hasattr(_audit_state, 'job_old_state') and instance.pk in _audit_state.job_old_state:
            del _audit_state.job_old_state[instance.pk]
            print(f"[AUDIT] Estado anterior limpiado para Job {instance.pk}")


@receiver(pre_delete, sender='jobs.Job')
def audit_job_delete(sender, instance, **kwargs):
    """Auditar cuando se elimina un Job"""
    # Obtener usuario y request del middleware
    user = get_current_user()
    request = get_current_request()

    print(f"[AUDIT] Signal pre_delete ejecutado para Job: {instance.title}")
    print(f"[AUDIT] Usuario: {user}")
    print(f"[AUDIT] Request: {request}")

    description = f"Job '{instance.title}' fue eliminado permanentemente"

    try:
        # Auditar incluso sin usuario (puede ser acción del sistema)
        log = AuditLog.log_action(
            user=user,
            obj=instance,
            action='delete',
            changes={},
            description=description,
            severity='critical',
            request=request
        )
        print(f"[AUDIT] Log creado exitosamente: {log.id}")
    except Exception as e:
        print(f"[AUDIT ERROR] Error al crear log: {e}")
        import traceback
        traceback.print_exc()


# ========== AUDITAR PLANORDERS ==========

@receiver(post_save, sender='payments.PlanOrder')
def audit_plan_order_save(sender, instance, created, **kwargs):
    """Auditar cuando se crea o actualiza una PlanOrder"""
    from payments.models import PlanOrder

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
