from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .models import Servico, Agendamento
from pets.models import Pet
from users.models import Profile


class ServicoModelTestCase(TestCase):
    def setUp(self):
        self.servico_data = {
            'nome': 'Banho e Tosa',
            'descricao': 'Serviço completo de banho e tosa',
            'duracao': timedelta(hours=1),
            'preco': 50.00,
            'disponivel': True
        }

    def test_servico_creation(self):
        """Testa a criação básica de um serviço"""
        servico = Servico.objects.create(**self.servico_data)
        self.assertEqual(servico.nome, 'Banho e Tosa')
        self.assertEqual(float(servico.preco), 50.00)
        self.assertTrue(servico.disponivel)

    def test_servico_str_method(self):
        """Testa o método __str__ do modelo Servico"""
        servico = Servico.objects.create(**self.servico_data)
        self.assertEqual(str(servico), 'Banho e Tosa')


class AgendamentoModelTestCase(TestCase):
    def setUp(self):
        # Criar usuário
        self.user = User.objects.create_user(
            username='tutor_agendamento',
            password='testpass123'
        )
        self.user.profile.role = Profile.Role.CLIENTE
        self.user.profile.save()

        # Criar pet
        self.pet = Pet.objects.create(
            nome='Rex',
            especie='Cachorro',
            tutor=self.user
        )

        # Criar serviço
        self.servico = Servico.objects.create(
            nome='Consulta Veterinária',
            descricao='Consulta de rotina',
            duracao=timedelta(minutes=30),
            preco=100.00
        )

        self.agendamento_data = {
            'pet': self.pet,
            'servico': self.servico,
            'data_hora': datetime.now() + timedelta(days=1),
            'status': Agendamento.StatusChoices.AGENDADO,
            'observacoes': 'Pet está bem comportado'
        }

    def test_agendamento_creation(self):
        """Testa a criação básica de um agendamento"""
        agendamento = Agendamento.objects.create(**self.agendamento_data)
        self.assertEqual(agendamento.pet.nome, 'Rex')
        self.assertEqual(agendamento.servico.nome, 'Consulta Veterinária')
        self.assertEqual(agendamento.status, Agendamento.StatusChoices.AGENDADO)

    def test_agendamento_status_choices(self):
        """Testa as opções de status do agendamento"""
        agendamento = Agendamento.objects.create(**self.agendamento_data)
        
        # Testa mudança para concluído
        agendamento.status = Agendamento.StatusChoices.CONCLUIDO
        agendamento.save()
        self.assertEqual(agendamento.status, 'CONCLUIDO')

        # Testa mudança para cancelado
        agendamento.status = Agendamento.StatusChoices.CANCELADO
        agendamento.save()
        self.assertEqual(agendamento.status, 'CANCELADO')

    def test_agendamento_ordering(self):
        """Testa se os agendamentos são ordenados por data_hora"""
        # Criar agendamento para amanhã
        agendamento1 = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico,
            data_hora=datetime.now() + timedelta(days=1)
        )
        
        # Criar agendamento para hoje
        agendamento2 = Agendamento.objects.create(
            pet=self.pet,
            servico=self.servico,
            data_hora=datetime.now()
        )

        agendamentos = list(Agendamento.objects.all())
        self.assertEqual(agendamentos[0], agendamento2)  # Hoje primeiro
        self.assertEqual(agendamentos[1], agendamento1)  # Amanhã depois
