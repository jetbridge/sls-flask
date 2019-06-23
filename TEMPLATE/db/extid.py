from sqlalchemy import Column, event, text
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from TEMPLATE.db import db
from sqlalchemy.schema import DDL


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
    def add_create_uuid_extension_trigger(cls):
        """Call this for any tables that use ext_id to ensure they have the uuid-ossp extension already available."""
        trigger = DDL('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        event.listen(
            cls.__table__, "before_create", trigger.execute_if(dialect="postgresql")
        )
