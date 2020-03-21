## Opinionated Serverless Flask

Comes with a lot of useful stuff ready to go.

## Features

- [Flask Smorest](https://pypi.org/project/flask-smorest/)
  - OpenAPI
  - Swagger UI
  - Redoc
- [Pytest using database subtransactions](https://pypi.org/project/pytest-flask-sqlalchemy/) for test isolation
- [Pytest-FactoryBoy](https://pytest-factoryboy.readthedocs.io/en/latest/#model-fixture) for generating sample data for seeding DB and tests.
- Flake8 with [Mypy](http://mypy-lang.org/) for type-checking
- AWS Lambda integration
  - [Serverless AWS](https://serverless.com/framework/docs/providers/aws/)
  - Load Flask config from AWS Secrets Manager
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) for DB migrations with alembic and Flask CLI
- [Poetry](https://python-poetry.org/docs/) for dependency management

## Quickstart:

### Prerequisites:

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python  # poetry
npm i -g serverless
```

### Create Project:

```
npx sls install --url https://github.com/jetbridge/sls-flask --name myapp
cd myapp
make init  # install dependencies and initialize project
```

### Python Virtual Environment:

```
poetry shell  # activate python virtual environment
poetry install  # install dependencies
```

### Do Stuff:

```
flask  # CLI commands
flask run --reload  # run flask dev server
npm install  # install serverless plugins
sls wsgi serve  # run flask server under serverless
sls deploy  # deploy serverless app
make deploy-dev  # deploy dev to AWS and reset database
make hooks  # install pre-commit hooks
```

### Database:

```
createdb TEMPLATE
flask db upgrade  # run migrations
flask seed  # populate with sample data
flask db migrate  # generate new migration
flask db  # more migration commands
```

### API Documentation:

Once your flask dev server is running:

- [OpenAPI JSON](http://localhost:5000/api/openapi.json) (http://localhost:5000/api/openapi.json)
- [Swagger UI](http://localhost:5000/api/swagger) (http://localhost:5000/api/swagger)
- [ReDoc](http://localhost:5000/api/doc) (http://localhost:5000/api/doc)
