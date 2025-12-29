#!/usr/bin/env python
"""Script para probar manualmente las notificaciones"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

print("=" * 60)
print("TEST DE NOTIFICACIONES")
print("=" * 60)

# 1. Importar modelos
from G_Jobs.notifications.models import Notification
from auth_api.models import CustomUser

# 2. Obtener una empresa
company = CustomUser.objects.filter(role='company').first()
if not company:
    print("❌ No hay empresas en la BD")
    exit(1)

print(f"\nEmpresa encontrada: {company.email}")

# 3. Crear notificación de prueba
try:
    notif = Notification.create_notification(
        user=company,
        notification_type='payment_verified',
        title='PRUEBA - Pago verificado',
        message='Esta es una notificación de prueba del sistema',
        metadata={'test': True}
    )
    print(f"Notificacion creada: {notif.id}")
    print(f"  - Titulo: {notif.title}")
    print(f"  - Usuario: {notif.user.email}")
    print(f"  - Tipo: {notif.notification_type}")

    # 4. Verificar que existe en BD
    count = Notification.objects.filter(user=company).count()
    print(f"\nTotal notificaciones para {company.email}: {count}")

    print("\n" + "=" * 60)
    print("ÉXITO: La notificación se creó correctamente")
    print("Ahora revisa el dashboard de la empresa")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
