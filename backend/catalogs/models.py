from django.db import models


class JobCategory(models.Model):
    """
    Categorías de trabajo dinámicas
    Permite gestionar categorías desde Django Admin
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la categoría"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="Slug (auto-generado)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Nombre del ícono (Material Icons)",
        verbose_name="Ícono"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Categoría de Trabajo"
        verbose_name_plural = "Categorías de Trabajo"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
        ]
        db_table = 'jobs_jobcategory'  # Mantener nombre de tabla original

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ContractType(models.Model):
    """
    Tipos de contrato dinámicos
    Permite gestionar tipos de contrato desde Django Admin
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre del tipo de contrato"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="Slug (auto-generado)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Tipo de Contrato"
        verbose_name_plural = "Tipos de Contrato"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
        ]
        db_table = 'jobs_contracttype'  # Mantener nombre de tabla original

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Ciudades/Departamentos dinámicos
    Permite gestionar ciudades desde Django Admin
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la ciudad"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="Slug (auto-generado)"
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Departamento"
    )
    region = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('altiplano', 'Altiplano'),
            ('valles', 'Valles'),
            ('llanos', 'Llanos'),
        ],
        verbose_name="Región"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
            models.Index(fields=['region']),
        ]
        db_table = 'jobs_city'  # Mantener nombre de tabla original

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.department})" if self.department else self.name
