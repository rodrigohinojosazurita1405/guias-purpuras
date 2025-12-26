"""
API Views para Catálogos Dinámicos
Endpoints para obtener categorías, tipos de contrato y ciudades
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import JobCategory, ContractType, City


@require_http_methods(["GET"])
@csrf_exempt
def get_job_categories(request):
    """
    Endpoint para obtener la lista de categorías de trabajo disponibles
    GET /api/jobs/categories

    Returns:
    {
        'success': bool,
        'categories': [
            { 'text': 'Administración y Gestión', 'value': 'Administración y Gestión' },
            ...
        ],
        'count': int
    }
    """
    try:
        from G_Jobs.catalogs.models import JobCategory

        # Cargar desde base de datos (dinámico)
        categories_qs = JobCategory.objects.filter(is_active=True).order_by('order', 'name')

        # Convertir a formato de opciones
        categories = [
            {'text': cat.name, 'value': cat.name}
            for cat in categories_qs
        ]

        return JsonResponse({
            'success': True,
            'categories': categories,
            'count': len(categories)
        }, status=200)

    except Exception as e:
        print(f'Error al obtener categorías: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@csrf_exempt
def get_job_categories_dynamic(request):
    """
    Endpoint para obtener categorias de trabajo dinamicas
    GET /api/jobs/categories-dynamic
    """
    try:
        # Obtener todas las categorías activas (sin ordenar por 'order')
        categories = JobCategory.objects.filter(is_active=True)

        data = [
            {
                'text': cat.name,
                'value': cat.name,
                'slug': cat.slug,
                'icon': cat.icon
            }
            for cat in categories
        ]

        # Ordenar alfabéticamente por el campo 'text' usando Python
        data_sorted = sorted(data, key=lambda x: x['text'])

        return JsonResponse({
            'success': True,
            'categories': data_sorted,
            'count': len(data_sorted)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al cargar categorias: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@csrf_exempt
def get_contract_types(request):
    """
    Endpoint para obtener tipos de contrato dinamicos
    GET /api/jobs/contract-types
    """
    try:
        contract_types = ContractType.objects.filter(is_active=True).order_by('order', 'name')

        data = [
            {
                'text': ct.name,
                'value': ct.name,
                'slug': ct.slug
            }
            for ct in contract_types
        ]

        return JsonResponse({
            'success': True,
            'contractTypes': data,
            'count': len(data)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al cargar tipos de contrato: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@csrf_exempt
def get_cities(request):
    """
    Endpoint para obtener ciudades dinamicas
    GET /api/jobs/cities
    """
    try:
        cities = City.objects.filter(is_active=True).order_by('order', 'name')

        data = [
            {
                'text': city.name,
                'value': city.name,
                'slug': city.slug,
                'department': city.department,
                'region': city.region
            }
            for city in cities
        ]

        return JsonResponse({
            'success': True,
            'cities': data,
            'count': len(data)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al cargar ciudades: {str(e)}'
        }, status=500)
