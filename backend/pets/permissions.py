from rest_framework import permissions
from users.models import Profile

class IsOwnerOrAdminOrFuncionario(permissions.BasePermission):
    """
    Permissão customizada. Regras:
    - Admin: pode tudo.
    - Dono do objeto: pode tudo.
    - Funcionário: pode tudo, exceto apagar.
    """
    def has_object_permission(self, request, view, obj):
        # Se o usuário não tiver um perfil, o acesso é negado.
        if not hasattr(request.user, 'profile'):
            return False

        # Admin sempre tem permissão total.
        if request.user.profile.role == Profile.Role.ADMIN:
            return True

        # O próprio dono do objeto sempre tem permissão total sobre ele.
        if obj.tutor == request.user:
            return True

        # Se o usuário não for Admin nem o dono, verificamos se é um Funcionário.
        # O Funcionário tem permissão para tudo, MENOS para o método DELETE.
        if request.user.profile.role == Profile.Role.FUNCIONARIO:
            return request.method != 'DELETE'

        # Se não se encaixou em nenhuma regra acima, o acesso é negado.
        return False