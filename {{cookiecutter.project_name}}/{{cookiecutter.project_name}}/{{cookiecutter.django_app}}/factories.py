from factory import Faker
from factory.django import DjangoModelFactory

from . import models


class UserProfileFactory(DjangoModelFactory):
    idp_id = Faker("uuid4")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    class Meta:
        model = models.UserProfile
