.PHONY: init migrate all-tests lint test db migrate rev run

init: init-from-template seed

VENV=pipenv run

init-from-template:
	yarn
	pipenv install --dev
	@bash script/initialize_project.sh

run:
	(VENV) flask run --reload

seed:
	(VENV) flask seed

test:
	(VENV) pytest

all-test:
	(VENV) flake8
	(VENV) pytest
