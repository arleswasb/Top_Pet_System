# agendamento/views.py

# --- Novas importações necessárias ---
from datetime import date, datetime, time, timedelta
from rest_framework.decorators import api_view, permission_classes
# --- Fim das novas importações ---

from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Agendamento, Servico
from .serializers import AgendamentoSerializer, ServicoSerializer
from .permissions import IsTutorOrAdminOrFuncionario
from users.permissions import IsAdminRole, IsFuncionarioOrAdmin
from users.models import Profile

@extend_schema_view(
    list=extend_schema(summary="Listar serviços", tags=["Serviços"]),
    create=extend_schema(summary="Criar serviço", tags=["Serviços"]),
    retrieve=extend_schema(summary="Detalhes do serviço", tags=["Serviços"]),
    partial_update=extend_schema(summary="Atualizar serviço", tags=["Serviços"]),
    destroy=extend_schema(summary="Deletar serviço", tags=["Serviços"])
)
class ServicoViewSet(viewsets.ModelViewSet):
    """
    Endpoint que permite gerenciar os Serviços da clínica veterinária.
    - **Listar/Ver**: Qualquer usuário autenticado
    - **Criar/Editar/Excluir**: Administradores, funcionários e veterinários
    """
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        else:
            # Criar/editar/deletar: admin, funcionário ou veterinário
            return [permissions.IsAuthenticated(), IsFuncionarioOrAdmin()]


@extend_schema_view(
    list=extend_schema(summary="Listar agendamentos", tags=["Agendamentos"]),
    create=extend_schema(summary="Criar agendamento", tags=["Agendamentos"]),
    retrieve=extend_schema(summary="Detalhes do agendamento", tags=["Agendamentos"]),
    partial_update=extend_schema(summary="Atualizar agendamento", tags=["Agendamentos"]),
    destroy=extend_schema(summary="Cancelar agendamento", tags=["Agendamentos"])
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
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'profile'):
            return Agendamento.objects.filter(pet__tutor=user)
        
        if user.profile.role in [Profile.Role.ADMIN, Profile.Role.VETERINARIO, Profile.Role.FUNCIONARIO] or user.is_staff:
            return Agendamento.objects.all()
        
        return Agendamento.objects.filter(pet__tutor=user)

    def perform_create(self, serializer):
        pet = serializer.validated_data.get('pet')
        user = self.request.user
        
        if hasattr(user, 'profile') and user.profile.role == Profile.Role.CLIENTE:
            if pet.tutor != user:
                raise serializers.ValidationError({"detail": "Você não tem permissão para agendar para este pet."})
        
        serializer.save()

# --- NOVA VIEW ADICIONADA ---

@extend_schema(
    summary="Listar horários disponíveis",
    description="Retorna uma lista de horários disponíveis para agendamento em um dia específico.",
    tags=["Horários"],
    parameters=[
        OpenApiParameter(
            name='data',
            description='Data para consulta no formato YYYY-MM-DD.',
            required=True,
            type=OpenApiTypes.DATE
        )
    ]
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def horarios_disponiveis(request):
    """
    Endpoint para listar os horários disponíveis para agendamento em um dia específico.
    Espera um parâmetro 'data' na query string no formato YYYY-MM-DD.
    """
    # 1. Obter e validar a data da requisição
    data_str = request.query_params.get('data')
    if not data_str:
        return Response(
            {"detail": "O parâmetro 'data' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        data_selecionada = date.fromisoformat(data_str)
    except ValueError:
        return Response(
            {"detail": "Formato de data inválido. Use YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if data_selecionada < date.today():
        return Response(
            {"detail": "Não é possível consultar horários para datas passadas."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. Definir regras de negócio para os horários
    HORA_INICIO_EXPEDIENTE = time(8, 0)
    HORA_FIM_EXPEDIENTE = time(18, 0)
    DURACAO_SERVICO_MINUTOS = 60  # Duração de 1 hora

    # 3. Gerar todos os horários possíveis para o dia
    horarios_possiveis = []
    horario_atual = datetime.combine(data_selecionada, HORA_INICIO_EXPEDIENTE)
    fim_expediente = datetime.combine(data_selecionada, HORA_FIM_EXPEDIENTE)

    while horario_atual < fim_expediente:
        horarios_possiveis.append(horario_atual.time())
        horario_atual += timedelta(minutes=DURACAO_SERVICO_MINUTOS)

    # 4. Obter todos os agendamentos já existentes para a data selecionada
    agendamentos_no_dia = Agendamento.objects.filter(data_hora__date=data_selecionada)
    horarios_ocupados = {ag.data_hora.time() for ag in agendamentos_no_dia}

    # 5. Filtrar e retornar apenas os horários disponíveis
    horarios_disponiveis_formatados = [
        horario.strftime('%H:%M') for horario in horarios_possiveis
        if horario not in horarios_ocupados
    ]

    return Response(horarios_disponiveis_formatados, status=status.HTTP_200_OK)