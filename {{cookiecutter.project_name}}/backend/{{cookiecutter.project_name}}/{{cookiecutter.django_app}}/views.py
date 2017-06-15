from rest_framework_json_api import views
from . import serializers
from . import models


class UserViewSet(views.ModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        user = self.request.user
        return models.User.objects.filter(id=user.id)
