# agendamentos/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AgendamentoViewSet, ServicoViewSet

# Cria o router
router = DefaultRouter()

# Registra as rotas
router.register(r"servicos", ServicoViewSet, basename="servico")
router.register(r"agendamentos", AgendamentoViewSet, basename="agendamento")

urlpatterns = [
    # Inclui as URLs geradas pelo router
    path("", include(router.urls)),
]