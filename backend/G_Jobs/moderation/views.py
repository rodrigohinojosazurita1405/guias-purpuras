"""
API Views para Moderación de Usuarios
Endpoints para bloquear/desbloquear usuarios
"""
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from auth_api.decorators import token_required
from .models import BlockedUser
from auth_api.models import CustomUser


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_blocked_users(request):
    """
    Obtener lista de usuarios bloqueados por la empresa actual
    GET /api/blocked-users/me

    Returns:
    {
        'success': bool,
        'blockedUsers': [
            {
                'id': int,
                'email': str,
                'reason': str,
                'reasonDisplay': str,
                'reasonNotes': str,
                'blockedAt': str (ISO),
                'blockedUntil': str (ISO) or null,
                'isPermanent': bool
            }
        ],
        'count': int
    }
    """
    try:
        # Obtener usuarios bloqueados por esta empresa
        blocked = BlockedUser.objects.filter(company=request.user).select_related('blocked_user')

        # Serializar
        blocked_data = []
        for block in blocked:
            blocked_data.append({
                'id': block.id,
                'email': block.blocked_user.email,
                'firstName': block.blocked_user.first_name,
                'lastName': block.blocked_user.last_name,
                'reason': block.reason,
                'reasonDisplay': block.get_reason_display(),
                'notes': block.notes,
                'blockedAt': block.blocked_at.isoformat(),
                'blockedUserId': block.blocked_user.id
            })

        return JsonResponse({
            'success': True,
            'blockedUsers': blocked_data,
            'count': len(blocked_data)
        }, status=200)

    except Exception as e:
        print(f'[BLOCKED] Error al obtener usuarios bloqueados: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["POST"])
@csrf_exempt
def block_user(request):
    """
    Bloquear un usuario
    POST /api/blocked-users/block

    Body:
    {
        'blockedUserId': int,
        'reason': 'SPAM' | 'UNQUALIFIED' | 'OTHER',
        'reasonNotes': str (opcional),
        'isPermanent': bool (opcional, default true)
    }

    Returns:
    {
        'success': bool,
        'message': str,
        'blockedUser': { ... }
    }
    """
    try:
        # Parsear body
        body = json.loads(request.body)
        blocked_user_id = body.get('blockedUserId')
        reason = body.get('reason', 'other')
        notes = body.get('notes', '')

        if not blocked_user_id:
            return JsonResponse({
                'success': False,
                'message': 'blockedUserId es requerido'
            }, status=400)

        # Obtener el usuario a bloquear
        try:
            blocked_user = CustomUser.objects.get(id=blocked_user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario a bloquear no encontrado'
            }, status=404)

        # Verificar si ya existe bloqueo
        existing = BlockedUser.objects.filter(company=request.user, blocked_user=blocked_user).first()
        if existing:
            return JsonResponse({
                'success': False,
                'message': 'Este usuario ya está bloqueado'
            }, status=400)

        # Crear bloqueo
        block = BlockedUser.objects.create(
            company=request.user,
            blocked_user=blocked_user,
            reason=reason,
            notes=notes
        )

        blocked_data = {
            'id': block.id,
            'email': block.blocked_user.email,
            'firstName': block.blocked_user.first_name,
            'lastName': block.blocked_user.last_name,
            'reason': block.reason,
            'reasonDisplay': block.get_reason_display(),
            'notes': block.notes,
            'blockedAt': block.blocked_at.isoformat(),
            'blockedUserId': block.blocked_user.id
        }

        return JsonResponse({
            'success': True,
            'message': f'Usuario {blocked_user.email} bloqueado correctamente',
            'blockedUser': blocked_data
        }, status=201)

    except Exception as e:
        print(f'[BLOCKED] Error al bloquear usuario: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["DELETE"])
@csrf_exempt
def unblock_user(request, block_id):
    """
    Desbloquear un usuario
    DELETE /api/blocked-users/:id

    Returns:
    {
        'success': bool,
        'message': str
    }
    """
    try:
        # Obtener y eliminar el bloqueo
        block = BlockedUser.objects.get(id=block_id, company=request.user)
        blocked_email = block.blocked_user.email

        block.delete()

        return JsonResponse({
            'success': True,
            'message': f'Usuario {blocked_email} desbloqueado correctamente'
        }, status=200)

    except BlockedUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Bloqueo no encontrado'
        }, status=404)

    except Exception as e:
        print(f'[BLOCKED] Error al desbloquear usuario: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@csrf_exempt
def check_if_blocked(request, user_id):
    """
    Verificar si un usuario está bloqueado para una empresa
    GET /api/blocked-users/check/:userId

    Params:
    - company_id: ID de la empresa (si no se proporciona, usa el usuario actual si está autenticado)

    Returns:
    {
        'success': bool,
        'isBlocked': bool,
        'blockInfo': { ... } or null
    }
    """
    try:
        # Obtener empresa
        company_id = request.GET.get('company_id')

        if not company_id and not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'Empresa no especificada'
            }, status=400)

        # Usar empresa actual o la especificada
        company = request.user if request.user.is_authenticated and not company_id else None
        if company_id:
            try:
                company = CustomUser.objects.get(id=company_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Empresa no encontrada'
                }, status=404)

        # Obtener usuario
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=404)

        # Buscar bloqueo
        block = BlockedUser.objects.filter(company=company, blocked_user=user).first()

        if not block:
            return JsonResponse({
                'success': True,
                'isBlocked': False,
                'blockInfo': None
            }, status=200)

        block_info = {
            'id': block.id,
            'reason': block.reason,
            'reasonDisplay': block.get_reason_display(),
            'notes': block.notes
        }

        return JsonResponse({
            'success': True,
            'isBlocked': True,
            'blockInfo': block_info
        }, status=200)

    except Exception as e:
        print(f'[BLOCKED] Error al verificar bloqueo: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
