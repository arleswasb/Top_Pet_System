import logging
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from users.models import Profile

logger = logging.getLogger(__name__)

class IsOwnerOrAdminOrFuncionario(permissions.BasePermission):
    """
    Permissão hierárquica para recursos Pet:
    - ADMIN: Acesso completo (CRUD)
    - DONO: Acesso completo ao seu pet (CRUD)
    - FUNCIONÁRIO: Acesso parcial (Create/Read/Update)
    - OUTROS: Apenas criação (se autenticado)
    """

    def has_permission(self, request, view):
        """Controle de acesso a nível de endpoint"""
        if not request.user.is_authenticated:
            logger.warning(f"Acesso não-autenticado negado para {request.path}")
            return False
            
        # Todos autenticados podem criar pets
        if view.action == 'create':
            return True
            
        # Outras ações são validadas em has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        """Controle de acesso a nível de objeto"""
        profile = getattr(request.user, 'profile', None)
        
        # Bloqueia usuários sem perfil
        if not profile:
            logger.warning(
                f"Acesso negado para {request.user} - Perfil não encontrado"
            )
            raise PermissionDenied(
                "Seu perfil de usuário não está configurado",
                code="profile_missing"
            )

        # 1. Admin tem acesso irrestrito
        if self._is_admin(profile):
            logger.debug(f"Acesso ADMIN concedido para {request.user}")
            return True

        # 2. Dono tem acesso completo
        if obj.tutor == request.user:
            logger.debug(f"Acesso DONO concedido para {request.user}")
            return True

        # 3. Funcionário tem acesso completo (incluindo DELETE) aos pets de clientes
        if self._is_funcionario(profile):
            # Funcionários podem deletar pets apenas de clientes
            if request.method == 'DELETE':
                # Verificar se o dono do pet é um cliente
                if hasattr(obj.tutor, 'profile') and obj.tutor.profile.role == Profile.Role.CLIENTE:
                    logger.debug(f"DELETE de pet de cliente permitido para funcionário {request.user}")
                    return True
                else:
                    logger.warning(
                        f"Tentativa de DELETE de pet não-cliente por funcionário {request.user}"
                    )
                    raise PermissionDenied(
                        "Funcionários podem excluir apenas pets de clientes",
                        code="funcionario_delete_cliente_only"
                    )
            return True

        # 4. Negar outros casos
        logger.warning(
            f"Acesso negado para {request.user} (Role: {profile.role})"
        )
        return False

    # --- Métodos auxiliares ---
    def _is_admin(self, profile):
        return profile.role == Profile.Role.ADMIN

    def _is_funcionario(self, profile):
        return profile.role == Profile.Role.FUNCIONARIO