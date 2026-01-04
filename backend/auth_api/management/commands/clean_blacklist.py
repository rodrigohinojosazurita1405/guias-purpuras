"""
Management command para limpiar tokens expirados de la blacklist.

Este comando elimina:
1. Tokens en la blacklist cuya fecha de expiración ya pasó
2. Outstanding tokens que ya expiraron (y no están en uso)

Se recomienda ejecutar este comando periódicamente (diariamente) para mantener
la base de datos limpia y mejorar el rendimiento de las consultas de validación.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)


class Command(BaseCommand):
    help = (
        "Elimina tokens expirados de la blacklist y outstanding tokens. "
        "Esto mejora el rendimiento de las consultas de validación de tokens."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra cuántos tokens se eliminarían sin borrar realmente',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Muestra información detallada de la limpieza',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        verbose = options['verbose']
        now = timezone.now()

        # Estadísticas iniciales
        total_outstanding_before = OutstandingToken.objects.count()
        total_blacklisted_before = BlacklistedToken.objects.count()

        self.stdout.write(self.style.MIGRATE_HEADING("=" * 70))
        self.stdout.write(self.style.MIGRATE_HEADING("LIMPIEZA DE TOKENS EXPIRADOS"))
        self.stdout.write(self.style.MIGRATE_HEADING("=" * 70))
        self.stdout.write("")

        # Mostrar estado actual
        self.stdout.write(self.style.WARNING("Estado actual de la base de datos:"))
        self.stdout.write(f"   • Outstanding Tokens: {total_outstanding_before}")
        self.stdout.write(f"   • Blacklisted Tokens: {total_blacklisted_before}")
        self.stdout.write("")

        # 1. Encontrar tokens en blacklist que ya expiraron
        expired_blacklisted = BlacklistedToken.objects.filter(
            token__expires_at__lt=now
        )
        count_blacklisted = expired_blacklisted.count()

        if verbose and count_blacklisted > 0:
            self.stdout.write(self.style.WARNING("Tokens en blacklist expirados:"))
            for bl_token in expired_blacklisted[:10]:  # Mostrar solo los primeros 10
                self.stdout.write(
                    f"   • Usuario: {bl_token.token.user} | "
                    f"Expiró: {bl_token.token.expires_at.strftime('%Y-%m-%d %H:%M')} | "
                    f"Blacklisted: {bl_token.blacklisted_at.strftime('%Y-%m-%d %H:%M')}"
                )
            if count_blacklisted > 10:
                self.stdout.write(f"   ... y {count_blacklisted - 10} más")
            self.stdout.write("")

        # 2. Encontrar outstanding tokens que ya expiraron
        expired_outstanding = OutstandingToken.objects.filter(expires_at__lt=now)
        count_outstanding = expired_outstanding.count()

        if verbose and count_outstanding > 0:
            self.stdout.write(self.style.WARNING("Outstanding tokens expirados:"))
            for token in expired_outstanding[:10]:
                self.stdout.write(
                    f"   • Usuario: {token.user} | "
                    f"Creado: {token.created_at.strftime('%Y-%m-%d %H:%M') if token.created_at else 'N/A'} | "
                    f"Expiró: {token.expires_at.strftime('%Y-%m-%d %H:%M')}"
                )
            if count_outstanding > 10:
                self.stdout.write(f"   ... y {count_outstanding - 10} más")
            self.stdout.write("")

        # Resumen de lo que se va a eliminar
        self.stdout.write(self.style.WARNING("Tokens a eliminar:"))
        self.stdout.write(f"   • Blacklisted tokens expirados: {count_blacklisted}")
        self.stdout.write(f"   • Outstanding tokens expirados: {count_outstanding}")
        self.stdout.write("")

        if dry_run:
            self.stdout.write(
                self.style.NOTICE("Modo DRY-RUN: No se eliminara nada realmente")
            )
            self.stdout.write("")
            return

        # Realizar la eliminación
        if count_blacklisted > 0 or count_outstanding > 0:
            self.stdout.write(self.style.WARNING("Ejecutando limpieza..."))
            self.stdout.write("")

            # Los blacklisted tokens se eliminan automáticamente cuando se elimina
            # el outstanding token (CASCADE), así que solo eliminamos outstanding
            deleted_count, deleted_details = expired_outstanding.delete()

            # Estadísticas finales
            total_outstanding_after = OutstandingToken.objects.count()
            total_blacklisted_after = BlacklistedToken.objects.count()

            self.stdout.write(self.style.SUCCESS("Limpieza completada exitosamente"))
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("Resultados:"))
            self.stdout.write(
                f"   • Outstanding Tokens eliminados: "
                f"{total_outstanding_before - total_outstanding_after}"
            )
            self.stdout.write(
                f"   • Blacklisted Tokens eliminados: "
                f"{total_blacklisted_before - total_blacklisted_after}"
            )
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("Estado final:"))
            self.stdout.write(f"   • Outstanding Tokens restantes: {total_outstanding_after}")
            self.stdout.write(f"   • Blacklisted Tokens restantes: {total_blacklisted_after}")
            self.stdout.write("")

            if verbose:
                self.stdout.write(self.style.NOTICE("Detalles de eliminacion:"))
                for model, count in deleted_details.items():
                    if count > 0:
                        self.stdout.write(f"   • {model}: {count}")
                self.stdout.write("")

            # Calcular mejora en rendimiento
            improvement_pct = 0
            if total_blacklisted_before > 0:
                improvement_pct = (
                    (total_blacklisted_before - total_blacklisted_after)
                    / total_blacklisted_before
                    * 100
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Mejora en rendimiento: ~{improvement_pct:.1f}% "
                    f"(menos registros a consultar en cada validacion)"
                )
            )
            self.stdout.write("")
        else:
            self.stdout.write(
                self.style.SUCCESS("No hay tokens expirados para limpiar. Base de datos limpia.")
            )
            self.stdout.write("")

        self.stdout.write(self.style.MIGRATE_HEADING("=" * 70))
