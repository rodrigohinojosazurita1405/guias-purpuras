"""
API Views para Autenticación
"""
import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from auth_api.models import CustomUser


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
        "name": "John Doe",
        "role": "applicant" o "company"
    }
    """
    try:
        data = json.loads(request.body)

        # Validaciones
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        role = data.get('role', 'applicant').strip()  # Por defecto postulante

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

        # Validar que el role sea válido
        valid_roles = ['applicant', 'company']
        if role not in valid_roles:
            return JsonResponse({
                'success': False,
                'message': f'Rol inválido. Debe ser: {", ".join(valid_roles)}'
            }, status=400)

        # Verificar si el usuario ya existe
        if CustomUser.objects.filter(username=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Este email ya está registrado'
            }, status=400)

        # Crear usuario con CustomUser
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name.split()[0] if ' ' in name else name,
            last_name=' '.join(name.split()[1:]) if ' ' in name else '',
            role=role  # Asignar el role del usuario
        )

        # Si el usuario es una empresa, crear automáticamente su perfil de empresa
        if role == 'company':
            from profiles.models import CompanyProfile, UserProfile

            # Crear perfil de usuario (owner) si no existe
            user_profile, created = UserProfile.objects.get_or_create(
                email=email,
                defaults={
                    'fullName': name,
                }
            )

            # Crear perfil de empresa vacío
            CompanyProfile.objects.create(
                owner=user_profile,
                companyName=name,  # Usar el nombre del registro como nombre inicial
                email=email,
                location='',  # Se completará después
                category='jobs'  # Por defecto, puede cambiarse después
            )
            print(f'✓ Perfil de empresa creado automáticamente para {email}')

        # Generar tokens
        refresh = RefreshToken.for_user(user)

        # Intentar obtener la foto de perfil del UserProfile o logo de CompanyProfile
        from profiles.models import UserProfile, CompanyProfile
        from django.conf import settings

        profile_photo = None
        full_name = user.get_full_name() or user.username  # Valor por defecto

        try:
            user_profile = UserProfile.objects.get(email=user.email)

            # IMPORTANTE: Usar el nombre del perfil (fullName) si existe
            # Esto asegura que se muestre el nombre exactamente como el usuario lo guardó
            if user_profile.fullName:
                full_name = user_profile.fullName

            # Si es empresa, buscar el logo de la empresa
            if user.role == 'company':
                company_profile = CompanyProfile.objects.filter(owner=user_profile).first()
                if company_profile and company_profile.logo:
                    photo_path = str(company_profile.logo)
                    if not photo_path.startswith('http'):
                        profile_photo = f"http://localhost:8000{settings.MEDIA_URL}{photo_path}"
                    else:
                        profile_photo = photo_path
            # Si es postulante, usar la foto del UserProfile
            elif user_profile.profilePhoto:
                photo_path = str(user_profile.profilePhoto)
                if not photo_path.startswith('http'):
                    profile_photo = f"http://localhost:8000{settings.MEDIA_URL}{photo_path}"
                else:
                    profile_photo = photo_path
        except UserProfile.DoesNotExist:
            # No hay perfil, usar el nombre del usuario de autenticación
            pass

        return JsonResponse({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': full_name,
                'role': user.role,
                'profilePhoto': profile_photo
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

        # Intentar obtener la foto de perfil del UserProfile o logo de CompanyProfile
        from profiles.models import UserProfile, CompanyProfile
        from django.conf import settings

        profile_photo = None
        full_name = user.get_full_name() or user.username  # Valor por defecto

        try:
            user_profile = UserProfile.objects.get(email=user.email)

            # IMPORTANTE: Usar el nombre del perfil (fullName) si existe
            # Esto asegura que se muestre el nombre exactamente como el usuario lo guardó
            if user_profile.fullName:
                full_name = user_profile.fullName

            # Si es empresa, buscar el logo de la empresa
            if user.role == 'company':
                company_profile = CompanyProfile.objects.filter(owner=user_profile).first()
                if company_profile and company_profile.logo:
                    photo_path = str(company_profile.logo)
                    if not photo_path.startswith('http'):
                        profile_photo = f"http://localhost:8000{settings.MEDIA_URL}{photo_path}"
                    else:
                        profile_photo = photo_path
            # Si es postulante, usar la foto del UserProfile
            elif user_profile.profilePhoto:
                photo_path = str(user_profile.profilePhoto)
                if not photo_path.startswith('http'):
                    profile_photo = f"http://localhost:8000{settings.MEDIA_URL}{photo_path}"
                else:
                    profile_photo = photo_path
        except UserProfile.DoesNotExist:
            # No hay perfil, usar el nombre del usuario de autenticación
            pass

        return JsonResponse({
            'success': True,
            'message': 'Sesión iniciada exitosamente',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': full_name,
                'role': user.role,
                'profilePhoto': profile_photo
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
            user = CustomUser.objects.get(email=email)

            # Importar modelo de token
            from auth_api.models import PasswordResetToken
            from django.core.mail import send_mail
            from django.conf import settings

            # Crear token de recuperación
            reset_token = PasswordResetToken.create_for_user(user)

            # Construir URL de reset (cambia según entorno)
            if settings.DEBUG:
                # Localhost
                reset_url = f"http://localhost:5173/reset-password/{reset_token.token}"
            else:
                # Producción - usar variable de entorno
                frontend_url = settings.FRONTEND_URL
                reset_url = f"{frontend_url}/reset-password/{reset_token.token}"

            # Preparar email
            subject = 'Recuperación de Contraseña - Guías Púrpuras'
            message = f"""
Hola {user.get_full_name() or user.username},

Recibimos una solicitud para restablecer tu contraseña en Guías Púrpuras.

Haz clic en el siguiente enlace para crear una nueva contraseña:
{reset_url}

Este enlace es válido por 1 hora.

Si no solicitaste este cambio, puedes ignorar este correo.

Saludos,
Equipo de Guías Púrpuras Bolivia
            """

            # Enviar email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            print(f'✓ Email de recuperación enviado a {email}')
            print(f'Token: {reset_token.token}')
            print(f'URL: {reset_url}')

            return JsonResponse({
                'success': True,
                'message': 'Si el email existe en nuestros registros, recibirás instrucciones de recuperación.'
            }, status=200)

        except CustomUser.DoesNotExist:
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
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def reset_password(request):
    """
    Endpoint para restablecer la contraseña
    POST /api/auth/reset-password

    Body:
    {
        "token": "token_value",
        "password": "new_password"
    }
    """
    try:
        data = json.loads(request.body)
        token_str = data.get('token', '').strip()
        new_password = data.get('password', '').strip()

        if not token_str:
            return JsonResponse({
                'success': False,
                'message': 'Token es requerido'
            }, status=400)

        if not new_password or len(new_password) < 6:
            return JsonResponse({
                'success': False,
                'message': 'La contraseña debe tener al menos 6 caracteres'
            }, status=400)

        # Buscar token
        from auth_api.models import PasswordResetToken

        try:
            reset_token = PasswordResetToken.objects.get(token=token_str)
        except PasswordResetToken.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Token inválido o expirado'
            }, status=400)

        # Verificar si el token es válido
        if not reset_token.is_valid():
            return JsonResponse({
                'success': False,
                'message': 'Token inválido o expirado'
            }, status=400)

        # Cambiar contraseña
        user = reset_token.user
        user.set_password(new_password)
        user.save()

        # Marcar token como usado
        reset_token.used = True
        reset_token.save()

        print(f'✓ Contraseña restablecida para {user.email}')

        return JsonResponse({
            'success': True,
            'message': 'Contraseña restablecida exitosamente'
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error en reset-password: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def change_password(request):
    """
    Endpoint para cambiar contraseña de usuario autenticado
    POST /api/auth/change-password

    Body:
    {
        "current_password": "currentpass123",
        "new_password": "newpass123",
        "confirm_password": "newpass123"
    }
    """
    try:
        # Verificar autenticación mediante JWT
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                'success': False,
                'message': 'Token de autenticación no proporcionado'
            }, status=401)

        token = auth_header.split(' ')[1]

        try:
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = CustomUser.objects.get(id=user_id)
        except (InvalidToken, TokenError):
            return JsonResponse({
                'success': False,
                'message': 'Token inválido o expirado'
            }, status=401)
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=404)

        data = json.loads(request.body)

        # Validaciones
        current_password = data.get('current_password', '').strip()
        new_password = data.get('new_password', '').strip()
        confirm_password = data.get('confirm_password', '').strip()

        if not current_password:
            return JsonResponse({
                'success': False,
                'message': 'Contraseña actual es requerida'
            }, status=400)

        if not new_password:
            return JsonResponse({
                'success': False,
                'message': 'Nueva contraseña es requerida'
            }, status=400)

        if len(new_password) < 6:
            return JsonResponse({
                'success': False,
                'message': 'La nueva contraseña debe tener al menos 6 caracteres'
            }, status=400)

        if new_password != confirm_password:
            return JsonResponse({
                'success': False,
                'message': 'Las contraseñas no coinciden'
            }, status=400)

        # Verificar que la contraseña actual sea correcta
        if not user.check_password(current_password):
            return JsonResponse({
                'success': False,
                'message': 'La contraseña actual es incorrecta'
            }, status=400)

        # Verificar que la nueva contraseña sea diferente
        if current_password == new_password:
            return JsonResponse({
                'success': False,
                'message': 'La nueva contraseña debe ser diferente a la actual'
            }, status=400)

        # Cambiar la contraseña
        user.set_password(new_password)
        user.save()

        return JsonResponse({
            'success': True,
            'message': 'Contraseña cambiada exitosamente'
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error en change-password: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
