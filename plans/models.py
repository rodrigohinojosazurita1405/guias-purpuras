from django.db import models
import json


class Plan(models.Model):
    """Modelo para gestionar planes de publicación de anuncios"""

    PLAN_CHOICES = [
        ('escencial', 'Escencial'),
        ('purpura', 'Púrpura'),
        ('impulso', 'Impulso Pro'),
    ]

    # Identificador del plan
    name = models.CharField(
        max_length=50,
        choices=PLAN_CHOICES,
        unique=True,
        help_text="Nombre único del plan"
    )

    # Información básica
    label = models.CharField(
        max_length=100,
        help_text="Etiqueta para mostrar en UI (ej: 'Escencial (35 Bs)')"
    )

    description = models.TextField(
        blank=True,
        default="",
        help_text="Descripción del plan para el usuario"
    )

    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio en Bs"
    )

    currency = models.CharField(
        max_length=3,
        default="Bs",
        help_text="Moneda (Bs, $, etc)"
    )

    # Validez del anuncio
    duration_days = models.IntegerField(
        default=15,
        help_text="Duración del anuncio en días"
    )

    # Características del plan (JSON)
    features = models.JSONField(
        default=dict,
        blank=True,
        help_text="Características y límites del plan en formato JSON"
    )

    # Estado
    is_active = models.BooleanField(
        default=True,
        help_text="¿Está disponible este plan?"
    )

    # Orden de visualización
    order = models.IntegerField(
        default=0,
        help_text="Orden para mostrar en la UI (menor número = primero)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    def __str__(self):
        return f"{self.label} ({self.price} {self.currency})"

    def get_features(self):
        """Obtener características como diccionario"""
        return self.features if isinstance(self.features, dict) else json.loads(self.features or '{}')

    def to_dict(self):
        """Convertir a diccionario para API"""
        return {
            'id': self.id,
            'name': self.name,
            'label': self.label,
            'description': self.description,
            'price': float(self.price),
            'currency': self.currency,
            'durationDays': self.duration_days,
            'features': self.get_features(),
            'isActive': self.is_active,
            'order': self.order,
        }
