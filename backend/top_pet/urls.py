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
    # 1. Rotas de Administração e Autenticação
    path('admin/', admin.site.urls),
    # Convenção comum para endpoints de token é usar /api/token/
    path('api/token/', CustomAuthTokenView.as_view(), name='api_token_auth'),

    # 2. Rotas da API para cada aplicativo (sem redundância)
    path('api/pets/', include('pets.urls')),
    path('api/users/', include('users.urls')),
    path('api/configuracao/', include('configuracao.urls')),
    path('api/agendamentos/', include('agendamentos.urls')),
    path('api/prontuarios/', include('prontuarios.urls')),
    # Descomente as linhas abaixo quando os respectivos apps tiverem seus arquivos urls.py

    # 4. Rotas de Documentação da API (Swagger/OpenAPI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Servir arquivos de mídia em modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)