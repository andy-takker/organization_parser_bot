from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, kw_only=True, slots=True)
class Organization:
    id: UUID
    import_id: str
    import_source: str
    name: str
    address_name: str


@dataclass(frozen=True, kw_only=True, slots=True)
class ImportOrganization:
    import_id: str
    import_source: str
    name: str
    address_name: str
