from django.db import models

class Pet(models.Model):
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raca = models.CharField(max_length=50, blank=True, null=True)
    idade = models.IntegerField(null=True, blank=True)
    data_de_nascimento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='pets/', null=True, blank=True)

    def __str__(self):
        return self.nome
