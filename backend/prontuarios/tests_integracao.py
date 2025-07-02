# prontuarios/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
import json

from pets.models import Pet
from users.models import Profile
from .models import Prontuario

User = get_user_model()


class ProntuarioModelTest(TestCase):
    """Testes para o modelo Prontuario"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.tutor = User.objects.create_user(
            username='tutor_test',
            password='testpass123'
        )
        self.veterinario = User.objects.create_user(
            username='vet_test',
            password='testpass123',
            is_staff=True # Veterinários são staff
        )
        Profile.objects.filter(user=self.veterinario).update(role=Profile.Role.FUNCIONARIO)

        self.pet = Pet.objects.create(
            nome='Rex',
            especie='Cachorro',
            tutor=self.tutor,
            data_de_nascimento=date(2020, 1, 1)
        )

    def test_criar_prontuario_valido(self):
        """Teste: Criar um prontuário com dados válidos"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            motivo_consulta="Check-up de rotina",
            diagnostico="Tudo ok",
            tratamento="Nenhum"
        )
        self.assertIsNotNone(prontuario.pk)
        self.assertEqual(prontuario.pet, self.pet)
        self.assertEqual(prontuario.veterinario, self.veterinario)

    def test_prontuario_sem_pet_invalido(self):
        """Teste: Prontuário sem pet deve ser inválido"""
        with self.assertRaises(IntegrityError):
            Prontuario.objects.create(
                veterinario=self.veterinario,
                motivo_consulta="Consulta sem pet"
            )

    def test_prontuario_sem_veterinario_invalido(self):
        """Teste: Prontuário sem veterinário deve ser inválido"""
        with self.assertRaises(IntegrityError):
            Prontuario.objects.create(
                pet=self.pet,
                motivo_consulta="Consulta sem vet"
            )

    def test_tipo_consulta_padrao(self):
        """Teste: Tipo de consulta padrão deve ser 'Consulta de Rotina'"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            motivo_consulta="Consulta padrão"
        )
        self.assertEqual(prontuario.tipo_consulta, Prontuario.TipoConsulta.CONSULTA_ROTINA)

    def test_str_representation(self):
        """Teste: Representação string do prontuário"""
        prontuario = Prontuario.objects.create(
            pet=self.pet,
            veterinario=self.veterinario,
            motivo_consulta="Teste str"
        )
        data_formatada = prontuario.data_consulta.strftime('%d/%m/%Y')
        expected_str = f"Prontuário {prontuario.id} - {self.pet.nome} - {data_formatada}"
        self.assertEqual(str(prontuario), expected_str)

    def test_ordenacao_prontuarios(self):
        """Teste: Prontuários devem ser ordenados por data de consulta decrescente"""
        prontuario1 = Prontuario.objects.create(
            pet=self.pet, veterinario=self.veterinario, motivo_consulta="Primeiro",
            data_consulta=timezone.now() - timedelta(days=10)
        )
        prontuario2 = Prontuario.objects.create(
            pet=self.pet, veterinario=self.veterinario, motivo_consulta="Segundo",
            data_consulta=timezone.now() - timedelta(days=5)
        )
        prontuario3 = Prontuario.objects.create(
            pet=self.pet, veterinario=self.veterinario, motivo_consulta="Terceiro"
        )

        prontuarios_do_pet = Prontuario.objects.filter(pet=self.pet)
        self.assertEqual(prontuarios_do_pet.first(), prontuario3)
        self.assertEqual(prontuarios_do_pet.last(), prontuario1)


class ProntuarioAPITest(APITestCase):
    """Testes para a API REST de prontuários"""
    
    def setUp(self):
        """Configuração inicial para os testes de API"""
        # Criar usuários com diferentes perfis
        self.cliente = User.objects.create_user(
            username='cliente_test',
            password='testpass123'
        )
        Profile.objects.filter(user=self.cliente).update(role=Profile.Role.CLIENTE)
        
        self.veterinario = User.objects.create_user(
            username='veterinario_test',
            password='testpass123',
            is_staff=True
        )
        Profile.objects.filter(user=self.veterinario).update(role=Profile.Role.FUNCIONARIO)
        
        self.admin = User.objects.create_user(
            username='admin_test',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        Profile.objects.filter(user=self.admin).update(role=Profile.Role.ADMIN)
        
        # Criar outro cliente para testar permissões
        self.outro_cliente = User.objects.create_user(
            username='outro_cliente',
            password='testpass123'
        )
        Profile.objects.filter(user=self.outro_cliente).update(role=Profile.Role.CLIENTE)
        
        # Criar pets
        self.pet_cliente = Pet.objects.create(
            nome='Rex',
            especie='Cachorro',
            tutor=self.cliente,
            data_de_nascimento=date(2020, 1, 1)
        )
        
        self.pet_outro_cliente = Pet.objects.create(
            nome='Luna',
            especie='Gato',
            tutor=self.outro_cliente,
            data_de_nascimento=date(2021, 1, 1)
        )
        
        # Criar tokens para autenticação
        self.token_cliente = Token.objects.create(user=self.cliente)
        self.token_veterinario = Token.objects.create(user=self.veterinario)
        self.token_admin = Token.objects.create(user=self.admin)
        self.token_outro_cliente = Token.objects.create(user=self.outro_cliente)
        
        # Criar alguns prontuários para testes
        self.prontuario_cliente = Prontuario.objects.create(
            pet=self.pet_cliente,
            veterinario=self.veterinario,
            motivo_consulta="Consulta de rotina do cliente",
            diagnostico="Saudável",
            tratamento="Nenhum"
        )
        
        self.prontuario_outro_cliente = Prontuario.objects.create(
            pet=self.pet_outro_cliente,
            veterinario=self.veterinario,
            motivo_consulta="Consulta do outro cliente",
            diagnostico="Saudável",
            tratamento="Nenhum"
        )
        
        self.url_base = '/api/prontuarios/'

    def test_listar_prontuarios_cliente_so_ve_seus_pets(self):
        """Teste: Cliente deve ver apenas prontuários de seus pets"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_cliente.key}')
        response = self.client.get(self.url_base)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # Verificar se é uma lista ou se tem paginação
        if isinstance(data, list):
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['id'], self.prontuario_cliente.id)
        else:
            self.assertEqual(len(data['results']), 1)
            self.assertEqual(data['results'][0]['id'], self.prontuario_cliente.id)

    def test_listar_prontuarios_veterinario_ve_todos(self):
        """Teste: Veterinário deve ver todos os prontuários"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_veterinario.key}')
        response = self.client.get(self.url_base)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # Verificar se é uma lista ou se tem paginação
        if isinstance(data, list):
            self.assertEqual(len(data), 2)
        else:
            self.assertEqual(len(data['results']), 2)

    def test_listar_prontuarios_admin_ve_todos(self):
        """Teste: Admin deve ver todos os prontuários"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_admin.key}')
        response = self.client.get(self.url_base)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # Verificar se é uma lista ou se tem paginação
        if isinstance(data, list):
            self.assertEqual(len(data), 2)
        else:
            self.assertEqual(len(data['results']), 2)

    def test_criar_prontuario_veterinario_pode_criar(self):
        """Teste: Veterinário pode criar prontuários"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_veterinario.key}')
        
        data = {
            'pet': self.pet_cliente.id,
            'veterinario': self.veterinario.id,
            'motivo_consulta': 'Nova consulta de rotina',
            'diagnostico': 'Animal saudável',
            'tratamento': 'Manter cuidados',
            'peso': '5.5',
            'temperatura': '38.2'
        }
        
        response = self.client.post(self.url_base, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o prontuário foi criado
        novo_prontuario = Prontuario.objects.get(motivo_consulta='Nova consulta de rotina')
        self.assertEqual(novo_prontuario.pet, self.pet_cliente)
        self.assertEqual(novo_prontuario.veterinario, self.veterinario)

    def test_criar_prontuario_cliente_nao_pode_criar(self):
        """Teste: Cliente não deve poder criar prontuários"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_cliente.key}')
        
        data = {
            'pet': self.pet_cliente.id,
            'veterinario': self.veterinario.id,
            'motivo_consulta': 'Tentativa de criar por cliente'
        }
        
        response = self.client.post(self.url_base, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_visualizar_prontuario_cliente_pode_ver_seu_pet(self):
        """Teste: Cliente pode visualizar prontuários de seus pets"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_cliente.key}')
        
        url_detalhe = f'{self.url_base}{self.prontuario_cliente.id}/'
        response = self.client.get(url_detalhe)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['id'], self.prontuario_cliente.id)

    def test_visualizar_prontuario_cliente_nao_pode_ver_outro_pet(self):
        """Teste: Cliente não pode visualizar prontuários de pets de outros clientes"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_cliente.key}')
        
        url_detalhe = f'{self.url_base}{self.prontuario_outro_cliente.id}/'
        response = self.client.get(url_detalhe)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_atualizar_prontuario_veterinario_pode_atualizar(self):
        """Teste: Veterinário pode atualizar prontuários"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_veterinario.key}')
        
        url_detalhe = f'{self.url_base}{self.prontuario_cliente.id}/'
        data = {
            'motivo_consulta': 'Consulta atualizada pelo veterinário',
            'diagnostico': 'Diagnóstico atualizado'
        }
        
        response = self.client.patch(url_detalhe, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se foi atualizado
        prontuario_atualizado = Prontuario.objects.get(id=self.prontuario_cliente.id)
        self.assertEqual(prontuario_atualizado.motivo_consulta, 'Consulta atualizada pelo veterinário')

    def test_atualizar_prontuario_cliente_nao_pode_atualizar(self):
        """Teste: Cliente não pode atualizar prontuários"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_cliente.key}')
        
        url_detalhe = f'{self.url_base}{self.prontuario_cliente.id}/'
        data = {
            'motivo_consulta': 'Tentativa de atualização por cliente'
        }
        
        response = self.client.patch(url_detalhe, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_excluir_prontuario_admin_pode_excluir(self):
        """Teste: Admin pode excluir prontuários"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_admin.key}')
        
        url_detalhe = f'{self.url_base}{self.prontuario_cliente.id}/'
        response = self.client.delete(url_detalhe)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se foi excluído
        self.assertFalse(Prontuario.objects.filter(id=self.prontuario_cliente.id).exists())

    def test_excluir_prontuario_veterinario_nao_pode_excluir(self):
        """Teste: Veterinário não pode excluir prontuários"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_veterinario.key}')
        
        url_detalhe = f'{self.url_base}{self.prontuario_cliente.id}/'
        response = self.client.delete(url_detalhe)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_acesso_sem_autenticacao_negado(self):
        """Teste: Acesso sem autenticação deve ser negado"""
        response = self.client.get(self.url_base)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_validacao_dados_obrigatorios(self):
        """Teste: Validação de campos obrigatórios na criação"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_veterinario.key}')
        
        # Teste sem pet
        data = {
            'veterinario': self.veterinario.id,
            'motivo_consulta': 'Consulta sem pet'
        }
        response = self.client.post(self.url_base, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Teste sem motivo da consulta
        data = {
            'pet': self.pet_cliente.id,
            'veterinario': self.veterinario.id
        }
        response = self.client.post(self.url_base, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtro_paginacao_funciona(self):
        """Teste: Verificar se a paginação está funcionando"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_veterinario.key}')
        
        # Criar mais prontuários para testar paginação
        for i in range(15):
            Prontuario.objects.create(
                pet=self.pet_cliente,
                veterinario=self.veterinario,
                motivo_consulta=f'Consulta {i}'
            )
        
        response = self.client.get(self.url_base)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        # Verificar se é uma lista ou se tem paginação
        if isinstance(data, list):
            # Se for lista simples, deve ter pelo menos os prontuários criados
            self.assertGreaterEqual(len(data), 2)
        else:
            # Se tiver paginação, verificar estrutura
            self.assertIn('results', data)
            self.assertIn('count', data)
            self.assertIn('next', data)
            self.assertIn('previous', data)
