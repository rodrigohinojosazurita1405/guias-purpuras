from django.db import models
import json


class Plan(models.Model):
    """Modelo para gestionar planes de publicación de anuncios"""

    # Identificador del plan
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nombre único del plan (ej: escencial, purpura, impulso)"
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

    badge_label = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Texto del badge (ej: 'Básico', 'Popular', 'Premium'). Dejar vacío si no deseas mostrar badge."
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

    # ========== CARACTERÍSTICAS DEL PLAN (CAMPOS VISUALES) ==========
    max_announcements = models.IntegerField(
        default=1,
        help_text="Número máximo de anuncios que puede publicar"
    )

    is_featured = models.BooleanField(
        default=False,
        help_text="¿Anuncio destacado/patrocinado?"
    )

    featured_days = models.IntegerField(
        default=0,
        help_text="Días que permanecerá destacado (0 = sin duración)"
    )

    has_highlighted_results = models.BooleanField(
        default=False,
        help_text="¿Mostrar resultados destacados?"
    )

    announcement_substitutions = models.IntegerField(
        default=0,
        help_text="Número de sustituciones de aviso permitidas (0 = No incluido)"
    )

    # Difusión en Redes Sociales
    facebook_posts = models.IntegerField(
        default=1,
        help_text="Posts en Facebook/Instagram permitidos"
    )

    linkedin_posts = models.IntegerField(
        default=0,
        help_text="Posts en LinkedIn permitidos"
    )

    tiktok_posts = models.IntegerField(
        default=0,
        help_text="Posts en TikTok permitidos"
    )

    # Características del plan (JSON - se genera automáticamente)
    features = models.JSONField(
        default=dict,
        blank=True,
        help_text="Generado automáticamente desde los campos anteriores"
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

    def save(self, *args, **kwargs):
        """Auto-generar features JSON desde campos separados"""
        self.features = {
            'maxAnnouncements': self.max_announcements,
            'featured': self.is_featured,
            'featuredDays': self.featured_days,
            'highlightedResults': self.has_highlighted_results,
            'announcementSubstitutions': self.announcement_substitutions,
            'socialMedia': {
                'facebook': self.facebook_posts,
                'linkedin': self.linkedin_posts,
                'tiktok': self.tiktok_posts,
            }
        }
        super().save(*args, **kwargs)

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
            'badgeLabel': self.badge_label,
            'price': float(self.price),
            'currency': self.currency,
            'durationDays': self.duration_days,
            'features': self.get_features(),
            'isActive': self.is_active,
            'order': self.order,
        }
