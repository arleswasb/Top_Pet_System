# Importa a classe TestCase do Django, que é a base para escrever testes.
from datetime import date

from django.test import TestCase

from .models import Pet

# Os testes de unidade são focados em testar a menor parte funcional de um código,
# como uma função ou um método de uma classe, de forma isolada.
# Eles não devem depender de serviços externos como bancos de dados, APIs ou o sistema de arquivos.
# O objetivo é garantir que a lógica interna da unidade de código esteja correta.
class PetModelUnitTestCase(TestCase):
    """Testes de unidade para o modelo Pet."""

    def test_idade_calculation(self):
        """
        Verifica se a propriedade 'idade' calcula a idade do pet corretamente.
        """
        # Cria uma data de nascimento para o pet que seja exatamente 2 anos atrás.
        birth_date = date(date.today().year - 2, date.today().month, date.today().day)

        # Instancia um objeto Pet sem salvá-lo no banco de dados.
        # Para um teste de unidade, não precisamos de um tutor ou outros campos,
        # apenas os que são necessários para a lógica que estamos testando.
        pet = Pet(data_de_nascimento=birth_date)

        # A asserção verifica se a idade calculada é igual a 2.
        self.assertEqual(pet.idade, 2)

    def test_idade_is_none_when_no_birth_date(self):
        """
        Verifica se a propriedade 'idade' retorna None quando a data de nascimento não é fornecida.
        """
        # Instancia um pet sem data de nascimento.
        pet = Pet(data_de_nascimento=None)

        # A asserção verifica se a idade é None.
        self.assertIsNone(pet.idade)
