"""
API Views para Órdenes y Pagos
Endpoints para gestionar órdenes de planes de pago
"""
import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from auth_api.decorators import token_required
from .models import PlanOrder


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_user_orders(request):
    """
    Obtener todas las órdenes de planes del usuario (empresa)
    GET /api/orders/me

    Returns:
    {
        'success': bool,
        'orders': [
            {
                'id': int,
                'invoiceNumber': str,
                'planLabel': str,
                'razonSocial': str,
                'nit': str,
                'ci': str,
                'amountPaid': float,
                'status': str,
                'orderDate': str (ISO),
                'electronicInvoiceSentDate': str (ISO) or null,
                'electronicInvoiceEmail': str,
                'electronicInvoiceWhatsapp': str
            }
        ],
        'count': int
    }
    """
    try:
        # Obtener órdenes del usuario autenticado
        orders = PlanOrder.objects.filter(user=request.user)

        # Serializar órdenes
        orders_data = []
        for order in orders:
            # Obtener logo de la empresa desde el job asociado
            company_logo = None
            job_title = None
            company_name = None

            if order.job:
                job_title = order.job.title
                company_name = order.job.companyName

                if order.job.companyProfile and order.job.companyProfile.logo:
                    logo_url = order.job.companyProfile.logo.url
                    # Si la URL es relativa, hacerla absoluta
                    if not logo_url.startswith(('http://', 'https://')):
                        company_logo = request.build_absolute_uri(logo_url)
                    else:
                        company_logo = logo_url

            orders_data.append({
                'id': order.id,
                'invoiceNumber': f'ORD-{order.id}',  # Número de orden basado en ID
                'planLabel': order.selected_plan.capitalize(),
                'razonSocial': order.razon_social,
                'nit': order.nit,
                'ci': order.ci,
                'ciComplement': order.ci_complement,
                'email': order.email,
                'electronicInvoiceEmail': order.email,  # Email para factura
                'whatsapp': order.whatsapp,
                'electronicInvoiceWhatsapp': order.whatsapp,  # WhatsApp para factura
                'amountPaid': float(order.plan_price),
                'status': order.status,
                'statusDisplay': order.get_status_display(),
                'orderDate': order.created_at.isoformat(),
                'electronicInvoiceSentDate': order.updated_at.isoformat() if order.status == 'completed' else None,
                'createdAt': order.created_at.isoformat(),
                'updatedAt': order.updated_at.isoformat(),
                'companyData': {
                    'requires_invoice': bool(
                        order.razon_social and
                        order.razon_social.lower() not in ['sin razon social', 'sin razón social', '0', 'no', 'n/a', ''] and
                        order.nit and
                        order.nit not in ['0', '00', 'no', 'n/a', '']
                    ),
                    'job_title': job_title,
                    'company_name': company_name,
                    'company_logo': company_logo
                }
            })

        return JsonResponse({
            'success': True,
            'orders': orders_data,
            'count': len(orders_data)
        }, status=200)

    except Exception as e:
        print(f'[ORDERS] Error al obtener órdenes: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_order_detail(request, order_id):
    """
    Obtener detalles de una orden específica
    GET /api/orders/:id

    Returns:
    {
        'success': bool,
        'order': { ... orden completa ... }
    }
    """
    try:
        # Obtener la orden y verificar que pertenece al usuario
        order = PlanOrder.objects.get(id=order_id, user=request.user)

        order_data = {
            'id': order.id,
            'invoiceNumber': f'ORD-{order.id}',
            'planLabel': order.selected_plan.capitalize(),
            'planName': order.selected_plan,
            'razonSocial': order.razon_social,
            'nit': order.nit,
            'ci': order.ci,
            'ciComplement': order.ci_complement,
            'email': order.email,
            'electronicInvoiceEmail': order.email,
            'whatsapp': order.whatsapp,
            'electronicInvoiceWhatsapp': order.whatsapp,
            'amountPaid': float(order.plan_price),
            'status': order.status,
            'statusDisplay': order.get_status_display(),
            'orderDate': order.created_at.isoformat(),
            'electronicInvoiceSentDate': order.updated_at.isoformat() if order.status == 'completed' else None,
            'createdAt': order.created_at.isoformat(),
            'updatedAt': order.updated_at.isoformat(),
            'companyData': {
                'requires_invoice': bool(order.razon_social and order.razon_social != 'Sin razon social')
            }
        }

        return JsonResponse({
            'success': True,
            'order': order_data
        }, status=200)

    except PlanOrder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Orden no encontrada o no tienes permiso para verla'
        }, status=404)

    except Exception as e:
        print(f'[ORDERS] Error al obtener detalle de orden: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_pending_orders_count(request):
    """
    Obtener el conteo de órdenes pendientes (processing) del usuario
    GET /api/user/orders/pending-count/

    Returns:
    {
        'success': bool,
        'count': int
    }
    """
    try:
        # Contar órdenes en estado 'processing'
        count = PlanOrder.objects.filter(
            user=request.user,
            status='processing'
        ).count()

        return JsonResponse({
            'success': True,
            'count': count
        }, status=200)

    except Exception as e:
        print(f'[ORDERS] Error al obtener conteo de órdenes pendientes: {str(e)}')
        return JsonResponse({
            'success': False,
            'count': 0
        }, status=200)  # Devolver 200 con count 0 en vez de error


@token_required
@require_http_methods(["POST"])
@csrf_exempt
def resend_invoice(request, order_id):
    """
    Reenviar factura electrónica por email o WhatsApp
    POST /api/orders/:id/resend-invoice

    Body:
    {
        'method': 'email' | 'whatsapp' (opcional, por defecto intenta ambas)
    }

    Returns:
    {
        'success': bool,
        'message': str,
        'updatedOrder': { ... }
    }
    """
    try:
        # Obtener la orden
        order = PlanOrder.objects.get(id=order_id, user=request.user)

        # Parsear body
        body = json.loads(request.body) if request.body else {}
        method = body.get('method', 'both')

        # Actualizar fecha de envío
        order.electronic_invoice_sent_date = datetime.now()
        order.save()

        # Aquí iría la lógica de envío real (email/WhatsApp)
        # Por ahora solo registramos el intento
        message = f'Factura reenviada por {method}'

        order_data = {
            'id': order.id,
            'invoiceNumber': order.invoice_number,
            'status': order.status,
            'electronicInvoiceSentDate': order.electronic_invoice_sent_date.isoformat()
        }

        return JsonResponse({
            'success': True,
            'message': message,
            'updatedOrder': order_data
        }, status=200)

    except PlanOrder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Orden no encontrada'
        }, status=404)

    except Exception as e:
        print(f'[ORDERS] Error al reenviar factura: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
