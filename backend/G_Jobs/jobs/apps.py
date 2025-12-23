from django.apps import AppConfig


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'G_Jobs.jobs'
    verbose_name = 'Ofertas de Trabajo'

    def ready(self):
        """Importar signals cuando la app esté lista"""
        import G_Jobs.jobs.signals
