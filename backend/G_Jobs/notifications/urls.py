from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Obtener notificaciones
    path('', views.get_notifications, name='get_notifications'),

    # Marcar como leída
    path('<uuid:notification_id>/mark-read/', views.mark_as_read, name='mark_as_read'),

    # Marcar todas como leídas
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),

    # Contador de no leídas
    path('unread-count/', views.get_unread_count, name='get_unread_count'),
]
