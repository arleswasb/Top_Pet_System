from rest_framework import permissions
from users.models import Profile

class IsTutorOrAdminOrFuncionario(permissions.BasePermission):
    """
    Permissão que permite acesso total ao dono do pet (tutor),
    e acesso diferenciado para Admin e Funcionário.
    """
    def has_object_permission(self, request, view, obj):
        user_profile = request.user.profile

        # Admin pode tudo
        if user_profile.role == Profile.Role.ADMIN:
            return True

        # O dono do pet do agendamento pode tudo
        if obj.pet.tutor == request.user:
            return True

        # Funcionário pode ver e editar, mas não apagar
        if user_profile.role == Profile.Role.FUNCIONARIO:
            return request.method != 'DELETE'

        return False