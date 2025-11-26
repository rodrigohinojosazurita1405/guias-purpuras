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

    CAMPOS REQUERIDOS:
    - title (str, 5-200 chars): Título del puesto
    - description (str, min 20 chars): Descripción del trabajo
    - email (str): Email de contacto
    - city (str): Ciudad
    - contractType (str): Tipo de contrato
    - requirements (str): Requisitos
    - selectedPlan (str: 'escencial'|'purpura'|'impulso'): Plan elegido
    - proofOfPayment (file): Comprobante de pago (imagen, max 5MB)

    CAMPOS OPCIONALES:
    - companyName (str, default: 'Empresa Confidencial')
    - companyAnonymous (bool, default: False)
    - jobCategory (str)
    - municipality (str)
    - subcategory (str)
    - modality (str: 'presencial'|'remoto'|'hibrido', default: 'presencial')
    - responsibilities (str)
    - education (str)
    - experience (str)
    - languages (str)
    - technicalSkills (str)
    - softSkills (str)
    - salaryType (str: 'range'|'fixed'|'negotiable'|'hidden', default: 'range')
    - salaryMin (float)
    - salaryMax (float)
    - salaryFixed (float)
    - benefits (str)
    - vacancies (int, default: 1)
    - whatsapp (str)
    - website (str)
    - applicationInstructions (str)
    - applicationType (str: 'internal'|'external'|'both', default: 'internal')
    - externalApplicationUrl (str)
    - screeningQuestions (list)

    RESPUESTA EXITOSA (201):
    {
        'success': True,
        'message': 'string',
        'id': 'job_id',
        'createdAt': 'ISO timestamp'
    }

    RESPUESTA ERROR (400, 401, 500):
    {
        'success': False,
        'message': 'string',
        'errors': {field: error_message} (opcional)
    }
    """
    try:
        # Parsear datos de POST multipart/form-data
        # Intentar primero JSON, si falla usar POST data
        try:
            data = json.loads(request.body) if request.body and 'application/json' in request.META.get('CONTENT_TYPE', '') else {}
        except (json.JSONDecodeError, AttributeError):
            data = {}

        # Combinar datos JSON con POST data y FILES
        data.update(request.POST.dict())
        files = request.FILES.dict()

        print(f'[PUBLISH] [PUBLISH_JOB] Usuario: {request.user.email}, Campos recibidos: {list(data.keys())}, Archivos: {list(files.keys())}')

        # ========== VALIDACIONES DE CAMPOS REQUERIDOS ==========
        errors = {}

        # 1. Title
        title = (data.get('title') or '').strip()
        if not title:
            errors['title'] = 'El título del puesto es requerido'
        elif len(title) < 5:
            errors['title'] = 'El título debe tener al menos 5 caracteres'
        elif len(title) > 200:
            errors['title'] = 'El título no puede exceder 200 caracteres'

        # 2. Description
        description = (data.get('description') or '').strip()
        if not description:
            errors['description'] = 'La descripción es requerida'
        elif len(description) < 20:
            errors['description'] = 'La descripción debe tener al menos 20 caracteres'

        # 3. Email (Opcional - solo se valida si se proporciona)
        email = (data.get('email') or '').strip()
        if email and ('@' not in email or '.' not in email):
            errors['email'] = 'Email inválido (ej: user@example.com)'
        if not email:
            # Si no hay email, usar un placeholder
            email = 'contact@empresa.com'

        # 4. City
        city = (data.get('city') or '').strip()
        if not city:
            errors['city'] = 'La ciudad es requerida'

        # 5. Contract Type
        contract_type = (data.get('contractType') or '').strip()
        if not contract_type:
            errors['contractType'] = 'El tipo de contrato es requerido'

        # 6. Plan Selection (para calcular automáticamente la fecha de expiración)
        from plans.models import Plan
        from datetime import datetime, timedelta

        plan = (data.get('selectedPlan') or 'escencial').lower()

        # Obtener el plan desde la BD
        try:
            plan_obj = Plan.objects.get(name=plan, is_active=True)
            duration_days = plan_obj.duration_days
        except Plan.DoesNotExist:
            errors['selectedPlan'] = "Plan no válido o inactivo. Debe ser 'escencial', 'purpura' o 'impulso'"
            duration_days = 15  # Default fallback

        # Calcular expiryDate automáticamente basándose en el plan
        try:
            today = datetime.now().date()
            expiry_date = today + timedelta(days=duration_days)
            expiry_date = expiry_date.strftime('%Y-%m-%d')
        except Exception as e:
            errors['expiryDate'] = f'Error al calcular fecha de vencimiento: {str(e)}'

        # 7. Requirements
        requirements = (data.get('requirements') or '').strip()
        if not requirements:
            errors['requirements'] = 'Los requisitos son requeridos'

        # 8. Proof of Payment (FASE 7.1)
        proof_of_payment = files.get('proofOfPayment')
        if not proof_of_payment:
            errors['proofOfPayment'] = 'El comprobante de pago es requerido (imagen JPEG, PNG o GIF)'
        else:
            # Validar tipo de archivo
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
            file_ext = proof_of_payment.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                errors['proofOfPayment'] = f'Tipo de archivo no permitido. Use: {", ".join(allowed_extensions).upper()}'
            # Validar tamaño (max 5MB)
            elif proof_of_payment.size > 5 * 1024 * 1024:
                errors['proofOfPayment'] = 'El archivo es demasiado grande. Máximo 5 MB'

        # Retornar errores si existen
        if errors:
            print(f'[ERROR] [PUBLISH_JOB] Errores de validación: {errors}')
            return JsonResponse({
                'success': False,
                'message': 'Errores de validación',
                'errors': errors
            }, status=400)

        # ========== VALIDACIONES OPCIONALES ==========

        # Modality
        modality = (data.get('modality') or 'presencial').lower()
        if modality not in ['presencial', 'remoto', 'hibrido']:
            errors['modality'] = "Debe ser 'presencial', 'remoto' o 'hibrido'"

        # Salary Type
        salary_type = (data.get('salaryType') or 'range').lower()
        if salary_type not in ['range', 'fixed', 'negotiable', 'hidden']:
            errors['salaryType'] = "Debe ser 'range', 'fixed', 'negotiable' o 'hidden'"

        # Application Type
        app_type = (data.get('applicationType') or 'internal').lower()
        if app_type not in ['internal', 'external', 'both']:
            errors['applicationType'] = "Debe ser 'internal', 'external' o 'both'"

        # Salary validation (si es tipo range)
        if salary_type == 'range':
            try:
                salary_min = float(data.get('salaryMin', 0)) if data.get('salaryMin') else None
                salary_max = float(data.get('salaryMax', 0)) if data.get('salaryMax') else None
                if salary_min and salary_max and salary_min > salary_max:
                    errors['salaryRange'] = 'El salario mínimo no puede ser mayor al máximo'
            except (ValueError, TypeError):
                errors['salaryRange'] = 'Valores de salario inválidos (deben ser números)'

        if errors:
            print(f'[ERROR] [PUBLISH_JOB] Errores de validación opcional: {errors}')
            return JsonResponse({
                'success': False,
                'message': 'Errores de validación',
                'errors': errors
            }, status=400)

        # ========== CREAR JOB ==========
        try:
            job = Job.objects.create(
                title=title,
                companyName=(data.get('companyName') or 'Empresa Confidencial').strip(),
                companyAnonymous=bool(data.get('companyAnonymous', False)),
                description=description,
                jobCategory=(data.get('jobCategory') or '').strip(),
                city=city,
                municipality=(data.get('municipality') or '').strip(),
                subcategory=(data.get('subcategory') or '').strip(),
                contractType=contract_type,
                modality=modality,
                expiryDate=expiry_date,
                requirements=requirements,
                responsibilities=(data.get('responsibilities') or '').strip(),
                education=(data.get('education') or '').strip(),
                experience=(data.get('experience') or '').strip(),
                languages=(data.get('languages') or '').strip(),
                technicalSkills=(data.get('technicalSkills') or '').strip(),
                softSkills=(data.get('softSkills') or '').strip(),
                salaryType=salary_type,
                salaryMin=float(data.get('salaryMin')) if data.get('salaryMin') else None,
                salaryMax=float(data.get('salaryMax')) if data.get('salaryMax') else None,
                salaryFixed=float(data.get('salaryFixed')) if data.get('salaryFixed') else None,
                benefits=(data.get('benefits') or '').strip(),
                vacancies=int(data.get('vacancies', 1)),
                email=email,
                whatsapp=(data.get('whatsapp') or '').strip(),
                website=(data.get('website') or '').strip(),
                applicationInstructions=(data.get('applicationInstructions') or '').strip(),
                applicationType=app_type,
                externalApplicationUrl=(data.get('externalApplicationUrl') or '').strip(),
                selectedPlan=plan,
                screeningQuestions=data.get('screeningQuestions', []),
                proofOfPayment=proof_of_payment,  # FASE 7.1: Comprobante de pago obligatorio
            )

            print(f'[OK] [PUBLISH_JOB] Éxito: ID={job.id}, Título="{job.title}", Plan={plan}')
            return JsonResponse({
                'success': True,
                'message': '¡Oferta publicada exitosamente!',
                'id': job.id,
                'createdAt': job.createdAt.isoformat()
            }, status=201)
        except Exception as create_error:
            import traceback
            print(f'[ERROR] [PUBLISH_JOB] Error al crear Job: {str(create_error)}')
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'message': f'Error al crear anuncio: {str(create_error)}'
            }, status=500)

    except json.JSONDecodeError as je:
        print(f'[ERROR] [PUBLISH_JOB] JSON inválido: {str(je)}')
        return JsonResponse({
            'success': False,
            'message': 'Error: JSON inválido o vacío'
        }, status=400)

    except Exception as e:
        print(f'[ERROR] [PUBLISH_JOB] Error inesperado: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error interno: {str(e)}'
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
                'municipality': job.municipality,
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
                'softSkills': job.softSkills,

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


@token_required
@require_http_methods(["GET"])
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


@token_required
@csrf_exempt
@require_http_methods(["PATCH"])
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


@token_required
@require_http_methods(["GET"])
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


@token_required
@require_http_methods(["GET"])
def get_user_published_jobs(request):
    """
    Endpoint para obtener trabajos publicados por el usuario
    GET /api/user/published?email=user@example.com

    Retorna:
    - Lista de trabajos publicados con información resumida
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
        jobs = Job.objects.filter(email=email).order_by('-createdAt')

        # Convertir a lista con fechas como strings
        jobs_list = []
        for job in jobs:
            job_dict = {
                'id': str(job.id),
                'title': str(job.title),
                'companyName': str(job.companyName),
                'status': str(job.status),
                'views': int(job.views or 0),
                'applications': int(job.applications or 0),
                'createdAt': str(job.createdAt.isoformat()) if job.createdAt else None,
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


@token_required
@require_http_methods(["GET"])
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


@token_required
@csrf_exempt
@require_http_methods(["PATCH"])
def verify_payment(request, job_id):
    """
    Endpoint para verificar el pago de una oferta de trabajo (SOLO SUPERADMIN)
    PATCH /api/jobs/<job_id>/verify-payment

    CAMPOS REQUERIDOS:
    - approved (bool): Verdadero si el pago fue aprobado, falso si fue rechazado
    - notes (str): Notas de la verificación (razón de aprobación/rechazo)

    RESPUESTA EXITOSA (200):
    {
        'success': True,
        'message': 'string',
        'job': {
            'id': 'job_id',
            'paymentVerified': bool,
            'paymentVerificationDate': 'ISO timestamp',
            'status': 'active' o 'draft'
        }
    }

    RESPUESTA ERROR (400, 401, 403, 404, 500):
    {
        'success': False,
        'message': 'string'
    }
    """
    try:
        # Verificar que el usuario es superadmin
        if not request.user.is_superuser:
            print(f'[ERROR] [VERIFY_PAYMENT] Acceso denegado: {request.user.email} no es superadmin')
            return JsonResponse({
                'success': False,
                'message': 'Solo superadmin puede verificar pagos'
            }, status=403)

        # Obtener la oferta de trabajo
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            print(f'[ERROR] [VERIFY_PAYMENT] Oferta no encontrada: {job_id}')
            return JsonResponse({
                'success': False,
                'message': 'Oferta de trabajo no encontrada'
            }, status=404)

        # Parsear datos del request
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Error: JSON inválido'
            }, status=400)

        # Validar campos requeridos
        approved = data.get('approved')
        notes = (data.get('notes') or '').strip()

        if approved is None:
            return JsonResponse({
                'success': False,
                'message': 'Campo "approved" requerido (true/false)'
            }, status=400)

        if not notes:
            return JsonResponse({
                'success': False,
                'message': 'Notas de verificación requeridas'
            }, status=400)

        # Actualizar estado de verificación
        from django.utils import timezone
        job.paymentVerified = approved
        job.paymentVerifiedBy = request.user
        job.paymentVerificationDate = timezone.now()
        job.paymentVerificationNotes = notes

        # Si el pago fue aprobado, cambiar estado a 'active', si no a 'draft'
        job.status = 'active' if approved else 'draft'

        job.save()

        status_text = "Aprobado" if approved else "Rechazado"
        print(f'[OK] [VERIFY_PAYMENT] ID={job_id}, Título="{job.title}", Estado={status_text}, Verificador={request.user.email}')

        return JsonResponse({
            'success': True,
            'message': f'Pago {status_text.lower()} exitosamente',
            'job': {
                'id': job.id,
                'title': job.title,
                'paymentVerified': job.paymentVerified,
                'paymentVerificationDate': job.paymentVerificationDate.isoformat(),
                'status': job.status
            }
        }, status=200)

    except Exception as e:
        print(f'[ERROR] [VERIFY_PAYMENT] Error inesperado: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@csrf_exempt
def get_job_categories(request):
    """
    Endpoint para obtener la lista de categorías de trabajo disponibles
    GET /api/jobs/categories

    Returns:
    {
        'success': bool,
        'categories': [
            { 'text': 'Administración y Gestión', 'value': 'Administración y Gestión' },
            ...
        ],
        'count': int
    }
    """
    try:
        from .constants import JOB_CATEGORIES

        # Convertir a formato de opciones
        categories = [
            {'text': category, 'value': category}
            for category in JOB_CATEGORIES
        ]

        return JsonResponse({
            'success': True,
            'categories': categories,
            'count': len(categories)
        }, status=200)

    except Exception as e:
        print(f'Error al obtener categorías: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
