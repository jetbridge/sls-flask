from sqlalchemy import Column, DateTime
from sqlalchemy.orm.query import Query

from TEMPLATE.db.query_filter import DefaultQueryFilter, QueryFilter


class SoftDeletableQueryFilter(QueryFilter):
    "By default only query for succesfully encoded videos." ""

    def apply_default_filter(self) -> Query:
        return self.filter(self.entity.deleted_on.is_(None))

    def get_filter(self, obj: "SoftDeletable") -> bool:
        return not obj.deleted_on


class SoftDeletable(DefaultQueryFilter):
    default_filters = [SoftDeletableQueryFilter]

    deleted_on = Column(DateTime(timezone=True))
