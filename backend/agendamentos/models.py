from django.db import models
from django.conf import settings
from pets.models import Pet

class Agendamento(models.Model):
    class ServicoChoices(models.TextChoices):
        BANHO_E_TOSA = "BANHO_E_TOSA", "Banho e Tosa"
        CONSULTA = "CONSULTA", "Consulta"
        VACINACAO = "VACINACAO", "Vacinação"
        EXAME = "EXAME", "Exame"

    class StatusChoices(models.TextChoices):
        AGENDADO = "AGENDADO", "Agendado"
        CONCLUIDO = "CONCLUIDO", "Concluído"
        CANCELADO = "CANCELADO", "Cancelado"

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='agendamentos')
    data_hora = models.DateTimeField()
    servico = models.CharField(max_length=50, choices=ServicoChoices.choices)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.AGENDADO)
    observacoes = models.TextField(blank=True, null=True)
    # No futuro, podemos adicionar o funcionário que realizou o atendimento
    # funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['data_hora'] # Ordena os agendamentos por data e hora

    def __str__(self):
        return f"{self.servico} para {self.pet.nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"