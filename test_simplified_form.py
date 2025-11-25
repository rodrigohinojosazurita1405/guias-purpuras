#!/usr/bin/env python
"""
Test Script - Verificar que la forma simplificada funciona correctamente
Prueba que los campos eliminados no causen errores
"""
import requests
import json
from datetime import datetime, timedelta

# Token válido (ajusta según tu usuario de test)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzNzU4ODQyLCJpYXQiOjE3NjM3NTUyNDIsImp0aSI6IjY0MWNkM2M1NGUzOTRlMWU5NDEzY2UwZWU3YjhhNTZkIiwidXNlcl9pZCI6IjgifQ.-W3e-qekdgyfoKeO1YBEV0qYwaHzE1qARma61sb89CI"
API_URL = "http://localhost:8000/api/jobs/publish"

# Test data - Forma simplificada (SIN los campos eliminados)
test_data = {
    # Información Básica
    "title": "Ingeniero de Software (Test Simplificado)",
    "companyName": "Tech Company Test",
    "companyAnonymous": False,
    "description": "Se busca un ingeniero de software con experiencia en desarrollo web. Responsabilidades: desarrollar nuevas funcionalidades, mantener código existente, participar en code reviews.",

    # Ubicación y Tipo
    "jobCategory": "Sistemas",
    "city": "La Paz",
    "municipality": "Cercado",
    "contractType": "Tiempo Completo",
    "expiryDate": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),

    # Requisitos Consolidados (SIN los campos separados eliminados)
    "requirements": "• Licenciatura en Informática o campo relacionado\n• Mínimo 3 años de experiencia en desarrollo web\n• Idiomas: Español (obligatorio), Inglés (deseable)\n• Experiencia con Python, JavaScript, React\n• Excelente comunicación y trabajo en equipo",

    # Competencias Técnicas (NUEVO campo simplificado)
    "technicalSkills": "Python, Django, JavaScript, React, PostgreSQL, Docker, Git, AWS",

    # Competencias Blandas (NUEVO campo opcional simplificado)
    "softSkills": "Liderazgo, comunicación efectiva, resolución de problemas, trabajo en equipo",

    # Compensación
    "salaryType": "range",
    "salaryMin": 3000,
    "salaryMax": 5000,
    "benefits": "Seguro de salud, bonos anuales, flexible work arrangement",

    # Contacto
    "email": "test@company.com",
    "whatsapp": "+59172345678",

    # Vacantes
    "vacancies": 2,

    # Aplicación
    "applicationType": "internal",
    "applicationInstructions": "Enviar CV actualizado y una carta de presentación",

    # Plan
    "selectedPlan": "purpura",

    # Screening Questions
    "screeningQuestions": [
        {
            "text": "¿Tienes experiencia con React?",
            "type": "yesno",
            "required": True
        }
    ]
}

# Campos que fueron ELIMINADOS (NO deben ser enviados)
# education, experience, languages, responsibilities, contactEmail, contactWhatsapp, cvSubmissionMethods, website

print("=" * 80)
print("TEST: Verificar forma simplificada sin campos redundantes")
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
        print("✅ TEST EXITOSO - Job publicado correctamente")
        print("=" * 80)
        print(f"Job ID: {result.get('id')}")
        print(f"Mensaje: {result.get('message')}")
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
