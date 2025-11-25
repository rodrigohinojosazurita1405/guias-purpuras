#!/usr/bin/env python
"""
Test Script - Verificar que la API está lista para recibir datos de facturación
"""
import requests
import json
from datetime import datetime, timedelta

# Token válido (ajusta según tu usuario de test)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzNzU4ODQyLCJpYXQiOjE3NjM3NTUyNDIsImp0aSI6IjY0MWNkM2M1NGUzOTRlMWU5NDEzY2UwZWU3YjhhNTZkIiwidXNlcl9pZCI6IjgifQ.-W3e-qekdgyfoKeO1YBEV0qYwaHzE1qARma61sb89CI"
API_URL = "http://localhost:8000/api/jobs/publish"

# Test data - CON datos de facturación
test_data = {
    # Información Básica
    "title": "Ingeniero de Software (Test Facturación)",
    "companyName": "Tech Company Test",
    "companyAnonymous": False,
    "description": "Se busca un ingeniero de software con experiencia en desarrollo web.",

    # Ubicación y Tipo
    "jobCategory": "Sistemas",
    "city": "La Paz",
    "municipality": "Cercado",
    "contractType": "Tiempo Completo",
    "expiryDate": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),

    # Requisitos
    "requirements": "• Licenciatura en Informática\n• Mínimo 3 años de experiencia\n• Python, Django, React",
    "technicalSkills": "Python, Django, JavaScript, React, PostgreSQL",
    "softSkills": "Liderazgo, comunicación, trabajo en equipo",

    # Compensación
    "salaryType": "range",
    "salaryMin": 3000,
    "salaryMax": 5000,
    "benefits": "Seguro de salud, bonos anuales",

    # Contacto
    "email": "test@company.com",
    "whatsapp": "+59172345678",

    # Vacantes
    "vacancies": 2,

    # Aplicación
    "applicationType": "internal",
    "applicationInstructions": "Enviar CV actualizado",

    # Plan
    "selectedPlan": "purpura",

    # ===== DATOS DE FACTURACIÓN (NUEVO) =====
    "billingBusinessName": "ABC Soluciones S.A.",
    "billingNIT": "1234567890",
    "billingInvoiceEmail": "contabilidad@empresa.com",

    # Screening Questions
    "screeningQuestions": [
        {
            "text": "¿Tienes experiencia con React?",
            "type": "yesno",
            "required": True
        }
    ]
}

print("=" * 80)
print("TEST: Verificar API lista para recibir datos de facturación")
print("=" * 80)
print("\n📝 Datos a enviar:")
print(json.dumps(test_data, indent=2, ensure_ascii=False))

print("\n" + "=" * 80)
print("Enviando POST a:", API_URL)
print("=" * 80)

try:
    response = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        },
        json=test_data,
        timeout=30
    )

    print(f"\n✅ Status Code: {response.status_code}")

    result = response.json()
    print("\n📥 Respuesta del servidor:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if response.status_code == 201 and result.get('success'):
        print("\n" + "=" * 80)
        print("✅ TEST EXITOSO - Job publicado con datos de facturación")
        print("=" * 80)
        print(f"Job ID: {result.get('id')}")
        print(f"Mensaje: {result.get('message')}")
        print("\n📋 Ahora verificar en Django admin que se guardaron:")
        print("   - billingBusinessName: ABC Soluciones S.A.")
        print("   - billingNIT: 1234567890")
        print("   - billingInvoiceEmail: contabilidad@empresa.com")
    else:
        print("\n" + "=" * 80)
        print("❌ ERROR - Job no fue publicado")
        print("=" * 80)
        if result.get('errors'):
            print("Errores de validación:")
            for field, error in result.get('errors', {}).items():
                print(f"  • {field}: {error}")

except requests.exceptions.ConnectionError:
    print("❌ ERROR: No se puede conectar al servidor")
    print("Verifica que Django esté corriendo en http://localhost:8000")
except requests.exceptions.Timeout:
    print("❌ ERROR: Timeout esperando respuesta del servidor")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
