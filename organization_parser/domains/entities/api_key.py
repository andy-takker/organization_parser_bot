from dataclasses import dataclass

from organization_parser.domains.entities.common.enums import Source
from organization_parser.domains.entities.common.value_objects import ApiKeyId, UserId


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiKey:
    id: ApiKeyId
    user_id: UserId
    source: Source
    value: str
