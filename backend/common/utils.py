"""
Utilidades compartidas entre apps del proyecto
"""
import os
from django.conf import settings
from django.http import JsonResponse


def get_absolute_media_url(media_path, request=None):
    """
    Convierte ruta de media relativa a URL absoluta

    Args:
        media_path: Ruta del archivo de media (str o FileField)
        request: Request object de Django (opcional)

    Returns:
        str: URL absoluta del archivo o None si no existe

    Example:
        >>> get_absolute_media_url('company_logos/logo.jpg', request)
        'http://localhost:8000/media/company_logos/logo.jpg'
    """
    if not media_path:
        return None

    # Convertir a string si es FileField
    media_str = str(media_path)

    # Si ya es una URL absoluta, retornarla
    if media_str.startswith(('http://', 'https://')):
        return media_str

    # Construir URL absoluta
    if request:
        # Usar build_absolute_uri si tenemos request
        if hasattr(media_path, 'url'):
            return request.build_absolute_uri(media_path.url)
        return request.build_absolute_uri(f"{settings.MEDIA_URL}{media_str}")

    # Fallback: construir URL manualmente
    return f"{settings.MEDIA_URL}{media_str}"


def safe_delete_file(file_field):
    """
    Elimina archivo de forma segura del sistema de archivos

    Args:
        file_field: Campo de archivo de Django (ImageField, FileField, etc.)

    Returns:
        bool: True si se eliminó exitosamente, False en caso contrario

    Example:
        >>> safe_delete_file(profile.photo)
        True
    """
    if not file_field or not file_field.name:
        return False

    try:
        file_path = file_field.path
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f'⚠️ Error al eliminar archivo: {str(e)}')

    return False


def validate_image_upload(file, max_size_mb=5):
    """
    Valida archivo de imagen subido

    Args:
        file: Archivo subido (UploadedFile)
        max_size_mb: Tamaño máximo en megabytes (default: 5)

    Returns:
        tuple: (is_valid: bool, error_message: str or None)

    Example:
        >>> is_valid, error = validate_image_upload(uploaded_file, max_size_mb=5)
        >>> if not is_valid:
        ...     return JsonResponse({'error': error}, status=400)
    """
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']

    # Validar tipo de archivo
    if file.content_type not in allowed_types:
        return False, 'Tipo de archivo no permitido. Use: JPG, PNG, GIF o WEBP'

    # Validar tamaño
    max_size_bytes = max_size_mb * 1024 * 1024
    if file.size > max_size_bytes:
        return False, f'Archivo demasiado grande. Máximo {max_size_mb}MB'

    return True, None


def validate_password_strength(password):
    """
    Valida fortaleza de contraseña

    Args:
        password: Contraseña a validar (str)

    Returns:
        tuple: (is_valid: bool, error_message: str or None)

    Example:
        >>> is_valid, error = validate_password_strength('abc123')
        >>> if not is_valid:
        ...     return JsonResponse({'error': error}, status=400)
    """
    if not password or len(password) < 6:
        return False, 'La contraseña debe tener al menos 6 caracteres'

    # Aquí se pueden agregar más validaciones en el futuro:
    # - Debe contener al menos una letra mayúscula
    # - Debe contener al menos un número
    # - Debe contener al menos un carácter especial

    return True, None


def format_salary(salary):
    """
    Formatea salario con separadores de miles

    Args:
        salary: Salario a formatear (int, float o str)

    Returns:
        str: Salario formateado o cadena vacía si es None

    Example:
        >>> format_salary(15000)
        '15,000'
        >>> format_salary(None)
        ''
    """
    if not salary:
        return ''

    try:
        return f"{int(salary):,}"
    except (ValueError, TypeError):
        return ''


def calculate_days_ago(date):
    """
    Calcula días transcurridos desde una fecha

    Args:
        date: Fecha a comparar (datetime.date o datetime.datetime)

    Returns:
        int: Número de días transcurridos

    Example:
        >>> from datetime import date, timedelta
        >>> yesterday = date.today() - timedelta(days=1)
        >>> calculate_days_ago(yesterday)
        1
    """
    from datetime import datetime

    if not date:
        return 0

    # Convertir a date si es datetime
    if isinstance(date, datetime):
        date = date.date()

    today = datetime.now().date()
    delta = today - date
    return delta.days
