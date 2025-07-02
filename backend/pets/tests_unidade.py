# pets/tests_unidade.py
"""
Testes unitários para funções e métodos puros do modelo Pet.
Estes testes focam em validações, cálculos e lógica de negócio do modelo,
sem envolver banco de dados, API ou integrações.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from unittest.mock import patch
from datetime import date

from .models import Pet

'''
class PetAgeCalculationTest(TestCase):
    """Testes unitários para o cálculo de idade do pet"""
    
    def setUp(self):
        """Configuração básica para os testes de idade"""
        self.user = User.objects.create_user(
            username='test_user_age',
            email='age@test.com',
            password='testpass123'
        )
        
    def test_calculo_idade_pet_exata(self):
        """Teste: Cálculo exato da idade do pet (5 anos)"""
        # Simular data atual específica para teste consistente
        data_atual_mock = date(2025, 6, 27)
        
        with patch('pets.models.date') as mock_date:
            mock_date.today.return_value = data_atual_mock
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            
            # Pet nascido exatamente 5 anos antes
            data_nascimento = date(2020, 6, 27)
            pet = Pet.objects.create(
                nome='Rex',
                especie='Cão',
                data_de_nascimento=data_nascimento,
                tutor=self.user
            )
            
            # Deve ter exatamente 5 anos
            self.assertEqual(pet.idade, 5)
            
    def test_calculo_idade_pet_ainda_nao_fez_aniversario(self):
        """Teste: Pet que ainda não fez aniversário este ano"""
        # Data atual: 27 de junho
        data_atual_mock = date(2025, 6, 27)
        
        with patch('pets.models.date') as mock_date:
            mock_date.today.return_value = data_atual_mock
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            
            # Pet nascido em dezembro (ainda não fez aniversário este ano)
            data_nascimento = date(2020, 12, 15)
            pet = Pet.objects.create(
                nome='Luna',
                especie='Gato',
                data_de_nascimento=data_nascimento,
                tutor=self.user
            )
            
            # Deve ter 4 anos (ainda não fez 5)
            self.assertEqual(pet.idade, 4)
            
    def test_calculo_idade_pet_ja_fez_aniversario(self):
        """Teste: Pet que já fez aniversário este ano"""
        # Data atual: 27 de junho
        data_atual_mock = date(2025, 6, 27)
        
        with patch('pets.models.date') as mock_date:
            mock_date.today.return_value = data_atual_mock
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            
            # Pet nascido em janeiro (já fez aniversário este ano)
            data_nascimento = date(2020, 1, 15)
            pet = Pet.objects.create(
                nome='Max',
                especie='Cão',
                data_de_nascimento=data_nascimento,
                tutor=self.user
            )
            
            # Deve ter 5 anos
            self.assertEqual(pet.idade, 5)
            
    def test_calculo_idade_pet_nascido_hoje(self):
        """Teste: Pet nascido hoje tem 0 anos"""
        data_atual_mock = date(2025, 6, 27)
        
        with patch('pets.models.date') as mock_date:
            mock_date.today.return_value = data_atual_mock
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            
            # Pet nascido hoje
            pet = Pet.objects.create(
                nome='Baby',
                especie='Hamster',
                data_de_nascimento=data_atual_mock,
                tutor=self.user
            )
            
            # Deve ter 0 anos
            self.assertEqual(pet.idade, 0)
        
    def test_idade_pet_sem_data_nascimento(self):
        """Teste: Pet sem data de nascimento deve retornar None para idade"""
        pet = Pet.objects.create(
            nome='Luna',
            especie='Gato',
            tutor=self.user
        )
        
        self.assertIsNone(pet.idade)
'''

class PetDetailedAgeCalculationTest(TestCase):
    """Testes unitários para o cálculo detalhado de idade do pet."""

    def setUp(self):
        """Configuração básica para os testes."""
        self.user = User.objects.create_user(
            username='test_user_detailed_age',
            password='testpass123'
        )

    def test_idade_detalhada_anos_exatos(self):
        """Teste: Cálculo para um pet com exatamente 2 anos."""
        data_atual_mock = date(2025, 7, 1)
        with patch('pets.models.date') as mock_date:
            mock_date.today.return_value = data_atual_mock
            
            pet = Pet(data_de_nascimento=date(2023, 7, 1))
            esperado = {"anos": 2, "meses": 0, "dias": 0}
            self.assertEqual(pet.idade_detalhada, esperado)

    def test_idade_detalhada_meses_e_dias(self):
        """Teste: Cálculo para um pet com 0 anos, alguns meses e dias."""
        data_atual_mock = date(2025, 7, 1)
        with patch('pets.models.date') as mock_date:
            mock_date.today.return_value = data_atual_mock

            pet = Pet(data_de_nascimento=date(2025, 3, 20))
            # De 20/Mar a 01/Jul -> 3 meses e 11 dias
            esperado = {"anos": 0, "meses": 3, "dias": 11}
            self.assertEqual(pet.idade_detalhada, esperado)

    def test_idade_detalhada_apenas_dias(self):
        """Teste: Cálculo para um pet com menos de 1 mês de vida."""
        data_atual_mock = date(2025, 7, 1)
        with patch('pets.models.date') as mock_date:
            mock_date.today.return_value = data_atual_mock

            pet = Pet(data_de_nascimento=date(2025, 6, 15))
            esperado = {"anos": 0, "meses": 0, "dias": 16}
            self.assertEqual(pet.idade_detalhada, esperado)

    def test_idade_detalhada_pet_nascido_hoje(self):
        """Teste: Cálculo para um pet que nasceu hoje."""
        data_atual_mock = date(2025, 7, 1)
        with patch('pets.models.date') as mock_date:
            mock_date.today.return_value = data_atual_mock
            
            pet = Pet(data_de_nascimento=date(2025, 7, 1))
            esperado = {"anos": 0, "meses": 0, "dias": 0}
            self.assertEqual(pet.idade_detalhada, esperado)

    def test_idade_detalhada_sem_data_retorna_none(self):
        """Teste: Deve retornar None se não houver data de nascimento."""
        pet = Pet(data_de_nascimento=None)
        self.assertIsNone(pet.idade_detalhada)


class PetStringRepresentationTest(TestCase):
    """Testes para a representação string do modelo Pet"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user_str',
            email='str@test.com',
            password='testpass123'
        )
        
    def test_pet_str_representation(self):
        """Teste: Representação string do pet deve ser 'Nome (Espécie)'"""
        pet = Pet.objects.create(
            nome='Mia',
            especie='Gato',
            tutor=self.user
        )
        
        self.assertEqual(str(pet), 'Mia (Gato)')
        
    def test_pet_str_representation_com_espacos(self):
        """Teste: Representação string com nomes que têm espaços"""
        pet = Pet.objects.create(
            nome='Bella Luna',
            especie='Cão Doméstico',
            tutor=self.user
        )
        
        self.assertEqual(str(pet), 'Bella Luna (Cão Doméstico)')


class PetDefaultValuesTest(TestCase):
    """Testes para valores padrão dos campos do modelo Pet"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user_defaults',
            email='defaults@test.com',
            password='testpass123'
        )
        
    def test_sexo_padrao_pet(self):
        """Teste: Sexo padrão do pet deve ser UNKNOWN"""
        pet = Pet.objects.create(
            nome='Charlie',
            especie='Hamster',
            tutor=self.user
        )
        
        self.assertEqual(pet.sexo, Pet.Gender.UNKNOWN)
        
    def test_campos_opcionais_defaults(self):
        """Teste: Campos opcionais devem ter valores padrão corretos"""
        pet = Pet.objects.create(
            nome='SimpleDoc',
            especie='Cão',
            tutor=self.user
        )
        
        # Campos que devem ser None por padrão
        self.assertIsNone(pet.raca)
        self.assertIsNone(pet.observacoes)
        self.assertIsNone(pet.data_de_nascimento)
        
        # Campo de foto deve estar vazio
        self.assertFalse(pet.foto)
        
        # Timestamps devem ser preenchidos automaticamente
        self.assertIsNotNone(pet.created_at)
        self.assertIsNotNone(pet.updated_at)


class PetChoicesValidationTest(TestCase):
    """Testes para validação de choices do modelo Pet"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user_choices',
            email='choices@test.com',
            password='testpass123'
        )
        
    def test_choices_sexo_pet_validos(self):
        """Teste: Todos os valores válidos para sexo do pet"""
        # Teste MALE
        pet_male = Pet.objects.create(
            nome='Max',
            especie='Cão',
            sexo=Pet.Gender.MALE,
            tutor=self.user
        )
        self.assertEqual(pet_male.sexo, Pet.Gender.MALE)
        
        # Teste FEMALE
        pet_female = Pet.objects.create(
            nome='Bella',
            especie='Gato',
            sexo=Pet.Gender.FEMALE,
            tutor=self.user
        )
        self.assertEqual(pet_female.sexo, Pet.Gender.FEMALE)
        
        # Teste UNKNOWN (padrão)
        pet_unknown = Pet.objects.create(
            nome='Mystery',
            especie='Pássaro',
            sexo=Pet.Gender.UNKNOWN,
            tutor=self.user
        )
        self.assertEqual(pet_unknown.sexo, Pet.Gender.UNKNOWN)


class PetBusinessLogicTest(TestCase):
    """Testes para lógicas de negócio específicas do modelo Pet"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user_logic',
            email='logic@test.com',
            password='testpass123'
        )
        
    def test_relacionamento_tutor_pet(self):
        """Teste: Relacionamento bidirecional entre tutor e pets"""
        pet1 = Pet.objects.create(
            nome='Pet1',
            especie='Cão',
            tutor=self.user
        )
        pet2 = Pet.objects.create(
            nome='Pet2',
            especie='Gato',
            tutor=self.user
        )
        
        # Verificar se o tutor tem os pets relacionados via related_name
        pets_do_tutor = self.user.pets.all()
        self.assertIn(pet1, pets_do_tutor)
        self.assertIn(pet2, pets_do_tutor)
        self.assertEqual(pets_do_tutor.count(), 2)
        
    def test_timestamps_automaticos(self):
        """Teste: Timestamps created_at e updated_at são automáticos"""
        pet = Pet.objects.create(
            nome='TimestampTest',
            especie='Pássaro',
            tutor=self.user
        )
        
        # Verificar se created_at foi definido
        self.assertIsNotNone(pet.created_at)
        
        # Salvar created_at original
        created_original = pet.created_at
        
        # Fazer uma atualização
        pet.observacoes = 'Atualizado'
        pet.save()
        
        # Verificar se updated_at foi atualizado mas created_at permanece igual
        self.assertEqual(pet.created_at, created_original)
        self.assertGreaterEqual(pet.updated_at, created_original)