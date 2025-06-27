# users/tests_pytest.py
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils.crypto import get_random_string
from .models import Profile


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_factory(db):
    def create_user(username, role, is_active=True):
        from django.db import transaction
        # Ensure unique usernames to prevent IntegrityError during test runs
        unique_username = f"{username}_{get_random_string(6)}"
        
        with transaction.atomic():
            user = User.objects.create_user(
                username=unique_username,
                password="password123",
                is_active=is_active
            )
            # The signal creates the profile with a default role.
            # We must fetch the profile and explicitly set the desired role for the test.
            profile = Profile.objects.get(user=user)
            profile.role = role
            profile.save()
        
        # Refresh to ensure we have the latest data
        user.refresh_from_db()
        return user

    return create_user


@pytest.mark.django_db
class TestUserAdminViewSet:
    def test_admin_can_list_users(self, api_client, user_factory):
        admin_user = user_factory("admin", Profile.Role.ADMIN)
        user_factory("client", Profile.Role.CLIENTE)  # create another user
        api_client.force_authenticate(user=admin_user)
        url = reverse("user-admin-list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 2

    def test_non_admin_cannot_list_users(self, api_client, user_factory):
        regular_user = user_factory("client", Profile.Role.CLIENTE)
        api_client.force_authenticate(user=regular_user)
        url = reverse("user-admin-list")
        response = api_client.get(url)
        assert response.status_code == 403

    def test_admin_can_toggle_user_active_status(self, api_client, user_factory):
        admin_user = user_factory("admin", Profile.Role.ADMIN)
        regular_user = user_factory(
            "client_to_toggle", Profile.Role.CLIENTE, is_active=True
        )
        api_client.force_authenticate(user=admin_user)
        assert regular_user.is_active is True
        url = reverse("user-admin-toggle-active", kwargs={"pk": regular_user.pk})
        response = api_client.post(url)
        assert response.status_code == 200
        regular_user.refresh_from_db()
        assert regular_user.is_active is False
        # Toggle back
        response = api_client.post(url)
        assert response.status_code == 200
        regular_user.refresh_from_db()
        assert regular_user.is_active is True

    def test_non_admin_cannot_toggle_status(self, api_client, user_factory):
        user_1 = user_factory("client1", Profile.Role.CLIENTE)
        user_2 = user_factory("client2", Profile.Role.CLIENTE)
        api_client.force_authenticate(user=user_1)
        url = reverse("user-admin-toggle-active", kwargs={"pk": user_2.pk})
        response = api_client.post(url)
        assert response.status_code == 403
