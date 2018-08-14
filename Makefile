.PHONY: test

test:
	rm -rf ci_project
	pip install cookiecutter
	cookiecutter --no-input . project_name=ci_project django_app=api
	echo "ENV=ci" > ci_project/.env
	echo "ADMINS=Test Example <test@example.com>,Test2 <test2@example.com>" >> ci_project/.env
	echo "DATABASE_ENGINE=django.db.backends.sqlite3" >> ci_project/.env
	make -C ci_project install-dev test
