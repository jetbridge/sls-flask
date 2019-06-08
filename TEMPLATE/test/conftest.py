import os
import sqlalchemy as sa
from faker import Faker
from pytest_postgresql.factories import (
    drop_postgresql_database,
    init_postgresql_database,
)
import pytest
from TEMPLATE.create_app import create_app
from flask_jwt_extended import create_access_token
from TEMPLATE.db.fixtures import NormalUserFactory
from pytest_factoryboy import register

register(NormalUserFactory)

# for faker
LOCALE = "en_US"

# Retrieve a database connection string from the environment
# should be a DB that doesn't exist
DB_CONN = os.getenv("TEST_DATABASE_URL", "postgresql:///TEMPLATE_test".lower())
DB_OPTS = sa.engine.url.make_url(DB_CONN).translate_connect_args()


@pytest.fixture(scope="session")
def database(request):
    """Create a Postgres database for the tests, and drop it when the tests are done."""
    pg_host = DB_OPTS.get("host")
    pg_port = DB_OPTS.get("port")
    pg_user = DB_OPTS.get("username")
    pg_db = DB_OPTS["database"]

    db = init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

    yield db

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 11.2)


@pytest.fixture(scope="session")
def app(database):
    """Create a Flask app context for tests."""
    # override config for test app here
    app = create_app(dict(SQLALCHEMY_DATABASE_URI=DB_CONN, TESTING=True))

    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def _db(app):
    """Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy database connection."""
    from TEMPLATE.db import db

    # create all tables for test DB
    db.create_all()

    return db


@pytest.fixture
def client_unauthenticated(app):
    return app.test_client()


@pytest.fixture
def client(app, user, session):
    # get flask test client
    client = app.test_client()

    access_token = create_access_token(identity=user)

    # set environ http header to authenticate user
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"

    return client


@pytest.fixture(scope="session")
def faker():
    return Faker(LOCALE)


@pytest.fixture
def user(normal_user_factory, session):
    user = normal_user_factory.create()
    session.add(user)
    session.commit()
    return user


@pytest.fixture(autouse=True)
def session(db_session):
    """Ensure every test is inside a subtransaction giving us a clean slate each test."""
    yield db_session
