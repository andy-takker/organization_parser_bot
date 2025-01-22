from abc import abstractmethod
from typing import Protocol

from organization_parser.domains.entities.api_key import ApiKey
from organization_parser.domains.entities.common.enums import Source
from organization_parser.domains.entities.common.value_objects import UserId


class IApiKeyRepository(Protocol):
    @abstractmethod
    async def get_api_key(self, source: Source, user_id: UserId) -> ApiKey | None:
        raise NotImplementedError
