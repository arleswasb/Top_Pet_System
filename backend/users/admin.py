"""User admin models."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Advanced configuration for Profile model in admin interface."""

    list_display = (
        "user_email",
        "user_username",
        "formatted_role",
        "get_user_is_active",
        "date_joined",
    )
    list_filter = ("role", "user__is_active", "user__date_joined")
    search_fields = (
        "user__username__exact",
        "user__email__exact",
        "user__first_name",
        "user__last_name",
    )
    list_select_related = ("user",)
    raw_id_fields = ("user",)
    list_per_page = 25
    date_hierarchy = "user__date_joined"

    fieldsets = (
        (None, {"fields": ("user",)}),
        (
            _("Role Settings"),
            {"fields": ("role",), "description": _("Define user access level")},
        ),
        (
            _("Metadata"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    @admin.display(description=_("Email"), ordering="user__email")
    def user_email(self, obj):
        """Get user email."""
        return obj.user.email

    @admin.display(description=_("Username"))
    def user_username(self, obj):
        """Get user username."""
        return obj.user.username

    @admin.display(description=_("Role"), ordering="role")
    def formatted_role(self, obj):
        """Get user role."""
        return obj.get_role_display()

    @admin.display(
        description=_("Active?"),
        boolean=True,
        ordering="user__is_active",
    )
    def get_user_is_active(self, obj):
        """Get user active status."""
        return obj.user.is_active

    @admin.display(description=_("Date Joined"), ordering="user__date_joined")
    def date_joined(self, obj):
        """Get user date joined."""
        return obj.user.date_joined


class ProfileInline(admin.StackedInline):
    """Profile inline admin."""

    model = Profile
    can_delete = False
    verbose_name = _("Profile")
    verbose_name_plural = _("Profile Settings")
    fields = ("role", ("created_at", "updated_at"))
    readonly_fields = ("created_at", "updated_at")
    classes = ("collapse",)


class CustomUserAdmin(UserAdmin):
    """Custom user admin."""

    inlines = (ProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "profile_role",
        "date_joined",
    )
    list_select_related = ("profile",)

    def profile_role(self, obj):
        """Get profile role."""
        return obj.profile.get_role_display()

    profile_role.short_description = _("Role")
    profile_role.admin_order_field = "profile__role"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)