import logging

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from users.models import Profile

logger = logging.getLogger(__name__)


class IsOwnerOrAdminOrFuncionario(permissions.BasePermission):
    """
    Hierarchical permission for Pet resources:
    - ADMIN: Full access (CRUD)
    - OWNER: Full access to their own pet (CRUD)
    - EMPLOYEE: Partial access (Create/Read/Update)
    - OTHERS: Creation only (if authenticated)
    """

    def has_permission(self, request, view):
        """Endpoint-level access control"""
        if not request.user.is_authenticated:
            logger.warning(
                f"Unauthenticated access denied for {request.path}"
            )
            return False

        if view.action == "create":
            return True

        return True

    def has_object_permission(self, request, view, obj):
        """Object-level access control"""
        profile = getattr(request.user, "profile", None)

        if not profile:
            logger.warning(
                f"Access denied for {request.user} - Profile not found"
            )
            raise PermissionDenied(
                "Your user profile is not configured",
                code="profile_missing",
            )

        if self._is_admin(profile):
            logger.debug(f"ADMIN access granted for {request.user}")
            return True

        if obj.tutor == request.user:
            logger.debug(f"OWNER access granted for {request.user}")
            return True

        if self._is_funcionario(profile):
            if request.method == "DELETE":
                logger.warning(
                    f"DELETE attempt by employee {request.user}"
                )
                raise PermissionDenied(
                    "Employees cannot delete records",
                    code="funcionario_no_delete",
                )
            return True

        logger.warning(
            f"Access denied for {request.user} (Role: {profile.role})"
        )
        return False

    def _is_admin(self, profile):
        return profile.role == Profile.Role.ADMIN

    def _is_funcionario(self, profile):
        return profile.role == Profile.Role.FUNCIONARIO