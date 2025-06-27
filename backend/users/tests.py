from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils.crypto import get_random_string
from .models import Profile

# Create your tests here.

class UsersTestCase(TestCase):
    def test_sample(self):
        self.assertEqual(1, 1)
    
    def test_user_profile_creation(self):
        """Teste criação de usuário e perfil"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Verificar se o profile foi criado automaticamente via signal
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.role, Profile.Role.CLIENTE)
    
    def test_profile_string_representation(self):
        """Teste representação string do perfil"""
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        expected_str = f"{user.username} - {user.profile.get_role_display()}"
        self.assertEqual(str(user.profile), expected_str)
    
    def test_profile_role_choices(self):
        """Teste opções de papel do usuário"""
        self.assertEqual(Profile.Role.ADMIN, "ADMIN")
        self.assertEqual(Profile.Role.FUNCIONARIO, "FUNCIONARIO")
        self.assertEqual(Profile.Role.CLIENTE, "CLIENTE")
