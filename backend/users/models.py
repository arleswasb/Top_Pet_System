"""User models."""

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Profile model.

    A profile holds a user's public data like role.
    """

    class Role(models.TextChoices):
        """Role choices."""

        ADMIN = "ADMIN", "Admin"
        FUNCIONARIO = "FUNCIONARIO", "Funcionário"
        CLIENTE = "CLIENTE", "Cliente"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=50, choices=Role.choices, default=Role.CLIENTE
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Última Atualização"
    )

    def __str__(self):
        """Return user's str representation."""
        return f"{self.user.username} - {self.get_role_display()}"