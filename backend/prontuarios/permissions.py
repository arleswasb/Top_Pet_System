# prontuarios/permissions.py

from rest_framework import permissions
from users.models import Profile


class IsOwnerOrAdminOrVet(permissions.BasePermission):
    """
    Permissão customizada para prontuários:
    - Admin: acesso total
    - Veterinário: pode ver/editar todos
    - Cliente: só pode ver os próprios pets
    """
    
    def has_permission(self, request, view):
        # Usuário deve estar autenticado
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin tem acesso total
        if request.user.is_superuser:
            return True
        
        # Verificar se o usuário tem perfil
        if not hasattr(request.user, 'profile'):
            return False
        
        profile = request.user.profile
        
        # Admin e Veterinário têm acesso total
        if profile.role in [Profile.Role.ADMIN, Profile.Role.VETERINARIO, Profile.Role.FUNCIONARIO]:
            return True
        
        # Cliente só pode ver prontuários dos próprios pets
        if profile.role == Profile.Role.CLIENTE:
            return obj.pet.tutor == request.user
        
        return False


class IsPetOwnerOrStaff(permissions.BasePermission):
    """
    Permissão para verificar se o usuário é dono do pet ou staff
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin/Staff tem acesso total
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # Verificar perfil
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            
            # Veterinário e Funcionário têm acesso
            if profile.role in [Profile.Role.ADMIN, Profile.Role.VETERINARIO, Profile.Role.FUNCIONARIO]:
                return True
        
        # Cliente só acessa seus próprios pets
        return obj.tutor == request.user