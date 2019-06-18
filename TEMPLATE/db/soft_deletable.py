from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm.query import Query

from TEMPLATE.db.query_filter import QueryFilter, FilteredQuery


class SoftDeletableQueryFilter(QueryFilter):
    """Omit rows marked as deleted."""

    def apply_default_filter(self) -> Query:
        return self.filter(self.entity.deleted_on.is_(None))

    def get_filter(self, obj: "SoftDeletable") -> bool:
        return not obj.deleted_on


class SoftDeletableQuery(FilteredQuery):
    """Query mixin."""

    default_filters = [SoftDeletableQueryFilter]


class SoftDeletable:
    """Model mixin."""

    deleted_on = Column(DateTime(timezone=True))

    def mark_deleted(self) -> None:
        self.deleted_on = func.now()
