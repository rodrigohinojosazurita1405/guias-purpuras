"""
Decoradores para proteger endpoints con autenticación JWT
"""
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def token_required(view_func):
    """
    Decorador que requiere un token JWT válido en el header Authorization

    Uso:
        @token_required
        def mi_vista(request):
            # request.user estará disponible
            pass
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()

        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return JsonResponse({
                'success': False,
                'message': 'Token de autenticación requerido'
            }, status=401)

        token_str = auth_header[1]

        try:
            # Decodificar token para obtener el user_id
            untyped_token = UntypedToken(token_str)
            user_id = untyped_token.get('user_id')

            if not user_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Token inválido'
                }, status=401)

            # Obtener el usuario
            try:
                user = User.objects.get(id=user_id)
                request.user = user
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }, status=404)

            return view_func(request, *args, **kwargs)

        except (InvalidToken, TokenError):
            return JsonResponse({
                'success': False,
                'message': 'Token inválido o expirado'
            }, status=401)
        except Exception as e:
            print(f'Error en token_required: {str(e)}')
            return JsonResponse({
                'success': False,
                'message': f'Error de autenticación: {str(e)}'
            }, status=500)

    return wrapper
