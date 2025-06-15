from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        FUNCIONARIO = "FUNCIONARIO", "Funcionário"
        CLIENTE = "CLIENTE", "Cliente"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CLIENTE)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"