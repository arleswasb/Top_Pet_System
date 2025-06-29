# prontuarios/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from pets.models import Pet
from users.models import Profile
from .models import Prontuario

User = get_user_model()


class ProntuarioModelTest(TestCase):
    """Testes para o modelo Prontuario"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.tutor = User.objects.create_user(
            username='tutor_test',
            password='testpass123'
        )
        self.veterinario = User.objects.create_user(
            username='vet_test',
            password='testpass123',
            is_staff=True # Veterinários são staff
        )
        Profile.objects.filter(user=self.veterinario).update(role=Profile.Role.FUNCIONARIO)

        self.pet = Pet.objects.create(
            nome='Rex',
            especie='Cachorro',
            tutor=self.tutor,
            data_de_nascimento=date(2020, 1, 1)
        )

    def test_criar_prontuario_valido(self):
        """Teste: Criar um prontuário com dados válidos"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            motivo_consulta="Check-up de rotina",
            diagnostico="Tudo ok",
            tratamento="Nenhum"
        )
        self.assertIsNotNone(prontuario.pk)
        self.assertEqual(prontuario.pet, self.pet)
        self.assertEqual(prontuario.veterinario, self.veterinario)

    def test_prontuario_sem_pet_invalido(self):
        """Teste: Prontuário sem pet deve ser inválido"""
        with self.assertRaises(IntegrityError):
            Prontuario.objects.create(
                veterinario=self.veterinario,
                motivo_consulta="Consulta sem pet"
            )

    def test_prontuario_sem_veterinario_invalido(self):
        """Teste: Prontuário sem veterinário deve ser inválido"""
        with self.assertRaises(IntegrityError):
            Prontuario.objects.create(
                pet=self.pet,
                motivo_consulta="Consulta sem vet"
            )

    def test_tipo_consulta_padrao(self):
        """Teste: Tipo de consulta padrão deve ser 'Consulta de Rotina'"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            motivo_consulta="Consulta padrão"
        )
        self.assertEqual(prontuario.tipo_consulta, Prontuario.TipoConsulta.CONSULTA_ROTINA)

    def test_str_representation(self):
        """Teste: Representação string do prontuário"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            motivo_consulta="Teste str"
        )
        data_formatada = prontuario.data_consulta.strftime('%d/%m/%Y')
        expected_str = f"Prontuário {prontuario.id} - {self.pet.nome} - {data_formatada}"
        self.assertEqual(str(prontuario), expected_str)

    def test_ordenacao_prontuarios(self):
        """Teste: Prontuários devem ser ordenados por data de consulta decrescente"""
        prontuario1 = Prontuario.objects.create(
            pet=self.pet, veterinario=self.veterinario, motivo_consulta="Primeiro",
            data_consulta=timezone.now() - timedelta(days=10)
        )
        prontuario2 = Prontuario.objects.create(
            pet=self.pet, veterinario=self.veterinario, motivo_consulta="Segundo",
            data_consulta=timezone.now() - timedelta(days=5)
        )
        prontuario3 = Prontuario.objects.create(
            pet=self.pet, veterinario=self.veterinario, motivo_consulta="Terceiro"
        )

        prontuarios_do_pet = Prontuario.objects.filter(pet=self.pet)
        self.assertEqual(prontuarios_do_pet.first(), prontuario3)
        self.assertEqual(prontuarios_do_pet.last(), prontuario1)
