"""
Script para probar los endpoints de saved-jobs con requests HTTP
Simula exactamente lo que hace el frontend
"""

import os
import django
import sys
import requests
import json

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configurar Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from G_Jobs.jobs.models import Job
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def test_api_endpoints():
    print("\n" + "="*60)
    print("TESTING SAVED-JOBS API ENDPOINTS")
    print("="*60 + "\n")

    # 1. Obtener usuario y generar tokens JWT
    print("1️⃣  Obteniendo usuario y generando tokens JWT...")
    user = User.objects.filter(role='applicant').first()
    if not user:
        print("❌ No hay usuarios postulantes")
        return

    print(f"✅ Usuario: {user.email}")

    # Generar tokens JWT
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    print(f"✅ Access Token generado: {access_token[:50]}...")

    # 2. Obtener un trabajo
    print("\n2️⃣  Obteniendo trabajo activo...")
    job = Job.objects.filter(status='active').first()
    if not job:
        print("❌ No hay trabajos activos")
        return

    print(f"✅ Trabajo: {job.title} (ID: {job.id})")

    # Base URL
    BASE_URL = "http://localhost:8000"

    # 3. Probar CHECK endpoint
    print("\n3️⃣  Probando GET /api/saved-jobs/check/{job_id}/ ...")
    url = f"{BASE_URL}/api/saved-jobs/check/{job.id}/"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    print(f"   URL: {url}")
    print(f"   Headers: Authorization: Bearer {access_token[:30]}...")

    try:
        response = requests.get(url, headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        if response.status_code == 200:
            print("   ✅ CHECK endpoint funciona!")
        else:
            print(f"   ❌ CHECK endpoint falló: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # 4. Probar SAVE endpoint
    print("\n4️⃣  Probando POST /api/saved-jobs/save/ ...")
    url = f"{BASE_URL}/api/saved-jobs/save/"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    body = {'job_id': job.id}

    print(f"   URL: {url}")
    print(f"   Headers: {headers}")
    print(f"   Body: {body}")

    try:
        response = requests.post(url, headers=headers, json=body)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        if response.status_code in [200, 201]:
            print("   ✅ SAVE endpoint funciona!")
        else:
            print(f"   ❌ SAVE endpoint falló: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # 5. Probar LIST endpoint
    print("\n5️⃣  Probando GET /api/saved-jobs/ ...")
    url = f"{BASE_URL}/api/saved-jobs/"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    print(f"   URL: {url}")

    try:
        response = requests.get(url, headers=headers)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Total guardados: {data.get('total', 0)}")
        print(f"   Response: {json.dumps(data, indent=2)}")

        if response.status_code == 200:
            print("   ✅ LIST endpoint funciona!")
        else:
            print(f"   ❌ LIST endpoint falló: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # 6. Probar UNSAVE endpoint
    print("\n6️⃣  Probando DELETE /api/saved-jobs/unsave/ ...")
    url = f"{BASE_URL}/api/saved-jobs/unsave/"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    body = {'job_id': job.id}

    print(f"   URL: {url}")

    try:
        response = requests.delete(url, headers=headers, json=body)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        if response.status_code == 200:
            print("   ✅ UNSAVE endpoint funciona!")
        else:
            print(f"   ❌ UNSAVE endpoint falló: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    print("\n" + "="*60)
    print("TESTS COMPLETADOS")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_api_endpoints()
