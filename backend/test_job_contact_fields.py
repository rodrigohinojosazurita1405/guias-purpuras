"""
Script de prueba para verificar que los campos de contacto se guardan correctamente
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

User = get_user_model()

def test_contact_fields():
    print("\n" + "="*60)
    print("TEST DE CAMPOS DE CONTACTO EN JOB")
    print("="*60 + "\n")

    # 1. Buscar el job creado por el usuario
    print("1. Buscando job 'Sefasfafaefafaefa'...")
    try:
        job = Job.objects.filter(title__icontains='Sefasfafaefafaefa').first()
        if not job:
            print("[ERROR] No se encontró el job")
            return

        print(f"[OK] Job encontrado: {job.title} (ID: {job.id})")
        print(f"\n2. Verificando campos de contacto:")
        print(f"   - WhatsApp: [{job.whatsapp}]")
        print(f"   - Website: [{job.website}]")
        print(f"   - Application Instructions: [{job.applicationInstructions}]")
        print(f"   - External URL: [{job.externalApplicationUrl}]")
        print(f"   - Email: [{job.email}]")

        # Verificar si algún método de contacto está disponible
        has_contact = (
            job.externalApplicationUrl or
            job.email or
            job.whatsapp or
            job.website
        )

        print(f"\n3. ¿Tiene al menos un método de contacto? {'✓ SÍ' if has_contact else '✗ NO'}")

        if not has_contact:
            print("\n[ERROR] El job NO tiene ningún método de contacto configurado")
            print("El usuario debería ver el mensaje: 'Esta oferta no tiene configurado ningún método de contacto'")
        else:
            print("\n[OK] El job tiene al menos un método de contacto")

    except Exception as e:
        print(f"[ERROR] Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*60)
    print("TEST COMPLETADO")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_contact_fields()
