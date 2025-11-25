"""
API Views para Autenticación
"""
import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


@require_http_methods(["POST"])
@csrf_exempt
def register(request):
    """
    Endpoint para registrar un nuevo usuario
    POST /api/auth/register

    Body:
    {
        "email": "user@example.com",
        "password": "password123",
        "name": "John Doe"
    }
    """
    try:
        data = json.loads(request.body)

        # Validaciones
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()

        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email es requerido'
            }, status=400)

        if not password or len(password) < 6:
            return JsonResponse({
                'success': False,
                'message': 'Contraseña debe tener al menos 6 caracteres'
            }, status=400)

        if not name:
            return JsonResponse({
                'success': False,
                'message': 'Nombre es requerido'
            }, status=400)

        # Verificar si el usuario ya existe
        if User.objects.filter(username=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Este email ya está registrado'
            }, status=400)

        # Crear usuario
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name.split()[0] if ' ' in name else name,
            last_name=' '.join(name.split()[1:]) if ' ' in name else ''
        )

        # Generar tokens
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.get_full_name() or user.username
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error en registro: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def login(request):
    """
    Endpoint para iniciar sesión
    POST /api/auth/login

    Body:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    try:
        data = json.loads(request.body)

        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email or not password:
            return JsonResponse({
                'success': False,
                'message': 'Email y contraseña son requeridos'
            }, status=400)

        # Autenticar usuario (Django usa username, pero nosotros usamos email como username)
        user = authenticate(username=email, password=password)

        if not user:
            return JsonResponse({
                'success': False,
                'message': 'Email o contraseña incorrectos'
            }, status=401)

        # Generar tokens
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'success': True,
            'message': 'Sesión iniciada exitosamente',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.get_full_name() or user.username
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error en login: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def refresh_token(request):
    """
    Endpoint para refrescar el access token
    POST /api/auth/refresh

    Body:
    {
        "refresh": "refresh_token_value"
    }
    """
    try:
        data = json.loads(request.body)
        refresh_token_str = data.get('refresh', '').strip()

        if not refresh_token_str:
            return JsonResponse({
                'success': False,
                'message': 'Refresh token es requerido'
            }, status=400)

        try:
            refresh = RefreshToken(refresh_token_str)

            return JsonResponse({
                'success': True,
                'message': 'Token refrescado exitosamente',
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=200)

        except (InvalidToken, TokenError) as e:
            return JsonResponse({
                'success': False,
                'message': 'Refresh token inválido o expirado'
            }, status=401)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error en refresh: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def logout(request):
    """
    Endpoint para cerrar sesión
    POST /api/auth/logout

    Body:
    {
        "refresh": "refresh_token_value"
    }

    IMPORTANTE: Este endpoint borra:
    1. El refresh token (blacklist)
    2. La sesión de Django (cookies)
    """
    try:
        print('[LOGOUT] Endpoint llamado')

        # PASO 1: Borrar la sesión de Django
        if hasattr(request, 'session'):
            request.session.flush()
            print('[LOGOUT] Django session flushed')

        # PASO 2: Intentar hacer blacklist del refresh token JWT
        data = json.loads(request.body)
        refresh_token_str = data.get('refresh', '').strip()
        print(f'[LOGOUT] Refresh token recibido: {refresh_token_str[:20]}...' if refresh_token_str else '[LOGOUT] No refresh token recibido')

        if refresh_token_str:
            try:
                refresh = RefreshToken(refresh_token_str)
                refresh.blacklist()
                print('[LOGOUT] Refresh token blacklisted')
            except (InvalidToken, TokenError) as e:
                # Si el token es inválido, no importa - ya borramos la sesión
                print(f'[LOGOUT] Token blacklist error (ignorado): {str(e)}')
                pass

        # PASO 3: Crear respuesta con header para limpiar cookies
        response = JsonResponse({
            'success': True,
            'message': 'Sesión cerrada exitosamente'
        }, status=200)

        # Establecer headers para limpiar las cookies de sesión del navegador
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        print('[LOGOUT] Cookies deletadas en respuesta')

        print('[LOGOUT] Logout completado exitosamente')
        return response

    except json.JSONDecodeError as e:
        print(f'[LOGOUT] JSON decode error: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'[LOGOUT] Error en logout: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def verify_token(request):
    """
    Endpoint para verificar si el token actual es válido
    GET /api/auth/verify

    Headers:
    Authorization: Bearer access_token_value
    """
    try:
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()

        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return JsonResponse({
                'success': False,
                'message': 'Token no proporcionado',
                'valid': False
            }, status=401)

        token_str = auth_header[1]

        try:
            # Intentar decodificar el token usando UntypedToken
            from rest_framework_simplejwt.tokens import UntypedToken
            from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

            UntypedToken(token_str)

            return JsonResponse({
                'success': True,
                'message': 'Token es válido',
                'valid': True
            }, status=200)

        except (InvalidToken, TokenError):
            return JsonResponse({
                'success': False,
                'message': 'Token inválido o expirado',
                'valid': False
            }, status=401)

    except Exception as e:
        print(f'Error verificando token: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}',
            'valid': False
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def forgot_password(request):
    """
    Endpoint para solicitar recuperación de contraseña
    POST /api/auth/forgot-password

    Body:
    {
        "email": "user@example.com"
    }
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()

        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email es requerido'
            }, status=400)

        # Verificar si el usuario existe
        try:
            user = User.objects.get(email=email)
            # En una aplicación real, aquí se enviaría un email con un link de reseteo
            # Por ahora, simplemente confirmamos que el email existe
            return JsonResponse({
                'success': True,
                'message': 'Si el email existe en nuestros registros, recibirás instrucciones de recuperación.'
            }, status=200)

        except User.DoesNotExist:
            # Por seguridad, no revelamos si el email existe o no
            # Retornamos el mismo mensaje de éxito
            return JsonResponse({
                'success': True,
                'message': 'Si el email existe en nuestros registros, recibirás instrucciones de recuperación.'
            }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error en forgot-password: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
