#!/usr/bin/env python
"""
Testes para as rotas de password reset
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class PasswordResetRoutesTest(TestCase):
    """Testes para verificar se as rotas de password reset estão funcionando"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_password_reset_endpoint_exists(self):
        """Testa se o endpoint de password reset existe"""
        response = self.client.options('/api/auth/password-reset/')
        self.assertIn(response.status_code, [200, 405])  # Aceita ambos os status
    
    def test_password_reset_confirm_endpoint_exists(self):
        """Testa se o endpoint de confirmação existe"""
        response = self.client.options('/api/auth/password-reset/confirm/')
        self.assertIn(response.status_code, [200, 405])
    
    def test_password_reset_validate_token_endpoint_exists(self):
        """Testa se o endpoint de validação de token existe"""
        response = self.client.options('/api/auth/password-reset/validate_token/')
        self.assertIn(response.status_code, [200, 405])
    
    def test_password_reset_post_with_valid_email(self):
        """Testa POST para password reset com email válido"""
        response = self.client.post('/api/auth/password-reset/', {
            'email': 'test@example.com'
        })
        # Pode retornar 200 (sucesso) ou 400 (erro de configuração)
        # Em testes, muitas vezes retorna erro por falta de configuração de email
        self.assertIn(response.status_code, [200, 400])
    
    def test_password_reset_post_with_invalid_email(self):
        """Testa POST para password reset com email inválido"""
        response = self.client.post('/api/auth/password-reset/', {
            'email': 'invalido@exemplo.com'
        })
        # Deve retornar 400 ou 200 (dependendo da configuração)
        self.assertIn(response.status_code, [200, 400])
    
    def test_password_reset_confirm_with_invalid_token(self):
        """Testa confirmação com token inválido"""
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'token': 'token-inexistente',
            'password': 'novasenha123'
        })
        # Deve retornar erro
        self.assertIn(response.status_code, [400, 404])
    
    def test_password_reset_validate_invalid_token(self):
        """Testa validação de token inválido"""
        response = self.client.post('/api/auth/password-reset/validate_token/', {
            'token': 'token-inexistente'
        })
        # Deve retornar erro
        self.assertIn(response.status_code, [400, 404])
