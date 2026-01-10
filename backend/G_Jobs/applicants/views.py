from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from .models import ApplicantProfile, ApplicantCV, JobApplication, SavedJob
from G_Jobs.jobs.models import Job
from G_Jobs.moderation.models import BlockedUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from xhtml2pdf import pisa
import json
import uuid
import io

User = get_user_model()


# Helper para verificar autenticación
def require_authentication(view_func):
    """Decorator para verificar que el usuario esté autenticado (Django session o JWT token)"""
    def wrapper(request, *args, **kwargs):
        # Opción 1: Sesión Django (request.user ya poblado por middleware)
        if request.user.is_authenticated:
            print(f"[AUTH] Usuario autenticado via sesion Django: {request.user.email}")
            return view_func(request, *args, **kwargs)

        # Opción 2: JWT Token en Authorization header
        auth_header = request.headers.get('Authorization', '')
        if auth_header:
            print(f"[AUTH] Header Authorization recibido: {auth_header[:50]}...")
        else:
            print("[AUTH] No se recibio Authorization header")

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
                print(f"[AUTH] Usuario autenticado via JWT: {user.email}")
                return view_func(request, *args, **kwargs)
            except (InvalidToken, TokenError) as e:
                print(f"[AUTH] Token invalido: {str(e)}")
            except User.DoesNotExist:
                print(f"[AUTH] Usuario no encontrado: user_id={user_id}")

        print("[AUTH] Autenticacion fallida")
        return JsonResponse({
            'success': False,
            'error': 'Autenticación requerida'
        }, status=401)
    return wrapper


# ========== CRUD ENDPOINTS PARA CVs ==========

@csrf_exempt
@require_authentication
@require_http_methods(["POST"])
def save_cv(request):
    """
    Guardar un CV (creado o subido)

    Request Body (Created CV):
    {
        "cv_type": "created",
        "name": "CV para Desarrollo Web",
        "cv_data": {...}
    }

    Request Body (Uploaded CV):
    {
        "cv_type": "uploaded",
        "name": "CV General",
        "file": <file>
    }
    """
    try:
        print(f"\n========== SAVE CV ==========")
        print(f"User: {request.user.email}")
        print(f"Content-Type: {request.content_type}")
        print(f"Files: {request.FILES.keys() if request.FILES else 'None'}")
        print(f"============================\n")

        # Nota: La validación de límites se maneja en el modelo (clean method)
        # - Máximo 2 CVs creados (MAX_CREATED_CVS)
        # - Máximo 1 PDF subido (MAX_UPLOADED_CVS)

        # Determinar tipo de CV
        if request.content_type == 'application/json':
            # CV creado en plataforma
            data = json.loads(request.body)

            cv = ApplicantCV.objects.create(
                applicant=request.user,
                cv_type='created',
                name=data.get('name', 'Mi CV'),
                cv_data=data.get('cv_data', {})
            )

        else:
            # CV subido como archivo
            if 'file' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'error': 'No se proporcionó ningún archivo'
                }, status=400)

            file = request.FILES['file']
            name = request.POST.get('name', f'CV {file.name}')

            # IMPORTANTE: Validar límites ANTES de guardar el archivo
            existing_uploaded = ApplicantCV.objects.filter(
                applicant=request.user,
                cv_type='uploaded',
                is_deleted=False
            ).count()

            if existing_uploaded >= ApplicantCV.MAX_UPLOADED_CVS:
                return JsonResponse({
                    'success': False,
                    'error': f'Ya tienes un PDF guardado. Elimina el PDF existente antes de subir uno nuevo.'
                }, status=400)

            # Ahora sí crear el CV (el archivo se guardará al crear el objeto)
            cv = ApplicantCV.objects.create(
                applicant=request.user,
                cv_type='uploaded',
                name=name,
                file=file
            )

        print(f"CV CREADO EXITOSAMENTE:")
        print(f"  ID: {cv.id}")
        print(f"  Nombre: {cv.name}")
        print(f"  Tipo: {cv.cv_type}")
        print(f"=============================\n")

        return JsonResponse({
            'success': True,
            'message': 'CV guardado exitosamente',
            'cv': {
                'id': str(cv.id),
                'name': cv.name,
                'cv_type': cv.cv_type,
                'created_at': cv.created_at.isoformat()
            }
        }, status=201)

    except ValidationError as e:
        error_msg = str(e) if isinstance(e, str) else str(e.message_dict if hasattr(e, 'message_dict') else e)
        print(f"❌ ValidationError en save_cv: {error_msg}")
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=400)
    except Exception as e:
        print(f"❌ Exception en save_cv: {str(e)}")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Request user: {request.user}")
        print(f"   Content-Type: {request.content_type}")
        print(f"   FILES keys: {list(request.FILES.keys())}")
        print(f"   POST keys: {list(request.POST.keys())}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Error al guardar CV: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def list_cvs(request):
    """
    Listar TODOS los CVs guardados del usuario (creados + PDFs subidos)

    Response:
    {
        "cvs": [
            {
                "id": "uuid",
                "name": "CV para Desarrollo Web",
                "cv_type": "created",
                "created_at": "2025-01-15T10:00:00Z",
                "updated_at": "2025-01-15T10:00:00Z"
            },
            {
                "id": "uuid",
                "name": "Mi CV.pdf",
                "cv_type": "uploaded",
                "file_url": "/media/applicant_cvs_uploaded/Mi_CV.pdf",
                "created_at": "2025-01-15T10:00:00Z",
                "updated_at": "2025-01-15T10:00:00Z"
            }
        ],
        "count": 2,
        "max_created_cvs": 2,
        "max_uploaded_cvs": 1
    }
    """
    try:
        # TODOS los CVs guardados (creados + PDFs subidos)
        cvs = ApplicantCV.objects.filter(
            applicant=request.user,
            is_deleted=False
        ).order_by('-created_at')

        cvs_data = []
        for cv in cvs:
            cv_info = {
                'id': str(cv.id),
                'name': cv.name,
                'cv_type': cv.cv_type,
                'created_at': cv.created_at.isoformat(),
                'updated_at': cv.updated_at.isoformat()
            }

            # Incluir cv_data para CVs creados (necesario para vista previa)
            if cv.cv_type == 'created' and cv.cv_data:
                cv_info['cv_data'] = cv.cv_data

            # Incluir file_url para CVs subidos y creados (PDF generado)
            if cv.file:
                cv_info['file'] = cv.file.url

            cvs_data.append(cv_info)

        return JsonResponse({
            'success': True,
            'cvs': cvs_data,
            'count': len(cvs_data),
            'max_created_cvs': ApplicantCV.MAX_CREATED_CVS,
            'max_uploaded_cvs': ApplicantCV.MAX_UPLOADED_CVS
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al listar CVs: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def get_cv_detail(request, cv_id):
    """
    Obtener detalle completo de un CV

    Response:
    {
        "cv": {
            "id": "uuid",
            "name": "CV para Desarrollo Web",
            "cv_type": "created",
            "cv_data": {...},
            "created_at": "2025-01-15T10:00:00Z"
        }
    }
    """
    try:
        cv = get_object_or_404(
            ApplicantCV,
            id=cv_id,
            applicant=request.user,
            is_deleted=False
        )

        cv_data = {
            'id': str(cv.id),
            'name': cv.name,
            'cv_type': cv.cv_type,
            'created_at': cv.created_at.isoformat(),
            'updated_at': cv.updated_at.isoformat()
        }

        if cv.cv_type == 'created':
            cv_data['cv_data'] = cv.cv_data
        elif cv.cv_type == 'uploaded':
            cv_data['file_url'] = cv.file.url if cv.file else None

        return JsonResponse({
            'success': True,
            'cv': cv_data
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener CV: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["PATCH", "PUT"])
def update_cv(request, cv_id):
    """
    Actualizar un CV existente

    Request Body:
    {
        "name": "Nuevo nombre",
        "cv_data": {...}  // Solo para CVs creados
    }
    """
    try:
        cv = get_object_or_404(
            ApplicantCV,
            id=cv_id,
            applicant=request.user,
            is_deleted=False
        )

        data = json.loads(request.body)

        # Actualizar nombre si se proporciona
        if 'name' in data:
            cv.name = data['name']

        # Actualizar datos del CV si es de tipo 'created'
        if cv.cv_type == 'created' and 'cv_data' in data:
            cv.cv_data = data['cv_data']

        cv.save()

        return JsonResponse({
            'success': True,
            'message': 'CV actualizado exitosamente',
            'cv': {
                'id': str(cv.id),
                'name': cv.name,
                'updated_at': cv.updated_at.isoformat()
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al actualizar CV: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["DELETE"])
def delete_cv(request, cv_id):
    """
    Eliminar un CV (soft delete + eliminar archivo físico si existe)
    """
    try:
        cv = get_object_or_404(
            ApplicantCV,
            id=cv_id,
            applicant=request.user,
            is_deleted=False
        )

        # Eliminar archivo físico si existe (para PDFs subidos)
        if cv.file and hasattr(cv.file, 'path'):
            try:
                import os
                if os.path.exists(cv.file.path):
                    os.remove(cv.file.path)
                    print(f"Archivo fisico eliminado: {cv.file.path}")
            except Exception as file_error:
                print(f"Error al eliminar archivo fisico: {file_error}")
                # Continuar con soft delete aunque falle eliminación de archivo

        # Soft delete en base de datos
        cv.is_deleted = True
        cv.deleted_at = timezone.now()
        cv.save()

        return JsonResponse({
            'success': True,
            'message': 'CV eliminado exitosamente'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al eliminar CV: {str(e)}'
        }, status=500)


# ========== ENDPOINTS PARA POSTULACIONES ==========

@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def check_if_blocked(request, job_id):
    """
    Verificar si el usuario actual está bloqueado por la empresa del trabajo

    GET /api/jobs/<job_id>/check-blocked/

    Returns:
    {
        "blocked": bool,
        "message": str (si está bloqueado)
    }
    """
    try:
        # Verificar que el trabajo existe
        job = get_object_or_404(Job, id=job_id)

        # Obtener el usuario de la empresa que publicó el trabajo
        from auth_api.models import CustomUser
        try:
            company_user = CustomUser.objects.get(email=job.email, role='company')
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'blocked': False
            }, status=200)

        # Verificar si el usuario está bloqueado
        block = BlockedUser.objects.filter(
            company=company_user,
            blocked_user=request.user
        ).first()

        if block:
            return JsonResponse({
                'blocked': True,
                'message': 'No puedes postularte a empleos de esta empresa en este momento.'
            }, status=200)

        return JsonResponse({
            'blocked': False
        }, status=200)

    except Exception as e:
        print(f'[ERROR] check_if_blocked: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["POST"])
def apply_to_job(request, job_id):
    """
    Postularse a un trabajo

    IMPORTANTE: Solo acepta CVs guardados (referencias).
    Si el usuario sube un PDF, debe guardarlo primero en /api/cvs/save/

    Request Body (JSON):
    {
        "cv_id": "uuid",
        "cover_letter": "string",
        "screening_answers": {...}
    }
    """
    try:
        # Solo acepta JSON con cv_id
        data = json.loads(request.body)
        screening_answers = data.get('screening_answers', {})

        # Verificar que el trabajo existe y está activo
        job = get_object_or_404(Job, id=job_id, status='active')

        # Obtener el usuario de la empresa que publicó el trabajo
        from auth_api.models import CustomUser
        try:
            company_user = CustomUser.objects.get(email=job.email, role='company')
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'No se pudo verificar la empresa publicadora.'
            }, status=400)

        # Verificar si el usuario está bloqueado por esta empresa
        block = BlockedUser.objects.filter(
            company=company_user,
            blocked_user=request.user
        ).first()

        if block:
            # Registrar intento de aplicación bloqueado
            from G_Jobs.audit.models import AuditLog
            AuditLog.log_action(
                user=company_user,
                obj=job,
                action='block_attempt',
                changes={
                    'blocked_user_email': request.user.email,
                    'blocked_user_id': str(request.user.id),
                    'job_id': str(job.id),
                    'job_title': job.title,
                    'block_reason': block.get_reason_display(),
                    'block_notes': block.notes or ''
                },
                description=f"Usuario bloqueado {request.user.email} intentó postularse a '{job.title}'",
                severity='warning',
                request=request
            )

            return JsonResponse({
                'success': False,
                'error': 'No puedes postularte a empleos de esta empresa en este momento. Si crees que esto es un error, contacta al empleador.',
                'blocked': True
            }, status=403)

        # Obtener CV guardado (requerido)
        cv_id = data.get('cv_id')
        if not cv_id:
            return JsonResponse({
                'success': False,
                'error': 'Debes seleccionar un CV guardado para postularte'
            }, status=400)

        cv = get_object_or_404(
            ApplicantCV,
            id=cv_id,
            applicant=request.user,
            is_deleted=False
        )

        # Crear la postulación (solo con referencia de CV)
        application = JobApplication.objects.create(
            job=job,
            applicant=request.user,
            cv=cv,
            attached_cv_file=None,  # Ya no se usa, siempre None
            cover_letter=data.get('cover_letter', ''),
            screening_answers=screening_answers
        )

        # Incrementar contador de aplicaciones en el trabajo
        job.applications += 1
        job.save()

        # Actualizar perfil de postulante
        profile, created = ApplicantProfile.objects.get_or_create(user=request.user)
        profile.total_applications += 1
        profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Postulación enviada exitosamente',
            'application': {
                'id': str(application.id),
                'job_title': job.title,
                'applied_at': application.applied_at.isoformat(),
                'status': application.status
            }
        }, status=201)

    except IntegrityError:
        return JsonResponse({
            'success': False,
            'error': 'Ya te has postulado a este trabajo'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al postularse: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def get_user_applications(request):
    """
    Obtener todas las postulaciones del usuario

    Query Params:
    - status: filtrar por estado
    - limit: número de resultados
    - offset: paginación
    """
    try:
        applications = JobApplication.objects.filter(
            applicant=request.user
        ).select_related('job', 'cv')

        # Filtrar por estado si se proporciona
        status = request.GET.get('status')
        if status:
            applications = applications.filter(status=status)

        # Paginación
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        total = applications.count()

        applications = applications[offset:offset + limit]

        applications_data = []
        for app in applications:
            applications_data.append({
                'id': str(app.id),
                'job_id': app.job.id,  # Solo el ID del trabajo
                'cv_name': app.cv.name if app.cv else None,
                'status': app.status,
                'applied_at': app.applied_at.isoformat(),
                'updated_at': app.updated_at.isoformat(),
                'viewed_by_employer': app.viewed_by_employer
            })

        return JsonResponse({
            'success': True,
            'applications': applications_data,
            'total': total,
            'limit': limit,
            'offset': offset
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener postulaciones: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def get_application_detail(request, application_id):
    """
    Obtener detalle de una postulación específica
    """
    try:
        application = get_object_or_404(
            JobApplication,
            id=application_id,
            applicant=request.user
        )

        return JsonResponse({
            'success': True,
            'application': {
                'id': str(application.id),
                'job': {
                    'id': application.job.id,
                    'title': application.job.title,
                    'company': application.job.companyName,
                    'description': application.job.description,
                    'city': application.job.city
                },
                'cv': {
                    'id': str(application.cv.id) if application.cv else None,
                    'name': application.cv.name if application.cv else None
                },
                'cover_letter': application.cover_letter,
                'status': application.status,
                'screening_answers': application.screening_answers,
                'employer_notes': application.employer_notes,
                'applied_at': application.applied_at.isoformat(),
                'updated_at': application.updated_at.isoformat(),
                'viewed_by_employer': application.viewed_by_employer
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener detalle de postulación: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["DELETE"])
def withdraw_application(request, application_id):
    """
    Retirar una postulación
    """
    try:
        application = get_object_or_404(
            JobApplication,
            id=application_id,
            applicant=request.user
        )

        # Solo se puede retirar si está en estado inicial
        if application.status not in ['submitted', 'reviewing']:
            return JsonResponse({
                'success': False,
                'error': 'No puedes retirar esta postulación en su estado actual'
            }, status=400)

        application.status = 'withdrawn'
        application.save()

        return JsonResponse({
            'success': True,
            'message': 'Postulación retirada exitosamente'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al retirar postulación: {str(e)}'
        }, status=500)


# ========== ENDPOINTS PARA TRABAJOS GUARDADOS ==========

@csrf_exempt
@require_authentication
@require_http_methods(["POST"])
def save_job(request):
    """
    Guardar un trabajo para ver más tarde

    Request Body:
    {
        "job_id": "string"
    }
    """
    try:
        data = json.loads(request.body)
        job_id = data.get('job_id')

        if not job_id:
            return JsonResponse({
                'success': False,
                'error': 'Se requiere job_id'
            }, status=400)

        job = get_object_or_404(Job, id=job_id)

        saved_job, created = SavedJob.objects.get_or_create(
            user=request.user,
            job=job
        )

        if created:
            message = 'Trabajo guardado exitosamente'
        else:
            message = 'Este trabajo ya estaba guardado'

        return JsonResponse({
            'success': True,
            'message': message,
            'saved_job': {
                'id': str(saved_job.id),
                'job_title': job.title,
                'saved_at': saved_job.saved_at.isoformat()
            }
        }, status=201 if created else 200)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al guardar trabajo: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["DELETE"])
def unsave_job(request):
    """
    Quitar un trabajo de los guardados

    Request Body:
    {
        "job_id": "string"
    }
    """
    try:
        data = json.loads(request.body)
        job_id = data.get('job_id')

        if not job_id:
            return JsonResponse({
                'success': False,
                'error': 'Se requiere job_id'
            }, status=400)

        saved_job = get_object_or_404(
            SavedJob,
            user=request.user,
            job__id=job_id
        )

        saved_job.delete()

        return JsonResponse({
            'success': True,
            'message': 'Trabajo eliminado de guardados'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al eliminar trabajo guardado: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def get_saved_jobs(request):
    """
    Obtener todos los trabajos guardados por el usuario
    """
    try:
        saved_jobs = SavedJob.objects.filter(
            user=request.user
        ).select_related('job').order_by('-saved_at')

        # Paginación
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        total = saved_jobs.count()

        saved_jobs = saved_jobs[offset:offset + limit]

        jobs_data = []
        for saved in saved_jobs:
            job = saved.job

            # Obtener logo del perfil de empresa si existe
            company_logo = None
            company_profile = None

            if job.companyProfile:
                # Logo
                if job.companyProfile.logo:
                    logo_url = job.companyProfile.logo.url
                    if logo_url and not logo_url.startswith('http'):
                        company_logo = request.build_absolute_uri(logo_url)
                    else:
                        company_logo = logo_url

                # Banner
                company_banner = None
                if job.companyProfile.banner:
                    banner_url = job.companyProfile.banner.url
                    if banner_url and not banner_url.startswith('http'):
                        company_banner = request.build_absolute_uri(banner_url)
                    else:
                        company_banner = banner_url

                # Perfil completo de la empresa
                company_profile = {
                    'id': job.companyProfile.id,
                    'companyName': job.companyProfile.companyName,
                    'description': job.companyProfile.description if job.companyProfile.description else None,
                    'website': job.companyProfile.website if job.companyProfile.website else None,
                    'phone': job.companyProfile.phone if job.companyProfile.phone else None,
                    'email': job.companyProfile.email if job.companyProfile.email else None,
                    'contactEmail': job.companyProfile.contactEmail if job.companyProfile.contactEmail else None,
                    'location': job.companyProfile.location if job.companyProfile.location else None,
                    'city': job.companyProfile.city if job.companyProfile.city else None,
                    'category': job.companyProfile.get_category_display() if job.companyProfile.category else None,
                    'verified': job.companyProfile.verified,
                    'logo': company_logo,
                    'banner': company_banner,
                    'createdAt': job.companyProfile.createdAt.isoformat() if job.companyProfile.createdAt else None,
                }

            # Función para formatear salario
            def format_salary(job):
                if job.salaryType == 'range' and job.salaryMin and job.salaryMax:
                    return f'Bs. {int(job.salaryMin)} - {int(job.salaryMax)}'
                elif job.salaryType == 'fixed' and job.salaryFixed:
                    return f'Bs. {int(job.salaryFixed)}'
                elif job.salaryType == 'negotiable':
                    return 'A convenir'
                elif job.salaryType == 'pretension_salarial':
                    return 'Indique su pretensión salarial'
                else:
                    return 'No Declarado'

            # Función para calcular días desde publicación
            def calculate_days_ago(date_obj):
                from django.utils import timezone
                now_local = timezone.localtime()
                date_local = timezone.localtime(date_obj)
                now_date = now_local.date()
                created_date = date_local.date()
                days = (now_date - created_date).days
                return days

            jobs_data.append({
                'saved_id': str(saved.id),
                'saved_at': saved.saved_at.isoformat(),
                'job': {
                    'id': job.id,
                    'title': job.title,
                    'companyName': job.companyName if not job.companyAnonymous else 'Empresa Confidencial',
                    'companyAnonymous': job.companyAnonymous,
                    'companyLogo': company_logo,
                    'companyProfile': company_profile,
                    'city': job.city,
                    'municipality': job.municipality if job.municipality else None,
                    'contractType': job.contractType,
                    'modality': job.modality.capitalize() if job.modality else 'Presencial',
                    'jobCategory': job.jobCategory,
                    'subcategory': job.subcategory if job.subcategory else None,
                    'salary': format_salary(job),
                    'salaryMin': float(job.salaryMin) if job.salaryMin else None,
                    'salaryMax': float(job.salaryMax) if job.salaryMax else None,
                    'salaryFixed': float(job.salaryFixed) if job.salaryFixed else None,
                    'salaryType': job.salaryType,
                    'description': job.description,
                    'expiryDate': job.expiryDate.isoformat() if job.expiryDate else None,
                    'applicationDeadline': job.applicationDeadline.isoformat() if job.applicationDeadline else None,
                    'selectedPlan': job.selectedPlan,
                    'planType': job.selectedPlan,  # Alias para compatibilidad
                    'urgent': job.urgent if hasattr(job, 'urgent') else False,
                    'paymentVerified': job.paymentVerified,
                    'status': job.status,
                    'publishedDaysAgo': calculate_days_ago(job.createdAt),
                    'views': job.views,
                    'applications': job.applications,
                    'createdAt': job.createdAt.isoformat() if job.createdAt else None,
                    'updatedAt': job.updatedAt.isoformat() if job.updatedAt else None,
                }
            })

        return JsonResponse({
            'success': True,
            'saved_jobs': jobs_data,
            'total': total,
            'limit': limit,
            'offset': offset
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener trabajos guardados: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def check_job_saved(request, job_id):
    """
    Verificar si un trabajo está guardado
    """
    try:
        is_saved = SavedJob.objects.filter(
            user=request.user,
            job__id=job_id
        ).exists()

        return JsonResponse({
            'success': True,
            'is_saved': is_saved
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al verificar trabajo guardado: {str(e)}'
        }, status=500)


# ========== ENDPOINTS PARA PERFIL DE POSTULANTE ==========

@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def get_applicant_profile(request):
    """
    Obtener perfil del postulante
    """
    try:
        profile, created = ApplicantProfile.objects.get_or_create(user=request.user)

        return JsonResponse({
            'success': True,
            'profile': {
                'ci': profile.ci,
                'nationality': profile.nationality,
                'hasDriverLicense': profile.has_driver_license,
                'driverLicenseCategory': profile.driver_license_category,
                'hasCriminalRecord': profile.has_criminal_record,
                'phone': profile.phone,
                'whatsapp': profile.whatsapp,
                'linkedin_url': profile.linkedin_url,
                'portfolio_url': profile.portfolio_url,
                'desired_job_categories': profile.desired_job_categories,
                'desired_cities': profile.desired_cities,
                'desired_modality': profile.desired_modality,
                'total_applications': profile.total_applications
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener perfil: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["PATCH", "PUT"])
def update_applicant_profile(request):
    """
    Actualizar perfil del postulante

    Request Body:
    {
        "ci": "string",
        "nationality": "string",
        "hasDriverLicense": bool,
        "driverLicenseCategory": "string",
        "hasCriminalRecord": bool,
        "phone": "string",
        "whatsapp": "string",
        "linkedin_url": "string",
        "portfolio_url": "string",
        "desired_job_categories": [],
        "desired_cities": [],
        "desired_modality": "string"
    }
    """
    try:
        profile, created = ApplicantProfile.objects.get_or_create(user=request.user)
        data = json.loads(request.body)

        # Actualizar nuevos campos personales
        if 'ci' in data:
            profile.ci = data['ci']
        if 'nationality' in data:
            profile.nationality = data['nationality']
        if 'hasDriverLicense' in data:
            profile.has_driver_license = data['hasDriverLicense']
        if 'driverLicenseCategory' in data:
            profile.driver_license_category = data['driverLicenseCategory']
        if 'hasCriminalRecord' in data:
            profile.has_criminal_record = data['hasCriminalRecord']

        # Actualizar campos de contacto
        if 'phone' in data:
            profile.phone = data['phone']
        if 'whatsapp' in data:
            profile.whatsapp = data['whatsapp']
        if 'linkedin_url' in data:
            profile.linkedin_url = data['linkedin_url']
        if 'portfolio_url' in data:
            profile.portfolio_url = data['portfolio_url']

        # Actualizar preferencias
        if 'desired_job_categories' in data:
            profile.desired_job_categories = data['desired_job_categories']
        if 'desired_cities' in data:
            profile.desired_cities = data['desired_cities']
        if 'desired_modality' in data:
            profile.desired_modality = data['desired_modality']

        profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Perfil actualizado exitosamente'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al actualizar perfil: {str(e)}'
        }, status=500)


# ========== ENDPOINTS PARA RECLUTADORES ==========

@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def get_job_applications(request, job_id):
    """
    Obtener todas las postulaciones de un trabajo específico
    Solo el dueño del trabajo puede ver sus postulaciones

    URL: /api/jobs/<job_id>/applications
    """
    try:
        # Verificar que el trabajo existe
        job = get_object_or_404(Job, id=job_id)

        # Verificar que el usuario es el dueño del trabajo
        if job.email != request.user.email:
            return JsonResponse({
                'success': False,
                'error': 'No tienes permiso para ver estas postulaciones'
            }, status=403)

        # Obtener todas las postulaciones del trabajo
        applications = JobApplication.objects.filter(
            job=job
        ).select_related('applicant', 'cv').order_by('-applied_at')

        # Serializar las postulaciones
        applications_data = []
        for app in applications:
            # Obtener información del CV
            cv_info = None
            if app.cv:
                # CV guardado reutilizable
                cv_info = {
                    'id': str(app.cv.id),
                    'name': app.cv.name,
                    'type': app.cv.cv_type,
                    'file_url': app.cv.file.url if app.cv.file else None,
                    'file_name': app.cv.name,
                    'full_name': app.cv.cv_data.get('personalInfo', {}).get('fullName') if app.cv.cv_data else None,
                    'cv_data': app.cv.cv_data if app.cv.cv_type == 'created' else None
                }
            elif app.attached_cv_file:
                # CV adjunto directamente a esta postulación
                import os
                cv_info = {
                    'id': None,  # No tiene ID porque no está en ApplicantCV
                    'name': os.path.basename(app.attached_cv_file.name),
                    'type': 'uploaded',
                    'file_url': app.attached_cv_file.url,
                    'file_name': os.path.basename(app.attached_cv_file.name),
                    'full_name': None,
                    'cv_data': None
                }

            # Obtener teléfono del perfil si existe
            applicant_phone = None
            try:
                if hasattr(app.applicant, 'applicant_profile'):
                    applicant_phone = app.applicant.applicant_profile.phone
            except Exception:
                pass

            applications_data.append({
                'id': str(app.id),
                'applicantId': str(app.applicant.id),  # ID del usuario que aplicó
                'applicantName': app.applicant.get_full_name() or app.applicant.email,
                'applicantEmail': app.applicant.email,
                'applicantPhone': applicant_phone,
                'applicantWhatsapp': applicant_phone,
                'cv': cv_info,
                'coverLetter': app.cover_letter,
                'status': app.status,
                'recruiterNotes': app.employer_notes,
                'rating': app.rating,
                'createdAt': app.applied_at.isoformat(),
                'viewedByEmployer': app.viewed_by_employer
            })

        return JsonResponse({
            'success': True,
            'applications': applications_data,
            'total': len(applications_data)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener postulaciones: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["PATCH"])
def update_application_status(request, job_id, application_id):
    """
    Actualizar el estado de una postulación

    URL: /api/jobs/<job_id>/applications/<application_id>
    Request Body: { "status": "reviewing|shortlisted|accepted|rejected", "recruiterNotes": "..." }
    """
    try:
        # Verificar que el trabajo existe y es del usuario
        job = get_object_or_404(Job, id=job_id, email=request.user.email)

        # Verificar que la postulación existe y pertenece a este trabajo
        application = get_object_or_404(
            JobApplication,
            id=application_id,
            job=job
        )

        data = json.loads(request.body)

        # Actualizar estado si se proporciona
        old_status = application.status
        if 'status' in data:
            new_status = data['status']
            valid_statuses = ['submitted', 'reviewing', 'shortlisted', 'interviewed', 'accepted', 'rejected', 'withdrawn']
            if new_status not in valid_statuses:
                return JsonResponse({
                    'success': False,
                    'error': f'Estado inválido. Debe ser uno de: {", ".join(valid_statuses)}'
                }, status=400)
            application.status = new_status

        # Actualizar notas si se proporcionan
        if 'recruiterNotes' in data:
            application.employer_notes = data['recruiterNotes']

        # Actualizar rating si se proporciona
        if 'rating' in data:
            rating = data['rating']
            # Validar que el rating esté entre 1 y 5, o sea None para quitar rating
            if rating is not None and (not isinstance(rating, int) or rating < 1 or rating > 5):
                return JsonResponse({
                    'success': False,
                    'error': 'El rating debe ser un número entre 1 y 5, o null para quitar la calificación'
                }, status=400)
            application.rating = rating

        # Marcar como visto por el empleador
        if not application.viewed_by_employer:
            application.viewed_by_employer = True

        application.save()

        # Crear notificación para el postulante si el estado cambió
        if 'status' in data and old_status != application.status:
            try:
                from G_Jobs.notifications.models import Notification

                # Mapeo de estados a notificaciones
                status_notifications = {
                    'reviewing': {
                        'type': 'application_reviewing',
                        'title': 'Tu postulación está en revisión',
                        'message': f'El reclutador está revisando tu postulación para el puesto de {job.title}.'
                    },
                    'shortlisted': {
                        'type': 'application_shortlisted',
                        'title': '¡Felicidades! Has sido pre-seleccionado',
                        'message': f'Tu postulación para {job.title} ha sido pre-seleccionada. El reclutador podría contactarte pronto.'
                    },
                    'interviewed': {
                        'type': 'application_interviewed',
                        'title': '¡Invitación a entrevista!',
                        'message': f'Has sido invitado a una entrevista para el puesto de {job.title}. El reclutador se pondrá en contacto contigo.'
                    },
                    'accepted': {
                        'type': 'application_accepted',
                        'title': '¡Felicidades! Tu postulación fue aceptada',
                        'message': f'Tu postulación para {job.title} ha sido aceptada. El reclutador se comunicará contigo con los siguientes pasos.'
                    },
                    'rejected': {
                        'type': 'application_rejected',
                        'title': 'Actualización de tu postulación',
                        'message': f'Lamentablemente, tu postulación para {job.title} no fue seleccionada en esta ocasión. Te animamos a seguir postulando a otras ofertas.'
                    }
                }

                # Crear la notificación si el estado está en el mapeo
                if application.status in status_notifications:
                    notif_data = status_notifications[application.status]
                    print(f"[NOTIFICATION] Creando notificación para {application.applicant.email}: {notif_data['type']}")
                    Notification.create_notification(
                        user=application.applicant,
                        notification_type=notif_data['type'],
                        title=notif_data['title'],
                        message=notif_data['message'],
                        metadata={
                            'job_id': str(job.id),
                            'application_id': str(application.id),
                            'job_title': job.title,
                            'company_name': job.companyName
                        }
                    )
                    print(f"[NOTIFICATION] Notificación creada exitosamente")
            except Exception as notif_error:
                # Log el error pero no fallar la actualización del estado
                print(f"[ERROR] Error al crear notificación: {str(notif_error)}")
                import traceback
                traceback.print_exc()

        return JsonResponse({
            'success': True,
            'message': 'Postulación actualizada exitosamente',
            'application': {
                'id': str(application.id),
                'status': application.status,
                'recruiterNotes': application.employer_notes,
                'rating': application.rating
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al actualizar postulación: {str(e)}'
        }, status=500)


@csrf_exempt
@require_authentication
@require_http_methods(["GET"])
def get_unviewed_applications_count(request):
    """
    Obtener el conteo de aplicaciones no vistas por el reclutador
    GET /api/applications/unviewed-count/

    Returns:
    {
        'success': bool,
        'count': int
    }
    """
    try:
        # Obtener todos los jobs del usuario
        user_jobs = Job.objects.filter(email=request.user.email).values_list('id', flat=True)

        # Contar aplicaciones no vistas en esos jobs
        count = JobApplication.objects.filter(
            job_id__in=user_jobs,
            viewed_by_employer=False
        ).count()

        return JsonResponse({
            'success': True,
            'count': count
        }, status=200)

    except Exception as e:
        print(f'[APPLICATIONS] Error al obtener conteo de aplicaciones no vistas: {str(e)}')
        return JsonResponse({
            'success': False,
            'count': 0
        }, status=200)  # Devolver 200 con count 0 en vez de error


@csrf_exempt
@require_authentication
@require_http_methods(["POST"])
def generate_cv_pdf(request, cv_id):
    """
    Generar PDF del CV usando xhtml2pdf

    Este endpoint se llama después de guardar/actualizar el CV
    - Renderiza el template HTML con los datos del CV
    - Genera el PDF con xhtml2pdf
    - Elimina el PDF antiguo si existe
    - Guarda el nuevo PDF en media/applicant_cvs_builder/
    """
    try:
        print(f"\n========== GENERATE CV PDF ==========")
        print(f"User: {request.user.email}")
        print(f"CV ID: {cv_id}")

        # Obtener el CV
        cv = get_object_or_404(
            ApplicantCV,
            id=cv_id,
            applicant=request.user,
            cv_type='created',
            is_deleted=False
        )

        print(f"CV encontrado: {cv.name}")

        # Renderizar template HTML
        html_content = render_to_string('applicants/cv_template.html', {
            'cv_data': cv.cv_data
        })

        print("HTML renderizado correctamente")

        # Generar PDF con xhtml2pdf
        pdf_buffer = io.BytesIO()
        pisa_status = pisa.CreatePDF(
            io.BytesIO(html_content.encode('UTF-8')),
            dest=pdf_buffer
        )

        if pisa_status.err:
            raise Exception("Error al generar el PDF")

        pdf_bytes = pdf_buffer.getvalue()
        pdf_buffer.close()

        print(f"PDF generado: {len(pdf_bytes)} bytes")

        # Eliminar PDF antiguo si existe
        if cv.file:
            try:
                import os
                if os.path.exists(cv.file.path):
                    os.remove(cv.file.path)
                    print(f"PDF antiguo eliminado: {cv.file.path}")
            except Exception as e:
                print(f"Error al eliminar PDF antiguo: {e}")

        # Sanitizar nombre del CV para el archivo
        import re
        safe_name = re.sub(r'[^\w\s-]', '', cv.name)  # Remover caracteres especiales
        safe_name = re.sub(r'[-\s]+', '_', safe_name)  # Reemplazar espacios/guiones con _
        safe_name = safe_name[:50]  # Limitar longitud

        # Guardar nuevo PDF con nombre legible
        pdf_filename = f"{safe_name}.pdf"
        cv.file.save(pdf_filename, ContentFile(pdf_bytes), save=True)

        print(f"Nuevo PDF guardado: {cv.file.name}")
        print(f"PDF URL: {cv.file.url}")
        print(f"====================================\n")

        return JsonResponse({
            'success': True,
            'message': 'PDF generado exitosamente',
            'pdf_url': cv.file.url,
            'cv': {
                'id': str(cv.id),
                'name': cv.name,
                'pdf_url': cv.file.url,
                'updated_at': cv.updated_at.isoformat()
            }
        })

    except ApplicantCV.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'CV no encontrado'
        }, status=404)

    except Exception as e:
        print(f"ERROR al generar PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Error al generar PDF: {str(e)}'
        }, status=500)
