"""
Modelo de Notificaciones para usuarios del sistema
"""
from django.db import models
from django.conf import settings
import uuid


class Notification(models.Model):
    """
    Notificaciones para usuarios (empresas y postulantes)
    """
    NOTIFICATION_TYPES = [
        # Notificaciones para empresas
        ('new_application', 'Nueva postulación recibida'),
        ('payment_verified', 'Pago verificado'),
        ('payment_rejected', 'Pago rechazado'),
        ('job_expiring_soon', 'Anuncio próximo a vencer'),
        ('job_expired', 'Anuncio vencido'),

        # Notificaciones para postulantes
        ('application_sent', 'Postulación enviada'),
        ('saved_job_closed', 'Trabajo guardado cerrado'),
        ('blocked_attempt', 'Intento de postulación bloqueado'),

        # Notificaciones generales
        ('password_changed', 'Contraseña cambiada'),
        ('profile_updated', 'Perfil actualizado'),
        ('system', 'Notificación del sistema'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Usuario que recibe la notificación
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Usuario"
    )

    # Tipo de notificación
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES,
        verbose_name="Tipo"
    )

    # Título de la notificación
    title = models.CharField(
        max_length=200,
        verbose_name="Título"
    )

    # Mensaje de la notificación
    message = models.TextField(
        verbose_name="Mensaje"
    )

    # Datos adicionales en JSON (job_id, application_id, etc.)
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Metadata"
    )

    # Estado de lectura
    is_read = models.BooleanField(
        default=False,
        verbose_name="Leída"
    )

    # Fecha de lectura
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Leída el"
    )

    # Fecha de creación
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creada el"
    )

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
        db_table = 'jobs_notification'

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    @classmethod
    def create_notification(cls, user, notification_type, title, message, metadata=None):
        """
        Crear una notificación de forma simple

        Args:
            user: Usuario que recibirá la notificación
            notification_type: Tipo de notificación (debe estar en NOTIFICATION_TYPES)
            title: Título de la notificación
            message: Mensaje de la notificación
            metadata: Diccionario con datos adicionales (opcional)

        Returns:
            Notification: La notificación creada
        """
        return cls.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            metadata=metadata or {}
        )

    def mark_as_read(self):
        """Marcar notificación como leída"""
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
