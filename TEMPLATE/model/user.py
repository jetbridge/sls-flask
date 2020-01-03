from enum import Enum, unique
from sqlalchemy.types import Text, Enum as SQLAEnum
from sqlalchemy import Column
from jetkit.db.extid import ExtID
from jetkit.model.user import CoreUser
from typing import Any, Mapping

from TEMPLATE.db import db


@unique
class UserType(Enum):
    normal = "normal"


class User(db.Model, CoreUser, ExtID["User"]):
    _user_type = Column(
        SQLAEnum(UserType), nullable=False, server_default=UserType.normal.value
    )
    avatar_url = db.Column(Text())
    __mapper_args__: Mapping[str, Any] = {"polymorphic_on": _user_type}


User.add_create_uuid_extension_trigger()


class NormalUser(User):
    __mapper_args__ = {"polymorphic_identity": UserType.normal}
