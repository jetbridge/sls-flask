from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm.query import Query

from TEMPLATE.db.query_filter import QueryFilter, FilteredQuery


class SoftDeletableQueryFilter(QueryFilter):
    """Omit rows marked as deleted."""

    def apply_default_filter(self) -> Query:
        return self.filter(self.entity.deleted_at.is_(None))

    def get_filter(self, obj: "SoftDeletable") -> bool:
        return obj is None or not obj.deleted_at


class SoftDeletableQuery(FilteredQuery):
    """Query mixin."""

    default_filters = [SoftDeletableQueryFilter]


class SoftDeletable:
    """Model mixin."""

    deleted_at = Column(DateTime(timezone=True))

    def mark_deleted(self) -> None:
        self.deleted_at = func.now()
