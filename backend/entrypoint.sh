#!/bin/bash

# Aplicando migrações do banco de dados...
echo "Aplicando migrações do banco de dados..."
python manage.py migrate

# Iniciando o servidor...
echo "Iniciando o servidor..."
exec python -u manage.py runserver 0.0.0.0:8000 --noreload