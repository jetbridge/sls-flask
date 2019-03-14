.PHONY: init migrate all-tests lint test db migrate rev run

init:
	yarn
	pipenv install --dev
	@bash script/initialize_project.sh

run:
	flask run --reload

db:
	flask db

migrate:
	flask db upgrade

rev:
	flask db migrate

test:
	pytest

all-test:
	flake8
	pytest
