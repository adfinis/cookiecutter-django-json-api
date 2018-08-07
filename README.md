Django JSON API CookieCutter template
=====================================

This cookie cutter provides a Django project with JSON API support. It combines Adfinis best practices in terms of setup, structure and configuration.

Requirements
------------
- Latest [Python & virtualenv](https://www.python.org/downloads/release)
- Latest [CookieCutter](http://cookiecutter.readthedocs.org/en/latest/)
- Latest [Docker](https://docs.docker.com/)
- Latest [Docker Compose](https://docs.docker.com/compose/)

Usage
-----

To use, simply run
`cookiecutter https://github.com/adfinis-sygroup/cookiecutter-django-json-api`

Included in this template
-------------------------

Django specific:

- [Django](https://www.djangoproject.com/) - usually last LTS release
- [Django REST Framework](http://www.django-rest-framework.org/)
- [Django REST Framework JSON API](https://github.com/django-json-api/django-rest-framework-json-api)
- [Django Filter](https://django-filter.readthedocs.org/en/latest/)
- [Django REST Framework JWT Auth](https://getblimp.github.io/django-rest-framework-jwt/)
- [Django Environ](https://github.com/joke2k/django-environ)


Code quality tools:

- [Flake8](http://flake8.pycqa.org/en/latest/) - includes .flake8 with some defaults
- [Flake8 Debugger Plugin](https://github.com/jbkahn/flake8-debugger)
- [Flake8 DocStrings Plugin](https://gitlab.com/pycqa/flake8-docstrings)
- [Flake8 isort plugin](https://github.com/gforcada/flake8-isort)
- [Flake8 String Format Plugin](https://github.com/xZise/flake8-string-format)
- [Flake8 Tuple](https://github.com/ar4s/flake8_tuple)
- [IPython debugger](https://github.com/gotcha/ipdb)
- [isort](https://pypi.python.org/pypi/isort)
- [Pytest](https://docs.pytest.org/en/latest/)
- [Pytest Coverage Plugin](https://github.com/pytest-dev/pytest-cov) - coverage set to 100%
- [Pytest Django Plugin](https://pytest-django.readthedocs.io/en/latest/)


Per default postgres is configured and a docker compose file provided. To support other database only
`DJANGO_DATABASE_ENGINE` environment variable needs to be changed.

License
-------

Code released under the [BSD-3 Clause](LICENSE).
