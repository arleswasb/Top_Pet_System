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
        # Cria um usuário comum (sem profile/role específico)
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
        
        # Cria um usuário funcionário
        self.funcionario_user = User.objects.create_user(
            username='funcionario',
            email='funcionario@example.com',
            password='funcionario123'
        )
        
        # Criar os Profiles
        from users.models import Profile
        
        # Profile ADMIN para o superuser
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
            
        # Profile FUNCIONARIO para o funcionário
        if hasattr(self.funcionario_user, 'profile'):
            self.funcionario_user.profile.role = Profile.Role.FUNCIONARIO
            self.funcionario_user.profile.save()
        else:
            Profile.objects.create(
                user=self.funcionario_user,
                role=Profile.Role.FUNCIONARIO
            )
        
        # URLs que serão usadas nos testes
        self.horarios_list_url = reverse('horariofuncionamento-list')
        self.feriados_list_url = reverse('feriado-list')

# --- Testes para o endpoint de Horários de Funcionamento ---

class HorarioFuncionamentoPermissionTests(ConfiguracaoAPITests):

    def test_anonymous_user_cannot_access_horarios(self):
        response = self.client.get(self.horarios_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_common_user_cannot_view_horarios(self):
        """Usuário comum (sem role específico) não pode visualizar horários"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.horarios_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_funcionario_can_view_horarios(self):
        """Funcionário pode visualizar horários"""
        self.client.force_authenticate(user=self.funcionario_user)
        response = self.client.get(self.horarios_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_list_horarios(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.horarios_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_create_horario(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "dia_semana": 0,
            "hora_abertura": "09:00:00",
            "hora_fechamento": "18:00:00",
            "ativo": True
        }
        response = self.client.post(self.horarios_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HorarioFuncionamento.objects.count(), 1)
        self.assertEqual(HorarioFuncionamento.objects.get().dia_semana, 0)

    def test_funcionario_cannot_create_horario(self):
        """Funcionário não pode criar horários (apenas admin pode)"""
        self.client.force_authenticate(user=self.funcionario_user)
        data = {
            "dia_semana": 2,
            "hora_abertura": "09:00:00",
            "hora_fechamento": "18:00:00",
            "ativo": True
        }
        response = self.client.post(self.horarios_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_validation_hora_fechamento_before_abertura(self):
        """Teste de validação: hora fechamento deve ser posterior à abertura"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "dia_semana": 1,
            "hora_abertura": "18:00:00",
            "hora_fechamento": "09:00:00",  # Erro: fechamento antes da abertura
            "ativo": True
        }
        response = self.client.post(self.horarios_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hora_fechamento', response.data)

# --- Testes para o endpoint de Feriados ---

class FeriadoPermissionTests(ConfiguracaoAPITests):

    def test_anonymous_user_cannot_access_feriados(self):
        response = self.client.get(self.feriados_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_common_user_cannot_view_feriados(self):
        """Usuário comum (sem role específico) não pode visualizar feriados"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.feriados_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_funcionario_can_view_feriados(self):
        """Funcionário pode visualizar feriados"""
        self.client.force_authenticate(user=self.funcionario_user)
        response = self.client.get(self.feriados_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_funcionario_cannot_create_feriado(self):
        """Funcionário não pode criar feriados (apenas admin pode)"""
        self.client.force_authenticate(user=self.funcionario_user)
        data = {
            "nome": "Feriado Funcionário",
            "data": "2026-07-01"
        }
        response = self.client.post(self.feriados_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_validation_data_passado(self):
        """Teste de validação: data não pode ser no passado"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "nome": "Feriado Passado",
            "data": "2020-01-01"  # Data no passado
        }
        response = self.client.post(self.feriados_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data', response.data)
    
    def test_validation_nome_muito_curto(self):
        """Teste de validação: nome deve ter pelo menos 3 caracteres"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "nome": "AA",  # Nome muito curto
            "data": "2026-01-01"
        }
        response = self.client.post(self.feriados_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nome', response.data)