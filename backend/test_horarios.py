#!/usr/bin/env python
"""
Teste do endpoint de horários disponíveis
"""
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import date, timedelta

def test_horarios_disponiveis():
    """Testa o endpoint de horários disponíveis"""
    print("=== Teste do endpoint de horários disponíveis ===")
    
    client = Client()
    
    # 1. Criar um usuário para teste
    print("\n1. Criando usuário de teste...")
    test_user, created = User.objects.get_or_create(
        username='testuser_horarios',
        defaults={'email': 'test_horarios@example.com'}
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
    
    # 2. Criar token para autenticação
    token, _ = Token.objects.get_or_create(user=test_user)
    headers = {'HTTP_AUTHORIZATION': f'Token {token.key}'}
    
    # 3. Testar endpoint sem parâmetros
    print("\n2. Testando sem parâmetros...")
    response = client.get('/api/agendamentos/horarios-disponiveis/', **headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 4. Testar com data inválida
    print("\n3. Testando com data inválida...")
    response = client.get('/api/agendamentos/horarios-disponiveis/?data=invalid', **headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 5. Testar com data passada
    print("\n4. Testando com data passada...")
    ontem = date.today() - timedelta(days=1)
    response = client.get(f'/api/agendamentos/horarios-disponiveis/?data={ontem}', **headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 6. Testar com data válida (amanhã)
    print("\n5. Testando com data válida (amanhã)...")
    amanha = date.today() + timedelta(days=1)
    response = client.get(f'/api/agendamentos/horarios-disponiveis/?data={amanha}', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        horarios = response.json()
        print(f"Horários disponíveis ({len(horarios)}): {horarios[:5]}...")  # Mostra os primeiros 5
    else:
        print(f"Response: {response.json()}")
    
    # 7. Testar sem autenticação
    print("\n6. Testando sem autenticação...")
    response = client.get(f'/api/agendamentos/horarios-disponiveis/?data={amanha}')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Cleanup
    print("\n7. Limpando dados de teste...")
    test_user.delete()
    print("Dados de teste removidos")

if __name__ == '__main__':
    test_horarios_disponiveis()
    print("\n=== Teste concluído ===")
