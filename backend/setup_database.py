#!/usr/bin/env python3
"""
Script para configurar o banco de dados do Top Pet System
Cria superusuário e aplica migrações necessárias
"""

import os
import sys
import django

# Configurar Django ANTES de qualquer import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

# Agora pode importar modelos Django
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

def run_migrations():
    """Aplica todas as migrações pendentes"""
    print("🔄 Aplicando migrações do banco de dados...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrações aplicadas com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao aplicar migrações: {e}")
        return False

def create_superuser():
    """Cria um superusuário se não existir"""
    print("👤 Verificando superusuário...")
    
    username = 'admin'
    email = 'admin@toppet.com'
    password = 'admin123'
    
    try:
        # Verificar se já existe
        if User.objects.filter(username=username).exists():
            print(f"ℹ️  Superusuário '{username}' já existe.")
            return True
        
        # Criar superusuário
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Administrador',
            last_name='Sistema'
        )
        user.role = 'Admin'
        user.save()
        print(f"✅ Superusuário criado:")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        return False

def create_test_user():
    """Cria um usuário de teste para a simulação"""
    print("🧪 Criando usuário de teste...")
    
    username = 'teste_api'
    email = 'teste@toppet.com'
    password = 'senha123'
    
    try:
        # Verificar se já existe
        if User.objects.filter(username=username).exists():
            print(f"ℹ️  Usuário de teste '{username}' já existe.")
            return True
        
        # Criar usuário de teste
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Usuário',
            last_name='Teste'
        )
        print(f"✅ Usuário de teste criado:")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário de teste: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 CONFIGURAÇÃO DO BANCO DE DADOS - TOP PET SYSTEM")
    print("=" * 55)
    
    success = True
    
    # Aplicar migrações
    if not run_migrations():
        success = False
    
    # Criar superusuário
    if not create_superuser():
        success = False
    
    # Criar usuário de teste
    if not create_test_user():
        success = False
    
    if success:
        print("\n✅ Configuração concluída com sucesso!")
        print("🎯 O banco está pronto para uso.")
        print("\n📋 Credenciais disponíveis:")
        print("   Admin: admin / admin123")
        print("   Teste: teste_api / senha123")
    else:
        print("\n❌ Houve erros na configuração.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
