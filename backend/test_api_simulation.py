#!/usr/bin/env python3
"""
Script de Simulação CRUD - Top Pet System API
Testa todos os endpoints principais com relatório detalhado
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
            'timing': {}
        }
        self.token = None
        self.user_id = None
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
    
    def log_route_test(self, method: str, endpoint: str, status_code: int, 
                       expected: int, duration: float, data: Optional[Dict] = None):
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
            'data_sent': data
        }
        
        self.results['routes_tested'].append(route_info)
        
        if status_code == expected:
            self.results['passed'] += 1
            self.print_success(f"{method} {endpoint} → {status_code} ({duration:.3f}s)")
        else:
            self.results['failed'] += 1
            self.print_error(f"{method} {endpoint} → {status_code} (esperado: {expected}) ({duration:.3f}s)")
            self.results['errors'].append({
                'route': f"{method} {endpoint}",
                'error': f"Status {status_code}, esperado {expected}"
            })
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     expected_status: int = 200, headers: Optional[Dict] = None) -> Dict:
        """Faz requisição HTTP e registra resultado"""
        start_time = time.time()
        
        # Headers padrão
        request_headers = {'HTTP_AUTHORIZATION': f'Token {self.token}'} if self.token else {}
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
            self.log_route_test(method, endpoint, response.status_code, expected_status, duration, data)
            
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
            self.log_route_test(method, endpoint, 0, expected_status, duration, data)
            self.results['errors'].append({
                'route': f"{method} {endpoint}",
                'error': str(e)
            })
            return {
                'status_code': 0,
                'data': {'error': str(e)},
                'success': False
            }
    
    def setup_authentication(self):
        """Configura autenticação para testes"""
        self.print_header("SETUP - Autenticação")
        
        # Primeiro, tentar fazer login com usuário existente
        login_data = {
            'username': 'teste_api',
            'password': 'senha123'
        }
        
        response = self.make_request(
            'POST',
            '/api/auth/token/',
            login_data,
            expected_status=200
        )
        
        if response['success']:
            self.token = response['data'].get('token')
            self.print_info(f"Login realizado com sucesso. Token: {self.token[:20]}...")
            
            # Buscar ID do usuário
            user_response = self.make_request('GET', '/api/users/', expected_status=200)
            if user_response['success'] and user_response['data'].get('results'):
                for user in user_response['data']['results']:
                    if user.get('username') == 'teste_api':
                        self.user_id = user.get('id')
                        self.print_info(f"ID do usuário: {self.user_id}")
                        break
            
            return True
        else:
            self.print_error("Falha no login. Verifique as credenciais.")
            return False
    
    def test_users_crud(self):
        """Testa CRUD de usuários"""
        self.print_header("TESTE CRUD - Usuários")
        
        # GET - Listar usuários
        self.make_request('GET', '/api/users/', expected_status=200)
        
        # GET - Perfil do usuário atual
        if self.user_id:
            self.make_request('GET', f'/api/users/{self.user_id}/', expected_status=200)
            
            # PUT - Atualizar perfil
            update_data = {
                'first_name': 'Usuário Atualizado',
                'last_name': 'Teste API',
                'email': 'teste_atualizado@toppet.com'
            }
            self.make_request('PUT', f'/api/users/{self.user_id}/', update_data, expected_status=200)
            
            # PATCH - Atualização parcial
            patch_data = {'first_name': 'Usuário Patch'}
            self.make_request('PATCH', f'/api/users/{self.user_id}/', patch_data, expected_status=200)
    
    def test_pets_crud(self):
        """Testa CRUD de pets"""
        self.print_header("TESTE CRUD - Pets")
        
        # POST - Criar pet
        pet_data = {
            'nome': 'Rex',
            'especie': 'Cachorro',
            'raca': 'Labrador',
            'idade': 3,
            'peso': 25.5,
            'cor': 'Dourado',
            'observacoes': 'Pet muito dócil e brincalhão'
        }
        
        response = self.make_request('POST', '/api/pets/', pet_data, expected_status=201)
        
        pet_id = None
        if response['success']:
            pet_id = response['data'].get('id')
            self.created_objects['pets'].append(pet_id)
            self.print_info(f"Pet criado com ID: {pet_id}")
        
        # GET - Listar pets
        self.make_request('GET', '/api/pets/', expected_status=200)
        
        if pet_id:
            # GET - Detalhe do pet
            self.make_request('GET', f'/api/pets/{pet_id}/', expected_status=200)
            
            # PUT - Atualizar pet
            update_data = pet_data.copy()
            update_data.update({
                'nome': 'Rex Atualizado',
                'peso': 26.0,
                'observacoes': 'Pet atualizado via API'
            })
            self.make_request('PUT', f'/api/pets/{pet_id}/', update_data, expected_status=200)
            
            # PATCH - Atualização parcial
            patch_data = {'idade': 4}
            self.make_request('PATCH', f'/api/pets/{pet_id}/', patch_data, expected_status=200)
        
        # Criar mais um pet para testes
        pet_data2 = {
            'nome': 'Mia',
            'especie': 'Gato',
            'raca': 'Siamês',
            'idade': 2,
            'peso': 4.5,
            'cor': 'Branco e marrom'
        }
        
        response = self.make_request('POST', '/api/pets/', pet_data2, expected_status=201)
        if response['success']:
            pet_id2 = response['data'].get('id')
            self.created_objects['pets'].append(pet_id2)
    
    def test_servicos_crud(self):
        """Testa CRUD de serviços"""
        self.print_header("TESTE CRUD - Serviços")
        
        # POST - Criar serviço
        servico_data = {
            'nome': 'Consulta Veterinária',
            'descricao': 'Consulta geral com veterinário',
            'preco': '150.00',
            'duracao_minutos': 60,
            'ativo': True
        }
        
        response = self.make_request('POST', '/api/agendamentos/servicos/', servico_data, expected_status=201)
        
        servico_id = None
        if response['success']:
            servico_id = response['data'].get('id')
            self.created_objects['servicos'].append(servico_id)
            self.print_info(f"Serviço criado com ID: {servico_id}")
        
        # GET - Listar serviços
        self.make_request('GET', '/api/agendamentos/servicos/', expected_status=200)
        
        if servico_id:
            # GET - Detalhe do serviço
            self.make_request('GET', f'/api/agendamentos/servicos/{servico_id}/', expected_status=200)
            
            # PUT - Atualizar serviço
            update_data = servico_data.copy()
            update_data.update({
                'preco': '180.00',
                'duracao_minutos': 90
            })
            self.make_request('PUT', f'/api/agendamentos/servicos/{servico_id}/', update_data, expected_status=200)
            
            # PATCH - Atualização parcial
            patch_data = {'ativo': False}
            self.make_request('PATCH', f'/api/agendamentos/servicos/{servico_id}/', patch_data, expected_status=200)
        
        # Criar mais serviços
        servicos_extras = [
            {
                'nome': 'Banho e Tosa',
                'descricao': 'Banho completo com tosa',
                'preco': '80.00',
                'duracao_minutos': 120
            },
            {
                'nome': 'Vacinação',
                'descricao': 'Aplicação de vacinas',
                'preco': '50.00',
                'duracao_minutos': 30
            }
        ]
        
        for servico in servicos_extras:
            response = self.make_request('POST', '/api/agendamentos/servicos/', servico, expected_status=201)
            if response['success']:
                self.created_objects['servicos'].append(response['data'].get('id'))
    
    def test_prontuarios_crud(self):
        """Testa CRUD de prontuários"""
        self.print_header("TESTE CRUD - Prontuários")
        
        if not self.created_objects['pets']:
            self.print_error("Nenhum pet disponível para criar prontuário")
            return
        
        pet_id = self.created_objects['pets'][0]
        
        # POST - Criar prontuário
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
        
        response = self.make_request('POST', '/api/prontuarios/', prontuario_data, expected_status=201)
        
        prontuario_id = None
        if response['success']:
            prontuario_id = response['data'].get('id')
            self.created_objects['prontuarios'].append(prontuario_id)
            self.print_info(f"Prontuário criado com ID: {prontuario_id}")
        
        # GET - Listar prontuários
        self.make_request('GET', '/api/prontuarios/', expected_status=200)
        
        # GET - Prontuários por pet
        self.make_request('GET', f'/api/pets/{pet_id}/prontuarios/', expected_status=200)
        
        if prontuario_id:
            # GET - Detalhe do prontuário
            self.make_request('GET', f'/api/prontuarios/{prontuario_id}/', expected_status=200)
            
            # PUT - Atualizar prontuário
            update_data = prontuario_data.copy()
            update_data.update({
                'diagnostico': 'Gastroenterite confirmada',
                'peso_atual': 25.5,
                'observacoes': 'Melhora significativa após tratamento'
            })
            self.make_request('PUT', f'/api/prontuarios/{prontuario_id}/', update_data, expected_status=200)
            
            # PATCH - Atualização parcial
            patch_data = {'temperatura': 37.8}
            self.make_request('PATCH', f'/api/prontuarios/{prontuario_id}/', patch_data, expected_status=200)
    
    def test_agendamentos_crud(self):
        """Testa CRUD de agendamentos"""
        self.print_header("TESTE CRUD - Agendamentos")
        
        if not self.created_objects['pets'] or not self.created_objects['servicos']:
            self.print_error("Pets ou serviços não disponíveis para agendamento")
            return
        
        pet_id = self.created_objects['pets'][0]
        servico_id = self.created_objects['servicos'][0]
        
        # Primeiro, testar consulta de horários disponíveis
        tomorrow = (datetime.now() + timedelta(days=1)).date().isoformat()
        self.make_request('GET', f'/api/agendamentos/horarios-disponiveis/?data={tomorrow}', expected_status=200)
        
        # POST - Criar agendamento
        agendamento_data = {
            'pet': pet_id,
            'servico': servico_id,
            'data_agendamento': tomorrow,
            'horario': '14:00:00',
            'observacoes': 'Agendamento teste via API'
        }
        
        response = self.make_request('POST', '/api/agendamentos/agendamentos/', agendamento_data, expected_status=201)
        
        agendamento_id = None
        if response['success']:
            agendamento_id = response['data'].get('id')
            self.created_objects['agendamentos'].append(agendamento_id)
            self.print_info(f"Agendamento criado com ID: {agendamento_id}")
        
        # GET - Listar agendamentos
        self.make_request('GET', '/api/agendamentos/agendamentos/', expected_status=200)
        
        # GET - Agendamentos por data
        self.make_request('GET', f'/api/agendamentos/agendamentos/?data={tomorrow}', expected_status=200)
        
        if agendamento_id:
            # GET - Detalhe do agendamento
            self.make_request('GET', f'/api/agendamentos/agendamentos/{agendamento_id}/', expected_status=200)
            
            # PUT - Atualizar agendamento
            update_data = agendamento_data.copy()
            update_data.update({
                'horario': '15:00:00',
                'observacoes': 'Agendamento reagendado'
            })
            self.make_request('PUT', f'/api/agendamentos/agendamentos/{agendamento_id}/', update_data, expected_status=200)
            
            # PATCH - Atualização parcial
            patch_data = {'status': 'confirmado'}
            self.make_request('PATCH', f'/api/agendamentos/agendamentos/{agendamento_id}/', patch_data, expected_status=200)
    
    def test_configuration_endpoints(self):
        """Testa endpoints de configuração"""
        self.print_header("TESTE - Configurações")
        
        # GET - Horários de funcionamento
        self.make_request('GET', '/api/configuracao/horarios-funcionamento/', expected_status=200)
        
        # GET - Feriados
        self.make_request('GET', '/api/configuracao/feriados/', expected_status=200)
        
        # POST - Criar horário de funcionamento
        horario_data = {
            'dia_semana': 1,  # Segunda-feira
            'hora_abertura': '08:00:00',
            'hora_fechamento': '18:00:00',
            'ativo': True
        }
        self.make_request('POST', '/api/configuracao/horarios-funcionamento/', horario_data, expected_status=201)
        
        # POST - Criar feriado
        feriado_data = {
            'nome': 'Dia do Teste',
            'data': (datetime.now() + timedelta(days=30)).date().isoformat(),
            'ativo': True
        }
        self.make_request('POST', '/api/configuracao/feriados/', feriado_data, expected_status=201)
    
    def test_system_endpoints(self):
        """Testa endpoints do sistema"""
        self.print_header("TESTE - Sistema")
        
        # GET - Status do sistema
        self.make_request('GET', '/api/', expected_status=200)
        
        # GET - Documentação
        self.make_request('GET', '/api/docs/', expected_status=200)
        
        # GET - Schema OpenAPI
        self.make_request('GET', '/api/schema/', expected_status=200)
    
    def cleanup_created_objects(self):
        """Remove objetos criados durante os testes"""
        self.print_header("CLEANUP - Removendo objetos de teste")
        
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
        
        # Detalhes das rotas
        print(f"\n{Colors.BOLD}📋 DETALHES DAS ROTAS TESTADAS:{Colors.ENDC}")
        for i, route in enumerate(self.results['routes_tested'], 1):
            status_color = Colors.OKGREEN if route['success'] else Colors.FAIL
            print(f"   {i:2d}. {route['method']:6s} {route['endpoint']:40s} "
                  f"{status_color}{route['status_code']:3d}{Colors.ENDC} "
                  f"({route['duration']:6.3f}s)")
        
        # Erros encontrados
        if self.results['errors']:
            print(f"\n{Colors.BOLD}{Colors.FAIL}❌ ERROS ENCONTRADOS:{Colors.ENDC}")
            for i, error in enumerate(self.results['errors'], 1):
                print(f"   {i}. {error['route']}: {error['error']}")
        
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
        print("🚀 TOP PET SYSTEM - SIMULAÇÃO CRUD API")
        print("=====================================")
        print(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Colors.ENDC}")
        
        try:
            # Setup
            if not self.setup_authentication():
                self.print_error("Falha na autenticação. Abortando simulação.")
                return False
            
            # Testes CRUD
            self.test_system_endpoints()
            self.test_users_crud()
            self.test_pets_crud()
            self.test_servicos_crud()
            self.test_prontuarios_crud()
            self.test_agendamentos_crud()
            self.test_configuration_endpoints()
            
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
            return False


def main():
    """Função principal"""
    simulator = APISimulator()
    success = simulator.run_full_simulation()
    
    if success:
        print(f"\n{Colors.OKCYAN}💡 Para analisar os resultados detalhados:")
        print(f"   cat api_test_report.json | python -m json.tool{Colors.ENDC}")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
