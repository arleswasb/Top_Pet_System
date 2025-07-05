#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from users.models import Profile

def test_pet_creation_detailed():
    """Teste detalhado de criação de pets"""
    client = Client()
    
    # Autenticar como admin
    admin_response = client.post('/api/auth/token/', {
        'username': 'admin',
        'password': 'admin123'
    })
    print(f"Login admin status: {admin_response.status_code}")
    if admin_response.status_code != 200:
        print(f"Erro no login: {admin_response.content}")
        return
    
    admin_token = json.loads(admin_response.content)['token']
    headers = {'HTTP_AUTHORIZATION': f'Token {admin_token}'}
    
    # Obter usuário cliente para usar como tutor
    cliente_user = User.objects.filter(profile__role=Profile.Role.CLIENTE).first()
    if not cliente_user:
        print("Nenhum usuário cliente encontrado")
        return
    
    print(f"Usando cliente como tutor: {cliente_user.id} ({cliente_user.username})")
    
    # Dados do pet - testando diferentes configurações
    test_cases = [
        {
            "name": "Pet sem tutor (admin deve especificar)",
            "data": {
                "nome": "Rex Admin Test 1",
                "especie": "Cão",
                "raca": "Golden Retriever", 
                "observacoes": "Pet criado pelo admin sem tutor"
            }
        },
        {
            "name": "Pet com tutor especificado",
            "data": {
                "nome": "Rex Admin Test 2",
                "especie": "Cão",
                "raca": "Golden Retriever", 
                "observacoes": "Pet criado pelo admin com tutor",
                "tutor": cliente_user.id
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Teste {i}: {test_case['name']}")
        
        response = client.post(
            '/api/pets/',
            data=json.dumps(test_case['data']),
            content_type='application/json',
            **headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.content.decode('utf-8')}")
        
        if response.status_code == 400:
            # Analisar erro de validação
            try:
                error_data = json.loads(response.content)
                print(f"Erros de validação: {error_data}")
            except:
                pass

if __name__ == "__main__":
    test_pet_creation_detailed()
