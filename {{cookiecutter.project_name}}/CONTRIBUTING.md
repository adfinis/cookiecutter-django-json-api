# Contributing

Contributions to {{cookiecutter.project_name}} are very welcome! Best have a look at the open [issues](https://github.com/{{cookiecutter.organization_slug}}/{{cookiecutter.project_name}})
and open a [GitHub pull request](https://github.com/{{cookiecutter.organization_slug}}/{{cookiecutter.project_name}}/compare). See instructions below how to setup development
environment. Before writing any code, best discuss your proposed change in a GitHub issue to see if the proposed change makes sense for the project.

## Setup development environment

### Clone

To work on {{cookiecutter.project_name}} you first need to clone

```bash
git clone https://github.com/{{cookiecutter.organization_slug}}/{{cookiecutter.project_name}}.git
cd {{cookiecutter.project_name}}
```

### Open Shell

Once it is cloned you can easily open a shell in the docker container to
open an development environment.

```bash
# needed for permission handling
# only needs to be run once
echo UID=$UID > .env
# open shell
docker compose run --rm {{cookiecutter.project_name}} bash
```

### Testing

Once you have shelled in docker container as described above
you can use common python tooling for formatting, linting, testing
etc.

```bash
# linting
ruff check .
# format code
ruff format .
# running tests
pytest
# create migrations
./manage.py makemigrations
# install debugger or other temporary dependencies
pip install --user pdbpp
```

Writing of code can still happen outside the docker container of course.

### Install new requirements

In case you're adding new requirements you simply need to build the docker container
again for those to be installed and re-open shell.

```bash
docker compose build --pull
```

### Setup pre commit

Pre commit hooks is an additional option instead of executing checks in your editor of choice.

```bash
pre-commit install --hook=pre-commit
pre-commit install --hook=commit-msg
```
