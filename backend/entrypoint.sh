#!/bin/bash
set -e

echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

echo "Aplicando migrações do banco de dados..."
python manage.py makemigrations
python manage.py migrate

echo "Iniciando o servidor..."
exec python manage.py runserver 0.0.0.0:8000