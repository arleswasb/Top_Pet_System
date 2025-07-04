#!/usr/bin/env python
"""
Script para resetar o banco de dados do Top Pet System.
Execute: python reset_db_simple.py
"""

import os
import sys
import shutil
from pathlib import Path

def reset_database():
    print("🔄 Top Pet System - Reset do Banco de Dados")
    print("=" * 45)
    
    # Verificar se estamos no diretório correto
    if not Path('manage.py').exists():
        print("❌ ERRO: Execute este script no diretório backend onde está o manage.py")
        return False
    
    # Confirmação
    print("\n⚠️  ATENÇÃO: Este script irá DELETAR o banco de dados atual!")
    confirm = input("Digite 'sim' para continuar: ").lower()
    
    if confirm not in ['sim', 's']:
        print("Operação cancelada.")
        return False
    
    try:
        # 1. Remover banco de dados
        print("\n🗑️  Removendo banco de dados...")
        db_file = Path('db.sqlite3')
        if db_file.exists():
            db_file.unlink()
            print("✅ Banco removido!")
        else:
            print("ℹ️  Banco não encontrado")
        
        # 2. Limpar migrações e cache
        print("🗑️  Limpando migrações e cache...")
        apps = ['agendamentos', 'pets', 'users', 'prontuarios', 'configuracao']
        
        for app in apps:
            migrations_dir = Path(app) / 'migrations'
            if migrations_dir.exists():
                # Remove migrações (exceto __init__.py)
                for file in migrations_dir.glob('*.py'):
                    if file.name != '__init__.py':
                        file.unlink()
                
                # Remove cache das migrações
                cache_dir = migrations_dir / '__pycache__'
                if cache_dir.exists():
                    shutil.rmtree(cache_dir)
            
            # Remove cache do app
            app_cache = Path(app) / '__pycache__'
            if app_cache.exists():
                shutil.rmtree(app_cache)
        
        # Remove cache raiz
        root_cache = Path('__pycache__')
        if root_cache.exists():
            shutil.rmtree(root_cache)
        
        print("✅ Cache limpo!")
        
        # 3. Criar e aplicar migrações
        print("🔄 Criando migrações...")
        if os.system('python manage.py makemigrations') != 0:
            print("❌ Erro ao criar migrações")
            return False
        print("✅ Migrações criadas!")
        
        print("🔄 Aplicando migrações...")
        if os.system('python manage.py migrate') != 0:
            print("❌ Erro ao aplicar migrações")
            return False
        print("✅ Migrações aplicadas!")
        
        # 4. Oferecer criar superusuário
        print("\n👤 Criação de superusuário...")
        create_user = input("Deseja criar um superusuário? (s/N): ").lower()
        if create_user in ['s', 'sim']:
            os.system('python manage.py createsuperuser')
        
        print("\n🎉 Reset concluído com sucesso!")
        print("🚀 Agora execute: python manage.py runserver")
        return True
        
    except PermissionError:
        print("❌ Erro: Feche todos os programas que possam estar usando o banco.")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == '__main__':
    success = reset_database()
    input(f"\nPressione Enter para sair...")
    sys.exit(0 if success else 1)
