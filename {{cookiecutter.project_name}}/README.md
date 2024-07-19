# {{cookiecutter.project_name}}

[![Build Status]({{cookiecutter.url}}/workflows/Tests/badge.svg)]({{cookiecutter.url}}/actions?query=workflow%3ATests)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)]({{cookiecutter.url}}/blob/main/{{cookiecutter.project_name}}/pyproject.toml#L115)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)

{{cookiecutter.description}}

## Getting started

### Installation

**Requirements**
* docker

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/{{cookiecutter.organization_slug}}/{{cookiecutter.project_name}}/master/docker-compose.yml) and run the following command:

```bash
docker compose build --pull
docker compose run --rm backend poetry run ./manage.py makemigrations
docker compose up -d
```

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).

### Configuration

{{cookiecutter.project_name}} is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
Different environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).

#### Common

A list of configuration options which you need

* `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
* `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).
* `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)
* `DATABASE_HOST`: Host to use when connecting to database (default: localhost)
* `DATABASE_PORT`: Port to use when connecting to database (default: 5432)
* `DATABASE_NAME`: Name of database to use (default: {{cookiecutter.project_name}})
* `DATABASE_USER`: Username to use when connecting to the database (default: {{cookiecutter.project_name}})
* `DATABASE_PASSWORD`: Password to use when connecting to database

## Contributing

Look at our [contributing guidelines](CONTRIBUTING.md) to start with your first contribution.
