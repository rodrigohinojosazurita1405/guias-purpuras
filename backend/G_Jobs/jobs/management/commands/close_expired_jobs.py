"""
Management command para cerrar ofertas de trabajo expiradas
Actualiza el status de 'active' a 'closed' para todos los anuncios
cuya fecha de expiración ya pasó
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from G_Jobs.jobs.models import Job


class Command(BaseCommand):
    help = 'Cierra todas las ofertas de trabajo que han expirado'

    def handle(self, *args, **options):
        today = timezone.now().date()

        # Encontrar todas las ofertas activas con fecha de expiración pasada
        expired_jobs = Job.objects.filter(
            status='active',
            expiryDate__lt=today
        )

        count = expired_jobs.count()

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No hay ofertas expiradas para cerrar.')
            )
            return

        # Mostrar información sobre las ofertas que se van a cerrar
        self.stdout.write(
            self.style.WARNING(f'\nSe encontraron {count} ofertas expiradas:')
        )

        for job in expired_jobs:
            self.stdout.write(
                f'  - {job.title} (ID: {job.id}) - Expiro: {job.expiryDate}'
            )

        # Actualizar todas las ofertas expiradas a estado 'closed'
        expired_jobs.update(status='closed')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSe cerraron {count} ofertas expiradas exitosamente.\n'
            )
        )
