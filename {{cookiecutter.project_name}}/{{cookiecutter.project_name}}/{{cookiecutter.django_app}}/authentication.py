import functools
import hashlib
import warnings
from typing import NamedTuple

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import SuspiciousOperation
from django.utils.encoding import force_bytes
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from urllib3.exceptions import InsecureRequestWarning

from .models import OIDCUser


class OIDCAuthenticationBackend(OIDCAuthenticationBackend):
    class _HistoricalRequestUser(NamedTuple):
        id: str

    def verify_claims(self, claims):
        # claims for human users
        claims_to_verify = [
            settings.OIDC_ID_CLAIM,
            settings.OIDC_EMAIL_CLAIM,
        ]

        # # claims for application clients
        # if claims.get(settings.OIDC_CLIENT_GRANT_USERNAME_CLAIM) in [
        #     settings.OIDC_RP_CLIENT_USERNAME,
        #     settings.OIDC_MONITORING_CLIENT_USERNAME,
        # ]:
        #     claims_to_verify = [
        #         settings.OIDC_ID_CLAIM,
        #     ]

        for claim in claims_to_verify:
            if claim not in claims:
                msg = f'Couldn\'t find "{claim}" claim'
                raise SuspiciousOperation(msg)

    def get_or_create_user(self, access_token, id_token, payload):
        """Verify claims and return user, otherwise raise an Exception."""

        claims = self.cached_request(access_token, id_token, payload)

        self.verify_claims(claims)

        return OIDCUser(access_token, claims)

    def cached_request(self, access_token, id_token, payload):
        token_hash = hashlib.sha256(force_bytes(access_token)).hexdigest()

        func = functools.partial(self.get_userinfo, access_token, id_token, payload)

        with warnings.catch_warnings():
            if settings.DEBUG:  # pragma: no cover
                warnings.simplefilter("ignore", InsecureRequestWarning)
            return cache.get_or_set(
                f"auth.userinfo.{token_hash}",
                func,
                timeout=settings.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
            )
