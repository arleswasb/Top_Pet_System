# pets/tests_validacao.py
"""
Testes específicos para validações do modelo Pet.
Estes testes focam nas regras de validação, constraints e verificações de integridade.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, timedelta

from .models import Pet


class PetRequiredFieldsValidationTest(TestCase):
    """Testes para validação de campos obrigatórios"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='validation_user',
            email='validation@test.com',
            password='testpass123'
        )
        
    def test_pet_sem_nome_invalido(self):
        """Teste: Pet sem nome deve ser inválido"""
        with self.assertRaises(ValidationError):
            pet = Pet(
                nome='',  # Nome vazio
                especie='Cão',
                tutor=self.user
            )
            pet.full_clean()
            
    def test_pet_sem_especie_invalido(self):
        """Teste: Pet sem espécie deve ser inválido"""
        with self.assertRaises(ValidationError):
            pet = Pet(
                nome='Buddy',
                especie='',  # Espécie vazia
                tutor=self.user
            )
            pet.full_clean()
            
    def test_pet_sem_tutor_invalido(self):
        """Teste: Pet sem tutor deve ser inválido"""
        with self.assertRaises(IntegrityError):
            Pet.objects.create(
                nome='Buddy',
                especie='Cão',
                tutor=None  # Tutor nulo
            )


class PetFieldLengthValidationTest(TestCase):
    """Testes para validação de tamanho de campos"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='length_user',
            email='length@test.com',
            password='testpass123'
        )
        
    def test_nome_max_length(self):
        """Teste: Nome deve respeitar limite de caracteres"""
        nome_longo = 'A' * 101  # 101 caracteres
        
        with self.assertRaises(ValidationError):
            pet = Pet(
                nome=nome_longo,
                especie='Cão',
                tutor=self.user
            )
            pet.full_clean()
            
    def test_especie_max_length(self):
        """Teste: Espécie deve respeitar limite de caracteres"""
        especie_longa = 'B' * 51  # 51 caracteres
        
        with self.assertRaises(ValidationError):
            pet = Pet(
                nome='Test',
                especie=especie_longa,
                tutor=self.user
            )
            pet.full_clean()
            
    def test_raca_max_length(self):
        """Teste: Raça deve respeitar limite de caracteres"""
        raca_longa = 'C' * 51  # 51 caracteres
        
        with self.assertRaises(ValidationError):
            pet = Pet(
                nome='Test',
                especie='Cão',
                raca=raca_longa,
                tutor=self.user
            )
            pet.full_clean()


class PetDateValidationTest(TestCase):
    """Testes para validação de datas"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='date_user',
            email='date@test.com',
            password='testpass123'
        )
        
    def test_data_nascimento_futura_invalida(self):
        """Teste: Data de nascimento futura deve ser inválida"""
        data_futura = date.today() + timedelta(days=1)
        
        with self.assertRaises(ValidationError):
            pet = Pet(
                nome='Future',
                especie='Cão',
                data_de_nascimento=data_futura,
                tutor=self.user
            )
            pet.full_clean()
            
    def test_data_nascimento_muito_antiga_valida(self):
        """Teste: Data de nascimento muito antiga deve ser válida"""
        data_antiga = date(1900, 1, 1)
        
        # Não deve gerar erro
        pet = Pet(
            nome='Ancient',
            especie='Tartaruga',
            data_de_nascimento=data_antiga,
            tutor=self.user
        )
        pet.full_clean()  # Deve passar sem exceções


class PetBusinessRulesValidationTest(TestCase):
    """Testes para regras de negócio e validações customizadas"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='business_user',
            email='business@test.com',
            password='testpass123'
        )
        
    def test_criar_pet_valido_completo(self):
        """Teste: Criar um pet com todos os dados válidos"""
        pet = Pet(
            nome='Buddy',
            especie='Cão',
            raca='Golden Retriever',
            data_de_nascimento=date(2020, 1, 15),
            sexo=Pet.Gender.MALE,
            tutor=self.user,
            observacoes='Pet muito amigável'
        )
        
        # Não deve gerar erro de validação
        pet.full_clean()
        pet.save()
        
        # Verificar se foi salvo corretamente
        self.assertEqual(pet.nome, 'Buddy')
        self.assertEqual(pet.especie, 'Cão')
        self.assertEqual(pet.raca, 'Golden Retriever')
        self.assertEqual(pet.sexo, Pet.Gender.MALE)
        self.assertEqual(pet.tutor, self.user)
        
    def test_criar_pet_valido_minimo(self):
        """Teste: Criar um pet apenas com campos obrigatórios"""
        pet = Pet(
            nome='Simple',
            especie='Gato',
            tutor=self.user
        )
        
        # Não deve gerar erro de validação
        pet.full_clean()
        pet.save()
        
        # Verificar valores padrão
        self.assertEqual(pet.sexo, Pet.Gender.UNKNOWN)
        self.assertIsNone(pet.raca)
        self.assertIsNone(pet.observacoes)
        self.assertIsNone(pet.data_de_nascimento)
