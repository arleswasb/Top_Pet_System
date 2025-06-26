from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User, Profile

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    """Fixture para criar um cliente de API."""
    return APIClient()

# --- Testes para a API de Criação de Usuário ---

def test_create_user_api(api_client):
    """Testa a criação de um novo usuário via API."""
    url = reverse('user-register') # CORRIGIDO: de 'user-create' para 'user-register'
    data = {
        'username': 'newuser',
        'password': 'newpassword123',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().username == 'newuser'
    assert Profile.objects.count() == 1
    assert Profile.objects.get().role == Profile.Role.CLIENTE

def test_create_user_api_missing_fields(api_client):
    """Testa a falha na criação de usuário com campos faltando."""
    url = reverse('user-register') # CORRIGIDO: de 'user-create' para 'user-register'
    data = {
        'username': 'anotheruser'
        # Faltando a senha
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0

# --- Testes para o Modelo Profile ---

def test_profile_creation_signal():
    """
    Testa se um Profile é criado automaticamente quando um User é criado.
    """
    # O UserCreateSerializer deve criar o Profile automaticamente.
    user = User.objects.create_user(username='testsignal', password='password')
    
    # CORRIGIDO: Apenas verifica se o profile foi criado, não tenta criar de novo.
    assert hasattr(user, 'profile')
    assert user.profile is not None
    assert user.profile.role == Profile.Role.CLIENTE

def test_profile_str_representation():
    """Testa a representação em string do modelo Profile."""
    user = User.objects.create_user(username='stringuser', password='password')
    
    # CORRIGIDO: Atualiza o profile existente em vez de tentar criar um novo.
    profile = user.profile
    profile.role = Profile.Role.ADMIN
    profile.save()
    
    assert str(user.profile) == 'stringuser - Admin'
