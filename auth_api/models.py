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
        if self.is_superuser:
            full_name = f"{self.first_name} {self.last_name}".strip()
            if full_name:
                return full_name
            return self.username
        return f"{self.email} ({self.get_role_display()})"

    def is_applicant(self):
        """Verifica si el usuario es postulante"""
        return self.role == 'applicant'

    def is_company(self):
        """Verifica si el usuario es empresa"""
        return self.role == 'company'


class AdminUser(CustomUser):
    """
    Proxy model para mostrar administradores del sistema en una sección separada del admin
    Permite mostrar la misma tabla de CustomUser en dos secciones diferentes
    """
    class Meta:
        proxy = True
        verbose_name = 'Administrador del Sistema'
        verbose_name_plural = 'Administradores del Sistema'
