from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # ========== USER PROFILE ROUTES ==========
    # Obtener o crear perfil del usuario autenticado
    path('me/', views.get_or_create_my_profile, name='get_or_create_my_profile'),

    # Crear perfil de usuario
    path('user/create', views.create_user_profile, name='create_user_profile'),

    # Obtener perfil por email
    path('user/email/<str:email>/', views.get_user_profile_by_email, name='get_user_profile_by_email'),

    # Cargar foto de perfil de usuario (more specific - must come before generic user/<id>/)
    path('user/<str:user_id>/photo', views.upload_user_photo, name='upload_user_photo'),

    # Eliminar foto de perfil de usuario
    path('user/<str:user_id>/photo/delete', views.delete_user_photo, name='delete_user_photo'),

    # Actualizar perfil de usuario
    path('user/<str:user_id>/edit', views.update_user_profile, name='update_user_profile'),

    # Obtener perfil por ID (more generic - must come last)
    path('user/<str:user_id>/', views.get_user_profile, name='get_user_profile'),

    # ========== COMPANY PROFILE ROUTES ==========
    # Obtener empresa del usuario autenticado
    path('company/me/', views.get_or_create_my_company, name='get_or_create_my_company'),

    # Crear perfil de empresa
    path('company/create', views.create_company_profile, name='create_company_profile'),

    # Obtener perfil de empresa por ID
    path('company/<str:company_id>/', views.get_company_profile, name='get_company_profile'),

    # Actualizar perfil de empresa (matches both /company/<id>/ with PATCH and /company/<id>/edit)
    # Note: update_company_profile handles PATCH on /company/<id>/

    # Listar empresas del usuario
    path('user/<str:user_id>/companies', views.list_user_companies, name='list_user_companies'),

    # ========== COMPANY LOGO ROUTES ==========
    # Cargar y eliminar logo de empresa
    path('company/<str:company_id>/logo', views.upload_company_logo, name='upload_company_logo'),
    path('company/<str:company_id>/logo/delete', views.delete_company_logo, name='delete_company_logo'),

    # ========== COMPANY BANNER ROUTES ==========
    # Cargar y eliminar banner de empresa
    path('company/<str:company_id>/banner/delete', views.delete_company_banner, name='delete_company_banner'),
]
