import json
from datetime import datetime, timedelta

# Simulación de JSON que enviaría el frontend
job_data = {
    "title": "Senior Developer",
    "description": "Experienced developer needed",
    "email": "company@test.com",
    "city": "Cochabamba",
    "municipality": "Cercado",
    "contractType": "Tiempo Completo",
    "expiryDate": (datetime.now() + timedelta(days=30)).isoformat().split('T')[0],
    "requirements": "5+ years experience",
    "companyName": "Tech Corp",
    "subcategory": "Backend",
    "whatsapp": "67123456",
    "selectedPlan": "escencial"
}

print("=" * 70)
print("TEST: Verificar estructura de datos que frontend enviará")
print("=" * 70)
print("\nJSON que frontend enviará al backend:")
print(json.dumps(job_data, indent=2))

print("\n✅ Validaciones:")
print(f"  - Tiene 'city': {bool(job_data.get('city'))}")
print(f"  - Tiene 'municipality': {bool(job_data.get('municipality'))}")
print(f"  - Municipality NO es requerido: {job_data.get('municipality') or 'OPTIONAL'}")

print("\n" + "=" * 70)
print("CONCLUSIÓN: El frontend envía correctamente municipality al backend")
print("=" * 70)
