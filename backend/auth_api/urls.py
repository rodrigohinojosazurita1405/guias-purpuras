from django.urls import path
from . import views

app_name = 'auth_api'

urlpatterns = [
    path('auth/register', views.register, name='register'),
    path('auth/login', views.login, name='login'),
    path('auth/refresh', views.refresh_token, name='refresh_token'),
    path('auth/logout', views.logout, name='logout'),
    path('auth/verify', views.verify_token, name='verify_token'),
    path('auth/forgot-password', views.forgot_password, name='forgot_password'),
    path('auth/reset-password', views.reset_password, name='reset_password'),
]
