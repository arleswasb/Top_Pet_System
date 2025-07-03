#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.test import Client

# Testar a rota de password reset
client = Client()

print("=== Testando rotas de password reset ===")

# Testar rota principal
response = client.options('/api/auth/password-reset/')
print(f"/api/auth/password-reset/ -> Status: {response.status_code}")
if response.status_code == 200:
    print(f"Methods: {response.get('Allow', 'N/A')}")

# Testar rota de confirmação
response = client.options('/api/auth/password-reset/confirm/')
print(f"/api/auth/password-reset/confirm/ -> Status: {response.status_code}")
if response.status_code == 200:
    print(f"Methods: {response.get('Allow', 'N/A')}")

# Testar rota de validação
response = client.options('/api/auth/password-reset/validate_token/')
print(f"/api/auth/password-reset/validate_token/ -> Status: {response.status_code}")
if response.status_code == 200:
    print(f"Methods: {response.get('Allow', 'N/A')}")

print("\n=== Testando com POST para verificar estrutura ===")

# Testar POST na rota principal (solicitar reset)
response = client.post('/api/auth/password-reset/', {'email': 'test@example.com'})
print(f"POST /api/auth/password-reset/ -> Status: {response.status_code}")
print(f"Response: {response.content.decode()}")

# Testar POST na rota de confirmação (sem token válido)
response = client.post('/api/auth/password-reset/confirm/', {
    'token': 'fake-token',
    'password': 'newpassword123'
})
print(f"POST /api/auth/password-reset/confirm/ -> Status: {response.status_code}")
print(f"Response: {response.content.decode()}")
