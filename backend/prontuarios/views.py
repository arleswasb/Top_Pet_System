# prontuarios/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Prontuario
from .serializers import ProntuarioSerializer
from .permissions import IsOwnerOrAdminOrVet
from users.models import Profile


class ProntuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar prontuários médicos dos pets.
    """
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrVet]

    def get_queryset(self):
        """
        Filtra prontuários baseado no perfil do usuário.
        Tutores veem apenas prontuários de seus pets.
        Funcionários e admins veem todos.
        """
        user = self.request.user
        
        # Verificar se o usuário tem profile
        if not hasattr(user, 'profile'):
            # Se não tem profile, assumir que é cliente e só ver prontuários de seus pets
            return Prontuario.objects.filter(pet__tutor=user)
        
        # Admins e funcionários veem todos os prontuários
        if user.profile.role in [Profile.Role.ADMIN, Profile.Role.FUNCIONARIO] or user.is_staff:
            return Prontuario.objects.all()
        
        # Clientes/tutores veem apenas prontuários de seus pets
        return Prontuario.objects.filter(pet__tutor=user)

    @action(detail=False, methods=["get"], url_path=r"por-pet/(?P<pet_id>\d+)")
    def por_pet(self, request, pet_id=None):
        """
        Retorna todos os prontuários de um pet específico.
        """
        prontuarios = self.get_queryset().filter(pet_id=pet_id)
        serializer = self.get_serializer(prontuarios, many=True)
        return Response(serializer.data)