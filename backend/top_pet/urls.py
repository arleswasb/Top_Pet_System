# top_pet_system/urls.py (seu urls.py principal)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

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
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('api/auth/', include('rest_framework.urls')),
]

# Adiciona as URLs para servir os arquivos de mídia (fotos) em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)