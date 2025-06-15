import logging 
from rest_framework import viewsets, permissions # Adicione permissions
from .models import Pet
from .serializers import PetSerializer
from .permissions import IsOwnerOrAdminOrFuncionario 

logger = logging.getLogger(__name__)
# views.py

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrFuncionario] # <-- APLIQUE AQUI

    def get_queryset(self):
        # ... (código do get_queryset que já fizemos) ...
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'profile') and user.profile.role == 'CLIENTE':
                return Pet.objects.filter(tutor=user)
            elif hasattr(user, 'profile') and user.profile.role in ['ADMIN', 'FUNCIONARIO']:
                return Pet.objects.all()
        return Pet.objects.none()

    def perform_create(self, serializer):
        serializer.save(tutor=self.request.user)