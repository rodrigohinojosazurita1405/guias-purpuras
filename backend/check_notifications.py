#!/usr/bin/env python
"""Script para verificar el estado de las notificaciones"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from G_Jobs.notifications.models import Notification
from auth_api.models import CustomUser
from G_Jobs.jobs.models import Job

print("=" * 60)
print("VERIFICACIÓN DE NOTIFICACIONES")
print("=" * 60)

# 1. Total de notificaciones
total_notifs = Notification.objects.count()
print(f"\n1. Total notificaciones en BD: {total_notifs}")

if total_notifs > 0:
    print("\nÚltimas 5 notificaciones:")
    for notif in Notification.objects.all()[:5]:
        print(f"  - [{notif.notification_type}] {notif.title} -> {notif.user.email}")

# 2. Usuarios empresa
print(f"\n2. Usuarios empresa:")
companies = CustomUser.objects.filter(role='company')
print(f"   Total: {companies.count()}")
for company in companies:
    print(f"   - {company.email}")
    notifs = Notification.objects.filter(user=company).count()
    print(f"     Notificaciones: {notifs}")

# 3. Jobs con pago verificado
print(f"\n3. Jobs con pago verificado:")
verified_jobs = Job.objects.filter(paymentVerified=True)
print(f"   Total: {verified_jobs.count()}")
for job in verified_jobs[:5]:
    print(f"   - {job.title} (email: {job.email})")

# 4. Verificar si el email del job coincide con alguna empresa
print(f"\n4. Verificación de emails:")
for job in verified_jobs[:3]:
    matching_company = CustomUser.objects.filter(email=job.email, role='company').first()
    if matching_company:
        print(f"   ✓ Job '{job.title}' -> Empresa encontrada: {matching_company.email}")
    else:
        print(f"   ✗ Job '{job.title}' -> NO hay empresa con email: {job.email}")

print("\n" + "=" * 60)
