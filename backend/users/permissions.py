from rest_framework import permissions
from .models import Profile

class IsAdminRole(permissions.BasePermission):
    """
    Permite acesso apenas a usuários com o papel de Admin.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.ADMIN