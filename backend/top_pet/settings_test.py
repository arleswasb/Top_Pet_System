# settings_test.py
# Configurações específicas para testes com MySQL

from .settings import *
from decouple import config

# Override database configuration for tests - Force MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('TEST_MYSQL_NAME', default='top_pet_test_db'),
        'USER': config('TEST_MYSQL_USER', default='test_user'),
        'PASSWORD': config('TEST_MYSQL_PASSWORD', default='test_password'),
        'HOST': config('TEST_MYSQL_HOST', default='localhost'),
        'PORT': config('TEST_MYSQL_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'TEST': {
            'NAME': 'test_top_pet_test_db',
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
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

# Media files para testes
import tempfile
import os
MEDIA_ROOT = os.path.join(tempfile.gettempdir(), 'test_media_pets')
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Acelerar testes
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Desabilitar migrações desnecessárias em testes
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

# Comentar a linha abaixo se precisar rodar migrações nos testes
# MIGRATION_MODULES = DisableMigrations()
