#!/bin/sh

# Garante que o script irá parar se algum comando falhar
set -e

echo "Aplicando migrações do banco de dados..."
python manage.py migrate --no-input

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input --clear

echo "Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000