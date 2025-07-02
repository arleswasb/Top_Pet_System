from django.shortcuts import render
from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import HorarioFuncionamento, Feriado
from .serializers import HorarioFuncionamentoSerializer, FeriadoSerializer
from users.permissions import IsAdminRole

# Create your views here.
# backend/configuracao/views.py

@extend_schema_view(
    list=extend_schema(summary="Listar horários de funcionamento", tags=["Configuração"]),
    create=extend_schema(summary="Criar horário de funcionamento", tags=["Configuração"]),
    retrieve=extend_schema(summary="Detalhes do horário", tags=["Configuração"]),
    update=extend_schema(summary="Atualizar horário", tags=["Configuração"]),
    partial_update=extend_schema(summary="Atualizar horário parcialmente", tags=["Configuração"]),
    destroy=extend_schema(summary="Deletar horário", tags=["Configuração"])
)
class HorarioFuncionamentoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar horários de funcionamento da clínica"""
    queryset = HorarioFuncionamento.objects.all()
    serializer_class = HorarioFuncionamentoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

@extend_schema_view(
    list=extend_schema(summary="Listar feriados", tags=["Configuração"]),
    create=extend_schema(summary="Criar feriado", tags=["Configuração"]),
    retrieve=extend_schema(summary="Detalhes do feriado", tags=["Configuração"]),
    update=extend_schema(summary="Atualizar feriado", tags=["Configuração"]),
    partial_update=extend_schema(summary="Atualizar feriado parcialmente", tags=["Configuração"]),
    destroy=extend_schema(summary="Deletar feriado", tags=["Configuração"])
)
class FeriadoViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar feriados da clínica"""
    queryset = Feriado.objects.all()
    serializer_class = FeriadoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]