# users/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        FUNCIONARIO = "FUNCIONARIO", "Funcionário"
        VETERINARIO = "VETERINARIO", "Veterinário"
        CLIENTE = "CLIENTE", "Cliente"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CLIENTE)
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    
    # Campos específicos para veterinários
    crmv = models.CharField(max_length=20, blank=True, null=True, verbose_name="CRMV")
    especialidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Especialidade")

    # ESTES CAMPOS PRECISAM ESTAR AQUI:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"