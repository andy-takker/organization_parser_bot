from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from organization_parser.domains.entities.organization import ImportOrganization


class IOrganizationSearchClient(Protocol):
    @abstractmethod
    async def search_organizations(self, name: str) -> Sequence[ImportOrganization]: ...
