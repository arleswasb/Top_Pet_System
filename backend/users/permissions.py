from rest_framework import permissions
from .models import Profile

class IsAdminRole(permissions.BasePermission):
    """
    Permite acesso apenas a usuários com o papel de Admin.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.ADMIN

class IsFuncionarioOrAdmin(permissions.BasePermission):
    """
    Permite acesso a funcionários e administradores.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if not hasattr(request.user, 'profile'):
            return False
        user_role = request.user.profile.role
        return user_role in [Profile.Role.FUNCIONARIO, Profile.Role.ADMIN, Profile.Role.VETERINARIO]