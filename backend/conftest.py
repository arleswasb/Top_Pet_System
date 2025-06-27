import pytest
from django.contrib.auth.models import User
from users.models import Profile
from pets.models import Pet
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Cliente API para testes"""
    return APIClient()


@pytest.fixture
def admin_user(db):
    """Usuário administrador para testes"""
    user = User.objects.create_user(
        username='admin_test',
        email='admin@test.com',
        password='admin123',
        is_staff=True,
        is_superuser=True
    )
    user.profile.role = Profile.Role.ADMIN
    user.profile.save()
    return user


@pytest.fixture
def funcionario_user(db):
    """Usuário funcionário para testes"""
    user = User.objects.create_user(
        username='funcionario_test',
        email='funcionario@test.com',
        password='func123'
    )
    user.profile.role = Profile.Role.FUNCIONARIO
    user.profile.save()
    return user


@pytest.fixture
def cliente_user(db):
    """Usuário cliente para testes"""
    user = User.objects.create_user(
        username='cliente_test',
        email='cliente@test.com',
        password='cliente123'
    )
    user.profile.role = Profile.Role.CLIENTE
    user.profile.save()
    return user


@pytest.fixture
def veterinario_user(db):
    """Usuário veterinário para testes"""
    user = User.objects.create_user(
        username='veterinario_test',
        email='veterinario@test.com',
        password='vet123'
    )
    user.profile.role = Profile.Role.VETERINARIO
    user.profile.save()
    return user


@pytest.fixture
def pet_data():
    """Dados básicos para criar um pet"""
    return {
        'nome': 'Rex Test',
        'especie': 'Cachorro',
        'sexo': Pet.Gender.MALE,
        'data_de_nascimento': '2020-01-01'
    }


@pytest.fixture
def pet(db, cliente_user, pet_data):
    """Pet de teste"""
    return Pet.objects.create(
        tutor=cliente_user,
        **pet_data
    )
