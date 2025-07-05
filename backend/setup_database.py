#!/usr/bin/env python3
"""
Script para configurar o banco de dados do Top Pet System
Cria superusuário e usuários com diferentes perfis para testar regras de negócio
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
from users.models import Profile

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

def create_user_with_profile(username, email, password, first_name, last_name, role, is_superuser=False):
    """Cria um usuário com perfil específico"""
    try:
        # Verificar se já existe
        if User.objects.filter(username=username).exists():
            print(f"ℹ️  Usuário '{username}' já existe.")
            return True
        
        # Criar usuário
        if is_superuser:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        
        # Criar ou atualizar perfil
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()
        
        print(f"✅ Usuário {role} criado:")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   Role: {role}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário {role}: {e}")
        return False

def create_all_users():
    """Cria todos os usuários necessários para testes"""
    print("👥 Criando usuários com diferentes perfis...")
    
    users = [
        {
            'username': 'admin',
            'email': 'admin@toppet.com',
            'password': 'admin123',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'role': Profile.Role.ADMIN,
            'is_superuser': True
        },
        {
            'username': 'veterinario',
            'email': 'vet@toppet.com',
            'password': 'vet123',
            'first_name': 'Dr. João',
            'last_name': 'Veterinário',
            'role': Profile.Role.VETERINARIO,
            'is_superuser': False
        },
        {
            'username': 'funcionario',
            'email': 'func@toppet.com',
            'password': 'func123',
            'first_name': 'Maria',
            'last_name': 'Funcionária',
            'role': Profile.Role.FUNCIONARIO,
            'is_superuser': False
        },
        {
            'username': 'cliente',
            'email': 'cliente@toppet.com',
            'password': 'cliente123',
            'first_name': 'Carlos',
            'last_name': 'Cliente',
            'role': Profile.Role.CLIENTE,
            'is_superuser': False
        },
        {
            'username': 'teste_api',
            'email': 'teste@toppet.com',
            'password': 'senha123',
            'first_name': 'Usuário',
            'last_name': 'Teste',
            'role': Profile.Role.CLIENTE,
            'is_superuser': False
        }
    ]
    
    success = True
    for user_data in users:
        if not create_user_with_profile(**user_data):
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
    
    # Criar usuários com diferentes perfis
    if not create_all_users():
        success = False
    
    if success:
        print("\n✅ Configuração concluída com sucesso!")
        print("🎯 O banco está pronto para uso com todos os perfis.")
        print("\n📋 Credenciais disponíveis:")
        print("   Admin:       admin / admin123")
        print("   Veterinário: veterinario / vet123")
        print("   Funcionário: funcionario / func123")
        print("   Cliente:     cliente / cliente123")
        print("   Teste API:   teste_api / senha123")
        print("\n🔐 Todas as senhas são para ambiente de desenvolvimento/teste!")
    else:
        print("\n❌ Houve erros na configuração.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
