"""
Comando de gestion para limpiar notificaciones antiguas
Estilo Facebook: Eliminar notificaciones descartadas de mas de 30 dias

Uso:
    python manage.py cleanup_old_notifications
    python manage.py cleanup_old_notifications --days 90
    python manage.py cleanup_old_notifications --dry-run
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from G_Jobs.notifications.models import Notification


class Command(BaseCommand):
    help = 'Limpia notificaciones antiguas descartadas (estilo Facebook)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Dias de antiguedad para eliminar notificaciones descartadas (default: 30)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar que se eliminaria sin ejecutar la eliminacion'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']

        # Calcular fecha limite
        cutoff_date = timezone.now() - timedelta(days=days)

        # Buscar notificaciones descartadas antiguas
        old_notifications = Notification.objects.filter(
            is_dismissed=True,
            dismissed_at__lt=cutoff_date
        )

        count = old_notifications.count()

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'[DRY RUN] Se eliminarian {count} notificaciones descartadas '
                    f'de hace mas de {days} dias'
                )
            )

            if count > 0:
                self.stdout.write('\nEjemplos:')
                for notif in old_notifications[:5]:
                    self.stdout.write(
                        f'  - {notif.user.email}: {notif.title} '
                        f'(descartada: {notif.dismissed_at.strftime("%Y-%m-%d")})'
                    )

            return

        # Eliminar
        deleted_count, _ = old_notifications.delete()

        if deleted_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Exito! Se eliminaron {deleted_count} notificaciones descartadas '
                    f'de hace mas de {days} dias'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'No hay notificaciones antiguas para eliminar'
                )
            )
