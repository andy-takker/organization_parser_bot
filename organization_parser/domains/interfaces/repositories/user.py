from abc import ABC, abstractmethod

from organization_parser.domains.entities.user import User


class IUserRepository(ABC):
    async def get_or_create(self, *, tg_user_id: int) -> User:
        user = await self.get_by_tg_id(tg_user_id=tg_user_id)
        return user or await self.create(tg_user_id=tg_user_id)

    @abstractmethod
    async def create(self, *, tg_user_id: int) -> User: ...

    @abstractmethod
    async def get_by_tg_id(self, *, tg_user_id: int) -> User | None: ...
