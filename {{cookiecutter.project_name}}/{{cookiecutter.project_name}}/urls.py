from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path(
        "api/v1/",
        include("{{cookiecutter.project_name}}.{{cookiecutter.django_app}}.urls"),
    ),
]
