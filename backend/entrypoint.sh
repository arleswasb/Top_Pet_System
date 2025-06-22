#!/bin/sh

# Garante que o script irá parar se algum comando falhar
set -e

echo "Aplicando migrações do banco de dados..."
python manage.py migrate --no-input

# A linha mágica: executa o comando principal (CMD) que foi passado para o contêiner.
exec "$@"