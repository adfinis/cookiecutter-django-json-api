import datetime
import os
import re

import environ

env = environ.Env()
django_root = environ.Path(__file__) - 2

ENV_FILE = env.str('DJANGO_ENV_FILE', default=django_root('.env'))
if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)

# per default production is enabled for security reasons
# for development create .env file with ENV=development
ENV = env.str('ENV', 'production')


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == 'production' else default_dev


SECRET_KEY = env.str('DJANGO_SECRET_KEY', default=default('uuuuuuuuuu'))
DEBUG = env.bool('DJANGO_DEBUG', default=default(True, False))
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=default(['*']))


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    '{{cookiecutter.project_name}}.{{cookiecutter.django_app}}.apps.DefaultConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = '{{cookiecutter.project_name}}.urls'
WSGI_APPLICATION = '{{cookiecutter.project_name}}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.str(
            'DJANGO_DATABASE_ENGINE',
            default='django.db.backends.postgresql_psycopg2'
        ),
        'NAME': env.str('DJANGO_DATABASE_NAME', default='{{cookiecutter.project_name}}'),
        'USER': env.str('DJANGO_DATABASE_USER', default='{{cookiecutter.project_name}}'),
        'PASSWORD': env.str(
            'DJANGO_DATABASE_PASSWORD', default=default('{{cookiecutter.project_name}}')
        ),
        'HOST': env.str('DJANGO_DATABASE_HOST', default='localhost'),
        'PORT': env.str('DJANGO_DATABASE_PORT', default='')
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },  # noqa: E501
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },  # noqa: E501
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },  # noqa: E501
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },  # noqa: E501
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = env.str('DJANGO_LANGUAGE_CODE', 'en-us')
TIME_ZONE = env.str('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = '{{cookiecutter.django_app}}.User'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER':
        'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_METADATA_CLASS':
        'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'ORDERING_PARAM': 'sort',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}

JSON_API_FORMAT_FIELD_NAMES = 'dasherize'
JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = True

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=30),
    'JWT_ALLOW_REFRESH': True,
}


def parse_admins(admins):
    """
    Parse env admins to django admins.

    Example of DJANGO_ADMINS environment variable:
    Test Example <test@example.com>,Test2 <test2@example.com>
    """
    result = []
    for admin in admins:
        match = re.search('(.+) \<(.+@.+)\>', admin)
        if not match:  # pragma: no cover
            raise environ.ImproperlyConfigured(
                'In DJANGO_ADMINS admin "{0}" is not in correct '
                '"Firstname Lastname <email@example.com>"'.format(admin))
        result.append((match.group(1), match.group(2)))
    return result


ADMINS = parse_admins(env.list('DJANGO_ADMINS', default=[]))
