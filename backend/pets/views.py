# pets/views.py
import logging
from rest_framework import viewsets, permissions, serializers
from .models import Pet
from .serializers import PetSerializer
from .permissions import IsOwnerOrAdminOrFuncionario # <-- Sua permissão personalizada
from users.models import Profile

logger = logging.getLogger(__name__)

class PetViewSet(viewsets.ModelViewSet):
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