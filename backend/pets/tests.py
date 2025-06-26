# pets/tests.py

from datetime import date
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from users.models import Profile

from .models import Pet


class PetModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tutor_model",
            password="testpass123",
        )
        self.user.profile.role = Profile.Role.CLIENTE
        self.user.profile.save()

        self.pet_data = {
            "nome": "Rex",
            "especie": "Cachorro",
            "tutor": self.user,
        }

    def test_pet_creation(self):
        """Test basic pet creation"""
        pet = Pet.objects.create(**self.pet_data)
        self.assertEqual(pet.nome, "Rex")
        self.assertEqual(pet.tutor.username, "tutor_model")
        self.assertIsNone(pet.raca)


class PetPermissionsTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin_perm",
            password="adminpass",
            is_staff=True,
            is_superuser=True,
        )
        self.admin.profile.role = Profile.Role.ADMIN
        self.admin.profile.save()

        self.funcionario = User.objects.create_user(
            username="func_perm", password="funcpass"
        )
        self.funcionario.profile.role = Profile.Role.FUNCIONARIO
        self.funcionario.profile.save()

        self.tutor = User.objects.create_user(
            username="tutor_perm", password="tutorpass"
        )
        self.tutor.profile.role = Profile.Role.CLIENTE
        self.tutor.profile.save()

        self.outro_user = User.objects.create_user(
            username="outro_perm", password="outropass"
        )
        self.outro_user.profile.role = Profile.Role.CLIENTE
        self.outro_user.profile.save()

        self.pet = Pet.objects.create(
            nome="Buddy", especie="Cachorro", tutor=self.tutor
        )

        self.client = APIClient()

    def test_admin_full_access(self):
        """Admin should have full access"""
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(f"/api/pets/{self.pet.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(f"/api/pets/{self.pet.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Pet.objects.filter(id=self.pet.id).exists())

    def test_owner_full_access(self):
        """Owner should have full access"""
        self.client.force_authenticate(user=self.tutor)

        updated_data = {
            "nome": "Novo Nome Pet",
            "especie": "Gato",
            "tutor": self.tutor.id,
        }
        response = self.client.put(
            f"/api/pets/{self.pet.id}/",
            data=updated_data,
            format="json",
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.json()
        )
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.nome, "Novo Nome Pet")
        self.assertEqual(self.pet.especie, "Gato")

    def test_funcionario_no_delete(self):
        """Employee cannot delete"""
        self.client.force_authenticate(user=self.funcionario)

        response = self.client.delete(f"/api/pets/{self.pet.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Pet.objects.filter(id=self.pet.id).exists())

    def test_other_user_access(self):
        """Other user should not have access"""
        self.client.force_authenticate(user=self.outro_user)

        response = self.client.get(f"/api/pets/{self.pet.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PetSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="serializertest_user",
            password="testpass",
        )
        self.user.profile.role = Profile.Role.CLIENTE
        self.user.profile.save()

        self.valid_data = {
            "nome": "Fluffy",
            "especie": "Gato",
            "sexo": Pet.Gender.FEMALE,
            "data_de_nascimento": "2023-01-01",
            "tutor": self.user.id,
        }

    def test_valid_serializer(self):
        """Test serializer with valid data"""
        from .serializers import PetSerializer

        serializer = PetSerializer(data=self.valid_data)
        self.assertTrue(
            serializer.is_valid(), serializer.errors
        )

        pet = serializer.save()
        self.assertEqual(pet.nome, "Fluffy")
        self.assertEqual(pet.tutor.id, self.user.id)
        self.assertEqual(pet.especie, "Gato")
        self.assertEqual(pet.sexo, Pet.Gender.FEMALE)

    def test_missing_required_field(self):
        """Test serializer with missing required field"""
        from .serializers import PetSerializer

        invalid_data = self.valid_data.copy()
        del invalid_data["nome"]

        serializer = PetSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("nome", serializer.errors)

    def test_read_only_fields(self):
        """Test that read-only fields are not accepted on creation"""
        from .serializers import PetSerializer

        data_with_readonly = self.valid_data.copy()
        data_with_readonly["id"] = 9999
        data_with_readonly[
            "created_at"
        ] = "2020-01-01T00:00:00Z"

        serializer = PetSerializer(data=data_with_readonly)
        self.assertTrue(
            serializer.is_valid(), serializer.errors
        )

        pet = serializer.save()
        self.assertNotEqual(pet.id, 9999)
        self.assertNotEqual(str(pet.created_at.date()), "2020-01-01")

    def test_image_upload(self):
        """Test image upload via API"""
        image_file = BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(image_file, "jpeg")
        image_file.seek(0)

        uploaded_image = SimpleUploadedFile(
            "test_image.jpg",
            image_file.getvalue(),
            content_type="image/jpeg",
        )

        data = {
            "nome": "PetComFoto",
            "especie": "Cachorro",
            "sexo": Pet.Gender.MALE,
            "data_de_nascimento": "2022-06-15",
            "foto": uploaded_image,
            "tutor": self.user.id,
        }

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/pets/", data=data, format="multipart"
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.json()
        )
        self.assertIn("foto", response.json())

        pet = Pet.objects.get(id=response.json()["id"])
        self.assertTrue(pet.foto.name.endswith(".jpg"))
        self.assertIsNotNone(pet.foto.url)

    def test_age_calculation(self):
        """Test pet age calculation"""
        pet = Pet.objects.create(
            nome="PetVelho",
            especie="Cachorro",
            data_de_nascimento=date(2010, 1, 1),
            tutor=self.user,
        )

        idade_calculada = pet.idade
        self.assertIsInstance(idade_calculada, int)
        self.assertEqual(idade_calculada, 15)