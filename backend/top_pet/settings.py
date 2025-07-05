#settings.py
import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-etva7+wfjug1hjg$5mb4fzq***=o&w0$rllq%!czw!xmj)y8xa')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv()) + ['testserver']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_rest_passwordreset',
    'pets',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'users',
    'agendamentos',
    'prontuarios',
    'configuracao',
    # Adicionar CORS para APIs (opcional, mas recomendado)
    # 'corsheaders',  # Descomente se precisar de CORS
]

# Configuração de autenticação do DRF 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication', # Opcional: para o browsable API
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Configuração do drf-spectacular (Swagger/OpenAPI)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Top Pet System API',
    'DESCRIPTION': 'Sistema de gestão para pet shops - API completa para gerenciamento de pets, usuários, agendamentos e prontuários médicos.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'Top Pet System',
        'email': 'contato@toppetsystem.com',
    },
    'LICENSE': {
        'name': 'MIT License',
    },
    'TAGS': [
        {'name': 'Sistema', 'description': 'Informações gerais do sistema, status e links de navegação'},
        {'name': 'Autenticação', 'description': 'Endpoints de login, registro e reset de senha'},
        {'name': 'Usuários', 'description': 'Gestão de perfis de usuários do sistema'},
        {'name': 'Pets', 'description': 'Operações relacionadas ao cadastro e gestão de pets'},
        {'name': 'Serviços', 'description': 'Catálogo de serviços veterinários disponíveis'},
        {'name': 'Agendamentos', 'description': 'Sistema de agendamento de consultas e serviços'},
        {'name': 'Horários', 'description': 'Consulta de horários disponíveis para agendamento'},
        {'name': 'Prontuários', 'description': 'Prontuários médicos e histórico de atendimentos'},
        {'name': 'Configuração', 'description': 'Configurações de horários de funcionamento e feriados do sistema'},
    ],
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'SCHEMA_PATH_PREFIX_TRIM': False,
    'DISABLE_ERRORS_AND_WARNINGS': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'displayRequestDuration': True,
        'docExpansion': 'none',
        'filter': True,
        'showExtensions': True,
        'showCommonExtensions': True,
        'defaultModelsExpandDepth': 1,
        'defaultModelExpandDepth': 1,
    },
    'REDOC_UI_SETTINGS': {
        'hideDownloadButton': False,
        'theme': {
            'colors': {
                'primary': {
                    'main': '#3f51b5'
                }
            }
        }
    },
}

# Cache configuration (para melhor performance da API)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutos
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'top_pet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'top_pet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Database configuration
# PostgreSQL apenas para produção real (via DATABASE_URL)
# SQLite para desenvolvimento e simulação (não interferem na produção)
if config('DATABASE_URL', default=None):
    # Produção: PostgreSQL via DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(config('DATABASE_URL'))
    }
else:
    # Desenvolvimento e Simulação: SQLite (arquivo local, não interfere na produção)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 20,
            },
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files (uploads)
import tempfile

# Configuração do MEDIA_ROOT baseada no ambiente
if config('DOCKER_ENV', default=False, cast=bool):
    # Em ambiente Docker/produção
    MEDIA_ROOT = '/app/media'
elif config('CI', default=False, cast=bool) or config('GITHUB_ACTIONS', default=False, cast=bool):
    # Em ambiente de CI/Testes
    MEDIA_ROOT = os.path.join(tempfile.gettempdir(), 'test_media')
else:
    # Em desenvolvimento local
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Garante que o diretório de mídia existe
os.makedirs(MEDIA_ROOT, exist_ok=True)

#conficuração do logging
# Detectar se estamos em ambiente CI/CD
IS_CI = bool(os.getenv('CI') or os.getenv('GITHUB_ACTIONS'))

# Configuração de logging baseada no ambiente
if IS_CI:
    # Em CI/CD: apenas console logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
else:
    # Em desenvolvimento local: console + arquivo
    # Garantir que o diretório de logs existe
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOGS_DIR, 'debug.log'),
                'maxBytes': 1024*1024*5,  # 5 MB
                'backupCount': 2,
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }

# Configurações específicas para testes
import sys
if 'test' in sys.argv or 'pytest' in sys.modules or 'unittest' in sys.modules:
    # Para TODOS os tipos de testes (rápidos, unidade, validação e integração) 
    # usar SQLite em memória para máxima velocidade e isolamento completo
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'OPTIONS': {
            'timeout': 20,
        }
    }
    
    # Durante os testes, usar um diretório temporário para mídia
    import tempfile
    MEDIA_ROOT = os.path.join(tempfile.gettempdir(), 'test_media_pets')
    
    # Criar o diretório se não existir
    os.makedirs(MEDIA_ROOT, exist_ok=True)
    
    # Desabilitar logs durante testes para performance
    LOGGING['loggers']['django']['level'] = 'ERROR'
    LOGGING['loggers']['django']['handlers'] = ['console']  # Garantir apenas console

    # Configuração de Email para testes (console)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
    # Configurações otimizadas para testes rápidos
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',  # Mais rápido para testes
    ]
    
    # Desabilitar migrações desnecessárias durante testes
    MIGRATION_MODULES = {
        'auth': None,
        'contenttypes': None,
        'sessions': None,
    }

# ======================================
# CONFIGURAÇÃO DE EMAIL PARA PRODUÇÃO
# ======================================
# Descomente e configure para usar email real:

# Para Gmail/Google Workspace:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'seu-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'sua-senha-de-app'  # Use senha de app, não senha normal
# DEFAULT_FROM_EMAIL = 'Top Pet System <seu-email@gmail.com>'

# Para outros provedores (exemplo com Outlook):
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp-mail.outlook.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'seu-email@outlook.com'
# EMAIL_HOST_PASSWORD = 'sua-senha'
# DEFAULT_FROM_EMAIL = 'Top Pet System <seu-email@outlook.com>'

# Para desenvolvimento local (imprime no console):
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Para salvar emails em arquivos (desenvolvimento):
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')

# Configurações do django-rest-passwordreset
DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomStringTokenGenerator",
    "OPTIONS": {
        "min_length": 20,
        "max_length": 30
    }
}

# Template de email personalizado (opcional)
# DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE = True