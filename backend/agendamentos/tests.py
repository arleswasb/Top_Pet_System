# agendamentos/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Agendamento, Servico
from pets.models import Pet
from users.models import Profile


class ServicoModelTest(TestCase):
    """Testes para o modelo Servico"""
    
    def test_criar_servico(self):
        """Teste criação de serviço"""
        servico = Servico.objects.create(
            nome='Banho e Tosa',
            descricao='Banho completo com tosa',
            duracao=timedelta(hours=1),
            preco=Decimal('50.00')
        )
        
        self.assertEqual(servico.nome, 'Banho e Tosa')
        self.assertEqual(servico.preco, Decimal('50.00'))
        self.assertTrue(servico.disponivel)
        self.assertEqual(str(servico), 'Banho e Tosa')


class AgendamentoModelTest(TestCase):
    """Testes para o modelo Agendamento"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário
        self.user = User.objects.create_user(
            username='tutor_test',
            email='tutor@test.com',
            password='testpass123'
        )
        
        # Criar pet
        self.pet = Pet.objects.create(
            nome='Rex',
            especie='Cachorro',
            raca='Labrador',
            tutor=self.user
        )
        
        # Criar serviço
        self.servico = Servico.objects.create(
            nome='Consulta Veterinária',
            descricao='Consulta de rotina',
            duracao=timedelta(minutes=30),
            preco=Decimal('80.00')
        )
    
    def test_criar_agendamento(self):
        """Teste criação de agendamento"""
        data_hora = timezone.now() + timedelta(days=1)
        
        agendamento = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico,
            data_hora=data_hora,
            observacoes='Pet nervoso'
        )
        
        self.assertEqual(agendamento.pet, self.pet)
        self.assertEqual(agendamento.servico, self.servico)
        self.assertEqual(agendamento.status, Agendamento.StatusChoices.AGENDADO)
        self.assertEqual(agendamento.observacoes, 'Pet nervoso')
    
    def test_agendamento_relacionamentos(self):
        """Teste relacionamentos do agendamento"""
        data_hora = timezone.now() + timedelta(days=1)
        
        agendamento = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico,
            data_hora=data_hora
        )
        
        # Verificar relacionamento pet -> agendamentos
        self.assertIn(agendamento, self.pet.agendamentos.all())
        
        # Verificar relacionamento servico -> agendamentos
        self.assertIn(agendamento, self.servico.agendamentos.all())
    
    def test_agendamento_status_choices(self):
        """Teste choices de status do agendamento"""
        data_hora = timezone.now() + timedelta(days=1)
        
        agendamento = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico,
            data_hora=data_hora,
            status=Agendamento.StatusChoices.CONCLUIDO
        )
        
        self.assertEqual(agendamento.status, Agendamento.StatusChoices.CONCLUIDO)
        self.assertEqual(agendamento.get_status_display(), 'Concluído')
    
    def test_agendamento_ordenacao(self):
        """Teste ordenação dos agendamentos por data_hora"""
        data_hoje = timezone.now()
        data_amanha = data_hoje + timedelta(days=1)
        
        # Criar agendamentos fora de ordem
        agendamento_amanha = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico,
            data_hora=data_amanha
        )
        
        agendamento_hoje = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico,
            data_hora=data_hoje
        )
        
        agendamentos = list(Agendamento.objects.all())
        
        # Deve estar ordenado por data_hora (mais antigo primeiro)
        self.assertEqual(agendamentos[0], agendamento_hoje)
        self.assertEqual(agendamentos[1], agendamento_amanha)
