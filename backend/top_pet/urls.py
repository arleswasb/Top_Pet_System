"""Main URL configuration for the project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("pets.urls")),  # Correto
    path("api/", include("users.urls")),  # <-- CORRIGIDO AQUI!
    path("api/", include("agendamentos.urls")),  # <-- CORRIGIDO AQUI!
]

# Adiciona as URLs para servir os arquivos de mídia (fotos) em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)