#!/usr/bin/env python
"""
Teste completo do fluxo de password reset
"""
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django_rest_passwordreset.models import ResetPasswordToken
import json

def test_complete_password_reset_flow():
    """Testa o fluxo completo de reset de senha"""
    print("=== Teste completo do fluxo de password reset ===")
    
    client = Client()
    
    # 1. Criar um usuário para teste
    print("\n1. Criando usuário de teste...")
    test_user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='oldpassword123'
    )
    print(f"Usuário criado: {test_user.username} ({test_user.email})")
    
    # 2. Solicitar reset de senha
    print("\n2. Solicitando reset de senha...")
    response = client.post('/api/password-reset/', {
        'email': 'test@example.com'
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        response_data = response.json()
        print(f"Response: {response_data}")
        
        # 3. Buscar o token gerado no banco
        print("\n3. Buscando token gerado...")
        token = ResetPasswordToken.objects.filter(user=test_user).first()
        if token:
            print(f"Token encontrado: {token.key[:10]}...")
            
            # 4. Testar validação do token
            print("\n4. Validando token...")
            validate_response = client.post('/api/password-reset/validate_token/', {
                'token': token.key
            })
            print(f"Validação - Status: {validate_response.status_code}")
            if validate_response.status_code == 200:
                print(f"Validação - Response: {validate_response.json()}")
            
            # 5. Confirmar reset com nova senha
            print("\n5. Confirmando reset com nova senha...")
            confirm_response = client.post('/api/password-reset/confirm/', {
                'token': token.key,
                'password': 'newpassword123'
            })
            print(f"Confirmação - Status: {confirm_response.status_code}")
            if confirm_response.status_code == 200:
                print(f"Confirmação - Response: {confirm_response.json()}")
                
                # 6. Verificar se a senha foi alterada
                print("\n6. Verificando se a senha foi alterada...")
                test_user.refresh_from_db()
                if test_user.check_password('newpassword123'):
                    print("✅ Senha alterada com sucesso!")
                else:
                    print("❌ Senha não foi alterada")
            else:
                print(f"Confirmação - Error: {confirm_response.content.decode()}")
        else:
            print("❌ Token não encontrado no banco")
    else:
        print(f"Error: {response.content.decode()}")
    
    # Cleanup
    print("\n7. Limpando dados de teste...")
    ResetPasswordToken.objects.filter(user=test_user).delete()
    test_user.delete()
    print("Dados de teste removidos")

def test_invalid_scenarios():
    """Testa cenários inválidos"""
    print("\n=== Testando cenários inválidos ===")
    
    client = Client()
    
    # Email inexistente
    print("\n1. Testando email inexistente...")
    response = client.post('/api/password-reset/', {
        'email': 'nonexistent@example.com'
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Token inválido
    print("\n2. Testando token inválido...")
    response = client.post('/api/password-reset/validate_token/', {
        'token': 'invalid_token'
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Confirmação com token inválido
    print("\n3. Testando confirmação com token inválido...")
    response = client.post('/api/password-reset/confirm/', {
        'token': 'invalid_token',
        'password': 'newpassword123'
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == '__main__':
    test_complete_password_reset_flow()
    test_invalid_scenarios()
    print("\n=== Testes concluídos ===")
