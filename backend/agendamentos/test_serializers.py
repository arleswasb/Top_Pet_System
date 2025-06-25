import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError

from .models import Servico, Agendamento
from pets.models import Pet
from .serializers import AgendamentoSerializer

# O decorador @pytest.mark.django_db dá acesso ao banco de dados para o teste.
@pytest.mark.django_db
class TestAgendamentoSerializerValidation:
    """
    Testa a validação de sobreposição de agendamentos no AgendamentoSerializer.
    """

    # Fixture para criar um usuário tutor reutilizável
    @pytest.fixture
    def tutor(self):
        return User.objects.create_user(username='tutor_teste', password='123')

    # Fixture para criar um pet reutilizável
    @pytest.fixture
    def pet(self, tutor):
        return Pet.objects.create(
            nome='Rex', 
            especie='Cachorro', 
            tutor=tutor, 
            data_de_nascimento=timezone.now().date() - timedelta(days=365)
        )

    # Fixture para criar um serviço reutilizável
    @pytest.fixture
    def servico_banho(self):
        return Servico.objects.create(
            nome='Banho', 
            duracao=timedelta(hours=1), 
            preco=50.00
        )

    # Fixture para o agendamento base que já existe no sistema
    @pytest.fixture
    def agendamento_existente(self, pet, servico_banho):
        # Agendamento base: Amanhã, das 10:00 às 11:00
        horario_base = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        return Agendamento.objects.create(
            pet=pet,
            servico=servico_banho,
            data_hora=horario_base
        )

    # Usando parametrize para testar vários cenários de conflito
    @pytest.mark.parametrize("horario_conflitante_delta, descricao_cenario", [
        (timedelta(minutes=30), "Começa durante o agendamento existente"),
        (timedelta(minutes=-30), "Termina durante o agendamento existente"),
        (timedelta(minutes=0), "Começa exatamente no mesmo horário"),
    ])
    def test_nao_permite_agendamentos_sobrepostos(self, pet, servico_banho, agendamento_existente, horario_conflitante_delta, descricao_cenario):
        """
        Garante que um ValidationError seja levantado para vários cenários de sobreposição.
        Cenário: {descricao_cenario}
        """
        horario_novo_agendamento = agendamento_existente.data_hora + horario_conflitante_delta
        
        dados_agendamento_conflitante = {
            'pet': pet.id,
            'servico': servico_banho.id,
            'data_hora': horario_novo_agendamento
        }

        serializer = AgendamentoSerializer(data=dados_agendamento_conflitante)
        # O `match` verifica se a mensagem de erro contém o texto esperado
        with pytest.raises(ValidationError, match="já possui um agendamento conflitante"):
            serializer.is_valid(raise_exception=True)

    # Teste para casos que NÃO devem dar conflito
    @pytest.mark.parametrize("horario_valido_delta, descricao_cenario", [
        (timedelta(hours=1), "Começa exatamente quando o anterior termina"),
        (timedelta(hours=-1), "Termina exatamente quando o posterior começa"),
        (timedelta(days=1), "Em um dia completamente diferente"),
    ])
    def test_permite_agendamentos_nao_sobrepostos(self, pet, servico_banho, agendamento_existente, horario_valido_delta, descricao_cenario):
        """
        Garante que agendamentos consecutivos ou distantes (sem sobreposição) sejam permitidos.
        Cenário: {descricao_cenario}
        """
        horario_novo_agendamento = agendamento_existente.data_hora + horario_valido_delta
        dados_agendamento_valido = {
            'pet': pet.id,
            'servico': servico_banho.id,
            'data_hora': horario_novo_agendamento
        }

        serializer = AgendamentoSerializer(data=dados_agendamento_valido)
        assert serializer.is_valid(raise_exception=True)