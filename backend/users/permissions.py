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

class CanManageClients(permissions.BasePermission):
    """
    Permite aos funcionários e admins gerenciar usuários clientes.
    - Funcionários: Podem CRUD de clientes apenas
    - Admins: Podem CRUD de qualquer usuário
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if not hasattr(request.user, 'profile'):
            return False
        user_role = request.user.profile.role
        return user_role in [Profile.Role.FUNCIONARIO, Profile.Role.ADMIN]
    
    def has_object_permission(self, request, view, obj):
        if not hasattr(request.user, 'profile'):
            return False
        
        user_role = request.user.profile.role
        
        # Admin pode gerenciar qualquer usuário
        if user_role == Profile.Role.ADMIN:
            return True
        
        # Funcionário pode gerenciar apenas clientes
        if user_role == Profile.Role.FUNCIONARIO:
            # Se o objeto é um usuário, verificar se é cliente
            if hasattr(obj, 'profile'):
                return obj.profile.role == Profile.Role.CLIENTE
            # Se é um profile diretamente
            if hasattr(obj, 'role'):
                return obj.role == Profile.Role.CLIENTE
        
        return False