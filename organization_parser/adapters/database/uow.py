import asyncio
import logging
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
)

from organization_parser.domains.uow import AbstractUow

logger = logging.getLogger(__name__)


class SqlalchemyUow(AbstractUow):
    __session: AsyncSession | None
    session_factory: async_sessionmaker[AsyncSession]
    transaction: AsyncSessionTransaction | None

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory
        self.__session = None
        self.transaction = None

    @property
    def session(self) -> AsyncSession:
        if self.__session is None:
            raise Exception("Session is not created")
        return self.__session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
        self.transaction = None

    async def create_transaction(self) -> None:
        if self.__session is not None:
            logger.warning("Attempt to create already existing session")
        self.__session = self.session_factory()
        self.transaction = await self.session.begin()

    async def close_transaction(self, *exc: Any) -> None:
        task = asyncio.create_task(self.session.close())
        await asyncio.shield(task)
