from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from organization_parser.adapters.database.tables.base import (
    BaseTable,
    IdentifiableMixin,
    TimestampedMixin,
)


class UserTable(TimestampedMixin, IdentifiableMixin, BaseTable):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        index=True,
        nullable=False,
    )
