# pets/tests_unidade.py

from django.test import TestCase
from datetime import date
from unittest import mock
from .models import Pet

# --- Testes de Unidade para o Modelo Pet ---

class PetUnitTests(TestCase):
    """
    Suíte de testes de unidade para o modelo `Pet`.

    Estes testes focam em validar a lógica de métodos individuais do modelo
    de forma isolada, sem depender de interações com o banco de dados ou
    outros componentes do sistema. Utiliza-se `unittest.mock` para
    substituir dependências externas, como a data atual.
    """

    @mock.patch('pets.models.date')
    def test_calculo_idade_exata(self, mock_date):
        """
        Testa o cálculo da idade do pet em um cenário ideal.

        Verifica se a propriedade `idade` retorna o valor correto quando a
        data atual coincide exatamente com o aniversário do pet.
        """
        # 1. Configuramos o mock para que 'date.today()' sempre retorne a mesma data
        mock_date.today.return_value = date(2023, 10, 27)

        # 2. Criamos uma instância do Pet em memória, SEM salvar no banco
        data_nascimento = date(2020, 10, 27)
        pet = Pet(nome="Unit-Test-Dog", data_de_nascimento=data_nascimento)

        # 3. Verificamos se a propriedade 'idade' calcula o valor corretamente
        self.assertEqual(pet.idade, 3)

    @mock.patch('pets.models.date')
    def test_calculo_idade_aniversario_amanha(self, mock_date):
        """
        Testa o cálculo da idade na véspera do aniversário do pet.

        Garante que a idade não é incrementada antes da data exata do
        aniversário.
        """
        mock_date.today.return_value = date(2023, 10, 26)
        data_nascimento = date(2020, 10, 27)
        pet = Pet(nome="Almost-Birthday-Dog", data_de_nascimento=data_nascimento)
        
        # A idade ainda deve ser 2, pois o aniversário é amanhã
        self.assertEqual(pet.idade, 2)

    def test_idade_sem_data_nascimento(self):
        """
        Testa o comportamento da propriedade `idade` quando não há data de nascimento.

        Verifica se a propriedade `idade` retorna `None` se o campo
        `data_de_nascimento` do pet não estiver definido.
        """
        pet = Pet(nome="No-Bday-Dog")
        self.assertIsNone(pet.idade)
