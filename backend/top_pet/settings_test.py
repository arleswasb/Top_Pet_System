# settings_test.py
# Configurações específicas para testes - SQLite em memória (não persistido)

from .settings import *
from decouple import config
import tempfile
import os

# Override database configuration for tests - SQLite em memória
# Muito mais rápido e não precisa de configuração/persistência
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Banco em memória - não persistido
        'OPTIONS': {
            'timeout': 20,
        },
        'TEST': {
            'NAME': ':memory:',
        },
    }
}

# Configurações otimizadas para testes
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email para testes
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Logs simplificados para testes
LOGGING['loggers']['django']['level'] = 'ERROR'

# Media files para testes - diretório temporário
MEDIA_ROOT = os.path.join(tempfile.gettempdir(), 'test_media_pets')
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Acelerar testes com hash mais simples
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Desabilitar migrações para acelerar testes
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Configurações adicionais para acelerar testes
DEBUG = False
TEMPLATE_DEBUG = False

# Desabilitar logs desnecessários
import logging
logging.disable(logging.CRITICAL)

# Desabilitar migrações desnecessárias em testes
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

# Comentar a linha abaixo se precisar rodar migrações nos testes
# MIGRATION_MODULES = DisableMigrations()
