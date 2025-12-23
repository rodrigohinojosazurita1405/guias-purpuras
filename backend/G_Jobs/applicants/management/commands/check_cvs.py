from django.core.management.base import BaseCommand
from G_Jobs.applicants.models import JobApplication, ApplicantCV
from G_Jobs.jobs.models import Job
from django.contrib.auth import get_user_model
import os
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = 'Verificar CVs en base de datos y sistema de archivos'

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write("VERIFICANDO CVS EN BASE DE DATOS")
        self.stdout.write("=" * 80)

        # Buscar usuario mauge
        try:
            mauge = User.objects.get(email='mauge@gmail.com')
            self.stdout.write(f"\nUsuario encontrado: {mauge.email}")
        except User.DoesNotExist:
            self.stdout.write("\nERROR: Usuario mauge@gmail.com no existe")
            return

        # Buscar CVs de mauge
        cvs = ApplicantCV.objects.filter(applicant=mauge)
        self.stdout.write(f"\nCVs en BD para mauge@gmail.com: {cvs.count()}")

        if cvs.count() > 0:
            for cv in cvs:
                self.stdout.write(f"\n  CV ID: {cv.id}")
                self.stdout.write(f"  Nombre: {cv.name}")
                self.stdout.write(f"  Tipo: {cv.cv_type}")
                if cv.file:
                    self.stdout.write(f"  Archivo: {cv.file.name}")
                    file_path = os.path.join(settings.MEDIA_ROOT, cv.file.name)
                    exists = os.path.exists(file_path)
                    self.stdout.write(f"  Existe en disco: {exists}")
                else:
                    self.stdout.write(f"  Archivo: Sin archivo")

        # Verificar archivos en el sistema
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("VERIFICANDO ARCHIVOS EN SISTEMA")
        self.stdout.write("=" * 80)

        cv_folder = os.path.join(settings.MEDIA_ROOT, 'applicant_cvs')
        self.stdout.write(f"\nBuscando en: {cv_folder}")

        if os.path.exists(cv_folder):
            files = os.listdir(cv_folder)
            self.stdout.write(f"Archivos encontrados: {len(files)}")
            for file in files:
                self.stdout.write(f"  - {file}")
        else:
            self.stdout.write("ERROR: La carpeta applicant_cvs no existe")

        # Verificar postulaciones sin CV
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("POSTULACIONES SIN CV")
        self.stdout.write("=" * 80)

        apps_no_cv = JobApplication.objects.filter(applicant=mauge, cv__isnull=True)
        self.stdout.write(f"\nPostulaciones sin CV: {apps_no_cv.count()}")

        for app in apps_no_cv:
            self.stdout.write(f"\n  Job: {app.job.title} (ID: {app.job.id})")
            self.stdout.write(f"  Fecha: {app.applied_at}")

        self.stdout.write("\n" + "=" * 80)
