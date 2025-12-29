"""
Comando para limpiar reportes antiguos (más de 30 días)
Elimina:
1. Registros de reportes de la base de datos
2. Carpeta media/reports/ (PDFs antiguos que ya no se usan)

Uso: python manage.py cleanup_old_reports [--days=30] [--dry-run]
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from G_Jobs.reports.models import Report
import os
import shutil


class Command(BaseCommand):
    help = 'Elimina reportes (registros BD) generados hace mas de N dias y carpeta media/reports/'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Número de días a mantener (por defecto: 30)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular la eliminación sin borrar nada'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']

        # Calcular fecha límite
        cutoff_date = timezone.now() - timedelta(days=days)

        self.stdout.write("="*80)
        self.stdout.write(f"LIMPIEZA DE REPORTES ANTIGUOS")
        self.stdout.write("="*80)
        self.stdout.write(f"Fecha limite: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write(f"Dias a mantener: {days}")
        self.stdout.write(f"Modo: {'SIMULACION (dry-run)' if dry_run else 'ELIMINACION REAL'}")
        self.stdout.write("")

        # Buscar reportes antiguos
        old_reports = Report.objects.filter(
            generated_at__lt=cutoff_date
        ).order_by('generated_at')

        total_reports = old_reports.count()

        if total_reports == 0:
            self.stdout.write(self.style.SUCCESS("No hay reportes antiguos para eliminar."))
        else:
            self.stdout.write(f"Reportes encontrados: {total_reports}")

        self.stdout.write("")

        # Estadísticas
        deleted_count = 0
        errors = []

        for report in old_reports:
            try:
                # Información del reporte
                report_info = (
                    f"  ID {report.id}: {report.get_report_type_display()} "
                    f"({report.period_start} - {report.period_end}) "
                    f"generado el {report.generated_at.strftime('%Y-%m-%d')}"
                )

                if dry_run:
                    self.stdout.write(self.style.WARNING(f"[SIMULACION] {report_info}"))
                else:
                    # Eliminar registro de la BD
                    report.delete()
                    deleted_count += 1
                    self.stdout.write(self.style.SUCCESS(f"[ELIMINADO] {report_info}"))

            except Exception as e:
                error_msg = f"Error al eliminar reporte ID {report.id}: {str(e)}"
                errors.append(error_msg)
                self.stdout.write(self.style.ERROR(f"[ERROR] {error_msg}"))

        # Limpiar carpeta media/reports/
        self.stdout.write("")
        self.stdout.write("="*80)
        self.stdout.write("LIMPIEZA DE CARPETA MEDIA/REPORTS/")
        self.stdout.write("="*80)

        reports_media_path = os.path.join(settings.MEDIA_ROOT, 'reports')

        if os.path.exists(reports_media_path):
            # Calcular tamaño de la carpeta
            total_size = 0
            file_count = 0
            for dirpath, dirnames, filenames in os.walk(reports_media_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
                    file_count += 1

            total_size_mb = total_size / (1024 * 1024)

            self.stdout.write(f"Carpeta encontrada: {reports_media_path}")
            self.stdout.write(f"Archivos: {file_count}")
            self.stdout.write(f"Tamano total: {total_size_mb:.2f} MB")
            self.stdout.write("")

            if dry_run:
                self.stdout.write(self.style.WARNING(
                    f"[SIMULACION] Se eliminaria la carpeta completa ({file_count} archivos, {total_size_mb:.2f} MB)"
                ))
            else:
                try:
                    shutil.rmtree(reports_media_path)
                    self.stdout.write(self.style.SUCCESS(
                        f"[ELIMINADO] Carpeta eliminada ({file_count} archivos, {total_size_mb:.2f} MB liberados)"
                    ))
                except Exception as e:
                    errors.append(f"Error al eliminar carpeta media/reports/: {str(e)}")
                    self.stdout.write(self.style.ERROR(f"[ERROR] {str(e)}"))
        else:
            self.stdout.write(self.style.SUCCESS("Carpeta media/reports/ no existe (ya estaba limpia)"))

        # Resumen final
        self.stdout.write("")
        self.stdout.write("="*80)
        self.stdout.write("RESUMEN FINAL")
        self.stdout.write("="*80)

        if dry_run:
            self.stdout.write(f"Reportes que SERIAN eliminados de BD: {total_reports}")
            self.stdout.write(self.style.WARNING("MODO SIMULACION - No se elimino nada"))
        else:
            self.stdout.write(f"Reportes eliminados de la BD: {deleted_count} de {total_reports}")

        if errors:
            self.stdout.write("")
            self.stdout.write(self.style.ERROR(f"Errores encontrados: {len(errors)}"))
            for error in errors:
                self.stdout.write(f"  - {error}")
        else:
            if not dry_run:
                self.stdout.write("")
                self.stdout.write(self.style.SUCCESS("Limpieza completada exitosamente!"))
