from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Plan


@require_http_methods(["GET"])
def get_plans(request):
    """
    Retorna todos los planes activos en formato JSON
    GET /api/plans/
    """
    plans = Plan.objects.filter(is_active=True).order_by('order')

    plans_data = [plan.to_dict() for plan in plans]

    return JsonResponse({
        'success': True,
        'data': plans_data,
        'count': len(plans_data)
    })
