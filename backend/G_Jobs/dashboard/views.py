"""
API Views para Dashboard de Usuario
Endpoints para estadísticas y actividades del usuario
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from auth_api.decorators import token_required
from G_Jobs.jobs.models import Job
from profiles.models import CompanyProfile
from G_Jobs.plans.models import Plan


@require_http_methods(["GET"])
@csrf_exempt
def get_user_statistics(request):
    """
    Endpoint para obtener estadísticas del usuario en el dashboard
    GET /api/user/stats?email=user@example.com

    Retorna:
    - jobsPublished: número total de trabajos publicados
    - jobsActive: número de trabajos activos
    - applications: total de aplicaciones recibidas
    - applicationsNew: aplicaciones nuevas (estado 'received')
    - totalViews: total de vistas en todos los trabajos
    - profileComplete: booleano indicando si perfil está completo
    """
    try:
        # Obtener email del usuario
        email = request.GET.get('email', '')
        print(f'\n📊 [STATS] ========================================')
        print(f'📊 [STATS] Email recibido: {email}')

        # Obtener todos los trabajos del usuario (excluir eliminados)
        all_user_jobs = Job.objects.filter(email=email, isDeleted=False)
        print(f'📊 [STATS] Jobs NO eliminados: {all_user_jobs.count()}')

        # Trabajos publicados = trabajos con pago verificado
        user_jobs = all_user_jobs.filter(paymentVerified=True)
        print(f'📊 [STATS] Jobs con pago verificado: {user_jobs.count()}')

        jobsPublished = user_jobs.count()
        jobsActive = user_jobs.filter(status='active').count()
        print(f'📊 [STATS] Jobs ACTIVOS (status=active): {jobsActive}')

        # Debug: mostrar todos los estados
        for job in user_jobs:
            print(f'📊 [STATS]   - Job {job.id}: {job.title[:30]} | status={job.status} | verified={job.paymentVerified} | deleted={job.isDeleted}')
        print(f'📊 [STATS] ========================================\n')

        # Contar aplicaciones (usando campo applications del Job)
        totalApplications = sum(job.applications for job in user_jobs)
        newApplications = 0  # TODO: Implementar cuando se tenga modelo Application

        # Contar vistas
        totalViews = sum(job.views for job in user_jobs)

        # Calcular completitud del perfil de empresa
        profileComplete = False
        profilePercentage = 0

        try:
            # Buscar perfil de empresa por email
            company_profile = CompanyProfile.objects.filter(email=email).first()

            if company_profile:
                # Campos obligatorios que se deben completar
                required_fields = {
                    'companyName': company_profile.companyName,
                    'description': company_profile.description,
                    'logo': company_profile.logo,
                    'email': company_profile.email,
                    'location': company_profile.location,
                }

                # Campos opcionales que suman al porcentaje
                optional_fields = {
                    'banner': company_profile.banner,
                    'contactEmail': company_profile.contactEmail,
                    'phone': company_profile.phone,
                    'website': company_profile.website,
                    'city': company_profile.city,
                }

                # Función helper para verificar si un campo está completo
                def is_field_complete(value):
                    if value is None:
                        return False
                    if isinstance(value, str):
                        return bool(value.strip())  # String no vacío
                    return bool(value)  # Para archivos (logo, banner)

                # Contar campos completados
                completed_required = sum(1 for v in required_fields.values() if is_field_complete(v))
                completed_optional = sum(1 for v in optional_fields.values() if is_field_complete(v))

                total_fields = len(required_fields) + len(optional_fields)
                completed_fields = completed_required + completed_optional

                # Calcular porcentaje (60% peso a obligatorios, 40% a opcionales)
                required_weight = 0.6
                optional_weight = 0.4

                required_percentage = (completed_required / len(required_fields)) * required_weight
                optional_percentage = (completed_optional / len(optional_fields)) * optional_weight

                profilePercentage = int((required_percentage + optional_percentage) * 100)

                # Perfil completo si tiene al menos 80% y todos los campos obligatorios
                profileComplete = (profilePercentage >= 80 and completed_required == len(required_fields))

                print(f'📊 [STATS] Perfil encontrado: {company_profile.companyName}')
                print(f'📊 [STATS] Campos obligatorios: {completed_required}/{len(required_fields)}')
                print(f'📊 [STATS] Campos opcionales: {completed_optional}/{len(optional_fields)}')
                print(f'📊 [STATS] Porcentaje: {profilePercentage}% | Completo: {profileComplete}')
            else:
                print(f'📊 [STATS] No se encontró perfil de empresa para {email}')
        except Exception as profile_err:
            print(f'⚠️ [STATS] Error calculando perfil: {profile_err}')

        return JsonResponse({
            'success': True,
            'statistics': {
                # Nombres agnósticos para cualquier tipo de guía
                'totalPublished': jobsPublished,
                'activeListings': jobsActive,
                'totalApplications': totalApplications,
                'newApplications': newApplications,
                'totalViews': totalViews,
                'profileComplete': profileComplete,
                'profilePercentage': profilePercentage,
                # Mantener nombres antiguos para compatibilidad
                'jobsPublished': jobsPublished,
                'jobsActive': jobsActive,
                'applications': totalApplications,
                'applicationsNew': newApplications
            }
        }, status=200)

    except Exception as e:
        print(f'Error al obtener estadísticas: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_user_published_jobs(request):
    """
    Endpoint para obtener trabajos publicados por el usuario
    GET /api/user/published?email=user@example.com

    Retorna:
    - Lista de trabajos publicados con información resumida
    - Incluye estado de verificación de pago
    - Solo muestra como "visible" si está activo Y verificado
    """
    email = request.GET.get('email', '')
    print(f'[ENDPOINT] get_user_published_jobs called')
    print(f'[ENDPOINT] Request user: {request.user}')
    print(f'[ENDPOINT] Email buscando: {email}')

    if not email:
        return JsonResponse({
            'success': False,
            'message': 'Email requerido'
        }, status=400)

    try:
        # Excluir trabajos eliminados
        jobs = Job.objects.filter(email=email, isDeleted=False).order_by('-createdAt')

        # Convertir a lista con fechas como strings
        jobs_list = []
        for job in jobs:
            # Determinar si el trabajo es visible públicamente
            is_publicly_visible = job.status == 'active' and job.paymentVerified and not job.isDeleted

            # Obtener logo del perfil de empresa si existe
            company_logo = None
            if job.companyProfile and job.companyProfile.logo:
                logo_url = job.companyProfile.logo.url
                # Si la URL es relativa, hacerla absoluta
                if not logo_url.startswith(('http://', 'https://')):
                    company_logo = request.build_absolute_uri(logo_url)
                else:
                    company_logo = logo_url

            # Obtener información del plan desde la base de datos
            plan_label = None
            plan_price = None
            plan_duration = None

            if job.selectedPlan:
                try:
                    plan = Plan.objects.filter(name=job.selectedPlan).first()
                    if plan:
                        plan_label = plan.label
                        plan_price = f"{plan.price} {plan.currency}"
                        plan_duration = f"{plan.duration_days} días"
                except Exception as e:
                    print(f'Warning: Could not load plan info for {job.selectedPlan}: {e}')

            job_dict = {
                'id': str(job.id),
                'title': str(job.title),
                'companyName': str(job.companyName),
                'companyLogo': company_logo,
                'status': str(job.status),
                'paymentVerified': bool(job.paymentVerified),
                'isPubliclyVisible': is_publicly_visible,
                'views': int(job.views or 0),
                'applications': int(job.applications or 0),
                'createdAt': str(job.createdAt.isoformat()) if job.createdAt else None,
                'expiryDate': str(job.expiryDate.isoformat()) if job.expiryDate else None,
                'selectedPlan': str(job.selectedPlan) if job.selectedPlan else None,
                'planLabel': plan_label,
                'planPrice': plan_price,
                'planDuration': plan_duration,
                'city': str(job.city) if job.city else '',
                'modality': str(job.modality) if job.modality else ''
            }
            jobs_list.append(job_dict)

        print(f'DEBUG: get_user_published_jobs - Total de trabajos encontrados: {len(jobs_list)}')

        return JsonResponse({
            'success': True,
            'jobs': jobs_list
        })

    except Exception as e:
        import traceback
        print(f'ERROR en get_user_published_jobs: {str(e)}')
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': f'Error al obtener trabajos: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_user_applied_jobs(request):
    """
    Endpoint para obtener trabajos a los que el usuario ha aplicado
    GET /api/user/applied?email=user@example.com

    Retorna:
    - Lista de trabajos con estado de aplicación
    """
    try:
        email = request.GET.get('email', '')
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email requerido'
            }, status=400)

        # TODO: Implementar cuando se tenga modelo Application
        # Por ahora retornar lista vacía
        # Obtener aplicaciones del usuario
        # applications = Application.objects.filter(
        #     applicantEmail=email
        # ).select_related('job').values(
        #     'id', 'job__id', 'job__title', 'job__companyName',
        #     'job__city', 'job__modality', 'status', 'createdAt', 'recruiterNotes'
        # ).order_by('-createdAt')

        # result = []
        # for app in applications:
        #     result.append({
        #         'id': app['id'],
        #         'jobId': app['job__id'],
        #         'jobTitle': app['job__title'],
        #         'companyName': app['job__companyName'],
        #         'jobCity': app['job__city'],
        #         'jobModality': app['job__modality'].capitalize(),
        #         'status': app['status'],
        #         'appliedAt': app['createdAt'],
        #         'recruiterNotes': app['recruiterNotes']
        #     })

        return JsonResponse({
            'success': True,
            'applications': []
        }, status=200)

    except Exception as e:
        print(f'Error al obtener trabajos aplicados: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_user_activities(request):
    """
    Endpoint para obtener actividades recientes del usuario
    GET /api/user/activities?email=user@example.com

    Retorna:
    - Lista de actividades recientes (publicar trabajo, aplicaciones, etc)
    """
    try:
        email = request.GET.get('email', '')
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email requerido'
            }, status=400)

        activities = []
        activity_id = 1

        # Trabajos publicados recientemente
        recent_jobs = Job.objects.filter(email=email).order_by('-createdAt')[:5]
        for job in recent_jobs:
            activities.append({
                'id': activity_id,
                'type': 'job',
                'title': f'Publicaste "{job.title}"',
                'description': 'Se publicó una nueva oferta de empleo',
                'date': job.createdAt.isoformat(),
                'metadata': {'jobId': str(job.id)}
            })
            activity_id += 1

        # TODO: Aplicaciones recibidas recientemente (cuando se implemente modelo Application)
        # Por ahora, solo mostramos actividades de trabajos publicados

        # Ordenar por fecha descendente y limitar a 5
        activities.sort(key=lambda x: x['date'], reverse=True)
        activities = activities[:5]

        return JsonResponse({
            'success': True,
            'activities': activities
        }, status=200)

    except Exception as e:
        print(f'Error al obtener actividades: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
