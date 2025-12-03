from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import json


class AuditLog(models.Model):
    """
    Sistema de auditoría genérico para rastrear todas las acciones de usuarios
    Utiliza GenericForeignKey para auditar cualquier modelo
    """

    # ========== INFORMACIÓN DEL USUARIO ==========
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name="Usuario"
    )

    user_email = models.EmailField(
        max_length=255,
        verbose_name="Email del Usuario",
        help_text="Email guardado para referencia histórica (en caso de que el usuario se elimine)"
    )

    user_role = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Rol del Usuario"
    )

    # ========== OBJETO AUDITADO (GENÉRICO) ==========
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Tipo de Objeto"
    )

    object_id = models.CharField(
        max_length=255,
        verbose_name="ID del Objeto"
    )

    content_object = GenericForeignKey('content_type', 'object_id')

    object_repr = models.CharField(
        max_length=500,
        verbose_name="Representación del Objeto",
        help_text="Nombre/título del objeto para referencia rápida"
    )

    # ========== ACCIÓN REALIZADA ==========
    ACTION_CHOICES = [
        ('create', 'Creado'),
        ('update', 'Actualizado'),
        ('delete', 'Eliminado'),
        ('soft_delete', 'Eliminado (Lógico)'),
        ('restore', 'Restaurado'),
        ('pause', 'Pausado'),
        ('activate', 'Activado'),
        ('close', 'Cerrado'),
        ('verify_payment', 'Pago Verificado'),
        ('reject_payment', 'Pago Rechazado'),
        ('duplicate', 'Duplicado'),
        ('view', 'Visualizado'),
        ('export', 'Exportado'),
        ('other', 'Otra Acción'),
    ]

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name="Acción"
    )

    action_description = models.TextField(
        blank=True,
        verbose_name="Descripción de la Acción",
        help_text="Descripción detallada de lo que se hizo"
    )

    # ========== CAMBIOS REALIZADOS ==========
    changes = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Cambios",
        help_text="Diccionario con los valores antes/después de cada campo modificado"
    )

    # ========== METADATOS ==========
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Dirección IP"
    )

    user_agent = models.TextField(
        blank=True,
        verbose_name="User Agent",
        help_text="Navegador y sistema operativo del usuario"
    )

    session_key = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Session Key"
    )

    # ========== TIMESTAMP ==========
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Fecha y Hora"
    )

    # ========== CATEGORIZACIÓN ==========
    severity = models.CharField(
        max_length=10,
        choices=[
            ('info', 'Información'),
            ('warning', 'Advertencia'),
            ('critical', 'Crítico'),
        ],
        default='info',
        verbose_name="Severidad"
    )

    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
            models.Index(fields=['user_email']),
        ]

    def __str__(self):
        return f"{self.user_email} - {self.get_action_display()} - {self.content_type} #{self.object_id} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    def get_changes_summary(self):
        """Retorna un resumen legible de los cambios"""
        if not self.changes:
            return "Sin cambios específicos"

        summary = []
        for field, change_data in self.changes.items():
            if isinstance(change_data, dict) and 'old' in change_data and 'new' in change_data:
                old_val = change_data['old']
                new_val = change_data['new']
                summary.append(f"{field}: '{old_val}' → '{new_val}'")
            else:
                summary.append(f"{field}: {change_data}")

        return "\n".join(summary)

    @classmethod
    def log_action(cls, user, obj, action, changes=None, description="", severity="info", request=None):
        """
        Método helper para crear logs de auditoría fácilmente

        Args:
            user: Usuario que realiza la acción
            obj: Objeto modificado (instancia del modelo)
            action: Tipo de acción (create, update, delete, etc)
            changes: Dict con cambios {field: {'old': val, 'new': val}}
            description: Descripción adicional
            severity: Nivel de severidad (info, warning, critical)
            request: Objeto request de Django (opcional)

        Returns:
            AuditLog instance
        """
        content_type = ContentType.objects.get_for_model(obj)

        # Extraer metadatos del request si está disponible
        ip_address = None
        user_agent = ""
        session_key = ""

        if request:
            # Obtener IP del usuario
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')

            user_agent = request.META.get('HTTP_USER_AGENT', '')
            session_key = request.session.session_key or ''

        return cls.objects.create(
            user=user,
            user_email=user.email if user else 'sistema',
            user_role=getattr(user, 'role', '') if user else '',
            content_type=content_type,
            object_id=str(obj.pk),
            object_repr=str(obj)[:500],
            action=action,
            action_description=description,
            changes=changes or {},
            ip_address=ip_address,
            user_agent=user_agent,
            session_key=session_key,
            severity=severity
        )


class AuditLogSummary(models.Model):
    """
    Resumen diario de actividad de auditoría (para reportes rápidos)
    """
    date = models.DateField(
        unique=True,
        db_index=True,
        verbose_name="Fecha"
    )

    total_actions = models.IntegerField(
        default=0,
        verbose_name="Total de Acciones"
    )

    total_creates = models.IntegerField(
        default=0,
        verbose_name="Creaciones"
    )

    total_updates = models.IntegerField(
        default=0,
        verbose_name="Actualizaciones"
    )

    total_deletes = models.IntegerField(
        default=0,
        verbose_name="Eliminaciones"
    )

    unique_users = models.IntegerField(
        default=0,
        verbose_name="Usuarios Únicos"
    )

    critical_events = models.IntegerField(
        default=0,
        verbose_name="Eventos Críticos"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Generado el"
    )

    class Meta:
        verbose_name = "Resumen de Auditoría"
        verbose_name_plural = "Resúmenes de Auditoría"
        ordering = ['-date']

    def __str__(self):
        return f"Resumen {self.date} - {self.total_actions} acciones"
