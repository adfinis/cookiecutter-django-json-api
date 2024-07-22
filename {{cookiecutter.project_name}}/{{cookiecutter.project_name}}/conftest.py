from functools import partial

import pytest
from django.core.cache import cache
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .{{cookiecutter.django_app}} import factories
from .{{cookiecutter.django_app}}.models import OIDCUser

register(factories.UserProfileFactory)


def _get_claims(
    settings,
    id_claim="00000000-0000-0000-0000-000000000000",
    groups_claim=None,
    email_claim="test@example.com",
    first_name_claim=None,
    last_name_claim=None,
):
    groups_claim = groups_claim if groups_claim else []
    return {
        settings.OIDC_ID_CLAIM: id_claim,
        settings.OIDC_GROUPS_CLAIM: groups_claim,
        settings.OIDC_EMAIL_CLAIM: email_claim,
        settings.OIDC_FIRST_NAME_CLAIM: first_name_claim,
        settings.OIDC_LAST_NAME_CLAIM: last_name_claim,
    }


@pytest.fixture
def get_claims(settings):
    return partial(_get_claims, settings)


@pytest.fixture
def claims(settings):
    return _get_claims(settings)


@pytest.fixture
def admin_user(settings, get_claims):
    return OIDCUser(
        "sometoken",
        get_claims(
            id_claim="admin",
            groups_claim=[settings.ADMIN_GROUP],
            email_claim="admin@example.com",
        ),
    )


@pytest.fixture
def user(get_claims):
    return OIDCUser(
        "sometoken",
        get_claims(id_claim="user", groups_claim=[], email_claim="user@example.com"),
    )


@pytest.fixture(params=["admin"])
def client(db, user, admin_user, request):
    usermap = {"user": user, "admin": admin_user}
    client = APIClient()
    user = usermap[request.param]
    client.force_authenticate(user=user)
    client.user = user
    return client


@pytest.fixture(autouse=True)
def _autoclear_cache():
    cache.clear()
