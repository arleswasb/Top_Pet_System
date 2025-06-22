#!/bin/sh

# Garante que o script irá parar se algum comando falhar
set -e

# Espera o banco de dados ficar pronto (opcional mas recomendado)
# (Isso pode exigir a instalação do netcat no seu Dockerfile: RUN apt-get update && apt-get install -y netcat)
# while ! nc -z db 5432; do
#   echo "Aguardando o PostgreSQL iniciar..."
#   sleep 1
# done
# echo "PostgreSQL iniciado."

# Aplicando migrações do banco de dados
echo "Aplicando migrações do banco de dados..."
python manage.py migrate --no-input

# A linha mágica: executa o comando principal que foi passado para o contêiner.
# Se você rodar 'docker compose run web python manage.py test', "$@" será 'python manage.py test'.
# Se você rodar 'docker compose up', "$@" será o comando padrão do seu Dockerfile (provavelmente 'runserver').
exec "$@"