from typing import Iterable, Type

from flask_sqlalchemy import BaseQuery as Query


class QueryFilter(Query):
    """Base class for constructing query filters."""

    def apply_default_filter(self) -> Query:
        """Modify query as desired here."""
        raise NotImplementedError()

    def get_filter(self, obj) -> bool:
        """Permit or deny the retrieval of model objects via the instance map cache.

        This is not done via a query so it must be a code-level check.
        """
        raise NotImplementedError()

    @property
    def entity(self):
        return self._primary_entity.type


class FilteredQuery(QueryFilter):
    """Automatically apply a filter to all queries by default.

    You must implement `apply_default_filter(self).`

    To remove all default filters, call `query.without_filters()`
    or `query.get_without_filters()`.
    """

    default_filters: Iterable[Type[QueryFilter]] = []

    def __new__(cls, *args, **kwargs):
        """Create and return a new query object."""
        obj = super(FilteredQuery, cls).__new__(cls)
        without_filters = kwargs.pop("_without_filters", False)
        if len(args) > 0:
            super(FilteredQuery, obj).__init__(*args, **kwargs)

            # add default filters unless without_filters() was called
            if not without_filters:
                return obj.apply_default_filters()
        return obj

    def __init__(self, *args, **kwargs):
        """Empty Init."""

    def without_filters(self):
        """Just get raw query without any default filters added."""
        # FIXME: figure out how to write this without needing `db`
        from TEMPLATE.db import db

        return self.__class__(
            db.class_mapper(self._mapper_zero().class_),
            session=db.session(),
            _without_filters=True,
        )

    def apply_default_filters(self):
        """Apply default filters to the query when it is first constructed."""
        default_filters = [filt.apply_default_filter for filt in self.default_filters]
        # apply each query filter in sequence
        # probably a sweeter way to write this.
        q = self
        for filt in default_filters:
            q = filt(q)
        return q

    def _orig_get(self, *args, **kwargs):
        """Call the original query.get function from the base class."""
        return super(FilteredQuery, self).get(*args, **kwargs)

    def get_without_filters(self, *args, **kwargs):
        return self.without_filters()._orig_get(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Return resource with given id."""
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.get_without_filters(*args, **kwargs)

        # all the get_filter methods on our filters
        get_filters = [filt.get_filter for filt in self.default_filters]

        # apply all get_filter(obj) methods
        if all(filt(self, obj) for filt in get_filters):
            # passed all get filters
            return obj
        else:
            return None
