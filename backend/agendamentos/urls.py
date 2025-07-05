# agendamento/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# --- Importe a nova view e as ViewSets ---
from .views import ServicoViewSet, AgendamentoViewSet, horarios_disponiveis

router = DefaultRouter()
router.register(r'servicos', ServicoViewSet, basename='servico')
router.register(r'', AgendamentoViewSet, basename='agendamento')

urlpatterns = [
    # --- URL específica para verificar os horários disponíveis ---
    path('horarios-disponiveis/', horarios_disponiveis, name='horarios-disponiveis'),
    
    # Inclui as URLs geradas pelo router
    path('', include(router.urls)),
]