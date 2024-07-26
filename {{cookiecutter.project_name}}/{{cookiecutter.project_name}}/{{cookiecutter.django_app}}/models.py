import logging

from django.conf import settings
from django.db import IntegrityError, models, transaction
from django.db.models import Q

from ..models import UUIDModel

logger = logging.getLogger(__name__)


class UserProfile(UUIDModel):
    idp_id = models.CharField(
        max_length=255, unique=True, null=True, blank=False, db_index=True
    )
    email = models.EmailField(unique=True, null=True, blank=True, db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ("last_name", "first_name", "email")


class BaseOIDCUser:  # pragma: no cover
    def __init__(self):
        self.email = None
        self.groups = []
        self.group = None
        self.token = None
        self.claims = {}
        self.is_authenticated = False

    def __str__(self):
        raise NotImplementedError

    @property
    def is_admin(self):
        return settings.ADMIN_GROUP in self.groups


class OIDCUser(BaseOIDCUser):
    def __init__(self, token: str, claims: dict):
        super().__init__()

        self.claims = claims
        self.id = self.claims[settings.OIDC_ID_CLAIM]
        self.email = self.claims.get(settings.OIDC_EMAIL_CLAIM)
        self.first_name = self.claims.get(settings.OIDC_FIRST_NAME_CLAIM)
        self.last_name = self.claims.get(settings.OIDC_LAST_NAME_CLAIM)

        self.groups = self.claims.get(settings.OIDC_GROUPS_CLAIM, [])
        self.group = self.groups[0] if self.groups else None
        self.token = token
        self.is_authenticated = True
        self.profile = self._update_or_create_profile()

    def _update_or_create_profile(self):
        """
        Update or create UserProfile.

        Analogous to QuerySet.get_or_create(), in order to handle race conditions as
        gracefully as possible.
        """
        try:
            profile = UserProfile.objects.get(
                Q(idp_id=self.id) | Q(email__iexact=self.email),
            )
            # we only want to save if necessary
            if profile.idp_id != self.id or profile.email != self.email:
                profile.idp_id = self.id
                profile.email = self.email
                profile.save()
        except UserProfile.MultipleObjectsReturned:
            # TODO: trigger notification for staff members or admins
            logger.warning(
                "Found one UserProfile with same idp_id and one with same email. "
                "Matching on idp_id.",
            )
            return UserProfile.objects.get(idp_id=self.id)
        except UserProfile.DoesNotExist:
            try:
                with transaction.atomic(using=UserProfile.objects.db):
                    return UserProfile.objects.create(
                        idp_id=self.id,
                        email=self.email,
                        first_name=self.first_name,
                        last_name=self.last_name,
                    )
            except IntegrityError:  # pragma: no cover
                # race condition happened
                try:
                    return UserProfile.objects.get(idp_id=self.id)
                except UserProfile.DoesNotExist:
                    pass
                raise
        else:
            return profile

    def __str__(self):
        return f"{self.email} - {self.id}"
