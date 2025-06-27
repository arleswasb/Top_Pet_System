# top_pet_system/urls.py (seu urls.py principal)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inclui as URLs dos apps, APENAS com o prefixo 'api/',
    # deixando o router de cada app adicionar o nome do recurso.
    path('api/', include('pets.urls')),       # Correto
    path('api/', include('users.urls')),      # <-- CORRIGIDO AQUI!
    path('api/', include('agendamentos.urls')), # <-- CORRIGIDO AQUI!
    # path('api/auth/', include('rest_framework.urls')),
]

# Adiciona as URLs para servir os arquivos de mídia (fotos) em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)