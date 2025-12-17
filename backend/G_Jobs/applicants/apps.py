from django.apps import AppConfig


class ApplicantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'G_Jobs.applicants'
    verbose_name = 'Postulantes y Aplicaciones'

    def ready(self):
        """Import signals when app is ready"""
        import G_Jobs.applicants.signals
