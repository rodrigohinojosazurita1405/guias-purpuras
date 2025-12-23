import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'G_Jobs.settings')

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from G_Jobs.applicants.models import JobApplication
from G_Jobs.jobs.models import Job
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 80)
print("VERIFICANDO POSTULACIONES EN LA BASE DE DATOS")
print("=" * 80)

# Buscar trabajos de clau@gmail.com
jobs = Job.objects.filter(email='clau@gmail.com')
print(f"\n📋 Trabajos de clau@gmail.com: {jobs.count()}")

# Buscar postulaciones
all_apps = JobApplication.objects.filter(job__email='clau@gmail.com')
print(f"\n📨 Total postulaciones a trabajos de clau@gmail.com: {all_apps.count()}")

if all_apps.count() > 0:
    print("\nDETALLE DE POSTULACIONES:")
    for app in all_apps:
        print(f"\n  ID: {app.id}")
        print(f"  Trabajo: {app.job.title} (ID: {app.job.id})")
        print(f"  Postulante: {app.applicant.email}")
        print(f"  Estado: {app.status}")
        print(f"  CV: {app.cv.name if app.cv else 'Sin CV'}")
        print(f"  Notas empleador: {app.employer_notes[:50] if app.employer_notes else 'Sin notas'}")
        print(f"  Fecha: {app.applied_at}")

# Verificar específicamente los trabajos que dieron error 500
error_jobs = ['8cf0d9d6', 'cd2dc7ad', '3be6182c', '27a0722c']
print("\n" + "=" * 80)
print("VERIFICANDO TRABAJOS QUE DIERON ERROR 500:")
print("=" * 80)

for job_id in error_jobs:
    try:
        job = Job.objects.get(id=job_id)
        apps = JobApplication.objects.filter(job=job)
        print(f"\n📋 Job: {job.title} (ID: {job_id})")
        print(f"   Email: {job.email}")
        print(f"   Postulaciones: {apps.count()}")

        if apps.count() > 0:
            for app in apps:
                print(f"   - {app.applicant.email} | CV: {app.cv.name if app.cv else 'N/A'}")
                # Verificar si tiene el atributo employer_notes
                print(f"     ✓ employer_notes existe: {hasattr(app, 'employer_notes')}")
                if hasattr(app, 'employer_notes'):
                    print(f"     ✓ Valor: {app.employer_notes[:30] if app.employer_notes else 'vacío'}")
    except Job.DoesNotExist:
        print(f"\n❌ Job {job_id} no existe")
    except Exception as e:
        print(f"\n❌ Error en job {job_id}: {str(e)}")

print("\n" + "=" * 80)
