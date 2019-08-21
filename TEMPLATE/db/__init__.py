import os
from abc import abstractmethod
from functools import partial
from typing import TYPE_CHECKING

from aws_xray_sdk.ext.flask_sqlalchemy.query import XRayFlaskSqlAlchemy, XRayBaseQuery
from flask_sqlalchemy import (
    Model as FlaskSQLAModel,
    SQLAlchemy as FlaskSQLAlchemy,
    BaseQuery as SQLABaseQuery,
)
from sqlalchemy import Column, DateTime, Integer, Table, func
from sqlalchemy.event import listen
from TEMPLATE.db.soft_deletable import SoftDeletable
from TEMPLATE.db.upsert import Upsertable

if TYPE_CHECKING:
    import TEMPLATE.model

# recommended to use TIMESTAMP WITH TIMEZONE
TSTZ = DateTime(timezone=True)

# if we are running with AWS-XRay enabled, use the XRay-enhanced versions of query and SQLA for tracing/profiling of queries
xray_enabled = os.getenv("XRAY")
BaseQueryBase = XRayBaseQuery if xray_enabled else SQLABaseQuery
SQLA = XRayFlaskSqlAlchemy if xray_enabled else FlaskSQLAlchemy


class BaseQuery(BaseQueryBase):  # type: ignore
    """Base class to use for queries."""


class BaseModel(FlaskSQLAModel, SoftDeletable, Upsertable):
    """Base class to use for all models."""

    id = Column(Integer(), primary_key=True)
    created_at = Column(TSTZ, nullable=False, server_default=func.now())
    updated_at = Column(TSTZ, nullable=True, onupdate=func.now())


# initialize our XRay?FlaskSQLAlchemy instance
db: FlaskSQLAlchemy = SQLA(model_class=BaseModel, query_class=BaseQuery)


class Owned:
    """Protocol for models that have an `owner` user."""

    @property
    @abstractmethod
    def id(self):
        ...

    @property
    @abstractmethod
    def owner(self) -> "TEMPLATE.model.user.User":
        ...


def on_table_create(class_, ddl):
    """Run DDL on model class `class_` after creation, whether in migration or in deploy (as in tests)."""

    def listener(tablename, ddl, table, bind, **kw):
        if table.name == tablename:
            ddl(table, bind, **kw)

    listen(Table, "after_create", partial(listener, class_.__table__.name, ddl))


# load all model classes now
import TEMPLATE.model  # noqa: F811
