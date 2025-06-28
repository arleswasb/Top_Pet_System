# agendamentos/views.py

from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Agendamento, Servico
from .serializers import AgendamentoSerializer, ServicoSerializer
from .permissions import IsTutorOrAdminOrFuncionario
from users.models import Profile

@extend_schema_view(
    list=extend_schema(
        summary="Listar serviços",
        description="Lista todos os serviços disponíveis na clínica veterinária.",
        tags=["Serviços"]
    ),
    retrieve=extend_schema(
        summary="Detalhes do serviço",
        description="Obtém os detalhes de um serviço específico.",
        tags=["Serviços"]
    ),
    create=extend_schema(
        summary="Criar serviço",
        description="Cria um novo serviço (apenas admin).",
        tags=["Serviços"]
    ),
    partial_update=extend_schema(
        summary="Atualizar serviço",
        description="Atualiza parcialmente um serviço (apenas admin).",
        tags=["Serviços"]
    ),
    destroy=extend_schema(
        summary="Excluir serviço",
        description="Exclui um serviço (apenas admin).",
        tags=["Serviços"]
    ),
)
class ServicoViewSet(viewsets.ModelViewSet):
    """
    Endpoint que permite gerenciar os Serviços da clínica veterinária.
    
    - **Listar/Ver**: Qualquer usuário autenticado
    - **Criar/Editar/Excluir**: Apenas administradores
    """
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [permissions.IsAdminUser]

    # Lista de ações HTTP permitidas (removendo 'put' que é o método PUT)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        # Permite que qualquer usuário autenticado possa listar ou ver detalhes (leitura)
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # Para outras ações (create, update, delete), exige que seja admin.
        return super().get_permissions()


@extend_schema_view(
    list=extend_schema(
        summary="Listar agendamentos",
        description="Lista agendamentos conforme permissão do usuário:\n"
                   "- **Clientes**: Apenas seus próprios agendamentos\n"
                   "- **Funcionários/Veterinários/Admins**: Todos os agendamentos",
        tags=["Agendamentos"]
    ),
    retrieve=extend_schema(
        summary="Detalhes do agendamento",
        description="Obtém os detalhes de um agendamento específico.",
        tags=["Agendamentos"]
    ),
    create=extend_schema(
        summary="Criar agendamento",
        description="Cria um novo agendamento para um pet.",
        tags=["Agendamentos"]
    ),
    partial_update=extend_schema(
        summary="Atualizar agendamento",
        description="Atualiza parcialmente um agendamento (ex: alterar status).",
        tags=["Agendamentos"]
    ),
    destroy=extend_schema(
        summary="Cancelar agendamento",
        description="Cancela/exclui um agendamento.",
        tags=["Agendamentos"]
    ),
)
class AgendamentoViewSet(viewsets.ModelViewSet):
    """
    Endpoint para gerenciar agendamentos de consultas e serviços.
    
    **Permissões:**
    - **Clientes**: Podem criar agendamentos para seus pets e ver apenas os próprios
    - **Funcionários/Veterinários**: Podem ver e gerenciar todos os agendamentos
    - **Admins**: Acesso completo a todos os agendamentos
    """
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutorOrAdminOrFuncionario]

    # Lista de ações HTTP permitidas (removendo 'put' que é o método PUT)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        
        # Verificar se o usuário tem profile
        if not hasattr(user, 'profile'):
            # Se não tem profile, assumir que é cliente e só ver seus agendamentos
            return Agendamento.objects.filter(pet__tutor=user)
        
        # Admins e funcionários veem todos os agendamentos
        if user.profile.role in [Profile.Role.ADMIN, Profile.Role.FUNCIONARIO] or user.is_staff:
            return Agendamento.objects.all()
        
        # Clientes/tutores veem apenas agendamentos de seus pets
        return Agendamento.objects.filter(pet__tutor=user)

    def perform_create(self, serializer):
        pet = serializer.validated_data.get('pet')
        user = self.request.user
        
        # Verificar se o usuário tem permissão para agendar para este pet
        if hasattr(user, 'profile') and user.profile.role == Profile.Role.CLIENTE:
            if pet.tutor != user:
                raise serializers.ValidationError({"detail": "Você não tem permissão para agendar para este pet."})
        
        serializer.save()