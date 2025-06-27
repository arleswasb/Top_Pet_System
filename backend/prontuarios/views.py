# prontuarios/views.py

from rest_framework import viewsets, permissions, serializers
from .models import Prontuario
from .serializers import ProntuarioSerializer
from .permissions import IsOwnerOrAdminOrVet
from users.models import Profile


class ProntuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar prontuários médicos dos pets.
    """
    queryset = Prontuario.objects.select_related('pet', 'veterinario')
    serializer_class = ProntuarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrVet]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        
        if not profile:
            # Se não tem profile, assumir que é cliente e só ver prontuários dos seus pets
            return Prontuario.objects.filter(pet__tutor=user)
        
        if profile.role in [Profile.Role.ADMIN, Profile.Role.FUNCIONARIO] or user.is_staff:
            # Admins e funcionários veem todos os prontuários
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