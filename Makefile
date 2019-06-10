.PHONY: init migrate all-tests lint test db migrate rev run

init: init-from-template seed

init-from-template:
	yarn
	pipenv install --dev
	@bash script/initialize_project.sh
	pre-commit install

run:
	flask run --reload

db:
	flask db

seed:
	flask seed

migrate:
	flask db upgrade

rev:
	flask db migrate

test:
	pytest

all-test:
	flake8
	pytest
