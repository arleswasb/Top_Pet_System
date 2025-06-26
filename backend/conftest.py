import django
import os
import pytest
from django.conf import settings
from django.test.utils import get_runner

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
    django.setup()