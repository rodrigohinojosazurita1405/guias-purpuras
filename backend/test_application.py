"""
Script de prueba para postulación a un trabajo
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from G_Jobs.jobs.models import Job
from G_Jobs.applicants.models import ApplicantCV, JobApplication
import json

User = get_user_model()

def test_application():
    print("\n" + "="*60)
    print("TEST DE POSTULACIÓN")
    print("="*60 + "\n")

    # 1. Buscar un usuario postulante
    print("1. Buscando usuario postulante...")
    try:
        applicant = User.objects.filter(role='applicant').first()
        if not applicant:
            print("[ERROR] No hay usuarios postulantes en la BD")
            return
        print(f"[OK] Usuario encontrado: {applicant.email}")
    except Exception as e:
        print(f"[ERROR] Error buscando usuario: {e}")
        return

    # 2. Buscar un trabajo activo
    print("\n2. Buscando trabajo activo...")
    try:
        job = Job.objects.filter(status='active').first()
        if not job:
            print("[ERROR] No hay trabajos activos en la BD")
            return
        print(f"[OK] Trabajo encontrado: {job.title} (ID: {job.id})")
        print(f"   Tipo de aplicación: {job.applicationType}")
        print(f"   Email empresa: {job.email}")
    except Exception as e:
        print(f"[ERROR] Error buscando trabajo: {e}")
        return

    # 3. Verificar si ya existe una postulación
    print("\n3. Verificando postulaciones existentes...")
    try:
        existing = JobApplication.objects.filter(
            applicant=applicant,
            job=job
        ).first()
        if existing:
            print(f"[WARN]  Ya existe una postulación de {applicant.email} a este trabajo")
            print(f"   Eliminando postulación anterior para la prueba...")
            existing.delete()
            print("[OK] Postulación anterior eliminada")
    except Exception as e:
        print(f"[ERROR] Error verificando postulaciones: {e}")

    # 4. Verificar CVs del usuario
    print("\n4. Verificando CVs del usuario...")
    try:
        cvs = ApplicantCV.objects.filter(
            applicant=applicant,
            is_deleted=False
        )
        print(f"   CVs encontrados: {cvs.count()}")

        if cvs.count() == 0:
            print("   Creando CV de prueba...")
            cv = ApplicantCV.objects.create(
                applicant=applicant,
                cv_type='created',
                name='CV de Prueba',
                cv_data={
                    'personalInfo': {
                        'fullName': 'Usuario de Prueba',
                        'email': applicant.email
                    }
                }
            )
            print(f"[OK] CV creado: {cv.id}")
        else:
            cv = cvs.first()
            print(f"[OK] Usando CV existente: {cv.id}")
    except Exception as e:
        print(f"[ERROR] Error con CVs: {e}")
        return

    # 5. Verificar si el usuario está bloqueado
    print("\n5. Verificando si el usuario está bloqueado...")
    try:
        from G_Jobs.moderation.models import BlockedUser

        # Obtener el usuario de la empresa
        company_user = User.objects.filter(email=job.email, role='company').first()
        if company_user:
            block = BlockedUser.objects.filter(
                company=company_user,
                blocked_user=applicant
            ).first()

            if block:
                print(f"[ERROR] Usuario bloqueado por la empresa")
                print(f"   Razón: {block.get_reason_display()}")
                print(f"   Notas: {block.notes}")
                return
            else:
                print("[OK] Usuario NO está bloqueado")
        else:
            print("[WARN]  No se encontró el usuario de la empresa")
    except Exception as e:
        print(f"[ERROR] Error verificando bloqueo: {e}")

    # 6. Intentar crear la postulación
    print("\n6. Creando postulación...")
    try:
        application = JobApplication.objects.create(
            applicant=applicant,
            job=job,
            cv=cv,
            cover_letter='Esta es una carta de presentación de prueba',
            screening_answers={}
        )
        print(f"[OK] Postulación creada exitosamente!")
        print(f"   ID: {application.id}")
        print(f"   Estado: {application.status}")
        print(f"   Fecha: {application.applied_at}")

    except Exception as e:
        print(f"[ERROR] Error creando postulación: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n" + "="*60)
    print("TEST COMPLETADO EXITOSAMENTE [OK]")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_application()
