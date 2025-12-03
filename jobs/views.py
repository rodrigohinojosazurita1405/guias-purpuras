"""
API Views para Ofertas de Trabajo
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import Job, Application, JobAuditLog
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
    - city (str): Ciudad
    - contractType (str): Tipo de contrato
    - selectedPlan (str: 'estandar'|'purpura'|'impulso'): Plan elegido
    - proofOfPayment (file): Comprobante de pago (imagen, max 5MB)

    CAMPOS OPCIONALES:
    - companyName (str, default: 'Empresa Confidencial')
    - companyAnonymous (bool, default: False)
    - email (str, default: 'contact@empresa.com')
    - jobCategory (str)
    - municipality (str)
    - subcategory (str)
    - modality (str: 'presencial'|'remoto'|'hibrido', default: 'presencial')
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
        # ========== VALIDAR QUE EL USUARIO SEA EMPRESA ==========
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'Debes iniciar sesión para publicar un anuncio'
            }, status=401)

        if request.user.role != 'company':
            return JsonResponse({
                'success': False,
                'message': 'Solo las empresas pueden publicar anuncios de trabajo. Tu cuenta está registrada como postulante.'
            }, status=403)

        # Parsear datos de POST multipart/form-data
        # Intentar primero JSON, si falla usar POST data
        try:
            data = json.loads(request.body) if request.body and 'application/json' in request.META.get('CONTENT_TYPE', '') else {}
        except (json.JSONDecodeError, AttributeError):
            data = {}

        # Combinar datos JSON con POST data y FILES
        data.update(request.POST.dict())
        files = request.FILES.dict()

        print(f'[PUBLISH] [PUBLISH_JOB] Usuario: {request.user.email} (rol: {request.user.role}), Campos recibidos: {list(data.keys())}, Archivos: {list(files.keys())}')

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

        plan = (data.get('selectedPlan') or 'estandar').lower()

        # Obtener el plan desde la BD (case-insensitive para compatibilidad)
        try:
            plan_obj = Plan.objects.get(name__iexact=plan, is_active=True)
            duration_days = plan_obj.duration_days
        except Plan.DoesNotExist:
            errors['selectedPlan'] = "Plan no válido o inactivo. Debe ser 'estandar', 'purpura' o 'impulso'"
            duration_days = 15  # Default fallback

        # Calcular expiryDate automáticamente basándose en el plan
        try:
            today = datetime.now().date()
            expiry_date = today + timedelta(days=duration_days)
            expiry_date = expiry_date.strftime('%Y-%m-%d')
        except Exception as e:
            errors['expiryDate'] = f'Error al calcular fecha de vencimiento: {str(e)}'

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
            # Obtener el CompanyProfile del usuario autenticado
            company_profile = None
            if request.user and request.user.is_authenticated:
                try:
                    from profiles.models import UserProfile
                    user_profile = request.user.userprofile
                    # Obtener el primer CompanyProfile del usuario (si existe)
                    company_profile = user_profile.company_profiles.first()
                except (UserProfile.DoesNotExist, AttributeError):
                    company_profile = None

            # Capturar datos del plan en el momento de publicación
            plan_label = plan_obj.label if 'plan_obj' in locals() else f"{plan.capitalize()} (--)"
            plan_price = f"{plan_obj.price} {plan_obj.currency}" if 'plan_obj' in locals() else "--"
            plan_duration = plan_obj.duration_days if 'plan_obj' in locals() else None

            # Parsear companyAnonymous correctamente desde FormData
            company_anonymous_value = data.get('companyAnonymous', False)
            if isinstance(company_anonymous_value, str):
                company_anonymous = company_anonymous_value.lower() in ('true', '1', 'yes')
            else:
                company_anonymous = bool(company_anonymous_value)

            job = Job.objects.create(
                title=title,
                companyProfile=company_profile,  # Asignar CompanyProfile si existe
                companyName=(data.get('companyName') or 'Empresa Confidencial').strip(),
                companyAnonymous=company_anonymous,
                description=description,
                jobCategory=(data.get('jobCategory') or '').strip(),
                city=city,
                municipality=(data.get('municipality') or '').strip(),
                subcategory=(data.get('subcategory') or '').strip(),
                contractType=contract_type,
                modality=modality,
                expiryDate=expiry_date,
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
                # Datos del plan capturados en el momento de publicación
                planLabel=plan_label,
                planPrice=plan_price,
                planDuration=plan_duration,
                screeningQuestions=data.get('screeningQuestions', []),
                proofOfPayment=proof_of_payment,  # FASE 7.1: Comprobante de pago obligatorio
            )

            print(f'[OK] [PUBLISH_JOB] Job creado: ID={job.id}, Título="{job.title}", Plan={plan}')

            # ========== CREAR PLANORDER (SIEMPRE) ==========
            try:
                from datetime import datetime
                from .models import PlanOrder

                # Parsear billingData que viene como JSON string desde el frontend
                billing_data_raw = data.get('billingData')
                requires_invoice = bool(billing_data_raw)

                # Valores por defecto (vacíos si no requiere factura)
                razon_social = ''
                nit = ''
                ci = ''
                ci_complement = ''
                invoice_email = ''
                whatsapp_invoice = ''

                # Si el usuario proporcionó datos de facturación, extraerlos
                if requires_invoice:
                    try:
                        # Si viene como string JSON, parsearlo
                        if isinstance(billing_data_raw, str):
                            billing_data = json.loads(billing_data_raw)
                        else:
                            billing_data = billing_data_raw

                        # Extraer campos de facturación
                        razon_social = (billing_data.get('businessName') or '').strip()
                        nit = (billing_data.get('nit') or '').strip()
                        ci = (billing_data.get('ci') or '').strip()
                        ci_complement = (billing_data.get('ciComplement') or '').strip()
                        invoice_email = (billing_data.get('invoiceEmail') or '').strip()
                        whatsapp_invoice = (billing_data.get('whatsapp') or '').strip()

                        print(f'[INFO] [PUBLISH_JOB] Usuario requiere factura: {razon_social} (NIT: {nit}, CI: {ci}, Complemento: {ci_complement})')
                        print(f'[INFO] [PUBLISH_JOB] Métodos de envío - Email: "{invoice_email}", WhatsApp: "{whatsapp_invoice}"')
                        print(f'[DEBUG] [PUBLISH_JOB] billingData completo recibido: {billing_data}')
                    except json.JSONDecodeError as je:
                        print(f'[WARN] [PUBLISH_JOB] Error al parsear billingData: {str(je)}')
                        requires_invoice = False
                else:
                    print(f'[INFO] [PUBLISH_JOB] Usuario NO requiere factura')

                # Generar número de orden único
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                invoice_number = f'GP-{request.user.id}-{timestamp}'

                # Crear PlanOrder SIEMPRE (con o sin factura)
                plan_order = PlanOrder.objects.create(
                    user=request.user,
                    plan=plan_obj,
                    invoice_number=invoice_number,
                    razon_social=razon_social,
                    nit=nit,
                    ci=ci,
                    ci_complement=ci_complement,
                    amount_paid=plan_obj.price,
                    status='PENDING',  # Inicia como pendiente, admin lo verifica
                    electronic_invoice_email=invoice_email,
                    electronic_invoice_whatsapp=whatsapp_invoice,
                    payment_proof=proof_of_payment,
                    company_data={
                        'job_id': job.id,
                        'job_title': job.title,
                        'company_name': job.companyName,
                        'plan_label': plan_label,
                        'plan_duration': plan_duration,
                        'requires_invoice': requires_invoice  # ← CLAVE: indica si requiere factura
                    }
                )

                print(f'[OK] [PUBLISH_JOB] PlanOrder creada: ID={plan_order.id}, Orden={invoice_number}, Requiere factura={requires_invoice}')

            except Exception as order_error:
                print(f'[ERROR] [PUBLISH_JOB] Error al crear PlanOrder: {str(order_error)}')
                import traceback
                traceback.print_exc()
                # No fallar la publicación del job, solo advertir
                print(f'[WARN] [PUBLISH_JOB] Job publicado pero sin orden registrada')

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
    Solo muestra si está activa Y el pago está verificado
    """
    try:
        job = Job.objects.get(id=job_id)

        # Verificar que no esté borrado
        if job.isDeleted:
            return JsonResponse({
                'success': False,
                'message': 'Esta oferta ha sido eliminada'
            }, status=404)

        # Verificar que el pago esté verificado
        if not job.paymentVerified:
            return JsonResponse({
                'success': False,
                'message': 'Esta oferta no está disponible. El pago aún no ha sido verificado.'
            }, status=403)

        # Incrementar vistas
        job.views += 1
        job.save(update_fields=['views'])

        # Obtener URL absoluta del logo si existe
        company_logo = None
        if job.companyProfile and job.companyProfile.logo:
            logo_url = job.companyProfile.logo.url
            # Si la URL es relativa, hacerla absoluta
            if not logo_url.startswith(('http://', 'https://')):
                company_logo = request.build_absolute_uri(logo_url)
            else:
                company_logo = logo_url

        return JsonResponse({
            'success': True,
            'job': {
                # Información básica
                'id': job.id,
                'title': job.title,
                'companyName': job.companyName if not job.companyAnonymous else 'Empresa Confidencial',
                'companyAnonymous': job.companyAnonymous,
                'companyLogo': company_logo,
                'description': job.description,

                # Clasificación
                'jobCategory': job.jobCategory,
                'city': job.city,
                'municipality': job.municipality,
                'subcategory': job.subcategory,
                'contractType': job.contractType,
                'modality': job.modality.capitalize() if hasattr(job, 'modality') else 'Presencial',
                'expiryDate': job.expiryDate.isoformat(),

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


def create_audit_log(job, action, userEmail='', changedFields=None, notes='', request=None):
    """
    Crea un registro de auditoría para cambios en trabajos

    Args:
        job: Instancia del modelo Job
        action: Tipo de acción (created, updated, activated, deactivated, etc.)
        userEmail: Email del usuario que realizó la acción
        changedFields: Dict con campos modificados {field: {before: old_value, after: new_value}}
        notes: Notas adicionales
        request: HttpRequest para extraer IP del cliente
    """
    try:
        clientIP = None
        if request:
            # Intentar obtener IP real del cliente (detrás de proxies)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                clientIP = x_forwarded_for.split(',')[0].strip()
            else:
                clientIP = request.META.get('REMOTE_ADDR')

        JobAuditLog.objects.create(
            job=job,
            action=action,
            userEmail=userEmail,
            changedFields=changedFields or {},
            notes=notes,
            clientIP=clientIP
        )
        print(f'[AUDIT] {action.upper()}: Job={job.id}, User={userEmail}')
    except Exception as e:
        print(f'[ERROR] Error creando audit log: {str(e)}')


@require_http_methods(["GET"])
def list_jobs(request):
    """
    Endpoint para listar todas las ofertas de trabajo
    GET /api/jobs/
    Formato optimizado para JobCard component
    Solo muestra trabajos ACTIVOS y con PAGO VERIFICADO
    """
    try:
        jobs = Job.objects.filter(status='active', isDeleted=False, paymentVerified=True)

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

        # Calcular completitud del perfil de empresa
        from profiles.models import CompanyProfile
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
        jobs = Job.objects.filter(email=email).order_by('-createdAt')

        # Convertir a lista con fechas como strings
        jobs_list = []
        for job in jobs:
            # Determinar si el trabajo es visible públicamente
            is_publicly_visible = job.status == 'active' and job.paymentVerified and not job.isDeleted

            job_dict = {
                'id': str(job.id),
                'title': str(job.title),
                'companyName': str(job.companyName),
                'status': str(job.status),
                'paymentVerified': bool(job.paymentVerified),
                'isPubliclyVisible': is_publicly_visible,
                'views': int(job.views or 0),
                'applications': int(job.applications or 0),
                'createdAt': str(job.createdAt.isoformat()) if job.createdAt else None,
                'expiryDate': str(job.expiryDate.isoformat()) if job.expiryDate else None,
                'selectedPlan': str(job.selectedPlan) if job.selectedPlan else None,
                # Datos del plan capturados en el momento de publicación
                'planLabel': str(job.planLabel) if job.planLabel else None,
                'planPrice': str(job.planPrice) if job.planPrice else None,
                'planDuration': int(job.planDuration) if job.planDuration else None,
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


@token_required
@csrf_exempt
@require_http_methods(["PATCH"])
def update_job(request, job_id):
    """
    Endpoint para actualizar un trabajo existente
    PATCH /api/jobs/<job_id>/update

    Body esperado (solo campos a actualizar):
    {
        "title": "string",
        "description": "string",
        "city": "string",
        "contractType": "string",
        "modality": "presencial|remoto|hibrido",
        "status": "active|closed|draft",
        ...otros campos opcionales
    }

    RESPUESTA EXITOSA (200):
    {
        'success': True,
        'message': 'Trabajo actualizado exitosamente',
        'job': {...actualizado}
    }
    """
    try:
        job = Job.objects.get(id=job_id)

        # Parsear datos del request
        data = json.loads(request.body) if request.body else {}

        # Campos permitidos para actualizar
        allowed_fields = [
            'title', 'description', 'city', 'contractType', 'modality',
            'jobCategory', 'municipality', 'subcategory',
            'salaryType', 'salaryMin',
            'salaryMax', 'salaryFixed', 'benefits', 'vacancies', 'email',
            'whatsapp', 'website', 'applicationInstructions', 'applicationType',
            'externalApplicationUrl', 'status'
        ]

        # Rastrear cambios para auditoría
        changedFields = {}
        for field in allowed_fields:
            if field in data:
                old_value = str(getattr(job, field))
                new_value = str(data[field])
                if old_value != new_value:
                    changedFields[field] = {
                        'before': old_value,
                        'after': new_value
                    }
                setattr(job, field, data[field])

        job.save()

        # Crear log de auditoría si hubo cambios
        if changedFields:
            action = 'activated' if data.get('status') == 'active' else 'deactivated' if data.get('status') == 'closed' else 'updated'
            userEmail = request.user.email if request.user else 'anonymous'
            create_audit_log(
                job=job,
                action=action,
                userEmail=userEmail,
                changedFields=changedFields,
                request=request
            )

        return JsonResponse({
            'success': True,
            'message': 'Trabajo actualizado exitosamente',
            'job': {
                'id': job.id,
                'title': job.title,
                'status': job.status,
                'updatedAt': job.updatedAt.isoformat()
            }
        }, status=200)

    except Job.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Trabajo no encontrado'
        }, status=404)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: JSON inválido'
        }, status=400)

    except Exception as e:
        print(f'Error al actualizar trabajo: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_job(request, job_id):
    """
    Endpoint para eliminar un trabajo (Borrado Lógico)
    DELETE /api/jobs/<job_id>/delete

    Marca el trabajo como eliminado sin eliminar el registro de BD.
    Las aplicaciones y auditoría se mantienen para historial.

    RESPUESTA EXITOSA (200):
    {
        'success': True,
        'message': 'Trabajo eliminado exitosamente',
        'id': job_id
    }
    """
    try:
        job = Job.objects.get(id=job_id)
        job_id_for_response = job.id
        job_title = job.title

        # Realizar borrado lógico
        from datetime import datetime, timezone
        job.isDeleted = True
        job.deletedAt = datetime.now(timezone.utc)
        job.save()

        # Crear log de auditoría
        userEmail = request.user.email if request.user else 'anonymous'
        create_audit_log(
            job=job,
            action='deleted',
            userEmail=userEmail,
            notes=f'Trabajo marcado como eliminado: "{job_title}"',
            request=request
        )

        return JsonResponse({
            'success': True,
            'message': 'Trabajo eliminado exitosamente',
            'id': job_id_for_response
        }, status=200)

    except Job.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Trabajo no encontrado'
        }, status=404)

    except Exception as e:
        print(f'Error al eliminar trabajo: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@csrf_exempt
@require_http_methods(["POST"])
def duplicate_job(request, job_id):
    """
    Endpoint para duplicar un trabajo
    POST /api/jobs/<job_id>/duplicate/

    Crea una copia del trabajo con status='draft'

    RESPUESTA EXITOSA (201):
    {
        'success': True,
        'message': 'Trabajo duplicado exitosamente',
        'newJobId': new_job_id,
        'createdAt': timestamp
    }
    """
    try:
        job = Job.objects.get(id=job_id)

        # Crear una copia del trabajo
        new_job = Job.objects.create(
            title=f"{job.title} (Copia)",
            companyName=job.companyName,
            companyAnonymous=job.companyAnonymous,
            description=job.description,
            jobCategory=job.jobCategory,
            city=job.city,
            municipality=job.municipality,
            subcategory=job.subcategory,
            contractType=job.contractType,
            modality=job.modality,
            expiryDate=job.expiryDate,
            salaryType=job.salaryType,
            salaryMin=job.salaryMin,
            salaryMax=job.salaryMax,
            salaryFixed=job.salaryFixed,
            benefits=job.benefits,
            vacancies=job.vacancies,
            email=job.email,
            whatsapp=job.whatsapp,
            website=job.website,
            applicationInstructions=job.applicationInstructions,
            applicationType=job.applicationType,
            externalApplicationUrl=job.externalApplicationUrl,
            selectedPlan=job.selectedPlan,
            screeningQuestions=job.screeningQuestions,
            status='draft'  # Nueva copia siempre comienza en draft
        )

        # Crear log de auditoría para el trabajo duplicado
        userEmail = request.user.email if request.user else 'anonymous'
        create_audit_log(
            job=new_job,
            action='created',
            userEmail=userEmail,
            notes=f'Duplicado desde trabajo: {job.id}',
            request=request
        )

        # Crear log de auditoría para el trabajo original
        create_audit_log(
            job=job,
            action='duplicated',
            userEmail=userEmail,
            notes=f'Se creó duplicado con ID: {new_job.id}',
            request=request
        )

        print(f'[OK] Trabajo duplicado: ID original={job.id}, ID nuevo={new_job.id}')

        return JsonResponse({
            'success': True,
            'message': 'Trabajo duplicado exitosamente',
            'newJobId': new_job.id,
            'createdAt': new_job.createdAt.isoformat()
        }, status=201)

    except Job.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Trabajo no encontrado'
        }, status=404)

    except Exception as e:
        print(f'Error al duplicar trabajo: {str(e)}')
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


# ========== ENDPOINTS PARA ÓRDENES DE PLANES ==========

@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_user_orders(request):
    """
    Obtener todas las órdenes de planes del usuario (empresa)
    GET /api/orders/me

    Returns:
    {
        'success': bool,
        'orders': [
            {
                'id': int,
                'invoiceNumber': str,
                'planLabel': str,
                'razonSocial': str,
                'nit': str,
                'ci': str,
                'amountPaid': float,
                'status': str,
                'orderDate': str (ISO),
                'electronicInvoiceSentDate': str (ISO) or null,
                'electronicInvoiceEmail': str,
                'electronicInvoiceWhatsapp': str
            }
        ],
        'count': int
    }
    """
    try:
        from .models import PlanOrder

        # Obtener órdenes del usuario autenticado
        orders = PlanOrder.objects.filter(user=request.user).select_related('plan')

        # Serializar órdenes
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'invoiceNumber': order.invoice_number,
                'planLabel': order.plan.label,
                'razonSocial': order.razon_social,
                'nit': order.nit,
                'ci': order.ci,
                'ciComplement': order.ci_complement,
                'amountPaid': float(order.amount_paid),
                'status': order.status,
                'statusDisplay': order.get_status_display(),
                'orderDate': order.order_date.isoformat(),
                'electronicInvoiceSentDate': order.electronic_invoice_sent_date.isoformat() if order.electronic_invoice_sent_date else None,
                'electronicInvoiceEmail': order.electronic_invoice_email,
                'electronicInvoiceWhatsapp': order.electronic_invoice_whatsapp,
                'paymentProof': order.payment_proof.url if order.payment_proof else None,
                'companyData': order.company_data,  # Incluye requires_invoice y otros datos
                'createdAt': order.created_at.isoformat(),
                'updatedAt': order.updated_at.isoformat()
            })

        return JsonResponse({
            'success': True,
            'orders': orders_data,
            'count': len(orders_data)
        }, status=200)

    except Exception as e:
        print(f'[ORDERS] Error al obtener órdenes: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_order_detail(request, order_id):
    """
    Obtener detalles de una orden específica
    GET /api/orders/:id

    Returns:
    {
        'success': bool,
        'order': { ... orden completa ... }
    }
    """
    try:
        from .models import PlanOrder

        # Obtener la orden y verificar que pertenece al usuario
        order = PlanOrder.objects.get(id=order_id, user=request.user)

        order_data = {
            'id': order.id,
            'invoiceNumber': order.invoice_number,
            'planLabel': order.plan.label,
            'planName': order.plan.name,
            'razonSocial': order.razon_social,
            'nit': order.nit,
            'ci': order.ci,
            'ciComplement': order.ci_complement,
            'amountPaid': float(order.amount_paid),
            'status': order.status,
            'statusDisplay': order.get_status_display(),
            'orderDate': order.order_date.isoformat(),
            'electronicInvoiceSentDate': order.electronic_invoice_sent_date.isoformat() if order.electronic_invoice_sent_date else None,
            'electronicInvoiceEmail': order.electronic_invoice_email,
            'electronicInvoiceWhatsapp': order.electronic_invoice_whatsapp,
            'paymentProof': order.payment_proof.url if order.payment_proof else None,
            'companyData': order.company_data,
            'createdAt': order.created_at.isoformat(),
            'updatedAt': order.updated_at.isoformat()
        }

        return JsonResponse({
            'success': True,
            'order': order_data
        }, status=200)

    except PlanOrder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Orden no encontrada o no tienes permiso para verla'
        }, status=404)

    except Exception as e:
        print(f'[ORDERS] Error al obtener detalle de orden: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["POST"])
@csrf_exempt
def resend_invoice(request, order_id):
    """
    Reenviar factura electrónica por email o WhatsApp
    POST /api/orders/:id/resend-invoice

    Body:
    {
        'method': 'email' | 'whatsapp' (opcional, por defecto intenta ambas)
    }

    Returns:
    {
        'success': bool,
        'message': str,
        'updatedOrder': { ... }
    }
    """
    try:
        import json
        from .models import PlanOrder
        from datetime import datetime

        # Obtener la orden
        order = PlanOrder.objects.get(id=order_id, user=request.user)

        # Parsear body
        body = json.loads(request.body) if request.body else {}
        method = body.get('method', 'both')

        # Actualizar fecha de envío
        order.electronic_invoice_sent_date = datetime.now()
        order.save()

        # Aquí iría la lógica de envío real (email/WhatsApp)
        # Por ahora solo registramos el intento
        message = f'Factura reenviada por {method}'

        order_data = {
            'id': order.id,
            'invoiceNumber': order.invoice_number,
            'status': order.status,
            'electronicInvoiceSentDate': order.electronic_invoice_sent_date.isoformat()
        }

        return JsonResponse({
            'success': True,
            'message': message,
            'updatedOrder': order_data
        }, status=200)

    except PlanOrder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Orden no encontrada'
        }, status=404)

    except Exception as e:
        print(f'[ORDERS] Error al reenviar factura: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


# ========== ENDPOINTS PARA USUARIOS BLOQUEADOS ==========

@token_required
@require_http_methods(["GET"])
@csrf_exempt
def get_blocked_users(request):
    """
    Obtener lista de usuarios bloqueados por la empresa actual
    GET /api/blocked-users/me

    Returns:
    {
        'success': bool,
        'blockedUsers': [
            {
                'id': int,
                'email': str,
                'reason': str,
                'reasonDisplay': str,
                'reasonNotes': str,
                'blockedAt': str (ISO),
                'blockedUntil': str (ISO) or null,
                'isPermanent': bool
            }
        ],
        'count': int
    }
    """
    try:
        from .models import BlockedUser

        # Obtener usuarios bloqueados por esta empresa
        blocked = BlockedUser.objects.filter(company=request.user).select_related('blocked_user')

        # Serializar
        blocked_data = []
        for block in blocked:
            blocked_data.append({
                'id': block.id,
                'email': block.blocked_user.email,
                'firstName': block.blocked_user.first_name,
                'lastName': block.blocked_user.last_name,
                'reason': block.reason,
                'reasonDisplay': block.get_reason_display(),
                'reasonNotes': block.reason_notes,
                'blockedAt': block.blocked_at.isoformat(),
                'blockedUntil': block.blocked_until.isoformat() if block.blocked_until else None,
                'isPermanent': block.is_permanent,
                'blockedUserId': block.blocked_user.id
            })

        return JsonResponse({
            'success': True,
            'blockedUsers': blocked_data,
            'count': len(blocked_data)
        }, status=200)

    except Exception as e:
        print(f'[BLOCKED] Error al obtener usuarios bloqueados: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["POST"])
@csrf_exempt
def block_user(request):
    """
    Bloquear un usuario
    POST /api/blocked-users/block

    Body:
    {
        'blockedUserId': int,
        'reason': 'SPAM' | 'UNQUALIFIED' | 'OTHER',
        'reasonNotes': str (opcional),
        'isPermanent': bool (opcional, default true)
    }

    Returns:
    {
        'success': bool,
        'message': str,
        'blockedUser': { ... }
    }
    """
    try:
        import json
        from .models import BlockedUser
        from auth_api.models import CustomUser
        from datetime import datetime, timedelta

        # Parsear body
        body = json.loads(request.body)
        blocked_user_id = body.get('blockedUserId')
        reason = body.get('reason', 'OTHER')
        reason_notes = body.get('reasonNotes', '')
        is_permanent = body.get('isPermanent', True)

        if not blocked_user_id:
            return JsonResponse({
                'success': False,
                'message': 'blockedUserId es requerido'
            }, status=400)

        # Obtener el usuario a bloquear
        try:
            blocked_user = CustomUser.objects.get(id=blocked_user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario a bloquear no encontrado'
            }, status=404)

        # Verificar si ya existe bloqueo
        existing = BlockedUser.objects.filter(company=request.user, blocked_user=blocked_user).first()
        if existing:
            return JsonResponse({
                'success': False,
                'message': 'Este usuario ya está bloqueado'
            }, status=400)

        # Crear bloqueo
        block = BlockedUser.objects.create(
            company=request.user,
            blocked_user=blocked_user,
            reason=reason,
            reason_notes=reason_notes,
            is_permanent=is_permanent,
            blocked_until=None if is_permanent else datetime.now() + timedelta(days=30)
        )

        blocked_data = {
            'id': block.id,
            'email': block.blocked_user.email,
            'firstName': block.blocked_user.first_name,
            'lastName': block.blocked_user.last_name,
            'reason': block.reason,
            'reasonDisplay': block.get_reason_display(),
            'reasonNotes': block.reason_notes,
            'blockedAt': block.blocked_at.isoformat(),
            'blockedUntil': block.blocked_until.isoformat() if block.blocked_until else None,
            'isPermanent': block.is_permanent
        }

        return JsonResponse({
            'success': True,
            'message': f'Usuario {blocked_user.email} bloqueado correctamente',
            'blockedUser': blocked_data
        }, status=201)

    except Exception as e:
        print(f'[BLOCKED] Error al bloquear usuario: {str(e)}')
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@token_required
@require_http_methods(["DELETE"])
@csrf_exempt
def unblock_user(request, block_id):
    """
    Desbloquear un usuario
    DELETE /api/blocked-users/:id

    Returns:
    {
        'success': bool,
        'message': str
    }
    """
    try:
        from .models import BlockedUser

        # Obtener y eliminar el bloqueo
        block = BlockedUser.objects.get(id=block_id, company=request.user)
        blocked_email = block.blocked_user.email

        block.delete()

        return JsonResponse({
            'success': True,
            'message': f'Usuario {blocked_email} desbloqueado correctamente'
        }, status=200)

    except BlockedUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Bloqueo no encontrado'
        }, status=404)

    except Exception as e:
        print(f'[BLOCKED] Error al desbloquear usuario: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@csrf_exempt
def check_if_blocked(request, user_id):
    """
    Verificar si un usuario está bloqueado para una empresa
    GET /api/blocked-users/check/:userId

    Params:
    - company_id: ID de la empresa (si no se proporciona, usa el usuario actual si está autenticado)

    Returns:
    {
        'success': bool,
        'isBlocked': bool,
        'blockInfo': { ... } or null
    }
    """
    try:
        from .models import BlockedUser
        from auth_api.models import CustomUser
        from datetime import datetime

        # Obtener empresa
        company_id = request.GET.get('company_id')

        if not company_id and not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'Empresa no especificada'
            }, status=400)

        # Usar empresa actual o la especificada
        company = request.user if request.user.is_authenticated and not company_id else None
        if company_id:
            try:
                company = CustomUser.objects.get(id=company_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Empresa no encontrada'
                }, status=404)

        # Obtener usuario
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=404)

        # Buscar bloqueo
        block = BlockedUser.objects.filter(company=company, blocked_user=user).first()

        if not block:
            return JsonResponse({
                'success': True,
                'isBlocked': False,
                'blockInfo': None
            }, status=200)

        # Verificar si el bloqueo sigue siendo válido (temporal)
        if not block.is_permanent and block.blocked_until:
            if datetime.now() > block.blocked_until:
                # Bloqueo expirado, eliminarlo
                block.delete()
                return JsonResponse({
                    'success': True,
                    'isBlocked': False,
                    'blockInfo': None
                }, status=200)

        block_info = {
            'id': block.id,
            'reason': block.reason,
            'reasonDisplay': block.get_reason_display(),
            'reasonNotes': block.reason_notes,
            'isPermanent': block.is_permanent,
            'blockedUntil': block.blocked_until.isoformat() if block.blocked_until else None
        }

        return JsonResponse({
            'success': True,
            'isBlocked': True,
            'blockInfo': block_info
        }, status=200)

    except Exception as e:
        print(f'[BLOCKED] Error al verificar bloqueo: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
