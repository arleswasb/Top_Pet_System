from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgendamentoViewSet

# Cria um roteador padrão
router = DefaultRouter()

# Registra nossa AgendamentoViewSet com o prefixo 'agendamentos'
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')

# As URLs são geradas automaticamente pelo roteador
urlpatterns = router.urls