from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from organization_parser.adapters.database.tables import UserTable
from organization_parser.adapters.database.uow import SqlalchemyUow
from organization_parser.domains.entities.common.value_objects import UserId
from organization_parser.domains.entities.user import User
from organization_parser.domains.interfaces.repositories.user import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, uow: SqlalchemyUow) -> None:
        self._uow = uow

    @property
    def session(self) -> AsyncSession:
        return self._uow.session

    async def get_by_tg_id(self, *, tg_user_id: int) -> User | None:
        query = select(UserTable).where(UserTable.tg_id == tg_user_id)
        result = await self._uow.session.scalar(query)
        if result is None:
            return None
        return User(
            id=UserId(result.id),
            tg_id=result.tg_id,
            created_at=result.created_at,
            updated_at=result.updated_at,
        )

    async def create(self, *, tg_user_id: int) -> User:
        stmt = (
            insert(UserTable)
            .values(
                tg_id=tg_user_id,
            )
            .returning(UserTable)
        )
        try:
            result = (await self.session.scalars(stmt)).one()
        except IntegrityError as e:
            raise e
        return User(
            id=UserId(result.id),
            tg_id=result.tg_id,
            created_at=result.created_at,
            updated_at=result.updated_at,
        )
