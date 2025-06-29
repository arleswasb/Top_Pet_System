from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions, viewsets, serializers
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from .serializers import (
    UserCreateSerializer, UserAdminSerializer, UserSelfRegisterSerializer,
    UserFuncionarioCreateSerializer, UserAdminCreateSerializer, UserDetailSerializer
)
from django.conf import settings
from .permissions import IsAdminRole, IsFuncionarioOrAdmin, CanManageClients # Importa nossas permissões
from .models import Profile  # Importa o modelo Profile
from .swagger_schemas import SELF_REGISTER_SCHEMA, USER_SELF_REGISTER_EXAMPLES
import os

class LogResponseSerializer(serializers.Serializer):
    """Serializer para resposta dos logs"""
    content = serializers.CharField(help_text="Conteúdo do arquivo de log")

@extend_schema(
    summary="Visualizar logs do sistema",
    description="Retorna as últimas 100 linhas do log de debug. Apenas administradores.",
    responses={200: LogResponseSerializer},
    tags=["Usuários"]
)
class LogFileView(APIView):
    """Endpoint para visualização dos logs do sistema por administradores."""
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    serializer_class = LogResponseSerializer

    def get(self, request, *args, **kwargs):
        log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'debug.log')
        try:
            with open(log_file_path, 'r') as log_file:
                # Lê as últimas 100 linhas para não sobrecarregar
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
    """
    Endpoint público para auto-cadastro de novos usuários.
    Usuários cadastrados por este endpoint são sempre do tipo CLIENTE.
    """
    queryset = User.objects.all()
    serializer_class = UserSelfRegisterSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema_view(
    list=extend_schema(
        summary="Listar usuários",
        description="Lista todos os usuários do sistema. Apenas administradores.",
        tags=["Usuários"]
    ),
    create=extend_schema(
        summary="Criar usuário",
        description="Cria um novo usuário via administrador.",
        tags=["Usuários"]
    ),
    retrieve=extend_schema(
        summary="Detalhes do usuário",
        description="Retorna detalhes de um usuário específico.",
        tags=["Usuários"]
    ),
    partial_update=extend_schema(
        summary="Atualizar usuário",
        description="Atualiza parcialmente um usuário. Apenas os campos enviados serão alterados.",
        tags=["Usuários"]
    ),
    destroy=extend_schema(
        summary="Deletar usuário",
        description="Remove um usuário do sistema.",
        tags=["Usuários"]
    ),
)
class UserAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestão administrativa de usuários.
    
    Funcionalidades:
    - CRUD completo de usuários
    - Ativar/desativar usuários
    - Apenas para administradores
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    
    # Lista de ações HTTP permitidas (removendo 'put' que é o método PUT)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Toggle user active status
        """
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Meu perfil",
    description="Retorna informações do perfil do usuário logado.",
    tags=["Usuários"],
    responses={200: UserDetailSerializer}
)
class UserProfileView(generics.RetrieveAPIView):
    """
    View para o usuário visualizar seu próprio perfil.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

@extend_schema(
    summary="Criar usuário (Funcionário)",
    description="Endpoint para funcionários criarem usuários dos tipos: Cliente, Funcionário ou Veterinário.",
    tags=["Usuários"],
    request=UserFuncionarioCreateSerializer,
    responses={201: UserDetailSerializer}
)
class UserFuncionarioCreateView(generics.CreateAPIView):
    """
    Endpoint para funcionários criarem usuários.
    Funcionários podem criar: CLIENTE, FUNCIONARIO ou VETERINARIO.
    """
    queryset = User.objects.all()
    serializer_class = UserFuncionarioCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsFuncionarioOrAdmin]

@extend_schema(
    summary="Criar usuário (Admin)", 
    description="Endpoint para administradores criarem usuários de qualquer tipo.",
    tags=["Usuários"],
    request=UserAdminCreateSerializer,
    responses={201: UserDetailSerializer}
)
class UserAdminCreateView(generics.CreateAPIView):
    """
    Endpoint para administradores criarem usuários.
    Administradores podem criar qualquer tipo de usuário.
    """
    queryset = User.objects.all()
    serializer_class = UserAdminCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

@extend_schema_view(
    list=extend_schema(
        summary="Listar clientes (Funcionário)",
        description="Funcionários podem listar apenas usuários do tipo CLIENTE.",
        tags=["Usuários"]
    ),
    retrieve=extend_schema(
        summary="Detalhes do cliente (Funcionário)",
        description="Funcionários podem ver detalhes apenas de clientes.",
        tags=["Usuários"]
    ),
    partial_update=extend_schema(
        summary="Atualizar cliente (Funcionário)",
        description="Funcionários podem atualizar parcialmente dados de clientes.",
        tags=["Usuários"]
    ),
    destroy=extend_schema(
        summary="Excluir cliente (Funcionário)",
        description="Funcionários podem excluir usuários clientes.",
        tags=["Usuários"]
    ),
)
class UserFuncionarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para funcionários gerenciarem usuários clientes.
    
    Funcionalidades:
    - Listar apenas clientes
    - Ver detalhes de clientes
    - Editar dados de clientes
    - Excluir clientes
    - Criar novos clientes
    - Apenas para funcionários e admins
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageClients]
    
    # Lista de ações HTTP permitidas (removendo 'put' que é o método PUT)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    def get_serializer_class(self):
        """
        Retorna o serializer apropriado com base na ação.
        """
        if self.action == 'create':
            return UserFuncionarioCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserAdminSerializer  # Para permitir edição de perfil
        return UserDetailSerializer
    
    def get_queryset(self):
        """
        Funcionários veem apenas usuários clientes.
        Admins veem todos os usuários.
        """
        user = self.request.user
        
        if not hasattr(user, 'profile'):
            return User.objects.none()
        
        # Admin vê todos os usuários
        if user.profile.role == Profile.Role.ADMIN:
            return User.objects.all()
        
        # Funcionário vê apenas clientes
        if user.profile.role == Profile.Role.FUNCIONARIO:
            return User.objects.filter(profile__role=Profile.Role.CLIENTE)
        
        return User.objects.none()
    
    def perform_destroy(self, instance):
        """
        Permite que funcionários excluam apenas clientes.
        """
        if hasattr(instance, 'profile') and instance.profile.role == Profile.Role.CLIENTE:
            instance.delete()
        else:
            raise serializers.ValidationError({"detail": "Funcionários podem excluir apenas usuários clientes."})