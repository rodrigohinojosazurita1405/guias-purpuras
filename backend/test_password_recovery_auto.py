#!/usr/bin/env python
"""
Script automatizado de prueba para recuperación de contraseña
No requiere interacción del usuario - extrae el token automáticamente
"""

import requests
import json
import re
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Configuración
BASE_URL = 'http://localhost:8000/api'
TEST_EMAIL = 'test_recovery@guiaspurpuras.com'
TEST_PASSWORD = 'password123'
NEW_PASSWORD = 'newpassword456'

def print_header(title):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{title}")
    print(f"{Fore.CYAN}{'='*60}")

def print_success(message):
    print(f"{Fore.GREEN}[OK] {message}")

def print_error(message):
    print(f"{Fore.RED}[ERROR] {message}")

def print_info(message):
    print(f"{Fore.YELLOW}[INFO] {message}")

def register_test_user():
    """Prueba 0: Registrar usuario de prueba"""
    print_header("PRUEBA 0: Registrar usuario de prueba")

    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "name": "Usuario Test Recovery",
        "role": "applicant"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        data = response.json()

        if response.status_code == 201 and data.get('success'):
            print_success(f"Usuario registrado: {TEST_EMAIL}")
            return True
        elif response.status_code == 400 and 'ya está registrado' in data.get('message', ''):
            print_info(f"Usuario ya existe: {TEST_EMAIL}")
            return True
        else:
            print_error(f"Error al registrar: {data.get('message')}")
            return False
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return False

def test_forgot_password():
    """Prueba 1: Solicitar recuperación de contraseña"""
    print_header("PRUEBA 1: Solicitar recuperación de contraseña")

    payload = {"email": TEST_EMAIL}

    try:
        response = requests.post(f"{BASE_URL}/auth/forgot-password", json=payload)
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            print_success(f"Solicitud enviada correctamente")
            print_info(f"Mensaje: {data.get('message')}")
            return True
        else:
            print_error(f"Error: {data.get('message')}")
            return False
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return False

def get_latest_token():
    """Obtiene el último token generado desde la base de datos"""
    print_header("Obteniendo token desde la base de datos")

    try:
        import os
        import django

        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()

        from auth_api.models import PasswordResetToken

        # Obtener el último token creado
        latest_token = PasswordResetToken.objects.filter(used=False).order_by('-created_at').first()

        if latest_token:
            print_success(f"Token encontrado para: {latest_token.user.email}")
            print_info(f"Token: {latest_token.token[:20]}...")
            return latest_token.token
        else:
            print_error("No se encontró ningún token válido")
            return None

    except Exception as e:
        print_error(f"Error al obtener token: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_reset_password(token):
    """Prueba 2: Restablecer contraseña con token"""
    print_header("PRUEBA 2: Restablecer contraseña con token")

    if not token:
        print_error("No hay token disponible")
        return False

    payload = {
        "token": token,
        "password": NEW_PASSWORD
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/reset-password", json=payload)
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            print_success("Contraseña restablecida exitosamente")
            print_info(f"Mensaje: {data.get('message')}")
            return True
        else:
            print_error(f"Error: {data.get('message')}")
            print_info(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return False

def test_login_with_new_password():
    """Prueba 3: Login con nueva contraseña"""
    print_header("PRUEBA 3: Login con nueva contraseña")

    payload = {
        "email": TEST_EMAIL,
        "password": NEW_PASSWORD
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            print_success("Login exitoso con nueva contraseña")
            print_info(f"Usuario: {data['user']['email']}")
            return True
        else:
            print_error(f"Error en login: {data.get('message')}")
            return False
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return False

def test_invalid_token():
    """Prueba 4: Token inválido debe ser rechazado"""
    print_header("PRUEBA 4: Validar rechazo de token inválido")

    payload = {
        "token": "token_invalido_12345",
        "password": "cualquier_password"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/reset-password", json=payload)
        data = response.json()

        if response.status_code == 400 and not data.get('success'):
            print_success("Token inválido rechazado correctamente")
            print_info(f"Mensaje: {data.get('message')}")
            return True
        else:
            print_error("Token inválido fue aceptado (BUG!)")
            return False
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return False

def main():
    print_header("PRUEBAS AUTOMATIZADAS - RECUPERACIÓN DE CONTRASEÑA")
    print_info("Servidor: http://localhost:8000")
    print_info(f"Email de prueba: {TEST_EMAIL}")

    results = {
        'total': 5,
        'passed': 0,
        'failed': 0
    }

    # Prueba 0: Registrar usuario
    if not register_test_user():
        print_error("No se pudo registrar el usuario - Deteniendo ejecución")
        results['failed'] += 5
        return results
    results['passed'] += 1

    # Prueba 1: Solicitar recuperación
    if test_forgot_password():
        results['passed'] += 1
    else:
        results['failed'] += 1
        print_error("Prueba 1 falló - Deteniendo ejecución")
        return results

    # Obtener token
    token = get_latest_token()
    if not token:
        print_error("No se pudo obtener el token - Deteniendo ejecución")
        results['failed'] += 3
        return results

    # Prueba 2: Restablecer contraseña
    if test_reset_password(token):
        results['passed'] += 1
    else:
        results['failed'] += 1

    # Prueba 3: Login con nueva contraseña
    if test_login_with_new_password():
        results['passed'] += 1
    else:
        results['failed'] += 1

    # Prueba 4: Token inválido
    if test_invalid_token():
        results['passed'] += 1
    else:
        results['failed'] += 1

    # Resumen
    print_header("RESUMEN DE PRUEBAS")
    print(f"{Fore.GREEN}Pruebas exitosas: {results['passed']}/{results['total']}")
    print(f"{Fore.RED}Pruebas fallidas: {results['failed']}/{results['total']}")

    if results['passed'] == results['total']:
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
        print(f"{Fore.GREEN}Sistema de recuperación funcionando al 100%")
        print(f"{Fore.GREEN}{'='*60}")
    else:
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}ALGUNAS PRUEBAS FALLARON - Revisar errores arriba")
        print(f"{Fore.YELLOW}{'='*60}")

    return results

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[INFO] Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR FATAL] {str(e)}")
        import traceback
        traceback.print_exc()
