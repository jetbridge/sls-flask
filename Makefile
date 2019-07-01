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

all-test:
	flake8
	pytest
