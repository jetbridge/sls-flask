.PHONY: init migrate all-tests lint test db migrate rev run

init: init-from-template

VENV=pipenv run

init-from-template:
	yarn
	pipenv install --dev
	@bash script/initialize_project.sh

run:
	flask run --reload

seed:
	flask seed

test:
	pytest

all-test:
	flake8
	pytest
