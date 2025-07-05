# prontuarios/views.py

from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Prontuario
from .serializers import ProntuarioSerializer
from .permissions import IsOwnerOrAdminOrVet
from users.models import Profile


@extend_schema_view(
    list=extend_schema(
        summary="Listar prontuários",
        description="Lista prontuários médicos conforme permissão do usuário:\n"
                   "- **Clientes**: Apenas prontuários dos seus pets\n"
                   "- **Funcionários/Admins**: Todos os prontuários\n"
                   "- **Veterinários**: Podem criar e ver todos os prontuários",
        tags=["Prontuários"]
    ),
    retrieve=extend_schema(
        summary="Detalhes do prontuário",
        description="Obtém os detalhes completos de um prontuário médico.",
        tags=["Prontuários"]
    ),
    create=extend_schema(
        summary="Criar prontuário",
        description="Cria um novo prontuário médico (apenas veterinários e admins).",
        tags=["Prontuários"]
    ),
    partial_update=extend_schema(
        summary="Atualizar prontuário",
        description="Atualiza parcialmente um prontuário médico.",
        tags=["Prontuários"]
    ),
    destroy=extend_schema(
        summary="Excluir prontuário",
        description="Exclui um prontuário médico (apenas admins).",
        tags=["Prontuários"]
    ),
)
class ProntuarioViewSet(viewsets.ModelViewSet):
    """
    Endpoint para gerenciar prontuários médicos dos pets.
    
    **Permissões:**
    - **Clientes**: Podem ver apenas prontuários dos seus pets
    - **Veterinários**: Podem criar e gerenciar prontuários
    - **Funcionários**: Podem ver todos os prontuários
    - **Admins**: Acesso completo a todos os prontuários
    """
    queryset = Prontuario.objects.select_related('pet', 'veterinario')
    serializer_class = ProntuarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrVet]

    # Lista de ações HTTP permitidas (removendo 'put' que é o método PUT)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        if not profile:
            # Se não tem profile, assumir que é cliente e só ver prontuários dos seus pets
            return Prontuario.objects.filter(pet__tutor=user)
        
        if profile.role in [Profile.Role.ADMIN, Profile.Role.FUNCIONARIO, Profile.Role.VETERINARIO] or user.is_staff:
            # Admins, funcionários e veterinários veem todos os prontuários
            return self.queryset.all()
        
        # Clientes/tutores veem apenas prontuários de seus pets
        return self.queryset.filter(pet__tutor=user)

    def perform_create(self, serializer):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        # Verificar se o usuário pode criar prontuários para o pet especificado
        pet = serializer.validated_data.get('pet')
        if profile and profile.role == Profile.Role.CLIENTE:
            if pet.tutor != user:
                raise serializers.ValidationError({
                    "detail": "Você não tem permissão para criar prontuários para este pet."
                })
        
        # Se for funcionário/admin e não especificou veterinário, usar o usuário atual
        if 'veterinario' not in serializer.validated_data:
            serializer.save(veterinario=user)
        else:
            serializer.save()

'''
class ProntuarioUpdateView(UpdateAPIView):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer
    # Remova o lookup_field para usar o padrão 'pk'
'''