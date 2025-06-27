# pets/tests_unidade.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, timedelta
from decimal import Decimal

from .models import Pet
from users.models import Profile


class PetModelTest(TestCase):
    """Testes unitários para o modelo Pet"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='test_tutor',
            email='tutor@test.com',
            password='testpass123'
        )
        # Profile é criado automaticamente pelo signal
        
    def test_criar_pet_valido(self):
        """Teste: Criar um pet com dados válidos"""
        pet = Pet.objects.create(
            nome='Buddy',
            especie='Cão',
            raca='Golden Retriever',
            data_de_nascimento=date(2020, 1, 15),
            sexo=Pet.Gender.MALE,
            tutor=self.user,
            observacoes='Pet muito amigável'
        )
        
        self.assertEqual(pet.nome, 'Buddy')
        self.assertEqual(pet.especie, 'Cão')
        self.assertEqual(pet.raca, 'Golden Retriever')
        self.assertEqual(pet.sexo, Pet.Gender.MALE)
        self.assertEqual(pet.tutor, self.user)
        self.assertIsNotNone(pet.created_at)
        self.assertIsNotNone(pet.updated_at)
        
    def test_pet_str_representation(self):
        """Teste: Representação string do pet"""
        pet = Pet.objects.create(
            nome='Mia',
            especie='Gato',
            tutor=self.user
        )
        
        self.assertEqual(str(pet), 'Mia (Gato)')
        
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
            
    def test_calculo_idade_pet_exata(self):
        """Teste: Cálculo exato da idade do pet"""
        from unittest.mock import patch
        from datetime import date
        
        # Simular data atual específica para teste consistente
        data_atual_mock = date(2025, 6, 27)  # Data atual do teste
        
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
        from unittest.mock import patch
        from datetime import date
        
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
        from unittest.mock import patch
        from datetime import date
        
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
        from unittest.mock import patch
        from datetime import date
        
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
        
    def test_sexo_padrao_pet(self):
        """Teste: Sexo padrão do pet deve ser DESCONHECIDO"""
        pet = Pet.objects.create(
            nome='Charlie',
            especie='Hamster',
            tutor=self.user
        )
        
        self.assertEqual(pet.sexo, Pet.Gender.UNKNOWN)
        
    def test_choices_sexo_pet(self):
        """Teste: Choices válidos para sexo do pet"""
        # Teste MACHO
        pet_male = Pet.objects.create(
            nome='Max',
            especie='Cão',
            sexo=Pet.Gender.MALE,
            tutor=self.user
        )
        self.assertEqual(pet_male.sexo, Pet.Gender.MALE)
        
        # Teste FEMEA
        pet_female = Pet.objects.create(
            nome='Bella',
            especie='Gato',
            sexo=Pet.Gender.FEMALE,
            tutor=self.user
        )
        self.assertEqual(pet_female.sexo, Pet.Gender.FEMALE)
        
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
            
    def test_relacionamento_tutor_pet(self):
        """Teste: Relacionamento entre tutor e pets"""
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
        
        # Verificar se o tutor tem os pets relacionados
        pets_do_tutor = self.user.pets.all()
        self.assertIn(pet1, pets_do_tutor)
        self.assertIn(pet2, pets_do_tutor)
        self.assertEqual(pets_do_tutor.count(), 2)
        
    def test_observacoes_opcionais(self):
        """Teste: Observações são opcionais"""
        pet_sem_obs = Pet.objects.create(
            nome='SimpleDoc',
            especie='Cão',
            tutor=self.user
        )
        
        pet_com_obs = Pet.objects.create(
            nome='DetailedDoc',
            especie='Gato',
            tutor=self.user,
            observacoes='Muito detalhado'
        )
        
        self.assertIsNone(pet_sem_obs.observacoes)
        self.assertEqual(pet_com_obs.observacoes, 'Muito detalhado')
        
    def test_raca_opcional(self):
        """Teste: Raça é opcional"""
        pet = Pet.objects.create(
            nome='MixedBreed',
            especie='Cão',
            tutor=self.user
        )
        
        self.assertIsNone(pet.raca)
        
    def test_foto_opcional(self):
        """Teste: Foto é opcional"""
        pet = Pet.objects.create(
            nome='NoPhoto',
            especie='Gato',
            tutor=self.user
        )
        
        self.assertFalse(pet.foto)  # Campo vazio
        
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


class PetValidationTest(TestCase):
    """Testes específicos de validação do modelo Pet"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='validation_user',
            email='validation@test.com',
            password='testpass123'
        )
        # Profile é criado automaticamente pelo signal
        
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


class PetQueryTest(TestCase):
    """Testes de consultas e filtros do modelo Pet"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tutor1',
            email='tutor1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='tutor2', 
            email='tutor2@test.com',
            password='testpass123'
        )
        
        # Profiles são criados automaticamente pelo signal
        
        # Criar pets para teste
        Pet.objects.create(nome='Dog1', especie='Cão', tutor=self.user1)
        Pet.objects.create(nome='Cat1', especie='Gato', tutor=self.user1)
        Pet.objects.create(nome='Dog2', especie='Cão', tutor=self.user2)
        
    def test_filtrar_pets_por_tutor(self):
        """Teste: Filtrar pets por tutor"""
        pets_user1 = Pet.objects.filter(tutor=self.user1)
        pets_user2 = Pet.objects.filter(tutor=self.user2)
        
        self.assertEqual(pets_user1.count(), 2)
        self.assertEqual(pets_user2.count(), 1)
        
    def test_filtrar_pets_por_especie(self):
        """Teste: Filtrar pets por espécie"""
        caes = Pet.objects.filter(especie='Cão')
        gatos = Pet.objects.filter(especie='Gato')
        
        self.assertEqual(caes.count(), 2)
        self.assertEqual(gatos.count(), 1)
        
    def test_total_pets(self):
        """Teste: Contar total de pets"""
        total = Pet.objects.count()
        self.assertEqual(total, 3)