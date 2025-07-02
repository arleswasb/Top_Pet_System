# top_pet/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
@extend_schema(
    summary="API Status",
    description="Retorna o status da API e informações básicas do sistema.",
    tags=['Sistema']
)
def api_status(request):
    """
    Endpoint para verificar o status da API.
    """
    return Response({
        'status': 'online',
        'message': 'Top Pet System API está funcionando!',
        'version': '1.0.0',
        'endpoints': {
            'documentacao': '/api/docs/',
            'admin': '/admin/',
            'autenticacao': '/api/auth/token/',
            'autenticacao': '/api/auth/token/refresh/',
            'autenticacao': '/api/auth/password-reset/',
            'autenticacao': '/api/auth/password-reset/confirm/',
            'pets': '/api/pets/',
            'usuarios': '/api/users/',
            'agendamentos': '/api/agendamentos/',
            'prontuarios': '/api/prontuarios/',
            'configuracao': '/api/configuracao/'
        }
    })


def home(request):
    """
    View simples para a página inicial.
    """
    return JsonResponse({
        'message': 'Bem-vindo ao Top Pet System!',
        'api_docs': '/api/docs/',
        'admin': '/admin/'
    })
