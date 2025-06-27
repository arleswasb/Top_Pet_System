# prontuarios/models.py

from django.db import models
from django.conf import settings
from pets.models import Pet


class Prontuario(models.Model):
    """
    Modelo para registrar prontuários médicos dos pets.
    Contém informações sobre consultas, diagnósticos, tratamentos e observações.
    """
    
    class TipoConsulta(models.TextChoices):
        CONSULTA_ROTINA = "ROTINA", "Consulta de Rotina"
        EMERGENCIA = "EMERGENCIA", "Emergência"
        RETORNO = "RETORNO", "Retorno"
        VACINACAO = "VACINACAO", "Vacinação"
        CIRURGIA = "CIRURGIA", "Cirurgia"
        EXAME = "EXAME", "Exame"
    
    # Relacionamentos
    pet = models.ForeignKey(
        Pet, 
        on_delete=models.CASCADE, 
        related_name='prontuarios',
        help_text="Pet ao qual pertence este prontuário"
    )
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='prontuarios_veterinario',
        help_text="Veterinário responsável pelo atendimento"
    )
    
    # Informações da consulta
    data_consulta = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora da consulta"
    )
    tipo_consulta = models.CharField(
        max_length=20,
        choices=TipoConsulta.choices,
        default=TipoConsulta.CONSULTA_ROTINA,
        help_text="Tipo de consulta realizada"
    )
    
    # Dados clínicos
    peso = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Peso do animal em kg"
    )
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Temperatura corporal em °C"
    )
    
    # Informações médicas
    sintomas = models.TextField(
        blank=True,
        null=True,
        help_text="Sintomas apresentados pelo animal"
    )
    diagnostico = models.TextField(
        blank=True,
        null=True,
        help_text="Diagnóstico veterinário"
    )
    tratamento = models.TextField(
        blank=True,
        null=True,
        help_text="Tratamento prescrito"
    )
    medicamentos = models.TextField(
        blank=True,
        null=True,
        help_text="Medicamentos prescritos e dosagens"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        help_text="Observações gerais sobre a consulta"
    )
    
    # Acompanhamento
    retorno_recomendado = models.DateField(
        null=True,
        blank=True,
        help_text="Data recomendada para retorno"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-data_consulta']
        verbose_name = 'Prontuário'
        verbose_name_plural = 'Prontuários'
    
    def __str__(self):
        return f"Prontuário de {self.pet.nome} - {self.data_consulta.strftime('%d/%m/%Y')}"


class Exame(models.Model):
    """
    Modelo para registrar exames realizados nos pets.
    """
    
    class TipoExame(models.TextChoices):
        SANGUE = "SANGUE", "Exame de Sangue"
        URINA = "URINA", "Exame de Urina"
        FEZES = "FEZES", "Exame de Fezes"
        RAIO_X = "RAIO_X", "Raio-X"
        ULTRASSOM = "ULTRASSOM", "Ultrassom"
        BIOPSIA = "BIOPSIA", "Biópsia"
        OUTRO = "OUTRO", "Outro"
    
    # Relacionamentos
    prontuario = models.ForeignKey(
        Prontuario,
        on_delete=models.CASCADE,
        related_name='exames',
        help_text="Prontuário ao qual este exame pertence"
    )
    
    # Informações do exame
    tipo_exame = models.CharField(
        max_length=20,
        choices=TipoExame.choices,
        help_text="Tipo de exame realizado"
    )
    data_realizacao = models.DateTimeField(
        help_text="Data e hora da realização do exame"
    )
    data_resultado = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Data e hora do resultado do exame"
    )
    
    # Resultados
    resultado = models.TextField(
        blank=True,
        null=True,
        help_text="Resultado do exame"
    )
    valores_referencia = models.TextField(
        blank=True,
        null=True,
        help_text="Valores de referência para o exame"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        help_text="Observações sobre o exame"
    )
    
    # Arquivo do resultado (opcional)
    arquivo_resultado = models.FileField(
        upload_to='exames/',
        null=True,
        blank=True,
        help_text="Arquivo digital do resultado do exame"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-data_realizacao']
        verbose_name = 'Exame'
        verbose_name_plural = 'Exames'
    
    def __str__(self):
        return f"{self.get_tipo_exame_display()} - {self.prontuario.pet.nome}"


class Vacina(models.Model):
    """
    Modelo para registrar vacinações dos pets.
    """
    
    # Relacionamentos
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vacinas',
        help_text="Pet que recebeu a vacina"
    )
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='vacinas_aplicadas',
        help_text="Veterinário que aplicou a vacina"
    )
    
    # Informações da vacina
    nome_vacina = models.CharField(
        max_length=100,
        help_text="Nome/tipo da vacina aplicada"
    )
    fabricante = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Fabricante da vacina"
    )
    lote = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Lote da vacina"
    )
    
    # Datas
    data_aplicacao = models.DateTimeField(
        help_text="Data e hora da aplicação da vacina"
    )
    data_vencimento = models.DateField(
        null=True,
        blank=True,
        help_text="Data de vencimento da vacina"
    )
    proxima_dose = models.DateField(
        null=True,
        blank=True,
        help_text="Data recomendada para próxima dose"
    )
    
    # Observações
    observacoes = models.TextField(
        blank=True,
        null=True,
        help_text="Observações sobre a vacinação"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-data_aplicacao']
        verbose_name = 'Vacina'
        verbose_name_plural = 'Vacinas'
    
    def __str__(self):
        return f"{self.nome_vacina} - {self.pet.nome} ({self.data_aplicacao.strftime('%d/%m/%Y')})"
