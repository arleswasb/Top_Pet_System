# backend/configuracao/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HorarioFuncionamentoViewSet, FeriadoViewSet

router = DefaultRouter()
router.register(r'horarios-funcionamento', HorarioFuncionamentoViewSet, basename='horariofuncionamento')
router.register(r'feriados', FeriadoViewSet, basename='feriado')

urlpatterns = [
    path('', include(router.urls)),
]