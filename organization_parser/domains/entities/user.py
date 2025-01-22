from dataclasses import dataclass
from datetime import datetime

from organization_parser.domains.entities.common.value_objects import UserId


@dataclass(frozen=True, slots=True, kw_only=True)
class User:
    id: UserId
    tg_id: int
    created_at: datetime
    updated_at: datetime
