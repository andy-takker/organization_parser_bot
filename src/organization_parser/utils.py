import csv
import logging
import math
from pathlib import Path
from typing import Any, Literal

import requests

from .dto import Company

logger = logging.getLogger(__name__)

QueryType = Literal["biz", "geo"]

REQUEST_API_URL = "https://search-maps.yandex.ru/v1/"


def save_companies_to_csv_file(companies: list[Company], output_filename: Path) -> None:
    with open(output_filename, "w+") as f:
        writer = csv.DictWriter(
            f, fieldnames=["name", "address", "email", "phone", "url"]
        )
        writer.writeheader()
        writer.writerows(map(lambda c: c.to_dict(), companies))
    logger.info("Companies was written into %s", output_filename)


def get_companies_dump(
    api_key: str, location: str, company_query: str, radius_km: float
) -> list[Company]:
    toponym_location = get_toponym_location(api_key=api_key, query=location)
    return sorted(
        get_all_results(
            api_key=api_key,
            query=company_query,
            ll=toponym_location,  # type: ignore[arg-type]
            radius_km=radius_km,
        ),
        key=lambda x: x.name,
    )


def get_all_results(
    api_key: str, query: str, ll: tuple[float, float], radius_km: float
) -> set[Company]:
    radius_radian = km_to_ll(radius_km)
    spn = (radius_radian, radius_radian)
    skip = 0
    k = 1
    total_companies = set()
    while True:
        logger.info("Make %d request...", k)
        result = search_on_maps(
            api_key=api_key,
            query=query,
            type_="biz",
            ll=ll,
            spn=spn,
            skip=skip,
        )
        if not result.ok:
            logger.error(
                "Occurred error. Status code: %d. message: `%s`",
                result.status_code,
                result.json()["message"],
            )
            break
        data = result.json()
        total_companies.update(parse_companies(data))
        total = data["properties"]["ResponseMetaData"]["SearchResponse"]["found"]
        skip += len(data["features"])
        if skip >= total:
            break
        k += 1
    return total_companies


def get_toponym_location(api_key: str, query: str) -> tuple[float, ...]:
    logger.info("Search location coordinates")
    result = search_on_maps(api_key=api_key, query=query, type_="geo")
    if not result.ok:
        raise ValueError(f"Result is not OK. Get status code - {result.status_code}")
    return tuple(map(float, result.json()["features"][0]["geometry"]["coordinates"]))


def search_on_maps(
    api_key: str,
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
        "apikey": api_key,
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
