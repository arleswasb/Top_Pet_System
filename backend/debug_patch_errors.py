#!/usr/bin/env python3
"""
Script para debugar os erros de PATCH nos prontuários e agendamentos para veterinário.
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from users.models import User, Profile
from pets.models import Pet
from agendamentos.models import Agendamento, Servico
from prontuarios.models import Prontuario

def get_auth_token(username):
    """Obter token de autenticação"""
    url = "http://localhost:8000/api/auth/token/"
    data = {"username": username, "password": "123456"}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            token = response.json().get('access')
            return token
        else:
            print(f"Erro ao obter token para {username}: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Erro de conexão ao obter token: {e}")
        return None

def test_patch_prontuario():
    """Testar PATCH de prontuário pelo veterinário"""
    print("=== TESTE PATCH PRONTUÁRIO ===")
    
    # Obter token do veterinário
    vet_token = get_auth_token("veterinario")
    if not vet_token:
        print("Não foi possível obter token do veterinário")
        return
    
    headers = {"Authorization": f"Bearer {vet_token}"}
    
    # Listar prontuários existentes
    list_url = "http://localhost:8000/api/prontuarios/"
    try:
        response = requests.get(list_url, headers=headers)
        print(f"Lista de prontuários - Status: {response.status_code}")
        
        if response.status_code == 200:
            prontuarios = response.json()
            print(f"Total de prontuários: {len(prontuarios)}")
            
            if prontuarios:
                # Tentar PATCH no primeiro prontuário
                prontuario_id = prontuarios[0]['id']
                print(f"Tentando PATCH no prontuário ID: {prontuario_id}")
                
                patch_url = f"http://localhost:8000/api/prontuarios/{prontuario_id}/"
                patch_data = {"temperatura": "37.8"}
                
                patch_response = requests.patch(patch_url, json=patch_data, headers=headers)
                print(f"PATCH prontuário - Status: {patch_response.status_code}")
                
                if patch_response.status_code != 200:
                    print("Erro no PATCH:")
                    print(patch_response.text)
                else:
                    print("PATCH realizado com sucesso!")
            else:
                print("Nenhum prontuário disponível para teste")
        else:
            print(f"Erro ao listar prontuários: {response.text}")
    except Exception as e:
        print(f"Erro ao testar prontuário: {e}")

def test_patch_agendamento():
    """Testar PATCH de agendamento pelo veterinário"""
    print("\n=== TESTE PATCH AGENDAMENTO ===")
    
    # Obter token do veterinário
    vet_token = get_auth_token("veterinario")
    if not vet_token:
        print("Não foi possível obter token do veterinário")
        return
    
    headers = {"Authorization": f"Bearer {vet_token}"}
    
    # Listar agendamentos existentes
    list_url = "http://localhost:8000/api/agendamentos/"
    try:
        response = requests.get(list_url, headers=headers)
        print(f"Lista de agendamentos - Status: {response.status_code}")
        
        if response.status_code == 200:
            agendamentos = response.json()
            print(f"Total de agendamentos: {len(agendamentos)}")
            
            if agendamentos:
                # Tentar PATCH no primeiro agendamento
                agendamento_id = agendamentos[0]['ID']
                print(f"Tentando PATCH no agendamento ID: {agendamento_id}")
                
                patch_url = f"http://localhost:8000/api/agendamentos/{agendamento_id}/"
                patch_data = {"status": "CONCLUIDO"}
                
                patch_response = requests.patch(patch_url, json=patch_data, headers=headers)
                print(f"PATCH agendamento - Status: {patch_response.status_code}")
                
                if patch_response.status_code != 200:
                    print("Erro no PATCH:")
                    print(patch_response.text)
                else:
                    print("PATCH realizado com sucesso!")
            else:
                print("Nenhum agendamento disponível para teste")
        else:
            print(f"Erro ao listar agendamentos: {response.text}")
    except Exception as e:
        print(f"Erro ao testar agendamento: {e}")

def check_database_objects():
    """Verificar objetos no banco de dados"""
    print("\n=== VERIFICAÇÃO DO BANCO ===")
    
    # Verificar usuários
    users = User.objects.all()
    print(f"Total de usuários: {users.count()}")
    
    # Verificar prontuários
    prontuarios = Prontuario.objects.all()
    print(f"Total de prontuários: {prontuarios.count()}")
    for p in prontuarios:
        print(f"  - Prontuário ID {p.id}: Pet {p.pet.nome} | Vet {p.veterinario.username}")
    
    # Verificar agendamentos
    agendamentos = Agendamento.objects.all()
    print(f"Total de agendamentos: {agendamentos.count()}")
    for a in agendamentos:
        print(f"  - Agendamento ID {a.id}: Pet {a.pet.nome} | Status {a.status}")

def test_admin_configs():
    """Testar problemas de configuração do admin"""
    print("\n=== TESTE CONFIGURAÇÕES ADMIN ===")
    
    # Obter token do admin
    admin_token = get_auth_token("admin")
    if not admin_token:
        print("Não foi possível obter token do admin")
        return
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Testar horário de funcionamento
    print("Testando criação de horário de funcionamento...")
    horario_url = "http://localhost:8000/api/configuracao/horarios-funcionamento/"
    
    # Primeiro, listar horários existentes
    response = requests.get(horario_url, headers=headers)
    print(f"Horários existentes - Status: {response.status_code}")
    if response.status_code == 200:
        horarios = response.json()
        print(f"Total de horários: {len(horarios)}")
        for h in horarios:
            print(f"  - Dia {h.get('dia_semana')}: {h.get('hora_abertura')} - {h.get('hora_fechamento')}")
    
    # Tentar criar novo horário
    horario_data = {
        'dia_semana': 1,  # Terça-feira
        'hora_abertura': '09:00:00',
        'hora_fechamento': '17:00:00',
        'ativo': True
    }
    
    response = requests.post(horario_url, json=horario_data, headers=headers)
    print(f"Criação de horário - Status: {response.status_code}")
    if response.status_code != 201:
        print("Erro na criação de horário:")
        print(response.text)
    
    # Testar feriado
    print("\nTestando criação de feriado...")
    feriado_url = "http://localhost:8000/api/configuracao/feriados/"
    
    # Primeiro, listar feriados existentes
    response = requests.get(feriado_url, headers=headers)
    print(f"Feriados existentes - Status: {response.status_code}")
    if response.status_code == 200:
        feriados = response.json()
        print(f"Total de feriados: {len(feriados)}")
        for f in feriados:
            print(f"  - {f.get('nome')}: {f.get('data')}")
    
    # Tentar criar novo feriado
    feriado_data = {
        'nome': 'Teste Debug',
        'data': (datetime.now() + timedelta(days=120)).date().isoformat(),
        'recorrente': False,
        'ativo': True
    }
    
    response = requests.post(feriado_url, json=feriado_data, headers=headers)
    print(f"Criação de feriado - Status: {response.status_code}")
    if response.status_code != 201:
        print("Erro na criação de feriado:")
        print(response.text)

if __name__ == "__main__":
    print("🔍 DEBUGGING DOS ERROS DE PATCH")
    print("=" * 50)
    
    check_database_objects()
    test_patch_prontuario()
    test_patch_agendamento()
    test_admin_configs()
    
    print("\n✅ Debug concluído!")
