from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet

# Cria um roteador padrão
router = DefaultRouter()

# Registra a nossa PetViewSet com o roteador.
# O prefixo da URL será 'pets'. Ex: /api/pets/ e /api/pets/1/
router.register(r'pets', PetViewSet, basename='pet')

# As URLs da API são agora determinadas automaticamente pelo roteador.
urlpatterns = router.urls
