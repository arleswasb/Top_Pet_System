from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inclui todas as URLs do app 'pets' sob o prefixo 'api/'
    path('api/pets/', include('pets.urls')),
    # Adicionaremos as URLs do app 'users'
     path('api/users/', include('users.urls')),
    # Adiciona as URLs do app 'agendamentos'
    path('api/agendamentos/', include('agendamentos.urls')),
    # Adiciona as URLs do app 'auth' para autenticação
    #path('api/auth/', include('rest_framework.urls')),    
]

# Adiciona as URLs para servir os arquivos de mídia (fotos) em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)