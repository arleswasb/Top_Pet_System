# teste_api.py

import requests
import json
import os
import sys

# --- CONFIGURAÇÕES E FUNÇÕES AUXILIARES (sem mudanças) ---
BASE_URL = 'http://localhost:8000/api'
ADMIN_USER = (os.environ.get('TEST_ADMIN_USER'), os.environ.get('TEST_ADMIN_PASSWORD'))
CLIENTE_USER = (os.environ.get('TEST_CLIENTE_USER'), os.environ.get('TEST_CLIENTE_PASSWORD'))
FUNCIONARIO_USER = (os.environ.get('TEST_FUNC_USER'), os.environ.get('TEST_FUNC_PASSWORD'))

def get_token(username, password):
    # ... (a função get_token continua exatamente a mesma) ...
    print(f"--- Obtendo token para o usuário: {username} ---")
    if not username or not password:
        print(f"!!! ERRO: Usuário ou senha não definidos para '{username}'.")
        sys.exit(1)
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
        sys.exit(1)

def fail_test(message):
    print(f"\n!!! TESTE FALHOU: {message} !!!")
    sys.exit(1)

# --- TESTES INDIVIDUAIS (NOVO!) ---
def teste_criar_servico(admin_token):
    print("\n--- ✅ [TESTE] Criando um novo Serviço (como Admin) ---")
    headers_admin = {'Authorization': f'Token {admin_token}'}
    servico_data = {"nome": "Vacina V10", "duracao": "00:15:00", "preco": "80.00"}
    response_servico = requests.post(f"{BASE_URL}/agendamentos/servicos/", json=servico_data, headers=headers_admin)
    if response_servico.status_code != 201:
        fail_test(f"Não foi possível criar o serviço. Status: {response_servico.status_code}, Resposta: {response_servico.text}")
    print("--- SUCESSO! ---")

def teste_criar_pet(funcionario_token):
    user_id_cliente3 = 6
    print(f"\n--- ✅ [TESTE] Criando um novo Pet (como Funcionário) para o tutor ID {user_id_cliente3} ---")
    headers_funcionario = {'Authorization': f'Token {funcionario_token}'}
    pet_data = {"nome": "Pipoca", "especie": "Cachorro", "raca": "Shih Tzu", "tutor_id": user_id_cliente3}
    response_pet = requests.post(f"{BASE_URL}/pets/pets/", data=pet_data, headers=headers_funcionario)
    if response_pet.status_code != 201:
        fail_test(f"Funcionário não conseguiu criar o pet. Status: {response_pet.status_code}, Resposta: {response_pet.text}")
    print("--- SUCESSO! ---")


# --- EXECUTOR PRINCIPAL (NOVO!) ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        fail_test("Nenhum teste específico foi fornecido. Ex: 'python teste_api.py criar_servico'")

    # Pega o nome do teste a ser executado do argumento da linha de comando
    test_to_run = sys.argv[1]

    print(f">>> EXECUTANDO TESTE INDIVIDUAL: {test_to_run} <<<")

    # Obtém todos os tokens necessários
    admin_token = get_token(*ADMIN_USER)
    cliente_token = get_token(*CLIENTE_USER)
    funcionario_token = get_token(*FUNCIONARIO_USER)

    # Executa o teste solicitado
    if test_to_run == "criar_servico":
        teste_criar_servico(admin_token)
    elif test_to_run == "criar_pet":
        teste_criar_pet(funcionario_token)
    # Adicione outros testes aqui com 'elif test_to_run == "nome_do_teste":'
    else:
        fail_test(f"O teste '{test_to_run}' não foi encontrado.")

    print(f"\n>>> TESTE '{test_to_run}' CONCLUÍDO COM SUCESSO! <<<")