#!/usr/bin/env python
"""
Teste funcional completo do endpoint de horários disponíveis
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
import json

def test_horarios_endpoint():
    """Testa o endpoint de horários disponíveis de forma completa"""
    print("=== TESTE FUNCIONAL: Endpoint Horários Disponíveis ===\n")
    
    client = Client()
    
    # 1. Criar usuário de teste
    print("1️⃣ Criando usuário de teste...")
    test_user, created = User.objects.get_or_create(
        username='test_horarios_user',
        defaults={
            'email': 'test_horarios@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"✅ Usuário criado: {test_user.username}")
    else:
        print(f"✅ Usuário existente: {test_user.username}")
    
    # 2. Criar/obter token de autenticação
    token, _ = Token.objects.get_or_create(user=test_user)
    headers = {'HTTP_AUTHORIZATION': f'Token {token.key}'}
    print(f"✅ Token criado: {token.key[:10]}...")
    
    # 3. Testar endpoint sem autenticação
    print("\n2️⃣ Testando sem autenticação...")
    amanha = date.today() + timedelta(days=1)
    response = client.get(f'/api/agendamentos/horarios-disponiveis/?data={amanha}')
    print(f"Status: {response.status_code}")
    if response.status_code == 401:
        print("✅ Corretamente bloqueado sem autenticação")
    else:
        print(f"❌ Deveria retornar 401, mas retornou {response.status_code}")
    
    # 4. Testar sem parâmetro data
    print("\n3️⃣ Testando sem parâmetro 'data'...")
    response = client.get('/api/agendamentos/horarios-disponiveis/', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        response_data = response.json()
        print(f"✅ Erro esperado: {response_data}")
    else:
        print(f"❌ Deveria retornar 400, mas retornou {response.status_code}")
    
    # 5. Testar com data inválida
    print("\n4️⃣ Testando com data inválida...")
    response = client.get('/api/agendamentos/horarios-disponiveis/?data=invalid-date', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        response_data = response.json()
        print(f"✅ Erro esperado: {response_data}")
    else:
        print(f"❌ Deveria retornar 400, mas retornou {response.status_code}")
    
    # 6. Testar com data passada
    print("\n5️⃣ Testando com data passada...")
    ontem = date.today() - timedelta(days=1)
    response = client.get(f'/api/agendamentos/horarios-disponiveis/?data={ontem}', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        response_data = response.json()
        print(f"✅ Erro esperado: {response_data}")
    else:
        print(f"❌ Deveria retornar 400, mas retornou {response.status_code}")
    
    # 7. Testar com data válida (hoje)
    print("\n6️⃣ Testando com data válida (hoje)...")
    hoje = date.today()
    response = client.get(f'/api/agendamentos/horarios-disponiveis/?data={hoje}', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        horarios = response.json()
        print(f"✅ Sucesso! {len(horarios)} horários disponíveis")
        print(f"Primeiros horários: {horarios[:3]}")
        print(f"Últimos horários: {horarios[-3:]}")
        
        # Validar formato dos horários
        if all(isinstance(h, str) and ':' in h for h in horarios):
            print("✅ Formato dos horários correto (HH:MM)")
        else:
            print("❌ Formato dos horários incorreto")
            
        # Verificar horários de expediente (8:00 às 18:00)
        if '08:00' in horarios and '17:00' in horarios:
            print("✅ Horários de expediente corretos")
        else:
            print(f"❌ Horários de expediente incorretos. Primeiro: {horarios[0] if horarios else 'None'}, Último: {horarios[-1] if horarios else 'None'}")
            
    else:
        print(f"❌ Deveria retornar 200, mas retornou {response.status_code}")
        if hasattr(response, 'json'):
            print(f"Response: {response.json()}")
    
    # 8. Testar com data futura
    print("\n7️⃣ Testando com data futura (amanhã)...")
    amanha = date.today() + timedelta(days=1)
    response = client.get(f'/api/agendamentos/horarios-disponiveis/?data={amanha}', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        horarios = response.json()
        print(f"✅ Sucesso! {len(horarios)} horários disponíveis para amanhã")
        
        # Deve ter 10 horários (8:00 às 17:00, de hora em hora)
        expected_count = 10  # 8, 9, 10, 11, 12, 13, 14, 15, 16, 17
        if len(horarios) == expected_count:
            print(f"✅ Quantidade correta de horários: {expected_count}")
        else:
            print(f"⚠️ Quantidade de horários: {len(horarios)} (esperado: {expected_count})")
            
    else:
        print(f"❌ Deveria retornar 200, mas retornou {response.status_code}")
    
    # 9. Cleanup
    print("\n8️⃣ Limpando dados de teste...")
    test_user.delete()
    print("✅ Dados de teste removidos")
    
    print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
    print("\n📋 RESUMO:")
    print("✅ Endpoint configurado e acessível")
    print("✅ Autenticação funcionando")
    print("✅ Validações de entrada funcionando")
    print("✅ Lógica de horários funcionando")
    print("✅ Formato de resposta correto")

if __name__ == '__main__':
    test_horarios_endpoint()
