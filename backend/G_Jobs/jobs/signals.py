"""
Signals para el módulo de Jobs
Maneja eventos automáticos relacionados con ofertas de trabajo
"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, date
from .models import Job


@receiver(pre_save, sender=Job)
def auto_close_expired_jobs(sender, instance, **kwargs):
    """
    Signal que automáticamente marca como 'closed' las ofertas que han expirado.
    Se ejecuta antes de cada guardado del modelo Job.

    Lógica:
    - Si la oferta tiene expiryDate y ya pasó la fecha
    - Y el estado actual es 'active'
    - Entonces cambiar estado a 'closed'
    """
    if instance.expiryDate:
        # Comparar solo fechas (sin hora) para evitar problemas de timezone
        today = timezone.now().date()
        expiry_date = instance.expiryDate

        # Convertir a date si es string
        if isinstance(expiry_date, str):
            try:
                expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            except ValueError:
                # Si el formato es diferente, intentar con ISO format
                try:
                    expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00')).date()
                except:
                    # Si falla, no hacer nada
                    return

        # Asegurarse de que sea un objeto date
        if isinstance(expiry_date, datetime):
            expiry_date = expiry_date.date()

        # Si la fecha de expiración ya pasó y la oferta está activa
        if isinstance(expiry_date, date) and expiry_date < today and instance.status == 'active':
            instance.status = 'closed'
            print(f"✓ Oferta '{instance.title}' marcada como cerrada automáticamente (expirada el {expiry_date})")
