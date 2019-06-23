from enum import Enum, unique
from sqlalchemy.types import Date, Text

from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from TEMPLATE.db import TSTZ, db
from TEMPLATE.db.extid import ExtID


@unique
class UserType(Enum):
    normal = "normal"


class User(db.Model, ExtID):
    email = db.Column(Text(), unique=True, nullable=True)
    email_validated = db.Column(TSTZ)

    dob = db.Column(Date())
    name = db.Column(Text())
    avatar_url = db.Column(Text())

    phone_number = db.Column(Text())
    _password = db.Column(Text())

    @hybrid_property
    def password(self):
        return self._password

    @password.setter  # noqa: T484
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return check_password_hash(self._password, plaintext)

    def __repr__(self):
        return f"<User id={self.id} {self.email}>"


User.add_create_uuid_extension_trigger()


class NormalUser(User):
    __mapper_args__ = {"polymorphic_identity": UserType.normal}
