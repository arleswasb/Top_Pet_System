# Seu arquivo: agendamentos/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Agendamento
from .serializers import AgendamentoSerializer
from .permissions import IsTutorOrAdminOrFuncionario
from pets.models import Pet
from users.models import Profile
# import json # Remova esta linha se 'json' não for mais usado em nenhum outro lugar na viewset

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutorOrAdminOrFuncionario]

    # Este é o método que lida com requisições POST para criação
    def create(self, request, *args, **kwargs):
        # A lógica padrão do DRF para criação de objetos via serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) # Este método chama o seu perform_create customizado
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """
        Filtra agendamentos:
        - Cliente vê apenas os agendamentos dos seus pets.
        - Admin/Funcionário veem todos.
        """
        user = self.request.user
        if user.profile.role == Profile.Role.CLIENTE:
            return Agendamento.objects.filter(pet__tutor=user)

        return Agendamento.objects.all()

    def perform_create(self, serializer):
        """
        Cria um agendamento, garantindo que o cliente
        só pode agendar para um pet que é seu.
        """
        pet_id = self.request.data.get('pet_id')
        try:
            pet = Pet.objects.get(id=pet_id)
            user = self.request.user

            # Regra de segurança: Cliente só pode agendar para seu próprio pet
            if user.profile.role == Profile.Role.CLIENTE and pet.tutor != user:
                raise serializers.ValidationError({"detail": "Você não tem permissão para agendar para este pet."})

            # Se passou na validação, salva o agendamento
            serializer.save(pet=pet)
        except Pet.DoesNotExist:
            raise serializers.ValidationError({"detail": "O pet com o ID fornecido não existe."})