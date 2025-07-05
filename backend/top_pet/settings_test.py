"""
Configurações específicas para TODOS os tipos de testes
- Testes rápidos
- Testes de validação 
- Testes de unidade
- Testes de integração

Utiliza SQLite em memória para máxima velocidade e sem persistência
"""

from .settings import *
import tempfile
import os

# Banco de dados - SQLite em memória para TODOS os testes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}

# Configurações de mídia para testes
MEDIA_ROOT = os.path.join(tempfile.gettempdir(), 'test_media_pets')
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Email para testes (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configurações otimizadas para velocidade de testes
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',  # Mais rápido para testes
]

# Cache simples para testes
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'test-cache',
    }
}

# Desabilitar logs durante testes para performance
LOGGING['loggers']['django']['level'] = 'ERROR'

# Desabilitar migrações desnecessárias durante testes
MIGRATION_MODULES = {
    'auth': None,
    'contenttypes': None,
    'sessions': None,
}

# Configurações de segurança relaxadas para testes
DEBUG = False
SECRET_KEY = 'test-secret-key-not-for-production'
ALLOWED_HOSTS = ['*']

print("🧪 Configurações de teste carregadas - SQLite em memória para todos os tipos de testes")
