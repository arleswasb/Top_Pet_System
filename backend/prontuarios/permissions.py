# prontuarios/permissions.py

from rest_framework import permissions
from users.models import Profile


class IsOwnerOrAdminOrVet(permissions.BasePermission):
    """
    Permissão customizada para prontuários:
    - Admin: acesso total
    - Veterinário: pode ver/editar/criar todos
    - Funcionário: pode ver/editar/criar todos
    - Cliente: só pode ver os próprios pets
    """
    
    def has_permission(self, request, view):
        # Usuário deve estar autenticado
        if not (request.user and request.user.is_authenticated):
            return False
            
        # Para operações de criação, verificar se o usuário pode criar
        if view.action == 'create':
            # Admin e Superuser sempre podem criar
            if request.user.is_superuser:
                return True
                
            # Verificar se tem perfil
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                # Veterinário, Funcionário e Admin podem criar
                if profile.role in [Profile.Role.ADMIN, Profile.Role.VETERINARIO, Profile.Role.FUNCIONARIO]:
                    return True
            
            # Staff também pode criar
            if request.user.is_staff:
                return True
                
            # Cliente não pode criar prontuários
            return False
        
        # Para outras operações (list, retrieve), todos autenticados podem tentar
        return True
    
    def has_object_permission(self, request, view, obj):
        # Admin tem acesso total
        if request.user.is_superuser:
            return True
        
        # Verificar se o usuário tem perfil
        profile = getattr(request.user, 'profile', None)
        
        # Para operações de exclusão, apenas admin
        if view.action == 'destroy':
            if profile and profile.role == Profile.Role.ADMIN:
                return True
            return request.user.is_superuser
        
        # Admin, Veterinário e Funcionário têm acesso de leitura/edição
        if profile and profile.role in [Profile.Role.ADMIN, Profile.Role.VETERINARIO, Profile.Role.FUNCIONARIO]:
            return True
        
        # Staff também tem acesso de leitura/edição
        if request.user.is_staff:
            return True
        
        # Cliente só pode ver prontuários dos próprios pets (apenas leitura)
        if profile and profile.role == Profile.Role.CLIENTE:
            if view.action in ['retrieve', 'list']:
                return obj.pet.tutor == request.user
            else:
                # Cliente não pode editar prontuários
                return False
        
        # Se não tem perfil, assumir que é cliente e só pode ver seus pets
        if not profile and view.action in ['retrieve', 'list']:
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