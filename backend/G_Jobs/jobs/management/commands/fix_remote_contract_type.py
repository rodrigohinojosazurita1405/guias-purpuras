"""
Management command para corregir trabajos con contractType='Remoto'
Cambia 'Remoto' a un tipo de contrato válido y establece modality='Remoto'
"""
from django.core.management.base import BaseCommand
from G_Jobs.jobs.models import Job


class Command(BaseCommand):
    help = 'Corrige trabajos con contractType="Remoto" (debería ser modalidad, no tipo)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué se haría sin realizar cambios',
        )
        parser.add_argument(
            '--default-contract-type',
            type=str,
            default='Tiempo Completo',
            help='Tipo de contrato por defecto para trabajos remotos (default: Tiempo Completo)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        default_contract_type = options['default_contract_type']

        # Encontrar todos los trabajos con contractType='Remoto'
        remote_jobs = Job.objects.filter(contractType='Remoto')
        count = remote_jobs.count()

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No hay trabajos con contractType="Remoto" para corregir.')
            )
            return

        # Mostrar información
        self.stdout.write(
            self.style.WARNING(f'\nSe encontraron {count} trabajos con contractType="Remoto":\n')
        )

        for job in remote_jobs:
            self.stdout.write(
                f'  - ID: {job.id} | {job.title} | Empresa: {job.companyName or "Anonima"}'
            )

        if dry_run:
            self.stdout.write(
                self.style.NOTICE(
                    f'\n[DRY RUN] Se cambiaria:\n'
                    f'   contractType: "Remoto" -> "{default_contract_type}"\n'
                    f'   modality: (actual) -> "Remoto"\n'
                )
            )
            return

        # Realizar los cambios
        self.stdout.write(
            self.style.NOTICE(
                f'\nAplicando cambios:\n'
                f'   contractType: "Remoto" -> "{default_contract_type}"\n'
                f'   modality: (actual) -> "Remoto"\n'
            )
        )

        updated_count = 0
        for job in remote_jobs:
            old_modality = job.modality
            job.contractType = default_contract_type
            job.modality = 'Remoto'
            job.save()
            updated_count += 1

            self.stdout.write(
                f'  OK {job.title} - modality: "{old_modality}" -> "Remoto"'
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSe actualizaron {updated_count} trabajos exitosamente.\n'
            )
        )

        # Verificación final
        remaining = Job.objects.filter(contractType='Remoto').count()
        if remaining == 0:
            self.stdout.write(
                self.style.SUCCESS('Verificacion: No quedan trabajos con contractType="Remoto"')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Advertencia: Aun quedan {remaining} trabajos con contractType="Remoto"')
            )
