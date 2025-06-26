# pets/views.py
import logging

from rest_framework import permissions, serializers, viewsets

from users.models import Profile

from .models import Pet
from .permissions import IsOwnerOrAdminOrFuncionario  # <-- Sua permissão personalizada
from .serializers import PetSerializer

logger = logging.getLogger(__name__)


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.select_related("tutor")
    serializer_class = PetSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdminOrFuncionario,
    ]  # <-- Permissões

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, "profile", None)

        if not profile:
            return Pet.objects.none()

        if profile.role == Profile.Role.CLIENTE:
            return self.queryset.filter(tutor=user)
        return self.queryset.all()

    def perform_create(self, serializer):  # <-- Lógica de criação
        user = self.request.user
        profile = getattr(user, "profile", None)

        if profile and profile.role == Profile.Role.CLIENTE:
            serializer.save(tutor=user)
        else:
            if "tutor" not in serializer.validated_data:
                raise serializers.ValidationError(
                    {"tutor": "O tutor é obrigatório para funcionários/admins"}
                )
            serializer.save()

        logger.info(f"Pet criado por {user.email}")