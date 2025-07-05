#!/usr/bin/env python3
"""
Script para verificar e corrigir autenticação dos usuários
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from users.models import Profile

def check_user_auth():
    """Verifica autenticação de todos os usuários"""
    print("🔍 VERIFICAÇÃO DE AUTENTICAÇÃO DOS USUÁRIOS")
    print("=" * 50)
    
    # Listar todos os usuários
    users = User.objects.all()
    print(f"\nTotal de usuários no banco: {users.count()}")
    
    for user in users:
        print(f"\n--- Usuário: {user.username} ---")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Ativo: {user.is_active}")
        print(f"Staff: {user.is_staff}")
        print(f"Superuser: {user.is_superuser}")
        print(f"Último login: {user.last_login}")
        print(f"Data criação: {user.date_joined}")
        
        # Verificar perfil
        try:
            profile = user.profile
            print(f"Perfil role: {profile.role}")
        except Profile.DoesNotExist:
            print("❌ Perfil não encontrado!")
        
        # Testar senhas comuns
        common_passwords = [
            'admin123', 'vet123', 'func123', 'cliente123',
            'admin', 'veterinario', 'funcionario', 'cliente',
            '123456', 'password'
        ]
        
        auth_success = False
        for password in common_passwords:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                print(f"✅ Senha correta: {password}")
                auth_success = True
                break
        
        if not auth_success:
            print("❌ Nenhuma senha comum funcionou")

def reset_user_passwords():
    """Redefine senhas dos usuários principais"""
    print("\n\n🔧 REDEFININDO SENHAS DOS USUÁRIOS")
    print("=" * 50)
    
    user_passwords = {
        'admin': 'admin123',
        'veterinario': 'vet123', 
        'funcionario': 'func123',
        'cliente': 'cliente123'
    }
    
    for username, password in user_passwords.items():
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_active = True  # Garantir que está ativo
            user.save()
            print(f"✅ Senha redefinida para {username}: {password}")
            
            # Testar autenticação
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                print(f"✅ Autenticação testada com sucesso para {username}")
            else:
                print(f"❌ Falha na autenticação para {username}")
                
        except User.DoesNotExist:
            print(f"❌ Usuário {username} não encontrado")

def create_missing_users():
    """Cria usuários que estão faltando"""
    print("\n\n🆕 CRIANDO USUÁRIOS FALTANTES")
    print("=" * 50)
    
    users_to_create = [
        {
            'username': 'admin',
            'email': 'admin@toppet.com',
            'password': 'admin123',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'role': Profile.Role.ADMIN,
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'veterinario',
            'email': 'vet@toppet.com', 
            'password': 'vet123',
            'first_name': 'Dr. João',
            'last_name': 'Veterinário',
            'role': Profile.Role.VETERINARIO
        },
        {
            'username': 'funcionario',
            'email': 'func@toppet.com',
            'password': 'func123', 
            'first_name': 'Maria',
            'last_name': 'Funcionária',
            'role': Profile.Role.FUNCIONARIO
        },
        {
            'username': 'cliente',
            'email': 'cliente@toppet.com',
            'password': 'cliente123',
            'first_name': 'Pedro',
            'last_name': 'Cliente', 
            'role': Profile.Role.CLIENTE
        }
    ]
    
    for user_data in users_to_create:
        username = user_data['username']
        
        # Verificar se já existe
        if User.objects.filter(username=username).exists():
            print(f"⚠️  Usuário {username} já existe - pulando criação")
            continue
            
        # Criar usuário
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_staff=user_data.get('is_staff', False),
            is_superuser=user_data.get('is_superuser', False),
            is_active=True
        )
        
        # Criar perfil
        Profile.objects.create(
            user=user,
            role=user_data['role']
        )
        
        print(f"✅ Usuário {username} criado com sucesso")
        
        # Testar autenticação
        auth_user = authenticate(username=username, password=user_data['password'])
        if auth_user:
            print(f"✅ Autenticação testada com sucesso para {username}")
        else:
            print(f"❌ Falha na autenticação para {username}")

def main():
    try:
        # Primeiro verificar usuários existentes
        check_user_auth()
        
        # Tentar resetar senhas dos existentes
        reset_user_passwords()
        
        # Criar usuários faltantes
        create_missing_users()
        
        print("\n\n✅ VERIFICAÇÃO E CORREÇÃO CONCLUÍDA!")
        print("Testando autenticação final...")
        
        # Teste final
        test_users = ['admin', 'veterinario', 'funcionario', 'cliente']
        test_passwords = ['admin123', 'vet123', 'func123', 'cliente123']
        
        print("\n--- TESTE FINAL DE AUTENTICAÇÃO ---")
        for username, password in zip(test_users, test_passwords):
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                print(f"✅ {username}: OK")
            else:
                print(f"❌ {username}: FALHA")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
