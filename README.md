Django JSON API CookieCutter template
=====================================

[![Build Status](https://github.com/adfinis/cookiecutter-django-json-api/workflows/Tests/badge.svg)](https://github.com/adfinis/cookiecutter-django-json-api/actions?query=workflow%3ATests)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/adfinis/cookiecutter-django-json-api/blob/master/{{cookiecutter.project_name}}/pyproject.toml#L155)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)
[![License: MIT](https://img.shields.io/badge/License-BSD-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

This cookie cutter provides a Django project with JSON API support. It combines Adfinis best practices in terms of setup, structure and configuration.

Requirements
------------
- Python ^3.9
- Latest [CookieCutter](http://cookiecutter.readthedocs.org/en/latest/)
- [Docker](https://docs.docker.com/)

Usage
-----

To use, simply run
`cookiecutter https://github.com/adfinis/cookiecutter-django-json-api`

Included in this template
-------------------------

Django specific:

- [Django](https://www.djangoproject.com/) - usually last LTS release
- [Django REST Framework](http://www.django-rest-framework.org/)
- [Django REST Framework JSON API](https://github.com/django-json-api/django-rest-framework-json-api)
- [Django Filter](https://django-filter.readthedocs.org/en/latest/)
- [mozilla_django_oidc](https://github.com/mozilla/mozilla-django-oidc)
- [Django Environ](https://github.com/joke2k/django-environ)


Code quality and formatting tools:

- [ruff](https://docs.astral.sh/ruff/)
- [Pytest](https://docs.pytest.org/en/latest/)
- [Pytest Coverage Plugin](https://github.com/pytest-dev/pytest-cov) - coverage set to 100%
- [Pytest Django Plugin](https://pytest-django.readthedocs.io/en/latest/)


Per default postgres is configured and a docker compose file provided. To support other database only
`DATABASE_ENGINE` environment variable needs to be changed.

License
-------

Code released under the [BSD-3 Clause](LICENSE).
