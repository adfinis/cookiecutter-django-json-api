FROM python:3.12-alpine as base

RUN apk update --no-cache && apk upgrade --no-cache && apk add wait4ports shadow --no-cache && useradd -m -r -u 1001 {{cookiecutter.project_name}} && apk del shadow && rm -rf /var/cache/apk/*

COPY manage.py /usr/local/bin

ENV DJANGO_SETTINGS_MODULE={{cookiecutter.project_name}}.settings \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

EXPOSE 8000

FROM base AS build

WORKDIR /app

COPY . ./

ENV POETRY_NO_INTERACTION 1

RUN pip install -U poetry

FROM build AS wheel

WORKDIR /app

RUN poetry build -f wheel && mv ./dist/*.whl /tmp/

FROM build AS dev

WORKDIR /app

RUN poetry config virtualenvs.create false && \
 poetry install

USER 1001

CMD ["sh", "-c", "wait4ports -s 15 tcp://${DATABASE_HOST:-db}:${DATABASE_PORT:-5432} && manage.py migrate --no-input && ./manage.py migrate && ./manage.py runserver --no-static 0.0.0.0:8000"]

FROM base AS prod

COPY --from=wheel /tmp/*.whl /tmp/

USER 1001

CMD ["sh", "-c", "wait4ports -s 15 tcp://${DATABASE_HOST}:${DATABASE_PORT:-5432} && manage.py migrate --no-input && ./manage.py migrate && gunicorn --workers 10 --access-logfile - --limit-request-line 16384 --bind :8000 {{cookiecutter.project_name}}.wsgi"]
