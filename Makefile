.PHONY: init init-from-template hooks run seed test check cfn-lint ldb init-db idb flask-init-db deploy-dev deploy-staging

PYTHON=pipenv run

init: init-from-template hooks

init-from-template:
	npm install
	pipenv install --dev
	@bash script/initialize_project.sh

hooks:
	$(PYTHON) pre-commit install

run:
	FLASK_ENV=development $(PYTHON) flask run --reload

seed:
	$(PYTHON) flask seed

test:
	$(PYTHON) pytest

check:
	$(PYTHON) flake8
	$(PYTHON) mypy .
	$(PYTHON) bento check
	$(PYTHON) pytest

cfn-lint:
	npm run sls-package
	cfn-lint

# init DB
init-db: idb
idb: dropcreatedb flask-init-db seed

dropcreatedb:
	dropdb TEMPLATE --if-exists
	createdb TEMPLATE

flask-init-db:
	flask init-db

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
