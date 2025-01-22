from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from organization_parser.adapters.database.tables.base import (
    BaseTable,
    IdentifiableMixin,
    TimestampedMixin,
)
from organization_parser.domains.entities.common.enums.source import Source


class ApiKeyTable(IdentifiableMixin, TimestampedMixin, BaseTable):
    __tablename__ = "api_keys"
    __table_args__ = (UniqueConstraint("user_id", "source"),)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        PGUUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    source: Mapped[Source] = mapped_column(
        String(32),
        nullable=False,
        index=True,
    )
    value: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )
