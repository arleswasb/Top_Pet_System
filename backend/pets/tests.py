from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Pet
from users.models import Profile

class PetModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tutor', 
            password='testpass123'
        )
        Profile.objects.create(user=self.user, role=Profile.Role.CLIENTE)
        
        self.pet_data = {
            'nome': 'Rex',
            'especie': 'Cachorro',
            'tutor': self.user
        }

    def test_pet_creation(self):
        """Testa a criação básica de um pet"""
        pet = Pet.objects.create(**self.pet_data)
        self.assertEqual(pet.nome, 'Rex')
        self.assertEqual(pet.tutor.username, 'tutor')
        self.assertIsNone(pet.raca)  # Campo opcional

class PetPermissionsTestCase(TestCase):
    def setUp(self):
        # Cria usuários com diferentes perfis
        self.admin = User.objects.create_user(
            username='admin', 
            password='adminpass'
        )
        Profile.objects.create(
            user=self.admin, 
            role=Profile.Role.ADMIN
        )

        self.funcionario = User.objects.create_user(
            username='func', 
            password='funcpass'
        )
        Profile.objects.create(
            user=self.funcionario, 
            role=Profile.Role.FUNCIONARIO
        )

        self.tutor = User.objects.create_user(
            username='tutor', 
            password='tutorpass'
        )
        Profile.objects.create(
            user=self.tutor, 
            role=Profile.Role.CLIENTE
        )

        self.outro_user = User.objects.create_user(
            username='outro', 
            password='outropass'
        )
        Profile.objects.create(
            user=self.outro_user, 
            role=Profile.Role.CLIENTE
        )

        # Cria pet para teste
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

    def test_owner_full_access(self):
        """Dono deve ter acesso completo"""
        self.client.force_authenticate(user=self.tutor)
        
        response = self.client.put(
            f'/api/pets/{self.pet.id}/',
            {'nome': 'Novo Nome', 'especie': 'Gato'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_funcionario_no_delete(self):
        """Funcionário não pode deletar"""
        self.client.force_authenticate(user=self.funcionario)
        
        response = self.client.delete(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_access(self):
        """Outro usuário não deve ter acesso"""
        self.client.force_authenticate(user=self.outro_user)
        
        response = self.client.get(f'/api/pets/{self.pet.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PetSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='serializertest',
            password='testpass'
        )
        Profile.objects.create(user=self.user, role=Profile.Role.CLIENTE)
        
        self.valid_data = {
            'nome': 'Fluffy',
            'especie': 'Gato',
            'tutor_id': self.user.id
        }

    def test_valid_serializer(self):
        """Testa serializer com dados válidos"""
        from .serializers import PetSerializer
        serializer = PetSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        pet = serializer.save()
        self.assertEqual(pet.nome, 'Fluffy')
        self.assertEqual(pet.tutor.id, self.user.id)

    def test_missing_required_field(self):
        """Testa serializer com campo obrigatório faltando"""
        from .serializers import PetSerializer
        invalid_data = self.valid_data.copy()
        del invalid_data['nome']
        
        serializer = PetSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nome', serializer.errors)

    def test_read_only_fields(self):
        """Testa que campos read_only não são aceitos na criação"""
        from .serializers import PetSerializer
        data = self.valid_data.copy()
        data['tutor'] = {'username': 'should_not_accept'}
        
        serializer = PetSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # Campo tutor é ignorado na escrita

    # Testar upload de imagem
    def test_image_upload(self):
        with open('test_image.jpg', 'rb') as img:
            response = self.client.post(
                '/api/pets/',
                {'nome': 'PetComFoto', 'especie': 'Cachorro', 'foto': img},
                format='multipart'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testar cálculo de idade
    def test_age_calculation(self):
        pet = Pet.objects.create(
            nome='PetVelho',
            especie='Cachorro',
            data_de_nascimento='2010-01-01'
        )
        self.assertGreaterEqual(pet.idade, 10)