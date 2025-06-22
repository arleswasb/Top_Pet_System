# users/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile
import os

class Command(BaseCommand):
    help = 'Cria usuários e perfis de teste para o ambiente de desenvolvimento/CI.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando o povoamento do banco de dados com dados de teste...')

        # Pega as credenciais das variáveis de ambiente
        users_data = [
            {'username': os.environ.get('TEST_ADMIN_USER'), 'password': os.environ.get('TEST_ADMIN_PASSWORD'), 'role': Profile.Role.ADMIN, 'is_staff': True, 'is_superuser': True},
            {'username': os.environ.get('TEST_CLIENTE_USER'), 'password': os.environ.get('TEST_CLIENTE_PASSWORD'), 'role': Profile.Role.CLIENTE},
            {'username': os.environ.get('TEST_FUNC_USER'), 'password': os.environ.get('TEST_FUNC_PASSWORD'), 'role': Profile.Role.FUNCIONARIO, 'is_staff': True}
        ]

        for data in users_data:
            if not data['username'] or not data['password']:
                self.stdout.write(self.style.ERROR(f"Variáveis de ambiente para o usuário não estão definidas. Pulando."))
                continue

            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    password=data['password']
                )
                user.is_staff = data.get('is_staff', False)
                user.is_superuser = data.get('is_superuser', False)
                user.save()

                Profile.objects.create(user=user, role=data['role'])
                self.stdout.write(self.style.SUCCESS(f"Usuário '{data['username']}' e seu perfil foram criados com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Usuário '{data['username']}' já existe. Pulando."))

        self.stdout.write(self.style.SUCCESS('Povoamento do banco de dados concluído.'))