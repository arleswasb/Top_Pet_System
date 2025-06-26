"""Permissions for users app."""

from rest_framework import permissions

from .models import Profile


class IsAdminRole(permissions.BasePermission):
    """Allow access only to admin users."""

    def has_permission(self, request, view):
        """Check if user is admin."""
        return (
            hasattr(request.user, "profile")
            and request.user.profile.role == Profile.Role.ADMIN
        )