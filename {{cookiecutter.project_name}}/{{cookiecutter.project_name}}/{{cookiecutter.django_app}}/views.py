from rest_framework_json_api import views

from . import models, serializers


class UserViewSet(views.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.UserProfile.objects

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(idp_id=user.id)
