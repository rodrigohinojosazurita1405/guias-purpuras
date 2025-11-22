"""
API Views para Ofertas de Trabajo
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import Job, Application
from auth_api.decorators import token_required


@require_http_methods(["POST"])
@csrf_exempt
@token_required
def publish_job(request):
    """
    Endpoint para publicar una nueva oferta de trabajo
    POST /api/jobs/publish
    """
    try:
        # Parsear datos JSON del request
        data = json.loads(request.body)

        # Validaciones básicas
        if not data.get('title'):
            return JsonResponse({
                'success': False,
                'message': 'El título del puesto es requerido'
            }, status=400)

        if not data.get('description'):
            return JsonResponse({
                'success': False,
                'message': 'La descripción es requerida'
            }, status=400)

        if not data.get('email'):
            return JsonResponse({
                'success': False,
                'message': 'El email de contacto es requerido'
            }, status=400)

        # Crear objeto de trabajo
        job = Job.objects.create(
            title=data.get('title'),
            companyName=data.get('companyName', 'Empresa Confidencial'),
            companyAnonymous=data.get('companyAnonymous', False),
            description=data.get('description'),
            jobCategory=data.get('jobCategory'),
            city=data.get('city'),
            subcategory=data.get('subcategory', ''),
            contractType=data.get('contractType'),
            modality=data.get('modality', 'presencial'),
            expiryDate=data.get('expiryDate'),
            requirements=data.get('requirements'),
            responsibilities=data.get('responsibilities', ''),
            education=data.get('education', ''),
            experience=data.get('experience', ''),
            languages=data.get('languages', ''),
            technicalSkills=data.get('technicalSkills', ''),
            salaryType=data.get('salaryType', 'range'),
            salaryMin=data.get('salaryMin'),
            salaryMax=data.get('salaryMax'),
            salaryFixed=data.get('salaryFixed'),
            benefits=data.get('benefits', ''),
            vacancies=data.get('vacancies', 1),
            email=data.get('email'),
            whatsapp=data.get('whatsapp'),
            website=data.get('website', ''),
            applicationInstructions=data.get('applicationInstructions', ''),
            applicationType=data.get('applicationType', 'internal'),
            externalApplicationUrl=data.get('externalApplicationUrl', ''),
            selectedPlan=data.get('selectedPlan', 'free'),
            screeningQuestions=data.get('screeningQuestions', []),
        )

        # Respuesta exitosa
        return JsonResponse({
            'success': True,
            'message': '¡Oferta publicada exitosamente!',
            'id': job.id,
            'createdAt': job.createdAt.isoformat()
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error al publicar trabajo: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_job(request, job_id):
    """
    Endpoint para obtener detalles completos de una oferta de trabajo
    GET /api/jobs/<job_id>/
    Devuelve TODOS los campos necesarios para JobDetailView
    """
    try:
        job = Job.objects.get(id=job_id)

        # Incrementar vistas
        job.views += 1
        job.save(update_fields=['views'])

        return JsonResponse({
            'success': True,
            'job': {
                # Información básica
                'id': job.id,
                'title': job.title,
                'companyName': job.companyName if not job.companyAnonymous else 'Empresa Confidencial',
                'companyAnonymous': job.companyAnonymous,
                'companyLogo': job.companyProfile.logo.url if job.companyProfile and job.companyProfile.logo else None,
                'description': job.description,

                # Clasificación
                'jobCategory': job.jobCategory,
                'city': job.city,
                'subcategory': job.subcategory,
                'contractType': job.contractType,
                'modality': job.modality.capitalize() if hasattr(job, 'modality') else 'Presencial',
                'expiryDate': job.expiryDate.isoformat(),

                # Requisitos
                'requirements': job.requirements,
                'responsibilities': job.responsibilities,
                'education': job.education,
                'experience': job.experience,
                'languages': job.languages,
                'technicalSkills': job.technicalSkills,

                # Compensación
                'salaryType': job.salaryType,
                'salaryMin': str(job.salaryMin) if job.salaryMin else None,
                'salaryMax': str(job.salaryMax) if job.salaryMax else None,
                'salaryFixed': str(job.salaryFixed) if job.salaryFixed else None,
                'salary': format_salary(job),
                'benefits': job.benefits,
                'vacancies': job.vacancies,

                # Contacto
                'email': job.email,
                'whatsapp': job.whatsapp,
                'website': job.website,
                'applicationInstructions': job.applicationInstructions,

                # Aplicación
                'applicationType': job.applicationType,
                'externalApplicationUrl': job.externalApplicationUrl,
                'screeningQuestions': job.screeningQuestions,

                # Plan
                'selectedPlan': job.selectedPlan,

                # Estadísticas
                'views': job.views,
                'applications': job.applications,
                'publishedDaysAgo': calculate_days_ago(job.createdAt),

                # Timestamps
                'createdAt': job.createdAt.isoformat(),
                'updatedAt': job.updatedAt.isoformat(),
                'status': job.status
            }
        })

    except Job.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Oferta no encontrada'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


def format_salary(job):
    """Formatea el salario según el tipo"""
    if job.salaryType == 'range' and job.salaryMin and job.salaryMax:
        return f'Bs. {int(job.salaryMin)} - {int(job.salaryMax)}'
    elif job.salaryType == 'fixed' and job.salaryFixed:
        return f'Bs. {int(job.salaryFixed)}'
    elif job.salaryType == 'negotiable':
        return 'A convenir'
    else:
        return 'No Declarado'


def calculate_days_ago(date_obj):
    """Calcula cuántos días han pasado desde una fecha"""
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    if date_obj.tzinfo is None:
        date_obj = date_obj.replace(tzinfo=timezone.utc)
    days = (now - date_obj).days
    return days


@require_http_methods(["GET"])
def list_jobs(request):
    """
    Endpoint para listar todas las ofertas de trabajo
    GET /api/jobs/
    Formato optimizado para JobCard component
    """
    try:
        jobs = Job.objects.filter(status='active')

        # Filtros opcionales
        city = request.GET.get('city')
        category = request.GET.get('category')
        contract_type = request.GET.get('contractType')
        search = request.GET.get('search')

        if city:
            jobs = jobs.filter(city=city)

        if category:
            jobs = jobs.filter(jobCategory=category)

        if contract_type:
            jobs = jobs.filter(contractType=contract_type)

        if search:
            jobs = jobs.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search) |
                models.Q(companyName__icontains=search) |
                models.Q(jobCategory__icontains=search)
            )

        jobs_list = []
        for job in jobs.order_by('-createdAt')[:50]:  # Limitar a 50 resultados
            # Obtener logo del perfil de empresa si existe
            company_logo = None
            if job.companyProfile and job.companyProfile.logo:
                company_logo = job.companyProfile.logo.url

            jobs_list.append({
                'id': job.id,
                'title': job.title,
                'companyName': job.companyName if not job.companyAnonymous else 'Empresa Confidencial',
                'companyAnonymous': job.companyAnonymous,
                'companyLogo': company_logo,
                'city': job.city,
                'contractType': job.contractType,
                'modality': job.modality.capitalize() if hasattr(job, 'modality') else 'Presencial',
                'jobCategory': job.jobCategory,
                'salary': format_salary(job),
                'plan': job.selectedPlan,
                'verified': False,  # Por ahora, puede agregarse al modelo si se necesita
                'confidential': job.companyAnonymous,
                'views': job.views,
                'applications': job.applications,
                'createdAt': job.createdAt.isoformat(),
                'publishedDaysAgo': calculate_days_ago(job.createdAt),
            })

        return JsonResponse({
            'success': True,
            'count': len(jobs_list),
            'jobs': jobs_list
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
@token_required
def apply_to_job(request, job_id):
    """
    Endpoint para aplicar a una oferta de trabajo
    POST /api/jobs/<job_id>/apply

    Body esperado:
    {
        "applicantName": "Juan Pérez",
        "applicantEmail": "juan@example.com",
        "applicantPhone": "1234567890",
        "applicantWhatsapp": "591XXXXXXXXX",
        "screeningAnswers": {
            "0": "Respuesta 1",
            "1": "Respuesta 2"
        }
    }
    """
    try:
        job = Job.objects.get(id=job_id)

        # Parsear datos del request
        data = json.loads(request.body) if request.body else {}

        applicant_name = data.get('applicantName', '')
        applicant_email = data.get('applicantEmail', '')
        applicant_phone = data.get('applicantPhone', '')
        applicant_whatsapp = data.get('applicantWhatsapp', '')
        screening_answers = data.get('screeningAnswers', {})

        # Validaciones
        if not applicant_name:
            return JsonResponse({
                'success': False,
                'message': 'El nombre del candidato es requerido'
            }, status=400)

        if not applicant_email:
            return JsonResponse({
                'success': False,
                'message': 'El email del candidato es requerido'
            }, status=400)

        # Verificar si el candidato ya ha aplicado a este trabajo
        existing_application = Application.objects.filter(
            job=job,
            applicantEmail=applicant_email
        ).first()

        if existing_application:
            return JsonResponse({
                'success': False,
                'message': 'Ya has aplicado a esta oferta con este email'
            }, status=409)

        # Crear aplicación
        application = Application.objects.create(
            job=job,
            applicantName=applicant_name,
            applicantEmail=applicant_email,
            applicantPhone=applicant_phone,
            applicantWhatsapp=applicant_whatsapp,
            screeningAnswers=screening_answers,
            status='received'
        )

        # Incrementar contador de aplicaciones en el trabajo
        job.applications += 1
        job.save(update_fields=['applications'])

        return JsonResponse({
            'success': True,
            'message': '¡Aplicación registrada exitosamente!',
            'applicationId': application.id,
            'applicantAnswers': screening_answers,
            'createdAt': application.createdAt.isoformat()
        }, status=201)

    except Job.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Oferta no encontrada'
        }, status=404)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error al aplicar a trabajo: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@token_required
def list_applications(request, job_id):
    """
    Endpoint para listar todas las aplicaciones de una oferta de trabajo
    GET /api/jobs/<job_id>/applications

    Parámetros opcionales:
    - status: filtrar por estado (received, reviewing, shortlisted, rejected, accepted)
    - search: buscar por nombre o email del candidato
    """
    try:
        job = Job.objects.get(id=job_id)

        # Obtener aplicaciones del trabajo
        applications = Application.objects.filter(job=job)

        # Filtros opcionales
        status = request.GET.get('status')
        search = request.GET.get('search')

        if status:
            applications = applications.filter(status=status)

        if search:
            applications = applications.filter(
                models.Q(applicantName__icontains=search) |
                models.Q(applicantEmail__icontains=search)
            )

        # Construir lista de aplicaciones
        applications_list = []
        for app in applications.order_by('-createdAt'):
            applications_list.append({
                'id': app.id,
                'jobId': app.job.id,
                'applicantName': app.applicantName,
                'applicantEmail': app.applicantEmail,
                'applicantPhone': app.applicantPhone,
                'applicantWhatsapp': app.applicantWhatsapp,
                'screeningAnswers': app.screeningAnswers,
                'status': app.status,
                'recruiterNotes': app.recruiterNotes,
                'createdAt': app.createdAt.isoformat(),
                'updatedAt': app.updatedAt.isoformat()
            })

        return JsonResponse({
            'success': True,
            'jobId': job_id,
            'jobTitle': job.title,
            'count': len(applications_list),
            'applications': applications_list
        })

    except Job.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Oferta no encontrada'
        }, status=404)

    except Exception as e:
        print(f'Error al listar aplicaciones: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["PATCH"])
@csrf_exempt
@token_required
def update_application_status(request, job_id, application_id):
    """
    Endpoint para actualizar el estado de una aplicación
    PATCH /api/jobs/<job_id>/applications/<application_id>

    Body esperado:
    {
        "status": "reviewing",
        "recruiterNotes": "Excelente candidato, requiere entrevista"
    }
    """
    try:
        job = Job.objects.get(id=job_id)
        application = Application.objects.get(id=application_id, job=job)

        # Parsear datos del request
        data = json.loads(request.body) if request.body else {}

        # Actualizar estado si se proporciona
        if 'status' in data:
            application.status = data['status']

        # Actualizar notas si se proporcionan
        if 'recruiterNotes' in data:
            application.recruiterNotes = data['recruiterNotes']

        application.save()

        return JsonResponse({
            'success': True,
            'message': 'Aplicación actualizada exitosamente',
            'application': {
                'id': application.id,
                'status': application.status,
                'recruiterNotes': application.recruiterNotes,
                'updatedAt': application.updatedAt.isoformat()
            }
        })

    except Job.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Oferta no encontrada'
        }, status=404)

    except Application.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Aplicación no encontrada'
        }, status=404)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error al actualizar aplicación: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@token_required
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
        # Obtener trabajos del usuario
        user_jobs = Job.objects.filter(email=request.GET.get('email', ''))

        jobsPublished = user_jobs.count()
        jobsActive = user_jobs.filter(status='active').count()

        # Contar aplicaciones
        totalApplications = Application.objects.filter(
            job__in=user_jobs
        ).count()

        newApplications = Application.objects.filter(
            job__in=user_jobs,
            status='received'
        ).count()

        # Contar vistas
        totalViews = sum(job.views for job in user_jobs)

        # Profile completion (placeholder - TODO: integrar con UserProfile)
        profileComplete = False
        profilePercentage = 0

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


@require_http_methods(["GET"])
@token_required
def get_user_published_jobs(request):
    """
    Endpoint para obtener trabajos publicados por el usuario
    GET /api/user/published?email=user@example.com

    Retorna:
    - Lista de trabajos publicados con información resumida
    """
    try:
        email = request.GET.get('email', '')
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email requerido'
            }, status=400)

        jobs = Job.objects.filter(email=email).values(
            'id', 'title', 'companyName', 'status', 'views',
            'applications', 'createdAt', 'city', 'modality'
        ).order_by('-createdAt')

        return JsonResponse({
            'success': True,
            'jobs': list(jobs)
        }, status=200)

    except Exception as e:
        print(f'Error al obtener trabajos publicados: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@token_required
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

        # Obtener aplicaciones del usuario
        applications = Application.objects.filter(
            applicantEmail=email
        ).select_related('job').values(
            'id', 'job__id', 'job__title', 'job__companyName',
            'job__city', 'job__modality', 'status', 'createdAt', 'recruiterNotes'
        ).order_by('-createdAt')

        result = []
        for app in applications:
            result.append({
                'id': app['id'],
                'jobId': app['job__id'],
                'jobTitle': app['job__title'],
                'companyName': app['job__companyName'],
                'jobCity': app['job__city'],
                'jobModality': app['job__modality'].capitalize(),
                'status': app['status'],
                'appliedAt': app['createdAt'],
                'recruiterNotes': app['recruiterNotes']
            })

        return JsonResponse({
            'success': True,
            'applications': result
        }, status=200)

    except Exception as e:
        print(f'Error al obtener trabajos aplicados: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@token_required
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

        # Aplicaciones recibidas recientemente
        recent_apps = Application.objects.filter(
            job__email=email
        ).order_by('-createdAt')[:5]
        for app in recent_apps:
            activities.append({
                'id': activity_id,
                'type': 'application',
                'title': f'{app.applicantName} aplicó a "{app.job.title}"',
                'description': f'Nuevo candidato interesado',
                'date': app.createdAt.isoformat(),
                'metadata': {'jobId': str(app.job.id), 'applicantName': app.applicantName}
            })
            activity_id += 1

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
