import uuid

from django.db import models


class UUIDModel(models.Model):
    """
    Models which use uuid as primary key.

    Defined as {{cookiecutter.project_name}} default
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
