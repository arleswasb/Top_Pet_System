# pets/permissions.py

from rest_framework import permissions
from users.models import Profile

class IsOwnerOrAdminOrFuncionario(permissions.BasePermission):
    """
    Permissão customizada. Regras:
    - Admin: pode tudo.
    - Dono do objeto: pode tudo.
    - Funcionário: pode tudo, exceto apagar.
    - Qualquer usuário logado pode listar ou tentar criar.
    """

    def has_permission(self, request, view):
        # --- LINHAS DE DEPURAÇÃO ---
        print(f"--- PERMISSION CHECK: has_permission foi chamado para o método {request.method} ---")
        resultado = request.user and request.user.is_authenticated
        print(f"--- O resultado da permissão foi: {resultado} ---")
        # -------------------------
        return resultado

    def has_object_permission(self, request, view, obj):
        """
        Permissão a nível de objeto (GET de detalhe, PUT, DELETE).
        """
        # Se o usuário não tiver um perfil, o acesso é negado.
        if not hasattr(request.user, 'profile'):
            return False

        # Admin sempre tem permissão total.
        if request.user.profile.role == Profile.Role.ADMIN:
            return True

        # O próprio dono do objeto (tutor do pet) sempre tem permissão total sobre ele.
        # obj aqui é a instância de Pet, então acessamos obj.tutor
        if obj.tutor == request.user:
            return True

        # Se o usuário não for Admin nem o dono, verificamos se é um Funcionário.
        # O Funcionário tem permissão para tudo, MENOS para o método DELETE.
        if request.user.profile.role == Profile.Role.FUNCIONARIO:
            return request.method != 'DELETE'

        # Se não se encaixou em nenhuma regra acima, o acesso é negado.
        return False