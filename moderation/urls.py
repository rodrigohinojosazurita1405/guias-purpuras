from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    # Usuarios bloqueados
    path('blocked-users/me/', views.get_blocked_users, name='get_blocked_users'),
    path('blocked-users/block/', views.block_user, name='block_user'),
    path('blocked-users/<int:block_id>/', views.unblock_user, name='unblock_user'),
    path('blocked-users/check/<int:user_id>/', views.check_if_blocked, name='check_if_blocked'),
]
