# pets/models.py
import logging
from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models


class Pet(models.Model):

    class Gender(models.TextChoices):
        MALE = "MACHO", "Macho"
        FEMALE = "FEMEA", "Fêmea"
        UNKNOWN = "DESCONHECIDO", "Desconhecido"

    nome = models.CharField(max_length=100, verbose_name="Nome")
    especie = models.CharField(
        max_length=50, verbose_name="Espécie"
    )
    raca = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Raça"
    )

    data_de_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Nascimento",
        validators=[
            MaxValueValidator(limit_value=date.today)
        ],
    )

    sexo = models.CharField(
        max_length=15,
        choices=Gender.choices,
        default=Gender.UNKNOWN,
        verbose_name="Sexo",
    )

    foto = models.ImageField(
        upload_to="pets_photos/",
        null=True,
        blank=True,
        verbose_name="Foto do Pet",
    )

    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pets",
        verbose_name="Tutor",
    )

    observacoes = models.TextField(
        blank=True, null=True, verbose_name="Observações Adicionais"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado Em"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Última Atualização"
    )

    class Meta:
        indexes = [
            models.Index(fields=["tutor"], name="pet_tutor_idx"),
            models.Index(
                fields=["especie"], name="pet_especie_idx"
            ),
            models.Index(
                fields=["raca"], name="pet_raca_idx"
            ),
        ]
        verbose_name = "Pet"
        verbose_name_plural = "Pets"

    def __str__(self):
        return f"{self.nome} ({self.especie})"

    def save(self, *args, **kwargs):
        """Sobrescreve o método save para adicionar um log."""
        super().save(*args, **kwargs)  # Chama o método save original
        logger = logging.getLogger(__name__)
        logger.info(f"Pet '{self.nome}' foi salvo com sucesso.")

    @property
    def idade(self):
        if self.data_de_nascimento:
            today = date.today()
            age = (
                today.year
                - self.data_de_nascimento.year
                - (
                    (today.month, today.day)
                    < (
                        self.data_de_nascimento.month,
                        self.data_de_nascimento.day,
                    )
                )
            )
            return age
        return None