#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

try:
    user = User.objects.get(email='impulsombolivia@gmail.com')
    print('User found:', user.email)
    print('ID:', user.id)

    token = AccessToken.for_user(user)
    print('\nFresh token:')
    print(str(token))

except User.DoesNotExist:
    print('User not found!')
except Exception as e:
    print('Error:', str(e))
