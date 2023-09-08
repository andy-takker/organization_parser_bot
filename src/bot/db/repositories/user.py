from typing import Any, NoReturn

from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.db.models import User
from src.bot.db.repositories.base import Repository
from src.bot.exceptions import EntityNotFoundError, OrganizationBotError


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=User, session=session)

    async def get_by_id_or_none(
        self,
        user_id: int,
    ) -> User | None:
        return await self._get_by_id_or_none(obj_id=user_id)

    async def create(self, *, user_id: int, yandex_api_key: str) -> User:
        query = (
            insert(User)
            .values(id=user_id, yandex_api_key=yandex_api_key)
            .returning(User)
        )
        try:
            result: ScalarResult[User] = await self._session.scalars(
                select(User).from_statement(query)
            )
        except IntegrityError as e:
            await self._session.rollback()
            self._raise_error(e)
        else:
            await self._session.commit()
            return result.one()

    async def create_or_update(self, *, user_id: int, yandex_api_key: str) -> User:
        try:
            user = await self.update(user_id=user_id, yandex_api_key=yandex_api_key)
        except EntityNotFoundError:
            user = await self.create(user_id=user_id, yandex_api_key=yandex_api_key)
        return user

    async def update(self, user_id: int, **kwargs: Any) -> User:
        try:
            return await self._update(User.id == user_id, **kwargs)
        except IntegrityError as e:
            await self._session.rollback()
            self._raise_error(e)

    def _raise_error(self, err: DBAPIError) -> NoReturn:
        raise OrganizationBotError from err
