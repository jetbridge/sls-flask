"""Create fake models for tests and seeding dev DB."""
from faker import Factory as FakerFactory
import factory
from pytest_factoryboy import register
import random
from TEMPLATE.model.user import NormalUser, User
from TEMPLATE.db import db

faker: FakerFactory = FakerFactory.create()
DEFAULT_NORMAL_USER_EMAIL = "test@test.test"
DEFAULT_PASSWORD = "testo"


def seed_db():
    # seed DB with factories here
    # https://pytest-factoryboy.readthedocs.io/en/latest/#model-fixture

    # default normal user
    if not User.query.filter_by(email=DEFAULT_NORMAL_USER_EMAIL).one_or_none():
        # add default user for testing
        db.session.add(
            NormalUserFactory.create(
                email=DEFAULT_NORMAL_USER_EMAIL, password=DEFAULT_PASSWORD
            )
        )
        print(
            f"Created default user with email {DEFAULT_NORMAL_USER_EMAIL} "
            f"with password '{DEFAULT_PASSWORD}'"
        )

    db.session.commit()
    print("Database seeded.")


class UserFactoryFactory(factory.Factory):
    dob = factory.LazyAttribute(lambda x: faker.simple_profile()["birthdate"])
    name = factory.LazyAttribute(lambda x: faker.name())
    password = DEFAULT_PASSWORD
    avatar_url = factory.LazyAttribute(
        lambda x: f"https://placem.at/people?w=200&txt=0&random={random.randint(1, 100000)}"
    )


@register
class NormalUserFactory(UserFactoryFactory):
    class Meta:
        model = NormalUser

    email = factory.Sequence(lambda n: f"normaluser.{n}@example.com")
