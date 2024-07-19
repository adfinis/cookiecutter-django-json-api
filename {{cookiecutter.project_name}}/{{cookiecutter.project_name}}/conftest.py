import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .{{cookiecutter.django_app}} import factories

register(factories.UserFactory)


@pytest.fixture
def admin_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
