"""
Comando Django para resetar completamente o banco de dados do projeto Top Pet System.
Este comando remove o banco existente, limpa migrações e recria tudo do zero.

Uso:
    python manage.py reset_database
    python manage.py reset_database --keep-media  # Mantém arquivos de mídia
    python manage.py reset_database --no-superuser  # Não pergunta sobre criar superusuário
"""

import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Reset the database completely - removes DB, migrations, and recreates everything'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-media',
            action='store_true',
            help='Keep media files (uploads) when resetting',
        )
        parser.add_argument(
            '--no-superuser',
            action='store_true',
            help='Do not prompt to create a superuser',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reset without confirmation',
        )

    def handle(self, *args, **options):
        if not options['force']:
            confirm = input(
                '\n⚠️  ATENÇÃO: Este comando irá DELETAR COMPLETAMENTE o banco de dados atual!\n'
                'Todos os dados serão perdidos permanentemente.\n'
                'Deseja continuar? Digite "sim" para confirmar: '
            )
            if confirm.lower() not in ['sim', 'yes', 's', 'y']:
                self.stdout.write(
                    self.style.WARNING('Operação cancelada pelo usuário.')
                )
                return

        self.stdout.write('\n🔄 Iniciando reset completo do banco de dados...\n')

        # Passo 1: Remover banco de dados SQLite
        self._remove_database()

        # Passo 2: Limpar migrações
        self._clean_migrations()

        # Passo 3: Limpar cache do Python
        self._clean_python_cache()

        # Passo 4: Limpar logs (opcional)
        self._clean_logs()

        # Passo 5: Limpar mídia (opcional)
        if not options['keep_media']:
            self._clean_media()

        # Passo 6: Criar novas migrações
        self._create_migrations()

        # Passo 7: Aplicar migrações
        self._apply_migrations()

        # Passo 8: Criar superusuário (opcional)
        if not options['no_superuser']:
            self._create_superuser()

        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Reset do banco de dados concluído com sucesso!\n'
                '🚀 Agora você pode executar: python manage.py runserver\n'
            )
        )

    def _remove_database(self):
        """Remove o arquivo do banco de dados SQLite."""
        self.stdout.write('🗑️  Removendo banco de dados antigo...')
        
        db_path = Path(settings.BASE_DIR) / 'db.sqlite3'
        if db_path.exists():
            try:
                db_path.unlink()
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Banco de dados removido com sucesso!')
                )
            except PermissionError:
                raise CommandError(
                    '❌ Erro: Não foi possível remover o banco de dados. '
                    'Certifique-se de que nenhum processo está usando o arquivo '
                    '(feche o Django, PyCharm, etc.)'
                )
        else:
            self.stdout.write(
                self.style.WARNING('   ℹ️  Banco de dados não encontrado')
            )

    def _clean_migrations(self):
        """Remove arquivos de migração (exceto __init__.py)."""
        self.stdout.write('🗑️  Limpando migrações antigas...')
        
        apps = ['agendamentos', 'pets', 'users', 'prontuarios', 'configuracao']
        
        for app in apps:
            migrations_dir = Path(settings.BASE_DIR) / app / 'migrations'
            if migrations_dir.exists():
                self.stdout.write(f'   Limpando migrações de {app}...')
                
                # Remove arquivos .py exceto __init__.py
                for file in migrations_dir.glob('*.py'):
                    if file.name != '__init__.py':
                        file.unlink()
                
                # Remove cache
                pycache_dir = migrations_dir / '__pycache__'
                if pycache_dir.exists():
                    shutil.rmtree(pycache_dir)
        
        self.stdout.write(
            self.style.SUCCESS('   ✅ Migrações limpas!')
        )

    def _clean_python_cache(self):
        """Remove cache do Python."""
        self.stdout.write('🗑️  Limpando cache do Python...')
        
        base_dir = Path(settings.BASE_DIR)
        
        # Remove __pycache__ do diretório raiz
        pycache_root = base_dir / '__pycache__'
        if pycache_root.exists():
            shutil.rmtree(pycache_root)
        
        # Remove __pycache__ dos apps
        apps = ['agendamentos', 'pets', 'users', 'prontuarios', 'configuracao', 'top_pet']
        for app in apps:
            pycache_dir = base_dir / app / '__pycache__'
            if pycache_dir.exists():
                shutil.rmtree(pycache_dir)
        
        self.stdout.write(
            self.style.SUCCESS('   ✅ Cache do Python limpo!')
        )

    def _clean_logs(self):
        """Remove arquivos de log."""
        self.stdout.write('🗑️  Limpando logs antigos...')
        
        logs_dir = Path(settings.BASE_DIR) / 'logs'
        if logs_dir.exists():
            for log_file in logs_dir.glob('*.log'):
                log_file.unlink()
            self.stdout.write(
                self.style.SUCCESS('   ✅ Logs limpos!')
            )

    def _clean_media(self):
        """Remove arquivos de mídia."""
        self.stdout.write('🗑️  Limpando arquivos de mídia...')
        
        media_dir = Path(settings.MEDIA_ROOT)
        if media_dir.exists():
            for item in media_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            self.stdout.write(
                self.style.SUCCESS('   ✅ Arquivos de mídia limpos!')
            )

    def _create_migrations(self):
        """Cria novas migrações."""
        self.stdout.write('🔄 Criando novas migrações...')
        
        try:
            call_command('makemigrations', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('   ✅ Migrações criadas com sucesso!')
            )
        except Exception as e:
            raise CommandError(f'❌ Erro ao criar migrações: {e}')

    def _apply_migrations(self):
        """Aplica as migrações."""
        self.stdout.write('🔄 Aplicando migrações...')
        
        try:
            call_command('migrate', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('   ✅ Migrações aplicadas com sucesso!')
            )
        except Exception as e:
            raise CommandError(f'❌ Erro ao aplicar migrações: {e}')

    def _create_superuser(self):
        """Opcionalmente cria um superusuário."""
        self.stdout.write('👤 Criação de superusuário...')
        
        create_superuser = input(
            'Deseja criar um superusuário agora? (s/N): '
        ).lower()
        
        if create_superuser in ['s', 'sim', 'y', 'yes']:
            try:
                call_command('createsuperuser')
            except KeyboardInterrupt:
                self.stdout.write(
                    self.style.WARNING(
                        '\n   ⚠️  Criação de superusuário cancelada. '
                        'Você pode criar depois com: python manage.py createsuperuser'
                    )
                )
