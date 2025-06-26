# agendamentos/models.py

from datetime import timedelta

from django.db import models
from pets.models import Pet


class Servico(models.Model):
    """
    Modelo para cadastrar os serviços oferecidos pelo pet shop.
    Ex: Banho e Tosa, Consulta, Vacinação.
    """

    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    duracao = models.DurationField(
        default=timedelta(minutes=30),
        help_text="Duração do serviço. Formato: HH:MM:SS",
    )
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    disponivel = models.BooleanField(
        default=True,
        help_text="Marque se o serviço está sendo oferecido no momento.",
    )

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    """
    Modelo para registrar os agendamentos dos pets.
    Agora se relaciona com o modelo Servico.
    """

    class StatusChoices(models.TextChoices):
        AGENDADO = "AGENDADO", "Agendado"
        CONCLUIDO = "CONCLUIDO", "Concluído"
        CANCELADO = "CANCELADO", "Cancelado"

    # Relacionamentos
    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name="agendamentos"
    )
    # O campo 'servico' agora é uma chave estrangeira
    servico = models.ForeignKey(
        Servico, on_delete=models.PROTECT, related_name="agendamentos"
    )

    # Detalhes do agendamento
    data_hora = models.DateTimeField()
    status = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.AGENDADO,
    )
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["data_hora"]

    def __str__(self):
        return (
            f"{self.servico.nome} para {self.pet.nome} em "
            f"{self.data_hora.strftime('%d/%m/%Y %H:%M')}"
        )