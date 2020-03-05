.PHONY: init init-from-template run hooks seed test check cfn-lint ldb init-db idb flask-init-db deploy-dev deploy-qa

PYTHON=poetry run

init: init-from-template hooks

init-from-template:
	@bash script/initialize_project.sh
	git init
	npm install

run:
	FLASK_ENV=development $(PYTHON) flask run --reload

hooks:
	$(PYTHON) pre-commit install

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

deploy-qa:
	sls deploy --stage qa
	sls --stage qa $(FLASK_MIGRATE_UPGRADE)

deploy-prd:
	sls deploy --stage prd
	sls --stage prd $(FLASK_MIGRATE_UPGRADE)
