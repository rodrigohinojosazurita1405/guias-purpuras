"""
URLs para sistema de auditoría
"""
from django.urls import path
from . import views

urlpatterns = [
    # Logs de actividad del usuario
    path('my-activity/', views.get_user_activity_logs, name='user_activity_logs'),

    # Resumen de actividad
    path('my-summary/', views.get_activity_summary, name='activity_summary'),
]
