# pets/tests_unidade.py

import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, timedelta
from decimal import Decimal

from .models import Pet
from users.models import Profile


class PetModelUnitTest(TestCase):
    """Testes de unidade específicos para o modelo Pet"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='tutor_unit_test',
            email='tutor@unittest.com',
            password='testpass123'
        )
        # Configurar perfil como cliente
        profile = Profile.objects.get(user=self.user)
        profile.role = Profile.Role.CLIENTE
        profile.save()
    
    def test_pet_creation_minimal_data(self):
        """Teste criação de pet com dados mínimos obrigatórios"""
        pet = Pet.objects.create(
            nome='Buddy',
            especie='Cachorro',
            tutor=self.user
        )
        
        self.assertEqual(pet.nome, 'Buddy')
        self.assertEqual(pet.especie, 'Cachorro')
        self.assertEqual(pet.tutor, self.user)
        self.assertEqual(pet.sexo, Pet.Gender.UNKNOWN)  # Valor padrão
        self.assertIsNone(pet.raca)
        self.assertIsNone(pet.data_de_nascimento)
        self.assertIsNotNone(pet.created_at)
        self.assertIsNotNone(pet.updated_at)
    
    def test_pet_creation_complete_data(self):
        """Teste criação de pet com todos os dados"""
        birth_date = date(2020, 5, 15)
        pet = Pet.objects.create(
            nome='Luna',
            especie='Gato',
            raca='Siamês',
            data_de_nascimento=birth_date,
            sexo=Pet.Gender.FEMALE,
            tutor=self.user,
            observacoes='Pet muito dócil e carinhoso'
        )
        
        self.assertEqual(pet.nome, 'Luna')
        self.assertEqual(pet.especie, 'Gato')
        self.assertEqual(pet.raca, 'Siamês')
        self.assertEqual(pet.data_de_nascimento, birth_date)
        self.assertEqual(pet.sexo, Pet.Gender.FEMALE)
        self.assertEqual(pet.observacoes, 'Pet muito dócil e carinhoso')
    
    def test_pet_str_method(self):
        """Teste do método __str__ do Pet"""
        pet = Pet.objects.create(
            nome='Max',
            especie='Cachorro',
            tutor=self.user
        )
        
        expected_str = "Max (Cachorro)"
        self.assertEqual(str(pet), expected_str)
    
    def test_pet_idade_property_with_birth_date(self):
        """Teste da propriedade idade quando há data de nascimento"""
        # Pet nascido há exatos 3 anos - garantindo data exata
        today = date.today()
        birth_date = today.replace(year=today.year - 3)
        pet = Pet.objects.create(
            nome='Rocky',
            especie='Cachorro',
            data_de_nascimento=birth_date,
            tutor=self.user
        )
        
        self.assertEqual(pet.idade, 3)
    
    def test_pet_idade_property_without_birth_date(self):
        """Teste da propriedade idade quando não há data de nascimento"""
        pet = Pet.objects.create(
            nome='Shadow',
            especie='Gato',
            tutor=self.user
        )
        
        self.assertIsNone(pet.idade)
    
    def test_pet_idade_calculation_edge_cases(self):
        """Teste cálculo de idade em casos extremos"""
        # Pet nascido hoje
        pet_today = Pet.objects.create(
            nome='Baby',
            especie='Hamster',
            data_de_nascimento=date.today(),
            tutor=self.user
        )
        self.assertEqual(pet_today.idade, 0)
        
        # Pet nascido há exatos 2 anos
        two_years_ago = date.today().replace(year=date.today().year - 2)
        pet_exact = Pet.objects.create(
            nome='Oldie',
            especie='Tartaruga',
            data_de_nascimento=two_years_ago,
            tutor=self.user
        )
        self.assertEqual(pet_exact.idade, 2)
    
    def test_pet_gender_choices(self):
        """Teste das opções de sexo do Pet"""
        # Teste sexo masculino
        pet_male = Pet.objects.create(
            nome='Thor',
            especie='Cachorro',
            sexo=Pet.Gender.MALE,
            tutor=self.user
        )
        self.assertEqual(pet_male.sexo, Pet.Gender.MALE)
        self.assertEqual(pet_male.get_sexo_display(), 'Macho')
        
        # Teste sexo feminino
        pet_female = Pet.objects.create(
            nome='Lola',
            especie='Gato',
            sexo=Pet.Gender.FEMALE,
            tutor=self.user
        )
        self.assertEqual(pet_female.sexo, Pet.Gender.FEMALE)
        self.assertEqual(pet_female.get_sexo_display(), 'Fêmea')
        
        # Teste sexo desconhecido (padrão)
        pet_unknown = Pet.objects.create(
            nome='Mystery',
            especie='Pássaro',
            tutor=self.user
        )
        self.assertEqual(pet_unknown.sexo, Pet.Gender.UNKNOWN)
        self.assertEqual(pet_unknown.get_sexo_display(), 'Desconhecido')
    
    def test_pet_required_fields(self):
        """Teste campos obrigatórios do Pet"""
        # Teste sem nome (deve falhar)
        with self.assertRaises((IntegrityError, ValidationError)):
            pet = Pet(
                especie='Cachorro',
                tutor=self.user
            )
            pet.full_clean()
            pet.save()
        
        # Teste sem espécie (deve falhar)
        with self.assertRaises((IntegrityError, ValidationError)):
            pet = Pet(
                nome='Nameless',
                tutor=self.user
            )
            pet.full_clean()
            pet.save()
        
        # Teste sem tutor (deve falhar)
        with self.assertRaises((IntegrityError, ValidationError)):
            pet = Pet(
                nome='Orphan',
                especie='Gato'
            )
            pet.full_clean()
            pet.save()
    
    def test_pet_tutor_relationship(self):
        """Teste relacionamento Pet-Tutor"""
        pet1 = Pet.objects.create(
            nome='Pet1',
            especie='Cachorro',
            tutor=self.user
        )
        
        pet2 = Pet.objects.create(
            nome='Pet2',
            especie='Gato',
            tutor=self.user
        )
        
        # Verificar que o usuário tem acesso aos pets
        user_pets = self.user.pets.all()
        self.assertIn(pet1, user_pets)
        self.assertIn(pet2, user_pets)
        self.assertEqual(user_pets.count(), 2)
    
    def test_pet_cascade_deletion(self):
        """Teste deleção em cascata quando tutor é removido"""
        pet = Pet.objects.create(
            nome='ToBeDeleted',
            especie='Cachorro',
            tutor=self.user
        )
        
        pet_id = pet.id
        
        # Deletar o tutor deve deletar o pet
        self.user.delete()
        
        # Verificar que o pet foi deletado
        with self.assertRaises(Pet.DoesNotExist):
            Pet.objects.get(id=pet_id)
    
    def test_pet_field_lengths(self):
        """Teste limites de tamanho dos campos"""
        # Nome muito longo (máximo 100 caracteres)
        long_name = 'A' * 101
        with self.assertRaises(Exception):  # ValidationError ou similar
            pet = Pet(
                nome=long_name,
                especie='Cachorro',
                tutor=self.user
            )
            pet.full_clean()
        
        # Espécie muito longa (máximo 50 caracteres)
        long_species = 'B' * 51
        with self.assertRaises(Exception):
            pet = Pet(
                nome='Test',
                especie=long_species,
                tutor=self.user
            )
            pet.full_clean()
    
    def test_pet_optional_fields(self):
        """Teste campos opcionais do Pet"""
        pet = Pet.objects.create(
            nome='SimpleTest',
            especie='Cachorro',
            tutor=self.user,
            raca=None,  # Opcional
            data_de_nascimento=None,  # Opcional
            observacoes=None  # Opcional
        )
        
        self.assertIsNone(pet.raca)
        self.assertIsNone(pet.data_de_nascimento)
        self.assertIsNone(pet.observacoes)
        # Campo foto é ImageField, verifica se não tem valor
        self.assertFalse(pet.foto)
    
    def test_pet_meta_options(self):
        """Teste opções de Meta do modelo Pet"""
        # Verificar verbose names
        self.assertEqual(Pet._meta.verbose_name, "Pet")
        self.assertEqual(Pet._meta.verbose_name_plural, "Pets")
        
        # Verificar que existem índices definidos
        index_names = [index.name for index in Pet._meta.indexes]
        self.assertIn('pet_tutor_idx', index_names)
        self.assertIn('pet_especie_idx', index_names)
        self.assertIn('pet_raca_idx', index_names)
    
    def test_pet_update_timestamp(self):
        """Teste atualização do timestamp updated_at"""
        pet = Pet.objects.create(
            nome='TimeTest',
            especie='Cachorro',
            tutor=self.user
        )
        
        original_updated_at = pet.updated_at
        
        # Pequena pausa para garantir diferença de tempo
        import time
        time.sleep(0.01)
        
        # Atualizar o pet
        pet.observacoes = 'Updated'
        pet.save()
        
        # Recarregar do banco
        pet.refresh_from_db()
        
        self.assertGreater(pet.updated_at, original_updated_at)
    
    def test_pet_multiple_species(self):
        """Teste criação de pets de diferentes espécies"""
        especies = ['Cachorro', 'Gato', 'Pássaro', 'Hamster', 'Peixe', 'Tartaruga']
        
        for i, especie in enumerate(especies):
            pet = Pet.objects.create(
                nome=f'Pet{i}',
                especie=especie,
                tutor=self.user
            )
            self.assertEqual(pet.especie, especie)
        
        # Verificar que todos foram criados
        self.assertEqual(Pet.objects.filter(tutor=self.user).count(), len(especies))


class PetValidationUnitTest(TestCase):
    """Testes específicos de validação do modelo Pet"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='validator_test',
            email='validator@unittest.com',
            password='testpass123'
        )
    
    def test_birth_date_validation_future_date(self):
        """Teste validação de data de nascimento futura"""
        future_date = date.today() + timedelta(days=1)
        
        pet = Pet(
            nome='FutureTest',
            especie='Cachorro',
            data_de_nascimento=future_date,
            tutor=self.user
        )
        
        # Deve falhar na validação
        with self.assertRaises(ValidationError):
            pet.full_clean()
    
    def test_birth_date_validation_valid_past_date(self):
        """Teste validação de data de nascimento válida (passado)"""
        past_date = date.today() - timedelta(days=365)
        
        pet = Pet(
            nome='PastTest',
            especie='Cachorro',
            data_de_nascimento=past_date,
            tutor=self.user
        )
        
        # Não deve levantar exceção
        try:
            pet.full_clean()
        except ValidationError:
            self.fail("Validação falhou para data válida no passado")
    
    def test_birth_date_validation_today(self):
        """Teste validação de data de nascimento hoje"""
        today = date.today()
        
        pet = Pet(
            nome='TodayTest',
            especie='Cachorro',
            data_de_nascimento=today,
            tutor=self.user
        )
        
        # Não deve levantar exceção
        try:
            pet.full_clean()
        except ValidationError:
            self.fail("Validação falhou para data de hoje")
