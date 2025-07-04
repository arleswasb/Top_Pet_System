# top_pet/views.py
"""
Views principais do projeto Top Pet System.
Contém views utilitárias e de informações gerais da API.
"""

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse
import datetime


@extend_schema(
    summary="Status da API",
    description="Retorna informações básicas sobre o status e versão da API Top Pet System.",
    tags=["Sistema"],
    responses={
        200: OpenApiResponse(
            description="Informações do sistema",
            examples=[
                {
                    "application/json": {
                        "status": "online",
                        "version": "1.0.0",
                        "timestamp": "2025-07-03T15:30:00Z",
                        "debug_mode": True,
                        "database": "connected"
                    }
                }
            ]
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """
    Endpoint público para verificar o status da API.
    Útil para monitoramento e health checks.
    """
    try:
        # Testar conexão com banco de dados
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except Exception:
        db_status = "error"
    
    return Response({
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "debug_mode": settings.DEBUG,
        "database": db_status,
        "message": "Top Pet System API está funcionando!"
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Informações da API",
    description="Retorna informações detalhadas sobre a API e suas funcionalidades.",
    tags=["Sistema"],
    responses={
        200: OpenApiResponse(
            description="Informações detalhadas da API",
            examples=[
                {
                    "application/json": {
                        "name": "Top Pet System API",
                        "description": "Sistema de gestão para pet shops",
                        "features": [
                            "Gestão de pets",
                            "Agendamentos",
                            "Prontuários médicos",
                            "Usuários e permissões"
                        ],
                        "endpoints": {
                            "authentication": "/api/auth/",
                            "pets": "/api/pets/",
                            "appointments": "/api/agendamentos/",
                            "medical_records": "/api/prontuarios/",
                            "users": "/api/users/",
                            "documentation": "/api/docs/"
                        }
                    }
                }
            ]
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    Endpoint público com informações sobre a API.
    Útil para desenvolvedores que querem conhecer as funcionalidades.
    """
    return Response({
        "name": "Top Pet System API",
        "description": "Sistema de gestão para pet shops - API completa para gerenciamento de pets, usuários, agendamentos e prontuários médicos.",
        "version": "1.0.0",
        "features": [
            "Gestão de pets",
            "Sistema de agendamentos",
            "Prontuários médicos",
            "Gestão de usuários e permissões",
            "Catálogo de serviços",
            "Consulta de horários disponíveis",
            "Sistema de autenticação por token",
            "Reset de senha por email"
        ],
        "user_types": [
            "CLIENTE - Donos de pets",
            "FUNCIONARIO - Funcionários da clínica",
            "VETERINARIO - Profissionais veterinários",
            "ADMIN - Administradores do sistema"
        ],
        "endpoints": {
            "authentication": "/api/auth/",
            "pets": "/api/pets/",
            "appointments": "/api/agendamentos/",
            "available_hours": "/api/agendamentos/horarios-disponiveis/",
            "medical_records": "/api/prontuarios/",
            "services": "/api/servicos/",
            "users": "/api/users/",
            "documentation": "/api/docs/",
            "admin": "/admin/"
        },
        "documentation": {
            "swagger_ui": "/api/docs/",
            "redoc": "/api/redoc/",
            "openapi_schema": "/api/schema/"
        },
        "support": {
            "email": "contato@toppetsystem.com",
            "github": "https://github.com/seu-usuario/Top_Pet_System"
        }
    }, status=status.HTTP_200_OK)


# View para página inicial da API (opcional)
@extend_schema(
    summary="Página inicial da API",
    description="Endpoint raiz da API com links de navegação.",
    tags=["Sistema"],
    responses={
        200: OpenApiResponse(
            description="Links de navegação da API"
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    Endpoint raiz da API com links de navegação.
    """
    return Response({
        "message": "Bem-vindo ao Top Pet System API!",
        "navigation": {
            "documentation": request.build_absolute_uri('/api/docs/'),
            "api_info": request.build_absolute_uri('/api/info/'),
            "api_status": request.build_absolute_uri('/api/status/'),
            "authentication": request.build_absolute_uri('/api/auth/token/'),
            "pets": request.build_absolute_uri('/api/pets/'),
            "agendamentos": request.build_absolute_uri('/api/agendamentos/'),
            "prontuarios": request.build_absolute_uri('/api/prontuarios/'),
            "admin": request.build_absolute_uri('/admin/')
        }
    }, status=status.HTTP_200_OK)
