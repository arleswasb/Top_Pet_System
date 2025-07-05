#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

# Corrigir roles existentes
print("🔄 Corrigindo roles dos usuários existentes...")

role_mapping = {
    'Admin': Profile.Role.ADMIN,
    'Veterinario': Profile.Role.VETERINARIO,
    'Funcionario': Profile.Role.FUNCIONARIO,
    'Cliente': Profile.Role.CLIENTE,
}

profiles = Profile.objects.all()
for profile in profiles:
    old_role = profile.role
    if old_role in role_mapping:
        profile.role = role_mapping[old_role]
        profile.save()
        print(f"✅ Usuário {profile.user.username}: '{old_role}' -> '{profile.role}'")
    else:
        print(f"⚠️  Usuário {profile.user.username}: role '{old_role}' já está correto")

print("\n🔍 Verificando roles finais:")
for profile in Profile.objects.all():
    print(f"User: {profile.user.username}, Role: {profile.role}")
    is_admin = profile.role == Profile.Role.ADMIN
    print(f"   Is admin: {is_admin}")
