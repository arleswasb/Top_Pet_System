# users/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Profile
from .serializers import UserSelfRegisterSerializer, UserDetailSerializer


class ProfileModelTest(TestCase):
    """Testes para o modelo Profile"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpassword123'
        )
    
    def test_profile_creation(self):
        """Testa criação de perfil"""
        # Profile já foi criado automaticamente pelo signal
        profile = self.user.profile
        profile.role = Profile.Role.CLIENTE
        profile.telefone = '(11) 99999-9999'
        profile.endereco = 'Rua Teste, 123'
        profile.save()
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.role, Profile.Role.CLIENTE)
        self.assertEqual(profile.telefone, '(11) 99999-9999')
        self.assertEqual(profile.endereco, 'Rua Teste, 123')
    
    def test_profile_str(self):
        """Testa representação string do perfil"""
        # Profile já foi criado automaticamente pelo signal
        profile = self.user.profile
        profile.role = Profile.Role.VETERINARIO
        profile.save()
        
        expected = f"{self.user.username} - {profile.get_role_display()}"
        self.assertEqual(str(profile), expected)
    
    def test_role_choices(self):
        """Testa choices do campo role"""
        expected_choices = [
            ('ADMIN', 'Admin'),
            ('FUNCIONARIO', 'Funcionário'),
            ('VETERINARIO', 'Veterinário'),
            ('CLIENTE', 'Cliente'),
        ]
        self.assertEqual(Profile.Role.choices, expected_choices)


class UserSelfRegisterTest(APITestCase):
    """Testes para auto-cadastro de usuários"""
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-register')
        
        self.valid_data = {
            'username': 'novouser',
            'password': 'senha123456',
            'confirm_password': 'senha123456',
            'email': 'novo@email.com',
            'first_name': 'Novo',
            'last_name': 'Usuario',
            'telefone': '(11) 88888-8888',
            'endereco': 'Rua Nova, 456'
        }
    
    def test_register_valid_user(self):
        """Testa cadastro válido de usuário"""
        response = self.client.post(self.url, self.valid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='novouser').exists())
        
        # Verifica se o perfil foi criado
        user = User.objects.get(username='novouser')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.role, Profile.Role.CLIENTE)
        self.assertEqual(user.profile.telefone, '(11) 88888-8888')
    
    def test_register_minimum_fields(self):
        """Testa cadastro apenas com campos obrigatórios"""
        minimal_data = {
            'username': 'userminimo',
            'password': 'senha123456',
            'confirm_password': 'senha123456',
            'email': 'minimo@email.com',
            'first_name': 'User',
            'last_name': 'Minimo'
        }
        
        response = self.client.post(self.url, minimal_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='userminimo')
        self.assertEqual(user.profile.telefone, '')
        self.assertEqual(user.profile.endereco, '')
    
    def test_register_password_mismatch(self):
        """Testa erro quando senhas não coincidem"""
        invalid_data = self.valid_data.copy()
        invalid_data['confirm_password'] = 'senhadiferente'
        
        response = self.client.post(self.url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data)
    
    def test_register_short_password(self):
        """Testa erro com senha muito curta"""
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = '123'
        invalid_data['confirm_password'] = '123'
        
        response = self.client.post(self.url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_register_duplicate_username(self):
        """Testa erro com username duplicado"""
        User.objects.create_user(username='novouser', email='outro@email.com')
        
        response = self.client.post(self.url, self.valid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_register_invalid_email(self):
        """Testa erro com email inválido"""
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'email_invalido'
        
        response = self.client.post(self.url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class UserAuthenticationTest(APITestCase):
    """Testes para autenticação de usuários"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpassword123'
        )
        # Atualizar perfil criado automaticamente pelo signal
        profile = self.user.profile
        profile.role = Profile.Role.CLIENTE
        profile.save()
        self.client = APIClient()
    
    def test_login_valid_credentials(self):
        """Testa login com credenciais válidas"""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'senhaerrada'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserPermissionsTest(APITestCase):
    """Testes para permissões de usuários"""
    
    def setUp(self):
        # Usuário administrador
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@email.com',
            password='admin123'
        )
        # Atualizar perfil criado automaticamente pelo signal
        admin_profile = self.admin_user.profile
        admin_profile.role = Profile.Role.ADMIN
        admin_profile.save()
        
        # Usuário funcionário
        self.funcionario_user = User.objects.create_user(
            username='funcionario',
            email='funcionario@email.com',
            password='func123'
        )
        # Atualizar perfil criado automaticamente pelo signal
        funcionario_profile = self.funcionario_user.profile
        funcionario_profile.role = Profile.Role.FUNCIONARIO
        funcionario_profile.save()
        
        # Usuário cliente
        self.cliente_user = User.objects.create_user(
            username='cliente',
            email='cliente@email.com',
            password='cliente123'
        )
        # Atualizar perfil criado automaticamente pelo signal
        cliente_profile = self.cliente_user.profile
        cliente_profile.role = Profile.Role.CLIENTE
        cliente_profile.save()
        
        self.client = APIClient()
    
    def test_admin_can_access_logs(self):
        """Testa que admin pode acessar logs"""
        token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = reverse('get-logs')
        response = self.client.get(url)
        
        # Pode retornar 200 (com logs) ou 404 (sem arquivo de log)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
    
    def test_funcionario_cannot_access_logs(self):
        """Testa que funcionário não pode acessar logs"""
        token = Token.objects.create(user=self.funcionario_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = reverse('get-logs')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_cliente_cannot_access_logs(self):
        """Testa que cliente não pode acessar logs"""
        token = Token.objects.create(user=self.cliente_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = reverse('get-logs')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserSerializerTest(TestCase):
    """Testes para serializers de usuários"""
    
    def test_user_self_register_serializer_valid(self):
        """Testa serializer de auto-cadastro com dados válidos"""
        data = {
            'username': 'testuser',
            'password': 'senha123456',
            'confirm_password': 'senha123456',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User',
            'telefone': '(11) 99999-9999',
            'endereco': 'Rua Teste, 123'
        }
        
        serializer = UserSelfRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.profile.role, Profile.Role.CLIENTE)
    
    def test_user_self_register_serializer_password_mismatch(self):
        """Testa erro no serializer quando senhas não coincidem"""
        data = {
            'username': 'testuser',
            'password': 'senha123456',
            'confirm_password': 'senhadiferente',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        serializer = UserSelfRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('confirm_password', serializer.errors)
    
    def test_user_detail_serializer(self):
        """Testa serializer de detalhes do usuário"""
        user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            first_name='Test',
            last_name='User'
        )
        # Atualizar perfil criado automaticamente pelo signal
        profile = user.profile
        profile.role = Profile.Role.CLIENTE
        profile.telefone = '(11) 99999-9999'
        profile.save()
        
        serializer = UserDetailSerializer(user)
        data = serializer.data
        
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@email.com')
        self.assertEqual(data['profile']['role'], Profile.Role.CLIENTE)
        self.assertEqual(data['profile']['telefone'], '(11) 99999-9999')


class UserFuncionarioViewSetTest(APITestCase):
    """Testes para o ViewSet de funcionários"""
    
    def setUp(self):
        # Usuário funcionário
        self.funcionario_user = User.objects.create_user(
            username='funcionario',
            email='funcionario@email.com',
            password='func123'
        )
        # Atualizar perfil criado automaticamente pelo signal
        funcionario_profile = self.funcionario_user.profile
        funcionario_profile.role = Profile.Role.FUNCIONARIO
        funcionario_profile.save()
        
        # Cliente para teste
        self.cliente_user = User.objects.create_user(
            username='cliente',
            email='cliente@email.com',
            password='cliente123'
        )
        # Atualizar perfil criado automaticamente pelo signal
        cliente_profile = self.cliente_user.profile
        cliente_profile.role = Profile.Role.CLIENTE
        cliente_profile.save()
        
        self.client = APIClient()
        token = Token.objects.create(user=self.funcionario_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_funcionario_can_list_clients(self):
        """Testa que funcionário pode listar clientes"""
        url = reverse('user-funcionario-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas o cliente
        self.assertEqual(response.data[0]['username'], 'cliente')
    
    def test_funcionario_can_create_client(self):
        """Testa que funcionário pode criar cliente"""
        url = reverse('user-funcionario-list')
        data = {
            'username': 'novocliente',
            'password': 'senha123456',
            'confirm_password': 'senha123456',
            'email': 'novocliente@email.com',
            'first_name': 'Novo',
            'last_name': 'Cliente',
            'role': Profile.Role.CLIENTE
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='novocliente').exists())
    
    def test_funcionario_can_update_client(self):
        """Testa que funcionário pode atualizar dados do cliente"""
        url = reverse('user-funcionario-detail', kwargs={'pk': self.cliente_user.pk})
        data = {
            'first_name': 'Novo Nome',
            'profile': {
                'telefone': '(11) 88888-8888'
            }
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cliente_user.refresh_from_db()
        self.assertEqual(self.cliente_user.first_name, 'Novo Nome')
    
    def test_funcionario_can_delete_client(self):
        """Testa que funcionário pode deletar cliente"""
        url = reverse('user-funcionario-detail', kwargs={'pk': self.cliente_user.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.cliente_user.pk).exists())

class UserAdminViewSetTest(APITestCase):
    """Testes para o ViewSet de administradores (/api/admin/users/)."""

    def setUp(self):
        # Usuário administrador que fará as requisições
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='adminpass'
        )
        self.admin_user.profile.role = Profile.Role.ADMIN
        self.admin_user.profile.save()

        # Usuário cliente para ser deletado
        self.cliente_user = User.objects.create_user(
            username='cliente_a_deletar',
            email='cliente@test.com',
            password='clientepass'
        )
        self.cliente_user.profile.role = Profile.Role.CLIENTE
        self.cliente_user.profile.save()

        self.client = APIClient()
        token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_admin_can_delete_client(self):
        """Testa que um administrador pode deletar um usuário cliente."""
        # A URL correta para o endpoint de admin
        url = reverse('user-admin-detail', kwargs={'pk': self.cliente_user.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.cliente_user.pk).exists())   