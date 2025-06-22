# teste_api.py

import requests
import json
import os
import sys # <-- Importe a biblioteca sys

# URL base da nossa API
BASE_URL = 'http://localhost:8000/api'

# Leia as credenciais das variáveis de ambiente
ADMIN_USER = (os.environ.get('TEST_ADMIN_USER'), os.environ.get('TEST_ADMIN_PASSWORD'))
CLIENTE_USER = (os.environ.get('TEST_CLIENTE_USER'), os.environ.get('TEST_CLIENTE_PASSWORD'))
FUNCIONARIO_USER = (os.environ.get('TEST_FUNC_USER'), os.environ.get('TEST_FUNC_PASSWORD')) # <-- MUDANÇA: Adicionado funcionário

def get_token(username, password):
    # ... (função get_token continua igual) ...
    print(f"--- Obtendo token para o usuário: {username} ---")
    if not username or not password:
        print(f"!!! ERRO: Usuário ou senha não definidos para '{username}'. Verifique os Secrets do GitHub.")
        return None
    try:
        response = requests.post(
            f"{BASE_URL}/users/login/",
            data={'username': username, 'password': password}
        )
        response.raise_for_status()
        token = response.json()['token']
        print(f"Token obtido com sucesso: ...{token[-6:]}")
        return token
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter token para {username}: {e}")
        print("Corpo da resposta:", e.response.text if e.response else "N/A")
        return None

def fail_script(message):
    """Função para imprimir uma mensagem de falha e sair."""
    print(f"\n!!! TESTE FALHOU: {message} !!!")
    sys.exit(1) # Sai do script com um código de erro

# --- INÍCIO DO SCRIPT DE TESTE ---
print(">>> INICIANDO SCRIPT DE TESTE COMPLETO DO TOP PET <<<")

# 1. Obter tokens
admin_token = get_token(*ADMIN_USER)
cliente_token = get_token(*CLIENTE_USER)
funcionario_token = get_token(*FUNCIONARIO_USER) # <-- MUDANÇA: Obter token do funcionário

if not all([admin_token, cliente_token, funcionario_token]):
    fail_script("Falha ao obter um ou mais tokens.")

# ... (Passo 2, criar um serviço, continua igual) ...
print("\n--- [TESTE] Criando um novo Serviço (como Admin) ---")
headers_admin = {'Authorization': f'Token {admin_token}'}
servico_data = {"nome": "Vacina V10", "duracao": "00:15:00", "preco": "80.00"}
response_servico = requests.post(f"{BASE_URL}/agendamentos/servicos/", json=servico_data, headers=headers_admin)
if response_servico.status_code != 201:
    fail_script(f"Não foi possível criar o serviço. Status: {response_servico.status_code}, Resposta: {response_servico.text}")
servico_criado = response_servico.json()
servico_id = servico_criado['id']
print(f"SUCESSO! Serviço '{servico_criado['nome']}' criado com ID: {servico_id}")


# 3. Criar um Pet para o cliente3 (como FUNCIONÁRIO) <-- MUDANÇA
user_id_cliente3 = 6 
print(f"\n--- [TESTE] Criando um novo Pet (como Funcionário) para o tutor ID {user_id_cliente3} ---")
headers_funcionario = {'Authorization': f'Token {funcionario_token}'}
pet_data = {"nome": "Pipoca", "especie": "Cachorro", "raca": "Shih Tzu", "tutor_id": user_id_cliente3}
response_pet = requests.post(f"{BASE_URL}/pets/pets/", data=pet_data, headers=headers_funcionario)
if response_pet.status_code != 201:
    fail_script(f"Funcionário não conseguiu criar o pet. Status: {response_pet.status_code}, Resposta: {response_pet.text}")
pet_criado = response_pet.json()
pet_id = pet_criado['id']
print(f"SUCESSO! Pet '{pet_criado['nome']}' criado com ID: {pet_id}")


# 4. TESTE NEGATIVO: Funcionário TENTA apagar o Pet <-- NOVO TESTE
print(f"\n--- [TESTE NEGATIVO] Funcionário tentando apagar o pet ID {pet_id} ---")
response_delete_fail = requests.delete(f"{BASE_URL}/pets/pets/{pet_id}/", headers=headers_funcionario)
if response_delete_fail.status_code == 403:
    print("SUCESSO! O funcionário foi corretamente PROIBIDO de apagar o pet (Status 403).")
else:
    fail_script(f"A permissão falhou! O funcionário conseguiu apagar o pet ou recebeu um erro inesperado. Status: {response_delete_fail.status_code}")


# 5. Criar um Agendamento (como Cliente)
# ... (este passo continua igual) ...
print(f"\n--- [TESTE] Criando um novo Agendamento (como Cliente) para o pet ID {pet_id} ---")
headers_cliente = {'Authorization': f'Token {cliente_token}'}
agendamento_data = {"pet_id": pet_id, "servico_id": servico_id, "data_hora": "2025-07-10T14:00:00-03:00"}
response_agendamento = requests.post(f"{BASE_URL}/agendamentos/agendamentos/", json=agendamento_data, headers=headers_cliente)
if response_agendamento.status_code != 201:
    fail_script(f"Cliente não conseguiu criar o agendamento. Status: {response_agendamento.status_code}, Resposta: {response_agendamento.text}")
agendamento_criado = response_agendamento.json()
print(f"SUCESSO! Agendamento criado com ID: {agendamento_criado['id']}")
print(json.dumps(agendamento_criado, indent=4, ensure_ascii=False))


print("\n>>> SCRIPT DE TESTE COMPLETO CONCLUÍDO COM SUCESSO! <<<")