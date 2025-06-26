import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from users.models import User
from pets.models import Pet
from .models import Servico, Agendamento

# Marca todos os testes neste arquivo para usar o banco de dados
pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    """Fixture para criar um cliente de API."""
    return APIClient()

@pytest.fixture
def test_user():
    """Fixture para criar um usuário de teste."""
    return User.objects.create_user(username='testuser', password='testpassword123')

@pytest.fixture
def authenticated_client(api_client, test_user):
    """Fixture para criar um cliente de API autenticado."""
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.fixture
def test_pet(test_user):
    """Fixture para criar um pet de teste."""
    return Pet.objects.create(
        nome='Miau',
        tutor=test_user,
        especie='Gato',
        raca='SRD',
        data_de_nascimento=timezone.now().date() - timedelta(days=365 * 2) # 2 anos
    )

@pytest.fixture
def test_servico():
    """Fixture para criar um serviço de teste."""
    return Servico.objects.create(
        nome='Banho e Tosa',
        descricao='Um banho completo e tosa higiênica.',
        duracao=timedelta(hours=1),
        preco=80.00
    )

# --- Testes para o modelo Agendamento ---

def test_create_agendamento(test_pet, test_servico):
    """Testa a criação de uma instância do modelo Agendamento."""
    data_hora_agendamento = timezone.now() + timedelta(days=5)
    agendamento = Agendamento.objects.create(
        pet=test_pet,
        servico=test_servico,
        data_hora=data_hora_agendamento,
        status='AGENDADO'
    )
    assert agendamento.pet.nome == 'Miau'
    assert agendamento.servico.nome == 'Banho e Tosa'
    assert Agendamento.objects.count() == 1
    assert str(agendamento) == f"Banho e Tosa para Miau em {data_hora_agendamento.strftime('%d/%m/%Y %H:%M')}"

# --- Testes para a API de Agendamentos ---

def test_list_agendamentos(authenticated_client, test_pet, test_servico):
    """Testa a listagem de agendamentos via API."""
    Agendamento.objects.create(
        pet=test_pet,
        servico=test_servico,
        data_hora=timezone.now() + timedelta(days=2)
    )
    url = reverse('agendamento-list')
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    # Acessando o nome do pet através do campo 'pet' que é um dicionário
    assert response.data[0]['pet']['nome'] == 'Miau'

def test_create_agendamento_api(authenticated_client, test_pet, test_servico):
    """Testa a criação de um agendamento via API."""
    url = reverse('agendamento-list')
    data = {
        'pet_id': test_pet.pk,
        'servico_id': test_servico.pk,
        'data_hora': (timezone.now() + timedelta(days=3)).isoformat(),
        'observacoes': 'Pet um pouco ansioso.'
    }
    response = authenticated_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Agendamento.objects.count() == 1
    assert response.data['pet']['id'] == test_pet.pk
    assert response.data['observacoes'] == 'Pet um pouco ansioso.'

def test_retrieve_agendamento(authenticated_client, test_pet, test_servico):
    """Testa a busca de um agendamento específico via API."""
    agendamento = Agendamento.objects.create(
        pet=test_pet,
        servico=test_servico,
        data_hora=timezone.now() + timedelta(days=4)
    )
    url = reverse('agendamento-detail', kwargs={'pk': agendamento.pk})
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == agendamento.pk

def test_update_agendamento_status(authenticated_client, test_pet, test_servico):
    """Testa a atualização do status de um agendamento via API."""
    agendamento = Agendamento.objects.create(
        pet=test_pet,
        servico=test_servico,
        data_hora=timezone.now() + timedelta(days=1)
    )
    url = reverse('agendamento-detail', kwargs={'pk': agendamento.pk})
    data = {'status': 'CANCELADO'}
    response = authenticated_client.patch(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'CANCELADO'
    agendamento.refresh_from_db()
    assert agendamento.status == 'CANCELADO'

def test_delete_agendamento(authenticated_client, test_pet, test_servico):
    """Testa a exclusão de um agendamento via API."""
    agendamento = Agendamento.objects.create(
        pet=test_pet,
        servico=test_servico,
        data_hora=timezone.now()
    )
    url = reverse('agendamento-detail', kwargs={'pk': agendamento.pk})
    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Agendamento.objects.count() == 0
