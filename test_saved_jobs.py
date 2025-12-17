"""
Script de prueba para endpoints de trabajos guardados
Ejecutar desde la raíz del proyecto backend
"""

import os
import django
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configurar Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from G_Jobs.jobs.models import Job
from G_Jobs.applicants.models import SavedJob

User = get_user_model()

def test_saved_jobs():
    print("\n" + "="*60)
    print("TESTING SAVED JOBS FUNCTIONALITY")
    print("="*60 + "\n")

    # 1. Buscar usuario postulante
    print("1️⃣  Buscando usuario postulante...")
    users = User.objects.filter(role='applicant')
    if not users.exists():
        print("❌ No hay usuarios postulantes en la BD")
        return

    user = users.first()
    print(f"✅ Usuario encontrado: {user.email} (ID: {user.id})")

    # 2. Buscar un trabajo activo
    print("\n2️⃣  Buscando trabajo activo...")
    jobs = Job.objects.filter(status='active')
    if not jobs.exists():
        print("❌ No hay trabajos activos en la BD")
        return

    job = jobs.first()
    print(f"✅ Trabajo encontrado: {job.title} (ID: {job.id})")

    # 3. Verificar si ya está guardado
    print("\n3️⃣  Verificando si el trabajo ya está guardado...")
    is_saved = SavedJob.objects.filter(user=user, job=job).exists()
    print(f"{'✅' if is_saved else '❌'} Estado actual: {'GUARDADO' if is_saved else 'NO GUARDADO'}")

    # 4. Guardar el trabajo (si no está guardado)
    if not is_saved:
        print("\n4️⃣  Guardando trabajo...")
        saved_job = SavedJob.objects.create(user=user, job=job)
        print(f"✅ Trabajo guardado exitosamente!")
        print(f"   SavedJob ID: {saved_job.id}")
        print(f"   Saved At: {saved_job.saved_at}")
    else:
        print("\n4️⃣  El trabajo ya estaba guardado, omitiendo creación")

    # 5. Listar todos los trabajos guardados del usuario
    print("\n5️⃣  Listando todos los trabajos guardados del usuario...")
    saved_jobs = SavedJob.objects.filter(user=user).select_related('job')
    print(f"✅ Total de trabajos guardados: {saved_jobs.count()}")

    for idx, saved in enumerate(saved_jobs, 1):
        print(f"\n   {idx}. {saved.job.title}")
        print(f"      Company: {saved.job.companyName}")
        print(f"      Saved At: {saved.saved_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"      Job Status: {saved.job.status}")

    # 6. URLs que deberían funcionar
    print("\n" + "="*60)
    print("ENDPOINTS DISPONIBLES:")
    print("="*60)
    print(f"\n✅ POST   /api/saved-jobs/save/")
    print(f"   Body: {{'job_id': '{job.id}'}}")
    print(f"\n✅ DELETE /api/saved-jobs/unsave/")
    print(f"   Body: {{'job_id': '{job.id}'}}")
    print(f"\n✅ GET    /api/saved-jobs/check/{job.id}/")
    print(f"\n✅ GET    /api/saved-jobs/")
    print(f"   Query: ?limit=20&offset=0")

    print("\n" + "="*60)
    print("TEST COMPLETADO")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_saved_jobs()
