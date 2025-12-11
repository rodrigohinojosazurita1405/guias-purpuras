"""
Comando de Django para generar resúmenes diarios de auditoría

Uso:
    python manage.py generate_audit_summary
    python manage.py generate_audit_summary --date 2025-12-08
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from audit.models import AuditLog, AuditLogSummary
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Genera resúmenes diarios de auditoría basados en los logs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Fecha específica en formato YYYY-MM-DD (por defecto: ayer)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Generar resúmenes para todos los días sin resumen',
        )

    def handle(self, *args, **options):
        if options['all']:
            self.generate_all_summaries()
        else:
            date_str = options.get('date')
            if date_str:
                try:
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    self.stdout.write(self.style.ERROR('Formato de fecha inválido. Use YYYY-MM-DD'))
                    return
            else:
                # Por defecto, procesar el día anterior
                target_date = (timezone.now() - timedelta(days=1)).date()

            self.generate_summary_for_date(target_date)

    def generate_summary_for_date(self, target_date):
        """Genera resumen para una fecha específica"""
        self.stdout.write(f'Generando resumen de auditoría para {target_date}...')

        # Obtener logs del día
        logs = AuditLog.objects.filter(
            timestamp__date=target_date
        )

        total_actions = logs.count()

        if total_actions == 0:
            self.stdout.write(self.style.WARNING(f'No hay logs para {target_date}'))
            return

        # Contar por tipo de acción
        total_creates = logs.filter(action='create').count()
        total_updates = logs.filter(action='update').count()
        total_deletes = logs.filter(action__in=['delete', 'soft_delete']).count()

        # Contar usuarios únicos
        unique_users = logs.values('user_email').distinct().count()

        # Contar eventos críticos
        critical_events = logs.filter(severity='critical').count()

        # Crear o actualizar resumen
        summary, created = AuditLogSummary.objects.update_or_create(
            date=target_date,
            defaults={
                'total_actions': total_actions,
                'total_creates': total_creates,
                'total_updates': total_updates,
                'total_deletes': total_deletes,
                'unique_users': unique_users,
                'critical_events': critical_events,
            }
        )

        action = 'Creado' if created else 'Actualizado'
        self.stdout.write(
            self.style.SUCCESS(
                f'{action} resumen para {target_date}: '
                f'{total_actions} acciones, {unique_users} usuarios, '
                f'{critical_events} eventos críticos'
            )
        )

    def generate_all_summaries(self):
        """Genera resúmenes para todas las fechas que tienen logs pero no resumen"""
        self.stdout.write('Generando resúmenes para todas las fechas faltantes...')

        # Obtener todas las fechas con logs
        dates_with_logs = AuditLog.objects.dates('timestamp', 'day')

        # Obtener fechas que ya tienen resumen
        dates_with_summaries = set(
            AuditLogSummary.objects.values_list('date', flat=True)
        )

        # Generar resúmenes para fechas faltantes
        generated = 0
        for log_date in dates_with_logs:
            if log_date not in dates_with_summaries:
                self.generate_summary_for_date(log_date)
                generated += 1

        if generated == 0:
            self.stdout.write(self.style.SUCCESS('Todos los resúmenes están actualizados'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Generados {generated} resúmenes'))
