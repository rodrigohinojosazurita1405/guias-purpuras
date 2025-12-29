"""
Tareas programadas para el sistema de notificaciones

Para ejecutar automaticamente, puedes usar:
1. django-crontab (recomendado para produccion)
2. APScheduler (para desarrollo)
3. Celery Beat (para sistemas mas complejos)
"""
from django.utils import timezone
from datetime import timedelta
from .models import Notification
import logging

logger = logging.getLogger(__name__)


def cleanup_old_dismissed_notifications(days=30):
    """
    Limpia notificaciones descartadas antiguas

    Esta funcion se puede ejecutar:
    - Manualmente: python manage.py cleanup_old_notifications
    - Automaticamente: via cron job o scheduler

    Args:
        days (int): Dias de antiguedad para eliminar (default: 30)

    Returns:
        int: Numero de notificaciones eliminadas
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=days)

        old_notifications = Notification.objects.filter(
            is_dismissed=True,
            dismissed_at__lt=cutoff_date
        )

        count = old_notifications.count()

        if count > 0:
            deleted_count, _ = old_notifications.delete()
            logger.info(
                f'[NOTIFICATIONS CLEANUP] Se eliminaron {deleted_count} '
                f'notificaciones descartadas de hace mas de {days} dias'
            )
            return deleted_count
        else:
            logger.info('[NOTIFICATIONS CLEANUP] No hay notificaciones antiguas para eliminar')
            return 0

    except Exception as e:
        logger.error(f'[NOTIFICATIONS CLEANUP] Error: {e}')
        import traceback
        traceback.print_exc()
        return 0


# ========== CONFIGURACION PARA DJANGO-CRONTAB ==========
# Agregar en settings.py:
#
# CRONJOBS = [
#     # Limpiar notificaciones descartadas cada dia a las 3 AM
#     ('0 3 * * *', 'G_Jobs.notifications.tasks.cleanup_old_dismissed_notifications'),
# ]
#
# Luego ejecutar:
# python manage.py crontab add


# ========== CONFIGURACION PARA APSCHEDULER (DESARROLLO) ==========
# Agregar en apps.py:
#
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
#
# def ready(self):
#     super().ready()
#     import G_Jobs.notifications.signals
#
#     # Iniciar scheduler
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(
#         cleanup_old_dismissed_notifications,
#         trigger=CronTrigger(hour=3, minute=0),  # Cada dia a las 3 AM
#         id='cleanup_notifications',
#         max_instances=1,
#         replace_existing=True
#     )
#     scheduler.start()
