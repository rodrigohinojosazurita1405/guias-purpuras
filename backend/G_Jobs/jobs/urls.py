from django.urls import path
from . import views

# Import views from modular apps (refactorización)
from G_Jobs.catalogs import views as catalog_views
from G_Jobs.payments import views as payment_views
from G_Jobs.moderation import views as moderation_views
from G_Jobs.dashboard import views as dashboard_views

app_name = 'jobs'

urlpatterns = [
    # Dashboard Statistics Endpoints (prioritarios) - Ahora en dashboard app
    path('user/stats', dashboard_views.get_user_statistics, name='get_user_statistics'),
    path('user/published', dashboard_views.get_user_published_jobs, name='get_user_published_jobs'),
    path('user/applied', dashboard_views.get_user_applied_jobs, name='get_user_applied_jobs'),
    path('user/activities', dashboard_views.get_user_activities, name='get_user_activities'),

    # Publicar nuevo trabajo
    path('jobs/publish', views.publish_job, name='publish_job'),

    # Job Categories Endpoint (DEBE estar antes del patrón genérico) - Ahora en catalogs app
    path('jobs/categories', catalog_views.get_job_categories, name='get_job_categories'),

    # Endpoints dinámicos (DEBEN estar antes de los patrones genéricos) - Ahora en catalogs app
    path('jobs/contract-types/', catalog_views.get_contract_types, name='get_contract_types'),
    path('jobs/cities/', catalog_views.get_cities, name='get_cities'),
    path('jobs/categories-dynamic/', catalog_views.get_job_categories_dynamic, name='get_job_categories_dynamic'),

    # Listar trabajos
    path('jobs/', views.list_jobs, name='list_jobs'),

    # Verificar pago de un trabajo (FASE 7.1 - Solo Superadmin)
    path('jobs/<str:job_id>/verify-payment', views.verify_payment, name='verify_payment'),

    # Obtener detalle de un trabajo (DEBE estar después de /publish para evitar conflictos)
    path('jobs/<str:job_id>/', views.get_job, name='get_job'),

    # Actualizar un trabajo
    path('jobs/<str:job_id>/update', views.update_job, name='update_job'),

    # Eliminar un trabajo
    path('jobs/<str:job_id>/delete', views.delete_job, name='delete_job'),

    # Duplicar un trabajo
    path('jobs/<str:job_id>/duplicate/', views.duplicate_job, name='duplicate_job'),

    # Aplicar a un trabajo
    path('jobs/<str:job_id>/apply', views.apply_to_job, name='apply_to_job'),

    # Listar aplicaciones de un trabajo
    path('jobs/<str:job_id>/applications', views.list_applications, name='list_applications'),

    # Actualizar estado de una aplicación
    path('jobs/<str:job_id>/applications/<str:application_id>', views.update_application_status, name='update_application_status'),

    # ========== ENDPOINTS PARA ÓRDENES DE PLANES ========== - Ahora en payments app
    path('orders/me', payment_views.get_user_orders, name='get_user_orders'),
    path('orders/<int:order_id>/', payment_views.get_order_detail, name='get_order_detail'),
    path('orders/<int:order_id>/resend-invoice', payment_views.resend_invoice, name='resend_invoice'),

    # ========== ENDPOINTS PARA USUARIOS BLOQUEADOS ========== - Ahora en moderation app
    path('blocked-users/me', moderation_views.get_blocked_users, name='get_blocked_users'),
    path('blocked-users/block', moderation_views.block_user, name='block_user'),
    path('blocked-users/<int:block_id>/', moderation_views.unblock_user, name='unblock_user'),
    path('blocked-users/check/<int:user_id>/', moderation_views.check_if_blocked, name='check_if_blocked'),
]
