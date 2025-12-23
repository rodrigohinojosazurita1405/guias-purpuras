from django.core.management.base import BaseCommand
from G_Jobs.applicants.models import JobApplication
from G_Jobs.jobs.models import Job


class Command(BaseCommand):
    help = 'Verificar postulaciones en la base de datos'

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write("VERIFICANDO POSTULACIONES")
        self.stdout.write("=" * 80)

        # Postulaciones a trabajos de clau@gmail.com
        all_apps = JobApplication.objects.filter(job__email='clau@gmail.com')
        self.stdout.write(f"\nTotal postulaciones a clau@gmail.com: {all_apps.count()}")

        if all_apps.count() > 0:
            self.stdout.write("\nDETALLE:")
            for app in all_apps:
                self.stdout.write(f"\n  Trabajo: {app.job.title} (ID: {app.job.id})")
                self.stdout.write(f"  Postulante: {app.applicant.email}")
                self.stdout.write(f"  CV: {app.cv.name if app.cv else 'Sin CV'}")
                self.stdout.write(f"  employer_notes existe: {hasattr(app, 'employer_notes')}")

        # Jobs con error
        error_jobs = ['8cf0d9d6', 'cd2dc7ad', '3be6182c', '27a0722c']
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("JOBS QUE DIERON ERROR 500:")

        for job_id in error_jobs:
            try:
                job = Job.objects.get(id=job_id)
                apps = JobApplication.objects.filter(job=job)
                self.stdout.write(f"\n{job.title} | Apps: {apps.count()}")

                for app in apps:
                    self.stdout.write(f"   - {app.applicant.email}")
                    self.stdout.write(f"     employer_notes: {hasattr(app, 'employer_notes')}")
            except Job.DoesNotExist:
                self.stdout.write(f"\nJob {job_id} no existe")
