from django.db import models
from django.contrib.auth.models import User # Importa o modelo User do Django

class Pet(models.Model):
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50) # 'especie' em vez de 'tipo'
    raca = models.CharField(max_length=50, blank=True, null=True)
    idade = models.IntegerField(null=True, blank=True)
    data_de_nascimento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='pets/', null=True, blank=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets') # Adiciona o campo tutor

    def __str__(self):
        return self.nome
