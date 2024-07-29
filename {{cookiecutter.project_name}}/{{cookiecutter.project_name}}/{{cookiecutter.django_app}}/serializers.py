from rest_framework_json_api import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = (
            "idp_id",
            "first_name",
            "last_name",
            "email",
        )
