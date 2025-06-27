# prontuarios/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from pets.models import Pet
from prontuarios.models import Prontuario, Exame, Vacina
from users.models import Profile

User = get_user_model()


class ProntuarioModelTest(TestCase):
    """Testes para o modelo Prontuario"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário tutor
        self.tutor = User.objects.create_user(
            username='tutor_test',
            email='tutor@test.com',
            password='testpass123'
        )
        
        # Criar usuário veterinário
        self.veterinario = User.objects.create_user(
            username='vet_test',
            email='vet@test.com',
            password='testpass123'
        )
        
        # Configurar perfis
        Profile.objects.filter(user=self.tutor).update(role=Profile.Role.CLIENTE)
        Profile.objects.filter(user=self.veterinario).update(role=Profile.Role.FUNCIONARIO)
        
        # Criar pet
        self.pet = Pet.objects.create(
            nome='Rex',
            especie='Cachorro',
            raca='Labrador',
            data_de_nascimento=date(2021, 1, 1),
            sexo=Pet.Gender.MALE,
            tutor=self.tutor
        )
    
    def test_criar_prontuario_basico(self):
        """Teste criação de prontuário básico"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            tipo_consulta=Prontuario.TipoConsulta.CONSULTA_ROTINA
        )
        
        self.assertEqual(prontuario.pet, self.pet)
        self.assertEqual(prontuario.veterinario, self.veterinario)
        self.assertEqual(prontuario.tipo_consulta, Prontuario.TipoConsulta.CONSULTA_ROTINA)
        self.assertIsNotNone(prontuario.data_consulta)
        self.assertIsNotNone(prontuario.created_at)
        self.assertIsNotNone(prontuario.updated_at)
    
    def test_prontuario_com_dados_clinicos(self):
        """Teste criação de prontuário com dados clínicos completos"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            tipo_consulta=Prontuario.TipoConsulta.EMERGENCIA,
            peso=Decimal('26.2'),
            temperatura=Decimal('38.5'),
            sintomas='Febre alta e vômito',
            diagnostico='Gastroenterite',
            tratamento='Hidratação e medicação',
            medicamentos='Soro fisiológico, Metoclopramida',
            observacoes='Animal desidratado',
            retorno_recomendado=date.today() + timedelta(days=7)
        )
        
        self.assertEqual(prontuario.peso, Decimal('26.2'))
        self.assertEqual(prontuario.temperatura, Decimal('38.5'))
        self.assertEqual(prontuario.sintomas, 'Febre alta e vômito')
        self.assertEqual(prontuario.diagnostico, 'Gastroenterite')
        self.assertEqual(prontuario.retorno_recomendado, date.today() + timedelta(days=7))
    
    def test_prontuario_str_method(self):
        """Teste do método __str__ do prontuário"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario
        )
        
        expected_str = f"Prontuário de {self.pet.nome} - {prontuario.data_consulta.strftime('%d/%m/%Y')}"
        self.assertEqual(str(prontuario), expected_str)
    
    def test_prontuario_relacionamento_pet(self):
        """Teste relacionamento com Pet"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario
        )
        
        # Verificar se o pet tem acesso aos prontuários
        self.assertIn(prontuario, self.pet.prontuarios.all())
        self.assertEqual(self.pet.prontuarios.count(), 1)
    
    def test_prontuario_relacionamento_veterinario(self):
        """Teste relacionamento com Veterinário"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario
        )
        
        # Verificar se o veterinário tem acesso aos prontuários
        self.assertIn(prontuario, self.veterinario.prontuarios_veterinario.all())
        self.assertEqual(self.veterinario.prontuarios_veterinario.count(), 1)
    
    def test_prontuario_campos_obrigatorios(self):
        """Teste campos obrigatórios do prontuário"""
        from django.db import transaction
        
        # Teste 1: prontuário sem pet deve falhar
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Prontuario.objects.create(
                    veterinario=self.veterinario
                    # pet é obrigatório
                )
        
        # Teste 2: prontuário sem veterinário deve falhar  
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Prontuario.objects.create(
                    pet=self.pet
                    # veterinario é obrigatório
                )
    
    def test_prontuario_ordenacao(self):
        """Teste ordenação dos prontuários por data (mais recente primeiro)"""
        prontuario1 = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario
        )
        
        # Simular prontuário mais antigo alterando o created_at
        prontuario_antigo = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario
        )
        prontuario_antigo.data_consulta = timezone.now() - timedelta(days=1)
        prontuario_antigo.save()
        
        prontuarios = list(Prontuario.objects.all())
        self.assertEqual(prontuarios[0], prontuario1)  # Mais recente primeiro
        self.assertEqual(prontuarios[1], prontuario_antigo)


class ExameModelTest(TestCase):
    """Testes para o modelo Exame"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário tutor
        self.tutor = User.objects.create_user(
            username='tutor_test',
            email='tutor@test.com',
            password='testpass123'
        )
        
        # Criar usuário veterinário
        self.veterinario = User.objects.create_user(
            username='vet_test',
            email='vet@test.com',
            password='testpass123'
        )
        
        # Configurar perfis
        Profile.objects.filter(user=self.tutor).update(role=Profile.Role.CLIENTE)
        Profile.objects.filter(user=self.veterinario).update(role=Profile.Role.FUNCIONARIO)
        
        # Criar pet
        self.pet = Pet.objects.create(
            nome='Mimi',
            especie='Gato',
            raca='Persa',
            data_de_nascimento=date(2022, 6, 1),
            sexo=Pet.Gender.FEMALE,
            tutor=self.tutor
        )
        
        # Criar prontuário
        self.prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            tipo_consulta=Prontuario.TipoConsulta.EXAME
        )
    
    def test_criar_exame_basico(self):
        """Teste criação de exame básico"""
        exame = Exame.objects.create(
            prontuario=self.prontuario,
            tipo_exame=Exame.TipoExame.SANGUE,
            data_realizacao=timezone.now()
        )
        
        self.assertEqual(exame.prontuario, self.prontuario)
        self.assertEqual(exame.tipo_exame, Exame.TipoExame.SANGUE)
        self.assertIsNotNone(exame.data_realizacao)
        self.assertIsNotNone(exame.created_at)
    
    def test_exame_com_resultado_completo(self):
        """Teste criação de exame com resultado completo"""
        data_realizacao = timezone.now()
        data_resultado = data_realizacao + timedelta(hours=24)
        
        exame = Exame.objects.create(
            prontuario=self.prontuario,
            tipo_exame=Exame.TipoExame.SANGUE,
            data_realizacao=data_realizacao,
            data_resultado=data_resultado,
            resultado='Hemoglobina: 12g/dL, Leucócitos: 8000/mm³',
            valores_referencia='Hemoglobina: 12-18g/dL, Leucócitos: 6000-12000/mm³',
            observacoes='Valores dentro da normalidade'
        )
        
        self.assertEqual(exame.data_resultado, data_resultado)
        self.assertIn('Hemoglobina', exame.resultado)
        self.assertIn('normalidade', exame.observacoes)
    
    def test_exame_str_method(self):
        """Teste do método __str__ do exame"""
        exame = Exame.objects.create(
            prontuario=self.prontuario,
            tipo_exame=Exame.TipoExame.RAIO_X,
            data_realizacao=timezone.now()
        )
        
        expected_str = f"Raio-X - {self.pet.nome}"
        self.assertEqual(str(exame), expected_str)
    
    def test_exame_relacionamento_prontuario(self):
        """Teste relacionamento com Prontuário"""
        exame = Exame.objects.create(
            prontuario=self.prontuario,
            tipo_exame=Exame.TipoExame.URINA,
            data_realizacao=timezone.now()
        )
        
        # Verificar se o prontuário tem acesso aos exames
        self.assertIn(exame, self.prontuario.exames.all())
        self.assertEqual(self.prontuario.exames.count(), 1)
    
    def test_exame_campos_obrigatorios(self):
        """Teste campos obrigatórios do exame"""
        with self.assertRaises(IntegrityError):
            Exame.objects.create(
                tipo_exame=Exame.TipoExame.SANGUE,
                data_realizacao=timezone.now()
                # prontuario é obrigatório
            )
    
    def test_exame_ordenacao(self):
        """Teste ordenação dos exames por data de realização (mais recente primeiro)"""
        data_hoje = timezone.now()
        data_ontem = data_hoje - timedelta(days=1)
        
        exame_hoje = Exame.objects.create(
            prontuario=self.prontuario,
            tipo_exame=Exame.TipoExame.SANGUE,
            data_realizacao=data_hoje
        )
        
        exame_ontem = Exame.objects.create(
            prontuario=self.prontuario,
            tipo_exame=Exame.TipoExame.URINA,
            data_realizacao=data_ontem
        )
        
        exames = list(Exame.objects.all())
        self.assertEqual(exames[0], exame_hoje)  # Mais recente primeiro
        self.assertEqual(exames[1], exame_ontem)


class VacinaModelTest(TestCase):
    """Testes para o modelo Vacina"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário tutor
        self.tutor = User.objects.create_user(
            username='tutor_test',
            email='tutor@test.com',
            password='testpass123'
        )
        
        # Criar usuário veterinário
        self.veterinario = User.objects.create_user(
            username='vet_test',
            email='vet@test.com',
            password='testpass123'
        )
        
        # Configurar perfis
        Profile.objects.filter(user=self.tutor).update(role=Profile.Role.CLIENTE)
        Profile.objects.filter(user=self.veterinario).update(role=Profile.Role.FUNCIONARIO)
        
        # Criar pet
        self.pet = Pet.objects.create(
            nome='Buddy',
            especie='Cachorro',
            raca='Golden Retriever',
            data_de_nascimento=date(2023, 1, 1),
            sexo=Pet.Gender.MALE,
            tutor=self.tutor
        )
    
    def test_criar_vacina_basica(self):
        """Teste criação de vacina básica"""
        vacina = Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='V10',
            data_aplicacao=timezone.now()
        )
        
        self.assertEqual(vacina.pet, self.pet)
        self.assertEqual(vacina.veterinario, self.veterinario)
        self.assertEqual(vacina.nome_vacina, 'V10')
        self.assertIsNotNone(vacina.data_aplicacao)
        self.assertIsNotNone(vacina.created_at)
    
    def test_vacina_com_dados_completos(self):
        """Teste criação de vacina com dados completos"""
        data_aplicacao = timezone.now()
        data_vencimento = date.today() + timedelta(days=365)
        proxima_dose = date.today() + timedelta(days=30)
        
        vacina = Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='Antirrábica',
            fabricante='Laboratório XYZ',
            lote='ABC123',
            data_aplicacao=data_aplicacao,
            data_vencimento=data_vencimento,
            proxima_dose=proxima_dose,
            observacoes='Animal reagiu bem à vacina'
        )
        
        self.assertEqual(vacina.fabricante, 'Laboratório XYZ')
        self.assertEqual(vacina.lote, 'ABC123')
        self.assertEqual(vacina.data_vencimento, data_vencimento)
        self.assertEqual(vacina.proxima_dose, proxima_dose)
        self.assertIn('reagiu bem', vacina.observacoes)
    
    def test_vacina_str_method(self):
        """Teste do método __str__ da vacina"""
        data_aplicacao = timezone.now()
        vacina = Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='V8',
            data_aplicacao=data_aplicacao
        )
        
        expected_str = f"V8 - {self.pet.nome} ({data_aplicacao.strftime('%d/%m/%Y')})"
        self.assertEqual(str(vacina), expected_str)
    
    def test_vacina_relacionamento_pet(self):
        """Teste relacionamento com Pet"""
        vacina = Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='Gripe Canina',
            data_aplicacao=timezone.now()
        )
        
        # Verificar se o pet tem acesso às vacinas
        self.assertIn(vacina, self.pet.vacinas.all())
        self.assertEqual(self.pet.vacinas.count(), 1)
    
    def test_vacina_relacionamento_veterinario(self):
        """Teste relacionamento com Veterinário"""
        vacina = Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='Leishmaniose',
            data_aplicacao=timezone.now()
        )
        
        # Verificar se o veterinário tem acesso às vacinas aplicadas
        self.assertIn(vacina, self.veterinario.vacinas_aplicadas.all())
        self.assertEqual(self.veterinario.vacinas_aplicadas.count(), 1)
    
    def test_vacina_campos_obrigatorios(self):
        """Teste campos obrigatórios da vacina"""
        from django.db import transaction
        
        # Teste 1: vacina sem pet deve falhar
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vacina.objects.create(
                    veterinario=self.veterinario,
                    nome_vacina='V10',
                    data_aplicacao=timezone.now()
                    # pet é obrigatório
                )
        
        # Teste 2: vacina sem veterinário deve falhar
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vacina.objects.create(
                    pet=self.pet,
                    nome_vacina='V10',
                    data_aplicacao=timezone.now()
                    # veterinario é obrigatório
                )
    
    def test_vacina_ordenacao(self):
        """Teste ordenação das vacinas por data de aplicação (mais recente primeiro)"""
        data_hoje = timezone.now()
        data_ontem = data_hoje - timedelta(days=1)
        
        vacina_hoje = Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='V10',
            data_aplicacao=data_hoje
        )
        
        vacina_ontem = Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='Antirrábica',
            data_aplicacao=data_ontem
        )
        
        vacinas = list(Vacina.objects.all())
        self.assertEqual(vacinas[0], vacina_hoje)  # Mais recente primeiro
        self.assertEqual(vacinas[1], vacina_ontem)


class IntegracaoModelosTest(TestCase):
    """Testes de integração entre os modelos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário tutor
        self.tutor = User.objects.create_user(
            username='tutor_test',
            email='tutor@test.com',
            password='testpass123'
        )
        
        # Criar usuário veterinário
        self.veterinario = User.objects.create_user(
            username='vet_test',
            email='vet@test.com',
            password='testpass123'
        )
        
        # Configurar perfis
        Profile.objects.filter(user=self.tutor).update(role=Profile.Role.CLIENTE)
        Profile.objects.filter(user=self.veterinario).update(role=Profile.Role.FUNCIONARIO)
        
        # Criar pet
        self.pet = Pet.objects.create(
            nome='Max',
            especie='Cachorro',
            raca='Border Collie',
            data_de_nascimento=date(2020, 6, 1),
            sexo=Pet.Gender.MALE,
            tutor=self.tutor
        )
    
    def test_relacionamentos_completos(self):
        """Teste relacionamentos completos entre modelos"""
        # Criar prontuário
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            tipo_consulta=Prontuario.TipoConsulta.CONSULTA_ROTINA,
            peso=Decimal('20.5'),
            diagnostico='Check-up de rotina'
        )
        
        # Criar exame relacionado ao prontuário
        exame = Exame.objects.create(
            prontuario=prontuario,
            tipo_exame=Exame.TipoExame.SANGUE,
            data_realizacao=timezone.now(),
            resultado='Hemograma normal'
        )
        
        # Criar vacina para o pet
        vacina = Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='V10',
            data_aplicacao=timezone.now()
        )
        
        # Verificar todos os relacionamentos
        self.assertEqual(self.pet.prontuarios.count(), 1)
        self.assertEqual(self.pet.vacinas.count(), 1)
        self.assertEqual(prontuario.exames.count(), 1)
        self.assertEqual(self.veterinario.prontuarios_veterinario.count(), 1)
        self.assertEqual(self.veterinario.vacinas_aplicadas.count(), 1)
        
        # Verificar que o exame está relacionado ao pet através do prontuário
        self.assertEqual(exame.prontuario.pet, self.pet)
    
    def test_cascata_delecao_pet(self):
        """Teste cascata de deleção quando pet é removido"""
        # Criar prontuário e vacina
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario
        )
        
        vacina = Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='V8',
            data_aplicacao=timezone.now()
        )
        
        # Criar exame relacionado ao prontuário
        exame = Exame.objects.create(
            prontuario=prontuario,
            tipo_exame=Exame.TipoExame.SANGUE,
            data_realizacao=timezone.now()
        )
        
        # Verificar que existem registros
        self.assertEqual(Prontuario.objects.count(), 1)
        self.assertEqual(Vacina.objects.count(), 1)
        self.assertEqual(Exame.objects.count(), 1)
        
        # Deletar pet
        self.pet.delete()
        
        # Verificar que prontuários, vacinas e exames foram deletados em cascata
        self.assertEqual(Prontuario.objects.count(), 0)
        self.assertEqual(Vacina.objects.count(), 0)
        self.assertEqual(Exame.objects.count(), 0)
    
    def test_protecao_veterinario(self):
        """Teste proteção contra deleção de veterinário com registros"""
        # Criar prontuário e vacina
        Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario
        )
        
        Vacina.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            nome_vacina='Antirrábica',
            data_aplicacao=timezone.now()
        )
        
        # Tentar deletar veterinário deve gerar erro de proteção
        with self.assertRaises(Exception):  # ProtectedError
            self.veterinario.delete()
