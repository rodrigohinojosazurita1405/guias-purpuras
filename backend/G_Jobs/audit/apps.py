from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'G_Jobs.audit'
    verbose_name = 'Auditoría del Sistema'

    def ready(self):
        """Importar señales cuando la app esté lista"""
        import G_Jobs.audit.signals
