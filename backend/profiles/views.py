"""
API Views para Perfiles de Usuario y Empresa
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import UserProfile, CompanyProfile


# ========== HELPER FUNCTIONS ==========

def get_absolute_media_url(media_path):
    """Convierte una ruta de media relativa a URL absoluta"""
    if not media_path:
        return None
    # Si ya es una URL absoluta, devolverla tal cual
    if str(media_path).startswith('http'):
        return str(media_path)
    # Construir URL absoluta
    return f"http://localhost:8000{settings.MEDIA_URL}{media_path}"


# ========== USER PROFILE ENDPOINTS ==========

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_or_create_my_profile(request):
    """
    Obtener o crear el perfil del usuario autenticado
    GET/POST /api/profiles/me/

    Si el usuario no tiene perfil, se crea automáticamente
    """
    try:
        user = request.user

        # Intentar obtener el perfil existente
        try:
            user_profile = UserProfile.objects.get(email=user.email)
        except UserProfile.DoesNotExist:
            # Crear perfil si no existe
            user_profile = UserProfile.objects.create(
                fullName=user.get_full_name() or user.username,
                email=user.email,
                phone='',
                location='',
                bio=''
            )

        return JsonResponse({
            'success': True,
            'profile': {
                'id': user_profile.id,
                'fullName': user_profile.fullName,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'location': user_profile.location,
                'bio': user_profile.bio,
                'profilePhoto': get_absolute_media_url(user_profile.profilePhoto),
                'createdAt': user_profile.createdAt.isoformat(),
                'updatedAt': user_profile.updatedAt.isoformat()
            }
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def create_user_profile(request):
    """
    Crear un nuevo perfil de usuario
    POST /api/profiles/user/create

    Body esperado:
    {
        "fullName": "Juan Pérez",
        "email": "juan@example.com",
        "phone": "1234567890",
        "location": "La Paz, Bolivia",
        "bio": "Ingeniero de software con 5 años de experiencia"
    }
    """
    try:
        data = json.loads(request.body)

        # Validaciones
        if not data.get('fullName'):
            return JsonResponse({
                'success': False,
                'message': 'El nombre completo es requerido'
            }, status=400)

        if not data.get('email'):
            return JsonResponse({
                'success': False,
                'message': 'El email es requerido'
            }, status=400)

        # Verificar si el usuario ya existe
        if UserProfile.objects.filter(email=data.get('email')).exists():
            return JsonResponse({
                'success': False,
                'message': 'El email ya está registrado'
            }, status=409)

        # Crear perfil
        user_profile = UserProfile.objects.create(
            fullName=data.get('fullName'),
            email=data.get('email'),
            phone=data.get('phone', ''),
            location=data.get('location', ''),
            bio=data.get('bio', '')
        )

        return JsonResponse({
            'success': True,
            'message': '¡Perfil de usuario creado exitosamente!',
            'profile': {
                'id': user_profile.id,
                'fullName': user_profile.fullName,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'location': user_profile.location,
                'bio': user_profile.bio,
                'createdAt': user_profile.createdAt.isoformat()
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)
    except Exception as e:
        print(f'Error al crear perfil de usuario: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_user_profile(request, user_id):
    """
    Obtener perfil de usuario por ID
    GET /api/profiles/user/<user_id>/
    """
    try:
        user_profile = UserProfile.objects.get(id=user_id)

        return JsonResponse({
            'success': True,
            'profile': {
                'id': user_profile.id,
                'fullName': user_profile.fullName,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'location': user_profile.location,
                'bio': user_profile.bio,
                'profilePhoto': get_absolute_media_url(user_profile.profilePhoto),
                'createdAt': user_profile.createdAt.isoformat(),
                'updatedAt': user_profile.updatedAt.isoformat()
            }
        })

    except UserProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de usuario no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_user_profile_by_email(request, email):
    """
    Obtener perfil de usuario por email
    GET /api/profiles/user/email/<email>/
    """
    try:
        user_profile = UserProfile.objects.get(email=email)

        return JsonResponse({
            'success': True,
            'profile': {
                'id': user_profile.id,
                'fullName': user_profile.fullName,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'location': user_profile.location,
                'bio': user_profile.bio,
                'profilePhoto': get_absolute_media_url(user_profile.profilePhoto),
                'createdAt': user_profile.createdAt.isoformat(),
                'updatedAt': user_profile.updatedAt.isoformat()
            }
        })

    except UserProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de usuario no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["PATCH"])
@csrf_exempt
def update_user_profile(request, user_id):
    """
    Actualizar perfil de usuario
    PATCH /api/profiles/user/<user_id>/

    Body esperado (todos los campos opcionales):
    {
        "fullName": "Juan Pérez",
        "phone": "1234567890",
        "location": "La Paz, Bolivia",
        "bio": "Ingeniero de software con 5 años de experiencia"
    }
    """
    try:
        user_profile = UserProfile.objects.get(id=user_id)
        data = json.loads(request.body) if request.body else {}

        # Actualizar campos
        if 'fullName' in data:
            user_profile.fullName = data['fullName']
        if 'phone' in data:
            user_profile.phone = data['phone']
        if 'location' in data:
            user_profile.location = data['location']
        if 'bio' in data:
            user_profile.bio = data['bio']

        user_profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Perfil de usuario actualizado exitosamente',
            'profile': {
                'id': user_profile.id,
                'fullName': user_profile.fullName,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'location': user_profile.location,
                'bio': user_profile.bio,
                'profilePhoto': get_absolute_media_url(user_profile.profilePhoto),
                'updatedAt': user_profile.updatedAt.isoformat()
            }
        })

    except UserProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de usuario no encontrado'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error: formato JSON inválido'
        }, status=400)
    except Exception as e:
        print(f'Error al actualizar perfil de usuario: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


# ========== COMPANY PROFILE ENDPOINTS ==========

@require_http_methods(["POST"])
@csrf_exempt
def create_company_profile(request):
    """
    Crear un nuevo perfil de empresa
    POST /api/profiles/company/create

    Body esperado (FormData):
    - userProfileId: "abc123"
    - companyName: "Tech Solutions"
    - description: "Empresa de desarrollo de software"
    - email: "contact@techsolutions.com"
    - phone: "1234567890"
    - website: "https://techsolutions.com"
    - address: "Av. Principal 123"
    - city: "La Paz"
    - category: "jobs"
    - logo: (archivo opcional)
    - banner: (archivo opcional)
    """
    try:
        # Obtener datos del FormData
        user_profile_id = request.POST.get('userProfileId')
        company_name = request.POST.get('companyName')
        email = request.POST.get('email')

        # Logging para debug
        print(f'[CREATE_COMPANY] {company_name} | FILES: {list(request.FILES.keys())}')

        # Validaciones
        if not user_profile_id:
            return JsonResponse({
                'success': False,
                'message': 'El ID del perfil de usuario es requerido'
            }, status=400)

        if not company_name:
            return JsonResponse({
                'success': False,
                'message': 'El nombre de la empresa es requerido'
            }, status=400)

        if not email:
            return JsonResponse({
                'success': False,
                'message': 'El email de la empresa es requerido'
            }, status=400)

        # Obtener usuario propietario
        try:
            user_profile = UserProfile.objects.get(id=user_profile_id)
        except UserProfile.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Perfil de usuario no encontrado'
            }, status=404)

        # Crear perfil de empresa
        company_profile = CompanyProfile.objects.create(
            owner=user_profile,
            companyName=company_name,
            description=request.POST.get('description', ''),
            email=email,
            contactEmail=request.POST.get('contactEmail', ''),
            phone=request.POST.get('phone', ''),
            website=request.POST.get('website', ''),
            location=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            category=request.POST.get('category', 'other')
        )

        # Procesar logo si fue enviado
        if 'logo' in request.FILES:
            logo_file = request.FILES['logo']
            # Validaciones básicas
            if logo_file.size <= 5 * 1024 * 1024:  # máx 5MB
                company_profile.logo = logo_file
                print(f'DEBUG: Logo file assigned to company_profile: {logo_file.name}')
            else:
                print(f'DEBUG: Logo file too large: {logo_file.size} bytes')
        else:
            print(f'DEBUG: No logo file in request.FILES')

        # Procesar banner si fue enviado
        if 'banner' in request.FILES:
            banner_file = request.FILES['banner']
            # Validaciones básicas
            if banner_file.size <= 10 * 1024 * 1024:  # máx 10MB
                company_profile.banner = banner_file
                print(f'DEBUG: Banner file assigned to company_profile: {banner_file.name}')
            else:
                print(f'DEBUG: Banner file too large: {banner_file.size} bytes')
        else:
            print(f'DEBUG: No banner file in request.FILES')

        print(f'DEBUG: Before save - logo={company_profile.logo}, banner={company_profile.banner}')
        company_profile.save()
        print(f'DEBUG: After save - logo={company_profile.logo}, banner={company_profile.banner}')

        return JsonResponse({
            'success': True,
            'message': '¡Perfil de empresa creado exitosamente!',
            'profile': {
                'id': company_profile.id,
                'companyName': company_profile.companyName,
                'description': company_profile.description,
                'email': company_profile.email,
                'contactEmail': company_profile.contactEmail,
                'phone': company_profile.phone,
                'website': company_profile.website,
                'location': company_profile.location,
                'city': company_profile.city,
                'category': company_profile.category,
                'verified': company_profile.verified,
                'logo': get_absolute_media_url(company_profile.logo) if company_profile.logo else None,
                'banner': get_absolute_media_url(company_profile.banner) if company_profile.banner else None,
                'createdAt': company_profile.createdAt.isoformat()
            }
        }, status=201)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f'Error al crear perfil de empresa: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@api_view(['GET', 'PATCH'])
@authentication_classes([JWTAuthentication])
@csrf_exempt
def get_company_profile(request, company_id):
    """
    Obtener o actualizar perfil de empresa por ID
    GET /api/profiles/company/<company_id>/
    PATCH /api/profiles/company/<company_id>/
    """
    # Handle PATCH requests (update)
    if request.method == 'PATCH':
        return update_company_profile(request, company_id)

    # Handle GET requests (retrieve)
    try:
        company_profile = CompanyProfile.objects.get(id=company_id)

        return JsonResponse({
            'success': True,
            'profile': {
                'id': company_profile.id,
                'owner': {
                    'id': company_profile.owner.id,
                    'fullName': company_profile.owner.fullName,
                    'email': company_profile.owner.email
                },
                'companyName': company_profile.companyName,
                'description': company_profile.description,
                'email': company_profile.email,
                'contactEmail': company_profile.contactEmail,
                'phone': company_profile.phone,
                'website': company_profile.website,
                'location': company_profile.location,
                'city': company_profile.city,
                'category': company_profile.category,
                'verified': company_profile.verified,
                'nit': company_profile.nit,
                'legalName': company_profile.legalName,
                'seprecCode': company_profile.seprecCode,
                'verificationRequestedAt': company_profile.verificationRequestedAt.isoformat() if company_profile.verificationRequestedAt else None,
                'logo': get_absolute_media_url(company_profile.logo) if company_profile.logo else None,
                'banner': get_absolute_media_url(company_profile.banner) if company_profile.banner else None,
                'createdAt': company_profile.createdAt.isoformat(),
                'updatedAt': company_profile.updatedAt.isoformat()
            }
        })

    except CompanyProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de empresa no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


def update_company_profile(request, company_id):
    """
    Actualizar perfil de empresa (llamado desde get_company_profile)
    PATCH /api/profiles/company/<company_id>/

    Body esperado (JSON o FormData - todos los campos opcionales):
    {
        "companyName": "Tech Solutions",
        "description": "Empresa de desarrollo de software",
        "email": "contact@techsolutions.com",
        "phone": "1234567890",
        "website": "https://techsolutions.com",
        "address": "Av. Principal 123",
        "city": "La Paz",
        "category": "jobs"
    }

    Files opcionales (solo con FormData):
    - logo (archivo)
    - banner (archivo)
    """
    try:
        import json
        company_profile = CompanyProfile.objects.get(id=company_id)

        # Parsear datos - puede ser JSON o FormData
        data_dict = {}

        # Intentar parsear JSON primero
        if request.content_type and 'application/json' in request.content_type:
            try:
                data_dict = json.loads(request.body)
                print(f'[DEBUG] Parsed JSON data')
            except json.JSONDecodeError:
                print(f'[DEBUG] Failed to parse JSON, trying FormData')
                data_dict = request.POST.dict()
        else:
            # Si no es JSON, usar FormData (request.POST)
            data_dict = request.POST.dict()

        print(f'[UPDATE_COMPANY] Data keys: {list(data_dict.keys())}')
        print(f'[UPDATE_COMPANY] FILES keys: {list(request.FILES.keys())}')
        print(f'[UPDATE_COMPANY] Content-Type: {request.content_type}')
        print(f'[UPDATE_COMPANY] REQUEST.FILES: {request.FILES}')
        for key, file in request.FILES.items():
            print(f'[UPDATE_COMPANY] File {key}: {file.name}, size: {file.size}, path: {file.file}')

        # Actualizar campos de texto
        if data_dict.get('companyName'):
            company_profile.companyName = data_dict.get('companyName')
            print(f'[UPDATE] companyName: {company_profile.companyName}')

        if data_dict.get('description'):
            company_profile.description = data_dict.get('description')
            print(f'[UPDATE] description: {company_profile.description}')

        if data_dict.get('email'):
            company_profile.email = data_dict.get('email')
            print(f'[UPDATE] email: {company_profile.email}')

        if 'contactEmail' in data_dict:
            company_profile.contactEmail = data_dict.get('contactEmail', '')
            print(f'[UPDATE] contactEmail: {company_profile.contactEmail}')

        if data_dict.get('phone'):
            company_profile.phone = data_dict.get('phone')
            print(f'[UPDATE] phone: {company_profile.phone}')

        if data_dict.get('website'):
            company_profile.website = data_dict.get('website')
            print(f'[UPDATE] website: {company_profile.website}')

        # Aceptar tanto 'address' como 'location' para mayor compatibilidad
        location_value = data_dict.get('location') or data_dict.get('address')
        if location_value:
            company_profile.location = location_value
            print(f'[UPDATE] location: {company_profile.location}')

        if data_dict.get('city'):
            company_profile.city = data_dict.get('city')
            print(f'[UPDATE] city: {company_profile.city}')

        if data_dict.get('category'):
            company_profile.category = data_dict.get('category')
            print(f'[UPDATE] category: {company_profile.category}')

        # Actualizar campos de verificación
        if 'nit' in data_dict:
            company_profile.nit = data_dict.get('nit', '')
            print(f'[UPDATE] nit: {company_profile.nit}')

        if 'legalName' in data_dict:
            company_profile.legalName = data_dict.get('legalName', '')
            print(f'[UPDATE] legalName: {company_profile.legalName}')

        if 'seprecCode' in data_dict:
            company_profile.seprecCode = data_dict.get('seprecCode', '')
            print(f'[UPDATE] seprecCode: {company_profile.seprecCode}')

        if 'verificationRequestedAt' in data_dict:
            verification_date_str = data_dict.get('verificationRequestedAt')
            if verification_date_str:
                # Parsear string ISO a datetime
                from datetime import datetime
                try:
                    company_profile.verificationRequestedAt = datetime.fromisoformat(verification_date_str.replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    company_profile.verificationRequestedAt = None
            else:
                company_profile.verificationRequestedAt = None
            print(f'[UPDATE] verificationRequestedAt: {company_profile.verificationRequestedAt}')

        # Procesar logo si fue enviado
        if 'logo' in request.FILES:
            logo_file = request.FILES['logo']
            # Validaciones básicas
            if logo_file.size <= 5 * 1024 * 1024:  # máx 5MB
                # Eliminar logo anterior si existe
                if company_profile.logo and company_profile.logo.name:
                    import os
                    try:
                        old_logo_path = company_profile.logo.path
                        if os.path.exists(old_logo_path):
                            os.remove(old_logo_path)
                    except Exception as e:
                        print(f'Advertencia: No se pudo eliminar el logo anterior: {str(e)}')

                company_profile.logo = logo_file

        # Procesar banner si fue enviado
        if 'banner' in request.FILES:
            banner_file = request.FILES['banner']
            # Validaciones básicas
            if banner_file.size <= 10 * 1024 * 1024:  # máx 10MB
                # Eliminar banner anterior si existe
                if company_profile.banner and company_profile.banner.name:
                    import os
                    try:
                        old_banner_path = company_profile.banner.path
                        if os.path.exists(old_banner_path):
                            os.remove(old_banner_path)
                    except Exception as e:
                        print(f'Advertencia: No se pudo eliminar el banner anterior: {str(e)}')

                company_profile.banner = banner_file

        company_profile.save()
        print(f'[SAVE] Company profile saved successfully. ID: {company_profile.id}, Name: {company_profile.companyName}')
        print(f'[SAVE] Logo: {company_profile.logo}')
        print(f'[SAVE] Banner: {company_profile.banner}')

        # Construir respuesta
        response_data = {
            'success': True,
            'message': 'Perfil de empresa actualizado exitosamente',
            'profile': {
                'id': company_profile.id,
                'companyName': company_profile.companyName,
                'description': company_profile.description,
                'email': company_profile.email,
                'contactEmail': company_profile.contactEmail,
                'phone': company_profile.phone,
                'website': company_profile.website,
                'location': company_profile.location,
                'city': company_profile.city,
                'category': company_profile.category,
                'verified': company_profile.verified,
                'nit': company_profile.nit,
                'legalName': company_profile.legalName,
                'seprecCode': company_profile.seprecCode,
                'verificationRequestedAt': company_profile.verificationRequestedAt.isoformat() if company_profile.verificationRequestedAt else None,
                'logo': get_absolute_media_url(company_profile.logo) if company_profile.logo else None,
                'banner': get_absolute_media_url(company_profile.banner) if company_profile.banner else None,
                'updatedAt': company_profile.updatedAt.isoformat()
            }
        }

        print(f'[RESPONSE] Enviando respuesta: {response_data}')
        return JsonResponse(response_data)

    except CompanyProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de empresa no encontrado'
        }, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f'Error al actualizar perfil de empresa: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def list_user_companies(request, user_id):
    """
    Listar todas las empresas de un usuario
    GET /api/profiles/user/<user_id>/companies
    """
    try:
        user_profile = UserProfile.objects.get(id=user_id)
        company_profiles = CompanyProfile.objects.filter(owner=user_profile)

        companies_list = []
        for company in company_profiles.order_by('-createdAt'):
            companies_list.append({
                'id': company.id,
                'companyName': company.companyName,
                'description': company.description,
                'email': company.email,
                'contactEmail': company.contactEmail,
                'phone': company.phone,
                'website': company.website,
                'location': company.location,
                'city': company.city,
                'category': company.category,
                'verified': company.verified,
                'logo': get_absolute_media_url(company.logo) if company.logo else None,
                'banner': get_absolute_media_url(company.banner) if company.banner else None,
                'createdAt': company.createdAt.isoformat()
            })

        return JsonResponse({
            'success': True,
            'userId': user_id,
            'count': len(companies_list),
            'companies': companies_list
        })

    except UserProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de usuario no encontrado'
        }, status=404)
    except Exception as e:
        print(f'Error al listar empresas: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_user_photo(request, user_id):
    """
    Cargar foto de perfil para un usuario
    PATCH /api/profiles/user/<user_id>/photo

    Espera un archivo multipart/form-data con el campo 'photo'
    Requiere autenticación JWT
    """
    try:
        user_profile = UserProfile.objects.get(id=user_id)

        # Validar que se envió un archivo
        if 'photo' not in request.FILES:
            return JsonResponse({
                'success': False,
                'message': 'No se proporcionó archivo de foto'
            }, status=400)

        photo_file = request.FILES['photo']

        # Validar tipo de archivo
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if photo_file.content_type not in allowed_types:
            return JsonResponse({
                'success': False,
                'message': 'Tipo de archivo no permitido. Solo JPG, PNG, GIF o WEBP.'
            }, status=400)

        # Validar tamaño (máximo 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if photo_file.size > max_size:
            return JsonResponse({
                'success': False,
                'message': 'Archivo demasiado grande. Máximo 5MB.'
            }, status=400)

        # Eliminar foto anterior si existe (solo permite una foto por perfil para evitar saturación del servidor)
        if user_profile.profilePhoto and user_profile.profilePhoto.name:
            import os
            try:
                old_photo_path = user_profile.profilePhoto.path
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
            except Exception as e:
                print(f'Advertencia: No se pudo eliminar la foto anterior: {str(e)}')

        # Guardar la nueva foto
        user_profile.profilePhoto = photo_file
        user_profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Foto de perfil actualizada exitosamente',
            'profile': {
                'id': user_profile.id,
                'fullName': user_profile.fullName,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'location': user_profile.location,
                'bio': user_profile.bio,
                'profilePhoto': get_absolute_media_url(user_profile.profilePhoto),
                'updatedAt': user_profile.updatedAt.isoformat()
            }
        })

    except UserProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de usuario no encontrado'
        }, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user_photo(request, user_id):
    """
    Eliminar foto de perfil de usuario
    DELETE /api/profiles/user/<user_id>/photo

    Requiere autenticación JWT
    """
    try:
        user_profile = UserProfile.objects.get(id=user_id)

        # Verificar si hay foto
        if not user_profile.profilePhoto:
            return JsonResponse({
                'success': False,
                'message': 'No hay foto de perfil para eliminar'
            }, status=400)

        # Eliminar el archivo físico si existe
        if user_profile.profilePhoto.name:
            import os
            file_path = user_profile.profilePhoto.path
            if os.path.exists(file_path):
                os.remove(file_path)

        # Eliminar la referencia en la BD
        user_profile.profilePhoto = None
        user_profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Foto de perfil eliminada exitosamente',
            'profile': {
                'id': user_profile.id,
                'fullName': user_profile.fullName,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'location': user_profile.location,
                'bio': user_profile.bio,
                'profilePhoto': None,
                'updatedAt': user_profile.updatedAt.isoformat()
            }
        })

    except UserProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de usuario no encontrado'
        }, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_or_create_my_company(request):
    """
    Obtener o crear la primera empresa del usuario autenticado
    GET /api/profiles/company/me/

    Si el usuario no tiene empresa, devuelve null en 'company'
    El frontend puede usar esto para determinar si crear una nueva
    """
    try:
        user = request.user

        # Obtener el perfil del usuario
        try:
            user_profile = UserProfile.objects.get(email=user.email)
        except UserProfile.DoesNotExist:
            # Crear perfil si no existe
            user_profile = UserProfile.objects.create(
                fullName=user.get_full_name() or user.username,
                email=user.email,
                phone='',
                location='',
                bio=''
            )

        # Obtener la primera empresa del usuario
        company = CompanyProfile.objects.filter(owner=user_profile).first()

        if not company:
            # Si no hay empresa, devolver que no existe
            return JsonResponse({
                'success': True,
                'company': None,
                'userProfileId': user_profile.id
            })

        return JsonResponse({
            'success': True,
            'company': {
                'id': company.id,
                'companyName': company.companyName,
                'description': company.description,
                'email': company.email,
                'contactEmail': company.contactEmail,
                'phone': company.phone,
                'website': company.website,
                'location': company.location,
                'city': company.city,
                'category': company.category,
                'verified': company.verified,
                'nit': company.nit,
                'legalName': company.legalName,
                'seprecCode': company.seprecCode,
                'verificationRequestedAt': company.verificationRequestedAt.isoformat() if company.verificationRequestedAt else None,
                'logo': get_absolute_media_url(company.logo) if company.logo else None,
                'banner': get_absolute_media_url(company.banner) if company.banner else None,
                'createdAt': company.createdAt.isoformat(),
                'updatedAt': company.updatedAt.isoformat()
            },
            'userProfileId': user_profile.id
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


# ========== COMPANY LOGO ENDPOINTS ==========

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_company_logo(request, company_id):
    """
    Cargar logo para una empresa
    POST /api/profiles/company/<company_id>/logo

    Espera un archivo multipart/form-data con el campo 'logo'
    Requiere autenticación JWT
    """
    try:
        company_profile = CompanyProfile.objects.get(id=company_id)

        # Validar que se envió un archivo
        if 'logo' not in request.FILES:
            return JsonResponse({
                'success': False,
                'message': 'No se proporcionó archivo de logo'
            }, status=400)

        logo_file = request.FILES['logo']

        # Validar tipo de archivo
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if logo_file.content_type not in allowed_types:
            return JsonResponse({
                'success': False,
                'message': 'Tipo de archivo no permitido. Solo JPG, PNG, GIF o WEBP.'
            }, status=400)

        # Validar tamaño (máximo 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if logo_file.size > max_size:
            return JsonResponse({
                'success': False,
                'message': 'Archivo demasiado grande. Máximo 5MB.'
            }, status=400)

        # Eliminar logo anterior si existe
        if company_profile.logo and company_profile.logo.name:
            import os
            try:
                old_logo_path = company_profile.logo.path
                if os.path.exists(old_logo_path):
                    os.remove(old_logo_path)
            except Exception as e:
                print(f'Advertencia: No se pudo eliminar el logo anterior: {str(e)}')

        # Guardar el nuevo logo
        company_profile.logo = logo_file
        company_profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Logo de empresa actualizado exitosamente',
            'logoUrl': get_absolute_media_url(company_profile.logo)
        })

    except CompanyProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de empresa no encontrado'
        }, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@api_view(['PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_company_logo(request, company_id):
    """
    Eliminar logo de empresa
    PATCH/DELETE /api/profiles/company/<company_id>/logo/delete

    Requiere autenticación JWT
    """
    try:
        company_profile = CompanyProfile.objects.get(id=company_id)

        # Eliminar logo si existe
        if company_profile.logo and company_profile.logo.name:
            import os
            try:
                logo_path = company_profile.logo.path
                if os.path.exists(logo_path):
                    os.remove(logo_path)
            except Exception as e:
                print(f'Advertencia: No se pudo eliminar el logo: {str(e)}')

            # Actualizar el modelo para eliminar la referencia
            company_profile.logo = None
            company_profile.save()

            return JsonResponse({
                'success': True,
                'message': 'Logo de empresa eliminado exitosamente',
                'profile': {
                    'id': company_profile.id,
                    'companyName': company_profile.companyName,
                    'email': company_profile.email,
                    'phone': company_profile.phone,
                    'location': company_profile.location,
                    'logo': get_absolute_media_url(company_profile.logo),
                    'banner': get_absolute_media_url(company_profile.banner),
                    'description': company_profile.description
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'La empresa no tiene logo'
            }, status=404)

    except CompanyProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de empresa no encontrado'
        }, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_company_banner(request, company_id):
    """
    Eliminar banner de empresa
    PATCH /api/profiles/company/<company_id>/banner/delete

    Requiere autenticación JWT
    """
    try:
        company_profile = CompanyProfile.objects.get(id=company_id)

        # Eliminar banner si existe
        if company_profile.banner and company_profile.banner.name:
            import os
            try:
                banner_path = company_profile.banner.path
                if os.path.exists(banner_path):
                    os.remove(banner_path)
            except Exception as e:
                print(f'Advertencia: No se pudo eliminar el banner: {str(e)}')

            # Actualizar el modelo para eliminar la referencia
            company_profile.banner = None
            company_profile.save()

            return JsonResponse({
                'success': True,
                'message': 'Banner de empresa eliminado exitosamente',
                'profile': {
                    'id': company_profile.id,
                    'companyName': company_profile.companyName,
                    'email': company_profile.email,
                    'phone': company_profile.phone,
                    'location': company_profile.location,
                    'logo': get_absolute_media_url(company_profile.logo),
                    'banner': get_absolute_media_url(company_profile.banner),
                    'description': company_profile.description
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'La empresa no tiene banner'
            }, status=404)

    except CompanyProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Perfil de empresa no encontrado'
        }, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
