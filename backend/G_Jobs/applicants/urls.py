from django.urls import path
from . import views

app_name = 'applicants'

urlpatterns = [
    # ========== CVs CRUD Endpoints ==========
    path('cvs/save/', views.save_cv, name='save_cv'),
    path('cvs/list/', views.list_cvs, name='list_cvs'),
    path('cvs/<uuid:cv_id>/', views.get_cv_detail, name='get_cv_detail'),
    path('cvs/<uuid:cv_id>/update/', views.update_cv, name='update_cv'),
    path('cvs/<uuid:cv_id>/delete/', views.delete_cv, name='delete_cv'),

    # ========== Postulaciones Endpoints ==========
    path('jobs/<str:job_id>/check-blocked/', views.check_if_blocked, name='check_if_blocked'),
    path('apply/<str:job_id>/', views.apply_to_job, name='apply_to_job'),
    path('applications/', views.get_user_applications, name='get_user_applications'),
    path('applications/<uuid:application_id>/', views.get_application_detail, name='get_application_detail'),
    path('applications/<uuid:application_id>/withdraw/', views.withdraw_application, name='withdraw_application'),

    # ========== Trabajos Guardados Endpoints ==========
    path('saved-jobs/save/', views.save_job, name='save_job'),
    path('saved-jobs/unsave/', views.unsave_job, name='unsave_job'),
    path('saved-jobs/', views.get_saved_jobs, name='get_saved_jobs'),
    path('saved-jobs/check/<str:job_id>/', views.check_job_saved, name='check_job_saved'),

    # ========== Perfil de Postulante Endpoints ==========
    path('profile/', views.get_applicant_profile, name='get_applicant_profile'),
    path('profile/update/', views.update_applicant_profile, name='update_applicant_profile'),
]
