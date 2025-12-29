"""
API Views para sistema de notificaciones
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from auth_api.decorators import token_required
from .models import Notification
import json


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_notifications(request):
    """
    Obtener notificaciones del usuario actual
    GET /api/notifications/

    Query params:
    - limit: Número máximo de registros (default: 50, max: 200)
    - offset: Offset para paginación (default: 0)
    - unread_only: true/false - Solo notificaciones no leídas
    - include_dismissed: true/false - Incluir notificaciones descartadas (default: false)

    Returns:
    {
        'success': bool,
        'notifications': [...],
        'count': int,
        'total': int,
        'unread_count': int
    }
    """
    try:
        # Parámetros de query
        limit = min(int(request.GET.get('limit', 50)), 200)
        offset = int(request.GET.get('offset', 0))
        unread_only = request.GET.get('unread_only', '').lower() == 'true'
        include_dismissed = request.GET.get('include_dismissed', '').lower() == 'true'

        # Query base
        notifications = Notification.objects.filter(user=request.user)

        # Por defecto, NO mostrar notificaciones descartadas (solo si se pide explícitamente)
        if not include_dismissed:
            notifications = notifications.filter(is_dismissed=False)

        # Filtrar solo no leídas si se solicita
        if unread_only:
            notifications = notifications.filter(is_read=False)

        # Contar total antes de paginar
        total_count = notifications.count()
        # Contador de no leídas NO incluye las descartadas
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False,
            is_dismissed=False
        ).count()
        # Contador de descartadas (para el historial)
        dismissed_count = Notification.objects.filter(
            user=request.user,
            is_dismissed=True
        ).count()

        # Paginar
        notifications = notifications[offset:offset + limit]

        # Serializar
        notifications_data = []
        for notif in notifications:
            notifications_data.append({
                'id': str(notif.id),
                'type': notif.notification_type,
                'typeDisplay': notif.get_notification_type_display(),
                'title': notif.title,
                'message': notif.message,
                'metadata': notif.metadata,
                'isRead': notif.is_read,
                'readAt': notif.read_at.isoformat() if notif.read_at else None,
                'createdAt': notif.created_at.isoformat(),
            })

        return JsonResponse({
            'success': True,
            'notifications': notifications_data,
            'count': len(notifications_data),
            'total': total_count,
            'unread_count': unread_count,
            'dismissed_count': dismissed_count
        }, status=200)

    except Exception as e:
        print(f'[NOTIFICATIONS] Error al obtener notificaciones: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["POST"])
@csrf_exempt
def mark_as_read(request, notification_id):
    """
    Marcar una notificación como leída
    POST /api/notifications/<notification_id>/mark-read/

    Returns:
    {
        'success': bool,
        'message': str
    }
    """
    try:
        notification = Notification.objects.filter(
            id=notification_id,
            user=request.user
        ).first()

        if not notification:
            return JsonResponse({
                'success': False,
                'message': 'Notificación no encontrada'
            }, status=404)

        notification.mark_as_read()

        return JsonResponse({
            'success': True,
            'message': 'Notificación marcada como leída'
        }, status=200)

    except Exception as e:
        print(f'[NOTIFICATIONS] Error al marcar como leída: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["POST"])
@csrf_exempt
def mark_all_as_read(request):
    """
    Marcar todas las notificaciones del usuario como leídas
    POST /api/notifications/mark-all-read/

    Returns:
    {
        'success': bool,
        'message': str,
        'count': int  # Cantidad de notificaciones marcadas
    }
    """
    try:
        from django.utils import timezone

        # Actualizar todas las notificaciones no leídas del usuario
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )

        return JsonResponse({
            'success': True,
            'message': f'{count} notificaciones marcadas como leídas',
            'count': count
        }, status=200)

    except Exception as e:
        print(f'[NOTIFICATIONS] Error al marcar todas como leídas: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["PATCH", "DELETE"])
@csrf_exempt
def dismiss_notification(request, notification_id):
    """
    Descartar/ocultar o eliminar permanentemente una notificación

    PATCH /api/notifications/<notification_id>/ - Descartar (archivar)
    DELETE /api/notifications/<notification_id>/ - Descartar (archivar) por defecto
    DELETE /api/notifications/<notification_id>/?permanent=true - Eliminar permanentemente

    Query params:
    - permanent: true/false - Si es true, elimina permanentemente (default: false)

    Returns:
    {
        'success': bool,
        'message': str,
        'action': 'dismissed' | 'deleted'
    }
    """
    try:
        notification = Notification.objects.filter(
            id=notification_id,
            user=request.user
        ).first()

        if not notification:
            return JsonResponse({
                'success': False,
                'message': 'Notificación no encontrada'
            }, status=404)

        # Verificar si se debe eliminar permanentemente
        permanent = request.GET.get('permanent', '').lower() == 'true'

        if permanent:
            # Eliminar permanentemente de la base de datos
            notification.delete()
            return JsonResponse({
                'success': True,
                'message': 'Notificación eliminada permanentemente',
                'action': 'deleted'
            }, status=200)
        else:
            # Descartar la notificación (ocultar, no eliminar)
            notification.dismiss()
            return JsonResponse({
                'success': True,
                'message': 'Notificación descartada exitosamente',
                'action': 'dismissed'
            }, status=200)

    except Exception as e:
        print(f'[NOTIFICATIONS] Error al procesar notificación: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_unread_count(request):
    """
    Obtener solo el contador de notificaciones no leídas (excluye descartadas)
    GET /api/notifications/unread-count/

    Returns:
    {
        'success': bool,
        'count': int
    }
    """
    try:
        # NO contar las descartadas
        count = Notification.objects.filter(
            user=request.user,
            is_read=False,
            is_dismissed=False
        ).count()

        return JsonResponse({
            'success': True,
            'count': count
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
