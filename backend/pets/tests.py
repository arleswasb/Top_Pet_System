# pets/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Pet
from users.models import Profile # Importar Profile para referenciar Profile.Role
from datetime import date # Para usar objetos date
from PIL import Image # Pip install Pillow - Necessário para criar imagens de teste
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

class PetModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tutor_model', # Nome de usuário único para este teste
            password='testpass123'
        )
        # O Profile é criado automaticamente pelo signal.
        # Apenas atualizamos a role, se necessário.
        self.user.profile.role = Profile.Role.CLIENTE
        self.user.profile.save()
        
        self.pet_data = {
            'nome': 'Rex',
            'especie': 'Cachorro',
            'tutor': self.user
        }

    def test_pet_creation(self):
        """Testa a criação básica de um pet"""
        pet = Pet.objects.create(**self.pet_data)
        self.assertEqual(pet.nome, 'Rex')
        self.assertEqual(pet.tutor.username, 'tutor_model')
        self.assertIsNone(pet.raca) # Campo opcional

class PetPermissionsTestCase(TestCase):
    def setUp(self):
        # Cria usuários com diferentes perfis. Nomes de usuário únicos.
        self.admin = User.objects.create_user(
            username='admin_perm',
            password='adminpass',
            is_staff=True,
            is_superuser=True
        )
        self.admin.profile.role = Profile.Role.ADMIN
        self.admin.profile.save()

        self.funcionario = User.objects.create_user(
            username='func_perm',
            password='funcpass'
        )
        self.funcionario.profile.role = Profile.Role.FUNCIONARIO
        self.funcionario.profile.save()

        self.tutor = User.objects.create_user(
            username='tutor_perm',
            password='tutorpass'
        )
        self.tutor.profile.role = Profile.Role.CLIENTE
        self.tutor.profile.save()

        self.outro_user = User.objects.create_user(
            username='outro_perm',
            password='outropass'
        )
        self.outro_user.profile.role = Profile.Role.CLIENTE
        self.outro_user.profile.save()

        # Cria pet para teste, associado ao self.tutor
        self.pet = Pet.objects.create(
            nome='Buddy',
            especie='Cachorro',
            tutor=self.tutor
        )

        self.client = APIClient()

    def test_admin_full_access(self):
        """Admin deve ter acesso completo"""
        self.client.force_authenticate(user=self.admin)
        
        # Testa GET
        response = self.client.get(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Testa DELETE
        response = self.client.delete(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verifica se o pet realmente foi deletado
        self.assertFalse(Pet.objects.filter(id=self.pet.id).exists())


    def test_owner_full_access(self):
        """Dono deve ter acesso completo"""
        self.client.force_authenticate(user=self.tutor)
        
        # Dados para atualização (incluindo campo obrigatório 'tutor')
        updated_data = {
            'nome': 'Novo Nome Pet', # Use um nome diferente para evitar confusão com outros testes
            'especie': 'Gato',
            'tutor': self.tutor.id # Tutor é obrigatório no modelo
        }
        response = self.client.put(
            f'/api/pets/{self.pet.id}/',
            data=updated_data, # Use 'data' para dicionários
            format='json' # Especifique o formato JSON
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.pet.refresh_from_db() # Recarrega o objeto do banco para verificar a mudança
        self.assertEqual(self.pet.nome, 'Novo Nome Pet')
        self.assertEqual(self.pet.especie, 'Gato')

    def test_funcionario_no_delete(self):
        """Funcionário não pode deletar"""
        self.client.force_authenticate(user=self.funcionario)
        
        response = self.client.delete(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Verifica que o pet NÃO foi deletado
        self.assertTrue(Pet.objects.filter(id=self.pet.id).exists())


    def test_other_user_access(self):
        """Outro usuário não deve ter acesso (receber 404 se não puder ver o pet)"""
        self.client.force_authenticate(user=self.outro_user)
        
        response = self.client.get(f'/api/pets/{self.pet.id}/')
        # A API deve retornar 404 Not Found se o recurso não existe ou não está visível para o usuário.
        # Se a permissão for baseada na visibilidade do queryset, 404 é o esperado.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 


class PetSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='serializertest_user', # Nome de usuário único
            password='testpass'
        )
        self.user.profile.role = Profile.Role.CLIENTE
        self.user.profile.save()
        
        # Dados válidos completos, incluindo todos os campos obrigatórios do modelo Pet
        self.valid_data = {
            'nome': 'Fluffy',
            'especie': 'Gato',
            'sexo': Pet.Gender.FEMALE, # Campo sexo é obrigatório (com default, mas bom testar)
            'data_de_nascimento': '2023-01-01', # Adicionando data para testes de idade e validadores
            'tutor': self.user.id # Campo ForeignKey deve ser o ID do tutor
        }

    def test_valid_serializer(self):
        """Testa serializer com dados válidos"""
        from .serializers import PetSerializer # Importação aqui para evitar circular references se serializer precisar do models
        serializer = PetSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors) # Passa erros para depuração
        
        pet = serializer.save()
        self.assertEqual(pet.nome, 'Fluffy')
        self.assertEqual(pet.tutor.id, self.user.id)
        self.assertEqual(pet.especie, 'Gato')
        self.assertEqual(pet.sexo, Pet.Gender.FEMALE)

    def test_missing_required_field(self):
        """Testa serializer com campo obrigatório faltando"""
        from .serializers import PetSerializer
        invalid_data = self.valid_data.copy()
        del invalid_data['nome'] # Remove um campo obrigatório
        
        serializer = PetSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nome', serializer.errors)

    def test_read_only_fields(self):
        """Testa que campos read_only (como 'id', 'created_at') não são aceitos na criação"""
        from .serializers import PetSerializer
        data_with_readonly = self.valid_data.copy()
        data_with_readonly['id'] = 9999 # Tentando definir um ID (que é read-only)
        data_with_readonly['created_at'] = '2020-01-01T00:00:00Z' # Tentando definir created_at

        serializer = PetSerializer(data=data_with_readonly)
        self.assertTrue(serializer.is_valid(), serializer.errors) # Deve ser válido, campos read-only são ignorados
        
        pet = serializer.save()
        self.assertNotEqual(pet.id, 9999) # O ID deve ser gerado pelo banco, não o que passamos
        # created_at é auto_now_add, então será a data de criação real, não a passada
        self.assertNotEqual(str(pet.created_at.date()), '2020-01-01') 

    def test_image_upload(self):
        """Testa o upload de imagem através da API"""
        # Cria uma imagem de teste em memória
        image_file = BytesIO()
        image = Image.new('RGB', (100, 100), color = 'red')
        image.save(image_file, 'jpeg')
        image_file.seek(0)

        # Envolve a imagem em SimpleUploadedFile
        uploaded_image = SimpleUploadedFile(
            "test_image.jpg",
            image_file.getvalue(),
            content_type="image/jpeg"
        )
        
        # Dados para criar o pet com a imagem (incluindo todos os obrigatórios)
        data = {
            'nome': 'PetComFoto',
            'especie': 'Cachorro',
            'sexo': Pet.Gender.MALE,
            'data_de_nascimento': '2022-06-15',
            'foto': uploaded_image,
            'tutor': self.user.id # Tutor é obrigatório
        }

        self.client = APIClient()
        self.client.force_authenticate(user=self.user) # Autentica o cliente para a requisição
        
        response = self.client.post(
            '/api/pets/',
            data=data,
            format='multipart' # Crucial para upload de arquivos
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertIn('foto', response.json()) # Verifica se a URL da foto está na resposta
        
        # Opcional: verifica se o arquivo foi salvo no modelo
        pet = Pet.objects.get(id=response.json()['id'])
        self.assertTrue(pet.foto.name.endswith('.jpg'))
        self.assertIsNotNone(pet.foto.url)


    def test_age_calculation(self):
        """Testa o cálculo da idade do pet"""
        pet = Pet.objects.create(
            nome='PetVelho',
            especie='Cachorro',
            data_de_nascimento=date(2010, 1, 1), 
            tutor=self.user
        )
        
        idade_calculada = pet.idade
        
        # A idade em 24/06/2025 para 2010-01-01 é 15 anos.
        # Ajuste a asserção conforme a lógica da sua propriedade `idade` e a data atual.
        # Sua propriedade idade calcula anos inteiros, então em 2025-06-24, seria 15.
        self.assertIsInstance(idade_calculada, int)
        self.assertEqual(idade_calculada, 15) # Assumindo o cálculo de idade é exato