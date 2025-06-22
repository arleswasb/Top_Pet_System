# pets/views.py

import logging 
from rest_framework import viewsets, permissions, serializers # Adicione serializers
from .models import Pet
from .serializers import PetSerializer
from .permissions import IsOwnerOrAdminOrFuncionario 
from users.models import Profile # Supondo que o Profile esteja em users.models

logger = logging.getLogger(__name__)

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrFuncionario]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Garante que user.profile existe antes de acessá-lo
            if hasattr(user, 'profile') and user.profile.role == Profile.Role.CLIENTE:
                return Pet.objects.filter(tutor=user)
            # Admin ou Funcionário podem ver todos
            elif hasattr(user, 'profile') and user.profile.role in [Profile.Role.ADMIN, Profile.Role.FUNCIONARIO]:
                return Pet.objects.all()
        # Se não for autenticado ou não tiver perfil, não retorna nada
        return Pet.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # Se o usuário logado for um CLIENTE, ele é o tutor.
        if hasattr(user, 'profile') and user.profile.role == Profile.Role.CLIENTE:
            serializer.save(tutor=user)
        
        # Se for um ADMIN ou FUNCIONÁRIO, ele deve ter enviado o tutor_id.
        # O serializer já validou se o tutor_id foi enviado e é válido.
        else:
            serializer.save()