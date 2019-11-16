.PHONY: init migrate all-tests lint test db migrate rev run ldb idb

VENV=pipenv run

init: init-from-template

init-from-template:
	npm install
	pipenv install --dev
	@bash script/initialize_project.sh

run:
	FLASK_ENV=development flask run --reload

seed:
	flask seed

test:
	pytest

cfn-lint:
	npm run sls-package
	cfn-lint

# init DB
idb: dropcreatedb flask-init-db seed

dropcreatedb:
	dropdb TEMPLATE --if-exists
	createdb TEMPLATE

flask-init-db:
	flask init-db

all-test:
	flake8
	pytest

ldb:  # lambda init-db
	sls invoke -f initDb
	sls invoke -f seed

deploy-dev:
	sls deploy -s dev
	sls invoke -f initDb -s dev
	sls invoke -f seed -s dev

deploy-staging:
	sls deploy -s staging
	sls invoke -f initDb -s staging
	sls invoke -f seed -s staging
