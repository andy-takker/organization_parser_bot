import math
from typing import Any, Literal

import requests

from .dto import Company

QueryType = Literal["biz", "geo"]

REQUEST_API_URL = "https://search-maps.yandex.ru/v1/"


def get_all_results(
    apikey: str, query: str, ll: tuple[float, float], radius: float
) -> set[Company]:
    r = km_to_ll(radius)
    spn = (r, r)
    skip = 0
    total_companies = set()
    while True:
        result = search_on_maps(
            apikey=apikey,
            query=query,
            type_="biz",
            ll=ll,
            spn=spn,
            skip=skip,
        )
        if not result.ok:
            break
        data = result.json()
        total_companies.update(parse_companies(data))
        total = data["properties"]["ResponseMetaData"]["SearchResponse"]["found"]
        print(total)
        skip += len(data["features"])
        if skip >= total:
            break
    return total_companies


def get_toponym_location(apikey: str, query: str) -> tuple[float, ...]:
    result = search_on_maps(apikey=apikey, query=query, type_="geo")
    if not result.ok:
        raise ValueError(f"Result is not OK. Get status code - {result.status_code}")
    return tuple(map(float, result.json()["features"][0]["geometry"]["coordinates"]))


def search_on_maps(
    apikey: str,
    query: str,
    type_: QueryType,
    ll: tuple[float, float] | None = None,
    spn: tuple[float, float] | None = None,
    skip: int = 0,
    results: int = 50,
    lang: str = "ru_RU",
) -> requests.Response:
    params: dict[str, int | float | str] = {
        "lang": lang,
        "type": type_,
        "results": results,
        "apikey": apikey,
        "text": query,
        "skip": skip,
    }
    if ll is not None and spn is not None:
        params["ll"] = ",".join(map(str, ll))
        params["spn"] = ",".join(map(str, spn))
    result = requests.get(
        url=REQUEST_API_URL,
        params=params,
    )
    return result


def parse_companies(data: dict[str, Any]) -> list[Company]:
    companies = []
    for feature in data["features"]:
        companies.append(
            Company(
                name=feature["properties"]["CompanyMetaData"]["name"],
                address=feature["properties"]["CompanyMetaData"]["address"],
                url=feature["properties"]["CompanyMetaData"].get("url"),
            )
        )
    return companies


def km_to_ll(km: float) -> float:
    """Transfer kilometers to radian coords"""
    return km * 180 / math.pi / 6371
