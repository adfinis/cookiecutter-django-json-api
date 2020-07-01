# {{cookiecutter.project_name}}

[![Build Status](https://travis-ci.com/{{cookiecutter.organization_slug}}/{{cookiecutter.project_name}}.svg?branch=master)](https://travis-ci.com/{{cookiecutter.organization_slug}}/{{cookiecutter.project_name}})
[![Pyup](https://pyup.io/repos/github/{{cookiecutter.organization_slug}}/{{cookiecutter.project_name}}/shield.svg)](https://pyup.io/account/repos/github/{{cookiecutter.organization_slug}}/{{cookiecutter.project_name}}/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)]({{cookiecutter.url}})

{{cookiecutter.description}}

## Getting started

### Installation

**Requirements**
* docker
* docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/{{cookiecutter.organization_slug}}/{{cookiecutter.project_name}}/master/docker-compose.yml) and run the following command:

```bash
docker-compose up -d
```

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).

### Configuration

Document Merge Service is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
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
