"""
URLs para la app de reportes
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('<int:report_id>/view/', views.view_report, name='view'),
    path('<int:report_id>/download/', views.download_report_html, name='download'),
]
