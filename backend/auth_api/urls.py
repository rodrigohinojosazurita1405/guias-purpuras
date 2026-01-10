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
    path('auth/change-password', views.change_password, name='change_password'),
    path('auth/check-delete-eligibility', views.check_delete_eligibility, name='check_delete_eligibility'),
    path('auth/delete-account', views.delete_account, name='delete_account'),
]
