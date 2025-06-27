# agendamentos/tests_integracao.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone

from .models import Agendamento, Servico
from pets.models import Pet
from users.models import Profile


class AgendamentoIntegrationTest(APITestCase):
    """Testes de integração para o sistema de agendamentos"""
    
    def setUp(self):
        """Configuração inicial para os testes de integração"""
        # Criar usuários
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        self.tutor_user = User.objects.create_user(
            username='tutor',
            email='tutor@test.com',
            password='tutorpass123'
        )
        
        self.funcionario_user = User.objects.create_user(
            username='funcionario',
            email='funcionario@test.com',
            password='funcpass123',
            is_staff=True
        )
        
        # Criar perfis manualmente (signals desabilitados)
        admin_profile = Profile.objects.create(user=self.admin_user, role=Profile.Role.ADMIN)
        tutor_profile = Profile.objects.create(user=self.tutor_user, role=Profile.Role.CLIENTE)
        funcionario_profile = Profile.objects.create(user=self.funcionario_user, role=Profile.Role.FUNCIONARIO)
        
        # Criar tokens para autenticação
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.tutor_token = Token.objects.create(user=self.tutor_user)
        self.funcionario_token = Token.objects.create(user=self.funcionario_user)
        
        # Criar cliente da API
        self.client = APIClient()
        
        # Criar serviços
        self.servico_banho = Servico.objects.create(
            nome='Banho e Tosa',
            descricao='Banho completo com tosa',
            duracao=timedelta(hours=1),
            preco=Decimal('50.00'),
            disponivel=True
        )
        
        self.servico_consulta = Servico.objects.create(
            nome='Consulta Veterinária',
            descricao='Consulta com veterinário',
            duracao=timedelta(minutes=30),
            preco=Decimal('80.00'),
            disponivel=True
        )
        
        # Criar pet
        self.pet = Pet.objects.create(
            nome='Buddy',
            especie='Cão',
            raca='Golden Retriever',
            tutor=self.tutor_user
        )
        
        # Data para agendamentos
        self.data_agendamento = timezone.now() + timedelta(days=1)
        
    def test_criar_agendamento_como_tutor(self):
        """Teste: Tutor pode criar agendamento para seu pet"""
        self.client.force_authenticate(user=self.tutor_user, token=self.tutor_token)
        
        data = {
            'pet_id': self.pet.id,
            'servico_id': self.servico_banho.id,
            'data_hora': self.data_agendamento.isoformat(),
            'observacoes': 'Pet muito agitado'
        }
        
        response = self.client.post('/api/agendamentos/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Agendamento.objects.count(), 1)
        agendamento = Agendamento.objects.first()
        self.assertEqual(agendamento.pet, self.pet)
        self.assertEqual(agendamento.servico, self.servico_banho)
        self.assertEqual(agendamento.status, Agendamento.StatusChoices.AGENDADO)
        
    def test_listar_agendamentos_como_tutor(self):
        """Teste: Tutor vê apenas agendamentos de seus pets"""
        # Criar agendamento do tutor
        agendamento_tutor = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico_banho,
            data_hora=self.data_agendamento
        )
        
        # Criar outro pet e agendamento de outro tutor
        outro_user = User.objects.create_user(
            username='outro_tutor',
            email='outro@test.com',
            password='pass123'
        )
        outro_pet = Pet.objects.create(
            nome='Rex',
            especie='Cão',
            tutor=outro_user
        )
        Agendamento.objects.create(
            pet=outro_pet,
            servico=self.servico_consulta,
            data_hora=self.data_agendamento + timedelta(hours=1)
        )
        
        self.client.force_authenticate(user=self.tutor_user, token=self.tutor_token)
        response = self.client.get('/api/agendamentos/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Tutor deve ver apenas seus agendamentos
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['pet']['id'], self.pet.id)
        
    def test_funcionario_ve_todos_agendamentos(self):
        """Teste: Funcionário vê todos os agendamentos"""
        # Criar múltiplos agendamentos
        Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico_banho,
            data_hora=self.data_agendamento
        )
        
        outro_user = User.objects.create_user(
            username='outro_tutor',
            email='outro@test.com',
            password='pass123'
        )
        outro_pet = Pet.objects.create(
            nome='Rex',
            especie='Cão',
            tutor=outro_user
        )
        Agendamento.objects.create(
            pet=outro_pet,
            servico=self.servico_consulta,
            data_hora=self.data_agendamento + timedelta(hours=1)
        )
        
        self.client.force_authenticate(user=self.funcionario_user, token=self.funcionario_token)
        response = self.client.get('/api/agendamentos/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Funcionário deve ver todos os agendamentos
        self.assertEqual(len(response.data), 2)
        
    def test_atualizar_status_agendamento(self):
        """Teste: Funcionário pode atualizar status do agendamento"""
        agendamento = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico_banho,
            data_hora=self.data_agendamento
        )
        
        self.client.force_authenticate(user=self.funcionario_user, token=self.funcionario_token)
        
        data = {
            'pet_id': self.pet.id,
            'servico_id': self.servico_banho.id,
            'data_hora': self.data_agendamento.isoformat(),
            'status': Agendamento.StatusChoices.CONCLUIDO,
            'observacoes': 'Serviço realizado com sucesso'
        }
        
        response = self.client.put(f'/api/agendamentos/{agendamento.id}/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        agendamento.refresh_from_db()
        self.assertEqual(agendamento.status, Agendamento.StatusChoices.CONCLUIDO)
        
    def test_cancelar_agendamento_como_tutor(self):
        """Teste: Tutor pode cancelar seu próprio agendamento"""
        agendamento = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico_banho,
            data_hora=self.data_agendamento
        )
        
        self.client.force_authenticate(user=self.tutor_user, token=self.tutor_token)
        
        data = {
            'pet_id': self.pet.id,
            'servico_id': self.servico_banho.id,
            'data_hora': self.data_agendamento.isoformat(),
            'status': Agendamento.StatusChoices.CANCELADO
        }
        
        response = self.client.put(f'/api/agendamentos/{agendamento.id}/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        agendamento.refresh_from_db()
        self.assertEqual(agendamento.status, Agendamento.StatusChoices.CANCELADO)
        
    def test_tutor_nao_pode_editar_agendamento_de_outro(self):
        """Teste: Tutor não pode editar agendamento de outro tutor"""
        outro_user = User.objects.create_user(
            username='outro_tutor',
            email='outro@test.com',
            password='pass123'
        )
        outro_pet = Pet.objects.create(
            nome='Rex',
            especie='Cão',
            tutor=outro_user
        )
        agendamento_outro = Agendamento.objects.create(
            pet=outro_pet,
            servico=self.servico_consulta,
            data_hora=self.data_agendamento
        )
        
        self.client.force_authenticate(user=self.tutor_user, token=self.tutor_token)
        
        data = {
            'pet_id': outro_pet.id,
            'servico_id': self.servico_consulta.id,
            'data_hora': self.data_agendamento.isoformat(),
            'status': Agendamento.StatusChoices.CANCELADO
        }
        
        response = self.client.put(f'/api/agendamentos/{agendamento_outro.id}/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_deletar_agendamento_como_admin(self):
        """Teste: Admin pode deletar qualquer agendamento"""
        agendamento = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico_banho,
            data_hora=self.data_agendamento
        )
        
        self.client.force_authenticate(user=self.admin_user, token=self.admin_token)
        response = self.client.delete(f'/api/agendamentos/{agendamento.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Agendamento.objects.count(), 0)


class ServicoIntegrationTest(APITestCase):
    """Testes de integração para serviços"""
    
    def setUp(self):
        """Configuração inicial para testes de serviços"""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        self.tutor_user = User.objects.create_user(
            username='tutor',
            email='tutor@test.com',
            password='tutorpass123'
        )
        
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.tutor_token = Token.objects.create(user=self.tutor_user)
        self.client = APIClient()
        
    def test_admin_pode_criar_servico(self):
        """Teste: Admin pode criar novos serviços"""
        self.client.force_authenticate(user=self.admin_user, token=self.admin_token)
        
        data = {
            'nome': 'Vacinação',
            'descricao': 'Aplicação de vacinas',
            'duracao': '00:15:00',  # 15 minutos
            'preco': '120.00'
        }
        
        response = self.client.post('/api/servicos/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Servico.objects.count(), 1)
        servico = Servico.objects.first()
        self.assertEqual(servico.nome, 'Vacinação')
        self.assertEqual(servico.preco, Decimal('120.00'))
        
    def test_tutor_pode_listar_servicos(self):
        """Teste: Tutor pode listar serviços disponíveis"""
        Servico.objects.create(
            nome='Banho',
            preco=Decimal('50.00'),
            disponivel=True
        )
        Servico.objects.create(
            nome='Tosa',
            preco=Decimal('40.00'),
            disponivel=False
        )
        
        self.client.force_authenticate(user=self.tutor_user, token=self.tutor_token)
        response = self.client.get('/api/servicos/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Lista todos, independente de disponibilidade
        
    def test_tutor_nao_pode_criar_servico(self):
        """Teste: Tutor não pode criar serviços"""
        self.client.force_authenticate(user=self.tutor_user, token=self.tutor_token)
        
        data = {
            'nome': 'Novo Serviço',
            'preco': '100.00'
        }
        
        response = self.client.post('/api/servicos/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_admin_pode_desativar_servico(self):
        """Teste: Admin pode desativar serviços"""
        servico = Servico.objects.create(
            nome='Banho',
            preco=Decimal('50.00'),
            disponivel=True
        )
        
        self.client.force_authenticate(user=self.admin_user, token=self.admin_token)
        
        data = {
            'nome': 'Banho',
            'descricao': '',
            'duracao': '00:30:00',
            'preco': '50.00',
            'disponivel': False
        }
        
        response = self.client.put(f'/api/servicos/{servico.id}/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        servico.refresh_from_db()
        self.assertFalse(servico.disponivel)


class AgendamentoWorkflowTest(APITestCase):
    """Testes de fluxo completo de agendamento"""
    
    def setUp(self):
        """Configuração para testes de workflow"""
        self.tutor_user = User.objects.create_user(
            username='tutor',
            email='tutor@test.com',
            password='tutorpass123'
        )
        
        self.funcionario_user = User.objects.create_user(
            username='funcionario',
            email='funcionario@test.com',
            password='funcpass123',
            is_staff=True
        )
        
        # Criar perfis manualmente (signals desabilitados)
        tutor_profile = Profile.objects.create(user=self.tutor_user, role=Profile.Role.CLIENTE)
        funcionario_profile = Profile.objects.create(user=self.funcionario_user, role=Profile.Role.FUNCIONARIO)
        
        self.tutor_token = Token.objects.create(user=self.tutor_user)
        self.funcionario_token = Token.objects.create(user=self.funcionario_user)
        self.client = APIClient()
        
        self.pet = Pet.objects.create(
            nome='Buddy',
            especie='Cão',
            tutor=self.tutor_user
        )
        
        self.servico = Servico.objects.create(
            nome='Banho e Tosa',
            preco=Decimal('50.00'),
            disponivel=True
        )
        
    def test_fluxo_completo_agendamento(self):
        """Teste: Fluxo completo de agendamento do início ao fim"""
        data_agendamento = timezone.now() + timedelta(days=1)
        
        # 1. Tutor cria agendamento
        self.client.force_authenticate(user=self.tutor_user, token=self.tutor_token)
        
        data_criacao = {
            'pet_id': self.pet.id,
            'servico_id': self.servico.id,
            'data_hora': data_agendamento.isoformat(),
            'observacoes': 'Pet precisa de cuidado especial'
        }
        
        response = self.client.post('/api/agendamentos/', data_criacao, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        agendamento_id = response.data['id']
        
        # 2. Funcionário visualiza agendamento
        self.client.force_authenticate(user=self.funcionario_user, token=self.funcionario_token)
        response = self.client.get(f'/api/agendamentos/{agendamento_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Agendamento.StatusChoices.AGENDADO)
        
        # 3. Funcionário conclui o serviço
        data_conclusao = {
            'pet_id': self.pet.id,
            'servico_id': self.servico.id,
            'data_hora': data_agendamento.isoformat(),
            'status': Agendamento.StatusChoices.CONCLUIDO,
            'observacoes': 'Serviço realizado com sucesso. Pet se comportou bem.'
        }
        
        response = self.client.put(f'/api/agendamentos/{agendamento_id}/', data_conclusao, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Verificar status final
        agendamento = Agendamento.objects.get(id=agendamento_id)
        self.assertEqual(agendamento.status, Agendamento.StatusChoices.CONCLUIDO)
        self.assertIn('Serviço realizado com sucesso', agendamento.observacoes)
        
    def test_reagendamento(self):
        """Teste: Reagendamento de um agendamento existente"""
        data_original = timezone.now() + timedelta(days=1)
        data_nova = timezone.now() + timedelta(days=2)
        
        # Criar agendamento original
        agendamento = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico,
            data_hora=data_original
        )
        
        # Reagendar
        self.client.force_authenticate(user=self.tutor_user, token=self.tutor_token)
        
        data_reagendamento = {
            'pet_id': self.pet.id,
            'servico_id': self.servico.id,
            'data_hora': data_nova.isoformat(),
            'observacoes': 'Reagendado por solicitação do cliente'
        }
        
        response = self.client.put(f'/api/agendamentos/{agendamento.id}/', data_reagendamento, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        agendamento.refresh_from_db()
        self.assertEqual(agendamento.data_hora.date(), data_nova.date())
        self.assertIn('Reagendado', agendamento.observacoes)