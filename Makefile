.DEFAULT_GOAL := help

SHELL:=/bin/sh
USER_ID=$(shell id --user)

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: uid
uid:
	@echo "UID=$(USER_ID)" > ci_project/.env

.PHONY: clean
clean: ## stop project and remove local build
	@if [ -d "ci_project" ]; then \
	  cd ci_project; docker compose down -v; cd ..; \
	  rm -rf ci_project; \
	fi

.PHONY: build
build: clean ## build the project
	@pip install -U cookiecutter
	@cookiecutter --no-input --overwrite-if-exists . project_name=ci_project django_app=api organization_slug=ci-project
	@echo "UID=$(USER_ID)" > ci_project/.env
	make -C ci_project start

.PHONY: lint-output ## Lint the built project
lint-output: build uid
	docker compose --file=ci_project/docker-compose.yml exec -T backend /bin/sh -c "poetry run ruff format . && poetry run ruff check ."

.PHONY: start
start: build uid ## start the project
	make -C ci_project start

.PHONY: test
test: start lint-output ## test the project
	docker compose --file=ci_project/docker-compose.yml exec -T backend /bin/sh -c "poetry run pytest -vv --no-cov-on-fail --cov --create-db"
