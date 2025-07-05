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
        print(f"✅ Superusuário criado:")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        return False

def create_test_users():
    """Cria usuários de teste com diferentes perfis para simulação"""
    print("🧪 Criando usuários de teste com diferentes perfis...")
    
    test_users = [
        {
            'username': 'cliente_teste',
            'email': 'cliente@toppet.com',
            'password': 'cliente123',
            'first_name': 'João',
            'last_name': 'Cliente',
            'role': 'Cliente',
            'is_staff': False
        },
        {
            'username': 'veterinario_teste',
            'email': 'veterinario@toppet.com',
            'password': 'vet123',
            'first_name': 'Dr. Maria',
            'last_name': 'Veterinária',
            'role': 'Veterinario',
            'is_staff': True
        },
        {
            'username': 'funcionario_teste',
            'email': 'funcionario@toppet.com',
            'password': 'func123',
            'first_name': 'Ana',
            'last_name': 'Funcionária',
            'role': 'Funcionario',
            'is_staff': True
        },
        {
            'username': 'admin_teste',
            'email': 'admin_teste@toppet.com',
            'password': 'admin123',
            'first_name': 'Carlos',
            'last_name': 'Administrador',
            'role': 'Admin',
            'is_staff': True
        }
    ]
    
    success = True
    
    for user_data in test_users:
        try:
            # Verificar se já existe
            if User.objects.filter(username=user_data['username']).exists():
                print(f"ℹ️  Usuário '{user_data['username']}' ({user_data['role']}) já existe.")
                continue
            
            # Criar usuário
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_staff=user_data['is_staff']
            )
            
            # Verificar se tem model Profile e criar
            try:
                from users.models import Profile
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'role': user_data['role']}
                )
                if created:
                    print(f"✅ Usuário {user_data['role']} criado:")
                    print(f"   Username: {user_data['username']}")
                    print(f"   Email: {user_data['email']}")
                    print(f"   Password: {user_data['password']}")
                    print(f"   Role: {user_data['role']}")
            except ImportError:
                # Se não tem model Profile, salvar role no próprio user (se campo existir)
                if hasattr(user, 'role'):
                    user.role = user_data['role']
                    user.save()
                print(f"✅ Usuário {user_data['role']} criado:")
                print(f"   Username: {user_data['username']}")
                print(f"   Email: {user_data['email']}")
                print(f"   Password: {user_data['password']}")
                print(f"   Role: {user_data['role']}")
            
        except Exception as e:
            print(f"❌ Erro ao criar usuário {user_data['username']}: {e}")
            success = False
    
    return success

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
    
    # Criar usuários de teste com diferentes perfis
    if not create_test_users():
        success = False
    
    if success:
        print("\n✅ Configuração concluída com sucesso!")
        print("🎯 O banco está pronto para uso.")
        print("\n📋 Credenciais disponíveis:")
        print("   🔑 Admin Principal: admin / admin123")
        print("   👤 Cliente: cliente_teste / cliente123")
        print("   🩺 Veterinário: veterinario_teste / vet123")
        print("   👥 Funcionário: funcionario_teste / func123")
        print("   ⚡ Admin Teste: admin_teste / admin123")
    else:
        print("\n❌ Houve erros na configuração.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
