from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.bot.db.base import Base
from src.bot.db.mixins import TimestampMixin


class User(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    yandex_api_key: Mapped[str] = mapped_column(String(32), nullable=False)
