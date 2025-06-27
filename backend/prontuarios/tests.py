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

User = get_user_model()


class ProntuarioBasicTest(TestCase):
    """Testes básicos para o módulo Prontuarios"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário tutor
        self.tutor = User.objects.create_user(
            username='tutor_test',
            email='tutor@test.com',
            password='testpass123'
        )
        
        # Criar usuário veterinário
        self.veterinario = User.objects.create_user(
            username='vet_test',
            email='vet@test.com',
            password='testpass123'
        )
        
        # Configurar perfis
        Profile.objects.filter(user=self.tutor).update(role=Profile.Role.CLIENTE)
        Profile.objects.filter(user=self.veterinario).update(role=Profile.Role.FUNCIONARIO)
        
        # Criar pet
        self.pet = Pet.objects.create(
            nome='Rex',
            especie='Cachorro',
            raca='Labrador',
            data_de_nascimento=date(2021, 1, 1),
            sexo=Pet.Gender.MALE,
            tutor=self.tutor
        )
    
    def test_basic_setup(self):
        """Teste básico para verificar se o setup está funcionando"""
        self.assertEqual(self.pet.nome, 'Rex')
        self.assertEqual(self.tutor.username, 'tutor_test')
        self.assertEqual(self.veterinario.username, 'vet_test')
        
    def test_pet_creation(self):
        """Teste básico de criação de pet"""
        pet = Pet.objects.create(
            nome='Mimi',
            especie='Gato',
            tutor=self.tutor
        )
        self.assertEqual(pet.nome, 'Mimi')
        self.assertEqual(pet.especie, 'Gato')
        
    def test_user_profiles(self):
        """Teste verificação de perfis de usuário"""
        tutor_profile = Profile.objects.get(user=self.tutor)
        vet_profile = Profile.objects.get(user=self.veterinario)
        
        self.assertEqual(tutor_profile.role, Profile.Role.CLIENTE)
        self.assertEqual(vet_profile.role, Profile.Role.FUNCIONARIO)