from . import db
import factory
from pytest_factoryboy import register
from faker import Factory as FakerFactory


faker: FakerFactory = FakerFactory.create()


def seed_db():
    # seed DB with factories here
    # https://pytest-factoryboy.readthedocs.io/en/latest/#model-fixture
    db.session.commit()
    print("Database seeded.")
