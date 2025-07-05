#!/usr/bin/env python3
"""
Script de Simulação CRUD Multi-Usuário - Top Pet System API
Testa todos os endpoints com diferentes perfis de usuário para validar regras de negócio
Autor: Desenvolvedor Senior
Data: 2025-07-04
"""

import os
import sys
import django
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any, Optional

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

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


class MultiUserAPISimulator:
    """Simulador de CRUD com múltiplos usuários para API do Top Pet System"""
    
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
        
        # Definir usuários de teste com diferentes perfis
        self.test_users = {
            'admin': {
                'username': 'admin_teste',
                'password': 'admin123',
                'role': 'Admin',
                'token': None,
                'user_id': None,
                'expected_permissions': ['all']
            },
            'veterinario': {
                'username': 'veterinario_teste',
                'password': 'vet123',
                'role': 'Veterinario',
                'token': None,
                'user_id': None,
                'expected_permissions': ['view_pets', 'create_prontuarios', 'view_agendamentos']
            },
            'funcionario': {
                'username': 'funcionario_teste',
                'password': 'func123',
                'role': 'Funcionario',
                'token': None,
                'user_id': None,
                'expected_permissions': ['view_pets', 'create_agendamentos', 'view_agendamentos']
            },
            'cliente': {
                'username': 'cliente_teste',
                'password': 'cliente123',
                'role': 'Cliente',
                'token': None,
                'user_id': None,
                'expected_permissions': ['view_own_pets', 'create_own_pets', 'view_own_agendamentos']
            }
        }
        
        self.current_user = None
        self.created_objects = {
            'pets': [],
            'prontuarios': [],
            'servicos': [],
            'agendamentos': [],
            'horarios': [],
            'feriados': []
        }
    
    def print_header(self, text: str):
        """Print cabeçalho formatado"""
        print(f"\n{Colors.HEADER}{'='*70}")
        print(f"{text.center(70)}")
        print(f"{'='*70}{Colors.ENDC}\n")
    
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
                       expected: int, duration: float, user_role: str, data: Optional[Dict] = None):
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
            'user_role': user_role,
            'data_sent': data
        }
        
        self.results['routes_tested'].append(route_info)
        
        # Registrar por usuário
        if user_role not in self.results['user_tests']:
            self.results['user_tests'][user_role] = {'passed': 0, 'failed': 0, 'tests': []}
        
        self.results['user_tests'][user_role]['tests'].append(route_info)
        
        if status_code == expected:
            self.results['passed'] += 1
            self.results['user_tests'][user_role]['passed'] += 1
            self.print_success(f"[{user_role}] {method} {endpoint} → {status_code} ({duration:.3f}s)")
        else:
            self.results['failed'] += 1
            self.results['user_tests'][user_role]['failed'] += 1
            self.print_error(f"[{user_role}] {method} {endpoint} → {status_code} (esperado: {expected}) ({duration:.3f}s)")
            self.results['errors'].append({
                'route': f"{method} {endpoint}",
                'user_role': user_role,
                'error': f"Status {status_code}, esperado {expected}"
            })
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     expected_status: int = 200, headers: Optional[Dict] = None) -> Dict:
        """Faz requisição HTTP e registra resultado"""
        start_time = time.time()
        
        user_role = self.current_user if self.current_user else 'anonymous'
        token = self.test_users[self.current_user]['token'] if self.current_user else None
        
        # Headers padrão
        request_headers = {'HTTP_AUTHORIZATION': f'Token {token}'} if token else {}
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
            self.log_route_test(method, endpoint, response.status_code, expected_status, duration, user_role, data)
            
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
            self.log_route_test(method, endpoint, 0, expected_status, duration, user_role, data)
            self.results['errors'].append({
                'route': f"{method} {endpoint}",
                'user_role': user_role,
                'error': str(e)
            })
            return {
                'status_code': 0,
                'data': {'error': str(e)},
                'success': False
            }
    
    def authenticate_user(self, user_type: str) -> bool:
        """Autentica usuário específico"""
        if user_type not in self.test_users:
            self.print_error(f"Tipo de usuário '{user_type}' não encontrado")
            return False
        
        user_info = self.test_users[user_type]
        self.current_user = user_type
        
        self.print_info(f"Autenticando como {user_info['role']}: {user_info['username']}")
        
        # Login
        login_data = {
            'username': user_info['username'],
            'password': user_info['password']
        }
        
        response = self.make_request(
            'POST',
            '/api/auth/token/',
            login_data,
            expected_status=200
        )
        
        if response['success']:
            user_info['token'] = response['data'].get('token')
            self.print_info(f"Token obtido: {user_info['token'][:20]}...")
            
            # Buscar ID do usuário
            user_response = self.make_request('GET', '/api/users/', expected_status=200)
            if user_response['success'] and user_response['data'].get('results'):
                for user in user_response['data']['results']:
                    if user.get('username') == user_info['username']:
                        user_info['user_id'] = user.get('id')
                        self.print_info(f"ID do usuário: {user_info['user_id']}")
                        break
            
            return True
        else:
            self.print_error(f"Falha no login para {user_info['username']}")
            self.current_user = None
            return False
    
    def test_system_endpoints_all_users(self):
        """Testa endpoints do sistema com todos os usuários"""
        self.print_header("TESTE - Endpoints do Sistema (Todos os Usuários)")
        
        # Testes sem autenticação
        self.current_user = None
        self.make_request('GET', '/api/', expected_status=200)
        self.make_request('GET', '/api/docs/', expected_status=200)
        self.make_request('GET', '/api/schema/', expected_status=200)
        
        # Testes com cada usuário
        for user_type in self.test_users.keys():
            if self.authenticate_user(user_type):
                self.make_request('GET', '/api/', expected_status=200)
    
    def test_user_permissions(self, user_type: str):
        """Testa permissões específicas de um tipo de usuário"""
        if not self.authenticate_user(user_type):
            return
        
        user_info = self.test_users[user_type]
        self.print_header(f"TESTE DE PERMISSÕES - {user_info['role'].upper()}")
        
        # Testes básicos de usuários
        self.make_request('GET', '/api/users/', expected_status=200)
        
        if user_info['user_id']:
            # Visualizar próprio perfil (todos devem conseguir)
            self.make_request('GET', f'/api/users/{user_info["user_id"]}/', expected_status=200)
            
            # Atualizar próprio perfil (todos devem conseguir)
            update_data = {
                'first_name': f'{user_info["role"]} Atualizado'
            }
            self.make_request('PATCH', f'/api/users/{user_info["user_id"]}/', update_data, expected_status=200)
        
        # Testes específicos por role
        if user_type == 'admin':
            self._test_admin_permissions()
        elif user_type == 'veterinario':
            self._test_veterinario_permissions()
        elif user_type == 'funcionario':
            self._test_funcionario_permissions()
        elif user_type == 'cliente':
            self._test_cliente_permissions()
    
    def _test_admin_permissions(self):
        """Testa permissões específicas do Admin"""
        self.print_info("Testando permissões de ADMIN...")
        
        # Admin deve poder criar serviços
        servico_data = {
            'nome': 'Serviço Admin Test',
            'descricao': 'Teste de criação por admin',
            'preco': '200.00',
            'duracao_minutos': 45,
            'ativo': True
        }
        response = self.make_request('POST', '/api/agendamentos/servicos/', servico_data, expected_status=201)
        if response['success']:
            servico_id = response['data'].get('id')
            self.created_objects['servicos'].append(servico_id)
        
        # Admin deve poder configurar horários
        horario_data = {
            'dia_semana': 2,  # Terça-feira
            'hora_abertura': '09:00:00',
            'hora_fechamento': '17:00:00',
            'ativo': True
        }
        response = self.make_request('POST', '/api/configuracao/horarios-funcionamento/', horario_data, expected_status=201)
        if response['success']:
            horario_id = response['data'].get('id')
            self.created_objects['horarios'].append(horario_id)
        
        # Admin deve poder criar feriados
        feriado_data = {
            'nome': 'Feriado Teste Admin',
            'data': (datetime.now() + timedelta(days=60)).date().isoformat(),
            'ativo': True
        }
        response = self.make_request('POST', '/api/configuracao/feriados/', feriado_data, expected_status=201)
        if response['success']:
            feriado_id = response['data'].get('id')
            self.created_objects['feriados'].append(feriado_id)
    
    def _test_veterinario_permissions(self):
        """Testa permissões específicas do Veterinário"""
        self.print_info("Testando permissões de VETERINÁRIO...")
        
        # Veterinário deve poder visualizar pets
        self.make_request('GET', '/api/pets/', expected_status=200)
        
        # Veterinário NÃO deve poder criar serviços (dependendo da regra de negócio)
        servico_data = {
            'nome': 'Serviço Vet Test',
            'descricao': 'Teste de criação por veterinário',
            'preco': '150.00',
            'duracao_minutos': 30
        }
        # Esperamos 403 (Forbidden) se veterinário não pode criar serviços
        self.make_request('POST', '/api/agendamentos/servicos/', servico_data, expected_status=403)
        
        # Veterinário deve poder visualizar agendamentos
        self.make_request('GET', '/api/agendamentos/agendamentos/', expected_status=200)
        
        # Veterinário NÃO deve poder configurar horários
        horario_data = {
            'dia_semana': 3,
            'hora_abertura': '08:00:00',
            'hora_fechamento': '18:00:00',
            'ativo': True
        }
        self.make_request('POST', '/api/configuracao/horarios-funcionamento/', horario_data, expected_status=403)
    
    def _test_funcionario_permissions(self):
        """Testa permissões específicas do Funcionário"""
        self.print_info("Testando permissões de FUNCIONÁRIO...")
        
        # Funcionário deve poder visualizar pets
        self.make_request('GET', '/api/pets/', expected_status=200)
        
        # Funcionário deve poder visualizar serviços
        self.make_request('GET', '/api/agendamentos/servicos/', expected_status=200)
        
        # Funcionário deve poder visualizar agendamentos
        self.make_request('GET', '/api/agendamentos/agendamentos/', expected_status=200)
        
        # Funcionário NÃO deve poder criar serviços
        servico_data = {
            'nome': 'Serviço Func Test',
            'descricao': 'Teste de criação por funcionário',
            'preco': '100.00',
            'duracao_minutos': 30
        }
        self.make_request('POST', '/api/agendamentos/servicos/', servico_data, expected_status=403)
        
        # Funcionário NÃO deve poder configurar horários
        horario_data = {
            'dia_semana': 4,
            'hora_abertura': '08:00:00',
            'hora_fechamento': '18:00:00',
            'ativo': True
        }
        self.make_request('POST', '/api/configuracao/horarios-funcionamento/', horario_data, expected_status=403)
    
    def _test_cliente_permissions(self):
        """Testa permissões específicas do Cliente"""
        self.print_info("Testando permissões de CLIENTE...")
        
        # Cliente deve poder visualizar seus próprios pets
        self.make_request('GET', '/api/pets/', expected_status=200)
        
        # Cliente deve poder criar pets
        pet_data = {
            'nome': 'Pet do Cliente',
            'especie': 'Cachorro',
            'raca': 'Vira-lata',
            'idade': 2,
            'peso': 15.0,
            'cor': 'Marrom'
        }
        response = self.make_request('POST', '/api/pets/', pet_data, expected_status=201)
        if response['success']:
            pet_id = response['data'].get('id')
            self.created_objects['pets'].append(pet_id)
        
        # Cliente deve poder visualizar serviços (para fazer agendamentos)
        self.make_request('GET', '/api/agendamentos/servicos/', expected_status=200)
        
        # Cliente NÃO deve poder criar serviços
        servico_data = {
            'nome': 'Serviço Cliente Test',
            'descricao': 'Teste de criação por cliente',
            'preco': '80.00',
            'duracao_minutos': 30
        }
        self.make_request('POST', '/api/agendamentos/servicos/', servico_data, expected_status=403)
        
        # Cliente NÃO deve poder acessar configurações
        self.make_request('GET', '/api/configuracao/horarios-funcionamento/', expected_status=403)
        self.make_request('GET', '/api/configuracao/feriados/', expected_status=403)
    
    def test_cross_user_access(self):
        """Testa acesso entre usuários (isolamento de dados)"""
        self.print_header("TESTE - Isolamento de Dados Entre Usuários")
        
        # Criar pet como cliente
        if self.authenticate_user('cliente'):
            pet_data = {
                'nome': 'Pet Privado Cliente',
                'especie': 'Gato',
                'raca': 'Persa',
                'idade': 1,
                'peso': 3.5,
                'cor': 'Branco'
            }
            response = self.make_request('POST', '/api/pets/', pet_data, expected_status=201)
            if response['success']:
                pet_cliente_id = response['data'].get('id')
                self.created_objects['pets'].append(pet_cliente_id)
                
                # Tentar acessar pet do cliente como funcionário
                if self.authenticate_user('funcionario'):
                    # Funcionário deve poder ver o pet (regra de negócio)
                    self.make_request('GET', f'/api/pets/{pet_cliente_id}/', expected_status=200)
                
                # Tentar modificar pet do cliente como outro cliente seria 403
                # (se houvesse outro cliente para testar)
    
    def cleanup_created_objects(self):
        """Remove objetos criados durante os testes"""
        self.print_header("CLEANUP - Removendo objetos de teste")
        
        # Fazer cleanup como admin para ter todas as permissões
        if self.authenticate_user('admin'):
            # Deletar agendamentos
            for agendamento_id in self.created_objects['agendamentos']:
                self.make_request('DELETE', f'/api/agendamentos/agendamentos/{agendamento_id}/', expected_status=204)
            
            # Deletar prontuários
            for prontuario_id in self.created_objects['prontuarios']:
                self.make_request('DELETE', f'/api/prontuarios/{prontuario_id}/', expected_status=204)
            
            # Deletar pets
            for pet_id in self.created_objects['pets']:
                self.make_request('DELETE', f'/api/pets/{pet_id}/', expected_status=204)
            
            # Deletar serviços
            for servico_id in self.created_objects['servicos']:
                self.make_request('DELETE', f'/api/agendamentos/servicos/{servico_id}/', expected_status=204)
            
            # Deletar configurações criadas
            for horario_id in self.created_objects['horarios']:
                self.make_request('DELETE', f'/api/configuracao/horarios-funcionamento/{horario_id}/', expected_status=204)
            
            for feriado_id in self.created_objects['feriados']:
                self.make_request('DELETE', f'/api/configuracao/feriados/{feriado_id}/', expected_status=204)
    
    def generate_report(self):
        """Gera relatório final dos testes"""
        self.print_header("RELATÓRIO FINAL DOS TESTES MULTI-USUÁRIO")
        
        # Resumo geral
        print(f"{Colors.BOLD}📊 RESUMO GERAL:{Colors.ENDC}")
        print(f"   Total de rotas testadas: {self.results['total_tests']}")
        print(f"   {Colors.OKGREEN}✓ Sucessos: {self.results['passed']}{Colors.ENDC}")
        print(f"   {Colors.FAIL}✗ Falhas: {self.results['failed']}{Colors.ENDC}")
        
        if self.results['total_tests'] > 0:
            success_rate = (self.results['passed'] / self.results['total_tests']) * 100
            print(f"   Taxa de sucesso: {success_rate:.1f}%")
        
        # Resultados por usuário
        print(f"\n{Colors.BOLD}👥 RESULTADOS POR PERFIL DE USUÁRIO:{Colors.ENDC}")
        for user_type, user_results in self.results['user_tests'].items():
            total_user = user_results['passed'] + user_results['failed']
            if total_user > 0:
                user_success_rate = (user_results['passed'] / total_user) * 100
                print(f"   {user_type.upper():12s}: {user_results['passed']:3d}✓ {user_results['failed']:3d}✗ ({user_success_rate:5.1f}%)")
        
        # Análise de permissões
        print(f"\n{Colors.BOLD}🔐 ANÁLISE DE PERMISSÕES:{Colors.ENDC}")
        permission_errors = [error for error in self.results['errors'] if '403' in error.get('error', '')]
        print(f"   Total de negações de acesso (403): {len(permission_errors)}")
        
        # Erros encontrados
        if self.results['errors']:
            print(f"\n{Colors.BOLD}{Colors.FAIL}❌ ERROS ENCONTRADOS:{Colors.ENDC}")
            for i, error in enumerate(self.results['errors'], 1):
                print(f"   {i}. [{error.get('user_role', 'unknown')}] {error['route']}: {error['error']}")
        
        print(f"\n{Colors.BOLD}📄 Relatório salvo em: api_multi_user_test_report.json{Colors.ENDC}")
        
        # Salvar relatório em JSON
        with open('api_multi_user_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
    
    def run_full_simulation(self):
        """Executa simulação completa com múltiplos usuários"""
        start_time = time.time()
        
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("🚀 TOP PET SYSTEM - SIMULAÇÃO CRUD API MULTI-USUÁRIO")
        print("====================================================")
        print(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Colors.ENDC}")
        
        try:
            # Testes do sistema
            self.test_system_endpoints_all_users()
            
            # Testes específicos por perfil de usuário
            for user_type in ['admin', 'veterinario', 'funcionario', 'cliente']:
                self.test_user_permissions(user_type)
            
            # Testes de isolamento de dados
            self.test_cross_user_access()
            
            # Cleanup
            self.cleanup_created_objects()
            
            # Relatório
            total_time = time.time() - start_time
            self.results['total_duration'] = round(total_time, 3)
            self.generate_report()
            
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}✅ Simulação multi-usuário concluída com sucesso!")
            print(f"⏱️  Tempo total: {total_time:.3f}s{Colors.ENDC}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Erro durante simulação: {str(e)}")
            return False


def main():
    """Função principal"""
    simulator = MultiUserAPISimulator()
    success = simulator.run_full_simulation()
    
    if success:
        print(f"\n{Colors.OKCYAN}💡 Para analisar os resultados detalhados:")
        print(f"   cat api_multi_user_test_report.json | python -m json.tool{Colors.ENDC}")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
