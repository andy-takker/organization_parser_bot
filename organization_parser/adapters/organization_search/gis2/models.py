from collections.abc import Sequence

from pydantic import BaseModel


class Gis2Company(BaseModel):
    id: str
    name: str
    address_name: str
    address_comment: str


class Gis2Result(BaseModel):
    items: Sequence[Gis2Company]


class Gis2Search(BaseModel):
    result: Gis2Result
