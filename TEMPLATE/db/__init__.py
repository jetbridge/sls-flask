import os
from abc import abstractmethod
from functools import partial
from typing import Optional

from aws_xray_sdk.ext.flask_sqlalchemy.query import XRayFlaskSqlAlchemy
from flask_sqlalchemy import Model as FlaskSQLAModel, SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, Table, event, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.event import listen
from sqlalchemy.schema import DDL
from TEMPLATE.db.soft_deletable import SoftDeletable
from TEMPLATE.db.upsert import Upsertable

# recommended to use TIMESTAMP WITH TIMEZONE
TSTZ = DateTime(timezone=True)


class BaseModel(FlaskSQLAModel, SoftDeletable, Upsertable):
    id = Column(Integer(), primary_key=True)
    created = Column(TSTZ, nullable=False, server_default=func.now())
    updated = Column(TSTZ, nullable=True, onupdate=func.now())


db: SQLAlchemy = None
if os.getenv("XRAY"):
    # enable x-ray tracing of queries
    db = XRayFlaskSqlAlchemy(model_class=BaseModel)
else:
    # normal Flask-SQLA
    db = SQLAlchemy(model_class=BaseModel)

Model = db.Model


class Owned:
    """Protocol for models that have an `owner` user."""

    @property
    @abstractmethod
    def id(self):
        ...

    @property
    @abstractmethod
    def owner(self):
        ...


class ExtID:
    """Add an external UUID column `extid`.

    Useful for exposing unique identifiers to clients.
    Requires "uuid-ossp" extension.
    """

    # UUID that can be used for semi-secret key
    extid = Column(
        UUID(as_uuid=True), nullable=False, server_default=text("uuid_generate_v4()")
    )

    @classmethod
    def get_by_extid(cls: db.Model, uuid: str) -> Optional["ExtID"]:
        return cls.filter_by(extid=uuid).one_or_none()

    @classmethod
    def add_create_uuid_extension_trigger(cls, TableClass):
        """Call this for any tables that use ext_id to ensure they have the uuid-ossp extension already available."""
        trigger = DDL('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        event.listen(
            TableClass.__table__,
            "before_create",
            trigger.execute_if(dialect="postgresql"),
        )


def on_table_create(class_, ddl):
    """Run DDL on model class `class_` after creation, whether in migration or in deploy (as in tests)."""

    def listener(tablename, ddl, table, bind, **kw):
        if table.name == tablename:
            ddl(table, bind, **kw)

    listen(Table, "after_create", partial(listener, class_.__table__.name, ddl))


# load all model classes now
import TEMPLATE.model  # noqa: F401
