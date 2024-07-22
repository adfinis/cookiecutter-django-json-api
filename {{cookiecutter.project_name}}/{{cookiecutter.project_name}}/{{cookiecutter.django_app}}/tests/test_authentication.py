import hashlib
import json
from uuid import uuid4

import pytest
from django.core.cache import cache
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from requests.exceptions import HTTPError
from rest_framework import exceptions, status
from rest_framework.exceptions import AuthenticationFailed

from {{cookiecutter.project_name}}.{{cookiecutter.django_app}}.models import UserProfile


@pytest.mark.parametrize(
    "authentication_header,authenticated,error",
    [
        ("", False, False),
        ("Bearer", False, True),
        ("Bearer Too many params", False, True),
        ("Basic Auth", False, True),
        ("Bearer Token", True, False),
    ],
)
def test_authentication(
    db,
    rf,
    authentication_header,
    authenticated,
    error,
    requests_mock,
    settings,
    claims,
):
    assert UserProfile.objects.count() == 0

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION=authentication_header)

    try:
        result = OIDCAuthentication().authenticate(request)
    except exceptions.AuthenticationFailed:
        assert error
    else:
        if authenticated:
            user, auth = result
            assert user.is_authenticated
            assert auth == authentication_header.split(" ")[1]
            assert (
                cache.get(f"auth.userinfo.{hashlib.sha256(b'Token').hexdigest()}")
                == claims
            )
            assert UserProfile.objects.count() == 1
        else:
            assert result is None


@pytest.mark.parametrize("email_claim", ["foo@example.com", "bar@example.com"])
@pytest.mark.parametrize("first_name_claim", ["Winston", "Hagbard"])
@pytest.mark.parametrize("last_name_claim", ["Smith", "Celine"])
def test_authentication_profile_create(
    db,
    rf,
    requests_mock,
    settings,
    get_claims,
    email_claim,
    first_name_claim,
    last_name_claim,
):
    idp_id = str(uuid4())
    claims = get_claims(
        id_claim=idp_id,
        email_claim=email_claim,
        first_name_claim=first_name_claim,
        last_name_claim=last_name_claim,
    )
    assert UserProfile.objects.count() == 0

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")

    result = OIDCAuthentication().authenticate(request)
    user, auth = result
    assert user.is_authenticated
    assert cache.get(f"auth.userinfo.{hashlib.sha256(b'Token').hexdigest()}") == claims
    assert UserProfile.objects.count() == 1

    profile = UserProfile.objects.get(idp_id=idp_id)

    assert [
        profile.email,
        profile.first_name,
        profile.last_name,
    ] == [
        email_claim,
        first_name_claim,
        last_name_claim,
    ]


@pytest.mark.parametrize(
    "user_profile__email,user_profile__first_name,user_profile__last_name",
    [
        (
            "foo@example.com",
            "Winston",
            "Smith",
        )
    ],
)
@pytest.mark.parametrize("email_claim", ["bar@example.com"])
@pytest.mark.parametrize("first_name_claim", ["Hagbard"])
@pytest.mark.parametrize("last_name_claim", ["Celine"])
def test_authentication_profile_update_existing_profile(
    db,
    rf,
    requests_mock,
    settings,
    get_claims,
    user_profile,
    email_claim,
    first_name_claim,
    last_name_claim,
):
    claims = get_claims(
        id_claim=str(user_profile.idp_id),
        email_claim=email_claim,
        first_name_claim=first_name_claim,
        last_name_claim=last_name_claim,
    )
    assert UserProfile.objects.count() == 1

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")

    result = OIDCAuthentication().authenticate(request)
    assert result[0].is_authenticated
    assert UserProfile.objects.count() == 1

    user_profile.refresh_from_db()

    # only the email should be updated
    assert user_profile.email == email_claim
    assert user_profile.first_name == "Winston"
    assert user_profile.last_name == "Smith"


def test_authentication_multiple_existing_profile(
    db,
    rf,
    requests_mock,
    settings,
    user_profile_factory,
    get_claims,
    caplog,
):
    user_profile = user_profile_factory(idp_id="matching_id")
    user_profile_factory(email="match@example.com")
    claims = get_claims(
        id_claim="matching_id",
        groups_claim=[],
        email_claim="match@example.com",
    )

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    assert UserProfile.objects.count() == 2

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")

    result = OIDCAuthentication().authenticate(request)

    user, auth = result
    assert user.is_authenticated
    assert user.profile == user_profile
    assert UserProfile.objects.count() == 2
    assert caplog.records[0].msg == (
        "Found one UserProfile with same idp_id and one with same email. "
        "Matching on idp_id."
    )


def test_authentication_idp_502(
    db,
    rf,
    requests_mock,
    settings,
):
    requests_mock.get(
        settings.OIDC_OP_USER_ENDPOINT,
        status_code=status.HTTP_502_BAD_GATEWAY,
    )

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(HTTPError):
        OIDCAuthentication().authenticate(request)


def test_authentication_idp_missing_claim(
    db,
    rf,
    requests_mock,
    settings,
    claims,
):
    settings.OIDC_ID_CLAIM = "missing"
    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(AuthenticationFailed):
        OIDCAuthentication().authenticate(request)
