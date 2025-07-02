# top_pet_system/urls.py (seu urls.py principal)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import CustomAuthTokenView
from drf_spectacular.utils import extend_schema  # <-- 1. IMPORTE O EXTEND_SCHEMA
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Agrupando as URLs da API
api_urlpatterns = [
    path('', include('pets.urls')),
    path('', include('users.urls')),
    path('', include('agendamentos.urls')),
    path('', include('prontuarios.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    
    path('api-token-auth/', CustomAuthTokenView.as_view(), name='api_token_auth'),
    # Customizando o endpoint de autenticação
    # para usar o token de autenticação do DRF
    
    # Swagger/OpenAPI URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Adiciona as URLs para servir os arquivos de mídia (fotos) em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)