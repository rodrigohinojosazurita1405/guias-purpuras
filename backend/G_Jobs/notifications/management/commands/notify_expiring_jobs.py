"""
Comando de Django para notificar sobre trabajos próximos a vencer

Uso:
    python manage.py notify_expiring_jobs

Este comando debe ejecutarse diariamente mediante cron o celery beat:
    0 9 * * * cd /path/to/project && python manage.py notify_expiring_jobs
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from G_Jobs.jobs.models import Job
from G_Jobs.notifications.models import Notification
from auth_api.models import CustomUser


class Command(BaseCommand):
    help = 'Notificar a empresas sobre trabajos próximos a vencer (3 días antes)'

    def handle(self, *args, **options):
        # Calcular fecha objetivo: en 3 días
        target_date = timezone.now() + timedelta(days=3)
        # Rango de 1 día (desde hoy + 3 días hasta hoy + 4 días)
        start_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)

        self.stdout.write(f'Buscando trabajos que vencen entre {start_date} y {end_date}...')

        # Buscar trabajos activos que vencen en 3 días
        expiring_jobs = Job.objects.filter(
            status='active',
            expiresAt__gte=start_date,
            expiresAt__lt=end_date,
            paymentVerified=True  # Solo trabajos con pago verificado
        )

        notifications_created = 0

        for job in expiring_jobs:
            try:
                # Obtener usuario de la empresa
                company_user = CustomUser.objects.filter(
                    email=job.email,
                    role='company'
                ).first()

                if not company_user:
                    self.stdout.write(
                        self.style.WARNING(f'No se encontró usuario empresa para: {job.email}')
                    )
                    continue

                # Verificar si ya existe una notificación de este tipo para este job
                existing = Notification.objects.filter(
                    user=company_user,
                    notification_type='job_expiring_soon',
                    metadata__job_id=str(job.id)
                ).exists()

                if existing:
                    self.stdout.write(
                        self.style.WARNING(f'Ya existe notificación para: {job.title}')
                    )
                    continue

                # Crear notificación
                Notification.create_notification(
                    user=company_user,
                    notification_type='job_expiring_soon',
                    title='Anuncio próximo a vencer',
                    message=f'Tu anuncio "{job.title}" vence en 3 días. Considera renovarlo para seguir recibiendo postulaciones.',
                    metadata={
                        'job_id': str(job.id),
                        'job_title': job.title,
                        'expires_at': job.expiresAt.isoformat()
                    }
                )

                notifications_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Notificación creada para: {job.title}')
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error al notificar {job.title}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Proceso completado: {notifications_created} notificaciones creadas'
            )
        )
