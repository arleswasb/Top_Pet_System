#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

# Verificar o usuário admin
try:
    admin_user = User.objects.get(username='admin')
    print(f'Admin user: {admin_user}')
    print(f'Has profile: {hasattr(admin_user, "profile")}')
    if hasattr(admin_user, 'profile'):
        print(f'Profile role: {admin_user.profile.role}')
        print(f'Is admin role: {admin_user.profile.role == Profile.Role.ADMIN}')
        print(f'Profile.Role.ADMIN value: {Profile.Role.ADMIN}')
    else:
        print('NO PROFILE FOUND!')
        
    # Verificar se existem profiles
    profiles = Profile.objects.all()
    print(f'\nTotal profiles: {profiles.count()}')
    for profile in profiles:
        print(f'User: {profile.user.username}, Role: {profile.role}')
        
except User.DoesNotExist:
    print('Admin user not found!')
