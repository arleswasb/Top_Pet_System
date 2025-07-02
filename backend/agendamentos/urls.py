# agendamentos/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Comentar temporariamente até implementar as views
# from .views import AgendamentoViewSet, ServicoViewSet

router = DefaultRouter()
# router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')
# router.register(r'servicos', ServicoViewSet, basename='servico')

urlpatterns = [
    # Inclui as URLs geradas pelo router
    path('', include(router.urls)),
]