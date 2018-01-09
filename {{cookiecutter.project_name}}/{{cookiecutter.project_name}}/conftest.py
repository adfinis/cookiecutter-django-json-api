import pytest
from rest_framework_jwt import test


@pytest.fixture
def client():
    return test.APIJWTClient()


@pytest.fixture
def admin_client(db, admin_user, client):
    client.login(username=admin_user.username, password='password')
    return client
