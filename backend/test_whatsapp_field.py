#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test para verificar que el campo whatsapp se guarda correctamente
"""
import os
import sys
import django

# Fix para encoding en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from G_Jobs.jobs.models import Job
from datetime import date, timedelta

def test_whatsapp_field():
    """Prueba la generación y guardado del campo whatsapp"""

    print("\n" + "="*60)
    print("TEST: Campo WhatsApp en modelo Job")
    print("="*60)

    # 1. Crear un trabajo de prueba con whatsappNumber
    print("\n1. Creando trabajo de prueba con número de WhatsApp...")

    # Eliminar trabajos de prueba anteriores
    Job.objects.filter(title="Test WhatsApp Job").delete()

    # Datos de prueba
    whatsapp_number = "65324767"
    expected_whatsapp_link = "https://wa.me/59165324767"

    job = Job.objects.create(
        title="Test WhatsApp Job",
        companyName="Test Company",
        description="Test description for WhatsApp functionality",
        jobCategory="Tecnología",
        city="La Paz",
        contractType="Tiempo Completo",
        modality="presencial",
        salaryType="negotiable",
        vacancies=1,
        expiryDate=date.today() + timedelta(days=30),
        applicationDeadline=date.today() + timedelta(days=25),
        email="test@example.com",
        applicationType="external",
        # Campo whatsapp - debe ser el enlace generado
        whatsapp=expected_whatsapp_link,
        selectedPlan="estandar",
        status="active"
    )

    print(f"   ✓ Trabajo creado: {job.id}")
    print(f"   ✓ Título: {job.title}")
    print(f"   ✓ Número ingresado: {whatsapp_number}")
    print(f"   ✓ Enlace esperado: {expected_whatsapp_link}")

    # 2. Verificar que se guardó correctamente
    print("\n2. Verificando que el enlace se guardó en la DB...")
    job_from_db = Job.objects.get(id=job.id)

    print(f"   WhatsApp en DB: {job_from_db.whatsapp}")
    print(f"   Email en DB: {job_from_db.email}")
    print(f"   Website en DB: {job_from_db.website}")
    print(f"   ExternalURL en DB: {job_from_db.externalApplicationUrl}")

    # 3. Validar
    if job_from_db.whatsapp == expected_whatsapp_link:
        print("\n   ✅ ÉXITO: El enlace de WhatsApp se guardó correctamente")
    else:
        print(f"\n   ❌ ERROR: Enlace incorrecto")
        print(f"      Esperado: {expected_whatsapp_link}")
        print(f"      Obtenido: {job_from_db.whatsapp}")

    # 4. Verificar últimos 3 trabajos para ver si tienen WhatsApp
    print("\n3. Verificando últimos 3 trabajos en la DB...")
    recent_jobs = Job.objects.filter(
        applicationType='external'
    ).order_by('-createdAt')[:3]

    print(f"\n   Total de trabajos externos: {recent_jobs.count()}")
    for i, j in enumerate(recent_jobs, 1):
        print(f"\n   Trabajo {i}:")
        print(f"      ID: {j.id}")
        print(f"      Título: {j.title}")
        print(f"      WhatsApp: {j.whatsapp or '(vacío)'}")
        print(f"      Email: {j.email or '(vacío)'}")
        print(f"      Website: {j.website or '(vacío)'}")
        print(f"      ExternalURL: {j.externalApplicationUrl or '(vacío)'}")

    # 5. Limpiar
    print("\n4. Limpiando trabajo de prueba...")
    job.delete()
    print("   ✓ Trabajo eliminado")

    print("\n" + "="*60)
    print("TEST COMPLETADO")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_whatsapp_field()
