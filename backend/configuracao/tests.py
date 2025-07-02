# backend/configuracao/tests.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import HorarioFuncionamento, Feriado

# Pega o modelo de usuário ativo do projeto (seja ele o padrão ou customizado)
User = get_user_model()

class ConfiguracaoAPITests(APITestCase):
    """
    Classe base de testes que cria os usuários necessários
    para os testes de permissão.
    """
    def setUp(self):
        # Cria um usuário comum
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        # Cria um usuário administrador com Profile
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123'
        )
        
        # Criar o Profile ADMIN para o superuser
        from users.models import Profile
        if hasattr(self.admin_user, 'profile'):
            # Se já existe um profile (criado por signal), atualiza o role
            self.admin_user.profile.role = Profile.Role.ADMIN
            self.admin_user.profile.save()
        else:
            # Se não existe, cria um novo profile
            Profile.objects.create(
                user=self.admin_user,
                role=Profile.Role.ADMIN
            )
        
        # URLs que serão usadas nos testes
        self.horarios_list_url = reverse('horariofuncionamento-list')
        self.feriados_list_url = reverse('feriado-list')

# --- Testes para o endpoint de Horários de Funcionamento ---

class HorarioFuncionamentoPermissionTests(ConfiguracaoAPITests):

    def test_anonymous_user_cannot_access_horarios(self):
        response = self.client.get(self.horarios_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_common_user_cannot_access_horarios(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.horarios_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_list_horarios(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.horarios_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_create_horario(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "dia_semana": 0,  # Corrigir nome do campo
            "hora_abertura": "09:00:00",  # Corrigir nome do campo
            "hora_fechamento": "18:00:00",  # Corrigir nome do campo
            "ativo": True
        }
        response = self.client.post(self.horarios_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HorarioFuncionamento.objects.count(), 1)
        self.assertEqual(HorarioFuncionamento.objects.get().dia_semana, 0)


# --- Testes para o endpoint de Feriados ---

class FeriadoPermissionTests(ConfiguracaoAPITests):

    def test_anonymous_user_cannot_access_feriados(self):
        response = self.client.get(self.feriados_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_common_user_cannot_access_feriados(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.feriados_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_list_feriados(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.feriados_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_user_can_create_feriado(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "nome": "Ano Novo",
            "data": "2026-01-01"
        }
        response = self.client.post(self.feriados_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feriado.objects.count(), 1)
        self.assertEqual(Feriado.objects.get().nome, "Ano Novo")