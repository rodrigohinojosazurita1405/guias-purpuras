from django.apps import AppConfig
import os


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'G_Jobs.notifications'
    verbose_name = 'Notificaciones'

    def ready(self):
        """Importar signals e iniciar scheduler cuando la app esté lista"""
        import G_Jobs.notifications.signals

        # Iniciar scheduler de tareas programadas
        # Solo ejecutar en el proceso principal de Django (evitar duplicados en reload)
        if os.environ.get('RUN_MAIN') == 'true':
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            from G_Jobs.notifications.tasks import cleanup_old_dismissed_notifications

            scheduler = BackgroundScheduler()
            scheduler.add_job(
                cleanup_old_dismissed_notifications,
                trigger=CronTrigger(hour=3, minute=0),  # Cada día a las 3:00 AM
                id='cleanup_notifications',
                max_instances=1,
                replace_existing=True
            )
            scheduler.start()

            import logging
            logger = logging.getLogger(__name__)
            logger.info('[NOTIFICATIONS SCHEDULER] Scheduler iniciado - Limpieza automática a las 3:00 AM')
