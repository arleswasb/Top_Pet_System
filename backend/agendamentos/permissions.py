# agendamentos/permissions.py

from rest_framework import permissions
from users.models import Profile

# O nome da classe é o que você já usa, está ótimo.
class IsTutorOrAdminOrFuncionario(permissions.BasePermission):
    """
    Permissão customizada para Agendamentos.
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
            return False

        user_profile = request.user.profile

        if user_profile.role == Profile.Role.ADMIN:
            return True

        # A verificação obj.pet.tutor está correta para um agendamento.
        if obj.pet.tutor == request.user:
            return True

        if user_profile.role == Profile.Role.FUNCIONARIO:
            return True

        return False