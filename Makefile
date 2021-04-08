.PHONY: test

SHELL:=/bin/sh
USER_ID=$(shell id --user)

clean:
	if [ -d "ci_project" ]; then \
	  cd ci_project; docker-compose down -v; cd ..; \
	  rm -rf ci_project; \
	fi

test: clean
	pip install -U cookiecutter black
	cookiecutter --no-input . project_name=ci_project django_app=api organization_slug=ci-project
	echo "UID=$(USER_ID)" > ci_project/.env
	# format build ci_project as line lengths have changed due to replacement
	black ci_project
	# not generated code needs to be checked for correct formatting as well
	black --check .
	make -C ci_project start
	# don't check black in the generated project
	docker-compose --file=ci_project/docker-compose.yml exec -T backend /bin/sh -c "flake8 && pytest --no-cov-on-fail --cov --create-db"
