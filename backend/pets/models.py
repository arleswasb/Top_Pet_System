# pets/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator # Importado MaxValueValidator
from datetime import date
from django.utils import timezone # Importado timezone para o default

class Pet(models.Model):
    """
    Representa um animal de estimação no sistema.

    Este modelo armazena informações detalhadas sobre cada pet,
    incluindo seu nome, espécie, raça, data de nascimento, sexo,
    foto e o tutor responsável.

    Atributos:
        nome (str): O nome do pet.
        especie (str): A espécie do pet (ex: "Cachorro", "Gato").
        raca (str, opcional): A raça específica do pet.
        data_de_nascimento (date, opcional): A data em que o pet nasceu.
        sexo (str): O sexo do pet, escolhido de opções pré-definidas.
        foto (ImageField, opcional): Uma foto do pet.
        tutor (User): O usuário (tutor) associado a este pet.
        observacoes (str, opcional): Quaisquer notas ou observações adicionais.
        created_at (datetime): A data e hora de criação do registro.
        updated_at (datetime): A data e hora da última atualização do registro.
    """

    class Gender(models.TextChoices):
        MALE = "MACHO", "Macho"
        FEMALE = "FEMEA", "Fêmea"
        UNKNOWN = "DESCONHECIDO", "Desconhecido"

    nome = models.CharField(max_length=100, verbose_name="Nome")
    especie = models.CharField(max_length=50, verbose_name="Espécie") # Mantido como CharField por simplicidade inicial
    raca = models.CharField(max_length=50, blank=True, null=True, verbose_name="Raça")
    
    data_de_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Nascimento",
        validators=[MaxValueValidator(limit_value=date.today)] # Validador para não permitir datas futuras
    )
    
    sexo = models.CharField(
        max_length=15,
        choices=Gender.choices,
        default=Gender.UNKNOWN,
        verbose_name="Sexo"
    )

    foto = models.ImageField(
        upload_to='pets_photos/', # Renomeado para 'pets_photos/' para clareza
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

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado Em"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        indexes = [
            models.Index(fields=['tutor'], name='pet_tutor_idx'),
            models.Index(fields=['especie'], name='pet_especie_idx'), # Adicionado índice para espécie
            models.Index(fields=['raca'], name='pet_raca_idx'),      # Adicionado índice para raça
        ]
        verbose_name = "Pet"
        verbose_name_plural = "Pets"


    def __str__(self):
        return f"{self.nome} ({self.especie})" # Melhorando a representação

    @property
    def idade(self):
        """
        Calcula e retorna a idade do pet em anos.

        A idade é calculada com base na `data_de_nascimento`.
        Se a data de nascimento não for fornecida, retorna None.

        Returns:
            int | None: A idade do pet em anos, ou None se a data de
                        nascimento for desconhecida.
        """
        if self.data_de_nascimento:
            today = date.today()
            # Calcula a idade considerando meses e dias
            age = today.year - self.data_de_nascimento.year - \
                  ((today.month, today.day) < (self.data_de_nascimento.month, self.data_de_nascimento.day))
            return age
        return None