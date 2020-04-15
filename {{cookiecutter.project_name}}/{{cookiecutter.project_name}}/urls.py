from django.conf.urls import include
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("api-token-auth/", TokenObtainPairView.as_view(), name="login"),
    path("api-token-refresh/", TokenRefreshView.as_view(), name="refresh"),
    path(
        "api/v1/",
        include("{{cookiecutter.project_name}}.{{cookiecutter.django_app}}.urls"),
    ),
]
