from . import db
from faker import Factory as FakerFactory
import factory  # noqa: F401
from pytest_factoryboy import register  # noqa: F401


faker: FakerFactory = FakerFactory.create()


def seed_db():
    # seed DB with factories here
    # https://pytest-factoryboy.readthedocs.io/en/latest/#model-fixture
    db.session.commit()
    print("Database seeded.")
