from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser
    Agrega campo de rol para distinguir entre postulantes y empresas
    """

    ROLE_CHOICES = (
        ('applicant', 'Postulante'),
        ('company', 'Empresa'),
    )

    # Campo de rol - identifica si es postulante o empresa
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='applicant',
        verbose_name='Tipo de Usuario',
        help_text='Especifica si el usuario es un postulante de empleos o una empresa'
    )

    # Timestamp de creación
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name = 'Usuario Personalizado'
        verbose_name_plural = 'Usuarios Personalizados'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def is_applicant(self):
        """Verifica si el usuario es postulante"""
        return self.role == 'applicant'

    def is_company(self):
        """Verifica si el usuario es empresa"""
        return self.role == 'company'
