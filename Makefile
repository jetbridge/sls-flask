.PHONY: init migrate all-tests lint test db migrate rev

init:
	@bash script/initialize_project.sh


db:
	flask db

migrate:
	flask db upgrade

rev:
	flask db migrate
