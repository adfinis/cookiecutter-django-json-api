from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "{{cookiecutter.project_name}}.{{cookiecutter.django_app}}"
