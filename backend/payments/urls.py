from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Órdenes del usuario
    path('orders/me/', views.get_user_orders, name='get_user_orders'),
    path('orders/<int:order_id>/', views.get_order_detail, name='get_order_detail'),
    path('orders/<int:order_id>/resend-invoice/', views.resend_invoice, name='resend_invoice'),
]
