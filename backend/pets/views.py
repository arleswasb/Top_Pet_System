# pets/views.py
import logging
from rest_framework import viewsets, permissions, serializers
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
        description="Cria um novo pet. Para clientes, o tutor é definido automaticamente.",
        tags=["Pets"]
    ),
    retrieve=extend_schema(
        summary="Detalhes do pet",
        description="Retorna detalhes de um pet específico.",
        tags=["Pets"]
    ),
    update=extend_schema(
        summary="Atualizar pet",
        description="Atualiza completamente um pet.",
        tags=["Pets"]
    ),
    partial_update=extend_schema(
        summary="Atualizar pet parcialmente",
        description="Atualiza parcialmente um pet.",
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
    """
    queryset = Pet.objects.select_related('tutor')
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrFuncionario] # <-- Permissões

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
        
        if profile and profile.role == Profile.Role.CLIENTE:
            serializer.save(tutor=user)
        else:
            if 'tutor' not in serializer.validated_data:
                raise serializers.ValidationError(
                    {"tutor": "O tutor é obrigatório para funcionários/admins"}
                )
            serializer.save()
        
        logger.info(f"Pet criado por {user.email}")