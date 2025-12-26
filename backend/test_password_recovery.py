#!/usr/bin/env python
"""
Script de prueba para el sistema de recuperación de contraseña
Verifica que todos los endpoints funcionan correctamente
"""

import requests
import json
from colorama import init, Fore, Style

# Inicializar colorama para colores en Windows
init(autoreset=True)

# Configuración
BASE_URL = 'http://localhost:8000/api'
TEST_EMAIL = 'test@guiaspurpuras.com'
TEST_PASSWORD = 'password123'
NEW_PASSWORD = 'newpassword123'

def print_test(test_name):
    """Imprime el nombre del test"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Test: {test_name}")
    print(f"{Fore.CYAN}{'='*60}")

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"{Fore.GREEN}[OK] {message}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"{Fore.RED}[ERROR] {message}")

def print_info(message):
    """Imprime información"""
    print(f"{Fore.YELLOW}[INFO] {message}")

def register_test_user():
    """Paso 1: Registrar un usuario de prueba"""
    print_test("Paso 1: Registrar usuario de prueba")

    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "name": "Usuario de Prueba",
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
        print_error(f"Excepción al registrar: {str(e)}")
        return False

def test_forgot_password():
    """Paso 2: Solicitar recuperación de contraseña"""
    print_test("Paso 2: Solicitar recuperación de contraseña")

    payload = {"email": TEST_EMAIL}

    try:
        response = requests.post(f"{BASE_URL}/auth/forgot-password", json=payload)
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            print_success("Solicitud de recuperación exitosa")
            print_info("Revisa la consola del servidor Django para ver el email y el token")
            print_info(f"Mensaje: {data.get('message')}")
            return True
        else:
            print_error(f"Error en forgot-password: {data.get('message')}")
            return False
    except Exception as e:
        print_error(f"Excepción en forgot-password: {str(e)}")
        return False

def test_reset_password(token):
    """Paso 3: Restablecer contraseña con token"""
    print_test("Paso 3: Restablecer contraseña")

    if not token:
        print_error("No se proporcionó token. Obtén el token de la consola del servidor")
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
            print_error(f"Error en reset-password: {data.get('message')}")
            print_info(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Excepción en reset-password: {str(e)}")
        return False

def test_login_with_new_password():
    """Paso 4: Intentar login con la nueva contraseña"""
    print_test("Paso 4: Login con nueva contraseña")

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
        print_error(f"Excepción en login: {str(e)}")
        return False

def test_invalid_token():
    """Paso 5: Probar con token inválido"""
    print_test("Paso 5: Probar token inválido")

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
            print_error("Token inválido fue aceptado (esto es un error)")
            return False
    except Exception as e:
        print_error(f"Excepción al probar token inválido: {str(e)}")
        return False

def main():
    """Función principal que ejecuta todas las pruebas"""
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}SISTEMA DE RECUPERACIÓN DE CONTRASEÑA - PRUEBAS")
    print(f"{Fore.MAGENTA}{'='*60}")

    print_info("Asegúrate de que el servidor Django esté corriendo en http://localhost:8000")
    input(f"\n{Fore.YELLOW}Presiona Enter para comenzar las pruebas...")

    # Contador de pruebas
    tests_passed = 0
    total_tests = 5

    # Ejecutar pruebas
    if register_test_user():
        tests_passed += 1

    if test_forgot_password():
        tests_passed += 1

    # Solicitar token al usuario
    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"{Fore.YELLOW}ACCIÓN REQUERIDA:")
    print(f"{Fore.YELLOW}{'='*60}")
    print_info("Ve a la consola del servidor Django y copia el TOKEN que aparece")
    print_info("Busca una línea que dice: 'Token: <valor_del_token>'")
    token = input(f"\n{Fore.CYAN}Pega el token aquí: {Style.RESET_ALL}").strip()

    if test_reset_password(token):
        tests_passed += 1

    if test_login_with_new_password():
        tests_passed += 1

    if test_invalid_token():
        tests_passed += 1

    # Resumen final
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}RESUMEN DE PRUEBAS")
    print(f"{Fore.MAGENTA}{'='*60}")

    if tests_passed == total_tests:
        print(f"{Fore.GREEN}✓ TODAS LAS PRUEBAS PASARON ({tests_passed}/{total_tests})")
        print(f"{Fore.GREEN}✓ Sistema de recuperación de contraseña funcionando correctamente")
    else:
        print(f"{Fore.YELLOW}⚠ Pruebas pasadas: {tests_passed}/{total_tests}")
        print(f"{Fore.YELLOW}⚠ Algunas pruebas fallaron, revisa los errores arriba")

    print(f"\n{Fore.CYAN}Notas:")
    print_info("En localhost, los emails se muestran en la consola del servidor")
    print_info("En producción, se enviarán emails reales a la bandeja de entrada")
    print_info("El token expira después de 1 hora")
    print_info("Cada token solo se puede usar una vez")

if __name__ == "__main__":
    main()
