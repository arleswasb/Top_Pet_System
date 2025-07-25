# pets/tests_integracao.py

"""
Testes de integração para o módulo pets.
Testa endpoints da API, permissões, autenticação e integração entre components.
"""

from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Pet
from users.models import Profile
from datetime import date, timedelta
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os


class PetAPIPermissionsTestCase(TestCase):
    """Testa as permissões da API de pets para diferentes tipos de usuários"""
    
    def setUp(self):
        # Cria usuários com diferentes perfis
        self.admin = User.objects.create_user(
            username='admin_api',
            password='adminpass',
            is_staff=True,
            is_superuser=True
        )
        # Atualizar perfil criado automaticamente pelo signal
        admin_profile = self.admin.profile
        admin_profile.role = Profile.Role.ADMIN
        admin_profile.save()

        self.funcionario = User.objects.create_user(
            username='func_api',
            password='funcpass'
        )
        # Atualizar perfil criado automaticamente pelo signal
        func_profile = self.funcionario.profile
        func_profile.role = Profile.Role.FUNCIONARIO
        func_profile.save()

        self.tutor = User.objects.create_user(
            username='tutor_api',
            password='tutorpass'
        )
        # Atualizar perfil criado automaticamente pelo signal
        tutor_profile = self.tutor.profile
        tutor_profile.role = Profile.Role.CLIENTE
        tutor_profile.save()

        self.outro_user = User.objects.create_user(
            username='outro_api',
            password='outropass'
        )
        # Atualizar perfil criado automaticamente pelo signal
        outro_profile = self.outro_user.profile
        outro_profile.role = Profile.Role.CLIENTE
        outro_profile.save()

        # Cria pet para teste, associado ao self.tutor
        self.pet = Pet.objects.create(
            nome='Buddy',
            especie='Cachorro',
            tutor=self.tutor
        )

        self.client = APIClient()

    def test_unauthenticated_access_denied(self):
        """Usuário não autenticado não deve ter acesso"""
        response = self.client.get('/api/pets/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_full_access(self):
        """Admin deve ter acesso completo a todos os pets"""
        self.client.force_authenticate(user=self.admin)
        
        # Testa GET list
        response = self.client.get('/api/pets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Testa GET detail
        response = self.client.get(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Testa DELETE
        response = self.client.delete(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Pet.objects.filter(id=self.pet.id).exists())

    def test_owner_full_access_to_own_pet(self):
        """Dono deve ter acesso completo ao próprio pet"""
        self.client.force_authenticate(user=self.tutor)
        
        # Testa GET detail
        response = self.client.get(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Buddy')
        
        # Testa PATCH (atualização parcial) - PUT foi removido
        updated_data = {
            'nome': 'Buddy Atualizado',
            'especie': 'Cachorro'
            # Note: não precisamos enviar tutor no PATCH
        }
        response = self.client.patch(
            f'/api/pets/{self.pet.id}/',
            data=updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.nome, 'Buddy Atualizado')

    def test_funcionario_can_delete_client_pets(self):
        """Funcionário pode deletar pets de clientes"""
        self.client.force_authenticate(user=self.funcionario)
        
        # Testa GET
        response = self.client.get(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Testa DELETE (deve ser permitido para pets de clientes)
        response = self.client.delete(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Pet.objects.filter(id=self.pet.id).exists())

    def test_funcionario_cannot_delete_non_client_pets(self):
        """Funcionário não pode deletar pets de usuários que não são clientes"""
        # Criar um pet para um funcionário (não cliente)
        funcionario2 = User.objects.create_user(
            username='funcionario2',
            password='testpass'
        )
        # Atualizar perfil criado automaticamente pelo signal
        funcionario2_profile = funcionario2.profile
        funcionario2_profile.role = Profile.Role.FUNCIONARIO
        funcionario2_profile.save()
        
        pet_funcionario = Pet.objects.create(
            nome='Pet do Funcionário',
            especie='Gato',
            tutor=funcionario2
        )
        
        self.client.force_authenticate(user=self.funcionario)
    
        
        # Testa DELETE (deve ser negado para pets de não-clientes)
        response = self.client.delete(f'/api/pets/{pet_funcionario.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Pet.objects.filter(id=pet_funcionario.id).exists())

    def test_other_user_no_access(self):
        """Outro usuário não deve ter acesso ao pet de outra pessoa"""
        self.client.force_authenticate(user=self.outro_user)
        
        response = self.client.get(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cliente_only_sees_own_pets(self):
        """Cliente deve ver apenas seus próprios pets"""
        # Cria outro pet para outro usuário
        outro_pet = Pet.objects.create(
            nome='Rex',
            especie='Gato',
            tutor=self.outro_user
        )
        
        self.client.force_authenticate(user=self.tutor)
        response = self.client.get('/api/pets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Corrigir verificação da estrutura de resposta
        if isinstance(response.data, dict) and 'results' in response.data:
            pets_nomes = [pet['nome'] for pet in response.data['results']]
        elif isinstance(response.data, list):
            pets_nomes = [pet['nome'] for pet in response.data]
        else:
            pets_nomes = []
            
        self.assertIn('Buddy', pets_nomes)
        self.assertNotIn('Rex', pets_nomes)

    def test_api_response_structure(self):
        """Testa a estrutura da resposta da API"""
        # Autenticar como tutor para testar a estrutura da resposta
        self.client.force_authenticate(user=self.tutor)
        response = self.client.get('/api/pets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Corrigir verificação da estrutura
        if isinstance(response.data, dict) and 'results' in response.data:
            pet_data = response.data['results'][0] if response.data['results'] else None
        elif isinstance(response.data, list) and response.data:
            pet_data = response.data[0]
        else:
            pet_data = None
            
        if pet_data:
            expected_fields = [
                'id', 'nome', 'especie', 'raca', 'sexo',
                'data_de_nascimento', 'foto', 'observacoes',
                'tutor_detail', 'created_at', 'updated_at'
            ]
            
            for field in expected_fields:
                self.assertIn(field, pet_data)


class PetAPICreateTestCase(TestCase):
    """Testa a criação de pets via API"""
    
    def setUp(self):
        self.cliente = User.objects.create_user(
            username='cliente_create',
            password='testpass'
        )
        # Atualizar perfil criado automaticamente pelo signal
        cliente_profile = self.cliente.profile
        cliente_profile.role = Profile.Role.CLIENTE
        cliente_profile.save()
        
        self.funcionario = User.objects.create_user(
            username='func_create',
            password='testpass'
        )
        # Atualizar perfil criado automaticamente pelo signal
        func_profile = self.funcionario.profile
        func_profile.role = Profile.Role.FUNCIONARIO
        func_profile.save()
        
        self.client = APIClient()

    def test_cliente_create_pet_auto_tutor(self):
        """Cliente cria pet e é automaticamente definido como tutor"""
        self.client.force_authenticate(user=self.cliente)
        
        pet_data = {
            'nome': 'Fluffy',
            'especie': 'Gato',
            'sexo': 'FEMEA'  # Usar string literal em vez de Pet.Gender.FEMALE
        }
        
        response = self.client.post('/api/pets/', data=pet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        pet = Pet.objects.get(id=response.data['id'])
        self.assertEqual(pet.tutor, self.cliente)
        self.assertEqual(pet.nome, 'Fluffy')

    def test_funcionario_create_pet_must_specify_tutor(self):
        """Funcionário deve especificar tutor ao criar pet"""
        self.client.force_authenticate(user=self.funcionario)
        
        # Sem especificar tutor (deve falhar)
        pet_data = {
            'nome': 'Max',
            'especie': 'Cachorro'
        }
        
        response = self.client.post('/api/pets/', data=pet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tutor', response.data)

    def test_funcionario_create_pet_with_tutor(self):
        """Funcionário cria pet especificando tutor"""
        self.client.force_authenticate(user=self.funcionario)
        
        pet_data = {
            'nome': 'Max',
            'especie': 'Cachorro',
            'tutor': self.cliente.id
        }
        
        response = self.client.post('/api/pets/', data=pet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        pet = Pet.objects.get(id=response.data['id'])
        self.assertEqual(pet.tutor, self.cliente)


class PetSerializerIntegrationTestCase(TestCase):
    """Testa a integração do serializer com a API"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='serializer_user',
            password='testpass'
        )
        # Atualizar perfil criado automaticamente pelo signal
        user_profile = self.user.profile
        user_profile.role = Profile.Role.CLIENTE
        user_profile.save()
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_pet_with_all_fields(self):
        """Testa criação de pet com todos os campos preenchidos"""
        pet_data = {
            'nome': 'Comprehensive Pet',
            'especie': 'Cachorro',
            'raca': 'Labrador',
            'sexo': 'MACHO',  # Usar string literal em vez de Pet.Gender.MALE
            'data_de_nascimento': '2020-01-01',
            'observacoes': 'Pet muito dócil'
        }
        
        response = self.client.post('/api/pets/', data=pet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se todos os dados foram salvos corretamente
        pet = Pet.objects.get(id=response.data['id'])
        self.assertEqual(pet.nome, 'Comprehensive Pet')
        self.assertEqual(pet.raca, 'Labrador')
        self.assertEqual(pet.observacoes, 'Pet muito dócil')
        self.assertEqual(str(pet.data_de_nascimento), '2020-01-01')

    def test_image_upload_via_api(self):
        """Testa upload de imagem através da API"""
        # Criar um diretório temporário para o teste
        with tempfile.TemporaryDirectory() as temp_dir:
            media_root = os.path.join(temp_dir, 'test_media')
            
            with override_settings(MEDIA_ROOT=media_root):
                # Cria uma imagem de teste
                image_file = BytesIO()
                image = Image.new('RGB', (100, 100), color='red')
                image.save(image_file, 'JPEG')
                image_file.seek(0)

                uploaded_image = SimpleUploadedFile(
                    "test_image.jpg",
                    image_file.getvalue(),
                    content_type="image/jpeg"
                )
                
                pet_data = {
                    'nome': 'Pet com Foto',
                    'especie': 'Gato',
                    'sexo': 'FEMEA',  # Usar string literal
                    'foto': uploaded_image
                }

                response = self.client.post(
                    '/api/pets/',
                    data=pet_data,
                    format='multipart'
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                
                # Verifica se a imagem foi salva
                pet = Pet.objects.get(id=response.data['id'])
                self.assertTrue(pet.foto.name.endswith('.jpg'))
                self.assertIsNotNone(pet.foto.url)

    def test_read_only_fields_ignored(self):
        """Testa que campos read-only são ignorados na criação"""
        pet_data = {
            'nome': 'Test Pet',
            'especie': 'Cachorro',
            'id': 9999,  # Campo read-only
            'created_at': '2020-01-01T00:00:00Z',  # Campo read-only
            'updated_at': '2020-01-01T00:00:00Z'   # Campo read-only
        }
        
        response = self.client.post('/api/pets/', data=pet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica que os campos read-only não foram definidos com os valores passados
        pet = Pet.objects.get(nome='Test Pet')
        self.assertNotEqual(pet.id, 9999)
        self.assertNotEqual(str(pet.created_at.date()), '2020-01-01')

    def test_serializer_validation_errors(self):
        """Testa erros de validação do serializer"""
        # Dados inválidos (sem nome obrigatório)
        pet_data = {
            'especie': 'Cachorro'
        }
        
        response = self.client.post('/api/pets/', data=pet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nome', response.data)


class PetAPIUpdateTestCase(TestCase):
    """Testa atualizações via API"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='update_user',
            password='testpass'
        )
        # Atualizar perfil criado automaticamente pelo signal
        user_profile = self.user.profile
        user_profile.role = Profile.Role.CLIENTE
        user_profile.save()
        
        self.pet = Pet.objects.create(
            nome='Pet Original',
            especie='Cachorro',
            tutor=self.user
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_partial_update_patch(self):
        """Testa atualização parcial usando PATCH"""
        update_data = {'nome': 'Pet Atualizado'}
        
        response = self.client.patch(
            f'/api/pets/{self.pet.id}/',
            data=update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.nome, 'Pet Atualizado')
        self.assertEqual(self.pet.especie, 'Cachorro')  # Campo não alterado

    def test_partial_update_patch_with_multiple_fields(self):
        """Testa atualização com múltiplos campos usando PATCH (PUT foi removido)"""
        update_data = {
            'nome': 'Pet Completamente Novo',
            'especie': 'Gato'
            # Com PATCH não precisamos enviar tutor
        }
        
        response = self.client.patch(
            f'/api/pets/{self.pet.id}/',
            data=update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.nome, 'Pet Completamente Novo')
        self.assertEqual(self.pet.especie, 'Gato')

    def test_put_method_not_allowed(self):
        """Confirma que PUT foi removido e retorna 405 Method Not Allowed"""
        update_data = {
            'nome': 'Teste PUT',
            'especie': 'Gato'
        }
        
        response = self.client.put(
            f'/api/pets/{self.pet.id}/',
            data=update_data,
            format='json'
        )
        # PUT deve retornar 405 Method Not Allowed - isso confirma nossa implementação
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PetAPIFilteringTestCase(TestCase):
    """Testa filtros e consultas da API"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='filter_user',
            password='testpass'
        )
        # Atualizar perfil criado automaticamente pelo signal
        user_profile = self.user.profile
        user_profile.role = Profile.Role.CLIENTE
        user_profile.save()
        
        # Cria pets de teste
        Pet.objects.create(nome='Rex', especie='Cachorro', tutor=self.user)
        Pet.objects.create(nome='Miau', especie='Gato', tutor=self.user)
        Pet.objects.create(nome='Bolt', especie='Cachorro', tutor=self.user)
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_all_user_pets(self):
        """Testa listagem de todos os pets do usuário"""
        response = self.client.get('/api/pets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Verifica se todos os pets estão na resposta
        nomes = [pet['nome'] for pet in response.data]
        self.assertIn('Rex', nomes)
        self.assertIn('Miau', nomes)
        self.assertIn('Bolt', nomes)

    def test_api_response_structure(self):
        """Testa a estrutura da resposta da API"""
        response = self.client.get('/api/pets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Corrigir verificação da estrutura
        if isinstance(response.data, dict) and 'results' in response.data:
            pet_data = response.data['results'][0] if response.data['results'] else None
        elif isinstance(response.data, list) and response.data:
            pet_data = response.data[0]
        else:
            pet_data = None
            
        if pet_data:
            expected_fields = [
                'id', 'nome', 'especie', 'raca', 'sexo',
                'data_de_nascimento', 'foto', 'observacoes',
                'tutor_detail', 'created_at', 'updated_at'
            ]
            
            for field in expected_fields:
                self.assertIn(field, pet_data)

    def test_api_response_idade_formatada(self):
        """Testa se a API retorna a idade formatada como um texto."""
        # Cria um pet com 2 meses e alguns dias de idade
        data_nascimento = date.today() - timedelta(days=70) # Aprox. 2 meses e 10 dias
        pet_jovem = Pet.objects.create(
            nome='Filhote',
            especie='Gato',
            tutor=self.user,
            data_de_nascimento=data_nascimento
        )

        response = self.client.get(f'/api/pets/{pet_jovem.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica se o campo 'idade' contém um texto esperado
        idade_api = response.data['idade']
        self.assertIn('2 meses', idade_api) # Verifica se a string contém "2 meses"
        self.assertIsInstance(idade_api, str) # Confirma que o tipo é string