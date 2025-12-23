#!/usr/bin/env python
"""Script para verificar postulaciones en la base de datos"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'G_Jobs.settings')
django.setup()

from G_Jobs.applicants.models import JobApplication
from G_Jobs.jobs.models import Job
from django.contrib.auth import get_user_model

User = get_user_model()

# Verificar trabajos de clau@gmail.com
print("=" * 60)
print("VERIFICANDO DATOS EN LA BASE DE DATOS")
print("=" * 60)

try:
    clau_user = User.objects.get(email='clau@gmail.com')
    print(f"\n✅ Usuario encontrado: {clau_user.email} (ID: {clau_user.id})")
except User.DoesNotExist:
    print("\n❌ Usuario clau@gmail.com NO existe")
    sys.exit(1)

# Trabajos publicados por clau@gmail.com
jobs = Job.objects.filter(email='clau@gmail.com')
print(f"\n📋 Trabajos publicados por clau@gmail.com: {jobs.count()}")
for job in jobs:
    print(f"  - ID: {job.id} | Título: {job.title} | Estado: {job.status}")

# Postulaciones a esos trabajos
apps = JobApplication.objects.filter(job__email='clau@gmail.com').select_related('applicant', 'job', 'cv')
print(f"\n📨 Postulaciones recibidas en trabajos de clau@gmail.com: {apps.count()}")
for app in apps:
    cv_info = ""
    if app.cv:
        cv_info = f" | CV: {app.cv.name} (tipo: {app.cv.cv_type})"
    print(f"  - {app.applicant.email} -> Job #{app.job.id} ({app.job.title}) | Estado: {app.status}{cv_info}")

# Verificar mauge@gmail.com
print("\n" + "=" * 60)
try:
    mauge_user = User.objects.get(email='mauge@gmail.com')
    print(f"✅ Usuario mauge encontrado: {mauge_user.email} (ID: {mauge_user.id})")

    mauge_apps = JobApplication.objects.filter(applicant=mauge_user).select_related('job', 'cv')
    print(f"\n📤 Postulaciones enviadas por mauge@gmail.com: {mauge_apps.count()}")
    for app in mauge_apps:
        cv_info = ""
        if app.cv:
            cv_info = f" | CV: {app.cv.name} (tipo: {app.cv.cv_type})"
        print(f"  - Job #{app.job.id} ({app.job.title}) - Empresa: {app.job.email}{cv_info}")
except User.DoesNotExist:
    print("❌ Usuario mauge@gmail.com NO existe")

print("\n" + "=" * 60)
