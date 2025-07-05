#!/usr/bin/env python
import os
import django
import json
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

# Dados de teste para admin
AUTH_USERS = {
    'admin': {'username': 'admin', 'password': 'admin123'},
    'funcionario': {'username': 'funcionario', 'password': 'func123'},
}

BASE_URL = "http://127.0.0.1:8000/api"

def get_token(username, password):
    """Obter token de autenticação"""
    response = requests.post(f"{BASE_URL}/auth/token/", {
        'username': username,
        'password': password
    })
    if response.status_code == 200:
        return response.json()['token']  # Corrigido para 'token'
    else:
        print(f"Erro na autenticação: {response.status_code}")
        print(response.text)
        return None

def test_pet_creation():
    """Testar criação de pets com diferentes usuários"""
    
    # Obter token do admin
    admin_token = get_token('admin', 'admin123')
    if not admin_token:
        print("Falha ao obter token do admin")
        return
    
    headers = {'Authorization': f'Token {admin_token}'}
    
    # Obter lista de usuários para escolher um tutor
    users_response = requests.get(f"{BASE_URL}/users/", headers=headers)
    if users_response.status_code == 200:
        users = users_response.json()
        cliente_user = None
        for user in users['results'] if 'results' in users else users:
            if user.get('profile', {}).get('role') == 'CLIENTE':
                cliente_user = user
                break
        
        if not cliente_user:
            print("Nenhum usuário cliente encontrado")
            return
        
        # Dados do pet para admin
        pet_data = {
            "nome": "Rex Admin Test",
            "especie": "Cão",
            "raca": "Golden Retriever", 
            "data_de_nascimento": "2020-05-15",
            "sexo": "MACHO",
            "observacoes": "Pet criado pelo admin",
            "tutor": cliente_user['id']  # Admin deve especificar tutor
        }
        
        print(f"Testando criação de pet pelo admin com dados:")
        print(json.dumps(pet_data, indent=2))
        
        response = requests.post(f"{BASE_URL}/pets/", data=pet_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code != 201:
            print("❌ Erro na criação pelo admin")
        else:
            print("✅ Pet criado com sucesso pelo admin")
    else:
        print(f"Erro ao obter lista de usuários: {users_response.status_code}")
        print(users_response.text)

if __name__ == "__main__":
    print("🧪 Testando criação de pets...")
    test_pet_creation()
