from django.urls import path
from . import views

app_name = 'catalogs'

urlpatterns = [
    # Categorías de trabajo
    path('jobs/categories', views.get_job_categories, name='get_job_categories'),
    path('jobs/categories-dynamic/', views.get_job_categories_dynamic, name='get_job_categories_dynamic'),

    # Tipos de contrato
    path('jobs/contract-types/', views.get_contract_types, name='get_contract_types'),

    # Ciudades
    path('jobs/cities/', views.get_cities, name='get_cities'),
]
