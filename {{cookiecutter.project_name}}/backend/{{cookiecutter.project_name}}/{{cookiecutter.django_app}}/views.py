from rest_framework_json_api import views
from . import serializers
from . import models


class UserViewSet(views.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
