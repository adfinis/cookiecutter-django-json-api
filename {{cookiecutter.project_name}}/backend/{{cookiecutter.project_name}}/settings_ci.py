"""
This is a settings file for GitLab CI to use
"""
from .settings import *  # noqa: F401

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     '{{cookiecutter.project_name}}',
        'USER':     '{{cookiecutter.project_name}}',
        'PASSWORD': '{{cookiecutter.project_name}}',
        'HOST':     'postgres'
    }
}
