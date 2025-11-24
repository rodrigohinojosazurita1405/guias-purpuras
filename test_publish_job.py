#!/usr/bin/env python
"""
SCRIPT DE TESTING PARA FASE 2: PUBLICACIÓN DE TRABAJOS
===================================================

Este script prueba exhaustivamente el endpoint POST /api/jobs/publish
con múltiples casos de prueba (exitosos y con errores).

Uso:
    python test_publish_job.py

Requisitos:
    - Django server corriendo en http://localhost:8000
    - Token JWT válido (obtenido al registrarse/login)
    - Base de datos con cambios aplicados
"""

import requests
import json
from datetime import datetime, timedelta
import sys

# Configuración
BASE_URL = 'http://localhost:8000'
API_ENDPOINT = f'{BASE_URL}/api/jobs/publish'

# Colores para output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def print_test_name(name, status):
    status_text = f"{Colors.OKGREEN}[PASS]{Colors.ENDC}" if status else f"{Colors.FAIL}[FAIL]{Colors.ENDC}"
    print(f"{status_text} {name}")


# Datos para pruebas
EXPIRY_DATE = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

TEST_DATA_VALID = {
    'title': 'Senior Full Stack Developer',
    'description': 'Buscamos un Senior Full Stack Developer con experiencia en Django y Vue.js para unirse a nuestro equipo dinámico.',
    'email': 'recruiter@company.com',
    'city': 'La Paz',
    'contractType': 'Tiempo Completo',
    'expiryDate': EXPIRY_DATE,
    'requirements': 'Mínimo 5 años de experiencia en desarrollo web, conocimiento de Python/Django, Vue.js, PostgreSQL',
    'companyName': 'Tech Solutions Bolivia',
    'companyAnonymous': False,
    'jobCategory': 'Tecnología',
    'subcategory': 'Desarrollo Web',
    'modality': 'hibrido',
    'responsibilities': 'Desarrollar features backend, mantener codebase, code review, mentoring juniors',
    'education': 'Licenciatura en Ingeniería Informática',
    'experience': 'Senior (5+ años)',
    'languages': 'Español, Inglés',
    'technicalSkills': 'Django, Vue.js, PostgreSQL, Docker, Git',
    'salaryType': 'range',
    'salaryMin': 35000,
    'salaryMax': 50000,
    'benefits': 'Bonos, Seguro médico, Home office flexible',
    'vacancies': 2,
    'whatsapp': '+591 7654321',
    'website': 'https://techsolutions.bo',
    'applicationInstructions': 'Enviar CV y portafolio',
    'applicationType': 'internal',
    'selectedPlan': 'featured',
    'screeningQuestions': [
        {'id': 1, 'question': '¿Cuántos años de experiencia tienes en Django?'},
        {'id': 2, 'question': '¿Has trabajado con Vue.js? ¿En cuántos proyectos?'}
    ]
}

TEST_CASES = {
    'VALID': {
        'name': 'Publicación válida completa',
        'data': TEST_DATA_VALID,
        'expect_status': 201,
        'expect_success': True
    },
    'MISSING_TITLE': {
        'name': 'Sin título (requerido)',
        'data': {**TEST_DATA_VALID, 'title': ''},
        'expect_status': 400,
        'expect_success': False
    },
    'SHORT_TITLE': {
        'name': 'Título muy corto (<5 caracteres)',
        'data': {**TEST_DATA_VALID, 'title': 'Dev'},
        'expect_status': 400,
        'expect_success': False
    },
    'MISSING_DESCRIPTION': {
        'name': 'Sin descripción (requerida)',
        'data': {**TEST_DATA_VALID, 'description': ''},
        'expect_status': 400,
        'expect_success': False
    },
    'SHORT_DESCRIPTION': {
        'name': 'Descripción muy corta (<20 caracteres)',
        'data': {**TEST_DATA_VALID, 'description': 'Puesto de trabajo'},
        'expect_status': 400,
        'expect_success': False
    },
    'INVALID_EMAIL': {
        'name': 'Email inválido',
        'data': {**TEST_DATA_VALID, 'email': 'not-an-email'},
        'expect_status': 400,
        'expect_success': False
    },
    'MISSING_EMAIL': {
        'name': 'Sin email (requerido)',
        'data': {**TEST_DATA_VALID, 'email': ''},
        'expect_status': 400,
        'expect_success': False
    },
    'MISSING_CITY': {
        'name': 'Sin ciudad (requerida)',
        'data': {**TEST_DATA_VALID, 'city': ''},
        'expect_status': 400,
        'expect_success': False
    },
    'MISSING_CONTRACT': {
        'name': 'Sin tipo de contrato (requerido)',
        'data': {**TEST_DATA_VALID, 'contractType': ''},
        'expect_status': 400,
        'expect_success': False
    },
    'MISSING_EXPIRY': {
        'name': 'Sin fecha de vencimiento (requerida)',
        'data': {**TEST_DATA_VALID, 'expiryDate': None},
        'expect_status': 400,
        'expect_success': False
    },
    'MISSING_REQUIREMENTS': {
        'name': 'Sin requisitos (requeridos)',
        'data': {**TEST_DATA_VALID, 'requirements': ''},
        'expect_status': 400,
        'expect_success': False
    },
    'INVALID_MODALITY': {
        'name': 'Modalidad inválida',
        'data': {**TEST_DATA_VALID, 'modality': 'virtual'},
        'expect_status': 400,
        'expect_success': False
    },
    'INVALID_SALARY_TYPE': {
        'name': 'Tipo de salario inválido',
        'data': {**TEST_DATA_VALID, 'salaryType': 'quarterly'},
        'expect_status': 400,
        'expect_success': False
    },
    'INVALID_APP_TYPE': {
        'name': 'Tipo de aplicación inválido',
        'data': {**TEST_DATA_VALID, 'applicationType': 'phone'},
        'expect_status': 400,
        'expect_success': False
    },
    'INVALID_PLAN': {
        'name': 'Plan inválido',
        'data': {**TEST_DATA_VALID, 'selectedPlan': 'premium'},
        'expect_status': 400,
        'expect_success': False
    },
    'SALARY_RANGE_INVALID': {
        'name': 'Salario mín > salario máx',
        'data': {**TEST_DATA_VALID, 'salaryMin': 60000, 'salaryMax': 40000},
        'expect_status': 400,
        'expect_success': False
    },
    'INVALID_SALARY_TYPE': {
        'name': 'Valores de salario no numéricos',
        'data': {**TEST_DATA_VALID, 'salaryMin': 'mucho'},
        'expect_status': 400,
        'expect_success': False
    },
    'MINIMAL_VALID': {
        'name': 'Publicación válida con datos mínimos',
        'data': {
            'title': 'Vendedor de seguros',
            'description': 'Buscamos vendedor de seguros con experiencia mínima de 2 años.',
            'email': 'sales@insurance.com',
            'city': 'Santa Cruz',
            'contractType': 'Por comisión',
            'expiryDate': EXPIRY_DATE,
            'requirements': 'Experiencia en ventas, licencia de conducir'
        },
        'expect_status': 201,
        'expect_success': True
    }
}


def get_valid_token():
    """
    Obtiene un token JWT válido.

    NOTA: Para este script funcionie, debes:
    1. Registrarte en http://localhost:3000/register
    2. O loguearte en http://localhost:3000/login
    3. El token se guarda en localStorage

    Para testing automatizado, aquí generamos uno o usamos uno existente.
    """
    print_info("Se necesita un token JWT válido para ejecutar las pruebas.")
    print_info("Opciones:")
    print_info("  1. Registrate en http://localhost:3000/register")
    print_info("  2. O logueate en http://localhost:3000/login")
    print_info("  3. O proporciona el token como argumento:")
    print_info("     python test_publish_job.py YOUR_TOKEN_HERE")

    if len(sys.argv) > 1:
        token = sys.argv[1]
        print_success(f"Token proporcionado: {token[:20]}...")
        return token

    # Intentar obtener token de variable de entorno
    import os
    token = os.getenv('JWT_TOKEN')
    if token:
        print_success(f"Token de variable de entorno: {token[:20]}...")
        return token

    print_error("No se proporcionó token. Usa: python test_publish_job.py TOKEN")
    sys.exit(1)


def run_test(test_key, token):
    """Ejecuta una prueba individual"""
    test = TEST_CASES[test_key]
    name = test['name']
    data = test['data']
    expect_status = test['expect_status']
    expect_success = test['expect_success']

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.post(API_ENDPOINT, json=data, headers=headers, timeout=10)
        result = response.json()

        status_ok = response.status_code == expect_status
        success_ok = result.get('success') == expect_success

        passed = status_ok and success_ok
        print_test_name(name, passed)

        if not passed:
            print_error(f"  Status: {response.status_code} (esperado {expect_status})")
            print_error(f"  Success: {result.get('success')} (esperado {expect_success})")
            if 'errors' in result:
                print_error(f"  Errores: {json.dumps(result['errors'], indent=2)}")
            if 'message' in result:
                print_warning(f"  Mensaje: {result['message']}")
        else:
            print_success(f"  Status: {response.status_code}, Success: {result.get('success')}")
            if 'id' in result:
                print_info(f"  Job ID creado: {result['id']}")

        return passed

    except requests.exceptions.Timeout:
        print_error(f"{name}: TIMEOUT (>10s)")
        return False
    except requests.exceptions.ConnectionError as e:
        print_error(f"{name}: ERROR DE CONEXIÓN - {str(e)}")
        print_error(f"  ¿El servidor está corriendo en {BASE_URL}?")
        return False
    except Exception as e:
        print_error(f"{name}: ERROR - {str(e)}")
        return False


def main():
    print_header("TESTING FASE 2: PUBLICACIÓN DE TRABAJOS")

    # Obtener token
    token = get_valid_token()

    print_header("Iniciando pruebas...")
    print_info(f"Endpoint: {API_ENDPOINT}")
    print_info(f"Token: {token[:30]}...")

    # Ejecutar pruebas
    results = {}
    for test_key in TEST_CASES.keys():
        results[test_key] = run_test(test_key, token)

    # Resumen
    print_header("RESUMEN DE PRUEBAS")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    percentage = (passed / total) * 100

    print(f"Pruebas pasadas: {Colors.OKGREEN}{passed}/{total}{Colors.ENDC} ({percentage:.1f}%)")

    if passed == total:
        print_success("Todas las pruebas pasaron!")
        sys.exit(0)
    else:
        failed_count = total - passed
        print_error(f"{failed_count} pruebas fallaron")
        sys.exit(1)


if __name__ == '__main__':
    main()
