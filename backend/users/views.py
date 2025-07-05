# users/views.py

import os
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Profile
from .permissions import IsAdminRole, CanManageClients
from .serializers import (
    UserAdminSerializer,
    UserSelfRegisterSerializer,
    UserFuncionarioCreateSerializer,
    UserAdminCreateSerializer,
    UserDetailSerializer
)
from .swagger_schemas import SELF_REGISTER_SCHEMA

# --- VIEWS DE UTILIDADES E PÚBLICAS ---

class LogResponseSerializer(serializers.Serializer):
    """Serializer para a resposta do endpoint de logs."""
    content = serializers.CharField(help_text="Conteúdo do arquivo de log")

@extend_schema(
    summary="Visualizar logs do sistema (Admin)",
    description="Retorna as últimas 100 linhas do log de debug. Acesso restrito a administradores.",
    responses={200: LogResponseSerializer},
    tags=["Usuários"]
)
class LogFileView(APIView):
    """Endpoint para visualização dos logs do sistema por administradores."""
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get(self, request, *args, **kwargs):
        log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'debug.log')
        try:
            with open(log_file_path, 'r', encoding='utf-8') as log_file:
                lines = log_file.readlines()[-100:]
                log_content = "".join(lines)
            return Response({"content": log_content}, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({"content": "Arquivo de log não encontrado."}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary=SELF_REGISTER_SCHEMA['summary'],
    description=SELF_REGISTER_SCHEMA['description'],
    tags=SELF_REGISTER_SCHEMA['tags'],
    request=UserSelfRegisterSerializer,
    responses={201: UserDetailSerializer},
    examples=SELF_REGISTER_SCHEMA['examples']
)
class UserCreateView(generics.CreateAPIView):
    """Endpoint público para auto-cadastro de novos usuários como CLIENTE."""
    queryset = User.objects.all()
    serializer_class = UserSelfRegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    summary="Meu perfil",
    description="Retorna informações detalhadas do perfil do usuário atualmente logado.",
    tags=["Usuários"],
    responses={200: UserDetailSerializer}
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """View para o usuário visualizar e atualizar seu próprio perfil."""
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# --- VIEWSETS DE GERENCIAMENTO ---

@extend_schema_view(
    list=extend_schema(summary="Listar todos os usuários (Admin)", tags=["Usuários"]),
    create=extend_schema(summary="Criar usuário (Admin)", tags=["Usuários"]),
    retrieve=extend_schema(summary="Detalhes do usuário (Admin)", tags=["Usuários"]),
    partial_update=extend_schema(summary="Atualizar usuário (Admin)", tags=["Usuários"]),
    destroy=extend_schema(summary="Deletar usuário (Admin)", tags=["Usuários"]),
    toggle_active=extend_schema(summary="Ativar/Desativar usuário (Admin)", tags=["Usuários"])
)
class UserAdminViewSet(viewsets.ModelViewSet):
    """ViewSet para gestão completa de todos os usuários por administradores."""
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        """Retorna o serializer correto baseado na ação (create vs. update/list)."""
        if self.action == 'create':
            return UserAdminCreateSerializer
        return UserAdminSerializer

    @action(detail=True, methods=['post'], url_path='toggle-active')
    def toggle_active(self, request, pk=None):
        """Ação customizada para ativar ou desativar um usuário."""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(summary="Listar clientes (Funcionário)", tags=["Usuários"]),
    create=extend_schema(summary="Criar usuário (Funcionário)", tags=["Usuários"]),
    retrieve=extend_schema(summary="Detalhes do cliente (Funcionário)", tags=["Usuários"]),
    partial_update=extend_schema(summary="Atualizar cliente (Funcionário)", tags=["Usuários"]),
    destroy=extend_schema(summary="Excluir cliente (Funcionário)", tags=["Usuários"]),
)
class UserFuncionarioViewSet(viewsets.ModelViewSet):
    """ViewSet para funcionários gerenciarem usuários do tipo CLIENTE."""
    permission_classes = [permissions.IsAuthenticated, CanManageClients]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        """Retorna o serializer apropriado com base na ação."""
        if self.action == 'create':
            return UserFuncionarioCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserAdminSerializer
        return UserDetailSerializer

    def get_queryset(self):
        """Admins veem todos. Funcionários veem apenas usuários clientes."""
        user = self.request.user
        if not hasattr(user, 'profile'):
            return User.objects.none()

        if user.profile.role == Profile.Role.ADMIN:
            return User.objects.all().order_by('-date_joined')

        if user.profile.role == Profile.Role.FUNCIONARIO:
            return User.objects.filter(profile__role=Profile.Role.CLIENTE).order_by('-date_joined')

        return User.objects.none()


# --- VIEW DE AUTENTICAÇÃO CUSTOMIZADA ---

@extend_schema(
    summary="Login e obter token",
    description="Envie `username` e `password` para receber um token de autenticação.",
    tags=['Autenticação']
)
class CustomAuthTokenView(ObtainAuthToken):
    """
    View customizada que herda da original para obter token,
    permitindo adicionar a documentação Swagger correta.
    """
    pass