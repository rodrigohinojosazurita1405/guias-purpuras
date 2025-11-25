from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Publicar nuevo trabajo
    path('jobs/publish', views.publish_job, name='publish_job'),

    # Job Categories Endpoint (DEBE estar antes del patrón genérico jobs/)
    path('jobs/categories', views.get_job_categories, name='get_job_categories'),

    # Listar trabajos
    path('jobs/', views.list_jobs, name='list_jobs'),

    # Obtener detalle de un trabajo (DEBE estar después de /publish para evitar conflictos)
    path('jobs/<str:job_id>/', views.get_job, name='get_job'),

    # Aplicar a un trabajo
    path('jobs/<str:job_id>/apply', views.apply_to_job, name='apply_to_job'),

    # Listar aplicaciones de un trabajo
    path('jobs/<str:job_id>/applications', views.list_applications, name='list_applications'),

    # Actualizar estado de una aplicación
    path('jobs/<str:job_id>/applications/<str:application_id>', views.update_application_status, name='update_application_status'),

    # Dashboard Statistics Endpoints
    path('user/stats', views.get_user_statistics, name='get_user_statistics'),
    path('user/published', views.get_user_published_jobs, name='get_user_published_jobs'),
    path('user/applied', views.get_user_applied_jobs, name='get_user_applied_jobs'),
    path('user/activities', views.get_user_activities, name='get_user_activities'),
]
