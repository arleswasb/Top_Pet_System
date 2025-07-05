# agendamentos/permissions.py

from rest_framework import permissions
from users.models import Profile

# O nome da classe é o que você já usa, está ótimo.
class IsTutorOrAdminOrFuncionario(permissions.BasePermission):
    """
    Permissão customizada para Agendamentos.
    Permite acesso a tutores, admins, funcionários e veterinários.
    """

    def has_permission(self, request, view):
        # ESTE MÉTODO É A ADIÇÃO NECESSÁRIA.
        # Ele permite que qualquer usuário logado possa TENTAR
        # listar ou criar agendamentos. A lógica específica de "pode ou não pode"
        # será tratada na view ou no has_object_permission.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # A sua lógica aqui já está perfeita para agendamentos.
        if not hasattr(request.user, 'profile'):
            # Se não tem profile, verificar se é staff (funcionário) ou se é o tutor do pet
            if request.user.is_staff or request.user.is_superuser:
                return True
            if hasattr(obj, 'pet') and obj.pet.tutor == request.user:
                return True
            return False

        user_profile = request.user.profile

        if user_profile.role == Profile.Role.ADMIN or request.user.is_superuser:
            return True

        # A verificação obj.pet.tutor está correta para um agendamento.
        if hasattr(obj, 'pet') and obj.pet.tutor == request.user:
            return True

        # Funcionários e veterinários têm acesso total
        if user_profile.role in [Profile.Role.FUNCIONARIO, Profile.Role.VETERINARIO] or request.user.is_staff:
            return True

        return False