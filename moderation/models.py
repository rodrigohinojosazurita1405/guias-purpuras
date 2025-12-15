from django.db import models
from django.conf import settings


class BlockedUser(models.Model):
    """
    Modelo para usuarios bloqueados por empresas
    Permite a las empresas bloquear candidatos específicos
    """
    # Empresa que realiza el bloqueo
    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='users_blocked_by_me',
        limit_choices_to={'role': 'company'},
        verbose_name="Empresa"
    )

    # Usuario bloqueado
    blocked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_by_companies',
        limit_choices_to={'role': 'applicant'},
        verbose_name="Usuario bloqueado"
    )

    # Razón del bloqueo
    reason = models.CharField(
        max_length=50,
        choices=[
            ('spam', 'Spam'),
            ('inappropriate', 'Comportamiento inapropiado'),
            ('unqualified', 'No calificado repetidamente'),
            ('other', 'Otra razón')
        ],
        verbose_name="Razón"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notas adicionales"
    )

    # Fecha del bloqueo
    blocked_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Bloqueado el"
    )

    class Meta:
        verbose_name = 'Usuario Bloqueado'
        verbose_name_plural = 'Usuarios Bloqueados'
        ordering = ['-blocked_at']
        unique_together = ['company', 'blocked_user']
        indexes = [
            models.Index(fields=['company', '-blocked_at']),
            models.Index(fields=['blocked_user']),
        ]
        db_table = 'jobs_blockeduser'  # Mantener nombre de tabla original

    def __str__(self):
        return f"{self.company.email} bloqueó a {self.blocked_user.email} - {self.get_reason_display()}"
