"""
Middleware para capturar el request actual y hacerlo disponible a los signals
"""
import threading

# Thread-local storage para almacenar el request actual
_thread_locals = threading.local()


def get_current_request():
    """Obtiene el request actual del thread-local storage"""
    return getattr(_thread_locals, 'request', None)


def get_current_user():
    """Obtiene el usuario actual del request"""
    request = get_current_request()
    if request and hasattr(request, 'user'):
        return request.user
    return None


class AuditMiddleware:
    """
    Middleware que captura el request actual y lo almacena en thread-local storage
    para que esté disponible en los signals de auditoría
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Almacenar el request en thread-local storage
        _thread_locals.request = request

        try:
            response = self.get_response(request)
        finally:
            # Limpiar el thread-local storage después de la petición
            if hasattr(_thread_locals, 'request'):
                del _thread_locals.request

        return response
