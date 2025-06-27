from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProntuarioViewSet

# Cria o router
router = DefaultRouter()

# Registra as rotas
router.register(r'prontuarios', ProntuarioViewSet, basename='prontuario')

app_name = 'prontuarios'

urlpatterns = [
    # Inclui as URLs geradas pelo router
    path('', include(router.urls)),
]