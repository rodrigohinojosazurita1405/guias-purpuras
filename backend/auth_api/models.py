from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import secrets


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


class PasswordResetToken(models.Model):
    """
    Modelo para almacenar tokens de recuperación de contraseña
    Los tokens son válidos por 1 hora
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        verbose_name='Usuario'
    )
    token = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Token'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    expires_at = models.DateTimeField(
        verbose_name='Fecha de Expiración'
    )
    used = models.BooleanField(
        default=False,
        verbose_name='Usado'
    )

    class Meta:
        verbose_name = 'Token de Recuperación de Contraseña'
        verbose_name_plural = 'Tokens de Recuperación de Contraseña'
        ordering = ['-created_at']

    def __str__(self):
        return f"Token para {self.user.email} - {'Usado' if self.used else 'Activo'}"

    def is_valid(self):
        """Verifica si el token es válido (no usado y no expirado)"""
        return not self.used and timezone.now() < self.expires_at

    @staticmethod
    def generate_token():
        """Genera un token seguro y único"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def create_for_user(user):
        """Crea un nuevo token de recuperación para un usuario"""
        # Invalidar tokens anteriores
        PasswordResetToken.objects.filter(user=user, used=False).update(used=True)

        # Crear nuevo token
        token = PasswordResetToken.generate_token()
        expires_at = timezone.now() + timedelta(hours=1)

        return PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
