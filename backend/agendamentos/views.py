# agendamentos/views.py

from rest_framework import viewsets, permissions, serializers
from .models import Agendamento, Servico
from .serializers import AgendamentoSerializer, ServicoSerializer
from .permissions import IsTutorOrAdminOrFuncionario
from users.models import Profile

class ServicoViewSet(viewsets.ModelViewSet):
    """
    Endpoint que permite gerenciar os Serviços.
    """
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    # CORREÇÃO:
    # A permissão padrão do DRF já faz o que queremos.
    # Mas para ser explícito, vamos definir que apenas admins podem modificar.
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        # Permite que qualquer usuário autenticado possa listar ou ver detalhes (leitura)
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # Para outras ações (create, update, delete), exige que seja admin.
        return super().get_permissions()



class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutorOrAdminOrFuncionario]

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