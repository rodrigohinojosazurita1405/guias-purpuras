from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Estadísticas del usuario
    path('user/stats/', views.get_user_statistics, name='get_user_statistics'),
    path('user/published/', views.get_user_published_jobs, name='get_user_published_jobs'),
    path('user/applied/', views.get_user_applied_jobs, name='get_user_applied_jobs'),
    path('user/activities/', views.get_user_activities, name='get_user_activities'),
]
