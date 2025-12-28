"""
API Views para sistema de auditoría
Endpoints para consultar logs de actividad del usuario
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from auth_api.decorators import token_required
from .models import AuditLog
from django.db.models import Q


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_user_activity_logs(request):
    """
    Obtener logs de actividad del usuario actual
    GET /api/audit/my-activity

    Query params:
    - limit: Número máximo de registros (default: 50, max: 200)
    - offset: Offset para paginación (default: 0)
    - action: Filtrar por tipo de acción (create, update, delete, etc.)
    - severity: Filtrar por severidad (info, warning, critical)

    Returns:
    {
        'success': bool,
        'logs': [
            {
                'id': int,
                'action': str,
                'actionDisplay': str,
                'objectType': str,
                'objectRepr': str,
                'description': str,
                'timestamp': str (ISO),
                'severity': str,
                'changes': dict
            }
        ],
        'count': int,
        'total': int
    }
    """
    try:
        # Obtener parámetros de query
        limit = min(int(request.GET.get('limit', 50)), 200)
        offset = int(request.GET.get('offset', 0))
        action_filter = request.GET.get('action', '')
        severity_filter = request.GET.get('severity', '')

        # Query base: logs del usuario actual
        logs = AuditLog.objects.filter(user=request.user).select_related('content_type')

        # Aplicar filtros opcionales
        if action_filter:
            logs = logs.filter(action=action_filter)

        if severity_filter:
            logs = logs.filter(severity=severity_filter)

        # Contar total antes de paginar
        total_count = logs.count()

        # Paginar
        logs = logs[offset:offset + limit]

        # Serializar
        logs_data = []
        for log in logs:
            logs_data.append({
                'id': log.id,
                'action': log.action,
                'actionDisplay': log.get_action_display(),
                'objectType': log.content_type.model,
                'objectTypeDisplay': log.content_type.name,
                'objectRepr': log.object_repr,
                'description': log.action_description,
                'timestamp': log.timestamp.isoformat(),
                'severity': log.severity,
                'severityDisplay': log.get_severity_display(),
                'changes': log.changes,
                'ipAddress': log.ip_address,
            })

        return JsonResponse({
            'success': True,
            'logs': logs_data,
            'count': len(logs_data),
            'total': total_count
        }, status=200)

    except Exception as e:
        print(f'[AUDIT] Error al obtener logs de actividad: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_activity_summary(request):
    """
    Obtener resumen de actividad del usuario
    GET /api/audit/my-summary

    Returns:
    {
        'success': bool,
        'summary': {
            'totalActions': int,
            'totalCreates': int,
            'totalUpdates': int,
            'totalDeletes': int,
            'recentActions': int (últimos 7 días),
            'byAction': { ... },
            'bySeverity': { ... }
        }
    }
    """
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count

        # Logs del usuario
        user_logs = AuditLog.objects.filter(user=request.user)

        # Contar por acción
        by_action = user_logs.values('action').annotate(count=Count('action'))
        action_counts = {item['action']: item['count'] for item in by_action}

        # Contar por severidad
        by_severity = user_logs.values('severity').annotate(count=Count('severity'))
        severity_counts = {item['severity']: item['count'] for item in by_severity}

        # Actividad reciente (últimos 7 días)
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_count = user_logs.filter(timestamp__gte=seven_days_ago).count()

        summary = {
            'totalActions': user_logs.count(),
            'totalCreates': action_counts.get('create', 0),
            'totalUpdates': action_counts.get('update', 0),
            'totalDeletes': action_counts.get('delete', 0) + action_counts.get('soft_delete', 0),
            'recentActions': recent_count,
            'byAction': action_counts,
            'bySeverity': severity_counts
        }

        return JsonResponse({
            'success': True,
            'summary': summary
        }, status=200)

    except Exception as e:
        print(f'[AUDIT] Error al obtener resumen de actividad: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
