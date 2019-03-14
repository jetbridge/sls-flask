## Opinionated Serverless Flask
Comes with a lot of useful stuff ready to go.


## Features
* [Flask REST API](https://github.com/Nobatek/flask-rest-api)
 * OpenAPI
 * Swagger UI
 * Redoc
* [Pytest using database subtransactions](https://pypi.org/project/pytest-flask-sqlalchemy/) for test isolation
* Flake8 with Mypy for type-checking
* AWS Lambda integration
 * [Serverless](https://serverless.com/)
 * Load Flask config from AWS Secrets Manager
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) for DB migrations with alembic and Flask CLI
* [Pipenv](https://pipenv.readthedocs.io/en/latest/) for dependency management

## Start a new flask serverless project:
```
sls install --url https://github.com/revmischa/slspy --name myapp
cd myapp
make init
```
