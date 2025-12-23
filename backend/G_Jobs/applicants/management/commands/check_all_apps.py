from django.core.management.base import BaseCommand
from G_Jobs.applicants.models import JobApplication
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Verificar TODAS las postulaciones de mauge'

    def handle(self, *args, **options):
        try:
            mauge = User.objects.get(email='mauge@gmail.com')
        except User.DoesNotExist:
            self.stdout.write("ERROR: Usuario no existe")
            return

        apps = JobApplication.objects.filter(applicant=mauge).order_by('-applied_at')

        self.stdout.write("=" * 80)
        self.stdout.write(f"TODAS LAS POSTULACIONES DE {mauge.email}")
        self.stdout.write("=" * 80)
        self.stdout.write(f"\nTotal: {apps.count()}\n")

        for app in apps:
            self.stdout.write(f"\n  Job: {app.job.title}")
            self.stdout.write(f"  Job ID: {app.job.id}")
            self.stdout.write(f"  Empleador: {app.job.email}")
            self.stdout.write(f"  Fecha: {app.applied_at}")
            self.stdout.write(f"  Status: {app.status}")

            if app.cv:
                self.stdout.write(f"  CV VINCULADO: {app.cv.name} (ID: {app.cv.id})")
                self.stdout.write(f"  Tipo CV: {app.cv.cv_type}")
                if app.cv.file:
                    self.stdout.write(f"  Archivo: {app.cv.file.name}")
            else:
                self.stdout.write(f"  CV: SIN CV VINCULADO")

            self.stdout.write("  " + "-" * 76)

        self.stdout.write("\n" + "=" * 80)
