.PHONY: init migrate all-tests lint test db migrate rev run

VENV=pipenv run

init: init-from-template

init-from-template:
	yarn
	pipenv install --dev
	@bash script/initialize_project.sh

run:
	FLASK_ENV=development flask run --reload

seed:
	flask seed

test:
	pytest

cfn-lint:
	yarn sls package
	cfn-lint

init-db: flask-init-db seed

flask-init-db:
	flask init-db

all-test:
	flake8
	pytest
