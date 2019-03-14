## Opinionated Serverless Flask
Comes with a lot of useful stuff ready to go.


## Features
* [Flask REST API](https://github.com/Nobatek/flask-rest-api)
  * OpenAPI
  * Swagger UI
  * Redoc
* [Pytest using database subtransactions](https://pypi.org/project/pytest-flask-sqlalchemy/) for test isolation
* Flake8 with [Mypy](http://mypy-lang.org/) for type-checking
* AWS Lambda integration
  * [Serverless AWS](https://serverless.com/framework/docs/providers/aws/)
  * Load Flask config from AWS Secrets Manager
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) for DB migrations with alembic and Flask CLI
* [Pipenv](https://pipenv.readthedocs.io/en/latest/) for dependency management


## Quickstart:

### Prerequisites:
`brew install pipenv yarn`

### Create Project:
```
yarn global add serverless
sls install --url https://github.com/jetbridge/sls-flask --name myapp
cd myapp
make init  # install dependencies and initialize project

pipenv shell  # activate python virtual environment
flask run --reload  # run flask dev server
sls wsgi serve  # run flask server under serverless
sls deploy  # deploy serverless app
```

### API Documentation:
Once your flask dev server is running:
* [OpenAPI JSON](http://localhost:5000/api/openapi.json)
* [Swagger UI](http://localhost:5000/api/swagger)
* [ReDoc](http://localhost:5000/api/doc)
