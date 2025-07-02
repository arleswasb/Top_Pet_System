# pets/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from datetime import date
import calendar

class Pet(models.Model):
    class Gender(models.TextChoices):
        MALE = "MACHO", "Macho"
        FEMALE = "FEMEA", "Fêmea"
        UNKNOWN = "DESCONHECIDO", "Desconhecido"

    nome = models.CharField(max_length=100, verbose_name="Nome")
    especie = models.CharField(max_length=50, verbose_name="Espécie")
    raca = models.CharField(max_length=50, blank=True, null=True, verbose_name="Raça")
    data_de_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Nascimento",
        validators=[MaxValueValidator(limit_value=date.today)]
    )
    sexo = models.CharField(
        max_length=15,
        choices=Gender.choices,
        default=Gender.UNKNOWN,
        verbose_name="Sexo"
    )
    foto = models.ImageField(
        upload_to='pets_photos/',
        null=True,
        blank=True,
        verbose_name="Foto do Pet"
    )
    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pets',
        verbose_name="Tutor"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações Adicionais"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado Em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        indexes = [
            models.Index(fields=['tutor'], name='pet_tutor_idx'),
            models.Index(fields=['especie'], name='pet_especie_idx'),
            models.Index(fields=['raca'], name='pet_raca_idx'),
        ]
        verbose_name = "Pet"
        verbose_name_plural = "Pets"

    def __str__(self):
        return f"{self.nome} ({self.especie})"

    @property
    def idade_detalhada(self):
        """
        Calcula a idade de forma detalhada e retorna um dicionário
        com anos, meses e dias.
        """
        if not self.data_de_nascimento:
            return None

        today = date.today()
        birth_date = self.data_de_nascimento

        # Lógica para "emprestar" dos meses e anos se os dias/meses forem negativos
        anos = today.year - birth_date.year
        meses = today.month - birth_date.month
        dias = today.day - birth_date.day

        if dias < 0:
            meses -= 1
            # Pega o número de dias do mês anterior
            last_month = today.month - 1 if today.month > 1 else 12
            year_of_last_month = today.year if today.month > 1 else today.year - 1
            dias += calendar.monthrange(year_of_last_month, last_month)[1]

        if meses < 0:
            anos -= 1
            meses += 12
            
        return {"anos": anos, "meses": meses, "dias": dias}