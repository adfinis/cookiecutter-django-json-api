import importlib
import inspect

import pytest
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from rest_framework.test import APIClient


def register_module(module):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            # name needs to be compatible with
            # `rest_framework.routers.SimpleRouter` naming for easier testing
            base_name = obj._meta.model._meta.object_name.lower()
            register(obj, base_name)


register_module(
    importlib.import_module(
        ".{{cookiecutter.django_app}}.factories", "{{cookiecutter.project_name}}"
    )
)


@pytest.fixture
def admin_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
