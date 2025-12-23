"""
Script de prueba para diagnosticar el flujo completo de CVs y Postulaciones
Verifica:
1. CVs guardados en la base de datos
2. Postulaciones vinculadas a CVs
3. Endpoint de aplicaciones
4. Datos serializados correctamente
"""

import os
import sys
import django

# Configurar Django
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from G_Jobs.jobs.models import Job
from profiles.models import UserProfile, CompanyProfile
from G_Jobs.applicants.models import ApplicantCV, JobApplication
import json

User = get_user_model()
Application = JobApplication  # Alias para simplificar

print("=" * 80)
print("TEST DE FLUJO COMPLETO: CVs y Postulaciones")
print("=" * 80)

# ========== 1. VERIFICAR USUARIOS ==========
print("\n📋 1. VERIFICANDO USUARIOS")
print("-" * 80)

mauge_email = "mauge@gmail.com"
clau_email = "clau@gmail.com"

try:
    mauge_user = User.objects.get(email=mauge_email)
    print(f"✅ Postulante encontrado: {mauge_email}")
    print(f"   - ID: {mauge_user.id}")
    print(f"   - Nombre: {mauge_user.get_full_name()}")
except User.DoesNotExist:
    print(f"❌ Postulante NO encontrado: {mauge_email}")
    mauge_user = None

try:
    clau_user = User.objects.get(email=clau_email)
    print(f"✅ Empleador encontrado: {clau_email}")
    print(f"   - ID: {clau_user.id}")
    print(f"   - Nombre: {clau_user.get_full_name()}")
except User.DoesNotExist:
    print(f"❌ Empleador NO encontrado: {clau_email}")
    clau_user = None

if not mauge_user or not clau_user:
    print("\n❌ ERROR: Faltan usuarios. No se puede continuar.")
    sys.exit(1)

# ========== 2. VERIFICAR CVs DEL POSTULANTE ==========
print("\n📋 2. VERIFICANDO CVs GUARDADOS")
print("-" * 80)

cvs = ApplicantCV.objects.filter(user=mauge_user).order_by('-created_at')
print(f"Total de CVs guardados: {cvs.count()}")

if cvs.count() == 0:
    print("⚠️ No hay CVs guardados para este usuario")
else:
    for idx, cv in enumerate(cvs, 1):
        print(f"\n  CV #{idx}:")
        print(f"  - ID: {cv.id}")
        print(f"  - Nombre: {cv.name}")
        print(f"  - Tipo: {cv.cv_type}")
        print(f"  - Archivo: {cv.file.name if cv.file else 'N/A'}")
        print(f"  - URL: {cv.file.url if cv.file else 'N/A'}")
        print(f"  - Existe físicamente: {cv.file.storage.exists(cv.file.name) if cv.file else False}")
        print(f"  - Creado: {cv.created_at}")

        if cv.cv_data:
            print(f"  - Datos CV (JSON): {len(str(cv.cv_data))} caracteres")
            if 'personalInfo' in cv.cv_data:
                print(f"    * Nombre completo: {cv.cv_data['personalInfo'].get('fullName', 'N/A')}")

# ========== 3. VERIFICAR TRABAJOS PUBLICADOS POR CLAU ==========
print("\n📋 3. VERIFICANDO TRABAJOS PUBLICADOS")
print("-" * 80)

try:
    clau_profile = UserProfile.objects.get(user=clau_user)
    print(f"✅ Perfil de usuario encontrado: {clau_profile.id}")

    # Buscar empresa
    try:
        company_profile = CompanyProfile.objects.get(user_profile=clau_profile)
        print(f"✅ Perfil de empresa encontrado: {company_profile.company_name}")
    except CompanyProfile.DoesNotExist:
        print("⚠️ No hay perfil de empresa")
        company_profile = None

except UserProfile.DoesNotExist:
    print(f"❌ No se encontró perfil de usuario para {clau_email}")
    clau_profile = None
    company_profile = None

if clau_profile:
    jobs = Job.objects.filter(
        user_profile=clau_profile,
        status__in=['published', 'active']
    ).order_by('-created_at')

    print(f"\nTotal de trabajos publicados: {jobs.count()}")

    if jobs.count() == 0:
        print("⚠️ No hay trabajos publicados")
    else:
        for idx, job in enumerate(jobs, 1):
            print(f"\n  Trabajo #{idx}:")
            print(f"  - ID: {job.id}")
            print(f"  - Título: {job.title}")
            print(f"  - Estado: {job.status}")
            print(f"  - Creado: {job.created_at}")

            # Buscar aplicaciones a este trabajo
            apps = Application.objects.filter(job=job)
            print(f"  - Postulaciones: {apps.count()}")

            if apps.count() > 0:
                for app_idx, app in enumerate(apps, 1):
                    print(f"\n    Postulación #{app_idx}:")
                    print(f"    - ID: {app.id}")
                    print(f"    - Postulante: {app.user.email}")
                    print(f"    - Estado: {app.status}")
                    print(f"    - Fecha: {app.created_at}")
                    print(f"    - Tiene CV: {'✅ SÍ' if app.cv else '❌ NO'}")

                    if app.cv:
                        print(f"    - CV ID: {app.cv.id}")
                        print(f"    - CV Nombre: {app.cv.name}")
                        print(f"    - CV Tipo: {app.cv.cv_type}")
                        print(f"    - CV Archivo: {app.cv.file.name if app.cv.file else 'N/A'}")
                        print(f"    - CV URL: {app.cv.file.url if app.cv.file else 'N/A'}")

                        # Verificar si el archivo existe físicamente
                        if app.cv.file:
                            exists = app.cv.file.storage.exists(app.cv.file.name)
                            print(f"    - Archivo existe: {'✅ SÍ' if exists else '❌ NO'}")
                            if exists:
                                size = app.cv.file.size
                                print(f"    - Tamaño: {size} bytes ({size/1024:.2f} KB)")

# ========== 4. SIMULAR ENDPOINT DE APLICACIONES ==========
print("\n📋 4. SIMULANDO ENDPOINT /api/jobs/{id}/applications")
print("-" * 80)

if clau_profile and jobs.count() > 0:
    # Tomar el primer trabajo
    test_job = jobs.first()
    print(f"\nProbando con trabajo: {test_job.title} (ID: {test_job.id})")

    # Obtener aplicaciones
    applications = Application.objects.filter(job=test_job).order_by('-created_at')

    print(f"Total de aplicaciones: {applications.count()}")

    if applications.count() > 0:
        print("\n📦 DATOS QUE SE ENVIARÍAN AL FRONTEND:")
        print("-" * 80)

        for app in applications:
            # Simular serialización
            app_data = {
                'id': str(app.id),
                'applicantName': app.applicant_name or 'Sin nombre',
                'applicantEmail': app.applicant_email or 'Sin email',
                'applicantPhone': app.applicant_phone,
                'applicantWhatsapp': app.applicant_whatsapp,
                'status': app.status,
                'coverLetter': app.cover_letter,
                'createdAt': app.created_at.isoformat() if app.created_at else None,
                'recruiterNotes': app.employer_notes,
            }

            # CV Info
            if app.cv:
                cv_info = {
                    'id': str(app.cv.id),
                    'name': app.cv.name,
                    'type': app.cv.cv_type,
                    'file_url': app.cv.file.url if app.cv.file else None,
                    'file_name': app.cv.name,
                    'full_name': app.cv.cv_data.get('personalInfo', {}).get('fullName') if app.cv.cv_data else None,
                    'cv_data': app.cv.cv_data if app.cv.cv_type == 'created' else None
                }
                app_data['cv'] = cv_info
                print(f"\n✅ Aplicación con CV:")
            else:
                app_data['cv'] = None
                print(f"\n❌ Aplicación SIN CV:")

            # Imprimir JSON formateado
            print(json.dumps(app_data, indent=2, ensure_ascii=False))
    else:
        print("⚠️ No hay aplicaciones para este trabajo")

# ========== 5. RESUMEN Y DIAGNÓSTICO ==========
print("\n" + "=" * 80)
print("📊 RESUMEN Y DIAGNÓSTICO")
print("=" * 80)

total_cvs = ApplicantCV.objects.filter(user=mauge_user).count()
total_apps = Application.objects.filter(user=mauge_user).count()
apps_with_cv = Application.objects.filter(user=mauge_user, cv__isnull=False).count()
apps_without_cv = Application.objects.filter(user=mauge_user, cv__isnull=True).count()

print(f"\n👤 Usuario: {mauge_email}")
print(f"  - CVs guardados: {total_cvs}")
print(f"  - Postulaciones totales: {total_apps}")
print(f"  - Postulaciones CON CV: {apps_with_cv} {'✅' if apps_with_cv > 0 else '❌'}")
print(f"  - Postulaciones SIN CV: {apps_without_cv} {'⚠️' if apps_without_cv > 0 else '✅'}")

if clau_profile:
    total_jobs = Job.objects.filter(user_profile=clau_profile, status__in=['published', 'active']).count()
    total_received_apps = Application.objects.filter(job__user_profile=clau_profile).count()

    print(f"\n🏢 Empleador: {clau_email}")
    print(f"  - Trabajos publicados: {total_jobs}")
    print(f"  - Postulaciones recibidas: {total_received_apps}")
    print(f"  - Postulaciones CON CV: {Application.objects.filter(job__user_profile=clau_profile, cv__isnull=False).count()}")

print("\n" + "=" * 80)
print("✅ TEST COMPLETADO")
print("=" * 80)
