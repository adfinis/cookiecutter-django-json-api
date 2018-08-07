FROM python:3.6

ENV DJANGO_SETTINGS_MODULE {{cookiecutter.project_name}}.settings
ENV UWSGI_INI /app/uwsgi.ini

COPY . /app
WORKDIR /app

RUN make install

EXPOSE 80
CMD ["uwsgi"]
