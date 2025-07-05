#!/usr/bin/env python3
"""
Script para validar se todos os endpoints estão funcionando corretamente
após as correções feitas nos testes
"""

import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from users.models import Profile

def test_basic_endpoints():
    """Testa endpoints básicos"""
    print("🧪 VALIDAÇÃO DOS ENDPOINTS APÓS CORREÇÕES")
    print("=" * 50)
    
    client = Client()
    
    # Criar usuário de teste
    print("\n1. Criando usuário de teste...")
    user, created = User.objects.get_or_create(
        username='test_validation',
        defaults={
            'email': 'test@example.com',
            'is_active': True
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        # Atualizar perfil criado automaticamente
        user.profile.role = Profile.Role.CLIENTE
        user.profile.save()
    
    # Criar token
    token, _ = Token.objects.get_or_create(user=user)
    headers = {'HTTP_AUTHORIZATION': f'Token {token.key}'}
    
    print("✅ Usuário criado com sucesso")
    
    # Testar endpoints principais
    endpoints_to_test = [
        ('GET', '/api/', 200, 'API Status'),
        ('GET', '/api/pets/', 200, 'Lista de Pets'),
        ('GET', '/api/agendamentos/', 200, 'Lista de Agendamentos'),
        ('GET', '/api/agendamentos/servicos/', 200, 'Lista de Serviços'),
        ('GET', '/api/prontuarios/', 200, 'Lista de Prontuários'),
        ('GET', '/api/users/me/', 200, 'Perfil do Usuário'),
        ('GET', '/api/configuracao/horarios-funcionamento/', 200, 'Horários de Funcionamento'),
        ('GET', '/api/configuracao/feriados/', 200, 'Feriados'),
    ]
    
    print("\n2. Testando endpoints principais...")
    success_count = 0
    total_tests = len(endpoints_to_test)
    
    for method, endpoint, expected_status, description in endpoints_to_test:
        try:
            if method == 'GET':
                response = client.get(endpoint, **headers)
            else:
                response = client.post(endpoint, **headers)
            
            if response.status_code == expected_status:
                print(f"✅ {description}: {endpoint} → {response.status_code}")
                success_count += 1
            else:
                print(f"❌ {description}: {endpoint} → {response.status_code} (esperado: {expected_status})")
                
        except Exception as e:
            print(f"❌ {description}: {endpoint} → Erro: {str(e)}")
    
    # Testar endpoint específico de horários disponíveis
    print("\n3. Testando endpoint de horários disponíveis...")
    try:
        from datetime import date, timedelta
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        response = client.get(f'/api/agendamentos/horarios-disponiveis/?data={tomorrow}', **headers)
        if response.status_code == 200:
            print(f"✅ Horários Disponíveis: /api/agendamentos/horarios-disponiveis/ → {response.status_code}")
            success_count += 1
        else:
            print(f"❌ Horários Disponíveis: /api/agendamentos/horarios-disponiveis/ → {response.status_code}")
        total_tests += 1
    except Exception as e:
        print(f"❌ Horários Disponíveis: Erro: {str(e)}")
        total_tests += 1
    
    # Resultado final
    print(f"\n4. RESULTADO DA VALIDAÇÃO:")
    print(f"   Total de testes: {total_tests}")
    print(f"   Sucessos: {success_count}")
    print(f"   Falhas: {total_tests - success_count}")
    print(f"   Taxa de sucesso: {(success_count / total_tests) * 100:.1f}%")
    
    if success_count == total_tests:
        print(f"\n🎉 TODOS OS ENDPOINTS ESTÃO FUNCIONANDO CORRETAMENTE!")
        print("✅ As correções nos testes foram bem-sucedidas")
    else:
        print(f"\n⚠️  ALGUNS ENDPOINTS APRESENTARAM PROBLEMAS")
        print("❗ Verifique os erros acima")
    
    # Limpeza
    if created:
        user.delete()
        print("\n🧹 Usuário de teste removido")
    
    return success_count == total_tests

if __name__ == '__main__':
    try:
        success = test_basic_endpoints()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erro durante a validação: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
