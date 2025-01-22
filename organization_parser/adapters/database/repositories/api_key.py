from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from organization_parser.adapters.database.tables import ApiKeyTable
from organization_parser.adapters.database.uow import SqlalchemyUow
from organization_parser.domains.entities.api_key import ApiKey
from organization_parser.domains.entities.common.enums.source import Source
from organization_parser.domains.entities.common.value_objects import ApiKeyId, UserId
from organization_parser.domains.interfaces.repositories.api_key import (
    IApiKeyRepository,
)


class ApiKeyRepository(IApiKeyRepository):
    def __init__(self, uow: SqlalchemyUow) -> None:
        self._uow = uow

    @property
    def session(self) -> AsyncSession:
        return self._uow.session

    async def get_api_key(self, source: Source, user_id: UserId) -> ApiKey | None:
        stmt = select(ApiKeyTable).where(
            ApiKeyTable.source == source,
            ApiKeyTable.user_id == user_id,
        )
        result = await self.session.scalar(stmt)
        if result is None:
            return None
        return ApiKey(
            id=ApiKeyId(result.id),
            user_id=UserId(result.user_id),
            source=result.source,
            value=result.value,
        )
