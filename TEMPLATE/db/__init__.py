from flask_sqlalchemy import SQLAlchemy
from jetkit.db import BaseQuery as JKBaseQuery, BaseModel as JKBaseModel, SQLA


class BaseQuery(JKBaseQuery):
    """Base class to use for queries."""


class BaseModel(JKBaseModel):
    """Base class to use for all models."""


# initialize our XRay?FlaskSQLAlchemy instance
db: SQLAlchemy = SQLA(model_class=BaseModel, query_class=BaseQuery)

# load all model classes now
import TEMPLATE.model  # noqa: F401
