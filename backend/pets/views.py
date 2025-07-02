# pets/views.py
import logging
from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Pet
from .serializers import PetSerializer
from .permissions import IsOwnerOrAdminOrFuncionario # <-- Sua permissão personalizada
from users.models import Profile

logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        summary="Listar pets",
        description="Retorna lista de pets. Clientes veem apenas seus pets, funcionários/admins veem todos.",
        tags=["Pets"]
    ),
    create=extend_schema(
        summary="Criar pet",
        description="Cria um novo pet. Para clientes, o tutor é definido automaticamente. Suporte a upload de foto (multipart/form-data).",
        tags=["Pets"]
    ),
    retrieve=extend_schema(
        summary="Detalhes do pet",
        description="Retorna detalhes de um pet específico.",
        tags=["Pets"]
    ),
    partial_update=extend_schema(
        summary="Atualizar pet",
        description="Atualiza parcialmente um pet. Apenas os campos enviados serão alterados, preservando os demais dados.",
        tags=["Pets"]
    ),
    destroy=extend_schema(
        summary="Deletar pet",
        description="Remove um pet do sistema. Apenas o dono ou admin pode deletar.",
        tags=["Pets"]
    ),
)
class PetViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar pets do sistema.
    
    Funcionalidades:
    - Clientes veem apenas seus próprios pets
    - Funcionários e admins veem todos os pets
    - Upload de fotos suportado
    - Validações automáticas de permissão
    - Apenas atualização parcial (PATCH) para segurança dos dados
    """
    queryset = Pet.objects.select_related('tutor')
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrFuncionario] # <-- Permissões
    parser_classes = [MultiPartParser, FormParser, JSONParser] # <-- Suporte a multipart/form-data
    
    # Lista de ações HTTP permitidas (removendo 'put' que é o método PUT)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        if not profile:
            return Pet.objects.none()
            
        if profile.role == Profile.Role.CLIENTE:
            return self.queryset.filter(tutor=user)
        return self.queryset.all()

    def perform_create(self, serializer): # <-- Lógica de criação
        user = self.request.user
        profile = getattr(user, 'profile', None)
        # Funcionário/Admin: deve especificar tutor
        if profile and profile.role in [Profile.Role.ADMIN, Profile.Role.FUNCIONARIO]:
            tutor = serializer.validated_data.get('tutor')
            if not tutor:
                raise serializers.ValidationError({"tutor": "Funcionário deve especificar o tutor do pet."})
            serializer.save()
        else:
            # Cliente: tutor é sempre o próprio usuário
            serializer.save(tutor=user)
        
        logger.info(f"Pet criado por {self.request.user.email}")
    
    def destroy(self, request, *args, **kwargs):
        """Override do método destroy para adicionar logs"""
        pet = self.get_object()
        user_profile = getattr(request.user, 'profile', None)
        
        # Log para debug
        if user_profile and user_profile.role == 'FUNCIONARIO':
            print(f"Tentativa de DELETE de pet {pet.nome} por funcionário {request.user.username}")
            
        return super().destroy(request, *args, **kwargs)