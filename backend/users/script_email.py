#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.core.mail import send_mail
from django.contrib.auth.models import User

def test_email():
    """Testa o envio de email"""
    print("=== Teste de Envio de Email ===")
    
    try:
        # Teste básico de email
        result = send_mail(
            subject='Teste - Top Pet System',
            message='Este é um email de teste do sistema Top Pet.',
            from_email='admin@toppetsystem.com',
            recipient_list=['teste@example.com'],
            fail_silently=False,
        )
        
        print(f"✅ Email enviado com sucesso! Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")

def test_password_reset():
    """Testa o reset de senha"""
    print("\n=== Teste de Reset de Senha ===")
    
    try:
        # Criar usuário de teste se não existir
        user, created = User.objects.get_or_create(
            username='teste_email',
            defaults={
                'email': 'teste@example.com',
                'first_name': 'Usuario',
                'last_name': 'Teste'
            }
        )
        
        if created:
            user.set_password('senha123')
            user.save()
            print(f"✅ Usuário de teste criado: {user.username}")
        else:
            print(f"ℹ️ Usuário de teste já existe: {user.username}")
        
        # Importar e testar o reset de senha
        from django_rest_passwordreset.models import ResetPasswordToken
        
        # Criar token
        token = ResetPasswordToken.objects.create(user=user)
        print(f"✅ Token criado: {token.key[:10]}...")
        
        # Simular envio do email de reset
        from django_rest_passwordreset.signals import reset_password_token_created
        
        print("📧 Simulando envio de email de reset...")
        
    except Exception as e:
        print(f"❌ Erro no teste de reset: {e}")

if __name__ == '__main__':
    test_email()
    test_password_reset()
    print("\n🎯 Teste concluído!")
