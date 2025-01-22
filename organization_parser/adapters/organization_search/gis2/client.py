from collections.abc import Sequence
from http import HTTPStatus

from aiohttp import ClientSession
from asyncly import BaseHttpClient
from asyncly.client.handlers.pydantic import parse_model
from yarl import URL

from organization_parser.adapters.organization_search.gis2.models import Gis2Search
from organization_parser.domains.entities.common.enums import Source
from organization_parser.domains.entities.organization import ImportOrganization
from organization_parser.domains.interfaces.clients.organization_search import (
    IOrganizationSearchClient,
)


class Gis2OrganizationSearchClient(IOrganizationSearchClient, BaseHttpClient):
    _auth_token: str

    def __init__(
        self, url: URL, session: ClientSession, client_name: str, auth_token: str
    ) -> None:
        super().__init__(url=url, session=session, client_name=client_name)
        self._auth_token = auth_token

    async def search_organizations(self, name: str) -> Sequence[ImportOrganization]:
        organizations: list[ImportOrganization] = []
        page = 1
        while True:
            items = await self._search_organizations(page=page, name=name)
            organizations.extend(items)
            page += 1
            if not items:
                break
        return organizations

    async def _search_organizations(
        self, *, page: int, name: str
    ) -> Sequence[ImportOrganization]:
        search: Gis2Search = await self._make_req(
            method="GET",
            handlers={
                HTTPStatus.OK: parse_model(Gis2Search),
            },
            url=self._url / "3.0/items",
            params={
                "fields": "items.contact_groups",
                "key": self._auth_token,
                "q": name,
                "page": page,
            },
        )
        return [
            ImportOrganization(
                import_id=item.id,
                import_source=Source.GIS2,
                name=item.name,
                address_name=item.address_name,
            )
            for item in search.result.items
        ]
