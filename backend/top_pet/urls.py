# top_pet/top_pet/urls.py (seu urls.py principal)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import CustomAuthTokenView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # 1. Rotas de Administração
    path('admin/', admin.site.urls),

    # 2. Rotas da API principal (status, info, etc.)
    path('api/', include('top_pet.api_urls')),

    # 3. Rotas de Autenticação (agrupadas)
    path('api/auth/token/', CustomAuthTokenView.as_view(), name='api_token_auth'),
    path('api/auth/password-reset/', include('users.password_reset_urls')),

    # 4. Rotas da API para cada aplicativo
    path('api/pets/', include('pets.urls')),
    path('api/users/', include('users.urls')),
    path('api/configuracao/', include('configuracao.urls')),
    path('api/agendamentos/', include('agendamentos.urls')),
    path('api/prontuarios/', include('prontuarios.urls')),

    # 5. Rotas de Documentação da API (Swagger/OpenAPI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Servir arquivos de mídia em modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)