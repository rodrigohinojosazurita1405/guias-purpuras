from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Dashboard Statistics Endpoints (prioritarios)
    path('user/stats', views.get_user_statistics, name='get_user_statistics'),
    path('user/published', views.get_user_published_jobs, name='get_user_published_jobs'),
    path('user/applied', views.get_user_applied_jobs, name='get_user_applied_jobs'),
    path('user/activities', views.get_user_activities, name='get_user_activities'),

    # Publicar nuevo trabajo
    path('jobs/publish', views.publish_job, name='publish_job'),

    # Job Categories Endpoint (DEBE estar antes del patrón genérico)
    path('jobs/categories', views.get_job_categories, name='get_job_categories'),

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
]
