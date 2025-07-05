#!/usr/bin/env python3
"""
Script de Simulação CRUD - Top Pet System API
Testa todos os endpoints principais com diferentes tipos de usuários
Autor: Desenvolvedor werbert arles
Data: 2025-07-05
"""

import os
import sys
import django
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any, Optional

# Configurar Django ANTES de qualquer import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

# Agora pode importar modelos Django
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status

# Imports dos modelos
from users.models import Profile
from pets.models import Pet
from prontuarios.models import Prontuario
from agendamentos.models import Servico, Agendamento
from configuracao.models import HorarioFuncionamento, Feriado


class Colors:
    """Cores para output no terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class APISimulator:
    """Simulador de CRUD para API do Top Pet System"""
    
    def __init__(self):
        self.client = Client()
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'routes_tested': [],
            'errors': [],
            'timing': {},
            'user_tests': {}
        }
        self.users = {
            'admin': {'token': None, 'user_id': None},
            'veterinario': {'token': None, 'user_id': None},
            'funcionario': {'token': None, 'user_id': None},
            'cliente': {'token': None, 'user_id': None}
        }
        self.created_objects = {
            'users': [],
            'pets': [],
            'prontuarios': [],
            'servicos': [],
            'agendamentos': []
        }
    
    def print_header(self, text: str):
        """Print cabeçalho formatado"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"{text.center(60)}")
        print(f"{'='*60}{Colors.ENDC}\n")
    
    def print_success(self, text: str):
        """Print sucesso"""
        print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")
    
    def print_error(self, text: str):
        """Print erro"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")
    
    def print_info(self, text: str):
        """Print informação"""
        print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")
    
    def print_warning(self, text: str):
        """Print aviso"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")
    
    def log_route_test(self, method: str, endpoint: str, status_code: int, 
                       expected: int, duration: float, user_type: str = 'unknown',
                       data: Optional[Dict] = None):
        """Registra teste de rota"""
        self.results['total_tests'] += 1
        
        route_info = {
            'method': method,
            'endpoint': endpoint,
            'status_code': status_code,
            'expected': expected,
            'success': status_code == expected,
            'duration': round(duration, 3),
            'timestamp': datetime.now().isoformat(),
            'user_type': user_type,
            'data_sent': data
        }
        
        self.results['routes_tested'].append(route_info)
        
        # Registrar por tipo de usuário
        if user_type not in self.results['user_tests']:
            self.results['user_tests'][user_type] = {'passed': 0, 'failed': 0, 'total': 0}
        
        self.results['user_tests'][user_type]['total'] += 1
        
        if status_code == expected:
            self.results['passed'] += 1
            self.results['user_tests'][user_type]['passed'] += 1
            self.print_success(f"[{user_type.upper()}] {method} {endpoint} → {status_code} ({duration:.3f}s)")
        else:
            self.results['failed'] += 1
            self.results['user_tests'][user_type]['failed'] += 1
            self.print_error(f"[{user_type.upper()}] {method} {endpoint} → {status_code} (esperado: {expected}) ({duration:.3f}s)")
            self.results['errors'].append({
                'route': f"{method} {endpoint}",
                'user_type': user_type,
                'error': f"Status {status_code}, esperado {expected}"
            })
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     expected_status: int = 200, user_type: str = 'unknown',
                     headers: Optional[Dict] = None) -> Dict:
        """Faz requisição HTTP e registra resultado"""
        start_time = time.time()
        
        # Headers padrão
        request_headers = {}
        if self.users[user_type]['token']:
            request_headers['HTTP_AUTHORIZATION'] = f'Token {self.users[user_type]["token"]}'
        if headers:
            request_headers.update(headers)
        
        try:
            if method == 'GET':
                response = self.client.get(endpoint, **request_headers)
            elif method == 'POST':
                response = self.client.post(
                    endpoint, 
                    data=json.dumps(data) if data else None,
                    content_type='application/json',
                    **request_headers
                )
            elif method == 'PUT':
                response = self.client.put(
                    endpoint,
                    data=json.dumps(data) if data else None,
                    content_type='application/json',
                    **request_headers
                )
            elif method == 'PATCH':
                response = self.client.patch(
                    endpoint,
                    data=json.dumps(data) if data else None,
                    content_type='application/json',
                    **request_headers
                )
            elif method == 'DELETE':
                response = self.client.delete(endpoint, **request_headers)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            duration = time.time() - start_time
            self.log_route_test(method, endpoint, response.status_code, expected_status, duration, user_type, data)
            
            # Tentar parsear JSON
            try:
                response_data = json.loads(response.content.decode('utf-8')) if response.content else {}
            except json.JSONDecodeError:
                response_data = {'raw_content': response.content.decode('utf-8')}
            
            return {
                'status_code': response.status_code,
                'data': response_data,
                'success': response.status_code == expected_status
            }
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_route_test(method, endpoint, 0, expected_status, duration, user_type, data)
            self.results['errors'].append({
                'route': f"{method} {endpoint}",
                'user_type': user_type,
                'error': str(e)
            })
            return {
                'status_code': 0,
                'data': {'error': str(e)},
                'success': False
            }
    
    def setup_authentication(self):
        """Configura autenticação para todos os tipos de usuários"""
        self.print_header("SETUP - Autenticação para Diferentes Usuários")
        
        # Credenciais dos usuários já criados
        user_credentials = {
            'admin': {'username': 'admin', 'password': 'admin123'},
            'veterinario': {'username': 'dr_silva', 'password': 'vet123'},
            'funcionario': {'username': 'maria_func', 'password': 'func123'},
            'cliente': {'username': 'joao_cliente', 'password': 'cliente123'}
        }
        
        success_count = 0
        
        for user_type, credentials in user_credentials.items():
            self.print_info(f"Autenticando usuário: {user_type}")
            
            # Login
            login_data = {
                'username': credentials['username'],
                'password': credentials['password']
            }
            
            response = self.make_request(
                'POST',
                '/api/auth/token/',
                login_data,
                expected_status=200,
                user_type=user_type
            )
            
            if response['success']:
                self.users[user_type]['token'] = response['data'].get('token')
                # Obter ID do usuário
                user_profile_response = self.make_request(
                    'GET',
                    '/api/users/profile/',
                    expected_status=200,
                    user_type=user_type
                )
                if user_profile_response['success']:
                    self.users[user_type]['user_id'] = user_profile_response['data'].get('id')
                
                self.print_success(f"Token obtido para {user_type}: {self.users[user_type]['token'][:20]}...")
                success_count += 1
            else:
                self.print_error(f"Falha na autenticação para {user_type}")
        
        return success_count == len(user_credentials)
    
    def test_system_endpoints(self):
        """Testa endpoints do sistema"""
        self.print_header("TESTE - Endpoints do Sistema")
        
        # Testar com usuário anônimo (sem autenticação)
        old_tokens = {}
        for user_type in self.users:
            old_tokens[user_type] = self.users[user_type]['token']
            self.users[user_type]['token'] = None
        
        # GET - Status do sistema (público)
        self.make_request('GET', '/api/', expected_status=200, user_type='anonimo')
        
        # GET - Documentação (público)
        self.make_request('GET', '/api/docs/', expected_status=200, user_type='anonimo')
        
        # GET - Schema OpenAPI (público)
        self.make_request('GET', '/api/schema/', expected_status=200, user_type='anonimo')
        
        # Restaurar tokens
        for user_type in self.users:
            self.users[user_type]['token'] = old_tokens[user_type]
    
    def test_users_crud_by_role(self):
        """Testa CRUD de usuários por diferentes perfis"""
        self.print_header("TESTE CRUD - Usuários por Perfil")
        
        # Admin pode listar todos os usuários
        self.make_request('GET', '/api/users/', expected_status=200, user_type='admin')
        
        # Funcionário pode listar usuários
        self.make_request('GET', '/api/users/', expected_status=200, user_type='funcionario')
        
        # Cliente só pode ver seu próprio perfil
        self.make_request('GET', '/api/users/', expected_status=200, user_type='cliente')
        
        # Veterinário pode ver usuários relacionados
        self.make_request('GET', '/api/users/', expected_status=200, user_type='veterinario')
        
        # Teste de perfil próprio
        for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
            self.make_request('GET', '/api/users/profile/', expected_status=200, user_type=user_type)
            
            # Atualização do próprio perfil
            update_data = {
                'first_name': f'{user_type.title()} Atualizado',
                'last_name': 'Via API'
            }
            self.make_request('PATCH', '/api/users/profile/', update_data, expected_status=200, user_type=user_type)
    
    def test_pets_crud_by_role(self):
        """Testa CRUD de pets por diferentes perfis"""
        self.print_header("TESTE CRUD - Pets por Perfil")
        
        # Dados do pet para teste
        pet_data = {
            'nome': 'Rex Teste',
            'especie': 'Cachorro',
            'raca': 'Labrador',
            'idade': 3,
            'peso': 25.5,
            'cor': 'Dourado',
            'observacoes': 'Pet muito dócil e brincalhão'
        }
        
        # Cliente pode criar pet
        response = self.make_request('POST', '/api/pets/', pet_data, expected_status=201, user_type='cliente')
        pet_id = None
        if response['success']:
            pet_id = response['data'].get('id')
            self.created_objects['pets'].append(pet_id)
        
        # Admin pode criar pet
        admin_pet_data = pet_data.copy()
        admin_pet_data['nome'] = 'Rex Admin'
        response = self.make_request('POST', '/api/pets/', admin_pet_data, expected_status=201, user_type='admin')
        if response['success']:
            admin_pet_id = response['data'].get('id')
            self.created_objects['pets'].append(admin_pet_id)
        
        # Funcionário pode criar pet
        func_pet_data = pet_data.copy()
        func_pet_data['nome'] = 'Rex Funcionário'
        response = self.make_request('POST', '/api/pets/', func_pet_data, expected_status=201, user_type='funcionario')
        if response['success']:
            func_pet_id = response['data'].get('id')
            self.created_objects['pets'].append(func_pet_id)
        
        # Veterinário pode criar pet
        vet_pet_data = pet_data.copy()
        vet_pet_data['nome'] = 'Rex Veterinário'
        response = self.make_request('POST', '/api/pets/', vet_pet_data, expected_status=201, user_type='veterinario')
        if response['success']:
            vet_pet_id = response['data'].get('id')
            self.created_objects['pets'].append(vet_pet_id)
        
        # Todos podem listar pets
        for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
            self.make_request('GET', '/api/pets/', expected_status=200, user_type=user_type)
        
        # Teste de detalhes e atualização
        if pet_id:
            for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
                # Ver detalhes
                self.make_request('GET', f'/api/pets/{pet_id}/', expected_status=200, user_type=user_type)
                
                # Atualizar (pode variar por permissão)
                update_data = {'peso': 26.0}
                expected_status = 200  # Assumindo que todos podem atualizar, mas pode ser 403 para alguns
                self.make_request('PATCH', f'/api/pets/{pet_id}/', update_data, expected_status=expected_status, user_type=user_type)
    
    def test_servicos_crud_by_role(self):
        """Testa CRUD de serviços por diferentes perfis"""
        self.print_header("TESTE CRUD - Serviços por Perfil")
        
        # Dados do serviço
        servico_data = {
            'nome': 'Consulta Veterinária Teste',
            'descricao': 'Consulta geral com veterinário',
            'preco': '150.00',
            'duracao_minutos': 60,
            'ativo': True
        }
        
        # Admin pode criar serviço
        response = self.make_request('POST', '/api/agendamentos/servicos/', servico_data, expected_status=201, user_type='admin')
        servico_id = None
        if response['success']:
            servico_id = response['data'].get('id')
            self.created_objects['servicos'].append(servico_id)
        
        # Funcionário pode criar serviço (dependendo das permissões)
        func_servico_data = servico_data.copy()
        func_servico_data['nome'] = 'Banho e Tosa'
        expected_status = 201  # Pode ser 403 dependendo das permissões
        response = self.make_request('POST', '/api/agendamentos/servicos/', func_servico_data, expected_status, user_type='funcionario')
        if response['success']:
            func_servico_id = response['data'].get('id')
            self.created_objects['servicos'].append(func_servico_id)
        
        # Veterinário pode tentar criar serviço
        vet_servico_data = servico_data.copy()
        vet_servico_data['nome'] = 'Cirurgia'
        expected_status = 201  # Pode ser 403 dependendo das permissões
        response = self.make_request('POST', '/api/agendamentos/servicos/', vet_servico_data, expected_status, user_type='veterinario')
        if response['success']:
            vet_servico_id = response['data'].get('id')
            self.created_objects['servicos'].append(vet_servico_id)
        
        # Cliente não deve conseguir criar serviço
        self.make_request('POST', '/api/agendamentos/servicos/', servico_data, expected_status=403, user_type='cliente')
        
        # Todos podem listar serviços
        for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
            self.make_request('GET', '/api/agendamentos/servicos/', expected_status=200, user_type=user_type)
        
        # Teste de atualização se o serviço foi criado
        if servico_id:
            update_data = {'preco': '180.00'}
            
            # Admin pode atualizar
            self.make_request('PATCH', f'/api/agendamentos/servicos/{servico_id}/', update_data, expected_status=200, user_type='admin')
            
            # Outros podem ou não poder atualizar
            for user_type in ['veterinario', 'funcionario']:
                expected_status = 200  # Pode ser 403 dependendo das permissões
                self.make_request('PATCH', f'/api/agendamentos/servicos/{servico_id}/', update_data, expected_status, user_type=user_type)
            
            # Cliente não pode atualizar
            self.make_request('PATCH', f'/api/agendamentos/servicos/{servico_id}/', update_data, expected_status=403, user_type='cliente')
    
    def test_prontuarios_crud_by_role(self):
        """Testa CRUD de prontuários por diferentes perfis"""
        self.print_header("TESTE CRUD - Prontuários por Perfil")
        
        if not self.created_objects['pets']:
            self.print_warning("Nenhum pet disponível para criar prontuário")
            return
        
        pet_id = self.created_objects['pets'][0]
        
        # Dados do prontuário
        prontuario_data = {
            'pet': pet_id,
            'data_consulta': datetime.now().date().isoformat(),
            'sintomas': 'Animal apresentando letargia e falta de apetite',
            'diagnostico': 'Possível infecção gastrointestinal',
            'tratamento': 'Antibiótico por 7 dias + dieta leve',
            'observacoes': 'Retorno em 1 semana para avaliação',
            'peso_atual': 25.8,
            'temperatura': 38.5
        }
        
        # Veterinário pode criar prontuário
        response = self.make_request('POST', '/api/prontuarios/', prontuario_data, expected_status=201, user_type='veterinario')
        prontuario_id = None
        if response['success']:
            prontuario_id = response['data'].get('id')
            self.created_objects['prontuarios'].append(prontuario_id)
        
        # Admin pode criar prontuário
        admin_prontuario = prontuario_data.copy()
        admin_prontuario['observacoes'] = 'Prontuário criado por admin'
        response = self.make_request('POST', '/api/prontuarios/', admin_prontuario, expected_status=201, user_type='admin')
        if response['success']:
            admin_prontuario_id = response['data'].get('id')
            self.created_objects['prontuarios'].append(admin_prontuario_id)
        
        # Funcionário pode ou não criar prontuário (dependendo das regras)
        expected_status = 201  # Pode ser 403
        self.make_request('POST', '/api/prontuarios/', prontuario_data, expected_status, user_type='funcionario')
        
        # Cliente não pode criar prontuário
        self.make_request('POST', '/api/prontuarios/', prontuario_data, expected_status=403, user_type='cliente')
        
        # Teste de listagem
        for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
            self.make_request('GET', '/api/prontuarios/', expected_status=200, user_type=user_type)
        
        # Prontuários por pet
        for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
            self.make_request('GET', f'/api/pets/{pet_id}/prontuarios/', expected_status=200, user_type=user_type)
        
        # Teste de atualização se prontuário foi criado
        if prontuario_id:
            update_data = {'temperatura': 37.8}
            
            # Veterinário pode atualizar
            self.make_request('PATCH', f'/api/prontuarios/{prontuario_id}/', update_data, expected_status=200, user_type='veterinario')
            
            # Admin pode atualizar
            self.make_request('PATCH', f'/api/prontuarios/{prontuario_id}/', update_data, expected_status=200, user_type='admin')
            
            # Cliente não pode atualizar
            self.make_request('PATCH', f'/api/prontuarios/{prontuario_id}/', update_data, expected_status=403, user_type='cliente')
    
    def test_agendamentos_crud_by_role(self):
        """Testa CRUD de agendamentos por diferentes perfis"""
        self.print_header("TESTE CRUD - Agendamentos por Perfil")
        
        if not self.created_objects['pets'] or not self.created_objects['servicos']:
            self.print_warning("Pets ou serviços não disponíveis para agendamento")
            return
        
        pet_id = self.created_objects['pets'][0]
        servico_id = self.created_objects['servicos'][0]
        
        # Primeiro, testar consulta de horários disponíveis
        tomorrow = (datetime.now() + timedelta(days=1)).date().isoformat()
        for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
            self.make_request('GET', f'/api/agendamentos/horarios-disponiveis/?data={tomorrow}', expected_status=200, user_type=user_type)
        
        # Dados do agendamento
        agendamento_data = {
            'pet': pet_id,
            'servico': servico_id,
            'data_agendamento': tomorrow,
            'horario': '14:00:00',
            'observacoes': 'Agendamento teste via API'
        }
        
        # Cliente pode criar agendamento
        response = self.make_request('POST', '/api/agendamentos/', agendamento_data, expected_status=201, user_type='cliente')
        agendamento_id = None
        if response['success']:
            agendamento_id = response['data'].get('id')
            self.created_objects['agendamentos'].append(agendamento_id)
        
        # Funcionário pode criar agendamento
        func_agendamento = agendamento_data.copy()
        func_agendamento['horario'] = '15:00:00'
        response = self.make_request('POST', '/api/agendamentos/', func_agendamento, expected_status=201, user_type='funcionario')
        if response['success']:
            func_agendamento_id = response['data'].get('id')
            self.created_objects['agendamentos'].append(func_agendamento_id)
        
        # Admin pode criar agendamento
        admin_agendamento = agendamento_data.copy()
        admin_agendamento['horario'] = '16:00:00'
        response = self.make_request('POST', '/api/agendamentos/', admin_agendamento, expected_status=201, user_type='admin')
        if response['success']:
            admin_agendamento_id = response['data'].get('id')
            self.created_objects['agendamentos'].append(admin_agendamento_id)
        
        # Veterinário pode criar agendamento
        vet_agendamento = agendamento_data.copy()
        vet_agendamento['horario'] = '17:00:00'
        response = self.make_request('POST', '/api/agendamentos/', vet_agendamento, expected_status=201, user_type='veterinario')
        if response['success']:
            vet_agendamento_id = response['data'].get('id')
            self.created_objects['agendamentos'].append(vet_agendamento_id)
        
        # Teste de listagem
        for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
            self.make_request('GET', '/api/agendamentos/', expected_status=200, user_type=user_type)
        
        # Agendamentos por data
        for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
            self.make_request('GET', f'/api/agendamentos/?data={tomorrow}', expected_status=200, user_type=user_type)
        
        # Teste de atualização se agendamento foi criado
        if agendamento_id:
            update_data = {'status': 'confirmado'}
            
            # Diferentes usuários tentam atualizar
            for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
                expected_status = 200  # Pode variar dependendo das regras de negócio
                self.make_request('PATCH', f'/api/agendamentos/{agendamento_id}/', update_data, expected_status, user_type=user_type)
    
    def test_configuration_endpoints_by_role(self):
        """Testa endpoints de configuração por diferentes perfis"""
        self.print_header("TESTE - Configurações por Perfil")
        
        # Teste de visualização de configurações
        for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
            # Horários de funcionamento
            self.make_request('GET', '/api/configuracao/horarios/', expected_status=200, user_type=user_type)
            
            # Feriados
            self.make_request('GET', '/api/configuracao/feriados/', expected_status=200, user_type=user_type)
        
        # Criação de configurações (apenas admin e funcionário devem conseguir)
        horario_data = {
            'dia_semana': 1,  # Segunda-feira
            'hora_abertura': '08:00:00',
            'hora_fechamento': '18:00:00',
            'ativo': True
        }
        
        # Admin pode criar
        self.make_request('POST', '/api/configuracao/horarios/', horario_data, expected_status=201, user_type='admin')
        
        # Funcionário pode ou não criar (dependendo das regras)
        expected_status = 201  # Pode ser 403
        self.make_request('POST', '/api/configuracao/horarios/', horario_data, expected_status, user_type='funcionario')
        
        # Veterinário e cliente não podem criar
        self.make_request('POST', '/api/configuracao/horarios/', horario_data, expected_status=403, user_type='veterinario')
        self.make_request('POST', '/api/configuracao/horarios/', horario_data, expected_status=403, user_type='cliente')
        
        # Feriado
        feriado_data = {
            'nome': 'Dia do Teste',
            'data': (datetime.now() + timedelta(days=30)).date().isoformat(),
            'ativo': True
        }
        
        # Admin pode criar
        self.make_request('POST', '/api/configuracao/feriados/', feriado_data, expected_status=201, user_type='admin')
        
        # Outros não podem
        for user_type in ['veterinario', 'funcionario', 'cliente']:
            expected_status = 403  # Apenas admin pode criar feriados
            self.make_request('POST', '/api/configuracao/feriados/', feriado_data, expected_status, user_type=user_type)
    
    def cleanup_created_objects(self):
        """Remove objetos criados durante os testes"""
        self.print_header("CLEANUP - Removendo objetos de teste")
        
        # Usar admin para cleanup (tem todas as permissões)
        user_type = 'admin'
        
        # Deletar agendamentos
        for agendamento_id in self.created_objects['agendamentos']:
            self.make_request('DELETE', f'/api/agendamentos/{agendamento_id}/', expected_status=204, user_type=user_type)
        
        # Deletar prontuários
        for prontuario_id in self.created_objects['prontuarios']:
            self.make_request('DELETE', f'/api/prontuarios/{prontuario_id}/', expected_status=204, user_type=user_type)
        
        # Deletar pets
        for pet_id in self.created_objects['pets']:
            self.make_request('DELETE', f'/api/pets/{pet_id}/', expected_status=204, user_type=user_type)
        
        # Deletar serviços
        for servico_id in self.created_objects['servicos']:
            self.make_request('DELETE', f'/api/agendamentos/servicos/{servico_id}/', expected_status=204, user_type=user_type)
    
    def generate_report(self):
        """Gera relatório final dos testes"""
        self.print_header("RELATÓRIO FINAL DOS TESTES")
        
        # Resumo geral
        print(f"{Colors.BOLD}📊 RESUMO GERAL:{Colors.ENDC}")
        print(f"   Total de rotas testadas: {self.results['total_tests']}")
        print(f"   {Colors.OKGREEN}✓ Sucessos: {self.results['passed']}{Colors.ENDC}")
        print(f"   {Colors.FAIL}✗ Falhas: {self.results['failed']}{Colors.ENDC}")
        
        if self.results['total_tests'] > 0:
            success_rate = (self.results['passed'] / self.results['total_tests']) * 100
            print(f"   Taxa de sucesso: {success_rate:.1f}%")
        
        # Resumo por tipo de usuário
        print(f"\n{Colors.BOLD}👥 RESUMO POR TIPO DE USUÁRIO:{Colors.ENDC}")
        for user_type, stats in self.results['user_tests'].items():
            if stats['total'] > 0:
                success_rate = (stats['passed'] / stats['total']) * 100
                print(f"   {user_type.upper():12}: {stats['passed']:3}/{stats['total']:3} ({success_rate:5.1f}%)")
        
        # Rotas testadas por método
        methods = defaultdict(int)
        for route in self.results['routes_tested']:
            methods[route['method']] += 1
        
        print(f"\n{Colors.BOLD}🔄 MÉTODOS HTTP TESTADOS:{Colors.ENDC}")
        for method, count in sorted(methods.items()):
            print(f"   {method}: {count} rotas")
        
        # Endpoints testados
        print(f"\n{Colors.BOLD}🛤️  ENDPOINTS TESTADOS:{Colors.ENDC}")
        endpoints = set()
        for route in self.results['routes_tested']:
            endpoint_base = route['endpoint'].split('?')[0]  # Remove query params
            endpoint_base = '/'.join(endpoint_base.split('/')[:3])  # Agrupa por base
            endpoints.add(endpoint_base)
        
        for endpoint in sorted(endpoints):
            print(f"   {endpoint}")
        
        # Erros encontrados por tipo de usuário
        if self.results['errors']:
            print(f"\n{Colors.BOLD}{Colors.FAIL}❌ ERROS ENCONTRADOS:{Colors.ENDC}")
            error_by_user = defaultdict(list)
            for error in self.results['errors']:
                error_by_user[error['user_type']].append(error)
            
            for user_type, errors in error_by_user.items():
                print(f"\n   {Colors.WARNING}{user_type.upper()}:{Colors.ENDC}")
                for i, error in enumerate(errors, 1):
                    print(f"      {i}. {error['route']}: {error['error']}")
        
        # Estatísticas de tempo
        durations = [route['duration'] for route in self.results['routes_tested']]
        if durations:
            print(f"\n{Colors.BOLD}⏱️  PERFORMANCE:{Colors.ENDC}")
            print(f"   Tempo total: {sum(durations):.3f}s")
            print(f"   Tempo médio por rota: {sum(durations)/len(durations):.3f}s")
            print(f"   Rota mais rápida: {min(durations):.3f}s")
            print(f"   Rota mais lenta: {max(durations):.3f}s")
        
        print(f"\n{Colors.BOLD}📄 Relatório salvo em: api_test_report.json{Colors.ENDC}")
        
        # Salvar relatório em JSON
        with open('api_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
    
    def run_full_simulation(self):
        """Executa simulação completa"""
        start_time = time.time()
        
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("🚀 TOP PET SYSTEM - SIMULAÇÃO CRUD API COM MÚLTIPLOS USUÁRIOS")
        print("==============================================================")
        print(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Colors.ENDC}")
        
        try:
            # Setup
            if not self.setup_authentication():
                self.print_error("Falha na autenticação. Abortando simulação.")
                return False
            
            # Testes por funcionalidade e perfil de usuário
            self.test_system_endpoints()
            self.test_users_crud_by_role()
            self.test_pets_crud_by_role()
            self.test_servicos_crud_by_role()
            self.test_prontuarios_crud_by_role()
            self.test_agendamentos_crud_by_role()
            self.test_configuration_endpoints_by_role()
            
            # Cleanup
            self.cleanup_created_objects()
            
            # Relatório
            total_time = time.time() - start_time
            self.results['total_duration'] = round(total_time, 3)
            self.generate_report()
            
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}✅ Simulação concluída com sucesso!")
            print(f"⏱️  Tempo total: {total_time:.3f}s{Colors.ENDC}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Erro durante simulação: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Função principal"""
    simulator = APISimulator()
    success = simulator.run_full_simulation()
    
    if success:
        print(f"\n{Colors.OKCYAN}💡 Para analisar os resultados detalhados:")
        print(f"   cat api_test_report.json | python -m json.tool{Colors.ENDC}")
        print(f"\n{Colors.OKCYAN}💡 Para analisar o relatório:")
        print(f"   python analyze_test_report.py{Colors.ENDC}")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
